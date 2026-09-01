"""Preflight checks backing the ``doctor`` command.

Every check is independent and returns a result rather than raising, so a single run reports
all problems at once instead of stopping at the first. Only the caller decides whether the
collected results are fatal.

The :class:`~config.settings.Settings` type is imported lazily under ``TYPE_CHECKING``:
``config.settings`` imports ``utils.exceptions``, so a runtime import here would close an
import cycle.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import requests

from config.constants import (
    MIN_FREE_DISK_BYTES,
    MIN_PYTHON_VERSION,
    OLLAMA_TAGS_PATH,
    OUTPUT_SUBDIRECTORIES,
    PROJECT_ROOT,
)
from utils.exceptions import FontNotFoundError, PreflightError, RenderError
from utils.fs import available_fonts, format_bytes, free_disk_bytes, resolve_font
from utils.media import ffmpeg_executable

if TYPE_CHECKING:
    from config.settings import Settings

__all__ = ["CheckResult", "raise_if_failed", "run_all_checks"]


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Outcome of a single preflight check.

    Attributes:
        name: Short label shown in the doctor table.
        passed: Whether the check succeeded.
        detail: What was found, shown whether or not the check passed.
        hint: Actionable next step, shown only on failure.
        fatal: When false, a failure is reported as a warning and does not block the run.
    """

    name: str
    passed: bool
    detail: str
    hint: str | None = None
    fatal: bool = True

    @property
    def status(self) -> str:
        """Render the outcome as ``OK``, ``WARN`` or ``FAIL``."""
        if self.passed:
            return "OK"
        return "FAIL" if self.fatal else "WARN"


def _check_python_version() -> CheckResult:
    """Verify the interpreter is new enough for the syntax this project uses."""
    current = sys.version_info[:2]
    required = MIN_PYTHON_VERSION
    ok = current >= required
    return CheckResult(
        name="Python version",
        passed=ok,
        detail=f"{sys.version.split()[0]} at {sys.executable}",
        hint=(
            None
            if ok
            else f"Python {required[0]}.{required[1]}+ is required; upgrade your interpreter."
        ),
    )


def _check_ffmpeg() -> CheckResult:
    """Verify an ffmpeg binary can be resolved and is executable."""
    try:
        binary = ffmpeg_executable()
    except RenderError as exc:
        return CheckResult(
            name="ffmpeg binary",
            passed=False,
            detail="not found",
            hint=exc.hint or "Install imageio-ffmpeg.",
        )
    exists = binary.is_file()
    return CheckResult(
        name="ffmpeg binary",
        passed=exists,
        detail=str(binary) if exists else f"{binary} (missing)",
        hint=(
            None
            if exists
            else "Reinstall imageio-ffmpeg: pip install --force-reinstall imageio-ffmpeg"
        ),
    )


def _check_env_file() -> CheckResult:
    """Verify a ``.env`` file exists, without reading its contents."""
    env_path = PROJECT_ROOT / ".env"
    exists = env_path.is_file()
    return CheckResult(
        name=".env file",
        passed=exists,
        detail=str(env_path) if exists else "not created yet",
        hint=None if exists else "Copy .env.example to .env and fill in your keys.",
        fatal=False,
    )


def _check_pexels_key(settings: Settings) -> CheckResult:
    """Verify a stock footage API key is present, without ever printing it."""
    has_pexels = bool(settings.PEXELS_API_KEY.strip())
    has_pixabay = bool(settings.PIXABAY_API_KEY.strip())
    if has_pexels:
        detail = "PEXELS_API_KEY set" + (" (PIXABAY_API_KEY also set)" if has_pixabay else "")
    elif has_pixabay:
        detail = "PEXELS_API_KEY missing, PIXABAY_API_KEY set"
    else:
        detail = "no stock provider key set"
    return CheckResult(
        name="Stock footage key",
        passed=has_pexels or has_pixabay,
        detail=detail,
        hint=(
            None
            if (has_pexels or has_pixabay)
            else (
                "Get a free key at https://www.pexels.com/api/ and set PEXELS_API_KEY in .env. "
                "Scenes using local_media do not need one."
            )
        ),
    )


