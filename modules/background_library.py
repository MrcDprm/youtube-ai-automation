"""Continuous background footage cut from a folder of long videos.

Gameplay channels lay narration over footage that never cuts: one long take of driving or
running that keeps the eye busy. This module reserves an unused stretch of such a video for
each project, records it in a ledger so no two videos share footage, and cuts the stretch into
one clip per scene so the scenes play back to back as a single take.
"""

from __future__ import annotations

import math
import random
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config.constants import (
    BACKGROUND_CLIP_MARGIN_SECONDS,
    BACKGROUND_EDGE_SKIP_SECONDS,
    BACKGROUND_VIDEO_EXTENSIONS,
)
from modules.interfaces import BackgroundCut, IBackgroundSource
from utils.exceptions import ConfigurationError, MediaNotFoundError, RenderError
from utils.fs import hash_payload, read_json, write_json
from utils.logger import get_logger, log_warn
from utils.media import ffmpeg_executable, probe_duration

__all__ = ["BackgroundLibrary", "Reservation", "free_stretches"]

logger = get_logger(__name__)

LEDGER_VERSION = 1
CUT_TIMEOUT_SECONDS = 600

Cutter = Callable[[Path, float, float, Path], None]
"""Writes ``length`` seconds of ``source`` starting at ``start`` to ``dest``."""


@dataclass(frozen=True, slots=True)
class Reservation:
    """A stretch of one library video that belongs to one project.

    Attributes:
        file: The video's file name inside the library folder.
        start: Where the stretch starts, in seconds.
        end: Where the stretch ends, in seconds.
    """

    file: str
    start: float
    end: float

    @property
    def length(self) -> float:
        """The stretch's length in seconds."""
        return self.end - self.start


def free_stretches(
    duration: float, taken: list[tuple[float, float]], *, edge: float
) -> list[tuple[float, float]]:
    """Return the parts of a video that no reservation covers.

    Args:
        duration: The video's length in seconds.
        taken: ``(start, end)`` pairs already reserved, in any order and possibly overlapping.
        edge: Seconds at both ends that are never handed out.

    Returns:
        Free ``(start, end)`` pairs in ascending order.
    """
    low, high = edge, duration - edge
    if high <= low:
        return []
    gaps: list[tuple[float, float]] = []
    cursor = low
    for start, end in sorted(taken):
        if end <= cursor:
            continue
        if start >= high:
            break
        if start > cursor:
            gaps.append((cursor, start))
        cursor = max(cursor, end)
        if cursor >= high:
            break
    if cursor < high:
        gaps.append((cursor, high))
    return gaps


