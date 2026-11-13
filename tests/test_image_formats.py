"""Images from outside the project are read only as JPEG, PNG or WebP.

Pillow 11.3 has published flaws in the decoders of rarer formats, and MoviePy 2.2.1 holds
Pillow below 12, where they are fixed. A downloaded file in another format, even one named
``.jpg``, must be refused before any of those decoders parses it.
"""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np
import pytest
import requests_mock as rm
from PIL import Image

from modules.interfaces import MediaCandidate
from modules.media_cache import MediaCache
from modules.photo_fetcher import PexelsPhotoProvider, PixabayPhotoProvider
from modules.studio_pack import prepare_youtube_thumbnail
from utils.exceptions import MediaDownloadError, RenderError
from utils.media import image_format

PHOTO_URL = "https://images.pexels.com/photos/2014422/pexels-photo-2014422.jpeg"


def _image_bytes(fmt: str, size: int = 160) -> bytes:
    """A noisy image, so even compressed formats stay above the cache's 10 KB floor."""
    pixels = np.random.default_rng(7).integers(0, 255, (size, size, 3), dtype=np.uint8)
    buffer = io.BytesIO()
    Image.fromarray(pixels).save(buffer, format=fmt)
    return buffer.getvalue()


def _candidate() -> MediaCandidate:
    return MediaCandidate(
        provider="pexels",
        media_id="photo-2014422",
        width=160,
        height=160,
        fps=0.0,
        duration=0.0,
        download_url=PHOTO_URL,
        author_name="Someone",
        author_url="https://www.pexels.com/@someone",
        page_url="https://www.pexels.com/photo/2014422/",
        file_type="image/jpeg",
    )


@pytest.mark.parametrize("fmt", ["JPEG", "PNG", "WEBP"])
def test_the_three_formats_are_recognised(tmp_path: Path, fmt: str) -> None:
    path = tmp_path / "photo.img"
    path.write_bytes(_image_bytes(fmt))

    assert image_format(path) == fmt


@pytest.mark.parametrize("fmt", ["TIFF", "BMP", "GIF", "PPM"])
def test_other_formats_are_refused_even_behind_a_jpg_name(tmp_path: Path, fmt: str) -> None:
    path = tmp_path / "photo.jpg"
    path.write_bytes(_image_bytes(fmt))

    with pytest.raises(OSError):
        image_format(path)


@pytest.mark.parametrize("provider_class", [PexelsPhotoProvider, PixabayPhotoProvider])
def test_a_disguised_download_is_refused_and_both_copies_deleted(
    tmp_path: Path, provider_class: type
) -> None:
    cache = MediaCache(tmp_path / "cache")
    provider = provider_class("test-key", cache)
    dest = tmp_path / "clips" / "photo_001.jpg"

    with rm.Mocker() as mock:
        mock.get(PHOTO_URL, content=_image_bytes("TIFF"))
        with pytest.raises(MediaDownloadError, match="not a JPEG, PNG or WebP"):
            provider.download(_candidate(), dest)

    assert not dest.exists()
    assert not cache.path_for(PHOTO_URL).exists()


def test_a_real_photo_download_is_kept(tmp_path: Path) -> None:
    cache = MediaCache(tmp_path / "cache")
    dest = tmp_path / "clips" / "photo_001.jpg"

    with rm.Mocker() as mock:
        mock.get(PHOTO_URL, content=_image_bytes("JPEG"))
        path = PexelsPhotoProvider("test-key", cache).download(_candidate(), dest)

    assert path == dest
    assert image_format(dest) == "JPEG"


def test_a_cover_in_another_format_is_refused(tmp_path: Path) -> None:
    source = tmp_path / "thumbnail.png"
    source.write_bytes(_image_bytes("BMP"))

    with pytest.raises(RenderError, match="Could not read paint thumbnail"):
        prepare_youtube_thumbnail(source, tmp_path / "thumb.jpg")


def test_a_png_cover_still_becomes_a_thumbnail(tmp_path: Path) -> None:
    source = tmp_path / "thumbnail.png"
    source.write_bytes(_image_bytes("PNG"))

    out = prepare_youtube_thumbnail(source, tmp_path / "thumb.jpg")

    assert image_format(out) == "JPEG"
