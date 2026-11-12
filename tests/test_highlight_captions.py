"""Shorts captions that highlight the word being spoken.

The ASS builder is checked event by event. A real, tiny scene is then rendered to prove that
the editor burns the captions in through ffmpeg and that the highlight moves from one word to
the next.
"""

from __future__ import annotations

import itertools
import re
import subprocess
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from config.constants import PROJECT_ROOT
from models.scenario import Scene, SubtitleSettings
from modules.editor import MoviePyEditor
from modules.interfaces import ScenePlan, SubtitleCue, WordCue
from modules.subtitle import ass_font_size
from utils.media import ffmpeg_executable
from zenn.captions.karaoke_ass import word_cues_to_highlight_ass, word_cues_to_karaoke_ass

ACTIVE = "{\\c&H00D6FF&}"
"""The default accent #FFD600 as an inline ASS colour tag."""

FONT = PROJECT_ROOT / "assets" / "fonts" / "Anton-Regular.ttf"


def _build(words: list[WordCue], **overrides: Any) -> str:
    options: dict[str, Any] = {
        "play_res_x": 1080,
        "play_res_y": 1920,
        "font_name": "Anton",
        "font_size": 80,
    }
    options.update(overrides)
    return word_cues_to_highlight_ass(words, **options)


def _events(body: str) -> list[tuple[str, str, str]]:
    """The start, end and text of every dialogue line."""
    events = []
    for line in body.splitlines():
        if line.startswith("Dialogue:"):
            fields = line.split(",", 9)
            events.append((fields[1], fields[2], fields[9]))
    return events


def _seconds(stamp: str) -> float:
    hours, minutes, seconds = stamp.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


# --------------------------------------------------------------------------------------
# The ASS builder
# --------------------------------------------------------------------------------------


def test_each_word_gets_an_event_that_lasts_until_the_next_word() -> None:
    """The line stays on screen through the pauses between words."""
    words = [
        WordCue(text="Bir", start=0.0, end=0.3),
        WordCue(text="iki", start=0.5, end=0.8),
        WordCue(text="üç.", start=1.0, end=1.4),
    ]

    events = _events(_build(words))

    assert [(start, end) for start, end, _ in events] == [
        ("0:00:00.00", "0:00:00.50"),
        ("0:00:00.50", "0:00:01.00"),
        ("0:00:01.00", "0:00:01.40"),
    ]


def test_only_the_spoken_word_is_coloured() -> None:
    """Every event repeats the whole line and recolours exactly one word."""
    words = [
        WordCue(text="Bir", start=0.0, end=0.3),
        WordCue(text="iki", start=0.5, end=0.8),
        WordCue(text="üç.", start=1.0, end=1.4),
    ]

    texts = [text for _, _, text in _events(_build(words))]

    assert texts == [
        f"{ACTIVE}Bir{{\\r}} iki üç.",
        f"Bir {ACTIVE}iki{{\\r}} üç.",
        f"Bir iki {ACTIVE}üç.{{\\r}}",
    ]


def test_the_accent_colour_is_configurable() -> None:
    body = _build([WordCue(text="kırmızı", start=0.0, end=0.5)], accent="#FF0000")

    assert _events(body)[0][2] == "{\\c&H0000FF&}kırmızı{\\r}"


def test_a_new_line_starts_after_a_sentence_and_events_never_overlap() -> None:
    """libass stacks overlapping events, so the last word of a line ends when the next begins.

    Here the speech engine reports the second sentence starting before the first one's last
    word ends. Without the cap both lines would show at once, one pushed above the other.
    """
    words = [
        WordCue(text="Bu", start=0.0, end=0.2),
        WordCue(text="bir.", start=0.25, end=0.7),
        WordCue(text="Sonra", start=0.6, end=0.9),
        WordCue(text="iki.", start=1.0, end=1.3),
    ]

    events = _events(_build(words))

    assert [text.replace(ACTIVE, "*").replace("{\\r}", "") for _, _, text in events] == [
        "*Bu bir.",
        "Bu *bir.",
        "*Sonra iki.",
        "Sonra *iki.",
    ]
    assert events[1][1] == "0:00:00.60"
    times = [(_seconds(start), _seconds(end)) for start, end, _ in events]
    for (_, previous_end), (next_start, _) in itertools.pairwise(times):
        assert next_start >= previous_end


