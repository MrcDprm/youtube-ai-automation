"""Caption numeral display: years and large counts become digits."""

from __future__ import annotations

from modules.caption_numbers import display_caption_numbers
from modules.interfaces import SubtitleCue
from modules.subtitle import SrtSubtitleBuilder
from models.scenario import SubtitleSettings


def test_years_become_digits() -> None:
    """Spoken year-words render as four-digit years."""
    assert display_caption_numbers("In November nineteen seventy,") == "In November 1970,"
    assert display_caption_numbers("eighteen fourteen") == "1814"
    assert display_caption_numbers("nineteen seventy two") == "1972"


def test_small_counts_stay_words() -> None:
    """Prose counts stay readable as words."""
    assert display_caption_numbers("three men and two guns") == "three men and two guns"


def test_scaled_and_measures() -> None:
    """Large counts and measurements use digits."""
    assert display_caption_numbers("twenty thousand birds") == "20,000 birds"
    assert display_caption_numbers("forty five feet") == "45 feet"
    assert display_caption_numbers("eight tons") == "8 tons"
    assert display_caption_numbers("the twelfth of November") == "November 12"
    assert display_caption_numbers("half past four") == "4:30"


def test_finish_applies_numerals_without_accent() -> None:
    """Drawn Anyway captions stay one colour and show years as digits."""
    builder = SrtSubtitleBuilder()
    settings = SubtitleSettings.model_validate(
        {
            "enabled": True,
            "burn_in": False,
            "numeral_display": True,
            "accent_color": None,
            "color": "#FFFFFF",
        }
    )
    cues = [
        SubtitleCue(index=1, start=0.0, end=1.0, text="In nineteen seventy,"),
        SubtitleCue(index=2, start=1.0, end=2.0, text="three men waited."),
    ]
    finished = builder.finish(cues, settings)
    assert finished[0].text == "In 1970,"
    assert finished[1].text == "three men waited."
    assert finished[0].color is None
    assert finished[1].color is None
