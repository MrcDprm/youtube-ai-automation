"""The YouTube uploader's request body and messages, without touching the network."""

from __future__ import annotations

from pathlib import Path

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
