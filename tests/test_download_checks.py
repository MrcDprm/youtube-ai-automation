"""Downloads are refused when they are web pages or larger than the limit for one file."""

from __future__ import annotations

from pathlib import Path

import pytest
import requests_mock as rm

from modules.media_cache import MAX_PHOTO_DOWNLOAD_BYTES, MediaCache
from modules.photo_fetcher import _download_checked_photo
from utils.exceptions import MediaDownloadError

URL = "https://videos.pexels.com/video-files/123/clip_1080.mp4"
BODY = b"\x00" * 60_000


def _leftovers(cache: MediaCache) -> list[Path]:
    return [path for path in cache.path_for(URL).parent.iterdir() if path.is_file()]


@pytest.mark.parametrize(
    "content_type",
    ["text/html; charset=utf-8", "application/json", "text/plain", "application/xml"],
)
def test_a_web_page_is_not_cached_as_media(tmp_path: Path, content_type: str) -> None:
    cache = MediaCache(tmp_path / "cache", max_attempts=1)

    with rm.Mocker() as mock:
        mock.get(URL, content=BODY, headers={"Content-Type": content_type})
        with pytest.raises(MediaDownloadError, match="instead of a media file"):
            cache.fetch(URL)

    assert _leftovers(cache) == []


@pytest.mark.parametrize("content_type", ["video/mp4", "application/octet-stream", ""])
def test_media_and_unlabelled_files_are_kept(tmp_path: Path, content_type: str) -> None:
    cache = MediaCache(tmp_path / "cache", max_attempts=1)
    headers = {"Content-Type": content_type} if content_type else {}

    with rm.Mocker() as mock:
        mock.get(URL, content=BODY, headers=headers)
        path = cache.fetch(URL)

    assert path.read_bytes() == BODY


def test_a_declared_size_over_the_limit_stops_before_writing(tmp_path: Path) -> None:
    cache = MediaCache(tmp_path / "cache", max_attempts=1)

    with rm.Mocker() as mock:
        mock.get(URL, content=BODY, headers={"Content-Length": str(len(BODY))})
        with pytest.raises(MediaDownloadError, match="above the"):
            cache.fetch(URL, maximum_bytes=len(BODY) - 1)

    assert _leftovers(cache) == []


def test_an_undeclared_stream_over_the_limit_is_cut_off(tmp_path: Path) -> None:
    cache = MediaCache(tmp_path / "cache", max_attempts=1)

    with rm.Mocker() as mock:
        mock.get(URL, content=BODY)
        with pytest.raises(MediaDownloadError, match="was stopped"):
            cache.fetch(URL, maximum_bytes=20_000)

    assert _leftovers(cache) == []


def test_photos_get_the_smaller_limit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cache = MediaCache(tmp_path / "cache", max_attempts=1)
    asked: list[int] = []

    def fetch(url: str, *, dest: Path, maximum_bytes: int) -> Path:
        asked.append(maximum_bytes)
        raise MediaDownloadError("stopped")

    monkeypatch.setattr(cache, "fetch", fetch)

    with pytest.raises(MediaDownloadError):
        _download_checked_photo(cache, URL, tmp_path / "photo.jpg")

    assert asked == [MAX_PHOTO_DOWNLOAD_BYTES]
