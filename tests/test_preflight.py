"""Preflight: the edge-tts version check behind ``doctor``."""

from __future__ import annotations

import pytest

from config.settings import Settings
from utils import preflight
from utils.preflight import CheckResult


@pytest.mark.parametrize(
    ("installed", "passed"),
    [
        ("7.3.1", True),
        ("7.3.2", True),
        ("7.10.0", True),
        ("8.0", True),
        ("7.2.8", False),
        ("7.3", False),
        ("7.3.0rc1", False),
    ],
)
def test_edge_tts_check_compares_versions_numerically(
    monkeypatch: pytest.MonkeyPatch, installed: str, passed: bool
) -> None:
    """7.10 is newer than 7.3, which a plain string comparison would get wrong."""
    monkeypatch.setattr(preflight, "_installed_edge_tts", lambda: installed)

    result = preflight._check_edge_tts()

    assert result.passed is passed
    assert result.fatal
    if not passed:
        assert result.hint is not None
        assert "pip install -U edge-tts" in result.hint


def test_edge_tts_check_reports_a_missing_package(monkeypatch: pytest.MonkeyPatch) -> None:
    """A missing package is a failure with an install hint, not a crash."""
    monkeypatch.setattr(preflight, "_installed_edge_tts", lambda: None)

    result = preflight._check_edge_tts()

    assert not result.passed
    assert result.detail == "not installed"


def test_doctor_runs_the_edge_tts_check(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The check is part of the doctor table. Ollama is stubbed so no socket is opened."""
    monkeypatch.setattr(
        preflight,
        "_check_ollama",
        lambda _settings: CheckResult(name="Script model (Ollama)", passed=True, detail="stub"),
    )

    names = [result.name for result in preflight.run_all_checks(settings)]

    assert "edge-tts" in names
