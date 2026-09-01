"""Rewrite spoken English number-words into digits for subtitle display.

TTS still says "nineteen seventy"; the burn-in can show ``1970``. Small counts in
running prose (``three men``, ``two guns``) stay words. Years, clock times, dates,
and quantities of a hundred or more become digits.
"""

from __future__ import annotations

import re

__all__ = ["display_caption_numbers"]

_ONES: dict[str, int] = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
}

_TENS: dict[str, int] = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}

_ORDINALS: dict[str, int] = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
    "eleventh": 11,
    "twelfth": 12,
    "thirteenth": 13,
    "fourteenth": 14,
    "fifteenth": 15,
    "sixteenth": 16,
    "seventeenth": 17,
    "eighteenth": 18,
    "nineteenth": 19,
    "twentieth": 20,
    "thirtieth": 30,
}

_MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)
_MONTH_INDEX = {name.lower(): name for name in _MONTHS}

_YEAR_CENTURY: dict[str, int] = {
    "fifteen": 1500,
    "sixteen": 1600,
    "seventeen": 1700,
    "eighteen": 1800,
    "nineteen": 1900,
}

_SMALL_WORDS = frozenset(_ONES) | frozenset(_TENS)
_SCALES = frozenset({"hundred", "thousand", "million"})


def display_caption_numbers(text: str) -> str:
    """Convert readable number-words in ``text`` to digits, preserving line breaks.

    Args:
        text: A subtitle cue, possibly wrapped with newlines.

    Returns:
        The same cue with years, dates, clocks, and large counts as numerals.
    """
    if not text:
        return text
    return "\n".join(_convert_line(line) for line in text.split("\n"))


def _convert_line(line: str) -> str:
    """Apply numeral rewrites to one subtitle line."""
    line = _ordinal_dates(line)
    line = _half_past(line)
    line = _year_phrases(line)
    line = _scaled_quantities(line)
    line = _measure_phrases(line)
    return line


def _unit_0_99(token: str) -> int | None:
    """Parse a 0–99 word such as ``fourteen`` or ``seventy``."""
    folded = token.casefold().replace("-", " ")
    if folded in _ONES:
        return _ONES[folded]
    if folded in _TENS:
        return _TENS[folded]
    parts = folded.split()
    if len(parts) == 2 and parts[0] in _TENS and parts[1] in _ONES and _ONES[parts[1]] < 10:
        return _TENS[parts[0]] + _ONES[parts[1]]
    if "-" in token.casefold():
        left, _, right = token.casefold().partition("-")
        if left in _TENS and right in _ONES and _ONES[right] < 10:
            return _TENS[left] + _ONES[right]
    return None


def _two_word_unit(first: str, second: str) -> int | None:
    """Parse ``seventy two`` as 72."""
    a = first.casefold()
    b = second.casefold()
    if a in _TENS and b in _ONES and _ONES[b] < 10:
        return _TENS[a] + _ONES[b]
    return None


def _format_int(value: int) -> str:
    """Render ``value`` with grouping commas when it is 1000 or more."""
    if value >= 1000:
        return f"{value:,}"
    return str(value)


def _ordinal_dates(line: str) -> str:
    """Turn ``the twelfth of November`` into ``November 12``."""
    ordinals = "|".join(sorted(_ORDINALS, key=len, reverse=True))
    months = "|".join(_MONTH_INDEX)
    pattern = re.compile(
        rf"\b(?:the\s+)?({ordinals})\s+of\s+({months})\b",
        flags=re.IGNORECASE,
    )

    def repl(match: re.Match[str]) -> str:
        day = _ORDINALS[match.group(1).casefold()]
        month = _MONTH_INDEX[match.group(2).casefold()]
        return f"{month} {day}"

    return pattern.sub(repl, line)


def _half_past(line: str) -> str:
    """Turn ``half past four`` into ``4:30``."""
    hours = "|".join(name for name, value in _ONES.items() if 1 <= value <= 12)
    pattern = re.compile(rf"\bhalf\s+past\s+({hours})\b", flags=re.IGNORECASE)

    def repl(match: re.Match[str]) -> str:
        hour = _ONES[match.group(1).casefold()]
        return f"{hour}:30"

    return pattern.sub(repl, line)


def _year_phrases(line: str) -> str:
    """Turn ``nineteen seventy`` / ``nineteen seventy two`` into ``1970`` / ``1972``."""
    centuries = "|".join(_YEAR_CENTURY)
    ones = "|".join(name for name, value in _ONES.items() if 1 <= value <= 19)
    tens = "|".join(_TENS)

    three = re.compile(
        rf"\b({centuries})\s+({tens})\s+({ones})\b",
        flags=re.IGNORECASE,
    )

    def three_repl(match: re.Match[str]) -> str:
        tens_val = _TENS[match.group(2).casefold()]
        ones_val = _ONES[match.group(3).casefold()]
        if ones_val >= 10:
            return match.group(0)
        year = _YEAR_CENTURY[match.group(1).casefold()] + tens_val + ones_val
        return str(year)

    line = three.sub(three_repl, line)

    two = re.compile(
        rf"\b({centuries})\s+(({tens})|({ones}))\b",
        flags=re.IGNORECASE,
    )

    def two_repl(match: re.Match[str]) -> str:
        rest = match.group(2).casefold()
        if rest in _SCALES:
            return match.group(0)
        unit = _unit_0_99(rest)
        if unit is None:
            return match.group(0)
        year = _YEAR_CENTURY[match.group(1).casefold()] + unit
        if 1500 <= year <= 1999:
            return str(year)
        return match.group(0)

    line = two.sub(two_repl, line)

    twenty_year = re.compile(
        rf"\btwenty\s+(({tens})|({ones}))\b",
        flags=re.IGNORECASE,
    )

    def twenty_repl(match: re.Match[str]) -> str:
        rest = match.group(1).casefold()
        if rest in _SCALES:
            return match.group(0)
        unit = _unit_0_99(rest)
        if unit is None or unit > 99:
            return match.group(0)
        year = 2000 + unit
        if 2000 <= year <= 2099:
            return str(year)
        return match.group(0)

    return twenty_year.sub(twenty_repl, line)


