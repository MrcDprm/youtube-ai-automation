"""Colored console logging, a plain-text per-run log file, and secret redaction.

Every module in this project logs through :func:`get_logger` or the ``log_*`` helpers. Those
helpers are the only sanctioned way for library code to write to the terminal, which keeps
``print`` confined to ``main.py`` and to this module's console object.
"""

from __future__ import annotations

import contextlib
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from rich import box
from rich.console import Console, RenderableType
from rich.logging import RichHandler
from rich.markup import escape
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.table import Table
from rich.theme import Theme

from config.constants import (
    MIN_REDACTABLE_SECRET_LENGTH,
    REDACTION_PLACEHOLDER,
    SECRET_ENV_VARS,
)

__all__ = [
    "SecretRedactingFilter",
    "console",
    "get_logger",
    "known_secret_env_vars",
    "log_blank",
    "log_error",
    "log_info",
    "log_metric",
    "log_renderable",
    "log_step",
    "log_success",
    "log_warn",
    "make_download_progress",
    "make_step_progress",
    "redact",
    "register_secret",
    "setup_logging",
    "summary_table",
    "table_box",
]


def _stream_supports(sample: str) -> bool:
    """Report whether the console's encoding can represent a string.

    Windows consoles commonly run a legacy code page such as cp1254, which encodes Turkish
    letters but not box-drawing or dingbat characters. Writing one raises ``UnicodeEncodeError``
    and would crash the run over a status glyph.

    Args:
        sample: Characters to test.

    Returns:
        ``True`` when the characters can be encoded for the console.
    """
    encoding = getattr(sys.stdout, "encoding", None) or "ascii"
    try:
        sample.encode(encoding)
    except (UnicodeEncodeError, LookupError):
        return False
    return True


