"""Every Level POV brand: scenario defaults, Studio pack, beat count."""

from __future__ import annotations

from pathlib import Path

from config.constants import (
    EVERY_LEVEL_POV_BRAND_ID,
    POV_CATEGORY_ID,
    POV_CHANNEL_NAME,
    POV_MAX_BEATS,
    POV_MIN_BEATS,
    POV_PLAYLIST,
    POV_TTS_RATE,
    POV_TTS_VOICE,
    POV_ZOOM_END,
    pov_beat_count,
)
from modules.brand import EVERY_LEVEL_POV, brand_for_scenario, load_active_brand_id
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_pov_scenario
from modules.studio_pack import suggest_playlist, write_studio_pack


def _pov_draft() -> DraftScript:
    return DraftScript(
        title="Your Life at Every Level of Football",
        description="Cartoon POV rank progression from park kickabout to European nights.",
        tags=("football", "pov", "cartoon", "every level", "soccer"),
        scenes=(
            DraftScene(
                narration="Level one is a park goal made of backpacks.",
                search_terms=("cartoon pov illustration",),
            ),
            DraftScene(
                narration="Level twelve is a national camp call-up.",
                search_terms=("football rank cartoon",),
            ),
        ),
        visual_beats=(
            DraftVisualBeat(
                slug="park-level",
                prompt="Kit at park kickabout, LEVEL 1, cartoon POV.",
                covers="Level one is a park goal made of backpacks.",
            ),
            DraftVisualBeat(
                slug="camp-level",
                prompt="Kit at national camp, LEVEL 12, cartoon POV.",
                covers="Level twelve is a national camp call-up.",
            ),
        ),
        thumbnail_hook="YOU START HERE",
    )


def test_pov_beat_count_fourteen_minutes() -> None:
    """A fourteen-minute POV episode uses eighty-four ten-second beats."""
    assert pov_beat_count(840.0) == 84


def test_pov_beat_count_twelve_minutes() -> None:
    assert pov_beat_count(720.0) == 72


def test_pov_beat_count_twenty_six_minutes() -> None:
    assert pov_beat_count(1560.0) == POV_MAX_BEATS


def test_pov_beat_count_clamps_low() -> None:
    assert pov_beat_count(60.0) == POV_MIN_BEATS


def test_build_pov_scenario_defaults() -> None:
    scenario = build_pov_scenario(
        _pov_draft(),
        topic="Your Life at Every Level of Football",
        language="en",
        minutes=14,
        target_seconds=840.0,
    )
    assert scenario.youtube.brand_id == EVERY_LEVEL_POV_BRAND_ID
    assert scenario.youtube.category_id == POV_CATEGORY_ID
    assert scenario.tts.voice == POV_TTS_VOICE
    assert scenario.tts.rate == POV_TTS_RATE
    assert scenario.video.format == "paint"
    assert scenario.video.story_visual.zoom_body_end == POV_ZOOM_END
    assert scenario.subtitles.numeral_display is True


def test_brand_for_pov_scenario() -> None:
    scenario = build_pov_scenario(
        _pov_draft(),
        topic="Test POV",
        language="en",
    )
    assert brand_for_scenario(scenario) is EVERY_LEVEL_POV


def test_studio_pack_uses_pov_channel(tmp_path: Path) -> None:
    scenario = build_pov_scenario(
        _pov_draft(),
        topic="Your Life at Every Level of Football",
        language="en",
        project_id="test-pov-14dk-20260902",
    )
    path = write_studio_pack(
        scenario,
        video_path=tmp_path / "final.mp4",
        thumbnail_path=tmp_path / "thumb.jpg",
        srt_path=tmp_path / "captions.srt",
        durations=[10.0, 20.0],
        out_dir=tmp_path / "studio",
    )
    text = path.read_text(encoding="utf-8")
    assert POV_CHANNEL_NAME in text
    assert "cartoon POV illustrations + TTS" in text
    assert suggest_playlist(
        scenario.youtube.title, list(scenario.youtube.tags), brand=EVERY_LEVEL_POV
    ) == POV_PLAYLIST


def test_active_brand_id_is_every_level_pov() -> None:
    from modules.brand import _BRANDS

    brand_id = load_active_brand_id()
    assert brand_id == EVERY_LEVEL_POV_BRAND_ID
    assert brand_id in _BRANDS
