"""Loading, validating and normalizing ``senaryo.json``.

A scenario is hand-authored, so this module treats every failure as a user-facing editing
mistake and reports it precisely: JSON syntax errors carry a line and column, and schema
violations are rendered as a per-field table rather than a pydantic stack trace.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError
from rich.markup import escape
from rich.table import Table
from rich.text import Text

from models.scenario import Scenario
from utils.exceptions import ScenarioValidationError
from utils.logger import (
    get_logger,
    log_blank,
    log_info,
    log_renderable,
    log_success,
    table_box,
)

__all__ = ["ScenarioLoader", "load_scenario"]

logger = get_logger(__name__)

_MAX_ERRORS_SHOWN = 25


class ScenarioLoader:
    """Reads a scenario file and turns it into a validated :class:`~models.scenario.Scenario`."""

    def __init__(self, *, render_errors: bool = True) -> None:
        """Initialise the loader.

        Args:
            render_errors: When true, validation failures are printed as a Rich table before
                the exception is raised. Tests disable this to keep output clean.
        """
        self._render_errors = render_errors

    def load(self, path: Path) -> Scenario:
        """Load and validate a scenario file.

        Args:
            path: Path to the JSON scenario.

        Returns:
            The validated scenario.

        Raises:
            ScenarioValidationError: If the file is missing, is not valid JSON, or violates
                the schema.
        """
        raw = self._read_text(path)
        payload = self._parse_json(raw, path)
        scenario = self._validate(payload, path)
        logger.debug(
            "Loaded scenario %s with %d scene(s)", scenario.project_id, scenario.total_scenes
        )
        return scenario

    # -- Stages -------------------------------------------------------------------------

    @staticmethod
    def _read_text(path: Path) -> str:
        """Read the scenario file as UTF-8.

        Args:
            path: File to read.

        Returns:
            The file contents.

        Raises:
            ScenarioValidationError: If the file is missing or is not valid UTF-8.
        """
        if not path.is_file():
            raise ScenarioValidationError(
                f"Scenario file not found: {path}",
                hint=(
                    "Pass --scenario with a valid path, or copy senaryo.example.json to "
                    "senaryo.json to get started."
                ),
            )
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise ScenarioValidationError(
                f"{path.name} is not valid UTF-8 (byte {exc.start}): {exc.reason}",
                hint="Re-save the file as UTF-8 without a byte-order mark.",
            ) from exc
        except OSError as exc:
            raise ScenarioValidationError(f"Cannot read {path}: {exc}") from exc

    def _parse_json(self, raw: str, path: Path) -> object:
        """Parse JSON, reporting syntax errors with their exact position.

        Args:
            raw: File contents.
            path: Source path, used in the error message.

        Returns:
            The decoded object.

        Raises:
            ScenarioValidationError: If the text is not valid JSON.
        """
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            if self._render_errors:
                self._render_json_error(raw, exc, path)
            raise ScenarioValidationError(
                f"{path.name} is not valid JSON: {exc.msg} at line {exc.lineno}, "
                f"column {exc.colno}",
                hint=(
                    "Common causes: a trailing comma, a missing comma between entries, "
                    "single quotes instead of double quotes, or an unescaped backslash."
                ),
            ) from exc

    def _validate(self, payload: object, path: Path) -> Scenario:
        """Validate the decoded payload against the schema.

        Args:
            payload: Decoded JSON.
            path: Source path, used in the error message.

        Returns:
            The validated scenario.

        Raises:
            ScenarioValidationError: If the payload violates the schema.
        """
        if not isinstance(payload, dict):
            raise ScenarioValidationError(
                f"{path.name} must contain a JSON object at the top level, "
                f"found {type(payload).__name__}.",
                hint="The file should start with '{' and define project_id, video, scenes, etc.",
            )
        try:
            return Scenario.model_validate(payload)
        except ValidationError as exc:
            if self._render_errors:
                self._render_validation_errors(exc, path)
            count = exc.error_count()
            raise ScenarioValidationError(
                f"{path.name} failed schema validation with {count} "
                f"error{'s' if count != 1 else ''}.",
                hint=(
                    "Fix the fields listed above. Unknown fields are rejected on purpose, so a "
                    "'extra_forbidden' error usually means a typo in a key name."
                ),
            ) from exc

    # -- Error rendering ------------------------------------------------------------------

    @staticmethod
    def _render_json_error(raw: str, exc: json.JSONDecodeError, path: Path) -> None:
        """Print the offending JSON line with a caret under the failure position.

        Args:
            raw: The full file contents.
            exc: The decoder error.
            path: Source path, used in the heading.
        """
        lines = raw.splitlines()

        # Built with Text.append rather than a markup string: the echoed source is raw JSON,
        # so it is full of brackets that markup parsing would swallow or choke on.
        report = Text()
        report.append(f"JSON syntax error in {path.name}\n", style="failure")
        report.append(f"  line {exc.lineno}, column {exc.colno}: {exc.msg}\n\n")

        start = max(0, exc.lineno - 3)
        end = min(len(lines), exc.lineno + 2)
        for number in range(start, end):
            marker = ">" if number + 1 == exc.lineno else " "
            report.append(f"  {marker} ")
            report.append(f"{number + 1:>4}", style="muted")
            report.append(f" | {lines[number]}\n")
            if number + 1 == exc.lineno:
                report.append(f"         | {' ' * max(0, exc.colno - 1)}")
                report.append("^\n", style="failure")

        log_blank()
        log_renderable(report)

    @staticmethod
    def _render_validation_errors(exc: ValidationError, path: Path) -> None:
        """Print schema violations as a readable per-field table.

        Args:
            exc: The pydantic validation error.
            path: Source path, used in the table title.
        """
        table = Table(
            title=f"Validation errors in {path.name}",
            title_style="failure",
            header_style="step",
            show_lines=False,
            box=table_box(),
        )
        table.add_column("Field", style="metric", no_wrap=True, overflow="fold")
        table.add_column("Problem", overflow="fold")
        table.add_column("Received", style="muted", overflow="fold", max_width=30)

        errors = exc.errors()
        for error in errors[:_MAX_ERRORS_SHOWN]:
            location = ".".join(str(part) for part in error["loc"]) or "<root>"
            received = error.get("input", "")
            rendered = repr(received)
            if len(rendered) > 120:
                rendered = rendered[:117] + "..."
            # Escape every cell: messages quote regex patterns like ^[a-z0-9-]{3,64}$, and Rich
            # would otherwise consume the bracketed part as a style tag and print it as nothing.
            table.add_row(escape(location), escape(error["msg"]), escape(rendered))

        log_blank()
        log_renderable(table)
        if len(errors) > _MAX_ERRORS_SHOWN:
            log_info(f"... and {len(errors) - _MAX_ERRORS_SHOWN} more")
        log_blank()


def load_scenario(path: Path, *, render_errors: bool = True) -> Scenario:
    """Load and validate a scenario file.

    Args:
        path: Path to the JSON scenario.
        render_errors: Whether to print a Rich error report before raising.

    Returns:
        The validated scenario.

    Raises:
        ScenarioValidationError: If the file cannot be loaded or fails validation.
    """
    return ScenarioLoader(render_errors=render_errors).load(path)


def describe_scenario(scenario: Scenario) -> None:
    """Log a short human summary of a validated scenario.

    Args:
        scenario: The scenario to describe.
    """
    log_success(f"Scenario '{scenario.project_id}' is valid")
    width, height = scenario.video.resolution
    log_info(
        f"{scenario.total_scenes} scene(s), {width}x{height} @ {scenario.video.fps}fps, "
        f"voice {scenario.tts.voice}"
    )
