"""Content-addressed cache and resilient downloader for stock media.

Downloads are keyed by a SHA-256 of their URL, so the same clip fetched for two scenes, or
across two runs, costs one request. Every write is atomic: bytes land in a sibling ``.part``
file that is renamed into place only after the transfer completes and its length has been
verified. A crash mid-download therefore leaves no truncated file that a later run would
mistake for a cache hit.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable
from pathlib import Path
from urllib.parse import urlparse

import requests

from config.constants import DOWNLOAD_CHUNK_SIZE, USER_AGENT
from utils.exceptions import MediaDownloadError
from utils.fs import ensure_parent, format_bytes, hash_payload
from utils.logger import get_logger
from utils.retry import make_retrying

__all__ = ["MediaCache"]

logger = get_logger(__name__)

ProgressCallback = Callable[[int, int | None], None]
"""Receives ``(bytes_downloaded, total_bytes_or_None)`` as a transfer proceeds."""

MIN_PLAUSIBLE_VIDEO_BYTES = 10_240
"""A stock clip smaller than this is an error page, not a video."""

_CONTENT_TYPE_SUFFIXES = {
    "video/mp4": ".mp4",
    "video/quicktime": ".mov",
    "video/webm": ".webm",
    "video/x-matroska": ".mkv",
}


class MediaCache:
    """Downloads media files once and reuses them forever."""

    def __init__(
        self,
        cache_dir: Path,
        *,
        timeout: float = 30.0,
        max_attempts: int = 4,
        force: bool = False,
        session: requests.Session | None = None,
    ) -> None:
        """Initialise the cache.

        Args:
            cache_dir: Directory holding cached media.
            timeout: Per-request timeout in seconds.
            max_attempts: Total download attempts including the first.
            force: When true, re-download even on a cache hit.
            session: Optional shared :class:`requests.Session`. One is created when omitted.
        """
        self._cache_dir = cache_dir
        self._timeout = timeout
        self._max_attempts = max_attempts
        self._force = force
        self._session = session or requests.Session()
        self._session.headers.setdefault("User-Agent", USER_AGENT)
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    # -- Paths --------------------------------------------------------------------------

    def key_for(self, url: str) -> str:
        """Compute the cache key for a URL.

        Args:
            url: The media URL.

        Returns:
            A 64-character hex digest.
        """
        return hash_payload("media-v1", url)

    def path_for(self, url: str, *, suffix: str | None = None) -> Path:
        """Return the cache path a URL maps to.

        Args:
            url: The media URL.
            suffix: File extension to use. Inferred from the URL when omitted.

        Returns:
            The cache file path, which may not exist yet.
        """
        extension = suffix or self._suffix_from_url(url)
        return self._cache_dir / f"{self.key_for(url)}{extension}"

    @staticmethod
    def _suffix_from_url(url: str) -> str:
        """Infer a file extension from a URL path.

        Args:
            url: The media URL.

        Returns:
            An extension including the leading dot, defaulting to ``.mp4``.
        """
        path = urlparse(url).path
        suffix = Path(path).suffix.lower()
        if suffix and len(suffix) <= 5 and suffix.isascii():
            return suffix
        return ".mp4"

    def is_cached(self, url: str, *, suffix: str | None = None) -> bool:
        """Report whether a URL is already downloaded and plausibly intact.

        Args:
            url: The media URL.
            suffix: File extension override.

        Returns:
            ``True`` when a cached file exists and is large enough to be real media.
        """
        path = self.path_for(url, suffix=suffix)
        return path.is_file() and path.stat().st_size >= MIN_PLAUSIBLE_VIDEO_BYTES

    # -- Download ------------------------------------------------------------------------

    def fetch(
        self,
        url: str,
        *,
        dest: Path | None = None,
        headers: dict[str, str] | None = None,
        on_progress: ProgressCallback | None = None,
        minimum_bytes: int = MIN_PLAUSIBLE_VIDEO_BYTES,
    ) -> Path:
        """Download a URL, or return the cached copy.

        Args:
            url: The media URL.
            dest: Optional path to also place the file at. The cache copy is the source of
                truth; this is a convenience copy for human-browsable output directories.
            headers: Extra request headers.
            on_progress: Called with ``(downloaded, total)`` as bytes arrive.
            minimum_bytes: Smallest acceptable file size.

        Returns:
            The path to the cached file, or to ``dest`` when one was requested.

        Raises:
            MediaDownloadError: If the download fails, is truncated, or is too small.
        """
        cache_path = self.path_for(url)

        if self._force or not self.is_cached(url):
            self._download(url, cache_path, headers=headers, on_progress=on_progress)
            self._verify(cache_path, minimum_bytes)
        else:
            logger.debug(
                "Media cache hit %s (%s)",
                cache_path.name,
                format_bytes(cache_path.stat().st_size),
            )
            if on_progress is not None:
                size = cache_path.stat().st_size
                on_progress(size, size)

        if dest is None:
            return cache_path
        return self._materialize(cache_path, dest)

    def _download(
        self,
        url: str,
        cache_path: Path,
        *,
        headers: dict[str, str] | None,
        on_progress: ProgressCallback | None,
    ) -> None:
        """Fetch a URL into the cache under the shared retry policy.

        Args:
            url: The media URL.
            cache_path: Destination inside the cache.
            headers: Extra request headers.
            on_progress: Progress callback.

        Raises:
            MediaDownloadError: If every attempt fails.
        """
        controller = make_retrying(max_attempts=self._max_attempts)
        try:
            controller(self._download_once, url, cache_path, headers, on_progress)
        except requests.RequestException as exc:
            raise MediaDownloadError(
                f"Could not download media after {self._max_attempts} attempts: {exc}",
                hint="Check your internet connection, then re-run. Completed work is cached.",
            ) from exc

    def _download_once(
        self,
        url: str,
        cache_path: Path,
        headers: dict[str, str] | None,
        on_progress: ProgressCallback | None,
    ) -> None:
        """Perform a single streaming download attempt.

        Args:
            url: The media URL.
            cache_path: Destination inside the cache.
            headers: Extra request headers.
            on_progress: Progress callback.

        Raises:
            requests.HTTPError: On a non-success status, so the retry policy can classify it.
            MediaDownloadError: If the transfer ends short of the advertised length.
        """
        ensure_parent(cache_path)
        part_path = cache_path.with_suffix(cache_path.suffix + ".part")
        part_path.unlink(missing_ok=True)

        response = self._session.get(
            url,
            stream=True,
            timeout=self._timeout,
            headers=headers,
            allow_redirects=True,
        )
        try:
            response.raise_for_status()

            declared = response.headers.get("Content-Length")
            total = int(declared) if declared and declared.isdigit() else None
            written = 0

            with part_path.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                    if not chunk:
                        continue
                    handle.write(chunk)
                    written += len(chunk)
                    if on_progress is not None:
                        on_progress(written, total)

            if total is not None and written != total:
                part_path.unlink(missing_ok=True)
                raise MediaDownloadError(
                    f"Truncated download: received {format_bytes(written)} of "
                    f"{format_bytes(total)}.",
                    hint="The connection dropped mid-transfer. Re-run to resume.",
                )

            part_path.replace(cache_path)
            logger.debug("Downloaded %s (%s)", cache_path.name, format_bytes(written))
        finally:
            response.close()
            with contextlib.suppress(OSError):
                part_path.unlink(missing_ok=True)

    @staticmethod
    def _verify(path: Path, minimum_bytes: int) -> None:
        """Reject a downloaded file that is too small to be real media.

        Args:
            path: The downloaded file.
            minimum_bytes: Smallest acceptable size.

        Raises:
            MediaDownloadError: If the file is missing or undersized.
        """
        if not path.is_file():
            raise MediaDownloadError(f"Download produced no file at {path}.")
        size = path.stat().st_size
        if size < minimum_bytes:
            path.unlink(missing_ok=True)
            raise MediaDownloadError(
                f"Downloaded file is only {format_bytes(size)}, which is too small to be a "
                "usable video.",
                hint="The provider likely returned an error page. Re-run with --force.",
            )

    @staticmethod
    def _materialize(cache_path: Path, dest: Path) -> Path:
        """Place a cached file at a second location.

        A hard link is attempted first so two paths share one copy on disk; filesystems that
        refuse links fall back to a byte copy.

        Args:
            cache_path: The cached file.
            dest: Where the caller wants it.

        Returns:
            The destination path.

        Raises:
            MediaDownloadError: If the file cannot be placed at ``dest``.
        """
        ensure_parent(dest)
        if dest.exists():
            if dest.stat().st_size == cache_path.stat().st_size:
                return dest
            dest.unlink(missing_ok=True)
        try:
            dest.hardlink_to(cache_path)
        except (OSError, NotImplementedError, AttributeError):
            try:
                dest.write_bytes(cache_path.read_bytes())
            except OSError as exc:
                raise MediaDownloadError(
                    f"Could not place the cached clip at {dest}: {exc}"
                ) from exc
        return dest

    # -- Maintenance ----------------------------------------------------------------------

    def total_size(self) -> int:
        """Return the cache's total size on disk.

        Returns:
            Total bytes used by cached media.
        """
        if not self._cache_dir.is_dir():
            return 0
        return sum(path.stat().st_size for path in self._cache_dir.iterdir() if path.is_file())

    def suffix_for_content_type(self, content_type: str) -> str:
        """Map a MIME type to a file extension.

        Args:
            content_type: The ``Content-Type`` header value.

        Returns:
            A file extension including the leading dot, defaulting to ``.mp4``.
        """
        return _CONTENT_TYPE_SUFFIXES.get(content_type.split(";")[0].strip().lower(), ".mp4")
