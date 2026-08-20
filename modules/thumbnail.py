"""Thumbnail generation with Pillow.

A frame is pulled from early in the finished video, fitted to YouTube's 1280x720 canvas with
the same cover-and-crop rule the editor uses, then overlaid with a gradient scrim and the
video title. The JPEG is re-encoded at decreasing quality until it fits under YouTube's 2 MB
upload ceiling, so the result is always accepted.
"""

from __future__ import annotations

import contextlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from config.constants import (
    THUMBNAIL_FRAME_RATIO,
    THUMBNAIL_JPEG_QUALITY,
    THUMBNAIL_MIN_JPEG_QUALITY,
    THUMBNAIL_SIZE,
    YOUTUBE_THUMBNAIL_MAX_BYTES,
)
from modules.interfaces import IThumbnailBuilder
from utils.exceptions import RenderError
from utils.fs import ensure_parent, format_bytes
from utils.logger import get_logger

__all__ = ["PillowThumbnailBuilder"]

logger = get_logger(__name__)

SCRIM_HEIGHT_RATIO = 0.55
"""Fraction of the canvas height covered by the bottom darkening gradient."""

SCRIM_MAX_ALPHA = 225
TEXT_MARGIN_RATIO = 0.055
MIN_FONT_SIZE = 24
MAX_TITLE_LINES = 3


