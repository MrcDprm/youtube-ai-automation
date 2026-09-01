"""Zenn beat packing and pose-rule assignment. No network."""

from __future__ import annotations

from modules.interfaces import WordCue
from zenn.segmentation import assign_tags, cues_to_beats


def _cues(*pairs: tuple[str, float, float]) -> list[WordCue]:
    """Build word cues from ``(text, start, end)`` tuples."""
    return [WordCue(text=text, start=start, end=end) for text, start, end in pairs]


def test_empty_cues_yield_no_beats() -> None:
    """No speech means no holds."""
    assert cues_to_beats([]) == []


def test_packs_near_target_two_point_two() -> None:
    """Ten 0.4s words split around the 2.2s target, not by word count."""
    cues = _cues(*((f"w{i}", i * 0.4, (i + 1) * 0.4) for i in range(10)))
    beats = cues_to_beats(cues)
    assert len(beats) == 2
    assert beats[0].start_ms == 0
    assert beats[0].end_ms == 2400
    assert beats[1].start_ms == 2400
    assert beats[1].end_ms == 4000
    first_hold = (beats[0].end_ms - beats[0].start_ms) / 1000.0
    assert 2.2 <= first_hold <= 4.0


def test_never_holds_longer_than_four_seconds() -> None:
    """A stream without sentence breaks still cuts at the 4s ceiling."""
    cues = _cues(*((f"w{i}", i * 0.5, (i + 1) * 0.5) for i in range(10)))
    beats = cues_to_beats(cues)
    for beat in beats:
        assert beat.duration_ms <= 4000


def test_single_word_longer_than_four_seconds_is_kept() -> None:
    """One over-long WordCue cannot be split; it is the documented exception."""
    beats = cues_to_beats(_cues(("loooooong", 0.0, 5.0)))
    assert len(beats) == 1
    assert beats[0].duration_ms == 5000
    assert beats[0].text == "loooooong"


def test_short_tail_merges_into_previous() -> None:
    """A leftover shorter than 1s is not a flicker frame."""
    cues = _cues(
        *[(f"a{i}", i * 0.4, (i + 1) * 0.4) for i in range(6)],
        ("tail", 2.4, 2.8),
    )
    beats = cues_to_beats(cues)
    assert len(beats) == 1
    assert beats[0].end_ms == 2800
    assert "tail" in beats[0].text


def test_sentence_end_cuts_after_one_second() -> None:
    """A period after the 1s floor is a preferred cut."""
    cues = _cues(
        ("Wait.", 0.0, 1.1),
        ("Next", 1.1, 2.0),
        ("word", 2.0, 2.8),
    )
    beats = cues_to_beats(cues)
    assert beats[0].text == "Wait."
    assert beats[0].end_ms == 1100
    assert beats[1].start_ms == 1100


def test_araba_selects_garage() -> None:
    """Turkish car keyword maps to the garage background."""
    _, bg = assign_tags("Bu araba 1908 model")
    assert bg == "garage"


def test_kostu_selects_running() -> None:
    """Turkish ran keyword maps to the running pose."""
    pose, _bg = assign_tags("Adam kaçtı ve koştu")
    assert pose == "running"


def test_no_keyword_uses_defaults() -> None:
    """Unmatched prose uses standing on the road default."""
    pose, bg = assign_tags("The leftover is a pebble.")
    assert pose == "standing"
    assert bg == "road"


def test_fallback_runs_only_when_rules_miss() -> None:
    """Injected predictor is unused when a keyword already hit."""
    calls: list[str] = []

    def predictor(text: str) -> tuple[str, str]:
        calls.append(text)
        return "thinking", "office"

    _, bg = assign_tags("the motor in the garage", fallback=predictor)
    assert bg == "garage"
    assert calls == []
    pose2, bg2 = assign_tags("nothing matches here", fallback=predictor)
    assert pose2 == "thinking"
    assert bg2 == "office"
    assert calls == ["nothing matches here"]


def test_beat_gets_visual_prompt_and_tags() -> None:
    """Packed beats carry pose, background, and a stick-figure prompt."""
    cues = _cues(("The", 0.0, 0.4), ("car", 0.4, 1.2), ("ran.", 1.2, 2.0))
    beats = cues_to_beats(cues)
    assert len(beats) == 1
    assert beats[0].bg_tag == "garage"
    assert beats[0].pose_tag == "running"
    assert "pose running" in beats[0].visual_prompt
    assert "background garage" in beats[0].visual_prompt


def test_scene_visuals_carry_chapter_background() -> None:
    """Chapter context keeps garage bg when a beat fragment has no car keyword."""
    from zenn.segmentation.beats import apply_scene_visuals, cues_to_beats

    cues = _cues(
        ("The", 0.0, 0.3),
        ("car", 0.3, 0.8),
        ("moved.", 0.8, 1.2),
        ("Then", 1.2, 1.5),
        ("silence.", 1.5, 2.0),
    )
    beats = apply_scene_visuals(cues_to_beats(cues), "Gasoline at the pump and the Ford motor.")
    assert beats[0].bg_tag == "garage"
    assert beats[-1].bg_tag == "garage"
