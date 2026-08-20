"""Provider parsing, candidate scoring, deduplication and the query-degradation ladder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import requests
import requests_mock as rm

from config.constants import (
    FALLBACK_QUERIES,
    PEXELS_SEARCH_URL,
    PIXABAY_SEARCH_URL,
    PROVIDER_PEXELS,
)
from modules.interfaces import IMediaProvider, MediaCandidate
from modules.media_cache import MediaCache
from modules.video_fetcher import (
    CompositeMediaProvider,
    PexelsVideoProvider,
    PixabayVideoProvider,
    build_query_ladder,
    score_candidate,
)
from utils.exceptions import MediaNotFoundError, MediaProviderError

PORTRAIT = (1080, 1920)


def _candidate(**overrides: Any) -> MediaCandidate:
    """Build a candidate with sensible portrait defaults."""
    fields: dict[str, Any] = {
        "provider": PROVIDER_PEXELS,
        "media_id": "1",
        "width": 1080,
        "height": 1920,
        "fps": 30.0,
        "duration": 10.0,
        "download_url": "https://example.invalid/clip.mp4",
        "author_name": "Someone",
        "author_url": "https://example.invalid/@someone",
        "page_url": "https://example.invalid/video/1",
    }
    fields.update(overrides)
    return MediaCandidate(**fields)


@pytest.fixture
def cache(tmp_path: Path) -> MediaCache:
    """A media cache rooted in the test's temporary directory."""
    return MediaCache(tmp_path / "media", timeout=1.0, max_attempts=1)


# --------------------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------------------


def test_exact_resolution_match_scores_highest() -> None:
    """A clip already at the target size beats every alternative."""
    exact = score_candidate(_candidate(width=1080, height=1920), *PORTRAIT, 4.0)
    larger = score_candidate(_candidate(width=2160, height=3840), *PORTRAIT, 4.0)
    landscape = score_candidate(_candidate(width=1920, height=1080), *PORTRAIT, 4.0)

    assert exact > larger > landscape


def test_wrong_aspect_ratio_is_penalised_below_correct_aspect() -> None:
    """Aspect ratio matters more than raw pixel count, since cropping discards the excess."""
    portrait_small = score_candidate(_candidate(width=540, height=960), *PORTRAIT, 4.0)
    landscape_hd = score_candidate(_candidate(width=1920, height=1080), *PORTRAIT, 4.0)

    assert portrait_small > landscape_hd


def test_undersized_clips_score_negative() -> None:
    """Upscaling is always visible, so undersized clips are pushed below zero."""
    assert score_candidate(_candidate(width=480, height=854), *PORTRAIT, 4.0) < 0


def test_too_short_clips_are_penalised() -> None:
    """A clip shorter than the scene needs would have to loop."""
    long_enough = score_candidate(_candidate(duration=10.0), *PORTRAIT, 4.0)
    too_short = score_candidate(_candidate(duration=1.0), *PORTRAIT, 4.0)

    assert long_enough > too_short


def test_mp4_is_preferred_over_other_containers() -> None:
    """MP4 avoids a transcode step later."""
    mp4 = score_candidate(_candidate(file_type="video/mp4"), *PORTRAIT, 4.0)
    mov = score_candidate(_candidate(file_type="video/quicktime"), *PORTRAIT, 4.0)

    assert mp4 > mov


# --------------------------------------------------------------------------------------
# Query ladder
# --------------------------------------------------------------------------------------


def test_ladder_goes_from_specific_to_generic() -> None:
    """The ladder narrows the phrase step by step, then falls back to generic terms."""
    ladder = build_query_ladder(["vintage computer machine"])

    assert ladder[0] == "vintage computer machine"
    assert ladder[1] == "vintage computer"
    assert ladder[2] == "vintage"
    assert FALLBACK_QUERIES[0] in ladder


