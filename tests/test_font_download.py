"""doctor --fix keeps a downloaded font only when it matches its pinned SHA-256."""

from __future__ import annotations

import hashlib
import io
import zipfile
from pathlib import Path

import pytest
import requests_mock as rm

from config.constants import (
    ANTON_TTF_SHA256,
    ANTON_TTF_URL,
    INTER_ZIP_URL,
    PROJECT_ROOT,
)
from utils import fs
from utils.exceptions import FontNotFoundError
from utils.fs import download_default_font, file_sha256

BUNDLED_ANTON = PROJECT_ROOT / "assets" / "fonts" / "Anton-Regular.ttf"


def _fake_inter_archive() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as bundle:
        bundle.writestr("extras/ttf/Inter-Bold.ttf", b"bold face bytes")
    return buffer.getvalue()


def test_the_pins_describe_the_fonts_the_repository_ships() -> None:
    """The Anton pin was taken from this very file, so a refresh must update both."""
    assert file_sha256(BUNDLED_ANTON) == ANTON_TTF_SHA256


def test_a_changed_inter_archive_falls_back_to_the_pinned_anton(tmp_path: Path) -> None:
    with rm.Mocker() as mock:
        mock.get(INTER_ZIP_URL, content=_fake_inter_archive())
        mock.get(ANTON_TTF_URL, content=BUNDLED_ANTON.read_bytes())
        path, source = download_default_font(tmp_path)

    assert path == tmp_path / "Anton-Regular.ttf"
    assert file_sha256(path) == ANTON_TTF_SHA256
    assert "Anton" in source
    assert not (tmp_path / "Inter-Bold.ttf").exists()


def test_nothing_is_written_when_neither_download_matches(tmp_path: Path) -> None:
    with rm.Mocker() as mock:
        mock.get(INTER_ZIP_URL, content=_fake_inter_archive())
        mock.get(ANTON_TTF_URL, content=b"a different file")
        with pytest.raises(FontNotFoundError, match="SHA-256"):
            download_default_font(tmp_path)

    assert list(tmp_path.iterdir()) == []


def test_an_archive_that_matches_its_pin_is_extracted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive = _fake_inter_archive()
    monkeypatch.setattr(fs, "INTER_ZIP_SHA256", hashlib.sha256(archive).hexdigest())

    with rm.Mocker() as mock:
        mock.get(INTER_ZIP_URL, content=archive)
        path, source = download_default_font(tmp_path)

    assert path == tmp_path / "Inter-Bold.ttf"
    assert path.read_bytes() == b"bold face bytes"
    assert "Inter" in source
