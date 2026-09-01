"""Render one PNG per Zenn beat."""

from __future__ import annotations

from pathlib import Path

from zenn.segmentation.beats import Beat
from zenn.visuals.compose import save_frame

__all__ = ["render_beat_frames"]


def render_beat_frames(
    beats: list[Beat],
    out_dir: Path,
    *,
    width: int,
    height: int,
) -> list[Path]:
    """Write ``beat_XXXX.png`` files aligned with ``beats``.

    Args:
        beats: Timeline-ordered visual holds.
        out_dir: Directory for PNG output.
        width: Frame width.
        height: Frame height.

    Returns:
        PNG paths in beat order.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for index, beat in enumerate(beats, start=1):
        dest = out_dir / f"beat_{index:04d}.png"
        save_frame(beat.pose_tag, beat.bg_tag, dest, width=width, height=height)
        paths.append(dest)
    return paths