def test_ladder_covers_every_search_term() -> None:
    """Each configured term contributes its own rungs."""
    ladder = build_query_ladder(["alpha beta gamma", "delta epsilon"])

    assert "alpha beta gamma" in ladder
    assert "delta epsilon" in ladder
    assert "delta" in ladder


def test_ladder_deduplicates_case_insensitively() -> None:
    """Repeating a term does not repeat the work."""
    ladder = build_query_ladder(["Sunset", "sunset", "SUNSET"])

    assert sum(1 for query in ladder if query.lower() == "sunset") == 1


def test_ladder_ignores_blank_terms() -> None:
    """Whitespace-only terms contribute nothing."""
    ladder = build_query_ladder(["   ", "ocean"])
    assert "ocean" in ladder
    assert "" not in ladder


def test_single_word_term_has_no_redundant_rungs() -> None:
    """A one-word query cannot be degraded further."""
    ladder = build_query_ladder(["ocean"])
    assert ladder[0] == "ocean"
    assert ladder[1] in FALLBACK_QUERIES


# --------------------------------------------------------------------------------------
# Pexels provider
# --------------------------------------------------------------------------------------


def test_pexels_requires_a_key(cache: MediaCache) -> None:
    """An empty key fails immediately with a link to the signup page."""
    with pytest.raises(MediaProviderError, match="PEXELS_API_KEY"):
        PexelsVideoProvider("   ", cache)


def test_pexels_parses_every_video_file(
    cache: MediaCache, pexels_response: dict[str, Any], requests_mock: rm.Mocker
) -> None:
    """Each video file becomes its own candidate, carrying the contributor's details."""
    requests_mock.get(PEXELS_SEARCH_URL, json=pexels_response)
    provider = PexelsVideoProvider("test-key", cache)

    candidates = provider.search("vintage computer", "portrait", 4.0, 15)

    assert len(candidates) == 4
    assert {candidate.media_id for candidate in candidates} == {"101", "202", "303"}

    hd = next(c for c in candidates if c.media_id == "101" and c.height == 1920)
    assert hd.author_name == "Ada Lovelace"
    assert hd.page_url == "https://www.pexels.com/video/portrait-clip-101/"
    assert hd.duration == 15.0


def test_pexels_sends_the_authorization_header(
    cache: MediaCache, pexels_response: dict[str, Any], requests_mock: rm.Mocker
) -> None:
    """The API key travels in the Authorization header, not a query parameter."""
    requests_mock.get(PEXELS_SEARCH_URL, json=pexels_response)
    PexelsVideoProvider("secret-key", cache).search("q", "portrait", 3.0, 5)

    request = requests_mock.last_request
    assert request is not None
    assert request.headers["Authorization"] == "secret-key"
    assert "orientation=portrait" in request.url
    assert "size=medium" in request.url


def test_pexels_401_is_not_retried(cache: MediaCache, requests_mock: rm.Mocker) -> None:
    """A bad key is a caller error, so it surfaces at once."""
    requests_mock.get(PEXELS_SEARCH_URL, status_code=401, json={"error": "unauthorized"})
    provider = PexelsVideoProvider("bad-key", cache)

    with pytest.raises(MediaProviderError, match="401"):
        provider.search("q", "portrait", 3.0, 5)

    assert requests_mock.call_count == 1


def test_pexels_429_reports_the_rate_limit(cache: MediaCache, requests_mock: rm.Mocker) -> None:
    """An exhausted rate limit explains the free tier's hourly budget."""
    requests_mock.get(PEXELS_SEARCH_URL, status_code=429, json={})
    provider = PexelsVideoProvider("key", cache, max_attempts=1)

    with pytest.raises(MediaProviderError, match="rate limit"):
        provider.search("q", "portrait", 3.0, 5)