def test_a_word_with_no_moment_of_its_own_is_never_highlighted() -> None:
    """A word that starts together with the next one would make a zero-length event."""
    words = [
        WordCue(text="hızlı", start=0.0, end=0.2),
        WordCue(text="ve", start=0.2, end=0.25),
        WordCue(text="net", start=0.2, end=0.6),
    ]

    events = _events(_build(words))

    assert len(events) == 2
    assert all(f"{ACTIVE}ve" not in text for _, _, text in events)
    assert all(_seconds(end) > _seconds(start) for start, end, _ in events)


def test_capitals_follow_the_language() -> None:
    """Turkish turns i into İ and ı into I; other languages keep plain I."""
    words = [WordCue(text="gizli", start=0.0, end=0.4), WordCue(text="ışık", start=0.4, end=0.8)]

    turkish = _events(_build(words, uppercase=True, language="tr"))[0][2]
    english = _events(_build(words, uppercase=True, language="en"))[0][2]

    assert turkish == f"{ACTIVE}GİZLİ{{\\r}} IŞIK"
    assert english == f"{ACTIVE}GIZLI{{\\r}} IŞIK"


def test_words_keep_their_case_unless_capitals_are_asked_for() -> None:
    body = _build([WordCue(text="Merhaba", start=0.0, end=0.5)], language="tr")

    assert _events(body)[0][2] == f"{ACTIVE}Merhaba{{\\r}}"


@pytest.mark.parametrize("builder", [word_cues_to_highlight_ass, word_cues_to_karaoke_ass])
def test_markup_in_the_narration_is_shown_as_plain_text(builder: Any) -> None:
    """Braces and backslashes would open ASS override tags such as a new line or bold."""
    words = [
        WordCue(text="{\\b1}kalın", start=0.0, end=0.4),
        WordCue(text="satır\\Nsonu", start=0.4, end=0.8),
    ]

    body = builder(words, play_res_x=1080, play_res_y=1920, font_name="Anton", font_size=80)

    for _, _, text in _events(body):
        own_tags = r"\{\\c&H[0-9A-F]{6}&\}|\{\\r\}|\{\\k\d+\}"
        visible = re.sub(own_tags, "", text)
        assert "\\N" not in visible
        assert re.sub(r"\\[{}]", "", visible).count("{") == 0
        assert "\\{b1\\}kalın" in visible
        assert "satırNsonu" in visible


def test_no_words_means_no_events() -> None:
    assert _events(_build([])) == []


# --------------------------------------------------------------------------------------
# Font size
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "size", "expected"),
    [("Anton-Regular.ttf", 92, 159), ("Inter-Bold.ttf", 60, 73)],
)
def test_ass_font_size_draws_letters_as_large_as_text_clips(
    name: str, size: int, expected: int
) -> None:
    """libass sizes the whole cell: Anton's is 1.73 em tall and Inter's 1.21 em.

    Measured against Pillow, these sizes draw capitals within a pixel of the same height.
    """
    assert ass_font_size(PROJECT_ROOT / "assets" / "fonts" / name, size) == expected


@pytest.mark.parametrize(
    "content",
    [
        b"",
        b"not a font",
        b"\x00\x01\x00\x00\x00\x05" + b"\x00" * 6,
        b"\x00\x01\x00\x00\x00\x00" + b"\x00" * 6,
    ],
    ids=["empty", "text", "cut-short", "no-tables"],
)
def test_ass_font_size_keeps_the_size_when_the_font_cannot_be_read(
    tmp_path: Path, content: bytes
) -> None:
    path = tmp_path / "broken.ttf"
    path.write_bytes(content)

    assert ass_font_size(path, 60) == 60
    assert ass_font_size(tmp_path / "missing.ttf", 60) == 60


# --------------------------------------------------------------------------------------
# The editor
# --------------------------------------------------------------------------------------

WIDTH, HEIGHT = 360, 640


def _ffmpeg(*args: str) -> bytes:
    result = subprocess.run(
        [str(ffmpeg_executable()), "-hide_banner", "-v", "error", "-y", *args],
        capture_output=True,
        check=True,
    )
    return result.stdout


