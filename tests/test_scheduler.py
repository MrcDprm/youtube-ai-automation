"""Windows Task Scheduler XML and crontab line — no real schtasks calls."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from modules.scheduler import (
    build_crontab_line,
    build_windows_task_xml,
    daily_command_args,
    query_task,
    register_daily_task,
    unregister_daily_task,
)
from utils.exceptions import SchedulerError


def test_daily_command_includes_yes_so_public_uploads_cannot_block() -> None:
    """A scheduled run has nobody to answer a confirmation prompt."""
    assert daily_command_args(upload=False) == ["main.py", "daily", "--yes"]
    assert "--upload" in daily_command_args(upload=True)


def test_windows_xml_enables_missed_trigger_catch_up() -> None:
    """StartWhenAvailable is the whole point of writing XML instead of a one-liner."""
    python_path = Path("C:/proj/.venv/Scripts/python.exe")
    workdir = Path("C:/proj")
    xml = build_windows_task_xml(
        time_of_day="09:00",
        python_path=python_path,
        workdir=workdir,
        upload=False,
    )

    assert "<StartWhenAvailable>true</StartWhenAvailable>" in xml
    assert "<DaysInterval>1</DaysInterval>" in xml
    assert "main.py daily --yes" in xml
    assert str(python_path) in xml
    assert str(workdir) in xml
    assert "<RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>" in xml


def test_windows_xml_escapes_paths_with_ampersands() -> None:
    """A project folder named 'A & B' must not produce malformed XML."""
    xml = build_windows_task_xml(
        time_of_day="21:30",
        python_path=Path("C:/A & B/python.exe"),
        workdir=Path("C:/A & B"),
        upload=True,
    )

    assert "A &amp; B" in xml
    assert "--upload" in xml
    assert "T21:30:00" in xml


def test_crontab_line_changes_into_the_project_directory() -> None:
    """Relative scenario paths only resolve if cron starts in the repo."""
    workdir = Path("/opt/youtube-automation")
    python_path = Path("/opt/venv/bin/python")
    line = build_crontab_line(
        time_of_day="09:15",
        python_path=python_path,
        workdir=workdir,
        upload=False,
    )

    assert line.startswith("15 9 * * * ")
    assert "cd /opt/youtube-automation" in line
    assert "/opt/venv/bin/python main.py daily --yes" in line


def test_register_on_posix_prints_the_crontab_instead(monkeypatch: pytest.MonkeyPatch) -> None:
    """Installing a cron job silently would hide it from the user."""
    monkeypatch.setattr("modules.scheduler.is_windows", lambda: False)

    with pytest.raises(SchedulerError, match="crontab line"):
        register_daily_task(time_of_day="09:00")


def test_register_invokes_schtasks_with_an_argument_vector(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """schtasks is called without a shell, so paths with spaces stay intact."""
    calls: list[list[str]] = []

    def fake_run(args: list[str]) -> subprocess.CompletedProcess[str]:
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, "SUCCESS", "")

    monkeypatch.setattr("modules.scheduler.is_windows", lambda: True)
    monkeypatch.setattr("modules.scheduler._run", fake_run)
    monkeypatch.setattr("modules.scheduler.python_executable", lambda: tmp_path / "python.exe")

    message = register_daily_task(time_of_day="09:00", upload=True)

    assert calls
    assert calls[0][:3] == ["schtasks", "/Create", "/TN"]
    assert "/XML" in calls[0]
    assert "09:00" in message
    assert "StartWhenAvailable" in message


def test_register_surfaces_schtasks_stderr(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Access-denied from Task Scheduler must not become a generic crash."""
    monkeypatch.setattr("modules.scheduler.is_windows", lambda: True)
    monkeypatch.setattr("modules.scheduler.python_executable", lambda: tmp_path / "python.exe")
    monkeypatch.setattr(
        "modules.scheduler._run",
        lambda args: subprocess.CompletedProcess(args, 1, "", "Access is denied."),
    )

    with pytest.raises(SchedulerError, match="Access is denied"):
        register_daily_task(time_of_day="09:00")


def test_unregister_treats_missing_task_as_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Removing a task that was never registered is not an error."""
    monkeypatch.setattr("modules.scheduler.is_windows", lambda: True)
    monkeypatch.setattr(
        "modules.scheduler._run",
        lambda args: subprocess.CompletedProcess(
            args, 1, "", "ERROR: The system cannot find the file specified."
        ),
    )

    assert "Removed" in unregister_daily_task()


def test_query_unregistered_task(monkeypatch: pytest.MonkeyPatch) -> None:
    """status should say the task is absent rather than raising."""
    monkeypatch.setattr("modules.scheduler.is_windows", lambda: True)
    monkeypatch.setattr(
        "modules.scheduler._run",
        lambda args: subprocess.CompletedProcess(args, 1, "", "cannot find"),
    )

    info = query_task(time_of_day="09:00", upload=False)

    assert info.registered is False
    assert "not registered" in info.detail
