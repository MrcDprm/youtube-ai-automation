"""Word-synced ASS captions: karaoke fill for Zenn stories, a moving highlight for Shorts."""

from __future__ import annotations

from pathlib import Path

from modules.interfaces import WordCue
from modules.subtitle import SubtitleError, ass_colour, format_ass_timestamp
from utils.fs import atomic_write_text
from utils.text import upper_text

__all__ = ["word_cues_to_highlight_ass", "word_cues_to_karaoke_ass", "write_karaoke_ass"]

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
    uppercase: bool = False,
    language: str | None = None,
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
        uppercase: Show every word in capitals, as the subtitle settings ask.
        language: The narration's language code, so capitals follow its casing rules.

    Returns:
        Full ASS file contents.
    """
    lines = [
        _header(
            play_res_x=play_res_x,
            play_res_y=play_res_y,
            font_name=font_name,
            font_size=font_size,
            primary=primary,
            accent=accent,
            margin_v=margin_v,
            outline=outline,
        )
    ]
    for group in _group_words(word_cues, max_chars=max_chars_per_line, max_lines=max_lines):
        if not group:
            continue
        start = group[0].start
        end = group[-1].end
        text = _karaoke_text(group, uppercase=uppercase, language=language)
        lines.append(
            "Dialogue: 0,"
            f"{format_ass_timestamp(start)},{format_ass_timestamp(end)},"
            f"Karaoke,,0,0,0,,{text}\n"
        )
    return "".join(lines)


def word_cues_to_highlight_ass(
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
    uppercase: bool = False,
    language: str | None = None,
) -> str:
    """Build ASS where only the word being spoken is coloured, the Shorts caption style.

    ``\\k`` karaoke fills words one after another and leaves them filled. Short-form video
    instead keeps the whole line in one colour and moves a highlight from word to word, so
    every word gets its own dialogue event that repeats the line with that word recoloured.
    Each event lasts until the next word starts, so the line stays put between words. No
    event may run past the next one's start either: libass stacks overlapping events, and
    the line would jump up for a moment.

    Args:
        word_cues: Timeline-ordered word timings from Edge TTS.
        play_res_x: Script play-res width.
        play_res_y: Script play-res height.
        font_name: Installed font family name.
        font_size: Caption size in points.
        primary: Colour of the words not being spoken.
        accent: Colour of the word being spoken.
        margin_v: Bottom margin in pixels.
        outline: Outline width.
        max_chars_per_line: Soft wrap budget per displayed line.
        max_lines: Maximum lines per dialogue event.
        uppercase: Show every word in capitals.
        language: The narration's language code, so capitals follow its casing rules.

    Returns:
        Full ASS file contents.
    """
    lines = [
        _header(
            play_res_x=play_res_x,
            play_res_y=play_res_y,
            font_name=font_name,
            font_size=font_size,
            primary=primary,
            accent=accent,
            margin_v=margin_v,
            outline=outline,
        )
    ]
    colour = _inline_colour(accent)
    groups = _group_words(word_cues, max_chars=max_chars_per_line, max_lines=max_lines)
    for group_index, group in enumerate(groups):
        tokens = [_ass_safe(_shown(word.text, uppercase, language)) for word in group]
        next_line = groups[group_index + 1][0].start if group_index + 1 < len(groups) else None
        for index, word in enumerate(group):
            start = word.start
            if index + 1 < len(group):
                end = group[index + 1].start
            elif next_line is not None:
                end = min(word.end, next_line)
            else:
                end = word.end
            if end <= start:
                # A word that starts as the next one does has no moment of its own.
                continue
            text = " ".join(
                f"{{\\c{colour}}}{token}{{\\r}}" if position == index else token
                for position, token in enumerate(tokens)
            )
            lines.append(
                "Dialogue: 0,"
                f"{format_ass_timestamp(start)},{format_ass_timestamp(end)},"
                f"Karaoke,,0,0,0,,{text}\n"
            )
    return "".join(lines)


def _header(
    *,
    play_res_x: int,
    play_res_y: int,
    font_name: str,
    font_size: int,
    primary: str,
    accent: str,
    margin_v: int,
    outline: int,
) -> str:
    """The script info, the one caption style and the events header shared by both builders."""
    return (
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
        f"Style: Karaoke,{font_name},{font_size},{ass_colour(primary)},{ass_colour(accent)},"
        f"&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,{outline},0,2,40,40,{margin_v},1\n"
        "\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )


def _inline_colour(hex_color: str) -> str:
    """Turn ``#RRGGBB`` into the ``&HBBGGRR&`` form an inline ``\\c`` tag takes."""
    return ass_colour(hex_color).replace("&H00", "&H", 1) + "&"


def _shown(text: str, uppercase: bool, language: str | None) -> str:
    """The word as it appears on screen."""
    return upper_text(text, language) if uppercase else text


def _ass_safe(token: str) -> str:
    """Keep spoken text from being read as ASS markup.

    Braces would open an override block and a backslash would start a tag such as ``\\N``,
    so braces are escaped and backslashes, which narration never needs, are dropped.
    """
    return token.replace("\\", "").replace("{", r"\{").replace("}", r"\}")


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


def _karaoke_text(
    words: list[WordCue],
    *,
    uppercase: bool = False,
    language: str | None = None,
) -> str:
    parts: list[str] = []
    for index, word in enumerate(words):
        duration_cs = max(1, int(round(word.duration * 100.0)))
        token = _ass_safe(_shown(word.text, uppercase, language))
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
