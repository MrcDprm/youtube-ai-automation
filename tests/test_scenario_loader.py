"""Scenario loading and every cross-field validator."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from models.scenario import (
    BackgroundMusic,
    Scenario,
    SubtitleSettings,
    VideoSettings,
    YouTubeSettings,
)
from modules.scenario_loader import ScenarioLoader, load_scenario
from utils.exceptions import ScenarioValidationError


def _loader() -> ScenarioLoader:
    """Return a loader that does not print Rich error tables during tests."""
    return ScenarioLoader(render_errors=False)


# --------------------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------------------


def test_loads_valid_scenario(valid_scenario_path: Path) -> None:
    """A well-formed scenario loads and exposes its parsed fields."""
    scenario = _loader().load(valid_scenario_path)

    assert scenario.project_id == "test-project-01"
    assert scenario.total_scenes == 2
    assert scenario.video.resolution == (1080, 1920)
    assert scenario.scenes[1].clips_per_scene == 2


def test_loads_the_shipped_example() -> None:
    """The example scenario shipped with the project is valid."""
    from config.constants import PROJECT_ROOT

    scenario = _loader().load(PROJECT_ROOT / "senaryo.example.json")
    assert scenario.project_id == "yapay-zeka-tarihi-01"
    assert scenario.total_scenes == 3


def test_missing_file_raises_with_a_hint(tmp_path: Path) -> None:
    """A missing scenario names the path and suggests a fix."""
    with pytest.raises(ScenarioValidationError) as info:
        _loader().load(tmp_path / "nope.json")

    assert "not found" in str(info.value)
    assert info.value.hint is not None


def test_malformed_json_reports_line_and_column(tmp_path: Path) -> None:
    """A JSON syntax error is reported with its exact position."""
    broken = tmp_path / "broken.json"
    broken.write_text('{\n  "project_id": "abc",\n  "video": {,}\n}', encoding="utf-8")

    with pytest.raises(ScenarioValidationError) as info:
        _loader().load(broken)

    message = str(info.value)
    assert "line 3" in message
    assert "column" in message


def test_non_object_top_level_is_rejected(tmp_path: Path) -> None:
    """A JSON array at the top level is rejected with a clear message."""
    path = tmp_path / "array.json"
    path.write_text("[1, 2, 3]", encoding="utf-8")

    with pytest.raises(ScenarioValidationError, match="JSON object"):
        _loader().load(path)


def test_invalid_scenario_reports_many_errors(invalid_scenario_path: Path) -> None:
    """The deliberately broken fixture fails validation."""
    with pytest.raises(ScenarioValidationError) as info:
        _loader().load(invalid_scenario_path)

    assert "failed schema validation" in str(info.value)


def test_invalid_scenario_error_count_is_high(invalid_scenario_path: Path) -> None:
    """Every independent mistake in the broken fixture is reported, not just the first."""
    payload = json.loads(invalid_scenario_path.read_text(encoding="utf-8"))

    with pytest.raises(ValidationError) as info:
        Scenario.model_validate(payload)

    fields = {".".join(str(part) for part in error["loc"]) for error in info.value.errors()}
    assert any("project_id" in field for field in fields)
    assert any("fps" in field for field in fields)
    assert any("preset" in field for field in fields)


def test_public_helper_matches_loader_class(valid_scenario_path: Path) -> None:
    """The module-level helper behaves like the class."""
    assert load_scenario(valid_scenario_path, render_errors=False).project_id == "test-project-01"


# --------------------------------------------------------------------------------------
# Field-level rules
# --------------------------------------------------------------------------------------


def test_unknown_keys_are_forbidden(valid_scenario_dict: dict[str, Any]) -> None:
    """A typo in a key name fails rather than being silently ignored."""
    valid_scenario_dict["video"]["frames_per_second"] = 30

    with pytest.raises(ValidationError) as info:
        Scenario.model_validate(valid_scenario_dict)

    assert any(error["type"] == "extra_forbidden" for error in info.value.errors())


@pytest.mark.parametrize("slug", ["ab", "Has-Capitals", "has spaces", "has_underscore!"])
def test_project_id_slug_is_enforced(valid_scenario_dict: dict[str, Any], slug: str) -> None:
    """Only lowercase slug-shaped project ids are accepted."""
    valid_scenario_dict["project_id"] = slug
    with pytest.raises(ValidationError):
        Scenario.model_validate(valid_scenario_dict)


@pytest.mark.parametrize("rate", ["8%", "+8", "++8%", "8 percent"])
def test_tts_rate_pattern(valid_scenario_dict: dict[str, Any], rate: str) -> None:
    """Prosody strings must carry an explicit sign and unit."""
    valid_scenario_dict["tts"]["rate"] = rate
    with pytest.raises(ValidationError):
        Scenario.model_validate(valid_scenario_dict)


def test_tts_pitch_requires_hz(valid_scenario_dict: dict[str, Any]) -> None:
    """Pitch is expressed in Hz, not percent."""
    valid_scenario_dict["tts"]["pitch"] = "+10%"
    with pytest.raises(ValidationError):
        Scenario.model_validate(valid_scenario_dict)


def test_subtitle_color_must_be_hex(valid_scenario_dict: dict[str, Any]) -> None:
    """Named colours are rejected in favour of unambiguous hex."""
    valid_scenario_dict["subtitles"]["color"] = "white"
    with pytest.raises(ValidationError):
        Scenario.model_validate(valid_scenario_dict)


# --------------------------------------------------------------------------------------
# Cross-field validators
# --------------------------------------------------------------------------------------


def test_duplicate_scene_ids_are_rejected(valid_scenario_dict: dict[str, Any]) -> None:
    """Scene ids name cache files, so duplicates must fail."""
    valid_scenario_dict["scenes"][1]["id"] = 1

    with pytest.raises(ValidationError, match="unique"):
        Scenario.model_validate(valid_scenario_dict)


def test_crossfade_must_fit_the_shortest_scene(valid_scenario_dict: dict[str, Any]) -> None:
    """Twice the crossfade must stay under the shortest scene."""
    valid_scenario_dict["video"]["crossfade_seconds"] = 2.0
    valid_scenario_dict["scenes"][1]["min_clip_duration"] = 3.0

    with pytest.raises(ValidationError, match="crossfade"):
        Scenario.model_validate(valid_scenario_dict)


def test_crossfade_exactly_half_is_rejected(valid_scenario_dict: dict[str, Any]) -> None:
    """The boundary case is excluded, since a crossfade would consume the whole scene."""
    valid_scenario_dict["video"]["crossfade_seconds"] = 1.5
    for scene in valid_scenario_dict["scenes"]:
        scene["min_clip_duration"] = 3.0

    with pytest.raises(ValidationError, match="crossfade"):
        Scenario.model_validate(valid_scenario_dict)


def test_zero_crossfade_always_passes(valid_scenario_dict: dict[str, Any]) -> None:
    """Hard cuts impose no constraint on scene length."""
    valid_scenario_dict["video"]["crossfade_seconds"] = 0.0
    assert Scenario.model_validate(valid_scenario_dict).video.crossfade_seconds == 0.0


def test_resolution_must_match_orientation(valid_scenario_dict: dict[str, Any]) -> None:
    """A landscape resolution cannot be declared as portrait."""
    valid_scenario_dict["video"]["resolution"] = [1920, 1080]

    with pytest.raises(ValidationError, match="orientation"):
        Scenario.model_validate(valid_scenario_dict)


def test_resolution_is_derived_from_orientation() -> None:
    """Omitting the resolution derives it from the orientation."""
    assert VideoSettings.model_validate({"orientation": "landscape"}).resolution == (1920, 1080)
    assert VideoSettings.model_validate({"orientation": "square"}).resolution == (1080, 1080)
    assert VideoSettings.model_validate({}).resolution == (1080, 1920)


def test_odd_resolution_is_rejected() -> None:
    """H.264 with yuv420p needs even dimensions."""
    with pytest.raises(ValidationError, match="even"):
        VideoSettings.model_validate({"orientation": "portrait", "resolution": [1081, 1920]})


def test_publish_at_must_be_in_the_future() -> None:
    """A past schedule is a mistake, not an instruction."""
    past = datetime.now(UTC) - timedelta(days=1)
    with pytest.raises(ValidationError, match="future"):
        YouTubeSettings.model_validate({"title": "x", "publish_at": past.isoformat()})


def test_publish_at_forces_private() -> None:
    """Scheduled uploads must start private; the API rejects anything else."""
    future = datetime.now(UTC) + timedelta(days=1)
    with pytest.raises(ValidationError, match="private"):
        YouTubeSettings.model_validate(
            {"title": "x", "publish_at": future.isoformat(), "privacy_status": "public"}
        )


def test_publish_at_accepts_a_future_private_schedule() -> None:
    """The valid combination is accepted and normalised to an aware datetime."""
    future = datetime.now(UTC) + timedelta(days=2)
    settings = YouTubeSettings.model_validate(
        {"title": "x", "publish_at": future.isoformat(), "privacy_status": "private"}
    )
    assert settings.publish_at is not None
    assert settings.publish_at.tzinfo is not None


def test_naive_publish_at_is_treated_as_utc() -> None:
    """A datetime without a zone is interpreted as UTC rather than rejected."""
    future = (datetime.now(UTC) + timedelta(days=2)).replace(tzinfo=None)
    settings = YouTubeSettings.model_validate({"title": "x", "publish_at": future.isoformat()})
    assert settings.publish_at is not None
    assert settings.publish_at.tzinfo is UTC


def test_music_file_required_when_enabled() -> None:
    """Enabling music without a file is a configuration error."""
    with pytest.raises(ValidationError, match="required"):
        BackgroundMusic.model_validate({"enabled": True})


def test_music_file_must_exist_when_enabled(tmp_path: Path) -> None:
    """A configured music file that is not on disk fails validation."""
    with pytest.raises(ValidationError, match="does not exist"):
        BackgroundMusic.model_validate({"enabled": True, "file": str(tmp_path / "gone.mp3")})


def test_music_file_is_not_checked_when_disabled(tmp_path: Path) -> None:
    """A missing file is fine as long as music is switched off."""
    music = BackgroundMusic.model_validate({"enabled": False, "file": str(tmp_path / "gone.mp3")})
    assert music.enabled is False


def test_existing_music_file_passes(tmp_path: Path) -> None:
    """An existing file is accepted and exposed as an absolute path."""
    track = tmp_path / "loop.mp3"
    track.write_bytes(b"not really audio, but it exists")

    music = BackgroundMusic.model_validate({"enabled": True, "file": str(track)})
    assert music.resolved_file == track


def test_burn_in_requires_a_resolvable_font(monkeypatch: pytest.MonkeyPatch) -> None:
    """Burn-in fails only when no font can be resolved anywhere."""
    monkeypatch.setattr("models.scenario.font_is_resolvable", lambda _path: False)

    with pytest.raises(ValidationError, match="could not be resolved"):
        SubtitleSettings.model_validate({"burn_in": True, "font": "missing.ttf"})


def test_sidecar_only_subtitles_need_no_font(monkeypatch: pytest.MonkeyPatch) -> None:
    """Writing only an SRT never needs a font file."""
    monkeypatch.setattr("models.scenario.font_is_resolvable", lambda _path: False)

    settings = SubtitleSettings.model_validate({"burn_in": False, "font": "missing.ttf"})
    assert settings.burn_in is False


def test_scene_orientation_override_must_match(valid_scenario_dict: dict[str, Any]) -> None:
    """Mixing aspect ratios in one render is rejected."""
    valid_scenario_dict["scenes"][0]["orientation"] = "landscape"

    with pytest.raises(ValidationError, match="orientation"):
        Scenario.model_validate(valid_scenario_dict)


def test_matching_scene_orientation_is_allowed(valid_scenario_dict: dict[str, Any]) -> None:
    """A redundant but consistent override is harmless."""
    valid_scenario_dict["scenes"][0]["orientation"] = "portrait"
    assert Scenario.model_validate(valid_scenario_dict).scenes[0].orientation == "portrait"


def test_blank_narration_is_rejected(valid_scenario_dict: dict[str, Any]) -> None:
    """Whitespace-only narration would synthesize silence."""
    valid_scenario_dict["scenes"][0]["narration"] = "     "
    with pytest.raises(ValidationError):
        Scenario.model_validate(valid_scenario_dict)


def test_empty_search_terms_are_rejected(valid_scenario_dict: dict[str, Any]) -> None:
    """A scene needs at least one search term unless it uses local media."""
    valid_scenario_dict["scenes"][0]["search_terms"] = []
    with pytest.raises(ValidationError):
        Scenario.model_validate(valid_scenario_dict)


def test_missing_local_media_is_rejected(
    valid_scenario_dict: dict[str, Any], tmp_path: Path
) -> None:
    """A local media override must point at a real file."""
    valid_scenario_dict["scenes"][0]["local_media"] = str(tmp_path / "absent.mp4")
    with pytest.raises(ValidationError, match="does not exist"):
        Scenario.model_validate(valid_scenario_dict)


def test_title_length_is_capped(valid_scenario_dict: dict[str, Any]) -> None:
    """YouTube truncates titles over 100 characters, so the schema rejects them."""
    valid_scenario_dict["youtube"]["title"] = "x" * 101
    with pytest.raises(ValidationError):
        Scenario.model_validate(valid_scenario_dict)


def test_tag_budget_is_enforced(valid_scenario_dict: dict[str, Any]) -> None:
    """The joined tag length has a hard API limit."""
    valid_scenario_dict["youtube"]["tags"] = ["a" * 60 for _ in range(10)]
    with pytest.raises(ValidationError, match="limit"):
        Scenario.model_validate(valid_scenario_dict)


def test_scene_lookup_and_estimate(valid_scenario_path: Path) -> None:
    """Helper accessors behave as documented."""
    scenario = _loader().load(valid_scenario_path)

    assert scenario.scene_by_id(2).id == 2
    with pytest.raises(KeyError):
        scenario.scene_by_id(99)
    assert scenario.estimated_narration_seconds() > 0
