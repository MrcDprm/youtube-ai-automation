"""Language-aware text casing.

Python's ``str.upper`` follows the default Unicode mapping, which is wrong for Turkish and
Azerbaijani: ``"iyi".upper()`` gives ``"IYI"`` where a Turkish reader expects ``"İYİ"``.
Captions and thumbnail hooks are set in capitals, so they need the language's own rules.
"""

from __future__ import annotations

__all__ = ["is_turkic", "upper_text"]

_TURKIC_LANGUAGES = frozenset({"tr", "az"})
_TURKIC_UPPER = str.maketrans({"i": "İ", "ı": "I"})


def is_turkic(language: str | None) -> bool:
    """Report whether a language code uses the dotted and dotless i.

    Args:
        language: A code such as ``"tr"``, ``"tr-TR"`` or ``"az_AZ"``. ``None`` and blank
            values count as not Turkic.

    Returns:
        ``True`` for Turkish and Azerbaijani.
    """
    if not language:
        return False
    primary = language.strip().lower().replace("_", "-").split("-", 1)[0]
    return primary in _TURKIC_LANGUAGES


def upper_text(text: str, language: str | None = None) -> str:
    """Uppercase ``text`` with the casing rules of ``language``.

    Args:
        text: Any text.
        language: The text's language code. Turkish and Azerbaijani map ``i`` to ``İ``.

    Returns:
        The uppercased text.
    """
    if is_turkic(language):
        return text.translate(_TURKIC_UPPER).upper()
    return text.upper()