def _harden_streams() -> None:
    """Make stdout and stderr replace unencodable characters instead of raising.

    A belt-and-braces guard: even with ASCII-safe glyphs selected, scenario text or a provider
    error message could contain a character the console cannot render.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            with contextlib.suppress(Exception):
                reconfigure(errors="replace")


_harden_streams()

UNICODE_SAFE: bool = _stream_supports("\u2714\u25b2\u2716\u00b7\u2500")
"""Whether the console can render the preferred Unicode glyphs and box drawing."""

SYMBOL_SUCCESS = "\u2714" if UNICODE_SAFE else "+"
SYMBOL_WARN = "\u25b2" if UNICODE_SAFE else "!"
SYMBOL_ERROR = "\u2716" if UNICODE_SAFE else "x"
SYMBOL_INFO = "\u00b7" if UNICODE_SAFE else "-"
RULE_CHARACTER = "\u2500" if UNICODE_SAFE else "-"


def table_box() -> box.Box:
    """Return a table border style the console can actually render.

    Returns:
        Rounded Unicode borders where supported, plain ASCII otherwise.
    """
    return box.ROUNDED if UNICODE_SAFE else box.ASCII


PIPELINE_THEME = Theme(
    {
        "logging.level.debug": "dim cyan",
        "logging.level.info": "white",
        "logging.level.warning": "yellow",
        "logging.level.error": "bold red",
        "logging.level.critical": "bold white on red",
        "step": "bold cyan",
        "success": "bold green",
        "warn": "yellow",
        "failure": "bold red",
        "metric": "magenta",
        "muted": "dim",
    }
)

console: Console = Console(theme=PIPELINE_THEME, highlight=False, soft_wrap=False)
"""The single shared Rich console. Library modules use the ``log_*`` helpers instead."""

_LOGGER_NAMESPACE = "pipeline"
_configured = False

_GENERIC_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    # Google OAuth client ids and secrets.
    re.compile(r"\b\d{10,}-[a-z0-9]{20,}\.apps\.googleusercontent\.com\b"),
    re.compile(r"\bGOCSPX-[A-Za-z0-9_-]{20,}\b"),
    # Google API keys.
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    # OAuth bearer and refresh tokens.
    re.compile(r"\b1//[0-9A-Za-z_-]{20,}\b"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/-]{20,}=*"),
    # Generic "key=value" shapes in URLs and query strings.
    re.compile(r"(?i)(?<=[?&])(api[_-]?key|key|token|secret|password)=[^&\s]{8,}"),
    # Long opaque tokens that look like Pexels or Pixabay keys.
    re.compile(r"\b[0-9a-zA-Z]{40,}\b"),
)


class SecretRedactingFilter(logging.Filter):
    """Replace secret values with a placeholder before a record reaches any handler.

    Two mechanisms run in sequence. Literal values registered via :meth:`add_secret` are
    replaced exactly, and a set of generic patterns catches API-key-shaped strings that were
    never registered, such as a key echoed back inside an HTTP error body.
    """

    def __init__(self, secrets: list[str] | None = None) -> None:
        """Initialise the filter.

        Args:
            secrets: Literal secret values to redact.
        """
        super().__init__()
        self._secrets: set[str] = set()
        for secret in secrets or []:
            self.add_secret(secret)

    def add_secret(self, secret: str | None) -> None:
        """Register a literal secret value.

        Values shorter than :data:`config.constants.MIN_REDACTABLE_SECRET_LENGTH` are ignored,
        since blanket-replacing a short string would mangle ordinary log text.

        Args:
            secret: The value to redact, or ``None``.
        """
        if secret and len(secret.strip()) >= MIN_REDACTABLE_SECRET_LENGTH:
            self._secrets.add(secret.strip())

    def redact(self, text: str) -> str:
        """Return ``text`` with every known and pattern-matched secret removed.

        Args:
            text: Arbitrary text, typically a formatted log message.

        Returns:
            The redacted text.
        """
        for secret in self._secrets:
            if secret in text:
                text = text.replace(secret, REDACTION_PLACEHOLDER)
        for pattern in _GENERIC_SECRET_PATTERNS:
            text = pattern.sub(REDACTION_PLACEHOLDER, text)
        return text

    def filter(self, record: logging.LogRecord) -> bool:
        """Redact the record in place.

        Args:
            record: The log record about to be emitted.

        Returns:
            Always ``True``; this filter censors rather than drops.
        """
        if isinstance(record.msg, str):
            record.msg = self.redact(record.msg)
        if record.args:
            if isinstance(record.args, dict):
                record.args = {
                    key: self.redact(value) if isinstance(value, str) else value
                    for key, value in record.args.items()
                }
            elif isinstance(record.args, tuple):
                record.args = tuple(
                    self.redact(value) if isinstance(value, str) else value for value in record.args
                )
        return True


_redaction_filter = SecretRedactingFilter()


def register_secret(value: str | None) -> None:
    """Register a secret with the shared redaction filter.

    Call this as soon as a secret is loaded, before anything can log it.

    Args:
        value: The secret to redact from all future log output.
    """
    _redaction_filter.add_secret(value)


def setup_logging(
    *,
    level: str = "INFO",
    log_dir: Path | None = None,
    project_id: str | None = None,
    secrets: list[str] | None = None,
    verbose: bool = False,
) -> Path | None:
    """Configure console and file logging for the process.

    Console output is colored and honours ``level``. The file handler, when a directory is
    given, always records at ``DEBUG`` so a failed run leaves a complete trace behind even if
    the console was quiet.

    Args:
        level: Console log level name, for example ``"INFO"``.
        log_dir: Directory for the per-run log file. No file is written when ``None``.
        project_id: Used in the log file name. Defaults to ``"run"``.
        secrets: Literal secret values to redact from every handler.
        verbose: Force the console to ``DEBUG`` regardless of ``level``.

    Returns:
        The path to the log file, or ``None`` when file logging was not requested.
    """
    global _configured

    for secret in secrets or []:
        _redaction_filter.add_secret(secret)

    console_level = logging.DEBUG if verbose else getattr(logging, level.upper(), logging.INFO)

    root = logging.getLogger(_LOGGER_NAMESPACE)
    root.setLevel(logging.DEBUG)
    root.propagate = False
    for handler in list(root.handlers):
        root.removeHandler(handler)
        handler.close()

    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=False,
        omit_repeated_times=False,
        rich_tracebacks=True,
        markup=False,
        log_time_format="[%H:%M:%S]",
    )
    rich_handler.setLevel(console_level)
    rich_handler.addFilter(_redaction_filter)
    root.addHandler(rich_handler)

    log_path: Path | None = None
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = log_dir / f"{project_id or 'run'}_{stamp}.log"
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s %(levelname)-8s %(name)-28s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        file_handler.addFilter(_redaction_filter)
        root.addHandler(file_handler)

    # Third-party libraries are noisy at DEBUG and can echo credentials in request URLs.
    for noisy in ("urllib3", "googleapiclient", "google_auth_httplib2", "asyncio", "PIL"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    _configured = True
    return log_path


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger.

    Args:
        name: Usually ``__name__``. The ``pipeline.`` prefix is added automatically.

    Returns:
        A logger whose records flow through the configured handlers and redaction filter.
    """
    short = name.rsplit(".", 1)[-1] if name.startswith(_LOGGER_NAMESPACE) else name
    logger = logging.getLogger(f"{_LOGGER_NAMESPACE}.{short}")
    if not _configured:
        # Keep library imports usable before setup_logging runs, without duplicating output.
        logger.addHandler(logging.NullHandler())
    return logger


