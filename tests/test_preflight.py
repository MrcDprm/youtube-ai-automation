"""Preflight: the edge-tts version check and the GTA checks behind ``doctor``."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from config.settings import Settings, get_settings
from utils import preflight
from utils.fs import write_json
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
    assert "GTA gameplay" not in names
    assert "GTA topics" not in names


def _gta_settings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, fact: str | None, videos: int
) -> Settings:
    scenarios = tmp_path / "scenarios"
    scenarios.mkdir()
    entry: dict[str, Any] = {"topic": "Fort Zancudo"}
    if fact is not None:
        entry["fact"] = fact
    write_json(scenarios / "topics-gta.json", {"topics": [entry]})
    gameplay = tmp_path / "gameplay"
    gameplay.mkdir()
    for index in range(videos):
        (gameplay / f"ride-{index}.mkv").write_bytes(b"\x00")
    (gameplay / "notes.txt").write_text("not a video", encoding="utf-8")
    monkeypatch.setenv("VIDEO_FORMAT", "gta")
    monkeypatch.setenv("SCENARIOS_DIR", str(scenarios))
    monkeypatch.setenv("GTA_BACKGROUND_DIR", str(gameplay))
    get_settings.cache_clear()
    return get_settings()


def test_doctor_checks_the_gta_list_and_gameplay_instead_of_daily_topics(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = _gta_settings(tmp_path, monkeypatch, fact="Bir bilgi.", videos=2)

    results = {result.name: result for result in preflight.run_all_checks(settings)}

    assert results["GTA topics"].passed
    assert results["GTA topics"].detail == "1 checked facts in topics-gta.json"
    assert results["GTA gameplay"].passed
    assert results["GTA gameplay"].detail.startswith("2 recording(s)")
    assert "Daily topics" not in results


def test_doctor_warns_when_there_is_no_gameplay(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = _gta_settings(tmp_path, monkeypatch, fact="Bir bilgi.", videos=0)

    result = preflight._check_gta_gameplay(settings)

    assert result.status == "WARN"
    assert result.hint is not None
    assert "GTA_BACKGROUND_DIR" in result.hint


def test_doctor_warns_about_a_topic_without_a_fact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = _gta_settings(tmp_path, monkeypatch, fact=None, videos=1)

    result = preflight._check_topics(settings)

    assert result.name == "GTA topics"
    assert result.status == "WARN"
    assert result.detail == "1 of 1 topic(s) have no fact"
