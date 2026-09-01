"""CLI wiring for ``daily --dry-run``: no generation, no render, no state mutation."""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from config.settings import get_settings
from main import app
from utils.fs import write_json

runner = CliRunner()


def test_daily_dry_run_reports_the_next_topic(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Dry run names the topic it would generate and writes nothing to the queue."""
    root = tmp_path / "scenarios"
    root.mkdir()
    write_json(root / "topics.json", {"topics": ["Kahvenin dünyaya yayılışı"]})
    monkeypatch.setenv("SCENARIOS_DIR", str(root))
    get_settings.cache_clear()

    result = runner.invoke(app, ["daily", "--dry-run"])

    assert result.exit_code == 0, result.output
    assert "Kahvenin" in result.output
    assert not list((root / "processing").glob("*.json"))
    assert not list((root / "done").glob("*.json"))


def test_daily_dry_run_prefers_inbox(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A dropped scenario beats the topic list, even in a dry run."""
    root = tmp_path / "scenarios"
    inbox = root / "inbox"
    inbox.mkdir(parents=True)
    (inbox / "hand.json").write_text("{}", encoding="utf-8")
    write_json(root / "topics.json", {"topics": ["Should not be used"]})
    monkeypatch.setenv("SCENARIOS_DIR", str(root))
    get_settings.cache_clear()

    result = runner.invoke(app, ["daily", "--dry-run"])

    assert result.exit_code == 0, result.output
    assert "hand.json" in result.output
    assert (inbox / "hand.json").exists()
