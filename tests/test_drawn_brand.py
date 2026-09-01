"""Drawn Anyway brand: scenario defaults, Studio pack, beat count."""

from __future__ import annotations

from pathlib import Path

from config.constants import (
    DRAWN_BRAND_ID,
    DRAWN_CATEGORY_ID,
    DRAWN_CHANNEL_NAME,
    DRAWN_PLAYLIST,
    DRAWN_TTS_RATE,
    DRAWN_TTS_VOICE,
    DRAWN_ZOOM_END,
    DRAWN_MAX_BEATS,
    drawn_beat_count,
)
from modules.brand import DRAWN_ANYWAY, brand_for_scenario, load_active_brand_id
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario
from modules.studio_pack import suggest_playlist, write_studio_pack


def _drawn_draft() -> DraftScript:
    return DraftScript(
        title="The Army That Lost to Emus",
        description="Australia sent three soldiers and two machine guns after birds. The birds ran.",
        tags=("history", "emu", "cartoon", "australia", "true story"),
        scenes=(
            DraftScene(narration="The army brought a machine gun to a bird problem.", search_terms=("cartoon illustration",)),
            DraftScene(narration="The birds did not line up.", search_terms=("storytime cartoon",)),
        ),
        visual_beats=(
            DraftVisualBeat(
                slug="army-gun",
                prompt="Cartoon soldiers staring at a giant emu, cream paper, mustard jacket mascot in corner.",
                covers="The army brought a machine gun to a bird problem.",
            ),
            DraftVisualBeat(
                slug="birds-ran",
                prompt="Cartoon emus sprinting in all directions, no gore, ink outlines.",
                covers="The birds did not line up.",
            ),
        ),
        thumbnail_hook="BIRDS WON",
    )


def test_drawn_beat_count_eight_minutes() -> None:
    """An eight-minute Drawn Anyway episode uses forty-eight ten-second beats."""
    assert drawn_beat_count(480.0) == 48


def test_drawn_beat_count_eleven_minutes() -> None:
    """An eleven-minute episode caps at sixty-six beats."""
    assert drawn_beat_count(660.0) == DRAWN_MAX_BEATS


def test_build_drawn_scenario_keeps_brand_when_voice_changes() -> None:
    """A British Edge voice still Studio-packs as Drawn Anyway, not After Hours File."""
    scenario = build_drawn_scenario(
        _drawn_draft(),
        topic="The Day a Town Flooded With Beer",
        project_id="beer-flood-10dk-20260825",
        language="en",
        voice="en-GB-ThomasNeural",
        tts_rate="+2%",
        subtitle_color="#F5D76E",
        target_seconds=540.0,
        minutes=9,
    )
    assert scenario.tts.voice == "en-GB-ThomasNeural"
    assert scenario.tts.rate == "+2%"
    assert scenario.youtube.brand_id == DRAWN_BRAND_ID
    assert scenario.subtitles.color == "#F5D76E"
    assert scenario.subtitles.accent_color is None
    assert brand_for_scenario(scenario) is DRAWN_ANYWAY


def test_build_drawn_scenario_locks_voice_and_category() -> None:
    """Drawn Anyway does not inherit RyanNeural or stickman Education."""
    scenario = build_drawn_scenario(
        _drawn_draft(),
        topic="The Army That Lost to Emus",
        project_id="army-lost-to-emus-8dk-20260825",
        language="en",
        target_seconds=480.0,
    )
    assert scenario.video.is_paint is True
    assert scenario.tts.voice == DRAWN_TTS_VOICE
    assert scenario.tts.rate == DRAWN_TTS_RATE
    assert scenario.youtube.category_id == DRAWN_CATEGORY_ID
    assert scenario.youtube.brand_id == DRAWN_BRAND_ID
    assert scenario.subtitles.numeral_display is True
    assert scenario.subtitles.accent_color is None
    assert scenario.video.story_visual.zoom_body_end == DRAWN_ZOOM_END
    assert brand_for_scenario(scenario) is DRAWN_ANYWAY


def test_write_studio_pack_drawn_anyway(tmp_path: Path) -> None:
    """Studio copy names Drawn Anyway and One True Story."""
    scenario = build_drawn_scenario(
        _drawn_draft(),
        topic="The Army That Lost to Emus",
        project_id="army-lost-to-emus-8dk-20260825",
        language="en",
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
    assert f"Channel: {DRAWN_CHANNEL_NAME}" in text
    assert "Entertainment (24)" in text
    assert "Education (27)" not in text
    assert "Badly Drawn Why" not in text
    assert "After Hours File" not in text
    assert DRAWN_PLAYLIST in text
    assert "cartoon animation + TTS" in text
    assert "BIRDS WON" in text
    assert "stick-figure" not in text
    assert (
        suggest_playlist(scenario.youtube.title, list(scenario.youtube.tags), brand=DRAWN_ANYWAY)
        == DRAWN_PLAYLIST
    )


def test_active_brand_id_is_known() -> None:
    """Active brand must resolve to a registered profile."""
    from modules.brand import _BRANDS

    brand_id = load_active_brand_id()
    assert brand_id in _BRANDS
    assert _BRANDS[brand_id].id == brand_id