_MEASURE_UNITS = (
    "foot",
    "feet",
    "ton",
    "tons",
    "pound",
    "pounds",
    "gallon",
    "gallons",
    "barrel",
    "barrels",
    "mile",
    "miles",
    "round",
    "rounds",
    "case",
    "cases",
    "percent",
)


def _measure_phrases(line: str) -> str:
    """Turn ``forty five feet`` / ``eight tons`` into ``45 feet`` / ``8 tons``."""
    small = "|".join(sorted(_SMALL_WORDS, key=len, reverse=True))
    units = "|".join(_MEASURE_UNITS)
    pattern = re.compile(
        rf"\b(({small})(?:[\s-]+({small}))?)\s+({units})\b",
        flags=re.IGNORECASE,
    )

    def repl(match: re.Match[str]) -> str:
        amount = match.group(1).replace("-", " ")
        parts = amount.casefold().split()
        if len(parts) == 2:
            pair = _two_word_unit(parts[0], parts[1])
            value = pair
        else:
            value = _unit_0_99(parts[0]) if parts else None
        if value is None:
            return match.group(0)
        unit = match.group(4)
        return f"{value} {unit}"

    return pattern.sub(repl, line)


def _scaled_quantities(line: str) -> str:
    """Turn ``twenty thousand`` / ``one hundred two thousand`` style counts into digits."""
    tokens = re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)?|\d+|[^\w\s]|\s+", line)
    words_only = [tok for tok in tokens if re.fullmatch(r"[A-Za-z]+(?:-[A-Za-z]+)?", tok)]
    if not words_only:
        return line

    # Walk the original string with a quantity regex instead of a full parser.
    small = "|".join(sorted(_SMALL_WORDS, key=len, reverse=True))
    pattern = re.compile(
        rf"\b(({small})(?:\s+({small}))?(?:\s+hundred)?(?:\s+and)?(?:\s+({small})(?:\s+({small}))?)?\s+(thousand|million))\b",
        flags=re.IGNORECASE,
    )

    def repl(match: re.Match[str]) -> str:
        value = _parse_scaled(match.group(0))
        if value is None or value < 100:
            return match.group(0)
        return _format_int(value)

    line = pattern.sub(repl, line)

    hundred = re.compile(
        rf"\b(({small})(?:\s+({small}))?\s+hundred(?:\s+and)?(?:\s+({small})(?:\s+({small}))?)?)\b",
        flags=re.IGNORECASE,
    )

    def hundred_repl(match: re.Match[str]) -> str:
        parsed = _parse_hundred_phrase(match.group(0))
        if parsed is None or parsed < 100:
            return match.group(0)
        return _format_int(parsed)

    return hundred.sub(hundred_repl, line)


def _consume_0_99(parts: list[str], index: int) -> tuple[int | None, int]:
    """Read one 0–99 value starting at ``index``. Returns (value, next_index)."""
    if index >= len(parts):
        return None, index
    pair = _two_word_unit(parts[index], parts[index + 1]) if index + 1 < len(parts) else None
    if pair is not None:
        return pair, index + 2
    unit = _unit_0_99(parts[index])
    if unit is not None:
        return unit, index + 1
    return None, index


def _parse_hundred_phrase(phrase: str) -> int | None:
    """Parse ``seven hundred`` or ``one hundred two``."""
    parts = [part.casefold() for part in re.findall(r"[A-Za-z]+", phrase)]
    parts = [part for part in parts if part != "and"]
    if "hundred" not in parts:
        return None
    index = 0
    total = 0
    leading, index = _consume_0_99(parts, index)
    if leading is None:
        return None
    if index < len(parts) and parts[index] == "hundred":
        total += leading * 100
        index += 1
    else:
        return None
    if index < len(parts):
        rest, index = _consume_0_99(parts, index)
        if rest is not None:
            total += rest
    return total if index == len(parts) else None


def _parse_scaled(phrase: str) -> int | None:
    """Parse a phrase that ends in thousand or million."""
    parts = [part.casefold() for part in re.findall(r"[A-Za-z]+", phrase)]
    parts = [part for part in parts if part != "and"]
    if not parts or parts[-1] not in {"thousand", "million"}:
        return None
    scale = 1_000 if parts[-1] == "thousand" else 1_000_000
    head = parts[:-1]
    if not head:
        return None
    if "hundred" in head:
        value = _parse_hundred_phrase(" ".join(head))
        if value is None:
            return None
        return value * scale
    unit, index = _consume_0_99(head, 0)
    if unit is None or index != len(head):
        return None
    return unit * scale
