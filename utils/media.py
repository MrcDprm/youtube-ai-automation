"""Pure geometry and timing math for video processing.

Everything here is deliberately free of MoviePy imports so the scale-and-crop arithmetic that
decides every output frame can be unit-tested instantly, without ffmpeg or a real clip.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from config.constants import (
    KEN_BURNS_UPSCALE,
    ORIENTATION_RESOLUTIONS,
    ORIENTATION_TOLERANCE,
    SUBTITLE_BOTTOM_MARGIN_RATIO,
    VALID_ORIENTATIONS,
)
from utils.exceptions import RenderError

__all__ = [
    "CropPlan",
    "aspect_ratio",
    "classify_orientation",
    "distribute_duration",
    "ffmpeg_executable",
    "ken_burns_zoompan_filter",
    "make_even",
    "matches_orientation",
    "plan_scale_and_crop",
    "probe_duration",
    "resolution_for_orientation",
    "subtitle_top_y",
    "zoom_scale_at",
]


def make_even(value: int) -> int:
    """Round a pixel dimension up to the nearest even number.

    H.264 with ``yuv420p`` chroma subsampling cannot encode odd dimensions.

    Args:
        value: A pixel dimension.

    Returns:
        The same value, or one greater when it was odd. Never below 2.
    """
    rounded = max(2, int(value))
    return rounded if rounded % 2 == 0 else rounded + 1


def aspect_ratio(width: int, height: int) -> float:
    """Compute a width-to-height ratio.

    Args:
        width: Frame width in pixels.
        height: Frame height in pixels.

    Returns:
        The aspect ratio.

    Raises:
        ValueError: If ``height`` is zero or negative.
    """
    if height <= 0:
        raise ValueError(f"height must be positive, got {height}")
    return width / height


def classify_orientation(width: int, height: int) -> str:
    """Bucket a resolution into ``portrait``, ``landscape`` or ``square``.

    Args:
        width: Frame width in pixels.
        height: Frame height in pixels.

    Returns:
        The orientation name.
    """
    ratio = aspect_ratio(width, height)
    if abs(ratio - 1.0) <= ORIENTATION_TOLERANCE:
        return "square"
    return "landscape" if ratio > 1.0 else "portrait"


def matches_orientation(width: int, height: int, orientation: str) -> bool:
    """Report whether a resolution has the given orientation.

    Args:
        width: Frame width in pixels.
        height: Frame height in pixels.
        orientation: One of ``portrait``, ``landscape`` or ``square``.

    Returns:
        ``True`` when the resolution's own classification matches.

    Raises:
        ValueError: If ``orientation`` is not a recognised name.
    """
    if orientation not in VALID_ORIENTATIONS:
        raise ValueError(
            f"Unknown orientation {orientation!r}; expected one of {sorted(VALID_ORIENTATIONS)}"
        )
    return classify_orientation(width, height) == orientation


def resolution_for_orientation(orientation: str) -> tuple[int, int]:
    """Return the canonical resolution for an orientation.

    Args:
        orientation: One of ``portrait``, ``landscape`` or ``square``.

    Returns:
        The ``(width, height)`` pair.

    Raises:
        ValueError: If ``orientation`` is not recognised.
    """
    try:
        return ORIENTATION_RESOLUTIONS[orientation]
    except KeyError as exc:
        raise ValueError(
            f"Unknown orientation {orientation!r}; expected one of {sorted(VALID_ORIENTATIONS)}"
        ) from exc


@dataclass(frozen=True, slots=True)
class CropPlan:
    """The exact transform that fits a source frame to a target frame.

    Attributes:
        source_width: Original frame width.
        source_height: Original frame height.
        target_width: Desired output width.
        target_height: Desired output height.
        scale: Uniform factor applied to the source before cropping.
        scaled_width: Source width after scaling, rounded to an even number.
        scaled_height: Source height after scaling, rounded to an even number.
        crop_x: Left edge of the crop window within the scaled frame.
        crop_y: Top edge of the crop window within the scaled frame.
    """

    source_width: int
    source_height: int
    target_width: int
    target_height: int
    scale: float
    scaled_width: int
    scaled_height: int
    crop_x: int
    crop_y: int

    @property
    def crop_center(self) -> tuple[int, int]:
        """Centre point of the crop window, as MoviePy's ``cropped`` expects."""
        return (
            self.crop_x + self.target_width // 2,
            self.crop_y + self.target_height // 2,
        )

    @property
    def scaled_size(self) -> tuple[int, int]:
        """The intermediate size to resize to before cropping."""
        return (self.scaled_width, self.scaled_height)

    @property
    def target_size(self) -> tuple[int, int]:
        """The final output size."""
        return (self.target_width, self.target_height)


