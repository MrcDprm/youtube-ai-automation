"""Twelve stick-figure poses drawn with Pillow."""

from __future__ import annotations

from PIL import ImageDraw

from zenn.visuals.palette import Palette

POSE_TAGS: tuple[str, ...] = (
    "standing",
    "running",
    "scared",
    "shocked",
    "thinking",
    "pointing",
    "sitting",
    "driving",
    "working",
    "reading",
    "waiting",
    "falling",
)

__all__ = ["POSE_TAGS", "draw_pose"]


def draw_pose(
    draw: ImageDraw.ImageDraw,
    tag: str,
    width: int,
    height: int,
    palette: Palette,
) -> None:
    """Draw a stick figure for ``tag`` centred on the lower third.

    Args:
        draw: Target canvas draw context.
        tag: Pose tag from ``pose-rules.json``.
        width: Frame width in pixels.
        height: Frame height in pixels.
        palette: Line and accent colours.
    """
    cx = width // 2
    foot_y = int(height * 0.78)
    scale = height / 1080.0
    stroke = max(3, int(6 * scale))
    line = palette.line
    accent = palette.accent

    head_r = int(28 * scale)
    head_y = foot_y - int(220 * scale)
    neck_y = head_y + head_r
    hip_y = foot_y - int(95 * scale)
    shoulder_y = neck_y + int(35 * scale)

    if tag == "falling":
        cx = int(width * 0.55)
        head_y = int(height * 0.35)
        hip_y = head_y + int(80 * scale)
        foot_y = hip_y + int(90 * scale)
        neck_y = head_y + head_r
        shoulder_y = neck_y + int(20 * scale)
        _head(draw, cx, head_y, head_r, line, stroke)
        _limb(draw, (cx, neck_y), (cx - int(40 * scale), hip_y), line, stroke)
        _limb(draw, (cx, shoulder_y), (cx + int(70 * scale), shoulder_y - int(30 * scale)), line, stroke)
        _limb(draw, (cx, shoulder_y), (cx - int(60 * scale), shoulder_y + int(40 * scale)), line, stroke)
        _limb(draw, (cx - int(10 * scale), hip_y), (cx + int(50 * scale), foot_y), line, stroke)
        _limb(draw, (cx - int(10 * scale), hip_y), (cx - int(80 * scale), foot_y - int(20 * scale)), line, stroke)
        return

    _head(draw, cx, head_y, head_r, line, stroke)
    _limb(draw, (cx, neck_y), (cx, hip_y), line, stroke)

    if tag == "running":
        _limb(draw, (cx, shoulder_y), (cx - int(55 * scale), shoulder_y - int(35 * scale)), line, stroke)
        _limb(draw, (cx, shoulder_y), (cx + int(45 * scale), shoulder_y + int(25 * scale)), line, stroke)
        _limb(draw, (cx, hip_y), (cx + int(65 * scale), foot_y - int(25 * scale)), line, stroke)
        _limb(draw, (cx, hip_y), (cx - int(45 * scale), foot_y), line, stroke)
        return

    if tag == "scared":
        _face_scared(draw, cx, head_y, head_r, accent, stroke)
        _limb(draw, (cx, shoulder_y), (cx - int(35 * scale), shoulder_y - int(55 * scale)), line, stroke)
        _limb(draw, (cx, shoulder_y), (cx + int(35 * scale), shoulder_y - int(55 * scale)), line, stroke)
        _limb(draw, (cx, hip_y), (cx - int(18 * scale), foot_y), line, stroke)
        _limb(draw, (cx, hip_y), (cx + int(18 * scale), foot_y), line, stroke)
        return

    if tag == "shocked":
        _face_shocked(draw, cx, head_y, head_r, accent, stroke)
        _limb(draw, (cx, shoulder_y), (cx - int(50 * scale), shoulder_y - int(10 * scale)), line, stroke)
        _limb(draw, (cx, shoulder_y), (cx + int(50 * scale), shoulder_y - int(10 * scale)), line, stroke)
        _limb(draw, (cx, hip_y), (cx - int(22 * scale), foot_y), line, stroke)
        _limb(draw, (cx, hip_y), (cx + int(22 * scale), foot_y), line, stroke)
        return

    if tag == "thinking":
        _limb(draw, (cx, shoulder_y), (cx - int(45 * scale), shoulder_y + int(15 * scale)), line, stroke)
        _limb(draw, (cx, shoulder_y), (cx + int(35 * scale), head_y + head_r // 2), line, stroke)
        draw.ellipse((cx + int(50 * scale), head_y - int(35 * scale), cx + int(90 * scale), head_y + int(5 * scale)), outline=accent, width=stroke)
        _limb(draw, (cx, hip_y), (cx - int(20 * scale), foot_y), line, stroke)
        _limb(draw, (cx, hip_y), (cx + int(20 * scale), foot_y), line, stroke)
        return

    if tag == "pointing":
        _limb(draw, (cx, shoulder_y), (cx - int(40 * scale), shoulder_y + int(25 * scale)), line, stroke)
        _limb(draw, (cx, shoulder_y), (cx + int(75 * scale), shoulder_y - int(15 * scale)), line, stroke)
        draw.ellipse((cx + int(72 * scale), shoulder_y - int(22 * scale), cx + int(88 * scale), shoulder_y - int(6 * scale)), fill=accent)
        _limb(draw, (cx, hip_y), (cx - int(20 * scale), foot_y), line, stroke)
        _limb(draw, (cx, hip_y), (cx + int(20 * scale), foot_y), line, stroke)
        return

    if tag == "sitting":
        seat_y = foot_y - int(35 * scale)
        draw.line((cx - int(55 * scale), seat_y, cx + int(55 * scale), seat_y), fill=line, width=stroke)
        hip_y = seat_y - int(5 * scale)
        _limb(draw, (cx, shoulder_y), (cx - int(40 * scale), shoulder_y + int(10 * scale)), line, stroke)
        _limb(draw, (cx, shoulder_y), (cx + int(40 * scale), shoulder_y + int(10 * scale)), line, stroke)
        _limb(draw, (cx, hip_y), (cx - int(45 * scale), foot_y - int(5 * scale)), line, stroke)
        _limb(draw, (cx, hip_y), (cx + int(45 * scale), foot_y - int(5 * scale)), line, stroke)
        return

    if tag == "driving":
        wheel_r = int(42 * scale)
        wheel_cx = cx + int(10 * scale)
        wheel_cy = shoulder_y + int(30 * scale)
        draw.arc(
            (wheel_cx - wheel_r, wheel_cy - wheel_r, wheel_cx + wheel_r, wheel_cy + wheel_r),
            start=200,
            end=340,
            fill=accent,
            width=stroke + 2,
        )
        _limb(draw, (cx, shoulder_y), (wheel_cx - int(15 * scale), wheel_cy - int(10 * scale)), line, stroke)
        _limb(draw, (cx, shoulder_y), (wheel_cx + int(20 * scale), wheel_cy), line, stroke)
        _limb(draw, (cx, hip_y), (cx - int(25 * scale), foot_y), line, stroke)
        _limb(draw, (cx, hip_y), (cx + int(25 * scale), foot_y), line, stroke)
        return

    if tag == "working":
        wrench_x = cx + int(55 * scale)
        draw.line((wrench_x, shoulder_y, wrench_x + int(35 * scale), shoulder_y + int(35 * scale)), fill=accent, width=stroke + 1)
        draw.ellipse((wrench_x + int(25 * scale), shoulder_y + int(28 * scale), wrench_x + int(45 * scale), shoulder_y + int(48 * scale)), outline=accent, width=stroke)
        _limb(draw, (cx, shoulder_y), (wrench_x, shoulder_y + int(5 * scale)), line, stroke)
        _limb(draw, (cx, shoulder_y), (cx - int(45 * scale), shoulder_y + int(20 * scale)), line, stroke)
        _limb(draw, (cx, hip_y), (cx - int(20 * scale), foot_y), line, stroke)
        _limb(draw, (cx, hip_y), (cx + int(20 * scale), foot_y), line, stroke)
        return

    if tag == "reading":
        book_w = int(70 * scale)
        book_h = int(50 * scale)
        bx = cx - book_w // 2
        by = shoulder_y
        draw.rectangle((bx, by, bx + book_w, by + book_h), outline=accent, width=stroke)
        draw.line((bx + book_w // 2, by, bx + book_w // 2, by + book_h), fill=accent, width=2)
        _limb(draw, (cx, shoulder_y), (bx - int(8 * scale), by + int(20 * scale)), line, stroke)
        _limb(draw, (cx, shoulder_y), (bx + book_w + int(8 * scale), by + int(20 * scale)), line, stroke)
        _limb(draw, (cx, hip_y), (cx - int(20 * scale), foot_y), line, stroke)
        _limb(draw, (cx, hip_y), (cx + int(20 * scale), foot_y), line, stroke)
        return

    if tag == "waiting":
        _limb(draw, (cx, shoulder_y), (cx - int(30 * scale), shoulder_y + int(35 * scale)), line, stroke)
        _limb(draw, (cx, shoulder_y), (cx + int(30 * scale), shoulder_y + int(35 * scale)), line, stroke)
        _limb(draw, (cx, hip_y), (cx - int(18 * scale), foot_y), line, stroke)
        _limb(draw, (cx, hip_y), (cx + int(18 * scale), foot_y), line, stroke)
        draw.arc(
            (cx + int(55 * scale), head_y - int(10 * scale), cx + int(95 * scale), head_y + int(30 * scale)),
            start=200,
            end=340,
            fill=accent,
            width=stroke,
        )
        return

    # standing (default)
    _limb(draw, (cx, shoulder_y), (cx - int(45 * scale), shoulder_y + int(30 * scale)), line, stroke)
    _limb(draw, (cx, shoulder_y), (cx + int(45 * scale), shoulder_y + int(30 * scale)), line, stroke)
    _limb(draw, (cx, hip_y), (cx - int(22 * scale), foot_y), line, stroke)
    _limb(draw, (cx, hip_y), (cx + int(22 * scale), foot_y), line, stroke)


def _head(draw: ImageDraw.ImageDraw, cx: int, cy: int, radius: int, color: str, stroke: int) -> None:
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=color, width=stroke)


def _limb(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    color: str,
    stroke: int,
) -> None:
    draw.line([start, end], fill=color, width=stroke)


def _face_scared(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    radius: int,
    accent: str,
    stroke: int,
) -> None:
    eye_y = cy - radius // 3
    for offset in (-radius // 2, radius // 2):
        draw.ellipse((cx + offset - 6, eye_y - 8, cx + offset + 6, eye_y + 8), fill=accent)
    draw.arc((cx - radius // 2, cy, cx + radius // 2, cy + radius), start=20, end=160, fill=accent, width=stroke)


def _face_shocked(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    radius: int,
    accent: str,
    stroke: int,
) -> None:
    eye_y = cy - radius // 3
    for offset in (-radius // 2, radius // 2):
        draw.ellipse((cx + offset - 10, eye_y - 12, cx + offset + 10, eye_y + 12), outline=accent, width=stroke)
    draw.ellipse((cx - 10, cy + radius // 4, cx + 10, cy + radius // 2 + 8), fill=accent)