def test_pexels_retries_server_errors(
    cache: MediaCache, pexels_response: dict[str, Any], requests_mock: rm.Mocker
) -> None:
    """A 500 is transient, so the request is retried and eventually succeeds."""
    requests_mock.get(
        PEXELS_SEARCH_URL,
        [{"status_code": 500, "json": {}}, {"status_code": 200, "json": pexels_response}],
    )
    provider = PexelsVideoProvider("key", cache, max_attempts=3)

    assert provider.search("q", "portrait", 4.0, 15)
    assert requests_mock.call_count == 2


def test_pexels_rate_limit_header_is_read(
    cache: MediaCache, pexels_response: dict[str, Any], requests_mock: rm.Mocker
) -> None:
    """A low remaining budget is surfaced rather than silently consumed."""
    requests_mock.get(
        PEXELS_SEARCH_URL,
        json=pexels_response,
        headers={"X-Ratelimit-Remaining": "3", "X-Ratelimit-Limit": "200"},
    )
    provider = PexelsVideoProvider("key", cache)

    assert provider.search("q", "portrait", 4.0, 15)


def test_pexels_malformed_payload_is_rejected(cache: MediaCache, requests_mock: rm.Mocker) -> None:
    """A response without a videos array is a provider error, not a crash."""
    requests_mock.get(PEXELS_SEARCH_URL, json={"unexpected": True})
    provider = PexelsVideoProvider("key", cache)

    with pytest.raises(MediaProviderError, match="unexpected payload"):
        provider.search("q", "portrait", 3.0, 5)


def test_pexels_skips_malformed_entries(cache: MediaCache, requests_mock: rm.Mocker) -> None:
    """Entries missing an id or dimensions are dropped without failing the search."""
    requests_mock.get(
        PEXELS_SEARCH_URL,
        json={
            "videos": [
                {"id": 1, "video_files": [{"link": "", "width": 0, "height": 0}]},
                "not-a-dict",
                {"no_id": True},
            ]
        },
    )
    assert PexelsVideoProvider("key", cache).search("q", "portrait", 3.0, 5) == []


# --------------------------------------------------------------------------------------
# Pixabay provider
# --------------------------------------------------------------------------------------


def test_pixabay_filters_by_orientation_client_side(
    cache: MediaCache, pixabay_response: dict[str, Any], requests_mock: rm.Mocker
) -> None:
    """Pixabay cannot filter orientation server-side, so mismatched streams are dropped."""
    requests_mock.get(PIXABAY_SEARCH_URL, json=pixabay_response)

    candidates = PixabayVideoProvider("key", cache).search("q", "portrait", 3.0, 10)

    assert len(candidates) == 1
    assert candidates[0].width == 1080
    assert candidates[0].height == 1920
    assert candidates[0].author_name == "PixabayUser"


def test_pixabay_requires_a_key(cache: MediaCache) -> None:
    """An empty key fails immediately."""
    with pytest.raises(MediaProviderError, match="PIXABAY_API_KEY"):
        PixabayVideoProvider("", cache)


def test_pixabay_403_is_not_retried(cache: MediaCache, requests_mock: rm.Mocker) -> None:
    """An authentication failure surfaces at once."""
    requests_mock.get(PIXABAY_SEARCH_URL, status_code=403, json={})

    with pytest.raises(MediaProviderError, match="403"):
        PixabayVideoProvider("key", cache).search("q", "portrait", 3.0, 5)

    assert requests_mock.call_count == 1


# --------------------------------------------------------------------------------------
# Composite provider
# --------------------------------------------------------------------------------------


class _StubProvider(IMediaProvider):
    """A scripted provider that answers from a query-to-candidates mapping."""

    def __init__(self, name: str, responses: dict[str, list[MediaCandidate]]) -> None:
        self._name = name
        self._responses = responses
        self.queries: list[str] = []
        self.downloads: list[str] = []

    @property
    def name(self) -> str:
        return self._name

    def search(
        self, query: str, orientation: str, min_duration: float, limit: int
    ) -> list[MediaCandidate]:
        self.queries.append(query)
        return list(self._responses.get(query, []))

    def download(self, candidate: MediaCandidate, dest: Path) -> Path:
        self.downloads.append(candidate.media_id)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b"x" * 32)
        return dest


