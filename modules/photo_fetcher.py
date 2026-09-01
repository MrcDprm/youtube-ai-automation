"""Stock photo providers for the longform story format.

Shorts continues to use :mod:`modules.video_fetcher`. These classes hit the still-image
endpoints of the same vendors and the same API keys. ``min_duration`` is accepted to honour
:class:`~modules.interfaces.IMediaProvider` and then ignored: a photograph has no runtime.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import requests

from config.constants import (
    PEXELS_MAX_PER_PAGE,
    PEXELS_PHOTO_SEARCH_URL,
    PEXELS_RATELIMIT_HEADER,
    PEXELS_RATELIMIT_LIMIT_HEADER,
    PEXELS_RATELIMIT_WARN_THRESHOLD,
    PHOTO_FALLBACK_QUERIES,
    PIXABAY_MAX_PER_PAGE,
    PIXABAY_PHOTO_SEARCH_URL,
    PROVIDER_PEXELS,
    PROVIDER_PIXABAY,
    USER_AGENT,
)
from modules.interfaces import IMediaProvider, MediaCandidate
from modules.media_cache import MediaCache
from modules.video_fetcher import score_candidate
from utils.exceptions import MediaNotFoundError, MediaProviderError
from utils.logger import get_logger, log_warn
from utils.retry import make_retrying

__all__ = [
    "PexelsPhotoProvider",
    "PixabayPhotoProvider",
    "collect_unique_photos",
]

logger = get_logger(__name__)

_PIXABAY_ORIENTATION = {
    "landscape": "horizontal",
    "portrait": "vertical",
    "square": "all",
}

# Pexels `src.landscape` / `src.portrait` are social-card crops (~1200x627). Always prefer
# the full photograph so Ken Burns has enough pixels for 1920x1080.
_STILL_URL_KEYS = ("original", "large2x", "large")


def _best_still_url(src: dict[str, Any], orientation: str) -> tuple[str, str]:
    """Pick the highest-resolution still URL from a Pexels ``src`` map."""
    for key in (*_STILL_URL_KEYS, orientation):
        link = str(src.get(key) or "").strip()
        if link:
            return link, key
    return "", ""


class PexelsPhotoProvider(IMediaProvider):
    """Searches and downloads from the free Pexels Photos API."""

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
            api_key: A Pexels API key (the same key used for videos).
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
        """Search Pexels for photographs.

        Args:
            query: Search phrase, in English.
            orientation: ``portrait``, ``landscape`` or ``square``.
            min_duration: Ignored; photographs have no runtime.
            limit: Maximum number of photos to consider.

        Returns:
            One candidate per usable photo, unsorted.

        Raises:
            MediaProviderError: If the API rejects the request or returns malformed JSON.
        """
        del min_duration
        params = {
            "query": query,
            "orientation": orientation,
            "per_page": min(max(1, limit), PEXELS_MAX_PER_PAGE),
            "page": 1,
        }
        payload = self._request(PEXELS_PHOTO_SEARCH_URL, params)
        photos = payload.get("photos")
        if not isinstance(photos, list):
            raise MediaProviderError(
                f"Pexels photos returned an unexpected payload for query {query!r}.",
                hint="The API shape may have changed; check https://www.pexels.com/api/.",
            )

        candidates: list[MediaCandidate] = []
        for photo in photos:
            parsed = self._parse_photo(photo, orientation)
            if parsed is not None:
                candidates.append(parsed)
        logger.debug(
            "Pexels photos '%s' (%s): %d hit(s) -> %d candidate(s)",
            query,
            orientation,
            len(photos),
            len(candidates),
        )
        return candidates

    def download(self, candidate: MediaCandidate, dest: Path) -> Path:
        """Download a Pexels photograph.

        Args:
            candidate: The still to fetch.
            dest: Destination path in the output directory.

        Returns:
            The path to the downloaded file.
        """
        return self._cache.fetch(candidate.download_url, dest=dest)

    def _request(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        """Perform an authenticated GET under the shared retry policy."""
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
                    hint="The free tier allows 200 requests per hour. Wait, then retry.",
                ) from exc
            raise MediaProviderError(f"Pexels photo request failed: {exc}") from exc
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
        """Perform one GET and surface retryable statuses as exceptions."""
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
        """Record the remaining hourly request budget and warn when it runs low."""
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
                f"hour (limit {limit}). Further photos may fail to download."
            )

    @staticmethod
    def _parse_photo(photo: Any, orientation: str) -> MediaCandidate | None:
        """Turn one Pexels photo object into a candidate."""
        if not isinstance(photo, dict):
            return None
        media_id = str(photo.get("id", "")).strip()
        if not media_id:
            return None
        width = int(photo.get("width") or 0)
        height = int(photo.get("height") or 0)
        src = photo.get("src")
        if not isinstance(src, dict) or width <= 0 or height <= 0:
            return None
        link, preferred = _best_still_url(src, orientation)
        if not link:
            return None
        return MediaCandidate(
            provider=PROVIDER_PEXELS,
            media_id=f"photo-{media_id}",
            width=width,
            height=height,
            fps=0.0,
            duration=0.0,
            download_url=link,
            author_name=str(photo.get("photographer") or "Unknown"),
            author_url=str(photo.get("photographer_url") or ""),
            page_url=str(photo.get("url") or ""),
            file_type="image/jpeg",
            quality=preferred,
        )


class PixabayPhotoProvider(IMediaProvider):
    """Searches and downloads from the Pixabay image API."""

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
        """Search Pixabay for photographs.

        Args:
            query: Search phrase, in English.
            orientation: ``portrait``, ``landscape`` or ``square``.
            min_duration: Ignored.
            limit: Maximum number of photos to consider.

        Returns:
            One candidate per usable photo.

        Raises:
            MediaProviderError: If the API rejects the request or returns malformed JSON.
        """
        del min_duration
        params = {
            "key": self._api_key,
            "q": query,
            "image_type": "photo",
            "orientation": _PIXABAY_ORIENTATION.get(orientation, "all"),
            "per_page": min(max(3, limit), PIXABAY_MAX_PER_PAGE),
            "safesearch": "true",
        }
        payload = self._request(params)
        hits = payload.get("hits")
        if not isinstance(hits, list):
            raise MediaProviderError(
                f"Pixabay photos returned an unexpected payload for query {query!r}."
            )
        candidates: list[MediaCandidate] = []
        for hit in hits:
            parsed = self._parse_hit(hit)
            if parsed is not None:
                candidates.append(parsed)
        return candidates

    def download(self, candidate: MediaCandidate, dest: Path) -> Path:
        """Download a Pixabay photograph."""
        return self._cache.fetch(candidate.download_url, dest=dest)

    def _request(self, params: dict[str, Any]) -> dict[str, Any]:
        """Perform a GET under the shared retry policy."""
        controller = make_retrying(max_attempts=self._max_attempts)
        try:
            response = controller(self._get_once, params)
        except requests.HTTPError as exc:
            raise MediaProviderError(f"Pixabay photo request failed: {exc}") from exc
        except requests.RequestException as exc:
            raise MediaProviderError(
                f"Could not reach Pixabay after {self._max_attempts} attempts: {exc}",
                hint="Check your internet connection.",
            ) from exc
        try:
            payload = response.json()
        except ValueError as exc:
            raise MediaProviderError(f"Pixabay returned invalid JSON: {exc}") from exc
        if not isinstance(payload, dict):
            raise MediaProviderError("Pixabay returned a non-object JSON payload.")
        return payload

    def _get_once(self, params: dict[str, Any]) -> requests.Response:
        """Perform one GET and surface retryable statuses as exceptions."""
        response = self._session.get(
            PIXABAY_PHOTO_SEARCH_URL, params=params, timeout=self._timeout
        )
        response.raise_for_status()
        return response

    @staticmethod
    def _parse_hit(hit: Any) -> MediaCandidate | None:
        """Turn one Pixabay image hit into a candidate."""
        if not isinstance(hit, dict):
            return None
        media_id = str(hit.get("id", "")).strip()
        link = str(hit.get("largeImageURL") or hit.get("webformatURL") or "").strip()
        width = int(hit.get("imageWidth") or hit.get("webformatWidth") or 0)
        height = int(hit.get("imageHeight") or hit.get("webformatHeight") or 0)
        if not media_id or not link or width <= 0 or height <= 0:
            return None
        user = str(hit.get("user") or "Unknown")
        page = str(hit.get("pageURL") or "")
        return MediaCandidate(
            provider=PROVIDER_PIXABAY,
            media_id=f"photo-{media_id}",
            width=width,
            height=height,
            fps=0.0,
            duration=0.0,
            download_url=link,
            author_name=user,
            author_url="",
            page_url=page,
            file_type="image/jpeg",
            quality="large",
        )


def collect_unique_photos(
    provider: IMediaProvider,
    queries: list[str],
    orientation: str,
    needed: int,
    target_resolution: tuple[int, int],
) -> list[MediaCandidate]:
    """Gather ``needed`` distinct stills, trying specific queries then fallbacks.

    Early queries fill the opening band; later queries fill the body. Duplicates (same
    provider id) are skipped.

    Args:
        provider: Any :class:`~modules.interfaces.IMediaProvider`, typically a composite of
            photo providers.
        queries: English search phrases, most specific first.
        orientation: Desired frame orientation.
        needed: How many unique photos to return.
        target_resolution: Output size, used to rank candidates.

    Returns:
        Up to ``needed`` candidates, best-first within each query.

    Raises:
        MediaNotFoundError: If fewer than ``needed`` unique photos could be found.
    """
    if needed < 1:
        return []

    width, height = target_resolution
    used: set[str] = set()
    chosen: list[MediaCandidate] = []
    ladder = [term.strip() for term in queries if term.strip()]
    for fallback in PHOTO_FALLBACK_QUERIES:
        if fallback not in ladder:
            ladder.append(fallback)

    for query in ladder:
        if len(chosen) >= needed:
            break
        try:
            found = provider.search(query, orientation, 0.0, max(needed * 2, 15))
        except MediaProviderError as exc:
            log_warn(f"Photo search {query!r} failed: {exc}")
            continue
        ranked = sorted(
            found,
            key=lambda candidate: score_candidate(candidate, width, height, 0.0),
            reverse=True,
        )
        for candidate in ranked:
            if candidate.dedup_key in used:
                continue
            used.add(candidate.dedup_key)
            chosen.append(candidate)
            if len(chosen) >= needed:
                break

    if len(chosen) < needed:
        raise MediaNotFoundError(
            f"Needed {needed} unique stills but only found {len(chosen)}.",
            hint="Broaden scene search_terms, or add PIXABAY_API_KEY as a photo fallback.",
        )
    return chosen[:needed]