def _check_font(settings: Settings) -> CheckResult:
    """Verify some usable font exists for burned-in text."""
    bundled = available_fonts(settings.fonts_dir)
    try:
        resolved, warning = resolve_font(settings.font_path, fonts_dir=settings.fonts_dir)
    except FontNotFoundError as exc:
        return CheckResult(
            name="Font file",
            passed=False,
            detail=f"none found (assets/fonts holds {len(bundled)} files)",
            hint=exc.hint,
        )
    exact = warning is None
    return CheckResult(
        name="Font file",
        passed=True,
        detail=str(resolved) if exact else f"{resolved} (substituted)",
        hint=None if exact else warning,
        fatal=False,
    )


def _check_output_dirs(settings: Settings) -> CheckResult:
    """Verify every output subdirectory can be created and written to."""
    problems: list[str] = []
    for name in OUTPUT_SUBDIRECTORIES:
        target = settings.output_dir / name
        try:
            target.mkdir(parents=True, exist_ok=True)
            probe = target / ".write_test"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
        except OSError as exc:
            problems.append(f"{name}: {exc.strerror or exc}")
    ok = not problems
    return CheckResult(
        name="Output directories",
        passed=ok,
        detail=(
            f"{len(OUTPUT_SUBDIRECTORIES)} writable under {settings.output_dir}"
            if ok
            else "; ".join(problems)
        ),
        hint=None if ok else "Check permissions, or point OUTPUT_DIR at a writable location.",
    )


def _check_cache_dir(settings: Settings) -> CheckResult:
    """Verify the cache directory is usable, since it is what makes runs resumable."""
    try:
        settings.cache_dir.mkdir(parents=True, exist_ok=True)
        probe = settings.cache_dir / ".write_test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        return CheckResult(
            name="Cache directory",
            passed=False,
            detail=f"{settings.cache_dir}: {exc.strerror or exc}",
            hint="Set CACHE_DIR in .env to a writable path.",
        )
    return CheckResult(
        name="Cache directory",
        passed=True,
        detail=str(settings.cache_dir),
    )


def _check_disk_space(settings: Settings) -> CheckResult:
    """Verify there is room to render without running the volume dry."""
    free = free_disk_bytes(settings.output_dir)
    ok = free >= MIN_FREE_DISK_BYTES
    return CheckResult(
        name="Free disk space",
        passed=ok,
        detail=f"{format_bytes(free)} available, {format_bytes(MIN_FREE_DISK_BYTES)} required",
        hint=None if ok else "Free up space or point OUTPUT_DIR at a larger volume.",
    )


def _check_youtube_credentials(settings: Settings) -> CheckResult:
    """Report OAuth readiness. Never fatal, because uploading is opt-in."""
    secrets_path = settings.client_secrets_path
    token_path = settings.token_path
    if not secrets_path.is_file():
        return CheckResult(
            name="YouTube OAuth",
            passed=False,
            detail=f"{secrets_path} not found",
            hint=(
                "Only needed for uploads. See the README's YouTube setup walkthrough, then "
                "run 'python main.py auth'."
            ),
            fatal=False,
        )
    if not token_path.is_file():
        return CheckResult(
            name="YouTube OAuth",
            passed=False,
            detail="client secrets present, not yet authorized",
            hint="Run 'python main.py auth' to complete the one-time consent flow.",
            fatal=False,
        )
    return CheckResult(
        name="YouTube OAuth",
        passed=True,
        detail="client secrets and token present",
        fatal=False,
    )


def _check_writable_project_root() -> CheckResult:
    """Verify the project directory itself is writable, for scenario and log files."""
    try:
        probe = PROJECT_ROOT / ".write_test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        return CheckResult(
            name="Project directory",
            passed=False,
            detail=f"{PROJECT_ROOT} is not writable: {exc.strerror or exc}",
            hint="Move the project somewhere your user account can write to.",
        )
    return CheckResult(name="Project directory", passed=True, detail=str(PROJECT_ROOT))