@pytest.fixture
def inputs(tmp_path: Path) -> tuple[Path, Path]:
    """A silent narration and a plain black clip, so any colour in the frame is a caption."""
    narration = tmp_path / "narration.wav"
    _ffmpeg("-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "1.0", str(narration))
    clip = tmp_path / "black.mp4"
    _ffmpeg(
        "-f",
        "lavfi",
        "-i",
        f"color=c=black:size={WIDTH}x{HEIGHT}:rate=30:duration=1.5",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-pix_fmt",
        "yuv420p",
        str(clip),
    )
    return narration, clip


def _plan(tmp_path: Path, inputs: tuple[Path, Path], *, karaoke: bool) -> ScenePlan:
    narration, clip = inputs
    return ScenePlan(
        scene=Scene(id=1, narration="bir iki", search_terms=["test"], zoom_effect=False),
        audio_path=narration,
        audio_duration=1.0,
        media_paths=[clip],
        subtitle_cues=[SubtitleCue(index=1, start=0.0, end=1.0, text="bir iki")],
        target_resolution=(WIDTH, HEIGHT),
        fps=30,
        scene_gap_seconds=0.2,
        subtitles=SubtitleSettings(
            font=FONT,
            font_size=48,
            position_ratio=0.6,
            uppercase=True,
            karaoke=karaoke,
        ),
        font_path=FONT,
        output_path=tmp_path / "scene.mp4",
        word_cues=[
            WordCue(text="bir", start=0.0, end=0.4),
            WordCue(text="iki", start=0.5, end=0.9),
        ],
        language="tr",
    )


def test_the_editor_turns_subtitle_settings_into_the_caption_style(tmp_path: Path) -> None:
    """Font, size, outline, position and the language's capitals all reach the ASS file.

    Size 48 becomes 83 because libass sizes Anton's whole 1.73 em cell, not its letters.
    """
    editor = MoviePyEditor(temp_dir=tmp_path / "temp", threads=1)
    plan = _plan(tmp_path, (tmp_path / "narration.wav", tmp_path / "clip.mp4"), karaoke=True)

    ass_path, video_filter = editor._write_highlight_captions(plan)

    lines = ass_path.read_text(encoding="utf-8").splitlines()
    style = next(line for line in lines if line.startswith("Style: Karaoke,"))
    assert style.startswith("Style: Karaoke,Anton,83,&H00FFFFFF,")
    # Outline 3, alignment 2 at the bottom centre, 40 px sides, 640 * (1 - 0.6) from the bottom.
    assert style.endswith(",3,0,2,40,40,256,1")
    assert any(line.endswith(f",{ACTIVE}BİR{{\\r}} İKİ") for line in lines)
    assert video_filter.startswith("ass='") and ":fontsdir='" in video_filter
    assert ass_path.parent == tmp_path / "temp"


def _frame(path: Path, at: float) -> np.ndarray:
    raw = _ffmpeg(
        "-ss",
        str(at),
        "-i",
        str(path),
        "-frames:v",
        "1",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-",
    )
    return np.frombuffer(raw, dtype=np.uint8).reshape(HEIGHT, WIDTH, 3).astype(int)


def _columns(frame: np.ndarray) -> tuple[float, float]:
    """Mean x of the yellow pixels and of the white pixels."""
    red, green, blue = frame[..., 0], frame[..., 1], frame[..., 2]
    yellow = (red > 200) & (green > 160) & (blue < 90)
    white = (red > 200) & (green > 200) & (blue > 200)
    assert yellow.sum() > 30, "no highlighted word on screen"
    assert white.sum() > 30, "no plain word on screen"
    return float(np.nonzero(yellow)[1].mean()), float(np.nonzero(white)[1].mean())


def test_the_highlight_moves_from_word_to_word_in_the_render(
    tmp_path: Path, inputs: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    """ffmpeg draws the captions, and the coloured word follows the narration."""

    def no_text_clips(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("highlighted captions must not go through MoviePy text clips")

    monkeypatch.setattr(MoviePyEditor, "_burn_subtitles", no_text_clips)
    editor = MoviePyEditor(temp_dir=tmp_path / "temp", threads=1, preset="ultrafast")

    out = editor.build_scene(_plan(tmp_path, inputs, karaoke=True))

    first_yellow, first_white = _columns(_frame(out, 0.2))
    second_yellow, second_white = _columns(_frame(out, 0.7))
    assert first_yellow < WIDTH / 2 < first_white
    assert second_white < WIDTH / 2 < second_yellow
    assert list((tmp_path / "temp").glob("*.ass")) == []


def test_plain_captions_still_use_text_clips(
    tmp_path: Path, inputs: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without karaoke the scene keeps the earlier caption path and no ffmpeg filter."""
    calls: list[ScenePlan] = []

    def record(self: MoviePyEditor, base: Any, plan: ScenePlan, opened: list[Any]) -> Any:
        calls.append(plan)
        return base

    monkeypatch.setattr(MoviePyEditor, "_burn_subtitles", record)
    editor = MoviePyEditor(temp_dir=tmp_path / "temp", threads=1, preset="ultrafast")

    out = editor.build_scene(_plan(tmp_path, inputs, karaoke=False))

    assert len(calls) == 1
    assert int(_frame(out, 0.2).max()) < 40