class PillowThumbnailBuilder(IThumbnailBuilder):
    """Builds a 1280x720 JPEG thumbnail from a video frame plus a title overlay."""

    def __init__(
        self,
        font_path: Path | None,
        *,
        font_size: int = 72,
        text_color: str = "#FFFFFF",
        stroke_color: str = "#000000",
        stroke_width: int = 4,
        frame_ratio: float = THUMBNAIL_FRAME_RATIO,
    ) -> None:
        """Initialise the builder.

        Args:
            font_path: Font used for the title. When ``None``, Pillow's bitmap default is used
                and the title renders small but legibly.
            font_size: Starting title size in points; shrunk automatically to fit.
            text_color: Title fill colour.
            stroke_color: Title outline colour, which keeps text readable over any footage.
            stroke_width: Title outline width in pixels.
            frame_ratio: How far into the video to sample the source frame, as a fraction.
        """
        self._font_path = font_path
        self._font_size = font_size
        self._text_color = text_color
        self._stroke_color = stroke_color
        self._stroke_width = stroke_width
        self._frame_ratio = min(max(frame_ratio, 0.0), 0.95)

    # -- Public API ---------------------------------------------------------------------

    def build(self, video_path: Path, title: str, out_path: Path) -> Path:
        """Create a thumbnail from a frame of the finished video.

        Args:
            video_path: The rendered video to sample.
            title: Text to overlay.
            out_path: Destination JPEG path.

        Returns:
            The written path.

        Raises:
            RenderError: If the frame cannot be extracted or the image cannot be written.
        """
        frame = self._grab_frame(video_path)
        canvas = self._fit_to_canvas(frame)
        canvas = self._apply_scrim(canvas)
        if title.strip():
            canvas = self._draw_title(canvas, title.strip())
        return self._save(canvas, out_path)

    # -- Stages -------------------------------------------------------------------------

    def _grab_frame(self, video_path: Path) -> Image.Image:
        """Extract a single frame from the video.

        Args:
            video_path: The video to sample.

        Returns:
            The frame as an RGB image.

        Raises:
            RenderError: If the video cannot be read.
        """
        if not video_path.is_file():
            raise RenderError(f"Cannot build a thumbnail, video not found: {video_path}")

        from moviepy import VideoFileClip

        clip = None
        try:
            clip = VideoFileClip(str(video_path))
            duration = float(clip.duration or 0.0)
            timestamp = min(max(0.0, duration * self._frame_ratio), max(0.0, duration - 0.05))
            array = clip.get_frame(timestamp)
            logger.debug("Sampled thumbnail frame at %.2fs of %.2fs", timestamp, duration)
        except Exception as exc:
            raise RenderError(
                f"Could not read a frame from {video_path.name}: {exc}",
                hint="The rendered video may be corrupt. Re-run with --force.",
            ) from exc
        finally:
            if clip is not None:
                with contextlib.suppress(Exception):
                    clip.close()

        return Image.fromarray(np.asarray(array, dtype=np.uint8)).convert("RGB")

    @staticmethod
    def _fit_to_canvas(frame: Image.Image) -> Image.Image:
        """Scale and centre-crop a frame onto the 1280x720 thumbnail canvas.

        Uses the same cover rule as the editor, so a portrait video yields a centre slice
        rather than pillarboxed bars.

        Args:
            frame: The source frame.

        Returns:
            An image at exactly :data:`config.constants.THUMBNAIL_SIZE`.
        """
        target_width, target_height = THUMBNAIL_SIZE
        source_width, source_height = frame.size

        scale = max(target_width / source_width, target_height / source_height)
        scaled = (
            max(target_width, int(round(source_width * scale))),
            max(target_height, int(round(source_height * scale))),
        )
        resized = frame.resize(scaled, Image.Resampling.LANCZOS)

        left = (scaled[0] - target_width) // 2
        top = (scaled[1] - target_height) // 2
        return resized.crop((left, top, left + target_width, top + target_height))

    @staticmethod
    def _apply_scrim(canvas: Image.Image) -> Image.Image:
        """Darken the lower portion of the image so overlaid text stays readable.

        Args:
            canvas: The thumbnail canvas.

        Returns:
            The canvas with a bottom-up gradient composited over it.
        """
        width, height = canvas.size
        scrim_height = int(height * SCRIM_HEIGHT_RATIO)
        if scrim_height <= 0:
            return canvas

        ramp = np.linspace(0, SCRIM_MAX_ALPHA, scrim_height, dtype=np.uint8)
        alpha = np.zeros((height, width), dtype=np.uint8)
        alpha[height - scrim_height :, :] = ramp[:, None]

        overlay = Image.new("RGB", canvas.size, (0, 0, 0))
        return Image.composite(overlay, canvas, Image.fromarray(alpha, mode="L"))

    def _draw_title(self, canvas: Image.Image, title: str) -> Image.Image:
        """Draw the title across the bottom of the thumbnail.

        The font size is reduced until the text fits within
        :data:`MAX_TITLE_LINES` lines and the available width.

        Args:
            canvas: The thumbnail canvas.
            title: The text to draw.

        Returns:
            The canvas with the title drawn on it.
        """
        width, height = canvas.size
        margin = int(width * TEXT_MARGIN_RATIO)
        available = width - margin * 2

        draw = ImageDraw.Draw(canvas)
        font, lines = self._fit_text(draw, title, available, height)

        line_heights = [self._line_height(draw, line, font) for line in lines]
        spacing = max(4, int(self._font_size * 0.12))
        block_height = sum(line_heights) + spacing * (len(lines) - 1)

        y = height - margin - block_height
        for line, line_height in zip(lines, line_heights, strict=True):
            draw.text(
                (margin, y),
                line,
                font=font,
                fill=self._text_color,
                stroke_width=self._stroke_width,
                stroke_fill=self._stroke_color,
            )
            y += line_height + spacing

        return canvas

    def _fit_text(
        self,
        draw: ImageDraw.ImageDraw,
        title: str,
        available_width: int,
        canvas_height: int,
    ) -> tuple[ImageFont.FreeTypeFont | ImageFont.ImageFont, list[str]]:
        """Choose the largest font size at which the title fits.

        Args:
            draw: Drawing context used to measure text.
            title: The text to lay out.
            available_width: Usable width in pixels.
            canvas_height: Canvas height, used to cap the total text block.

        Returns:
            The chosen font and the wrapped lines.
        """
        size = self._font_size
        while size >= MIN_FONT_SIZE:
            font = self._load_font(size)
            lines = self._wrap(draw, title, font, available_width)
            if len(lines) <= MAX_TITLE_LINES:
                block = sum(self._line_height(draw, line, font) for line in lines)
                if block <= canvas_height * 0.45:
                    return font, lines
            size = int(size * 0.9) if int(size * 0.9) < size else size - 1

        font = self._load_font(MIN_FONT_SIZE)
        lines = self._wrap(draw, title, font, available_width)[:MAX_TITLE_LINES]
        return font, lines

    def _load_font(self, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        """Load the title font at a given size.

        Args:
            size: Point size.

        Returns:
            A Pillow font. Falls back to the built-in bitmap font when no TrueType file is
            configured or the file cannot be parsed.
        """
        if self._font_path is not None:
            try:
                return ImageFont.truetype(str(self._font_path), size)
            except OSError as exc:
                logger.warning(
                    "Could not load the thumbnail font %s (%s); using Pillow's default.",
                    self._font_path,
                    exc,
                )
        return ImageFont.load_default()

    @staticmethod
    def _wrap(
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
        available_width: int,
    ) -> list[str]:
        """Word-wrap text to a pixel width.

        Args:
            draw: Drawing context used to measure text.
            text: The text to wrap.
            font: The font it will be drawn in.
            available_width: Usable width in pixels.

        Returns:
            The wrapped lines. Words wider than the line are kept whole rather than split.
        """
        words = text.split()
        if not words:
            return []

        lines: list[str] = []
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if draw.textlength(candidate, font=font) <= available_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    @staticmethod
    def _line_height(
        draw: ImageDraw.ImageDraw,
        line: str,
        font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    ) -> int:
        """Measure a single line's height in pixels.

        Args:
            draw: Drawing context used to measure text.
            line: The text to measure.
            font: The font it will be drawn in.

        Returns:
            The line height in pixels.
        """
        box = draw.textbbox((0, 0), line or "Ag", font=font)
        return max(1, int(round(box[3] - box[1])))

    def _save(self, canvas: Image.Image, out_path: Path) -> Path:
        """Write the thumbnail as a JPEG under YouTube's size limit.

        Args:
            canvas: The finished image.
            out_path: Destination path.

        Returns:
            The written path.

        Raises:
            RenderError: If the image cannot be written, or cannot be squeezed under the
                2 MB ceiling.
        """
        ensure_parent(out_path)
        quality = THUMBNAIL_JPEG_QUALITY

        while quality >= THUMBNAIL_MIN_JPEG_QUALITY:
            try:
                canvas.save(
                    out_path, format="JPEG", quality=quality, optimize=True, progressive=True
                )
            except OSError as exc:
                raise RenderError(f"Could not write the thumbnail to {out_path}: {exc}") from exc

            size = out_path.stat().st_size
            if size <= YOUTUBE_THUMBNAIL_MAX_BYTES:
                logger.info(
                    "Thumbnail written: %s (%s, quality %d)",
                    out_path.name,
                    format_bytes(size),
                    quality,
                )
                return out_path
            quality -= 10

        raise RenderError(
            f"Could not compress the thumbnail below {format_bytes(YOUTUBE_THUMBNAIL_MAX_BYTES)}.",
            hint="The source frame is unusually detailed. Try a different frame_ratio.",
        )