def plan_scale_and_crop(
    source_width: int,
    source_height: int,
    target_width: int,
    target_height: int,
) -> CropPlan:
    """Compute a cover-style scale and centre-crop.

    The source is scaled by ``max(tw/w, th/h)`` so it fully covers the target, then the excess
    is cropped equally from both sides. This never letterboxes and never distorts: one axis
    matches exactly and the other is trimmed.

    Args:
        source_width: Source frame width in pixels.
        source_height: Source frame height in pixels.
        target_width: Desired output width in pixels.
        target_height: Desired output height in pixels.

    Returns:
        A :class:`CropPlan` describing the resize and crop.

    Raises:
        ValueError: If any dimension is not positive.
    """
    if min(source_width, source_height, target_width, target_height) <= 0:
        raise ValueError(
            "All dimensions must be positive, got "
            f"source {source_width}x{source_height}, target {target_width}x{target_height}"
        )

    scale = max(target_width / source_width, target_height / source_height)

    scaled_width = make_even(round(source_width * scale))
    scaled_height = make_even(round(source_height * scale))

    # Rounding to even can leave a scaled edge a pixel short of the target; nudge it up so the
    # crop window always fits inside the scaled frame.
    scaled_width = max(scaled_width, make_even(target_width))
    scaled_height = max(scaled_height, make_even(target_height))

    crop_x = (scaled_width - target_width) // 2
    crop_y = (scaled_height - target_height) // 2

    return CropPlan(
        source_width=source_width,
        source_height=source_height,
        target_width=target_width,
        target_height=target_height,
        scale=scale,
        scaled_width=scaled_width,
        scaled_height=scaled_height,
        crop_x=crop_x,
        crop_y=crop_y,
    )


def subtitle_top_y(
    frame_height: int,
    box_height: int,
    *,
    margin_ratio: float = SUBTITLE_BOTTOM_MARGIN_RATIO,
) -> int:
    """Place a caption box so its bottom edge sits above the frame bottom.

    MoviePy ``with_position(("center", y))`` uses ``y`` as the top of the clip. Using a
    ratio of the frame as that top edge lets a two-line box overflow the frame.

    Args:
        frame_height: Output frame height in pixels.
        box_height: Rendered caption clip height in pixels.
        margin_ratio: Fraction of the frame to keep clear below the text.

    Returns:
        Y coordinate of the top of the caption box, never negative.
    """
    margin = max(0, int(round(frame_height * margin_ratio)))
    return max(0, int(frame_height) - max(0, int(box_height)) - margin)


def ken_burns_zoompan_filter(
    width: int,
    height: int,
    fps: int,
    frames: int,
    start_scale: float,
    end_scale: float,
    *,
    upscale: int = KEN_BURNS_UPSCALE,
) -> str:
    """Build an ffmpeg filter that zooms a still without 1-pixel jitter.

    The photograph is cover-cropped to the output frame, scaled up by ``upscale``, then
    zoompan'd back to ``width``×``height``. The large intermediate buffer makes each zoom
    increment a fraction of an output pixel.

    Args:
        width: Output width.
        height: Output height.
        fps: Output frame rate.
        frames: Number of output frames.
        start_scale: Zoom at frame 0 (typically 1.0).
        end_scale: Zoom at the last frame (typically 1.08).
        upscale: Integer scale of the fitted frame before zoompan.

    Returns:
        An ffmpeg ``-vf`` filter graph.
    """
    count = max(1, int(frames))
    denom = max(count - 1, 1)
    zoom_expr = (
        f"min({start_scale:.6f}+({end_scale:.6f}-{start_scale:.6f})*on/{denom},"
        f"{end_scale:.6f})"
    )
    factor = max(2, int(upscale))
    wide = width * factor
    high = height * factor
    # Top-anchored zoom keeps titles and labels visible; center crop was clipping MS Paint text.
    return (
        f"scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},"
        f"scale={wide}:{high},"
        f"zoompan=z='{zoom_expr}':x='iw/2-(iw/zoom/2)':y='0'"
        f":d=1:s={width}x{height}:fps={fps}"
    )


