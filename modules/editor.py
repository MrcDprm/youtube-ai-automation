"""Video composition and encoding with MoviePy 2.x.

Three decisions shape everything here.

Audio drives the cut. Each scene lasts exactly as long as its narration plus the configured
gap, and the footage is stretched, looped or trimmed to fit, never the other way round.

Nothing is ever letterboxed or distorted. Source clips are scaled to cover the target frame
and then centre-cropped, so one axis matches exactly and the excess on the other is discarded.

Scenes are rendered individually before assembly. That per-scene file is what makes a run
resumable: a crash during final encoding never costs the scenes already completed.

This module targets the MoviePy 2.x API exclusively. The legacy 1.x clip helpers and the old
top-level editor shim were removed upstream, so none of them appear here.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

import numpy as np
from moviepy import (
    AudioArrayClip,
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    TextClip,
    VideoFileClip,
    afx,
    concatenate_audioclips,
    concatenate_videoclips,
    vfx,
)

from config.constants import (
    AUDIO_BITRATE,
    AUDIO_CODEC,
    FIRST_FRAMES_SKIP_SECONDS,
    PIXEL_FORMAT,
    SUBTITLE_WIDTH_RATIO,
    VIDEO_CODEC,
    ZOOM_END_SCALE,
    ZOOM_START_SCALE,
)
from models.scenario import Scenario
from modules.interfaces import IVideoEditor, ScenePlan, SubtitleCue
from utils.exceptions import RenderError
from utils.fs import ensure_parent, format_bytes, human_duration
from utils.logger import get_logger, log_info, log_warn
from utils.media import distribute_duration, plan_scale_and_crop, probe_duration

__all__ = ["MoviePyEditor"]

logger = get_logger(__name__)

MIN_SEGMENT_SECONDS = 0.20
"""Shorter than this and a segment reads as a glitch rather than a cut."""


def _close_quietly(*clips: Any) -> None:
    """Close clips without letting cleanup failures mask the original error.

    MoviePy keeps ffmpeg subprocesses and file handles open per clip. On Windows an unclosed
    reader keeps a lock on the file, so a later write to the same path fails.

    Args:
        *clips: Clips or ``None`` values to close.
    """
    for clip in clips:
        if clip is None:
            continue
        with contextlib.suppress(Exception):
            clip.close()


class MoviePyEditor(IVideoEditor):
    """Renders scenes and assembles the finished video."""

    def __init__(
        self,
        *,
        temp_dir: Path,
        threads: int = 4,
        crf: int = 20,
        preset: str = "medium",
        force: bool = False,
    ) -> None:
        """Initialise the editor.

        Args:
            temp_dir: Directory for encoder scratch files.
            threads: ffmpeg worker threads.
            crf: Constant rate factor; lower is higher quality and larger.
            preset: libx264 speed preset.
            force: When true, re-render scenes even if an output file already exists.
        """
        self._temp_dir = temp_dir
        self._threads = threads
        self._crf = crf
        self._preset = preset
        self._force = force
        self._temp_dir.mkdir(parents=True, exist_ok=True)

    # ----------------------------------------------------------------------------------
    # Scene rendering
    # ----------------------------------------------------------------------------------

    def build_scene(self, plan: ScenePlan) -> Path:
        """Render one scene to its own MP4.

        Args:
            plan: The fully resolved scene plan.

        Returns:
            Path to the rendered scene file.

        Raises:
            RenderError: If composition or encoding fails.
        """
        if not self._force and plan.output_path.is_file() and plan.output_path.stat().st_size > 0:
            logger.debug("Scene %d already rendered, reusing", plan.scene.id)
            return plan.output_path

        if not plan.media_paths:
            raise RenderError(
                f"Scene {plan.scene.id} has no source footage.",
                hint="Every scene needs at least one downloaded clip or a local_media path.",
            )

        opened: list[Any] = []
        composed: Any = None
        narration: Any = None

        try:
            segments = self._build_segments(plan, opened)
            composed = (
                segments[0]
                if len(segments) == 1
                else concatenate_videoclips(segments, method="chain")
            )
            composed = composed.with_duration(plan.total_duration).with_fps(plan.fps)

            narration = AudioFileClip(str(plan.audio_path))
            composed = composed.without_audio().with_audio(
                self._pad_audio(narration, plan.total_duration)
            )

            if plan.burn_subtitles:
                composed = self._burn_subtitles(composed, plan, opened)

            self._encode(composed, plan.output_path, fps=plan.fps, with_audio=True)
        except RenderError:
            raise
        except Exception as exc:
            raise RenderError(
                f"Failed to render scene {plan.scene.id}: {exc}",
                hint=(
                    "A source clip may be corrupt. Delete .cache/media and re-run, or set "
                    "local_media for this scene."
                ),
            ) from exc
        finally:
            _close_quietly(composed, narration, *opened)

        size = plan.output_path.stat().st_size if plan.output_path.is_file() else 0
        logger.info(
            "Scene %d rendered: %s, %s",
            plan.scene.id,
            human_duration(plan.total_duration),
            format_bytes(size),
        )
        return plan.output_path

    def _build_segments(self, plan: ScenePlan, opened: list[Any]) -> list[Any]:
        """Cut, normalize and fit every source clip for a scene.

        Args:
            plan: The scene plan.
            opened: Accumulator for clips that must be closed by the caller.

        Returns:
            Video segments whose durations sum to the scene length.

        Raises:
            RenderError: If no segment could be produced.
        """
        needed = plan.total_duration
        durations = distribute_duration(needed, len(plan.media_paths), MIN_SEGMENT_SECONDS)
        segments: list[Any] = []

        for media_path, wanted in zip(plan.media_paths, durations, strict=False):
            segment = self._prepare_segment(
                media_path,
                wanted=wanted,
                target_width=plan.width,
                target_height=plan.height,
                fps=plan.fps,
                zoom=plan.scene.zoom_effect,
                opened=opened,
            )
            segments.append(segment)

        if not segments:
            raise RenderError(f"Scene {plan.scene.id} produced no usable video segments.")
        return segments

    def _prepare_segment(
        self,
        media_path: Path,
        *,
        wanted: float,
        target_width: int,
        target_height: int,
        fps: int,
        zoom: bool,
        opened: list[Any],
    ) -> Any:
        """Turn one source file into a segment of exactly ``wanted`` seconds.

        Args:
            media_path: Source video file.
            wanted: Required segment length in seconds.
            target_width: Output frame width.
            target_height: Output frame height.
            fps: Output frame rate.
            zoom: Whether to apply the Ken Burns effect.
            opened: Accumulator for clips that must be closed by the caller.

        Returns:
            A clip at the target resolution and duration.

        Raises:
            RenderError: If the source cannot be opened.
        """
        try:
            source = VideoFileClip(str(media_path))
        except Exception as exc:
            raise RenderError(
                f"Could not open source clip {media_path.name}: {exc}",
                hint="Delete .cache/media and re-run to re-download it.",
            ) from exc
        opened.append(source)

        clip = self._extract_window(source, wanted)
        clip = self._fit_to_frame(clip, target_width, target_height)
        if zoom:
            clip = self._apply_zoom(clip, target_width, target_height, wanted)
        return clip.with_duration(wanted).with_fps(fps)

    @staticmethod
    def _extract_window(source: Any, wanted: float) -> Any:
        """Take a ``wanted``-second window from the middle of a clip, looping if too short.

        Stock clips frequently open on a fade from black, so the window starts after a short
        skip whenever the source is long enough to allow it.

        Args:
            source: The opened source clip.
            wanted: Required duration in seconds.

        Returns:
            A clip of exactly ``wanted`` seconds.
        """
        available = float(source.duration or 0.0)

        if available <= 0:
            return source.with_duration(wanted)

        if available < wanted:
            looped = source.with_effects([vfx.Loop(duration=wanted)])
            return looped.with_duration(wanted)

        skip = FIRST_FRAMES_SKIP_SECONDS if available >= wanted + FIRST_FRAMES_SKIP_SECONDS else 0.0
        usable = available - skip
        start = skip + max(0.0, (usable - wanted) / 2.0)
        end = min(available, start + wanted)
        if end - start < wanted:
            start = max(0.0, end - wanted)
        return source.subclipped(start, end)

    @staticmethod
    def _fit_to_frame(clip: Any, target_width: int, target_height: int) -> Any:
        """Scale a clip to cover the target frame, then centre-crop the excess.

        Args:
            clip: The clip to fit.
            target_width: Output frame width.
            target_height: Output frame height.

        Returns:
            A clip at exactly ``target_width`` by ``target_height``.
        """
        source_width, source_height = clip.size
        crop_plan = plan_scale_and_crop(
            int(source_width), int(source_height), target_width, target_height
        )

        resized = clip.resized(new_size=crop_plan.scaled_size)
        center_x, center_y = crop_plan.crop_center
        return resized.cropped(
            x_center=center_x,
            y_center=center_y,
            width=target_width,
            height=target_height,
        )

    @staticmethod
    def _apply_zoom(clip: Any, target_width: int, target_height: int, duration: float) -> Any:
        """Apply a slow linear zoom and crop back to the target frame.

        MoviePy's ``Resize`` accepts a callable returning a scale factor per timestamp, which
        is how the Ken Burns move is expressed. The zoomed frame is then re-cropped, since
        scaling up makes it larger than the target.

        Args:
            clip: A clip already at the target resolution.
            target_width: Output frame width.
            target_height: Output frame height.
            duration: Segment length, over which the zoom completes.

        Returns:
            The zooming clip, cropped back to the target frame.
        """
        span = max(duration, 1e-3)

        def scale_at(t: float) -> float:
            """Interpolate the zoom factor, clamped so boundary frames never over-zoom."""
            progress = min(1.0, max(0.0, float(t) / span))
            return ZOOM_START_SCALE + (ZOOM_END_SCALE - ZOOM_START_SCALE) * progress

        zoomed = clip.with_effects([vfx.Resize(new_size=scale_at)])
        return zoomed.with_effects(
            [
                vfx.Crop(
                    x_center=target_width // 2,
                    y_center=target_height // 2,
                    width=target_width,
                    height=target_height,
                )
            ]
        )

    @staticmethod
    def _pad_audio(narration: Any, total_duration: float) -> Any:
        """Extend narration audio with real trailing silence to fill the scene.

        The gap has to be actual samples rather than a longer declared duration: reading a
        clip past the end of its underlying audio is undefined, and ffmpeg would either error
        or repeat the final frame.

        Args:
            narration: The narration audio clip.
            total_duration: Scene length in seconds.

        Returns:
            An audio clip of exactly ``total_duration`` seconds.
        """
        spoken = float(narration.duration or 0.0)
        if spoken >= total_duration:
            return narration.subclipped(0, total_duration)

        gap = total_duration - spoken
        fps = int(getattr(narration, "fps", 0) or 44100)
        channels = int(getattr(narration, "nchannels", 0) or 2)
        samples = max(1, int(round(gap * fps)))

        silence = AudioArrayClip(np.zeros((samples, channels), dtype=np.float64), fps=fps)
        return concatenate_audioclips([narration, silence])

    def _burn_subtitles(self, base: Any, plan: ScenePlan, opened: list[Any]) -> Any:
        """Composite caption cues over a scene.

        Args:
            base: The scene video.
            plan: The scene plan, holding cues and appearance settings.
            opened: Accumulator for clips that must be closed by the caller.

        Returns:
            The scene with captions composited on top.

        Raises:
            RenderError: If the font cannot be used for text rendering.
        """
        if plan.font_path is None:
            return base

        settings = plan.subtitles
        box_width = int(plan.width * SUBTITLE_WIDTH_RATIO)
        vertical = int(plan.height * settings.position_ratio)
        layers: list[Any] = [base]

        for cue in plan.subtitle_cues:
            visible = self._clamp_cue(cue, plan.total_duration)
            if visible is None:
                continue
            start, end = visible
            try:
                text_clip = TextClip(
                    font=str(plan.font_path),
                    text=cue.text,
                    font_size=settings.font_size,
                    color=settings.color,
                    stroke_color=settings.stroke_color,
                    stroke_width=settings.stroke_width,
                    method="caption",
                    size=(box_width, None),
                    text_align="center",
                    horizontal_align="center",
                    vertical_align="center",
                    transparent=True,
                )
            except ValueError as exc:
                raise RenderError(
                    f"Pillow could not render text with the font {plan.font_path}: {exc}",
                    hint=(
                        "The file may not be a valid TrueType font. Run "
                        "'python main.py doctor --fix' to install a known-good one."
                    ),
                ) from exc

            positioned = (
                text_clip.with_start(start)
                .with_duration(end - start)
                .with_position(("center", vertical))
            )
            opened.append(text_clip)
            layers.append(positioned)

        if len(layers) == 1:
            return base

        composite = CompositeVideoClip(layers, size=(plan.width, plan.height))
        return composite.with_duration(plan.total_duration)

    @staticmethod
    def _clamp_cue(cue: SubtitleCue, limit: float) -> tuple[float, float] | None:
        """Clip a cue's time range to the scene, dropping it when nothing remains.

        Args:
            cue: The cue to clamp.
            limit: Scene duration in seconds.

        Returns:
            The visible ``(start, end)`` range, or ``None`` when the cue falls outside.
        """
        start = max(0.0, cue.start)
        end = min(cue.end, limit)
        if end - start < 0.05:
            return None
        return start, end

    # ----------------------------------------------------------------------------------
    # Final assembly
    # ----------------------------------------------------------------------------------

    def assemble(self, scene_paths: list[Path], scenario: Scenario, out_path: Path) -> Path:
        """Concatenate rendered scenes into the finished video.

        Args:
            scene_paths: Scene files in playback order.
            scenario: The project, for crossfade, music and encoder settings.
            out_path: Destination MP4 path.

        Returns:
            The written path.

        Raises:
            RenderError: If assembly fails or the result exceeds the configured maximum
                duration.
        """
        if not scene_paths:
            raise RenderError("Cannot assemble a video with no scenes.")

        missing = [path for path in scene_paths if not path.is_file()]
        if missing:
            names = ", ".join(path.name for path in missing)
            raise RenderError(f"Missing rendered scene file(s): {names}")

        clips: list[Any] = []
        timeline: Any = None
        music: Any = None

        try:
            clips = [VideoFileClip(str(path)) for path in scene_paths]
            timeline = self._concatenate(clips, scenario.video.crossfade_seconds)

            self._enforce_duration_limit(
                float(timeline.duration or 0.0), scenario.video.max_duration_seconds
            )

            if scenario.video.background_music.enabled:
                timeline, music = self._mix_music(timeline, scenario)

            self._encode(
                timeline,
                out_path,
                fps=scenario.video.fps,
                with_audio=True,
                crf=scenario.video.video_bitrate_crf,
                preset=scenario.video.preset,
            )
        except RenderError:
            raise
        except Exception as exc:
            raise RenderError(f"Final assembly failed: {exc}") from exc
        finally:
            _close_quietly(timeline, music, *clips)

        size = out_path.stat().st_size if out_path.is_file() else 0
        logger.info("Final video written: %s (%s)", out_path.name, format_bytes(size))
        return out_path

    @staticmethod
    def _concatenate(clips: Sequence[Any], crossfade: float) -> Any:
        """Join scene clips, with or without crossfades.

        ``method="chain"`` is the cheap path and is correct here because every scene was
        rendered at the same resolution and frame rate. It cannot crossfade, though, so any
        non-zero crossfade switches to ``method="compose"`` with negative padding, which
        overlaps each scene with its predecessor.

        Args:
            clips: Scene clips in playback order.
            crossfade: Crossfade duration in seconds; ``0`` means hard cuts.

        Returns:
            The concatenated timeline.
        """
        if crossfade <= 0 or len(clips) < 2:
            return concatenate_videoclips(list(clips), method="chain")

        shortest = min(float(clip.duration or 0.0) for clip in clips)
        effective = min(crossfade, max(0.0, shortest / 2.0 - 0.05))
        if effective <= 0:
            log_warn(
                f"Crossfade of {crossfade:.2f}s does not fit the shortest scene "
                f"({shortest:.2f}s); using hard cuts instead."
            )
            return concatenate_videoclips(list(clips), method="chain")

        faded = [clips[0]] + [clip.with_effects([vfx.CrossFadeIn(effective)]) for clip in clips[1:]]
        return concatenate_videoclips(faded, method="compose", padding=-effective)

    @staticmethod
    def _enforce_duration_limit(duration: float, maximum: float) -> None:
        """Stop the run when the assembled video is longer than allowed.

        Truncating silently would cut a sentence in half and publish it, so this raises
        instead.

        Args:
            duration: Assembled duration in seconds.
            maximum: Configured ceiling in seconds.

        Raises:
            RenderError: If ``duration`` exceeds ``maximum``.
        """
        if duration <= maximum:
            return
        raise RenderError(
            f"Assembled video is {human_duration(duration)} "
            f"({duration:.1f}s), over the {maximum:.0f}s limit set by "
            "video.max_duration_seconds.",
            hint=(
                "Shorten the narration, remove a scene, or raise max_duration_seconds. "
                "The video was not truncated, because that would cut mid-sentence."
            ),
        )

    def _mix_music(self, timeline: Any, scenario: Scenario) -> tuple[Any, Any]:
        """Mix a ducked background music bed under the narration.

        MoviePy has no sidechain compressor, so ducking is applied as a deterministic gain
        envelope: the music sits at ``volume * duck_to`` for the whole narrated span and
        returns to ``volume`` only in the trailing tail. The result is identical on every run.

        Args:
            timeline: The assembled video, with narration already attached.
            scenario: The project, for music settings.

        Returns:
            A tuple of the timeline with music mixed in, and the music clip so the caller can
            close it.
        """
        settings = scenario.video.background_music
        music_file = settings.resolved_file
        duration = float(timeline.duration or 0.0)

        if music_file is None or not music_file.is_file():
            log_warn(f"Background music file is missing: {music_file}. Continuing without it.")
            return timeline, None

        music = AudioFileClip(str(music_file))
        source_length = float(music.duration or 0.0)

        if source_length <= 0:
            log_warn("Background music has zero duration; continuing without it.")
            _close_quietly(music)
            return timeline, None

        bed = (
            music.with_effects([afx.AudioLoop(duration=duration)])
            if source_length < duration
            else music.subclipped(0, duration)
        )

        ducked = settings.volume * settings.duck_to
        bed = bed.with_volume_scaled(ducked)

        fade_in = min(settings.fade_in_seconds, duration / 2)
        fade_out = min(settings.fade_out_seconds, duration / 2)
        effects = []
        if fade_in > 0:
            effects.append(afx.AudioFadeIn(fade_in))
        if fade_out > 0:
            effects.append(afx.AudioFadeOut(fade_out))
        if effects:
            bed = bed.with_effects(effects)

        narration = timeline.audio
        mixed = CompositeAudioClip([narration, bed]) if narration is not None else bed
        log_info(
            f"Mixed background music at {ducked:.3f} gain "
            f"({settings.volume:.2f} x {settings.duck_to:.2f} ducking)"
        )
        return timeline.with_audio(mixed), music

    # ----------------------------------------------------------------------------------
    # Encoding
    # ----------------------------------------------------------------------------------

    def _encode(
        self,
        clip: Any,
        out_path: Path,
        *,
        fps: int,
        with_audio: bool,
        crf: int | None = None,
        preset: str | None = None,
    ) -> None:
        """Write a clip to disk as H.264 / AAC.

        Args:
            clip: The clip to encode.
            out_path: Destination file.
            fps: Output frame rate.
            with_audio: Whether to include an audio track.
            crf: Constant rate factor override.
            preset: libx264 preset override.

        Raises:
            RenderError: If ffmpeg fails or writes nothing.
        """
        ensure_parent(out_path)
        temp_audio = self._temp_dir / f"{out_path.stem}_audio.m4a"

        try:
            clip.write_videofile(
                str(out_path),
                codec=VIDEO_CODEC,
                audio=with_audio,
                audio_codec=AUDIO_CODEC,
                audio_bitrate=AUDIO_BITRATE,
                fps=fps,
                preset=preset or self._preset,
                threads=self._threads,
                temp_audiofile=str(temp_audio),
                remove_temp=True,
                logger=None,
                ffmpeg_params=[
                    "-pix_fmt",
                    PIXEL_FORMAT,
                    "-crf",
                    str(crf if crf is not None else self._crf),
                    "-movflags",
                    "+faststart",
                ],
            )
        except Exception as exc:
            raise RenderError(
                f"ffmpeg failed while writing {out_path.name}: {exc}",
                hint=(
                    "Run 'python main.py doctor' to confirm the ffmpeg binary resolves, and "
                    "check that the output drive has free space."
                ),
            ) from exc
        finally:
            with contextlib.suppress(OSError):
                temp_audio.unlink(missing_ok=True)

        if not out_path.is_file() or out_path.stat().st_size == 0:
            raise RenderError(
                f"ffmpeg reported success but {out_path.name} is empty.",
                hint="Check the per-run log file for the ffmpeg output.",
            )

    # ----------------------------------------------------------------------------------
    # Introspection
    # ----------------------------------------------------------------------------------

    @staticmethod
    def probe(path: Path) -> float:
        """Measure a rendered file's duration.

        Args:
            path: The media file.

        Returns:
            Duration in seconds.

        Raises:
            RenderError: If the duration cannot be determined.
        """
        return probe_duration(path)

    @staticmethod
    def total_duration(paths: Iterable[Path]) -> float:
        """Sum the durations of several media files.

        Args:
            paths: Files to measure.

        Returns:
            Total duration in seconds.
        """
        return sum(probe_duration(path) for path in paths)
