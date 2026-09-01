"""Narration language packs: voices, locales and duration estimates.

Script prompts and TTS voices must not hard-code Turkish. A pack is looked up from a
language code (``tr``, ``en``, ``es``); unknown codes fall back to English names in the
prompt and to the Turkish voice pool only when the code is ``tr``. Adding a language later
is a new pack, not a new editor.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Final

from config.constants import NARRATION_CHARS_PER_SECOND

__all__ = [
    "LANGUAGE_NAMES",
    "LanguagePack",
    "apply_pronunciations",
    "chars_per_second_for",
    "get_language_pack",
    "language_display_name",
    "pick_voice",
]


LANGUAGE_NAMES: Final[dict[str, str]] = {
    "tr": "Turkish",
    "en": "English",
    "es": "Spanish",
    "de": "German",
    "fr": "French",
    "it": "Italian",
    "ar": "Arabic",
    "ru": "Russian",
}


@dataclass(frozen=True, slots=True)
class LanguagePack:
    """Everything that changes when the spoken language changes.

    Attributes:
        code: Short language code such as ``tr``.
        locale: BCP-47 locale used to filter edge-tts voices, for example ``tr-TR``.
        voices: Preferred Neural voices, first-best. Selection is hashed from the project id
            so a re-render of the same scenario keeps the same voice.
        chars_per_second: Used only to size ``max_duration_seconds`` and chapter length.
        youtube_language: Value written to ``youtube.default_language``.
        pronunciations: Whole-word substitutions applied before TTS so names and acronyms
            are spoken correctly.
    """

    code: str
    locale: str
    voices: tuple[str, ...]
    chars_per_second: float
    youtube_language: str
    pronunciations: tuple[tuple[str, str], ...] = ()


_PACKS: Final[dict[str, LanguagePack]] = {
    "tr": LanguagePack(
        code="tr",
        locale="tr-TR",
        voices=("tr-TR-AhmetNeural", "tr-TR-EmelNeural"),
        chars_per_second=NARRATION_CHARS_PER_SECOND,
        youtube_language="tr",
        pronunciations=(
            ("John McCarthy", "Con Mekarti"),
            ("McCarthy", "Mekarti"),
            ("Dartmouth", "Dartmut"),
            ("OpenAI", "Open ey ay"),
            ("ChatGPT", "Çet ci pi ti"),
            ("GPU", "ci pi yu"),
            ("CPU", "si pi yu"),
            ("IBM", "ay bi em"),
            ("MIT", "em ay ti"),
            ("NASA", "nasa"),
        ),
    ),
    "en": LanguagePack(
        code="en",
        locale="en-US",
        voices=("en-US-GuyNeural", "en-US-JennyNeural", "en-US-AriaNeural"),
        chars_per_second=15.0,
        youtube_language="en",
        pronunciations=(
            ("GPU", "G P U"),
            ("CPU", "C P U"),
            ("IBM", "I B M"),
            ("MIT", "M I T"),
        ),
    ),
    "es": LanguagePack(
        code="es",
        locale="es-ES",
        voices=("es-ES-AlvaroNeural", "es-ES-ElviraNeural"),
        chars_per_second=14.5,
        youtube_language="es",
    ),
}

_DEFAULT_PACK: Final[LanguagePack] = _PACKS["tr"]


def get_language_pack(language: str) -> LanguagePack:
    """Return the pack for ``language``, defaulting to Turkish.

    Args:
        language: A short code or a BCP-47 tag such as ``en-US``.

    Returns:
        The matching :class:`LanguagePack`, or the Turkish pack when unknown.
    """
    code = language.strip().lower().replace("_", "-")
    if code in _PACKS:
        return _PACKS[code]
    prefix = code.split("-", 1)[0]
    return _PACKS.get(prefix, _DEFAULT_PACK)


def language_display_name(language: str) -> str:
    """Spell out a language code for a model prompt.

    Args:
        language: A short code or BCP-47 tag.

    Returns:
        An English language name, or the original string when unknown.
    """
    code = language.strip().lower().replace("_", "-")
    prefix = code.split("-", 1)[0]
    return LANGUAGE_NAMES.get(prefix, language.strip())


def chars_per_second_for(language: str) -> float:
    """Reading-speed estimate used to size generated scenarios.

    Args:
        language: A short code or BCP-47 tag.

    Returns:
        Characters per second.
    """
    return get_language_pack(language).chars_per_second


def apply_pronunciations(text: str, language: str) -> str:
    """Replace names and acronyms with speakable forms for ``language``.

    Longer keys win so ``John McCarthy`` is not partially eaten by ``McCarthy``.

    Args:
        text: Narration after abbreviation expansion.
        language: Narration language code.

    Returns:
        Text with pack substitutions applied.
    """
    spoken = text
    for source, replacement in sorted(
        get_language_pack(language).pronunciations, key=lambda item: len(item[0]), reverse=True
    ):
        spoken = spoken.replace(source, replacement)
    return spoken


def pick_voice(
    language: str,
    project_id: str,
    *,
    override: str | None = None,
    available: tuple[str, ...] | None = None,
) -> str:
    """Choose one Neural voice for a video.

    Args:
        language: Narration language code.
        project_id: Hashed so the same project always draws the same voice.
        override: Explicit voice name; wins when non-empty.
        available: Optional live ``list_voices`` names. Pack entries not in this set are
            skipped. The full pack is used when ``available`` is ``None`` or empty.

    Returns:
        An edge-tts voice short name.
    """
    if override and override.strip():
        return override.strip()

    pack = get_language_pack(language)
    pool = pack.voices
    if available:
        allowed = {name.casefold() for name in available}
        filtered = tuple(name for name in pack.voices if name.casefold() in allowed)
        if filtered:
            pool = filtered

    digest = hashlib.sha256(f"{pack.code}:{project_id}".encode()).digest()
    index = int.from_bytes(digest[:2], "big") % len(pool)
    return pool[index]