def zoom_scale_at(elapsed: float, duration: float, start: float, end: float) -> float:
    """Interpolate the Ken Burns zoom factor at a point in time.

    Args:
        elapsed: Seconds since the segment started.
        duration: Total segment duration in seconds.
        start: Scale at ``elapsed == 0``.
        end: Scale at ``elapsed == duration``.

    Returns:
        The interpolated scale, clamped to the ``[start, end]`` range so a frame requested
        slightly past the end (which MoviePy does at segment boundaries) never over-zooms.
    """
    if duration <= 0:
        return start
    progress = min(1.0, max(0.0, elapsed / duration))
    return start + (end - start) * progress


def distribute_duration(total: float, parts: int, minimum: float = 0.5) -> list[float]:
    """Split a duration across several clips.

    Args:
        total: Total seconds to cover.
        parts: Number of clips to split across.
        minimum: Smallest acceptable slice; fewer, longer slices are returned rather than
            producing sub-``minimum`` flashes.

    Returns:
        A list of durations summing to ``total`` (within floating-point tolerance).

    Raises:
        ValueError: If ``parts`` is not positive or ``total`` is not positive.
    """
    if parts <= 0:
        raise ValueError(f"parts must be positive, got {parts}")
    if total <= 0:
        raise ValueError(f"total must be positive, got {total}")

    usable_parts = max(1, min(parts, int(total // minimum) or 1))
    slice_length = total / usable_parts
    durations = [slice_length] * usable_parts
    # Absorb accumulated float error into the last slice so the sum is exact.
    durations[-1] = total - slice_length * (usable_parts - 1)
    return durations


def ffmpeg_executable() -> Path:
    """Locate the ffmpeg binary this project will use.

    Prefers the copy bundled with ``imageio-ffmpeg`` so the pipeline works without a
    system-wide install, and falls back to one on ``PATH``.

    Returns:
        Absolute path to an ffmpeg executable.

    Raises:
        RenderError: If no ffmpeg binary can be found.
    """
    try:
        import imageio_ffmpeg

        return Path(imageio_ffmpeg.get_ffmpeg_exe())
    except (ImportError, RuntimeError, OSError):
        discovered = shutil.which("ffmpeg")
        if discovered:
            return Path(discovered)
        raise RenderError(
            "No ffmpeg binary found.",
            hint=(
                "Reinstall dependencies with 'pip install -r requirements.txt'; "
                "imageio-ffmpeg bundles its own ffmpeg build."
            ),
        ) from None


def probe_duration(path: Path) -> float:
    """Measure a media file's duration.

    Audio files are probed with ``mutagen``, which reads only the header and is far faster
    than decoding. Anything else, and any file mutagen cannot parse, falls back to MoviePy.

    Args:
        path: Media file to inspect.

    Returns:
        Duration in seconds.

    Raises:
        RenderError: If the duration cannot be determined.
    """
    if not path.is_file():
        raise RenderError(f"Cannot probe duration, file does not exist: {path}")

    if path.suffix.lower() in {".mp3", ".m4a", ".aac", ".ogg", ".opus", ".flac", ".wav"}:
        try:
            from mutagen import File as MutagenFile

            parsed = MutagenFile(str(path))
            if parsed is not None and parsed.info is not None:
                duration = float(parsed.info.length)
                if duration > 0:
                    return duration
        except (OSError, AttributeError, ValueError, TypeError):
            pass

    try:
        from moviepy import AudioFileClip, VideoFileClip

        is_audio = path.suffix.lower() in {".mp3", ".m4a", ".aac", ".ogg", ".opus", ".flac", ".wav"}
        clip = AudioFileClip(str(path)) if is_audio else VideoFileClip(str(path))
        try:
            duration = float(clip.duration or 0.0)
        finally:
            clip.close()
    except Exception as exc:
        raise RenderError(
            f"Could not determine the duration of {path.name}: {exc}",
            hint="The file may be truncated or corrupt. Delete it and re-run to re-fetch.",
        ) from exc

    if duration <= 0:
        raise RenderError(
            f"{path.name} reports a duration of zero.",
            hint="The file is likely a zero-byte or truncated download. Re-run with --force.",
        )
    return duration