# --------------------------------------------------------------------------------------
# Console helpers used by every module
# --------------------------------------------------------------------------------------


def _body(message: str) -> str:
    """Redact secrets from a message and neutralise any Rich markup inside it.

    Messages carry filenames, scenario titles and regex patterns, all of which can contain
    square brackets. Without escaping, Rich would read ``[2026]`` as a style tag and drop it,
    or raise ``MarkupError`` on something like ``[unclosed``.

    Args:
        message: Caller-supplied text.

    Returns:
        Text that is safe to interpolate into a markup string.
    """
    return escape(_redaction_filter.redact(message))


def log_step(number: int, total: int, title: str) -> None:
    """Print a bold cyan rule announcing a pipeline stage.

    Args:
        number: 1-based stage index.
        total: Total number of stages.
        title: Stage description.
    """
    console.rule(
        f"[step]STEP {number}/{total} {SYMBOL_INFO} {_body(title)}[/step]",
        style="step",
        characters=RULE_CHARACTER,
    )


def log_success(message: str) -> None:
    """Print a green success line.

    Args:
        message: Text to display.
    """
    console.print(f"[success]{SYMBOL_SUCCESS}[/success] {_body(message)}")


def log_warn(message: str) -> None:
    """Print a yellow warning line.

    Args:
        message: Text to display.
    """
    console.print(f"[warn]{SYMBOL_WARN}[/warn] {_body(message)}")


def log_error(message: str) -> None:
    """Print a red error line.

    Args:
        message: Text to display.
    """
    console.print(f"[failure]{SYMBOL_ERROR}[/failure] {_body(message)}")


def log_info(message: str) -> None:
    """Print a dimmed informational line.

    Args:
        message: Text to display.
    """
    console.print(f"[muted]{SYMBOL_INFO} {_body(message)}[/muted]")


def log_metric(label: str, value: Any) -> None:
    """Print a magenta key/value metric line.

    Args:
        label: Metric name.
        value: Metric value; converted with ``str``.
    """
    console.print(f"  [metric]{escape(label)}:[/metric] {_body(str(value))}")


def log_renderable(renderable: RenderableType) -> None:
    """Print an already-prepared Rich renderable such as a table or styled text block.

    Library modules route console output through this module rather than importing the console
    directly, which keeps every write in one place.

    Args:
        renderable: Any Rich renderable.
    """
    console.print(renderable)


def log_blank(count: int = 1) -> None:
    """Print blank lines to separate console sections.

    Args:
        count: How many blank lines to emit.
    """
    for _ in range(count):
        console.print()


# --------------------------------------------------------------------------------------
# Progress bars
# --------------------------------------------------------------------------------------


def make_download_progress() -> Progress:
    """Build a progress bar suited to byte-oriented transfers.

    Returns:
        An unstarted :class:`rich.progress.Progress` showing size, speed and ETA.
    """
    return Progress(
        SpinnerColumn(style="step"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
    )


def make_step_progress() -> Progress:
    """Build a progress bar suited to counted work such as per-scene rendering.

    Returns:
        An unstarted :class:`rich.progress.Progress` showing percentage and elapsed time.
    """
    return Progress(
        SpinnerColumn(style="step"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    )


def summary_table(title: str, rows: list[tuple[str, str]]) -> Table:
    """Build a two-column key/value summary table.

    Args:
        title: Table caption.
        rows: ``(label, value)`` pairs, already formatted.

    Returns:
        A Rich table ready to pass to ``console.print``.
    """
    table = Table(
        title=escape(title), title_style="step", show_header=False, box=table_box(), pad_edge=False
    )
    table.add_column("Field", style="metric", no_wrap=True)
    table.add_column("Value", overflow="fold")
    for label, value in rows:
        table.add_row(escape(label), _body(value))
    return table


def redact(text: str) -> str:
    """Redact secrets from arbitrary text.

    Exposed so non-logging surfaces, such as the run manifest, can reuse the same rules.

    Args:
        text: Text that may contain secrets.

    Returns:
        The redacted text.
    """
    return _redaction_filter.redact(text)


def known_secret_env_vars() -> tuple[str, ...]:
    """Return the environment variable names treated as secrets.

    Returns:
        The configured secret variable names.
    """
    return SECRET_ENV_VARS
