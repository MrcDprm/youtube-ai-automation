"""Word-sync karaoke ASS captions for Zenn."""

from __future__ import annotations

from pathlib import Path

from modules.interfaces import WordCue
from modules.subtitle import SubtitleError, ass_colour, format_ass_timestamp
from utils.fs import atomic_write_text

__all__ = ["word_cues_to_karaoke_ass", "write_karaoke_ass"]

_SENTENCE_END = frozenset(".!?…")


def word_cues_to_karaoke_ass(
    word_cues: list[WordCue],
    *,
    play_res_x: int,
    play_res_y: int,
    font_name: str,
    font_size: int,
    primary: str = "#FFFFFF",
    accent: str = "#FFD600",
    margin_v: int = 72,
    outline: int = 4,
    max_chars_per_line: int = 32,
    max_lines: int = 2,
) -> str:
    """Build ASS with ``\\k`` tags so the active word highlights in yellow.

    Args:
        word_cues: Timeline-ordered word timings from Edge TTS.
        play_res_x: Script play-res width.
        play_res_y: Script play-res height.
        font_name: Installed font family name.
        font_size: Caption size in points.
        primary: Default fill colour.
        accent: Highlight colour while a word is spoken.
        margin_v: Bottom margin in pixels.
        outline: Outline width.
        max_chars_per_line: Soft wrap budget per displayed line.
        max_lines: Maximum lines per dialogue event.

    Returns:
        Full ASS file contents.
    """
    default = ass_colour(primary)
    highlight = ass_colour(accent)
    header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        f"PlayResX: {play_res_x}\n"
        f"PlayResY: {play_res_y}\n"
        "WrapStyle: 0\n"
        "ScaledBorderAndShadow: yes\n"
        "\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
        "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
        "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Karaoke,{font_name},{font_size},{default},{highlight},&H00000000,&H00000000,"
        f"-1,0,0,0,100,100,0,0,1,{outline},0,2,40,40,{margin_v},1\n"
        "\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    lines = [header]
    for group in _group_words(word_cues, max_chars=max_chars_per_line, max_lines=max_lines):
        if not group:
            continue
        start = group[0].start
        end = group[-1].end
        text = _karaoke_text(group)
        lines.append(
            "Dialogue: 0,"
            f"{format_ass_timestamp(start)},{format_ass_timestamp(end)},"
            f"Karaoke,,0,0,0,,{text}\n"
        )
    return "".join(lines)


def write_karaoke_ass(word_cues: list[WordCue], out_path: Path, body: str) -> Path:
    """Write a karaoke ASS script to disk."""
    try:
        atomic_write_text(out_path, body, encoding="utf-8")
    except OSError as exc:
        raise SubtitleError(
            f"Could not write karaoke subtitles to {out_path}: {exc}",
            hint="Check that the output directory exists and is writable.",
        ) from exc
    return out_path


def _karaoke_text(words: list[WordCue]) -> str:
    parts: list[str] = []
    for index, word in enumerate(words):
        duration_cs = max(1, int(round(word.duration * 100.0)))
        token = word.text.replace("{", r"\{").replace("}", r"\}")
        prefix = "" if index == 0 else " "
        parts.append(f"{prefix}{{\\k{duration_cs}}}{token}")
    return "".join(parts)


def _group_words(
    words: list[WordCue],
    *,
    max_chars: int,
    max_lines: int,
) -> list[list[WordCue]]:
    if not words:
        return []

    groups: list[list[WordCue]] = []
    current: list[WordCue] = []
    current_chars = 0
    line_count = 1

    for word in words:
        addition = len(word.text) + (1 if current else 0)
        next_chars = current_chars + addition
        if current and (next_chars > max_chars or _ends_sentence(current[-1].text)):
            groups.append(current)
            current = [word]
            current_chars = len(word.text)
            line_count = 1
            continue
        if current and line_count >= max_lines and _ends_sentence(word.text):
            groups.append(current)
            current = [word]
            current_chars = len(word.text)
            line_count = 1
            continue
        current.append(word)
        current_chars = next_chars
        if current_chars >= max_chars and _ends_sentence(word.text):
            groups.append(current)
            current = []
            current_chars = 0
            line_count = 1

    if current:
        groups.append(current)
    return groups


def _ends_sentence(word: str) -> bool:
    stripped = word.rstrip("\"')]}»”’")
    return bool(stripped) and stripped[-1] in _SENTENCE_END
