"""Tests for Zenn visuals, captions, and timeline helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from models.scenario import Scene
from modules.interfaces import TTSResult, WordCue
from zenn.captions.karaoke_ass import word_cues_to_karaoke_ass
from zenn.render.timeline import collect_word_cues, story_beats
from zenn.visuals import BACKGROUND_TAGS, POSE_TAGS, compose_frame
from zenn.visuals.svg_assets import write_svg_assets


def test_twelve_pose_tags_and_six_backgrounds() -> None:
    """Asset catalogue matches the rule table."""
    assert len(POSE_TAGS) == 12
    assert len(BACKGROUND_TAGS) == 7


def test_compose_frame_is_rgb_1920x1080() -> None:
    """Composed frames match the landscape essay canvas."""
    image = compose_frame("running", "road")
    assert image.size == (1920, 1080)
    assert image.mode == "RGB"
    # Sky band should not be pure black when a visible bg is requested.
    pixel = image.getpixel((960, 200))
    assert pixel != (0, 0, 0)


def test_svg_assets_written(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Bundled SVG pose and background files exist."""
    import zenn.visuals.svg_assets as svg_assets

    monkeypatch.setattr(svg_assets, "ASSETS_DIR", tmp_path)
    monkeypatch.setattr(svg_assets, "POSE_DIR", tmp_path / "poses")
    monkeypatch.setattr(svg_assets, "BG_DIR", tmp_path / "backgrounds")
    paths = write_svg_assets()
    assert len(paths) == 18
    assert (tmp_path / "poses" / "standing.svg").is_file()
    assert (tmp_path / "backgrounds" / "garage.svg").is_file()


def test_karaoke_ass_uses_k_tags() -> None:
    """Active-word highlighting uses ASS karaoke timing."""
    cues = [
        WordCue(text="Hello", start=0.0, end=0.5),
        WordCue(text="world.", start=0.5, end=1.0),
    ]
    body = word_cues_to_karaoke_ass(
        cues,
        play_res_x=1920,
        play_res_y=1080,
        font_name="Arial",
        font_size=60,
    )
    assert "{\\k50}Hello" in body
    assert "{\\k50}world." in body
    assert "SecondaryColour" in body


def test_story_beats_insert_gap_hold() -> None:
    """Inter-chapter silence becomes a hold on the last pose."""
    scenes = [
        Scene.model_validate(
            {
                "id": 1,
                "narration": "The car ran.",
                "search_terms": ["car"],
                "clips_per_scene": 1,
            }
        ),
        Scene.model_validate(
            {
                "id": 2,
                "narration": "Then it stopped.",
                "search_terms": ["road"],
                "clips_per_scene": 1,
            }
        ),
    ]
    results = {
        1: TTSResult(
            audio_path=Path("a1.mp3"),
            duration=2.0,
            word_cues=[
                WordCue("The", 0.0, 0.4),
                WordCue("car", 0.4, 0.8),
                WordCue("ran.", 0.8, 1.2),
            ],
        ),
        2: TTSResult(
            audio_path=Path("a2.mp3"),
            duration=2.0,
            word_cues=[
                WordCue("Then", 0.0, 0.4),
                WordCue("it", 0.4, 0.7),
                WordCue("stopped.", 0.7, 1.1),
            ],
        ),
    }
    beats = story_beats(scenes, results, gap=0.3)
    assert any(beat.text == "" and beat.duration_ms == 300 for beat in beats)
    total_ms = sum(beat.duration_ms for beat in beats)
    assert total_ms >= int(round(results[1].duration * 1000.0))
    merged = collect_word_cues(scenes, results, gap=0.3)
    assert merged[-1].start >= 2.0
