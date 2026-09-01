"""Compose one Zenn frame from pose and background tags."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from zenn.visuals.backgrounds import draw_background, normalize_bg
from zenn.visuals.palette import Palette, load_palette
from zenn.visuals.poses import draw_pose

__all__ = ["compose_frame", "save_frame"]


def compose_frame(
    pose_tag: str,
    bg_tag: str,
    *,
    width: int = 1920,
    height: int = 1080,
    palette: Palette | None = None,
) -> Image.Image:
    """Render one stick-figure still.

    Args:
        pose_tag: Pose name from ``pose-rules.json``.
        bg_tag: Background name from ``pose-rules.json``.
        width: Output width in pixels.
        height: Output height in pixels.
        palette: Optional palette override.

    Returns:
        An RGB PIL image.
    """
    colours = palette or load_palette()
    effective_bg = normalize_bg(bg_tag)
    effective_pose = pose_tag if pose_tag else "standing"
    image = Image.new("RGB", (width, height), colours.background)
    draw = ImageDraw.Draw(image)
    draw_background(draw, effective_bg, width, height, colours)
    draw_pose(draw, effective_pose, width, height, colours)
    return image


def save_frame(
    pose_tag: str,
    bg_tag: str,
    dest: Path,
    *,
    width: int = 1920,
    height: int = 1080,
) -> Path:
    """Write a composed frame to ``dest`` as PNG.

    Args:
        pose_tag: Pose name.
        bg_tag: Background name.
        dest: Destination ``.png`` path.
        width: Output width.
        height: Output height.

    Returns:
        The written path.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    compose_frame(pose_tag, bg_tag, width=width, height=height).save(dest, format="PNG")
    return dest