class BackgroundLibrary(IBackgroundSource):
    """Reserves and cuts unused stretches from a folder of long background videos."""

    def __init__(
        self,
        folder: Path,
        ledger_path: Path,
        *,
        rng: random.Random | None = None,
        probe: Callable[[Path], float] = probe_duration,
        cutter: Cutter | None = None,
        edge_skip: float = BACKGROUND_EDGE_SKIP_SECONDS,
        clip_margin: float = BACKGROUND_CLIP_MARGIN_SECONDS,
    ) -> None:
        """Initialise the library.

        Args:
            folder: Directory holding the long videos. Subfolders are not searched.
            ledger_path: JSON file recording which project owns which stretch.
            rng: Random source, injectable so tests are deterministic.
            probe: Measures a video's duration.
            cutter: Writes one clip; ffmpeg by default.
            edge_skip: Seconds at both ends of every video that are never used.
            clip_margin: Extra seconds cut onto every clip so the editor's middle window
                lines up across scenes.
        """
        self._folder = folder
        self._ledger_path = ledger_path
        self._rng = rng or random.Random()
        self._probe = probe
        self._cutter = cutter or cut_with_ffmpeg
        self._edge_skip = edge_skip
        self._clip_margin = clip_margin

    # -- Public API ---------------------------------------------------------------------

    def cut(self, project_id: str, durations: list[float], dest_dir: Path) -> BackgroundCut:
        """Reserve footage for a project and cut it into one clip per scene.

        Args:
            project_id: The project the stretch belongs to.
            durations: Every scene's length in seconds, in playback order.
            dest_dir: Directory for the cut clips.

        Returns:
            The clips and where they came from.

        Raises:
            ValueError: If ``durations`` is empty or holds a non-positive length.
            ConfigurationError: If the video folder is missing.
            MediaNotFoundError: If no unused stretch is long enough.
            RenderError: If a clip cannot be cut.
        """
        if not durations or any(not duration > 0 for duration in durations):
            raise ValueError("Every scene duration must be a positive number of seconds.")

        needed = sum(durations) + self._clip_margin
        library = self._scan()
        reservations = self._load_ledger()
        reservation = self._reserve(project_id, needed, library, reservations)
        if reservations.get(project_id) != reservation:
            reservations[project_id] = reservation
            self._save_ledger(reservations)

        source = self._folder / reservation.file
        clips = self._cut_clips(source, reservation.start, durations, dest_dir)
        logger.info(
            "Background for %s: %s %.2f-%.2fs",
            project_id,
            source.name,
            reservation.start,
            reservation.start + needed,
        )
        return BackgroundCut(
            clips=clips,
            source=source,
            start=reservation.start,
            end=reservation.start + needed,
        )

    # -- Library ------------------------------------------------------------------------

    def _scan(self) -> dict[str, float]:
        """Measure every playable video in the folder.

        Returns:
            File name to duration in seconds, for videos that could be measured.

        Raises:
            ConfigurationError: If the folder does not exist.
            MediaNotFoundError: If it holds no playable video.
        """
        if not self._folder.is_dir():
            raise ConfigurationError(
                f"Background video folder not found: {self._folder}",
                hint="Create it and add long videos, or set background_video.enabled to false.",
            )
        library: dict[str, float] = {}
        for path in sorted(self._folder.iterdir()):
            if not path.is_file() or path.suffix.lower() not in BACKGROUND_VIDEO_EXTENSIONS:
                continue
            try:
                duration = float(self._probe(path))
            except RenderError as exc:
                log_warn(f"Skipping background video {path.name}: {exc.message}")
                continue
            if duration > 0:
                library[path.name] = duration
        if not library:
            extensions = ", ".join(sorted(BACKGROUND_VIDEO_EXTENSIONS))
            raise MediaNotFoundError(
                f"No playable video in {self._folder}.",
                hint=f"Add long videos with one of these extensions: {extensions}.",
            )
        return library

    def _reserve(
        self,
        project_id: str,
        needed: float,
        library: dict[str, float],
        reservations: dict[str, Reservation],
    ) -> Reservation:
        """Keep the project's stretch when it still fits, otherwise pick a new free one.

        Args:
            project_id: The project asking for footage.
            needed: Seconds of footage the project needs.
            library: File name to duration.
            reservations: Every recorded reservation, the project's own included.

        Returns:
            The project's reservation.

        Raises:
            MediaNotFoundError: If no free stretch is long enough.
        """
        current = reservations.get(project_id)
        if (
            current is not None
            and current.file in library
            and current.length >= needed
            and current.end <= library[current.file]
        ):
            return current

        taken: dict[str, list[tuple[float, float]]] = {}
        for owner, reservation in reservations.items():
            if owner != project_id:
                taken.setdefault(reservation.file, []).append((reservation.start, reservation.end))

        free = [
            (name, low, high)
            for name, duration in library.items()
            for low, high in free_stretches(duration, taken.get(name, []), edge=self._edge_skip)
        ]
        options = [(name, low, high) for name, low, high in free if high - low >= needed]
        if not options:
            longest = max((high - low for _, low, high in free), default=0.0)
            raise MediaNotFoundError(
                f"No unused stretch of {needed:.1f}s is left in {self._folder.name}; "
                f"the longest free stretch is {longest:.1f}s.",
                hint=(
                    f"Add more long videos to {self._folder}, or delete {self._ledger_path} "
                    "to let new videos reuse old footage."
                ),
            )

        # Weighting by the number of possible start points makes every placement across the
        # whole library equally likely, so long videos are used in proportion to their length.
        weights = [high - low - needed + 1e-3 for _, low, high in options]
        name, low, high = self._rng.choices(options, weights=weights, k=1)[0]
        start = math.floor(self._rng.uniform(low, high - needed) * 1000) / 1000
        return Reservation(file=name, start=start, end=start + needed)

    # -- Ledger -------------------------------------------------------------------------

    def _load_ledger(self) -> dict[str, Reservation]:
        """Read every valid reservation from the ledger.

        A missing ledger is empty. An unreadable one is reported and treated as empty, and
        malformed entries are skipped, so a hand-edited file can never crash a run.

        Returns:
            Project id to reservation.
        """
        if not self._ledger_path.is_file():
            return {}
        try:
            payload = read_json(self._ledger_path)
        except (OSError, ValueError) as exc:
            log_warn(f"Background ledger {self._ledger_path} is unreadable ({exc}); starting over.")
            return {}

        entries = payload.get("reservations") if isinstance(payload, dict) else None
        if not isinstance(entries, dict):
            log_warn(f"Background ledger {self._ledger_path} has no reservations; starting over.")
            return {}

        reservations: dict[str, Reservation] = {}
        for project_id, raw in entries.items():
            parsed = _parse_reservation(raw)
            if parsed is None:
                log_warn(f"Ignoring a malformed background ledger entry for {project_id}.")
                continue
            reservations[str(project_id)] = parsed
        return reservations

    def _save_ledger(self, reservations: dict[str, Reservation]) -> None:
        """Write every reservation back to the ledger atomically.

        Args:
            reservations: Project id to reservation.
        """
        payload = {
            "version": LEDGER_VERSION,
            "reservations": {
                project_id: {"file": item.file, "start": item.start, "end": item.end}
                for project_id, item in sorted(reservations.items())
            },
        }
        self._ledger_path.parent.mkdir(parents=True, exist_ok=True)
        write_json(self._ledger_path, payload)

    # -- Cutting ------------------------------------------------------------------------

    def _cut_clips(
        self, source: Path, start: float, durations: list[float], dest_dir: Path
    ) -> list[Path]:
        """Cut consecutive clips from ``source``, reusing any that were cut before.

        Clip names carry a fingerprint of the source and the cut, so an existing file is
        reused only when it holds exactly this footage.

        Args:
            source: The long video.
            start: Where the first clip starts, in seconds.
            durations: Every scene's length, in playback order.
            dest_dir: Directory for the clips.

        Returns:
            One clip path per duration.
        """
        dest_dir.mkdir(parents=True, exist_ok=True)
        size = source.stat().st_size
        clips: list[Path] = []
        offset = start
        for index, duration in enumerate(durations, start=1):
            length = duration + self._clip_margin
            key = hash_payload("background-v1", source.name, size, round(offset, 3), length)
            dest = dest_dir / f"background_{index:03d}_{key[:12]}.mp4"
            if not (dest.is_file() and dest.stat().st_size > 0):
                self._cutter(source, offset, length, dest)
            clips.append(dest)
            offset += duration
        return clips


