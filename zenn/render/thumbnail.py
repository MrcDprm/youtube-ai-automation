"""YouTube thumbnail template for Zenn / Badly Drawn Why stick-cut."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from config.constants import THUMBNAIL_JPEG_QUALITY, THUMBNAIL_SIZE, YOUTUBE_THUMBNAIL_MAX_BYTES
from utils.exceptions import RenderError
from utils.fs import ensure_parent, format_bytes
from zenn.visuals.compose import compose_frame
from zenn.visuals.palette import load_palette

__all__ = ["build_zenn_thumbnail"]

HOOK_MAX_CHARS = 28


def build_zenn_thumbnail(
    hook: str,
    out_path: Path,
    *,
    font_path: Path | None = None,
    font_size: int = 96,
) -> Path:
    """Create a 1280x720 JPEG: stick figure preview + yellow hook on black.

    Args:
        hook: Two-to-four-word ALL CAPS hook (not the full title).
        out_path: Destination ``.jpg`` path.
        font_path: Optional bold font; Pillow default when omitted.
        font_size: Starting hook size; shrunk to fit.

    Returns:
        The written JPEG path.

    Raises:
        RenderError: If the hook is empty or encoding fails.
    """
    text = " ".join(hook.strip().upper().split())
    if not text:
        raise RenderError("Zenn thumbnail needs a non-empty hook.")
    if len(text) > HOOK_MAX_CHARS:
        text = text[: HOOK_MAX_CHARS - 1].rstrip() + "…"

    palette = load_palette()
    preview = compose_frame("standing", "blank", width=1920, height=1080, palette=palette)
    canvas = preview.resize(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(canvas)

    scrim_h = int(THUMBNAIL_SIZE[1] * 0.42)
    overlay = Image.new("RGBA", THUMBNAIL_SIZE, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for row in range(scrim_h):
        alpha = int(210 * (row / max(1, scrim_h)))
        overlay_draw.line(
            [(0, THUMBNAIL_SIZE[1] - scrim_h + row), (THUMBNAIL_SIZE[0], THUMBNAIL_SIZE[1] - scrim_h + row)],
            fill=(0, 0, 0, alpha),
        )
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(canvas)

    font = _load_font(font_path, font_size)
    margin = int(THUMBNAIL_SIZE[0] * 0.06)
    max_width = THUMBNAIL_SIZE[0] - margin * 2
    while font_size >= 36:
        font = _load_font(font_path, font_size)
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=4)
        if bbox[2] - bbox[0] <= max_width:
            break
        font_size -= 4

    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=4)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (THUMBNAIL_SIZE[0] - text_w) // 2
    y = THUMBNAIL_SIZE[1] - int(THUMBNAIL_SIZE[1] * 0.12) - text_h
    draw.text(
        (x, y),
        text,
        font=font,
        fill=palette.accent,
        stroke_width=4,
        stroke_fill="#000000",
    )

    ensure_parent(out_path)
    quality = THUMBNAIL_JPEG_QUALITY
    while quality >= 60:
        canvas.save(out_path, format="JPEG", quality=quality, optimize=True)
        size = out_path.stat().st_size if out_path.is_file() else 0
        if size <= YOUTUBE_THUMBNAIL_MAX_BYTES:
            return out_path
        quality -= 5
    if not out_path.is_file() or out_path.stat().st_size == 0:
        raise RenderError("Could not write a Zenn thumbnail JPEG.")
    if out_path.stat().st_size > YOUTUBE_THUMBNAIL_MAX_BYTES:
        raise RenderError(
            f"Zenn thumbnail still exceeds YouTube limit ({format_bytes(out_path.stat().st_size)})."
        )
    return out_path


def _load_font(font_path: Path | None, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if font_path is not None and font_path.is_file():
        try:
            return ImageFont.truetype(str(font_path), size=size)
        except OSError:
            pass
    try:
        return ImageFont.truetype("arialbd.ttf", size=size)
    except OSError:
        return ImageFont.load_default()
