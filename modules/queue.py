"""Daily production queue: topics, inbox/done/failed folders, run-once-per-day state.

This module has no network and no language-model dependency. ``main.py daily`` uses it to
decide *what* to produce; generating the script and rendering the video stay in the composition
root, so a crashed encoder cannot leave the topic list in a half-written state.

Priority, by design:

1. A scenario already sitting in ``inbox/`` always wins. Dropping a JSON file is how a human
   overrides the model for a day.
2. Otherwise the next unused topic in ``topics.json`` is generated.
3. At most one video per calendar day, unless ``--force``. A missed day (the PC was off) is
   recovered by producing *one* video the next time the command runs — never a burst, because
   YouTube's daily quota is about six uploads and quality drops when five scripts are rushed.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Literal

from config.constants import (
    DAILY_LOCK_FILENAME,
    DAILY_LOCK_STALE_SECONDS,
    SCENARIO_QUEUE_SUBDIRECTORIES,
    SCRIPT_DEFAULT_SCENES,
)
from utils.exceptions import ConfigurationError
from utils.fs import ensure_parent, read_json, write_json

__all__ = [
    "DailyAction",
    "DailyLock",
    "ScenarioQueue",
    "SchedulerState",
    "Topic",
    "decide_daily_action",
    "default_scene_count",
    "load_state",
    "load_topics",
    "next_unused_topic",
    "save_state",
]

ActionKind = Literal["skip", "idle", "inbox", "generate"]


@dataclass(frozen=True, slots=True)
class Topic:
    """One video idea from ``topics.json``.

    Attributes:
        topic: The subject, passed to the script generator.
        scenes: Scene count override; ``None`` means use the daily default.
        guidance: Optional extra steering for the model.
        language: Optional narration-language override.
    """

    topic: str
    scenes: int | None = None
    guidance: str | None = None
    language: str | None = None


@dataclass(frozen=True, slots=True)
class DailyAction:
    """What the daily command should do on this invocation.

    Attributes:
        kind: ``skip`` already ran today, ``idle`` nothing left to do, ``inbox`` a dropped
            scenario, ``generate`` the next unused topic.
        reason: Human-readable explanation printed to the console.
        inbox_path: Set when ``kind`` is ``inbox``.
        topic: Set when ``kind`` is ``generate``.
    """

    kind: ActionKind
    reason: str
    inbox_path: Path | None = None
    topic: Topic | None = None


@dataclass
class SchedulerState:
    """Persisted bookkeeping for the daily command.

    Attributes:
        last_success_date: ISO calendar date of the last successful production, or ``None``.
        used_topics: Topics already consumed, in order, matched case-insensitively.
        last_project_id: Project id of the last successful run.
        last_status: ``success`` / ``failed`` / ``skipped`` of the most recent invocation.
        runs: Compact history, newest last, capped so the file cannot grow without bound.
    """

    last_success_date: str | None = None
    used_topics: list[str] = field(default_factory=list)
    last_project_id: str | None = None
    last_status: str | None = None
    runs: list[dict[str, Any]] = field(default_factory=list)

    def already_ran_on(self, today: date) -> bool:
        """Report whether a successful production already happened on ``today``."""
        return self.last_success_date == today.isoformat()

    def mark_used(self, topic: str) -> None:
        """Record a topic as consumed, ignoring duplicates."""
        key = topic.strip().casefold()
        if key and key not in {item.casefold() for item in self.used_topics}:
            self.used_topics.append(topic.strip())

    def record(
        self,
        *,
        status: str,
        today: date,
        project_id: str | None = None,
        topic: str | None = None,
        detail: str | None = None,
    ) -> None:
        """Append a compact history row and update the success date on a clean run.

        Args:
            status: ``success``, ``failed`` or ``skipped``.
            today: The local calendar date of this invocation.
            project_id: Scenario project id, when one was produced.
            topic: Topic string, when one was consumed.
            detail: Optional one-line note.
        """
        self.last_status = status
        if project_id:
            self.last_project_id = project_id
        if status == "success":
            self.last_success_date = today.isoformat()
            if topic:
                self.mark_used(topic)
        self.runs.append(
            {
                "date": today.isoformat(),
                "status": status,
                "project_id": project_id,
                "topic": topic,
                "detail": detail,
            }
        )
        self.runs = self.runs[-50:]


class ScenarioQueue:
    """Four-folder job queue under ``scenarios/``."""

    def __init__(self, root: Path) -> None:
        """Initialise the queue.

        Args:
            root: The ``scenarios/`` directory.
        """
        self.root = root
        self.inbox = root / "inbox"
        self.processing = root / "processing"
        self.done = root / "done"
        self.failed = root / "failed"

    def ensure(self) -> None:
        """Create every queue subdirectory, including the root."""
        for name in SCENARIO_QUEUE_SUBDIRECTORIES:
            (self.root / name).mkdir(parents=True, exist_ok=True)

    def next_inbox(self) -> Path | None:
        """Return the oldest JSON file in the inbox, or ``None`` when it is empty.

        Returns:
            An inbox path, sorted by name so the order is stable across platforms.
        """
        files = sorted(path for path in self.inbox.glob("*.json") if path.is_file())
        return files[0] if files else None

    def claim(self, source: Path) -> Path:
        """Move ``source`` into ``processing/``, avoiding name collisions.

        Args:
            source: A file currently in the inbox, or a freshly generated scenario.

        Returns:
            The path inside ``processing/``.
        """
        self.ensure()
        destination = self._unique(self.processing, source.name)
        source.replace(destination)
        return destination

    def complete(self, processing_path: Path, *, ok: bool) -> Path:
        """Move a processing file into ``done/`` or ``failed/``.

        Args:
            processing_path: The file currently being worked on.
            ok: Whether the pipeline succeeded.

        Returns:
            The final resting path.
        """
        folder = self.done if ok else self.failed
        destination = self._unique(folder, processing_path.name)
        if processing_path.exists():
            processing_path.replace(destination)
        return destination

    @staticmethod
    def _unique(folder: Path, name: str) -> Path:
        """Pick a path in ``folder`` that does not yet exist.

        Args:
            folder: Destination directory.
            name: Preferred filename.

        Returns:
            ``folder / name``, or ``folder / stem-N.suffix`` if that is taken.
        """
        candidate = folder / name
        if not candidate.exists():
            return candidate
        stem, suffix = Path(name).stem, Path(name).suffix
        index = 2
        while True:
            candidate = folder / f"{stem}-{index}{suffix}"
            if not candidate.exists():
                return candidate
            index += 1


class DailyLock:
    """Process-wide exclusive lock so two overlapping daily runs cannot both produce a video.

    Implemented with ``O_CREAT | O_EXCL`` so it works on Windows and POSIX without extra
    packages. A lock older than :data:`DAILY_LOCK_STALE_SECONDS` is treated as a crash leftover
    and stolen.
    """

    def __init__(self, directory: Path) -> None:
        """Initialise the lock.

        Args:
            directory: Directory that will hold the lock file, typically the scheduler cache.
        """
        self.path = directory / DAILY_LOCK_FILENAME
        self._fd: int | None = None

    def __enter__(self) -> DailyLock:
        """Acquire the lock, stealing it if it is stale.

        Returns:
            ``self``.

        Raises:
            ConfigurationError: If another daily run is currently holding the lock.
        """
        ensure_parent(self.path)
        try:
            self._fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
        except FileExistsError:
            age = time.time() - self.path.stat().st_mtime
            if age < DAILY_LOCK_STALE_SECONDS:
                raise ConfigurationError(
                    "A daily run is already in progress.",
                    hint=(
                        f"If you are sure nothing is running, delete {self.path} and retry. "
                        "Overlapping runs are refused so two videos cannot be produced on the "
                        "same day by accident."
                    ),
                ) from None
            self.path.unlink(missing_ok=True)
            self._fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
        os.write(self._fd, str(os.getpid()).encode("ascii"))
        return self

    def __exit__(self, *exc: object) -> None:
        """Release the lock, ignoring a race where another process already stole it."""
        if self._fd is not None:
            os.close(self._fd)
            self._fd = None
        self.path.unlink(missing_ok=True)


def load_topics(path: Path) -> list[Topic]:
    """Load ``topics.json``.

    The file accepts either a top-level array or an object with a ``topics`` array. Each entry
    may be a string or an object with ``topic`` plus optional ``scenes``, ``guidance`` and
    ``language``.

    Args:
        path: Path to ``topics.json``.

    Returns:
        Parsed topics, possibly empty.

    Raises:
        ConfigurationError: If the file is missing, is not JSON, or has the wrong shape.
    """
    if not path.is_file():
        raise ConfigurationError(
            f"Topic list not found: {path}",
            hint="Copy scenarios/topics.example.json to scenarios/topics.json and add subjects.",
        )
    try:
        payload = read_json(path)
    except (OSError, ValueError) as exc:
        raise ConfigurationError(
            f"Could not read {path}: {exc}",
            hint="The file must be UTF-8 JSON.",
        ) from exc

    raw_items: Any
    if isinstance(payload, list):
        raw_items = payload
    elif isinstance(payload, dict):
        raw_items = payload.get("topics", [])
    else:
        raise ConfigurationError(
            f"{path.name} must be a JSON array or an object with a 'topics' array.",
        )

    if not isinstance(raw_items, list):
        raise ConfigurationError(f"{path.name}: 'topics' must be an array.")

    topics: list[Topic] = []
    for index, item in enumerate(raw_items, start=1):
        parsed = _parse_topic(item, index=index, source=path.name)
        if parsed is not None:
            topics.append(parsed)
    return topics


def _parse_topic(item: Any, *, index: int, source: str) -> Topic | None:
    """Parse one topics.json entry, skipping blanks.

    Args:
        item: A string or a mapping.
        index: 1-based position, used in error messages.
        source: Filename for error messages.

    Returns:
        A :class:`Topic`, or ``None`` when the entry is an empty string.

    Raises:
        ConfigurationError: If the entry has the wrong type or a blank ``topic`` key.
    """
    if isinstance(item, str):
        text = item.strip()
        return Topic(topic=text) if text else None
    if not isinstance(item, dict):
        raise ConfigurationError(f"{source}: topic {index} must be a string or an object.")
    raw = item.get("topic")
    if not isinstance(raw, str) or not raw.strip():
        raise ConfigurationError(f"{source}: topic {index} is missing a non-empty 'topic' field.")
    scenes_raw = item.get("scenes")
    scenes = int(scenes_raw) if isinstance(scenes_raw, int) else None
    guidance_raw = item.get("guidance")
    guidance = (
        guidance_raw.strip() if isinstance(guidance_raw, str) and guidance_raw.strip() else None
    )
    language_raw = item.get("language")
    language = (
        language_raw.strip() if isinstance(language_raw, str) and language_raw.strip() else None
    )
    return Topic(topic=raw.strip(), scenes=scenes, guidance=guidance, language=language)


def load_state(path: Path) -> SchedulerState:
    """Load scheduler state, returning empty state when the file does not exist.

    Args:
        path: State file path.

    Returns:
        The decoded state, or a fresh empty one.
    """
    if not path.is_file():
        return SchedulerState()
    try:
        payload = read_json(path)
    except (OSError, ValueError):
        return SchedulerState()
    if not isinstance(payload, dict):
        return SchedulerState()
    used = payload.get("used_topics") or []
    runs = payload.get("runs") or []
    return SchedulerState(
        last_success_date=payload.get("last_success_date")
        if isinstance(payload.get("last_success_date"), str)
        else None,
        used_topics=[str(item) for item in used] if isinstance(used, list) else [],
        last_project_id=payload.get("last_project_id")
        if isinstance(payload.get("last_project_id"), str)
        else None,
        last_status=payload.get("last_status")
        if isinstance(payload.get("last_status"), str)
        else None,
        runs=[item for item in runs if isinstance(item, dict)] if isinstance(runs, list) else [],
    )


def save_state(path: Path, state: SchedulerState) -> Path:
    """Persist scheduler state atomically.

    Args:
        path: Destination file.
        state: Current state.

    Returns:
        The written path.
    """
    return write_json(
        path,
        {
            "last_success_date": state.last_success_date,
            "used_topics": state.used_topics,
            "last_project_id": state.last_project_id,
            "last_status": state.last_status,
            "runs": state.runs,
        },
    )


def next_unused_topic(topics: list[Topic], used: list[str]) -> Topic | None:
    """Return the first topic whose text has not been consumed.

    Matching is case-insensitive so a regenerated wording with different casing cannot sneak
    through as a 'new' topic.

    Args:
        topics: The configured list, in priority order.
        used: Previously consumed topic strings.

    Returns:
        The next topic, or ``None`` when the list is exhausted.
    """
    used_keys = {item.strip().casefold() for item in used}
    for topic in topics:
        if topic.topic.casefold() not in used_keys:
            return topic
    return None


def decide_daily_action(
    *,
    queue: ScenarioQueue,
    topics: list[Topic],
    state: SchedulerState,
    today: date,
    force: bool = False,
) -> DailyAction:
    """Choose the next daily action without performing any I/O beyond listing the inbox.

    Args:
        queue: The scenario folder queue.
        topics: Parsed topic list.
        state: Persisted daily state.
        today: Local calendar date.
        force: Ignore the once-per-day guard.

    Returns:
        The action the caller should take.
    """
    if not force and state.already_ran_on(today):
        return DailyAction(
            kind="skip",
            reason=f"A video was already produced today ({today.isoformat()}).",
        )

    inbox = queue.next_inbox()
    if inbox is not None:
        return DailyAction(
            kind="inbox",
            reason=f"Inbox has {inbox.name}; the topic list is not consulted.",
            inbox_path=inbox,
        )

    topic = next_unused_topic(topics, state.used_topics)
    if topic is None:
        if not topics:
            return DailyAction(
                kind="idle",
                reason="topics.json and the inbox are both empty.",
            )
        return DailyAction(
            kind="idle",
            reason="Every topic in topics.json has already been used.",
        )

    missed = _missed_days(state.last_success_date, today)
    extra = ""
    if missed > 1:
        extra = (
            f" Last success was {missed} day(s) ago; producing one video now "
            "(never a burst — YouTube quota is ~6 uploads/day)."
        )
    return DailyAction(
        kind="generate",
        reason=f"Next topic: {topic.topic}.{extra}",
        topic=topic,
    )


def _missed_days(last_success: str | None, today: date) -> int:
    """Count whole days since the last success, or ``0`` when there has never been one.

    Args:
        last_success: ISO date string, or ``None``.
        today: Local calendar date.

    Returns:
        Non-negative day count.
    """
    if not last_success:
        return 0
    try:
        previous = date.fromisoformat(last_success)
    except ValueError:
        return 0
    return max(0, (today - previous).days)


def default_scene_count(topic: Topic, fallback: int = SCRIPT_DEFAULT_SCENES) -> int:
    """Resolve the scene count for a topic.

    Args:
        topic: The chosen topic.
        fallback: Default when the topic does not override.

    Returns:
        A positive integer.
    """
    return topic.scenes if topic.scenes is not None else fallback


def iso_now() -> str:
    """UTC timestamp used in generated filenames.

    Returns:
        An ``YYYYMMDDTHHMMSS`` stamp.
    """
    return datetime.now().strftime("%Y%m%dT%H%M%S")
