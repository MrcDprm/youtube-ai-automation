"""Register and remove the OS-level daily trigger for ``python main.py daily``.

Windows is the supported target: the command writes a Task Scheduler XML with
``StartWhenAvailable`` so a missed 09:00 (the PC was asleep) fires as soon as it is back.
POSIX hosts get a crontab line printed rather than installed, because cron dialects vary and
silently installing a job the user cannot find is worse than telling them what to paste.

``schtasks`` is invoked with an argument list, never a shell string.
"""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from config.constants import PROJECT_ROOT, SCHEDULER_EXECUTION_LIMIT, SCHEDULER_TASK_NAME
from utils.exceptions import SchedulerError

__all__ = [
    "SchedulerStatus",
    "build_crontab_line",
    "build_windows_task_xml",
    "is_windows",
    "query_task",
    "register_daily_task",
    "unregister_daily_task",
]


@dataclass(frozen=True, slots=True)
class SchedulerStatus:
    """Whether the daily task is currently registered.

    Attributes:
        registered: True when the OS knows the task name.
        detail: Free-text status from the OS, or an explanation when it is not registered.
        command: The command the task would run.
    """

    registered: bool
    detail: str
    command: str


def is_windows() -> bool:
    """Report whether the current host is Windows.

    Isolated as a function so tests can stub the platform without making ``pathlib.Path``
    try to construct a ``PosixPath`` on Windows.
    """
    return os.name == "nt"


def python_executable() -> Path:
    """Return the interpreter that should run the daily command.

    Prefers the project virtualenv so the scheduled task does not depend on whichever Python
    happens to be first on PATH at 09:00.

    Returns:
        An absolute path to a Python executable.
    """
    if is_windows():
        venv = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
    else:
        venv = PROJECT_ROOT / ".venv" / "bin" / "python"
    if venv.is_file():
        return venv
    return Path(sys.executable).resolve()


def daily_command_args(*, upload: bool) -> list[str]:
    """Build the argument vector for the scheduled ``daily`` invocation.

    Args:
        upload: Whether the scheduled run should enable YouTube upload.

    Returns:
        Arguments following the interpreter, including ``main.py``.
    """
    args = ["main.py", "daily", "--yes"]
    if upload:
        args.append("--upload")
    return args


def build_windows_task_xml(
    *,
    time_of_day: str,
    python_path: Path,
    workdir: Path,
    upload: bool,
    task_name: str = SCHEDULER_TASK_NAME,
) -> str:
    """Render a Task Scheduler 1.2 XML document.

    ``StartWhenAvailable`` is the catch-up switch: if the machine was off at the trigger time,
    Windows runs the task once when it comes back rather than skipping the day.

    Args:
        time_of_day: ``HH:MM`` 24-hour clock.
        python_path: Interpreter to execute.
        workdir: Working directory, which must be the project root so relative paths resolve.
        upload: Forwarded to ``daily --upload``.
        task_name: Windows task name.

    Returns:
        XML text (UTF-8).
    """
    hour, minute = time_of_day.split(":")
    start = (
        datetime.now()
        .replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
        .strftime("%Y-%m-%dT%H:%M:%S")
    )
    arguments = " ".join(_xml_arg(part) for part in daily_command_args(upload=upload))
    return f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>{escape(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))}</Date>
    <Author>youtube-automation</Author>
    <Description>Daily video run. Missed triggers fire when the PC is next on.</Description>
    <URI>\\{escape(task_name)}</URI>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>{escape(start)}</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>{SCHEDULER_EXECUTION_LIMIT}</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{escape(str(python_path))}</Command>
      <Arguments>{escape(arguments)}</Arguments>
      <WorkingDirectory>{escape(str(workdir))}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""


def _xml_arg(value: str) -> str:
    """Quote an argument the way Task Scheduler's command line expects.

    Args:
        value: One argument.

    Returns:
        The argument, quoted if it contains whitespace.
    """
    if any(char.isspace() for char in value):
        return f'"{value}"'
    return value


def build_crontab_line(
    *,
    time_of_day: str,
    python_path: Path,
    workdir: Path,
    upload: bool,
) -> str:
    """Build a crontab line equivalent to the Windows daily task.

    Args:
        time_of_day: ``HH:MM``.
        python_path: Interpreter.
        workdir: Project root.
        upload: Whether to pass ``--upload``.

    Returns:
        A single crontab line, including a ``cd`` so relative paths resolve.
    """
    hour, minute = time_of_day.split(":")
    args = " ".join(daily_command_args(upload=upload))
    root = Path(workdir).as_posix()
    interpreter = Path(python_path).as_posix()
    return (
        f"{int(minute)} {int(hour)} * * * "
        f"cd {root} && {interpreter} {args} "
        f">> {root}/output/logs/daily-cron.log 2>&1"
    )


