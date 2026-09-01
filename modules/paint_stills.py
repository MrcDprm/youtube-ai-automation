"""Resolve agent-drawn stills for the paint format without talking to stock APIs."""

from __future__ import annotations

from pathlib import Path

from models.scenario import VisualBeat
from utils.exceptions import MediaNotFoundError

__all__ = ["copy_paint_stills", "expected_beat_name", "resolve_paint_stills"]

_IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp")


def expected_beat_name(index: int, slug: str) -> str:
    """Return the canonical stem ``NN-slug`` for beat ``index`` (1-based)."""
    return f"{index:02d}-{slug}"


def resolve_paint_stills(
    beats: list[VisualBeat],
    *,
    project_id: str,
    search_roots: list[Path],
) -> list[Path]:
    """Find one image file per visual beat.

    Args:
        beats: Drawing slots from the scenario, in playback order.
        project_id: Used when searching ``storyboard/{project_id}/``.
        search_roots: Directories to walk, first match wins.

    Returns:
        Absolute paths, one per beat.

    Raises:
        MediaNotFoundError: If any beat is missing a still.
    """
    if len(beats) < 2:
        raise MediaNotFoundError(
            "Paint format needs at least two visual beats.",
            hint="Re-run generate --format paint so the scenario includes visual_beats.",
        )

    found: list[Path] = []
    missing: list[str] = []
    for index, beat in enumerate(beats, start=1):
        path = _resolve_one(beat, index, project_id, search_roots)
        if path is None:
            missing.append(expected_beat_name(index, beat.slug) + ".png")
        else:
            found.append(path)

    if missing:
        roots = ", ".join(str(root) for root in search_roots)
        raise MediaNotFoundError(
            f"Missing {len(missing)} paint still(s): {', '.join(missing[:8])}"
            + ("…" if len(missing) > 8 else ""),
            hint=(
                f"Drop 16:9 MS Paint PNGs into one of: {roots}. "
                "Name them NN-slug.png to match visual_beats."
            ),
        )
    return found


def copy_paint_stills(sources: list[Path], destination_dir: Path) -> list[Path]:
    """Copy resolved stills into the run clips directory as ``photo_NNN`` files.

    Args:
        sources: Absolute source images.
        destination_dir: Usually ``output/clips``.

    Returns:
        Paths inside ``destination_dir``.
    """
    destination_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for index, source in enumerate(sources, start=1):
        dest = destination_dir / f"photo_{index:03d}{source.suffix.lower()}"
        dest.write_bytes(source.read_bytes())
        written.append(dest)
    return written


def _resolve_one(
    beat: VisualBeat,
    index: int,
    project_id: str,
    search_roots: list[Path],
) -> Path | None:
    declared = beat.resolved_image
    if declared is not None and declared.is_file():
        return declared

    stem = expected_beat_name(index, beat.slug)
    names = [f"{stem}{suffix}" for suffix in _IMAGE_SUFFIXES]
    names.extend(f"{index:02d}-{beat.slug}{suffix}" for suffix in _IMAGE_SUFFIXES)

    for root in search_roots:
        if not root.is_dir():
            continue
        for name in names:
            candidate = root / name
            if candidate.is_file():
                return candidate
        prefixed = sorted(root.glob(f"{index:02d}-*"))
        for candidate in prefixed:
            if candidate.is_file() and candidate.suffix.lower() in _IMAGE_SUFFIXES:
                return candidate
        nested = root / project_id
        if nested.is_dir() and nested not in search_roots:
            nested_hit = _resolve_one(beat, index, project_id, [nested])
            if nested_hit is not None:
                return nested_hit
    return None
