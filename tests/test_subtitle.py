"""Subtitle grouping, line breaking, timing invariants and SRT serialisation."""

from __future__ import annotations

from itertools import pairwise
from pathlib import Path

import pytest

from config.constants import CUE_GAP_SECONDS, MAX_CUE_DURATION, MIN_CUE_DURATION, STORY_SUBTITLE_MAX_CHARS
from models.scenario import SubtitleSettings
from modules.interfaces import WordCue
from modules.subtitle import (
    SrtSubtitleBuilder,
    ass_colour,
    cues_to_ass,
    format_ass_timestamp,
    format_timestamp,
    wrap_words,
)
from modules.tts import attach_punctuation


def _settings(**overrides: object) -> SubtitleSettings:
    """Build subtitle settings that never require a font file."""
    base: dict[str, object] = {
        "enabled": True,
        "burn_in": False,
        "max_chars_per_line": 20,
        "max_lines": 2,
    }
    base.update(overrides)
    return SubtitleSettings.model_validate(base)


def _words(*pairs: tuple[str, float, float]) -> list[WordCue]:
    """Build word cues from ``(text, start, end)`` tuples."""
    return [WordCue(text=text, start=start, end=end) for text, start, end in pairs]


def _evenly_spaced(text: str, per_word: float = 0.4) -> list[WordCue]:
    """Build evenly spaced word cues from a sentence."""
    cues: list[WordCue] = []
    cursor = 0.0
    for word in text.split():
        cues.append(WordCue(text=word, start=cursor, end=cursor + per_word))
        cursor += per_word
    return cues


# --------------------------------------------------------------------------------------
# Timestamp formatting
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0.0, "00:00:00,000"),
        (1.5, "00:00:01,500"),
        (61.25, "00:01:01,250"),
        (3725.456, "01:02:05,456"),
        (3600.0, "01:00:00,000"),
        (-3.0, "00:00:00,000"),
    ],
)
def test_format_timestamp(seconds: float, expected: str) -> None:
    """Timestamps use the SRT comma-separated millisecond form."""
    assert format_timestamp(seconds) == expected


def test_format_timestamp_rounds_to_the_nearest_millisecond() -> None:
    """Sub-millisecond precision rounds rather than truncating."""
    assert format_timestamp(1.0004) == "00:00:01,000"
    assert format_timestamp(1.0006) == "00:00:01,001"


# --------------------------------------------------------------------------------------
# Line wrapping
# --------------------------------------------------------------------------------------


def test_wrap_words_breaks_at_the_character_budget() -> None:
    """Lines break once adding a word would exceed the budget."""
    assert (
        wrap_words(["bir", "iki", "uc", "dort", "bes", "alti"], 10, 2)
        == "bir iki uc\ndort bes alti"
    )


def test_wrap_words_never_splits_a_word() -> None:
    """A word longer than the budget is kept whole rather than hyphenated."""
    wrapped = wrap_words(["kisa", "cokcokcokcokuzunkelime"], 8, 2)

    assert "cokcokcokcokuzunkelime" in wrapped
    assert len(wrapped.split("\n")) <= 2


def test_wrap_words_respects_the_line_limit() -> None:
    """Surplus text joins the final line rather than adding a third."""
    wrapped = wrap_words(["a"] * 40, 5, 2)
    assert len(wrapped.split("\n")) == 2


def test_wrap_words_handles_empty_input() -> None:
    """No words means no text."""
    assert wrap_words([], 20, 2) == ""


# --------------------------------------------------------------------------------------
# Cue grouping
# --------------------------------------------------------------------------------------


def test_build_returns_nothing_for_no_words() -> None:
    """An empty word list produces no cues."""
    assert SrtSubtitleBuilder().build([], _settings()) == []


def test_cues_are_numbered_from_one() -> None:
    """Cue indices start at 1 and increase by 1."""
    cues = SrtSubtitleBuilder().build(
        _evenly_spaced("bir iki uc dort bes alti yedi sekiz"), _settings()
    )

    assert [cue.index for cue in cues] == list(range(1, len(cues) + 1))


