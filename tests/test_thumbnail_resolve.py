"""Thumbnail resolution must not fall back to unrelated episodes."""

from __future__ import annotations

from pathlib import Path

from modules.studio_pack import project_slug, resolve_episode_thumbnail_source


def test_project_slug() -> None:
    assert (
        project_slug("why-a-number-plate-is-a-tax-receipt-11dk-20260829")
        == "why-a-number-plate-is-a-tax-receipt"
    )


def test_resolve_keyword_thumbnail_plate(tmp_path: Path) -> None:
    assets = tmp_path / "assets"
    assets.mkdir()
    rain = assets / "thumbnail-rain.png"
    plate = assets / "thumbnail-plate.png"
    rain.write_bytes(b"rain")
    plate.write_bytes(b"plate")
    project_id = "why-a-number-plate-is-a-tax-receipt-11dk-20260829"
    resolved = resolve_episode_thumbnail_source(project_id, assets_dir=assets, prefer_assets=True)
    assert resolved == plate


def test_resolve_legacy_zero_key(tmp_path: Path) -> None:
    assets = tmp_path / "assets"
    assets.mkdir()
    zero = assets / "thumbnail-zero.png"
    rain = assets / "thumbnail-rain.png"
    zero.write_bytes(b"zero")
    rain.write_bytes(b"rain")
    project_id = "why-nothing-became-a-number-11dk-20260829"
    resolved = resolve_episode_thumbnail_source(project_id, assets_dir=assets, prefer_assets=True)
    assert resolved == zero


def test_no_rain_for_unrelated_episode(tmp_path: Path) -> None:
    assets = tmp_path / "assets"
    assets.mkdir()
    rain = assets / "thumbnail-rain.png"
    rain.write_bytes(b"rain")
    project_id = "why-a-cup-holder-beat-horsepower-11dk-20260901"
    resolved = resolve_episode_thumbnail_source(project_id, assets_dir=assets, prefer_assets=True)
    assert resolved is None