def test_composite_requires_at_least_one_provider() -> None:
    """An empty provider list is a configuration error."""
    with pytest.raises(MediaProviderError, match="No stock footage providers"):
        CompositeMediaProvider([], target_resolution=PORTRAIT)


def test_composite_degrades_the_query_until_something_matches() -> None:
    """The ladder is walked until a rung returns results."""
    stub = _StubProvider("stub", {"vintage": [_candidate(media_id="7")]})
    composite = CompositeMediaProvider([stub], target_resolution=PORTRAIT)

    found = composite.find_best(["vintage computer machine"], "portrait", 3.0, 1)

    assert [c.media_id for c in found] == ["7"]
    assert stub.queries[:3] == ["vintage computer machine", "vintage computer", "vintage"]


def test_composite_never_reuses_a_clip() -> None:
    """A clip selected for one scene is retired for the rest of the run."""
    stub = _StubProvider("stub", {"ocean": [_candidate(media_id="1"), _candidate(media_id="2")]})
    composite = CompositeMediaProvider([stub], target_resolution=PORTRAIT)

    first = composite.find_best(["ocean"], "portrait", 3.0, 1)
    second = composite.find_best(["ocean"], "portrait", 3.0, 1)

    assert first[0].media_id != second[0].media_id


def test_composite_raises_when_nothing_matches() -> None:
    """Exhausting the whole ladder is a hard failure with an actionable hint."""
    composite = CompositeMediaProvider([_StubProvider("stub", {})], target_resolution=PORTRAIT)

    with pytest.raises(MediaNotFoundError) as info:
        composite.find_best(["nothing at all"], "portrait", 3.0, 1)

    assert info.value.hint is not None


def test_composite_returns_a_partial_result_rather_than_failing() -> None:
    """Finding fewer clips than requested is a warning, not an error."""
    stub = _StubProvider("stub", {"ocean": [_candidate(media_id="1")]})
    composite = CompositeMediaProvider([stub], target_resolution=PORTRAIT)

    found = composite.find_best(["ocean"], "portrait", 3.0, 3)

    assert len(found) == 1


def test_composite_keeps_one_file_per_source_clip() -> None:
    """Several files from one video must not crowd out other results."""
    stub = _StubProvider(
        "stub",
        {
            "ocean": [
                _candidate(media_id="1", width=1080, height=1920),
                _candidate(media_id="1", width=540, height=960),
                _candidate(media_id="2", width=1080, height=1920),
            ]
        },
    )
    composite = CompositeMediaProvider([stub], target_resolution=PORTRAIT)

    results = composite.search("ocean", "portrait", 3.0, limit=10)

    assert len(results) == 2
    assert {candidate.media_id for candidate in results} == {"1", "2"}


def test_composite_prefers_adequately_sized_clips() -> None:
    """Undersized files are rejected while any adequate option exists."""
    stub = _StubProvider(
        "stub",
        {
            "ocean": [
                _candidate(media_id="small", width=480, height=854),
                _candidate(media_id="big", width=1080, height=1920),
            ]
        },
    )
    composite = CompositeMediaProvider([stub], target_resolution=PORTRAIT)

    assert composite.search("ocean", "portrait", 3.0, limit=10)[0].media_id == "big"


def test_composite_falls_through_to_the_next_provider() -> None:
    """A failing provider does not stop the search."""

    class _Failing(_StubProvider):
        def search(
            self, query: str, orientation: str, min_duration: float, limit: int
        ) -> list[MediaCandidate]:
            raise MediaProviderError("provider is down")

    working = _StubProvider("working", {"ocean": [_candidate(media_id="9")]})
    composite = CompositeMediaProvider(
        [_Failing("broken", {}), working], target_resolution=PORTRAIT
    )

    assert composite.find_best(["ocean"], "portrait", 3.0, 1)[0].media_id == "9"