def register_daily_task(
    *,
    time_of_day: str,
    upload: bool = False,
    task_name: str = SCHEDULER_TASK_NAME,
) -> str:
    """Register (or replace) the daily OS task.

    Args:
        time_of_day: ``HH:MM``.
        upload: Whether scheduled runs should upload.
        task_name: Windows task name.
        runner: Unused; present so tests can monkeypatch :func:`_run`.

    Returns:
        A short confirmation including the trigger time.

    Raises:
        SchedulerError: If ``schtasks`` fails, or the host is not Windows.
    """
    python_path = python_executable()
    workdir = PROJECT_ROOT
    if not is_windows():
        line = build_crontab_line(
            time_of_day=time_of_day, python_path=python_path, workdir=workdir, upload=upload
        )
        raise SchedulerError(
            "Automatic installation is only implemented for Windows Task Scheduler.",
            hint=f"Install this crontab line yourself: {line}",
        )

    xml = build_windows_task_xml(
        time_of_day=time_of_day,
        python_path=python_path,
        workdir=workdir,
        upload=upload,
        task_name=task_name,
    )
    xml_path = workdir / ".cache" / "scheduler" / f"{task_name}.xml"
    xml_path.parent.mkdir(parents=True, exist_ok=True)
    # Task Scheduler 1.2 XML is UTF-16 LE with BOM; schtasks rejects UTF-8.
    xml_path.write_bytes(xml.encode("utf-16"))

    result = _run(["schtasks", "/Create", "/TN", task_name, "/XML", str(xml_path), "/F"])
    if result.returncode != 0:
        stderr = (result.stderr or result.stdout or "").strip()
        raise SchedulerError(
            f"schtasks could not register '{task_name}': {stderr or 'unknown error'}",
            hint="Run the terminal as the same Windows user that will be logged in at 09:00.",
        )
    return f"Registered '{task_name}' daily at {time_of_day} (StartWhenAvailable=true)."


def unregister_daily_task(task_name: str = SCHEDULER_TASK_NAME) -> str:
    """Remove the daily OS task if it exists.

    Args:
        task_name: Windows task name.

    Returns:
        A short confirmation.

    Raises:
        SchedulerError: If the host is not Windows, or deletion fails for a reason other than
            'task not found'.
    """
    if not is_windows():
        raise SchedulerError(
            "Automatic uninstallation is only implemented for Windows Task Scheduler.",
            hint="Remove the crontab line that calls 'python main.py daily'.",
        )
    result = _run(["schtasks", "/Delete", "/TN", task_name, "/F"])
    combined = f"{result.stdout} {result.stderr}".lower()
    if (
        result.returncode != 0
        and "cannot find" not in combined
        and "cannot find the file" not in combined
    ):
        raise SchedulerError(
            f"schtasks could not remove '{task_name}': "
            f"{(result.stderr or result.stdout or '').strip()}",
        )
    return f"Removed scheduled task '{task_name}'."


def query_task(
    *,
    time_of_day: str,
    upload: bool,
    task_name: str = SCHEDULER_TASK_NAME,
) -> SchedulerStatus:
    """Report whether the daily task is registered.

    Args:
        time_of_day: Used only to describe the command the task *would* run.
        upload: Used only to describe the command the task *would* run.
        task_name: Windows task name.

    Returns:
        Registration status. On POSIX this always reports unregistered, with the crontab line
        in ``detail``.
    """
    python_path = python_executable()
    command = f"{python_path} {' '.join(daily_command_args(upload=upload))}"
    if not is_windows():
        line = build_crontab_line(
            time_of_day=time_of_day, python_path=python_path, workdir=PROJECT_ROOT, upload=upload
        )
        return SchedulerStatus(
            registered=False, detail=f"Not Windows. Crontab: {line}", command=command
        )

    result = _run(["schtasks", "/Query", "/TN", task_name, "/FO", "LIST"])
    if result.returncode != 0:
        return SchedulerStatus(
            registered=False,
            detail=f"Task '{task_name}' is not registered.",
            command=command,
        )
    return SchedulerStatus(
        registered=True,
        detail=(result.stdout or "registered").strip(),
        command=command,
    )


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a command without a shell, capturing text output.

    Args:
        args: Argument vector.

    Returns:
        The completed process.
    """
    return subprocess.run(
        args,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