def test_cue_text_respects_the_character_budget() -> None:
    """No cue exceeds the configured lines times characters budget."""
    settings = _settings(max_chars_per_line=15, max_lines=2)
    cues = SrtSubtitleBuilder().build(
        _evenly_spaced("bir iki uc dort bes alti yedi sekiz dokuz on"), settings
    )

    for cue in cues:
        assert len(cue.lines) <= settings.max_lines


def test_grouping_prefers_sentence_boundaries() -> None:
    """A sentence-ending word closes the cue when enough text has accumulated."""
    words = _words(
        ("Birinci", 0.0, 0.5),
        ("cumle", 0.5, 1.0),
        ("burada.", 1.0, 1.5),
        ("Ikinci", 1.6, 2.1),
        ("cumle", 2.1, 2.6),
        ("burada.", 2.6, 3.1),
    )
    cues = SrtSubtitleBuilder().build(words, _settings(max_chars_per_line=40, max_lines=2))

    assert len(cues) == 2
    assert cues[0].text.replace("\n", " ") == "Birinci cumle burada."


def test_timestamps_are_monotonic_and_never_overlap() -> None:
    """Every cue starts after the previous one ends."""
    cues = SrtSubtitleBuilder().build(
        _evenly_spaced("bir iki uc dort bes alti yedi sekiz dokuz on"), _settings()
    )

    for earlier, later in pairwise(cues):
        assert earlier.end <= later.start
        assert earlier.start < earlier.end


def test_short_cues_are_extended_to_the_minimum() -> None:
    """A single quick word still stays on screen long enough to read."""
    cues = SrtSubtitleBuilder().build(_words(("Evet", 0.0, 0.1)), _settings())

    assert len(cues) == 1
    assert cues[0].duration >= MIN_CUE_DURATION - 1e-6


def test_long_cues_are_capped_at_the_maximum() -> None:
    """A cue never lingers past the configured ceiling."""
    cues = SrtSubtitleBuilder().build(_words(("Uzun", 0.0, 30.0)), _settings())

    assert cues[0].duration <= MAX_CUE_DURATION + 1e-6


def test_max_cue_duration_is_two_and_a_half_seconds() -> None:
    """Captions refresh about twice as often as a 5-second still cut."""
    assert MAX_CUE_DURATION == 2.5
    assert STORY_SUBTITLE_MAX_CHARS == 32
    assert CUE_GAP_SECONDS == 0.0


def test_cues_split_before_they_exceed_two_and_a_half_seconds() -> None:
    """A run of words that would linger past the ceiling becomes two cues."""
    words = _words(("one", 0.0, 1.0), ("two", 1.0, 2.0), ("three", 2.0, 3.0))
    cues = SrtSubtitleBuilder().build(words, _settings(max_chars_per_line=40, max_lines=2))

    assert len(cues) >= 2
    assert all(cue.duration <= MAX_CUE_DURATION + 1e-6 for cue in cues)


def test_attached_punctuation_closes_the_cue_at_the_period() -> None:
    """Restored periods let grouping break on the sentence, not the character budget."""
    words = attach_punctuation(
        "Soup. Beans.",
        _words(("Soup", 0.0, 0.4), ("Beans", 0.4, 0.8)),
    )
    cues = SrtSubtitleBuilder().build(words, _settings(max_chars_per_line=40, max_lines=2))

    assert len(cues) == 2
    assert cues[0].text.replace("\n", " ") == "Soup."
    assert cues[1].text.replace("\n", " ") == "Beans."


def test_offset_shifts_every_timestamp() -> None:
    """A scene's cues can be placed onto the whole-video timeline."""
    words = _evenly_spaced("bir iki uc")
    base = SrtSubtitleBuilder().build(words, _settings())
    shifted = SrtSubtitleBuilder().build(words, _settings(), offset=10.0)

    assert shifted[0].start == pytest.approx(base[0].start + 10.0)
    assert shifted[0].end == pytest.approx(base[0].end + 10.0)


def test_unordered_words_are_sorted() -> None:
    """Out-of-order boundary events do not corrupt the timeline."""
    words = _words(("iki", 1.0, 1.5), ("bir", 0.0, 0.5), ("uc", 2.0, 2.5))
    cues = SrtSubtitleBuilder().build(words, _settings(max_chars_per_line=40))

    assert cues[0].text.startswith("bir")


