"""Paint format: Badly Drawn Why scenario, beats, studio pack, heuristic storyboard."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import requests_mock as rm

from config.constants import PAINT_MAX_BEATS, PAINT_STILL_SECONDS, paint_beat_count
from models.scenario import StoryVisualSettings, VisualBeat
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.language import get_language_pack
from modules.paint_generator import OllamaPaintGenerator, _beats_from_narration, _strip_banned
from modules.paint_stills import expected_beat_name, resolve_paint_stills
from modules.scenario_builder import build_paint_scenario
from modules.script_generator import OllamaScriptGenerator
from modules.story_timeline import plan_story_visual, plan_weighted_visual
from modules.studio_pack import (
    chapter_markers,
    format_chapter_time,
    suggest_playlist,
    write_studio_pack,
)
from tests.test_script_generator import CHAT_URL, HOST, MODEL, _reply
from utils.exceptions import MediaNotFoundError


def test_build_paint_scenario_is_landscape_paint() -> None:
    """Paint assembly does not reuse Shorts portrait defaults or Pexels search terms."""
    draft = DraftScript(
        title="Why Your Ancestors Slept Twice Every Night",
        description="You were not designed to sleep in one block.",
        tags=("sleep", "history", "night", "science", "darkness"),
        scenes=(
            DraftScene(narration="A" * 200, search_terms=("stickman drawing",)),
            DraftScene(narration="B" * 200, search_terms=("ms paint illustration",)),
        ),
        visual_beats=(
            DraftVisualBeat(
                slug="light-switch",
                prompt="Stickman flips a yellow switch in a simple room.",
                covers="You flip a switch.",
            ),
            DraftVisualBeat(
                slug="first-sleep",
                prompt="Stickman asleep then awake in a dark bed.",
                covers="First sleep then the watch.",
            ),
        ),
        thumbnail_hook="2 AM?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Your Ancestors Slept Twice Every Night",
        project_id="ancestors-slept-twice-20260822",
        language="en",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 22, tzinfo=UTC),
        use_zenn=False,
    )
    assert scenario.video.is_paint is True
    assert scenario.video.is_story is False
    assert scenario.video.is_longform is True
    assert scenario.video.orientation == "landscape"
    assert scenario.video.resolution == (1920, 1080)
    assert len(scenario.video.visual_beats) == 2
    assert scenario.video.story_visual.photo_count == 2
    assert scenario.youtube.thumbnail_hook == "2 AM?"
    assert scenario.youtube.privacy_status == "unlisted"
    assert scenario.youtube.upload_enabled is False
    assert scenario.youtube.default_language == "en"
    assert scenario.tts.voice in get_language_pack("en").voices
    assert scenario.tts.rate == "-4%"
    assert scenario.subtitles.accent_color is None
    assert scenario.subtitles.stroke_width == 5
    stamped = build_paint_scenario(
        draft,
        topic="Why Your Ancestors Slept Twice Every Night",
        language="en",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 22, tzinfo=UTC),
        use_zenn=False,
    )
    assert "11dk" in stamped.project_id
    assert stamped.video.target_duration_seconds == 660.0


def test_build_paint_scenario_defaults_to_legacy_paint_for_bdw() -> None:
    """Badly Drawn Why uses MS Paint stills by default, not Zenn."""
    draft = DraftScript(
        title="Why Your Week Has Seven Days",
        description="The week is a leftover grid.",
        tags=("calendar", "week", "history"),
        scenes=(
            DraftScene(narration="You count seven days.", search_terms=("calendar",)),
            DraftScene(narration="The moon disagrees.", search_terms=("moon",)),
        ),
        visual_beats=(
            DraftVisualBeat(slug="0000-seven", prompt="Seven boxes, MS Paint.", covers="Seven days."),
            DraftVisualBeat(slug="0005-moon", prompt="Moon phases, MS Paint.", covers="Moon phases."),
        ),
        thumbnail_hook="SEVEN DAYS?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Your Week Has Seven Days",
        language="en",
        minutes=11,
        target_seconds=660.0,
    )
    assert scenario.video.is_zenn is False
    assert scenario.video.story_visual.zenn_enabled is False
    assert len(scenario.video.visual_beats) == 2
    assert scenario.youtube.brand_id == "badly-drawn-why"


def test_plan_weighted_visual_follows_coverage() -> None:
    """A still that covers more transcript holds longer, and slots sum to the runtime."""
    plan = plan_weighted_visual(100.0, [1.0, 3.0, 1.0], zoom_end=1.08)
    assert len(plan.body_slots) == 3
    assert abs(plan.body_slots[1].duration - 60.0) < 1e-6
    assert abs(sum(slot.duration for slot in plan.body_slots) - 100.0) < 1e-9
    assert plan.body_slots[0].zoom_end == 1.08


def test_paint_beat_count_for_eleven_minutes() -> None:
    """An 11-minute essay needs 132 unique stills at five seconds each."""
    assert paint_beat_count(660.0) == 132
    assert paint_beat_count(0.0) == 60
    assert paint_beat_count(10_000.0) == PAINT_MAX_BEATS


def test_paint_stills_share_five_seconds_equally() -> None:
    """Paint timing is equal-time, not covers-weighted, so 660s / 132 stills is 5s."""
    count = paint_beat_count(660.0)
    visual = StoryVisualSettings(photo_count=count, opening_photo_count=1)
    plan = plan_story_visual(660.0, visual)
    assert visual.photo_count == 132
    assert len(plan.body_slots) == 132
    assert abs(plan.body_slots[0].duration - PAINT_STILL_SECONDS) < 1e-9
    assert abs(plan.body_slots[-1].duration - PAINT_STILL_SECONDS) < 1e-9


def test_paint_equal_time_ignores_covers_length() -> None:
    """A long covers line no longer steals hold time from its neighbours."""
    visual = StoryVisualSettings(photo_count=3, opening_photo_count=1)
    equal = plan_story_visual(30.0, visual)
    weighted = plan_weighted_visual(30.0, [10.0, 80.0, 10.0], zoom_end=1.08)
    assert abs(equal.body_slots[0].duration - 10.0) < 1e-9
    assert abs(equal.body_slots[1].duration - 10.0) < 1e-9
    assert equal.body_slots[1].duration != weighted.body_slots[1].duration


def test_chapter_markers_start_at_zero() -> None:
    """YouTube chapters must include a 0:00 row."""
    from models.scenario import Scene

    scenes = [
        Scene.model_validate(
            {"id": 1, "narration": "You flip a switch tonight.", "search_terms": ["room"]}
        ),
        Scene.model_validate(
            {"id": 2, "narration": "Fire added extra hours.", "search_terms": ["fire"]}
        ),
    ]
    markers = chapter_markers(scenes, [12.0, 48.0], gap=0.3)
    assert markers[0][0] == "0:00"
    assert markers[1][0] == format_chapter_time(12.3)
    assert "flip a switch" in markers[0][1].lower()


def test_write_studio_pack_contains_checklist(tmp_path: Path) -> None:
    """The Studio file is paste-ready: title, chapters, tags, altered-content note."""
    scenario = build_paint_scenario(
        DraftScript(
            title="Why Fire Gave Humans Extra Hours",
            description="The night used to end at sunset.",
            tags=("fire", "night", "history", "sleep", "human"),
            scenes=(
                DraftScene(narration="You sit in the dark.", search_terms=("stickman drawing",)),
                DraftScene(narration="Fire added hours.", search_terms=("ms paint illustration",)),
            ),
            visual_beats=(
                DraftVisualBeat(
                    slug="dark", prompt="Stickman in darkness looking lost.", covers="dark"
                ),
                DraftVisualBeat(
                    slug="fire", prompt="Tiny campfire with two stickmen.", covers="fire"
                ),
            ),
            thumbnail_hook="EXTRA HOURS",
        ),
        topic="fire hours",
        project_id="fire-hours-20260822",
        language="en",
        use_zenn=False,
    )
    video = tmp_path / "final.mp4"
    video.write_bytes(b"mp4")
    thumb = tmp_path / "thumb.jpg"
    thumb.write_bytes(b"jpg")
    srt = tmp_path / "captions.srt"
    srt.write_text("1\n", encoding="utf-8")
    path = write_studio_pack(
        scenario,
        video_path=video,
        thumbnail_path=thumb,
        srt_path=srt,
        durations=[10.0, 20.0],
        out_dir=tmp_path / "studio",
    )
    text = path.read_text(encoding="utf-8")
    assert "Why Fire Gave Humans Extra Hours" in text
    assert "Chapters:" in text
    assert "0:00" in text
    assert "Education (27)" in text
    assert "Altered / synthetic content: Yes" in text
    assert "Unlisted" in text
    assert "EXTRA HOURS" in text
    assert (
        suggest_playlist(scenario.youtube.title, list(scenario.youtube.tags)) == "The Human Night"
    )


def test_resolve_paint_stills_from_storyboard(tmp_path: Path) -> None:
    """NN-slug.png in the project storyboard folder is enough; no API key."""
    folder = tmp_path / "board" / "demo"
    folder.mkdir(parents=True)
    (folder / "01-switch.png").write_bytes(b"a")
    (folder / "02-stars.png").write_bytes(b"b")
    beats = [
        VisualBeat(
            slug="switch", prompt="Stickman at a wall switch looking surprised.", covers="click"
        ),
        VisualBeat(slug="stars", prompt="Black sky rectangle with three star dots.", covers="sky"),
    ]
    found = resolve_paint_stills(beats, project_id="demo", search_roots=[tmp_path / "board"])
    assert [path.name for path in found] == ["01-switch.png", "02-stars.png"]


def test_resolve_paint_stills_reports_missing(tmp_path: Path) -> None:
    """A missing still names the expected file so the image agent can drop it."""
    beats = [
        VisualBeat(
            slug="switch", prompt="Stickman at a wall switch looking surprised.", covers="click"
        ),
        VisualBeat(slug="stars", prompt="Black sky rectangle with three star dots.", covers="sky"),
    ]
    try:
        resolve_paint_stills(beats, project_id="demo", search_roots=[tmp_path])
    except MediaNotFoundError as exc:
        assert "01-switch.png" in exc.message
        assert expected_beat_name(1, "switch") in exc.message
    else:
        raise AssertionError("expected MediaNotFoundError")


def test_expected_beat_name_keeps_three_digit_indexes() -> None:
    """Beat 132 is `132-slug.png`, not a two-digit overflow."""
    assert expected_beat_name(132, "grin-no-arms") == "132-grin-no-arms"


def test_heuristic_beats_cover_the_essay() -> None:
    """When the model beat pass fails, sentence groups still yield a usable storyboard."""
    text = " ".join(f"Sentence number {index} is spoken aloud." for index in range(80))
    beats = _beats_from_narration(text, target=40)
    assert 2 <= len(beats) <= PAINT_MAX_BEATS
    assert all(beat.prompt for beat in beats)
    assert all(beat.slug for beat in beats)


def test_heuristic_beats_can_fill_five_second_cadence() -> None:
    """Enough sentences yield one still per five-second slot."""
    text = " ".join(f"Sentence number {index} is spoken aloud." for index in range(132))
    beats = _beats_from_narration(text, target=paint_beat_count(660.0))
    assert len(beats) == 132


def test_strip_banned_drops_subscribe_asks() -> None:
    """Retention rules strip lecture framing if the model sneaks it in."""
    cleaned = _strip_banned(
        "Welcome back. You flip a switch. Don't forget to subscribe. Night falls."
    )
    lowered = cleaned.lower()
    assert "welcome back" not in lowered
    assert "subscribe" not in lowered
    assert "flip a switch" in lowered


def test_paint_generator_asks_chapters_then_beats(requests_mock: rm.Mocker) -> None:
    """Paint generation is sequential chapters plus one storyboard pass."""
    long_text = "You flip a switch tonight. " * 60
    first: dict[str, object] = {
        "title": "Why Your Ancestors Slept Twice Every Night",
        "description": "The night used to have a hole in the middle.",
        "tags": ["sleep", "night", "history", "dark", "fire"],
        "thumbnail_hook": "2 AM?",
        "narration": long_text,
        "summary": "The switch and the missing night.",
    }
    beats_payload = {
        "beats": [
            {
                "slug": "switch",
                "covers": "You flip a switch.",
                "prompt": "Stickman flips a yellow switch on a white wall.",
            },
            {
                "slug": "fire-circle",
                "covers": "A campfire makes a thirty foot circle.",
                "prompt": "Tiny orange fire with a dashed circle and two stickmen inside.",
            },
        ]
    }
    requests_mock.post(
        CHAT_URL,
        [{"json": _reply(first)}, {"json": _reply(beats_payload)}],
    )
    draft = OllamaPaintGenerator(_generator()).generate(
        "Why Your Ancestors Slept Twice Every Night",
        target_seconds=30.0,
        language="en",
        max_chapters=8,
    )
    assert len(draft.scenes) == 1
    assert draft.thumbnail_hook == "2 AM?"
    assert len(draft.visual_beats) == 2
    assert draft.visual_beats[0].slug == "switch"
    assert "Badly Drawn Why" in requests_mock.request_history[0].json()["messages"][0]["content"]
    assert "COLD OPEN" in requests_mock.request_history[0].json()["messages"][0]["content"]


def test_topics_paint_lists_the_bank() -> None:
    """``topics --paint`` prints the Badly Drawn Why idea list."""
    from typer.testing import CliRunner

    from main import app

    result = CliRunner().invoke(app, ["topics", "--paint"])
    assert result.exit_code == 0, result.output
    assert "Why Your Ancestors Slept Twice Every Night" in result.output


def _generator() -> OllamaScriptGenerator:
    """Build a generator pointed at the stubbed endpoint."""
    return OllamaScriptGenerator(HOST, MODEL, timeout=5.0, max_attempts=3)
