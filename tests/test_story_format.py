"""Language packs, story visual timing, photo parsing and story scenario assembly."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests_mock as rm

from models.scenario import Scenario, StoryVisualSettings, VideoSettings
from modules.interfaces import DraftScene, DraftScript, SubtitleCue
from modules.language import (
    get_language_pack,
    language_display_name,
    pick_voice,
)
from modules.photo_fetcher import PexelsPhotoProvider
from modules.scenario_builder import build_scenario, build_story_scenario
from modules.script_generator import OllamaScriptGenerator
from modules.story_duration import keep_leading_scenes, spoken_length
from modules.story_generator import OllamaStoryGenerator
from modules.story_timeline import plan_story_visual
from modules.subtitle import colorize_cues
from tests.test_script_generator import CHAT_URL, HOST, MODEL, _reply


def test_existing_scenarios_default_to_shorts(valid_scenario_path: Path) -> None:
    """Hand-authored Shorts files keep working without a format field."""
    scenario = Scenario.model_validate_json(valid_scenario_path.read_text(encoding="utf-8"))
    assert scenario.video.format == "shorts"
    assert scenario.video.is_story is False


def test_video_settings_story_flag() -> None:
    """format=story flips the story path without changing Shorts defaults."""
    shorts = VideoSettings()
    story = VideoSettings.model_validate({"format": "story", "orientation": "landscape"})
    paint = VideoSettings.model_validate({"format": "paint", "orientation": "landscape"})
    assert shorts.format == "shorts"
    assert shorts.resolution == (1080, 1920)
    assert story.is_story is True
    assert story.is_longform is True
    assert story.is_paint is False
    assert paint.is_paint is True
    assert paint.is_story is False
    assert paint.is_longform is True
    assert paint.resolution == (1920, 1080)


def test_language_packs_cover_tr_en_es() -> None:
    """The three production languages resolve to distinct voice locales."""
    assert get_language_pack("tr").locale == "tr-TR"
    assert get_language_pack("en-US").locale == "en-US"
    assert get_language_pack("es").youtube_language == "es"
    assert language_display_name("es") == "Spanish"
    assert language_display_name("tr") == "Turkish"


def test_pick_voice_is_stable_for_a_project() -> None:
    """The same project id always draws the same pack voice."""
    first = pick_voice("en", "history-of-light-20260820")
    second = pick_voice("en", "history-of-light-20260820")
    other = pick_voice("en", "different-project-20260820")
    assert first == second
    assert first in get_language_pack("en").voices
    assert pick_voice("tr", "x", override="tr-TR-EmelNeural") == "tr-TR-EmelNeural"
    assert other in get_language_pack("en").voices


def test_story_visual_splits_time_equally() -> None:
    """A 15-minute narration gives every photo the same hold and the same slow zoom."""
    visual = StoryVisualSettings()
    plan = plan_story_visual(15 * 60, visual)
    assert plan.opening_duration == 0.0
    assert plan.opening_slots == ()
    assert len(plan.body_slots) == 20
    assert abs(plan.body_slots[0].duration - 45.0) < 0.01
    assert plan.body_slots[0].zoom_end == plan.body_slots[-1].zoom_end
    assert abs(sum(slot.duration for slot in plan.body_slots) - plan.total_duration) < 1e-6


def test_story_visual_scales_when_audio_is_short() -> None:
    """A 4-minute video still uses every photo, just with shorter holds."""
    plan = plan_story_visual(240.0, StoryVisualSettings())
    assert plan.opening_slots == ()
    assert len(plan.body_slots) == 20
    assert abs(plan.body_slots[0].duration - 12.0) < 0.01


def test_colorize_cues_alternates_white_and_gold() -> None:
    """Story burn-in alternates fill colour across cues."""
    cues = [
        SubtitleCue(index=1, start=0.0, end=1.0, text="one"),
        SubtitleCue(index=2, start=1.0, end=2.0, text="two"),
        SubtitleCue(index=3, start=2.0, end=3.0, text="three"),
    ]
    painted = colorize_cues(cues)
    assert painted[0].color == "#FFFFFF"
    assert painted[1].color == "#FFD34F"
    assert painted[2].color == "#FFFFFF"
    assert painted[0].shifted(1.0).color == "#FFFFFF"


def test_pexels_photo_provider_parses_search(tmp_path: Path) -> None:
    """The Photos API shape becomes MediaCandidate stills, not video files."""
    from modules.media_cache import MediaCache

    fixture = Path(__file__).parent / "fixtures" / "pexels_photo_search_response.json"
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    with rm.Mocker() as mock:
        mock.get("https://api.pexels.com/v1/search", json=payload)
        provider = PexelsPhotoProvider("test-key", MediaCache(tmp_path / "cache"))
        found = provider.search("library", "landscape", 0.0, 5)

    assert len(found) == 2
    assert found[0].file_type == "image/jpeg"
    assert found[0].duration == 0.0
    assert found[0].media_id.startswith("photo-")
    assert "images.pexels.com" in found[0].download_url
    assert found[0].download_url.endswith("pexels-photo-2014422.jpeg")
    assert "fit=crop" not in found[0].download_url


def test_build_story_scenario_is_landscape_story() -> None:
    """Story assembly does not reuse Shorts portrait defaults."""
    draft = DraftScript(
        title="The long night",
        description="A spoken history.",
        tags=("history", "night", "sky", "science", "story"),
        scenes=(
            DraftScene(
                narration="A" * 200,
                search_terms=("starry sky", "old telescope"),
            ),
            DraftScene(
                narration="B" * 200,
                search_terms=("desert night", "campfire"),
            ),
        ),
    )
    scenario = build_story_scenario(
        draft,
        topic="The long night",
        project_id="the-long-night-20260820",
        language="en",
        now=datetime(2026, 8, 20, tzinfo=UTC),
    )
    assert scenario.video.is_story is True
    assert scenario.video.orientation == "landscape"
    assert scenario.video.resolution == (1920, 1080)
    assert scenario.subtitles.accent_color == "#FFD34F"
    assert scenario.tts.voice in get_language_pack("en").voices
    assert scenario.tts.rate == "-4%"
    assert scenario.youtube.default_language == "en"
    stamped = build_story_scenario(
        draft,
        topic="The long night",
        language="en",
        minutes=15,
        target_seconds=900.0,
        now=datetime(2026, 8, 21, tzinfo=UTC),
    )
    assert stamped.project_id.endswith("15dk-20260821")
    assert stamped.video.target_duration_seconds == 900.0
    shorts = build_scenario(draft, topic="x", orientation="portrait")
    assert shorts.video.format == "shorts"
    assert shorts.video.resolution == (1080, 1920)


def test_story_generator_asks_one_chapter_at_a_time(requests_mock: rm.Mocker) -> None:
    """Longform generation never asks the model for every chapter in one JSON object."""
    long_text = "Spoken prose. " * 80
    first: dict[str, Any] = {
        "title": "A long story",
        "description": "About time.",
        "tags": ["time", "history", "story", "night", "sky"],
        "narration": long_text,
        "search_terms": ["hourglass sand", "old clock"],
        "summary": "Time begins to move.",
    }
    second: dict[str, Any] = {
        "narration": long_text,
        "search_terms": ["desert stars", "campfire night"],
        "summary": "The travellers look up.",
    }
    requests_mock.post(CHAT_URL, [{"json": _reply(first)}, {"json": _reply(second)}])

    draft = OllamaStoryGenerator(_generator()).generate("time", chapter_count=2, language="en")
    assert len(draft.scenes) == 2
    assert draft.title == "A long story"
    assert len(requests_mock.request_history) == 2
    first_prompt = requests_mock.request_history[0].json()["messages"][0]["content"]
    assert "English" in first_prompt
    assert "novelist-narrator" in first_prompt
    assert "spoken" in first_prompt.lower()


def test_story_generator_stops_when_duration_is_reached(requests_mock: rm.Mocker) -> None:
    """``--minutes`` stops asking once estimated speech covers the target."""
    long_text = "Spoken prose. " * 80
    first: dict[str, Any] = {
        "title": "A long story",
        "description": "About time.",
        "tags": ["time", "history", "story", "night", "sky"],
        "narration": long_text,
        "search_terms": ["hourglass sand", "old clock"],
        "summary": "Time begins to move.",
    }
    requests_mock.post(CHAT_URL, json=_reply(first))

    draft = OllamaStoryGenerator(_generator()).generate(
        "time", target_seconds=30.0, language="en", max_chapters=8
    )
    assert len(draft.scenes) == 1
    assert len(requests_mock.request_history) == 1


def test_keep_leading_scenes_drops_the_overshoot() -> None:
    """A 15-minute target with 45s tolerance keeps chapters that still fit."""
    durations = [100.0] * 12
    keep = keep_leading_scenes(durations, 900.0, tolerance=45.0, gap=0.3)
    assert keep < 12
    assert spoken_length(durations[:keep], 0.3) <= 945.0
    assert keep_leading_scenes([100.0] * 8, 900.0, gap=0.3) == 8


def _generator() -> OllamaScriptGenerator:
    """Build a generator pointed at the stubbed endpoint."""
    return OllamaScriptGenerator(HOST, MODEL, timeout=5.0, max_attempts=3)
