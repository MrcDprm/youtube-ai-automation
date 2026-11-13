"""The YouTube uploader's request body and messages, without touching the network."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

import modules.uploader as uploader_module
from models.scenario import YouTubeSettings
from modules.interfaces import MediaCredit
from modules.uploader import YouTubeUploader

CREDIT = MediaCredit(
    provider="pexels",
    author_name="Ayşe Kaya",
    author_url="https://www.pexels.com/@ayse",
    page_url="https://www.pexels.com/video/123/",
)


def _uploader(tmp_path: Path) -> YouTubeUploader:
    return YouTubeUploader(tmp_path / "client_secrets.json", tmp_path / "token.json")


def test_the_description_names_the_footage_contributors(tmp_path: Path) -> None:
    meta = YouTubeSettings(title="Deneme", description="Kısa bir açıklama.")

    body = _uploader(tmp_path)._build_body(meta, [CREDIT, CREDIT])

    description = body["snippet"]["description"]
    assert description.startswith("Kısa bir açıklama.")
    assert description.count("Ayşe Kaya") == 1
    assert "https://www.pexels.com/video/123/" in description


def test_without_credits_only_the_disclosure_is_added(tmp_path: Path) -> None:
    meta = YouTubeSettings(title="Deneme", description="Kısa bir açıklama.")

    description = _uploader(tmp_path)._build_body(meta)["snippet"]["description"]

    assert "Footage:" not in description
    assert description != "Kısa bir açıklama."


class _Request:
    def __init__(self, response: dict[str, Any]) -> None:
        self._response = response

    def next_chunk(self) -> tuple[None, dict[str, Any]]:
        return None, self._response


class _Videos:
    def __init__(self, response: dict[str, Any]) -> None:
        self._response = response

    def insert(self, **_: Any) -> _Request:
        return _Request(self._response)


class _Service:
    """Answers an upload the way YouTube does for a project that has not been audited."""

    def __init__(self, applied_privacy: str) -> None:
        self._videos = _Videos({"id": "abc123", "status": {"privacyStatus": applied_privacy}})

    def videos(self) -> _Videos:
        return self._videos


@pytest.mark.parametrize(("requested", "warned"), [("public", True), ("private", False)])
def test_a_private_lock_points_to_the_audit_and_youtube_studio(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, requested: str, warned: bool
) -> None:
    warnings: list[str] = []
    monkeypatch.setattr(uploader_module, "log_warn", warnings.append)
    video = tmp_path / "video.mp4"
    video.write_bytes(b"\x00" * 1024)
    uploader = _uploader(tmp_path)
    uploader._service = _Service("private")

    meta = YouTubeSettings.model_validate({"title": "Deneme", "privacy_status": requested})

    result = uploader.upload(video, meta, None)

    assert result.privacy_status == "private"
    if warned:
        assert len(warnings) == 1
        assert "compliance audit" in warnings[0]
        assert "YouTube Studio" in warnings[0]
    else:
        assert warnings == []
