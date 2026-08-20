"""Stock footage providers: Pexels, Pixabay and a composite that degrades gracefully.

Search results are ranked rather than taken in API order. A stock query returns clips at wildly
different resolutions and aspect ratios, and picking the first one routinely yields a landscape
480p file that has to be upscaled into a portrait frame. The scoring below prefers clips that
already match the target geometry, so the editor's crop discards as few pixels as possible.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import requests

from config.constants import (
    FALLBACK_QUERIES,
    PEXELS_MAX_PER_PAGE,
    PEXELS_RATELIMIT_HEADER,
    PEXELS_RATELIMIT_LIMIT_HEADER,
    PEXELS_RATELIMIT_WARN_THRESHOLD,
    PEXELS_SEARCH_URL,
    PIXABAY_MAX_PER_PAGE,
    PIXABAY_SEARCH_URL,
    PROVIDER_PEXELS,
    PROVIDER_PIXABAY,
    USER_AGENT,
)
from modules.interfaces import IMediaProvider, MediaCandidate
from modules.media_cache import MediaCache
from utils.exceptions import MediaNotFoundError, MediaProviderError
from utils.logger import get_logger, log_warn
from utils.media import classify_orientation
from utils.retry import make_retrying

__all__ = [
    "CompositeMediaProvider",
    "PexelsVideoProvider",
    "PixabayVideoProvider",
    "build_query_ladder",
    "score_candidate",
]

logger = get_logger(__name__)


# --------------------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------------------


def score_candidate(
    candidate: MediaCandidate,
    target_width: int,
    target_height: int,
    min_duration: float,
) -> float:
    """Rank a candidate against the target frame.

    Higher is better. The weights encode a simple priority order: an exact resolution match
    beats a matching aspect ratio, which beats raw resolution, which beats format and length
    preferences.

    Args:
        candidate: The clip to score.
        target_width: Desired output width in pixels.
        target_height: Desired output height in pixels.
        min_duration: Shortest acceptable clip length in seconds.

    Returns:
        A score. Candidates too small for the target frame score negatively and are filtered
        out by the caller.
    """
    score = 0.0

    if candidate.width == target_width and candidate.height == target_height:
        score += 1000.0

    target_aspect = target_width / target_height
    if candidate.aspect > 0:
        aspect_error = abs(candidate.aspect - target_aspect) / target_aspect
        score += max(0.0, 300.0 * (1.0 - min(aspect_error, 1.0)))
        if aspect_error <= 0.02:
            score += 200.0

    if candidate.height < target_height or candidate.width < target_width:
        # Upscaling a stock clip is always visible; push these below every adequate option.
        shortfall = max(
            (target_height - candidate.height) / target_height,
            (target_width - candidate.width) / target_width,
        )
        score -= 500.0 * (1.0 + shortfall)
    else:
        # Prefer headroom, but not absurd 8K files that cost minutes to decode.
        overshoot = candidate.pixels / max(1, target_width * target_height)
        score += 120.0 if overshoot <= 4.0 else 40.0

    if candidate.file_type.lower() == "video/mp4":
        score += 80.0

    if candidate.duration >= min_duration:
        score += 60.0
        if candidate.duration >= min_duration * 2:
            score += 20.0
    else:
        score -= 200.0 * (1.0 - candidate.duration / max(min_duration, 0.1))

    if 24.0 <= candidate.fps <= 60.0:
        score += 25.0

    return score


def build_query_ladder(terms: list[str]) -> list[str]:
    """Build the progressively broader queries to try before giving up.

    Stock libraries return nothing for an over-specific phrase such as
    ``"vintage computer machine close up"``, but plenty for ``"vintage computer"``. The ladder
    walks from most to least specific and ends on generic terms that always match.

    Args:
        terms: The scene's search terms, most specific first.

    Returns:
        Deduplicated queries in the order they should be attempted.
    """
    ladder: list[str] = []

    for term in terms:
        cleaned = " ".join(term.split())
        if not cleaned:
            continue
        words = cleaned.split()
        ladder.append(cleaned)
        if len(words) > 2:
            ladder.append(" ".join(words[:2]))
        if len(words) > 1:
            ladder.append(words[0])

    ladder.extend(FALLBACK_QUERIES)

    seen: set[str] = set()
    unique: list[str] = []
    for query in ladder:
        lowered = query.lower()
        if lowered not in seen:
            seen.add(lowered)
            unique.append(query)
    return unique


# --------------------------------------------------------------------------------------
# Pexels
# --------------------------------------------------------------------------------------


class PexelsVideoProvider(IMediaProvider):
    """Searches and downloads from the free Pexels Videos API."""

    def __init__(
        self,
        api_key: str,
        cache: MediaCache,
        *,
        timeout: float = 30.0,
        max_attempts: int = 4,
        session: requests.Session | None = None,
    ) -> None:
        """Initialise the provider.

        Args:
            api_key: A Pexels API key.
            cache: Shared media cache used for downloads.
            timeout: Per-request timeout in seconds.
            max_attempts: Total attempts per request including the first.
            session: Optional shared HTTP session.

        Raises:
            MediaProviderError: If ``api_key`` is empty.
        """
        if not api_key.strip():
            raise MediaProviderError(
                "PEXELS_API_KEY is empty.",
                hint="Get a free key at https://www.pexels.com/api/ and set it in .env.",
            )
        self._api_key = api_key.strip()
        self._cache = cache
        self._timeout = timeout
        self._max_attempts = max_attempts
        self._session = session or requests.Session()
        self._session.headers.update({"User-Agent": USER_AGENT})
        self._rate_limit_warned = False

    @property
    def name(self) -> str:
        """The provider's short name."""
        return PROVIDER_PEXELS

    def search(
        self,
        query: str,
        orientation: str,
        min_duration: float,
        limit: int,
    ) -> list[MediaCandidate]:
        """Search Pexels for videos.

        Args:
            query: Search phrase, in English.
            orientation: ``portrait``, ``landscape`` or ``square``.
            min_duration: Shortest acceptable clip length in seconds.
            limit: Maximum number of source videos to consider.

        Returns:
            One candidate per usable video file, unsorted.

        Raises:
            MediaProviderError: If the API rejects the request or returns malformed JSON.
        """
        params = {
            "query": query,
            "orientation": orientation,
            "size": "medium",
            "per_page": min(max(1, limit), PEXELS_MAX_PER_PAGE),
            "page": 1,
        }
        payload = self._request(PEXELS_SEARCH_URL, params)
        videos = payload.get("videos")
        if not isinstance(videos, list):
            raise MediaProviderError(
                f"Pexels returned an unexpected payload for query {query!r}.",
                hint="The API shape may have changed; check https://www.pexels.com/api/.",
            )

        candidates: list[MediaCandidate] = []
        for video in videos:
            candidates.extend(self._parse_video(video, min_duration))
        logger.debug(
            "Pexels '%s' (%s): %d video(s) -> %d candidate file(s)",
            query,
            orientation,
            len(videos),
            len(candidates),
        )
        return candidates

    def download(self, candidate: MediaCandidate, dest: Path) -> Path:
        """Download a Pexels clip.

        Args:
            candidate: The clip to fetch.
            dest: Destination path in the output directory.

        Returns:
            The path to the downloaded file.

        Raises:
            MediaDownloadError: If the download fails.
        """
        return self._cache.fetch(candidate.download_url, dest=dest)

    # -- Internals ------------------------------------------------------------------------

    def _request(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        """Perform an authenticated GET under the shared retry policy.

        Args:
            url: The endpoint.
            params: Query parameters.

        Returns:
            The decoded JSON body.

        Raises:
            MediaProviderError: On authentication failure, exhausted retries or bad JSON.
        """
        controller = make_retrying(max_attempts=self._max_attempts)
        try:
            response = controller(self._get_once, url, params)
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else 0
            if status == 401:
                raise MediaProviderError(
                    "Pexels rejected the API key (HTTP 401).",
                    hint="Check PEXELS_API_KEY in .env against https://www.pexels.com/api/.",
                ) from exc
            if status == 429:
                raise MediaProviderError(
                    "Pexels rate limit exhausted (HTTP 429).",
                    hint=(
                        "The free tier allows 200 requests per hour. Wait for the window to "
                        "reset, or re-run later; downloaded clips are cached."
                    ),
                ) from exc
            raise MediaProviderError(f"Pexels request failed: {exc}") from exc
        except requests.RequestException as exc:
            raise MediaProviderError(
                f"Could not reach Pexels after {self._max_attempts} attempts: {exc}",
                hint="Check your internet connection.",
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise MediaProviderError(f"Pexels returned invalid JSON: {exc}") from exc
        if not isinstance(payload, dict):
            raise MediaProviderError("Pexels returned a non-object JSON payload.")
        return payload

    def _get_once(self, url: str, params: dict[str, Any]) -> requests.Response:
        """Perform one GET and surface retryable statuses as exceptions.

        Args:
            url: The endpoint.
            params: Query parameters.

        Returns:
            The successful response.

        Raises:
            requests.HTTPError: On any non-success status.
        """
        response = self._session.get(
            url,
            params=params,
            headers={"Authorization": self._api_key},
            timeout=self._timeout,
        )
        self._log_rate_limit(response)
        response.raise_for_status()
        return response

    def _log_rate_limit(self, response: requests.Response) -> None:
        """Record the remaining hourly request budget and warn when it runs low.

        Args:
            response: The response whose headers to inspect.
        """
        raw_remaining = response.headers.get(PEXELS_RATELIMIT_HEADER)
        if raw_remaining is None:
            return
        try:
            remaining = int(raw_remaining)
        except ValueError:
            return

        limit = response.headers.get(PEXELS_RATELIMIT_LIMIT_HEADER, "?")
        logger.debug("Pexels rate limit: %s of %s requests remaining", remaining, limit)

        if remaining <= PEXELS_RATELIMIT_WARN_THRESHOLD and not self._rate_limit_warned:
            self._rate_limit_warned = True
            log_warn(
                f"Pexels rate limit nearly exhausted: only {remaining} request(s) left this "
                f"hour (limit {limit}). Further scenes may fail to find footage."
            )

    def _parse_video(self, video: Any, min_duration: float) -> list[MediaCandidate]:
        """Turn one Pexels video object into candidates, one per video file.

        Args:
            video: A ``videos[]`` entry from the API response.
            min_duration: Shortest acceptable clip length, recorded on each candidate.

        Returns:
            Candidates for every MP4 file the video offers, possibly empty.
        """
        if not isinstance(video, dict):
            return []

        media_id = str(video.get("id", "")).strip()
        if not media_id:
            return []

        duration = float(video.get("duration", 0) or 0)
        page_url = str(video.get("url", ""))
        user = video.get("user") or {}
        author_name = str(user.get("name", "Unknown")) if isinstance(user, dict) else "Unknown"
        author_url = str(user.get("url", "")) if isinstance(user, dict) else ""

        files = video.get("video_files")
        if not isinstance(files, list):
            return []

        candidates: list[MediaCandidate] = []
        for entry in files:
            if not isinstance(entry, dict):
                continue
            link = str(entry.get("link", "")).strip()
            width = int(entry.get("width") or 0)
            height = int(entry.get("height") or 0)
            if not link or width <= 0 or height <= 0:
                continue
            candidates.append(
                MediaCandidate(
                    provider=PROVIDER_PEXELS,
                    media_id=media_id,
                    width=width,
                    height=height,
                    fps=float(entry.get("fps") or 0.0),
                    duration=duration if duration > 0 else min_duration,
                    download_url=link,
                    author_name=author_name,
                    author_url=author_url,
                    page_url=page_url,
                    file_type=str(entry.get("file_type", "video/mp4")),
                    quality=str(entry.get("quality", "")),
                )
            )
        return candidates


# --------------------------------------------------------------------------------------
# Pixabay
# --------------------------------------------------------------------------------------


class PixabayVideoProvider(IMediaProvider):
    """Searches and downloads from the Pixabay video API.

    Pixabay does not accept an orientation filter, so orientation is applied client-side after
    the results come back.
    """

    _STREAM_PREFERENCE = ("large", "medium", "small", "tiny")

    def __init__(
        self,
        api_key: str,
        cache: MediaCache,
        *,
        timeout: float = 30.0,
        max_attempts: int = 4,
        session: requests.Session | None = None,
    ) -> None:
        """Initialise the provider.

        Args:
            api_key: A Pixabay API key.
            cache: Shared media cache used for downloads.
            timeout: Per-request timeout in seconds.
            max_attempts: Total attempts per request including the first.
            session: Optional shared HTTP session.

        Raises:
            MediaProviderError: If ``api_key`` is empty.
        """
        if not api_key.strip():
            raise MediaProviderError(
                "PIXABAY_API_KEY is empty.",
                hint="Get a free key at https://pixabay.com/api/docs/ and set it in .env.",
            )
        self._api_key = api_key.strip()
        self._cache = cache
        self._timeout = timeout
        self._max_attempts = max_attempts
        self._session = session or requests.Session()
        self._session.headers.update({"User-Agent": USER_AGENT})

    @property
    def name(self) -> str:
        """The provider's short name."""
        return PROVIDER_PIXABAY

    def search(
        self,
        query: str,
        orientation: str,
        min_duration: float,
        limit: int,
    ) -> list[MediaCandidate]:
        """Search Pixabay for videos.

        Args:
            query: Search phrase, in English.
            orientation: Desired orientation, applied client-side.
            min_duration: Shortest acceptable clip length in seconds.
            limit: Maximum number of source videos to consider.

        Returns:
            One candidate per usable video stream, unsorted.

        Raises:
            MediaProviderError: If the API rejects the request or returns malformed JSON.
        """
        params = {
            "key": self._api_key,
            "q": query,
            "per_page": min(max(3, limit), PIXABAY_MAX_PER_PAGE),
            "video_type": "all",
            "safesearch": "true",
        }
        payload = self._request(PIXABAY_SEARCH_URL, params)
        hits = payload.get("hits")
        if not isinstance(hits, list):
            raise MediaProviderError(f"Pixabay returned an unexpected payload for query {query!r}.")

        candidates: list[MediaCandidate] = []
        for hit in hits:
            candidates.extend(self._parse_hit(hit, min_duration, orientation))
        logger.debug(
            "Pixabay '%s': %d hit(s) -> %d candidate file(s)", query, len(hits), len(candidates)
        )
        return candidates

    def download(self, candidate: MediaCandidate, dest: Path) -> Path:
        """Download a Pixabay clip.

        Args:
            candidate: The clip to fetch.
            dest: Destination path in the output directory.

        Returns:
            The path to the downloaded file.

        Raises:
            MediaDownloadError: If the download fails.
        """
        return self._cache.fetch(candidate.download_url, dest=dest)

    # -- Internals ------------------------------------------------------------------------

    def _request(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        """Perform a GET under the shared retry policy.

        Args:
            url: The endpoint.
            params: Query parameters, including the API key.

        Returns:
            The decoded JSON body.

        Raises:
            MediaProviderError: On authentication failure, exhausted retries or bad JSON.
        """
        controller = make_retrying(max_attempts=self._max_attempts)
        try:
            response = controller(self._get_once, url, params)
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else 0
            if status in {400, 401, 403}:
                raise MediaProviderError(
                    f"Pixabay rejected the request (HTTP {status}).",
                    hint="Check PIXABAY_API_KEY in .env against https://pixabay.com/api/docs/.",
                ) from exc
            raise MediaProviderError(f"Pixabay request failed: {exc}") from exc
        except requests.RequestException as exc:
            raise MediaProviderError(
                f"Could not reach Pixabay after {self._max_attempts} attempts: {exc}"
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise MediaProviderError(f"Pixabay returned invalid JSON: {exc}") from exc
        if not isinstance(payload, dict):
            raise MediaProviderError("Pixabay returned a non-object JSON payload.")
        return payload

    def _get_once(self, url: str, params: dict[str, Any]) -> requests.Response:
        """Perform one GET and surface retryable statuses as exceptions.

        Args:
            url: The endpoint.
            params: Query parameters.

        Returns:
            The successful response.

        Raises:
            requests.HTTPError: On any non-success status.
        """
        response = self._session.get(url, params=params, timeout=self._timeout)
        response.raise_for_status()
        return response

    def _parse_hit(self, hit: Any, min_duration: float, orientation: str) -> list[MediaCandidate]:
        """Turn one Pixabay hit into candidates, one per available stream size.

        Args:
            hit: A ``hits[]`` entry from the API response.
            min_duration: Shortest acceptable clip length, recorded on each candidate.
            orientation: Desired orientation; mismatched streams are dropped here because the
                API cannot filter them server-side.

        Returns:
            Candidates for each usable stream, possibly empty.
        """
        if not isinstance(hit, dict):
            return []

        media_id = str(hit.get("id", "")).strip()
        videos = hit.get("videos")
        if not media_id or not isinstance(videos, dict):
            return []

        duration = float(hit.get("duration", 0) or 0)
        page_url = str(hit.get("pageURL", ""))
        author_name = str(hit.get("user", "Unknown"))
        author_id = hit.get("user_id")
        author_url = (
            f"https://pixabay.com/users/{author_id}/" if author_id else "https://pixabay.com/"
        )

        candidates: list[MediaCandidate] = []
        for quality in self._STREAM_PREFERENCE:
            stream = videos.get(quality)
            if not isinstance(stream, dict):
                continue
            link = str(stream.get("url", "")).strip()
            width = int(stream.get("width") or 0)
            height = int(stream.get("height") or 0)
            if not link or width <= 0 or height <= 0:
                continue
            if classify_orientation(width, height) != orientation:
                continue
            candidates.append(
                MediaCandidate(
                    provider=PROVIDER_PIXABAY,
                    media_id=media_id,
                    width=width,
                    height=height,
                    fps=0.0,
                    duration=duration if duration > 0 else min_duration,
                    download_url=link,
                    author_name=author_name,
                    author_url=author_url,
                    page_url=page_url,
                    file_type="video/mp4",
                    quality=quality,
                )
            )
        return candidates


# --------------------------------------------------------------------------------------
# Composite
# --------------------------------------------------------------------------------------


class CompositeMediaProvider(IMediaProvider):
    """Tries several providers and progressively broader queries before giving up.

    Also enforces run-wide deduplication: once a clip has been selected for any scene, its id
    is retired so the same footage never appears twice in one video.
    """

    def __init__(
        self,
        providers: list[IMediaProvider],
        *,
        target_resolution: tuple[int, int],
        search_limit: int = 15,
    ) -> None:
        """Initialise the composite.

        Args:
            providers: Providers to try, in priority order.
            target_resolution: Output frame size, used to score candidates.
            search_limit: Results requested per provider query.

        Raises:
            MediaProviderError: If no providers were supplied.
        """
        if not providers:
            raise MediaProviderError(
                "No stock footage providers are configured.",
                hint=(
                    "Set PEXELS_API_KEY (or PIXABAY_API_KEY) in .env, or give every scene a "
                    "local_media path."
                ),
            )
        self._providers = providers
        self._target_resolution = target_resolution
        self._search_limit = search_limit
        self._used_ids: set[str] = set()

    @property
    def name(self) -> str:
        """A composite name listing the wrapped providers."""
        return "+".join(provider.name for provider in self._providers)

    @property
    def used_ids(self) -> frozenset[str]:
        """Clip identities already consumed by this run."""
        return frozenset(self._used_ids)

    def reserve(self, candidate: MediaCandidate) -> None:
        """Mark a candidate as used so it is never selected again.

        Args:
            candidate: The clip that was chosen.
        """
        self._used_ids.add(candidate.dedup_key)

    def release_all(self) -> None:
        """Forget every reservation, allowing clips to be reused."""
        self._used_ids.clear()

    def search(
        self,
        query: str,
        orientation: str,
        min_duration: float,
        limit: int,
    ) -> list[MediaCandidate]:
        """Search every provider for a single query, best candidates first.

        Args:
            query: Search phrase.
            orientation: Desired orientation.
            min_duration: Shortest acceptable clip length in seconds.
            limit: Maximum number of candidates to return.

        Returns:
            Scored, deduplicated candidates, possibly empty.
        """
        target_width, target_height = self._target_resolution
        collected: list[MediaCandidate] = []

        for provider in self._providers:
            try:
                found = provider.search(query, orientation, min_duration, self._search_limit)
            except MediaProviderError as exc:
                logger.warning("Provider %s failed for '%s': %s", provider.name, query, exc)
                continue
            collected.extend(found)

        return self._rank(collected, target_width, target_height, min_duration)[:limit]

    def find_best(
        self,
        search_terms: list[str],
        orientation: str,
        min_duration: float,
        count: int,
    ) -> list[MediaCandidate]:
        """Find distinct clips for one scene, degrading the query until something matches.

        Args:
            search_terms: The scene's search terms, most specific first.
            orientation: Desired orientation.
            min_duration: Shortest acceptable clip length in seconds.
            count: How many distinct clips the scene needs.

        Returns:
            Exactly ``count`` candidates when possible, or as many as could be found.

        Raises:
            MediaNotFoundError: If no provider yielded a usable clip for any query.
        """
        selected: list[MediaCandidate] = []
        attempted: list[str] = []

        for query in build_query_ladder(search_terms):
            attempted.append(query)
            candidates = self.search(query, orientation, min_duration, limit=self._search_limit)

            for candidate in candidates:
                if candidate.dedup_key in self._used_ids:
                    continue
                if any(candidate.media_id == chosen.media_id for chosen in selected):
                    continue
                selected.append(candidate)
                self.reserve(candidate)
                if len(selected) >= count:
                    break

            if len(selected) >= count:
                if len(attempted) > 1:
                    logger.info("Query degraded to '%s' after %d attempt(s)", query, len(attempted))
                return selected

        if selected:
            log_warn(
                f"Only found {len(selected)} of {count} requested clip(s) for "
                f"{search_terms[0]!r}; the scene will reuse what is available."
            )
            return selected

        raise MediaNotFoundError(
            f"No stock footage found for {search_terms!r} in {orientation} orientation "
            f"after trying {len(attempted)} query variation(s).",
            hint=(
                "Try broader, English-language search_terms, set a local_media path for this "
                "scene, or lower min_clip_duration."
            ),
        )

    def download(self, candidate: MediaCandidate, dest: Path) -> Path:
        """Download a candidate using the provider that produced it.

        Args:
            candidate: The clip to fetch.
            dest: Destination path.

        Returns:
            The path to the downloaded file.

        Raises:
            MediaProviderError: If no configured provider owns the candidate.
        """
        for provider in self._providers:
            if provider.name == candidate.provider:
                return provider.download(candidate, dest)
        raise MediaProviderError(
            f"No configured provider can download a {candidate.provider} clip."
        )

    def _rank(
        self,
        candidates: list[MediaCandidate],
        target_width: int,
        target_height: int,
        min_duration: float,
    ) -> list[MediaCandidate]:
        """Score, filter and order candidates, keeping the best file per source clip.

        A single Pexels video yields several files at different resolutions. Keeping only the
        highest-scoring file per ``media_id`` stops one popular clip from crowding out the
        whole result set.

        Args:
            candidates: Raw candidates from every provider.
            target_width: Desired output width.
            target_height: Desired output height.
            min_duration: Shortest acceptable clip length.

        Returns:
            Candidates ordered best-first. Files smaller than the target frame are rejected
            outright whenever any adequately sized option exists, and only fall back into the
            list when they are all that is available.
        """
        best_per_media: dict[str, tuple[float, MediaCandidate]] = {}

        for candidate in candidates:
            if candidate.dedup_key in self._used_ids:
                continue
            score = score_candidate(candidate, target_width, target_height, min_duration)
            existing = best_per_media.get(candidate.dedup_key)
            if existing is None or score > existing[0]:
                best_per_media[candidate.dedup_key] = (score, candidate)

        adequate: list[tuple[float, MediaCandidate]] = []
        undersized: list[tuple[float, MediaCandidate]] = []
        for score, candidate in best_per_media.values():
            fits = candidate.width >= target_width and candidate.height >= target_height
            (adequate if fits else undersized).append((score, candidate))

        if adequate and undersized:
            logger.debug(
                "Rejected %d clip(s) smaller than %dx%d",
                len(undersized),
                target_width,
                target_height,
            )

        ordered = sorted(adequate, key=lambda pair: pair[0], reverse=True)
        ordered += sorted(undersized, key=lambda pair: pair[0], reverse=True)
        return [candidate for _, candidate in ordered]