def test_composite_download_routes_to_the_owning_provider(tmp_path: Path) -> None:
    """Downloads go to whichever provider produced the candidate."""
    stub = _StubProvider(PROVIDER_PEXELS, {})
    composite = CompositeMediaProvider([stub], target_resolution=PORTRAIT)

    composite.download(_candidate(media_id="5"), tmp_path / "clip.mp4")

    assert stub.downloads == ["5"]


def test_composite_rejects_an_unknown_provider(tmp_path: Path) -> None:
    """A candidate from an unconfigured provider cannot be downloaded."""
    composite = CompositeMediaProvider(
        [_StubProvider(PROVIDER_PEXELS, {})], target_resolution=PORTRAIT
    )

    with pytest.raises(MediaProviderError, match="No configured provider"):
        composite.download(_candidate(provider="unknown"), tmp_path / "clip.mp4")


# --------------------------------------------------------------------------------------
# Media cache
# --------------------------------------------------------------------------------------


def test_download_is_atomic_and_cached(tmp_path: Path, requests_mock: rm.Mocker) -> None:
    """A completed download is reused and leaves no partial file behind."""
    url = "https://example.invalid/clip.mp4"
    payload = b"y" * 50_000
    requests_mock.get(url, content=payload, headers={"Content-Length": str(len(payload))})

    cache = MediaCache(tmp_path / "media", timeout=1.0, max_attempts=1)
    first = cache.fetch(url)

    assert first.read_bytes() == payload
    assert not list((tmp_path / "media").glob("*.part"))

    cache.fetch(url)
    assert requests_mock.call_count == 1


def test_truncated_download_is_rejected(tmp_path: Path, requests_mock: rm.Mocker) -> None:
    """A body shorter than Content-Length is discarded rather than cached."""
    from utils.exceptions import MediaDownloadError

    url = "https://example.invalid/short.mp4"
    requests_mock.get(url, content=b"z" * 100, headers={"Content-Length": "999999"})

    cache = MediaCache(tmp_path / "media", timeout=1.0, max_attempts=1)

    with pytest.raises(MediaDownloadError):
        cache.fetch(url)

    assert not list((tmp_path / "media").glob("*.mp4"))


def test_tiny_response_is_rejected_as_an_error_page(
    tmp_path: Path, requests_mock: rm.Mocker
) -> None:
    """A few bytes of HTML is not a video."""
    from utils.exceptions import MediaDownloadError

    url = "https://example.invalid/error.mp4"
    requests_mock.get(url, content=b"<html>nope</html>")

    cache = MediaCache(tmp_path / "media", timeout=1.0, max_attempts=1)

    with pytest.raises(MediaDownloadError, match="too small"):
        cache.fetch(url)


def test_cache_key_depends_only_on_the_url(tmp_path: Path) -> None:
    """The same URL always maps to the same cache entry."""
    cache = MediaCache(tmp_path / "media")

    assert cache.key_for("https://a.invalid/x.mp4") == cache.key_for("https://a.invalid/x.mp4")
    assert cache.key_for("https://a.invalid/x.mp4") != cache.key_for("https://a.invalid/y.mp4")
    assert cache.path_for("https://a.invalid/x.mp4").suffix == ".mp4"


def test_network_failure_raises_a_download_error(tmp_path: Path, requests_mock: rm.Mocker) -> None:
    """A connection error is reported as a download failure, not a raw requests exception."""
    from utils.exceptions import MediaDownloadError

    url = "https://example.invalid/gone.mp4"
    requests_mock.get(url, exc=requests.ConnectionError("no route to host"))

    cache = MediaCache(tmp_path / "media", timeout=1.0, max_attempts=2)

    with pytest.raises(MediaDownloadError):
        cache.fetch(url)
