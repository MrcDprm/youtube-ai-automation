"""Language-aware casing: the Turkish dotted and dotless i."""

from __future__ import annotations

import pytest

from utils.text import is_turkic, upper_text


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("iyi", "İYİ"),
        ("ışık", "IŞIK"),
        ("istanbul ışıkları", "İSTANBUL IŞIKLARI"),
        ("çğöşü", "ÇĞÖŞÜ"),
        ("GTA 5'te gizli bir detay", "GTA 5'TE GİZLİ BİR DETAY"),
    ],
)
def test_upper_text_uses_turkish_rules(text: str, expected: str) -> None:
    assert upper_text(text, "tr") == expected


def test_other_languages_keep_default_casing() -> None:
    assert upper_text("this is fine", "en") == "THIS IS FINE"
    assert upper_text("iyi") == "IYI"


@pytest.mark.parametrize("code", ["tr", "TR", "tr-TR", "tr_TR", " az ", "az-Latn-AZ"])
def test_is_turkic_accepts_code_variants(code: str) -> None:
    assert is_turkic(code)


@pytest.mark.parametrize("code", [None, "", "  ", "en", "en-US", "trk", "es"])
def test_is_turkic_rejects_other_codes(code: str | None) -> None:
    assert not is_turkic(code)