def _check_ffmpeg_threads(settings: Settings) -> CheckResult:
    """Report the encoder thread count against the machine's CPU count."""
    cpu_count = os.cpu_count() or 1
    configured = settings.FFMPEG_THREADS
    sensible = configured <= max(1, cpu_count * 2)
    return CheckResult(
        name="Encoder threads",
        passed=sensible,
        detail=f"FFMPEG_THREADS={configured}, {cpu_count} logical CPUs detected",
        hint=(
            None
            if sensible
            else f"FFMPEG_THREADS is far above the CPU count; {cpu_count} is a good value."
        ),
        fatal=False,
    )


def _check_ollama(settings: Settings) -> CheckResult:
    """Report whether the local model server is reachable and has the configured model.

    Never fatal: script generation is optional, and a hand-written scenario needs no model.
    The timeout is deliberately short because this only ever contacts localhost.
    """
    name = "Script model (Ollama)"
    url = settings.ollama_url(OLLAMA_TAGS_PATH)
    try:
        response = requests.get(url, timeout=3.0)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        return CheckResult(
            name=name,
            passed=False,
            detail=f"not reachable at {settings.OLLAMA_HOST}",
            hint=(
                "Only needed for 'generate'. Install from https://ollama.com, then run "
                f"'ollama pull {settings.OLLAMA_MODEL}'."
            ),
            fatal=False,
        )
    except ValueError:
        return CheckResult(
            name=name,
            passed=False,
            detail=f"{settings.OLLAMA_HOST} replied with malformed JSON",
            hint="Confirm OLLAMA_HOST points at an Ollama server and not another service.",
            fatal=False,
        )

    installed: list[str] = []
    if isinstance(payload, dict) and isinstance(payload.get("models"), list):
        installed = [
            str(entry["name"])
            for entry in payload["models"]
            if isinstance(entry, dict) and entry.get("name")
        ]

    wanted = settings.OLLAMA_MODEL
    # Ollama reports tags as "name:tag", so a bare model name should still count as present.
    if any(tag == wanted or tag.split(":")[0] == wanted.split(":")[0] for tag in installed):
        return CheckResult(name=name, passed=True, detail=f"{wanted} available")

    return CheckResult(
        name=name,
        passed=False,
        detail=f"server up, but '{wanted}' is not installed",
        hint=f"Pull it with: ollama pull {wanted}",
        fatal=False,
    )


def _check_topics(settings: Settings) -> CheckResult:
    """Report whether a daily topic list exists. Never fatal: daily is optional."""
    path = settings.topics_path()
    if path.is_file():
        return CheckResult(name="Daily topics", passed=True, detail=str(path))
    return CheckResult(
        name="Daily topics",
        passed=False,
        detail=f"{path} not found",
        hint="Copy scenarios/topics.example.json to scenarios/topics.json.",
        fatal=False,
    )


def run_all_checks(settings: Settings) -> list[CheckResult]:
    """Run every preflight check.

    Args:
        settings: Loaded runtime settings.

    Returns:
        One :class:`CheckResult` per check, in display order.
    """
    return [
        _check_python_version(),
        _check_ffmpeg(),
        _check_writable_project_root(),
        _check_env_file(),
        _check_pexels_key(settings),
        _check_font(settings),
        _check_output_dirs(settings),
        _check_cache_dir(settings),
        _check_disk_space(settings),
        _check_ffmpeg_threads(settings),
        _check_ollama(settings),
        _check_topics(settings),
        _check_youtube_credentials(settings),
    ]


def raise_if_failed(results: list[CheckResult]) -> None:
    """Raise when any fatal check failed.

    Args:
        results: Results from :func:`run_all_checks`.

    Raises:
        PreflightError: Naming every fatal failure.
    """
    fatal = [result for result in results if not result.passed and result.fatal]
    if not fatal:
        return
    summary = "; ".join(f"{result.name} ({result.detail})" for result in fatal)
    hints = [result.hint for result in fatal if result.hint]
    raise PreflightError(
        f"{len(fatal)} preflight check(s) failed: {summary}",
        hint=" | ".join(hints) if hints else None,
    )


def font_directory_is_empty(fonts_dir: Path) -> bool:
    """Report whether the project font directory has no font files.

    Args:
        fonts_dir: Directory to inspect.

    Returns:
        ``True`` when no font files are present.
    """
    return not available_fonts(fonts_dir)