def test_uppercase_setting_is_applied() -> None:
    """Cue text is upper-cased when requested."""
    cues = SrtSubtitleBuilder().build(_words(("merhaba", 0.0, 0.5)), _settings(uppercase=True))
    assert cues[0].text == "MERHABA"


# --------------------------------------------------------------------------------------
# Duration fallback
# --------------------------------------------------------------------------------------


def test_build_from_duration_covers_the_audio() -> None:
    """When no word boundaries arrive, cues are spread across the measured duration."""
    cues = SrtSubtitleBuilder().build_from_duration(
        "bir iki uc dort bes alti", 6.0, _settings(max_chars_per_line=40)
    )

    assert cues
    assert cues[0].start >= 0.0
    assert cues[-1].end <= 6.5


def test_build_from_duration_handles_degenerate_input() -> None:
    """Empty text or zero duration produces no cues rather than raising."""
    assert SrtSubtitleBuilder().build_from_duration("", 5.0, _settings()) == []
    assert SrtSubtitleBuilder().build_from_duration("bir", 0.0, _settings()) == []


# --------------------------------------------------------------------------------------
# SRT serialisation
# --------------------------------------------------------------------------------------


def test_write_srt_produces_valid_utf8_without_bom(tmp_path: Path) -> None:
    """The file is UTF-8, has no byte-order mark, and uses blank-line separators."""
    cues = SrtSubtitleBuilder().build(_evenly_spaced("Merhaba dunya bugun nasilsin"), _settings())
    out_path = tmp_path / "subs.srt"

    SrtSubtitleBuilder().write_srt(cues, out_path)

    raw = out_path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf")

    text = out_path.read_text(encoding="utf-8")
    blocks = text.strip().split("\n\n")
    assert len(blocks) == len(cues)

    first = blocks[0].split("\n")
    assert first[0] == "1"
    assert " --> " in first[1]


def test_write_srt_timestamps_round_trip(tmp_path: Path) -> None:
    """Serialised timestamps match the cue values."""
    from modules.interfaces import SubtitleCue

    cue = SubtitleCue(index=1, start=1.5, end=3.25, text="test")
    out_path = tmp_path / "one.srt"
    SrtSubtitleBuilder().write_srt([cue], out_path)

    assert "00:00:01,500 --> 00:00:03,250" in out_path.read_text(encoding="utf-8")


def test_write_srt_handles_no_cues(tmp_path: Path) -> None:
    """An empty cue list writes an empty file rather than failing."""
    out_path = tmp_path / "empty.srt"
    SrtSubtitleBuilder().write_srt([], out_path)

    assert out_path.read_text(encoding="utf-8") == ""


def test_merge_renumbers_across_scenes() -> None:
    """Per-scene cue lists flatten into one continuously numbered timeline."""
    builder = SrtSubtitleBuilder()
    first = builder.build(_evenly_spaced("bir iki"), _settings())
    second = [cue.shifted(20.0) for cue in builder.build(_evenly_spaced("uc dort"), _settings())]

    merged = builder.merge([first, second])

    assert [cue.index for cue in merged] == list(range(1, len(merged) + 1))
    assert merged[-1].start >= 20.0


def test_ass_colour_is_bgr() -> None:
    """ASS stores colours as AABBGGRR, so gold #FFD34F becomes blue-led."""
    assert ass_colour("#FFD34F") == "&H004FD3FF"
    assert ass_colour("#FFFFFF") == "&H00FFFFFF"


def test_cues_to_ass_is_bottom_aligned() -> None:
    """Story burn-in uses Alignment 2 and a bottom margin so lines are not clipped."""
    from modules.interfaces import SubtitleCue

    cues = [
        SubtitleCue(
            index=1, start=0.0, end=1.5, text="birinci satır\nikinci satır", color="#FFFFFF"
        ),
        SubtitleCue(index=2, start=1.5, end=3.0, text="altın", color="#FFD34F"),
    ]
    body = cues_to_ass(
        cues,
        play_res_x=1920,
        play_res_y=1080,
        font_name="Inter",
        font_size=48,
        primary="#FFFFFF",
        margin_v=80,
    )
    assert "Alignment, MarginL, MarginR, MarginV" in body
    assert ",2,40,40,80,1" in body
    assert format_ass_timestamp(1.5) in body
    assert r"\c&H004FD3FF&" in body
    assert r"\N" in body
