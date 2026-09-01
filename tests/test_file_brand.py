"""After Hours File brand: scenario defaults, Studio pack, beat count."""

from __future__ import annotations

from pathlib import Path

from config.constants import (
    FILE_BRAND_ID,
    FILE_CATEGORY_ID,
    FILE_CHANNEL_NAME,
    FILE_PLAYLIST,
    FILE_TTS_RATE,
    FILE_TTS_VOICE,
    file_beat_count,
)
from modules.brand import AFTER_HOURS_FILE, brand_for_scenario
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_file_scenario
from modules.studio_pack import suggest_playlist, write_studio_pack


def _file_draft() -> DraftScript:
    return DraftScript(
        title="The Night the Lightship Went Quiet",
        description="A closed file on a lightship that stopped answering.",
        tags=("mystery", "file", "night", "sea", "archive"),
        scenes=(
            DraftScene(narration="The radio room waited.", search_terms=("night illustration",)),
            DraftScene(narration="The file never closed.", search_terms=("archive folder",)),
        ),
        visual_beats=(
            DraftVisualBeat(
                slug="radio-room",
                prompt="Empty radio room at night, weak yellow lamp, charcoal walls.",
                covers="The radio room waited.",
            ),
            DraftVisualBeat(
                slug="open-folder",
                prompt="Open manila folder on a dark desk, no faces.",
                covers="The file never closed.",
            ),
        ),
        thumbnail_hook="WENT QUIET",
    )


def test_file_beat_count_ten_minutes() -> None:
    """A ten-minute file uses about sixty stills at ten seconds each."""
    assert file_beat_count(600.0) == 60


def test_build_file_scenario_locks_voice_and_category() -> None:
    """After Hours File does not inherit GuyNeural or Education."""
    scenario = build_file_scenario(
        _file_draft(),
        topic="The Night the Lightship Went Quiet",
        project_id="lightship-quiet-10dk-20260825",
        language="en",
        target_seconds=600.0,
    )
    assert scenario.video.is_paint is True
    assert scenario.tts.voice == FILE_TTS_VOICE
    assert scenario.tts.rate == FILE_TTS_RATE
    assert scenario.youtube.category_id == FILE_CATEGORY_ID
    assert scenario.youtube.brand_id == FILE_BRAND_ID
    assert scenario.subtitles.font_size == 42
    assert scenario.subtitles.position_ratio == 0.86
    assert scenario.subtitles.accent_color is None
    assert brand_for_scenario(scenario) is AFTER_HOURS_FILE


def test_write_studio_pack_after_hours_file(tmp_path: Path) -> None:
    """Studio copy names After Hours File and Closed Files, not Badly Drawn Why."""
    scenario = build_file_scenario(
        _file_draft(),
        topic="The Night the Lightship Went Quiet",
        project_id="lightship-quiet-10dk-20260825",
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
    assert f"Channel: {FILE_CHANNEL_NAME}" in text
    assert "Entertainment (24)" in text
    assert "Education (27)" not in text
    assert "Badly Drawn Why" not in text
    assert FILE_PLAYLIST in text
    assert "illustrated stills + TTS" in text
    assert "WENT QUIET" in text
    assert "stick-figure" not in text
    assert (
        suggest_playlist(scenario.youtube.title, list(scenario.youtube.tags), brand=AFTER_HOURS_FILE)
        == FILE_PLAYLIST
    )


def test_active_brand_id_is_after_hours_file() -> None:
    """After Hours File remains a known brand id even when another channel is active."""
    from modules.brand import AFTER_HOURS_FILE, _BRANDS

    assert FILE_BRAND_ID in _BRANDS
    assert _BRANDS[FILE_BRAND_ID] is AFTER_HOURS_FILE