def _parse_reservation(raw: Any) -> Reservation | None:
    """Validate one ledger entry.

    The file name must be a bare name, so a tampered ledger cannot point outside the folder.

    Args:
        raw: The decoded JSON value.

    Returns:
        The reservation, or ``None`` when the entry is malformed.
    """
    if not isinstance(raw, dict):
        return None
    name = raw.get("file")
    start = raw.get("start")
    end = raw.get("end")
    if not isinstance(name, str) or not name or Path(name).name != name:
        return None
    if not isinstance(start, int | float) or not isinstance(end, int | float):
        return None
    if isinstance(start, bool) or isinstance(end, bool):
        return None
    if not (math.isfinite(start) and math.isfinite(end) and 0 <= start < end):
        return None
    return Reservation(file=name, start=float(start), end=float(end))


def cut_with_ffmpeg(source: Path, start: float, length: float, dest: Path) -> None:
    """Re-encode ``length`` seconds of ``source`` from ``start`` into ``dest``.

    Seeking before ``-i`` is fast, and re-encoding makes the cut frame accurate; a stream
    copy could only start on a keyframe and would break the single-take effect. The file
    is written under a temporary name first, so an interrupted cut never looks finished.

    Args:
        source: The long video.
        start: Where the clip starts, in seconds.
        length: The clip's length in seconds.
        dest: Destination ``.mp4`` path.

    Raises:
        RenderError: If ffmpeg fails or times out.
    """
    partial = dest.with_name(f"{dest.stem}.part{dest.suffix}")
    command = [
        str(ffmpeg_executable()),
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        f"{start:.3f}",
        "-i",
        str(source),
        "-t",
        f"{length:.3f}",
        "-map",
        "0:v:0",
        "-map",
        "0:a:0?",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        str(partial),
    ]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=CUT_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        partial.unlink(missing_ok=True)
        raise RenderError(f"Could not cut background footage from {source.name}: {exc}") from exc

    if result.returncode != 0 or not partial.is_file():
        partial.unlink(missing_ok=True)
        last_line = (result.stderr or "").strip().splitlines()[-1:] or ["no output"]
        raise RenderError(
            f"ffmpeg could not cut background footage from {source.name}: {last_line[0]}",
            hint="The video may be corrupt. Remove it from the folder and re-run.",
        )
    partial.replace(dest)
