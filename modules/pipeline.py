"""The pipeline orchestrator.

This module imports only :mod:`modules.interfaces`, :mod:`models`, :mod:`config` and
:mod:`utils`. It never names a concrete provider, engine, editor or uploader. Every
collaborator arrives through the constructor, so switching stock footage providers or speech
engines is a change to the composition root in ``main.py`` and to nothing here.

Stage order: preflight, narration, subtitles, footage, per-scene render, assembly, thumbnail,
upload, manifest. The manifest is written in a ``finally`` block, so a failed run still leaves
a machine-readable record of how far it got and why it stopped.
"""

from __future__ import annotations

import asyncio
import time
import traceback
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from config.constants import (
    PHOTO_FALLBACK_QUERIES,
    PROJECT_ROOT,
    PROVIDER_LOCAL,
    STORY_DURATION_TOLERANCE_SECONDS,
)
from config.settings import Settings
from models.scenario import Scenario, Scene, resolve_project_path
from modules.interfaces import (
    IMediaProvider,
    ISubtitleBuilder,
    IThumbnailBuilder,
    ITTSEngine,
    IUploader,
    IVideoEditor,
    MediaCandidate,
    MediaCredit,
    ScenePlan,
    SubtitleCue,
    TTSResult,
    UploadResult,
)
from modules.paint_stills import copy_paint_stills, resolve_paint_stills
from modules.story_duration import keep_leading_scenes, spoken_length
from modules.studio_pack import (
    find_paint_thumbnail,
    prepare_youtube_thumbnail,
    write_studio_pack,
)
from utils.exceptions import MediaNotFoundError, PipelineError, RenderError
from utils.fs import (
    format_bytes,
    human_duration,
    resolve_font,
    write_json,
)
from utils.logger import (
    get_logger,
    log_blank,
    log_info,
    log_metric,
    log_renderable,
    log_step,
    log_success,
    log_warn,
    make_step_progress,
    summary_table,
)
from zenn.render.frames import render_beat_frames
from zenn.render.thumbnail import build_zenn_thumbnail
from zenn.render.timeline import collect_word_cues, story_beats

__all__ = ["PipelineOptions", "RunManifest", "VideoPipeline"]

logger = get_logger(__name__)

TOTAL_STAGES = 8


@dataclass(slots=True)
class PipelineOptions:
    """Per-run switches that change what the pipeline does, not how it is wired.

    Attributes:
        dry_run: Plan and report without synthesizing, downloading, rendering or uploading.
        no_upload: Render everything but skip publishing, overriding the scenario.
        force: Ignore caches and re-do every expensive step.
        scene_limit: Render only the first N scenes, for quick iteration.
        keep_temp: Leave intermediate files in place for inspection.
        assume_yes: Skip the interactive confirmation for public uploads.
    """

    dry_run: bool = False
    no_upload: bool = False
    force: bool = False
    scene_limit: int | None = None
    keep_temp: bool = False
    assume_yes: bool = False


@dataclass
class RunManifest:
    """A machine-readable record of one run.

    Written whether the run succeeds or fails, so a crashed run can be diagnosed and resumed
    without re-reading the console scrollback.
    """

    project_id: str
    started_at: str
    status: str = "running"
    failed_stage: str | None = None
    error: str | None = None
    traceback_digest: str | None = None
    finished_at: str | None = None
    duration_seconds: float = 0.0
    resolution: list[int] = field(default_factory=list)
    fps: int = 0
    voice: str = ""
    scenes: list[dict[str, Any]] = field(default_factory=list)
    credits: list[dict[str, str]] = field(default_factory=list)
    artifacts: dict[str, str] = field(default_factory=dict)
    stage_timings: dict[str, float] = field(default_factory=dict)
    video_duration_seconds: float = 0.0
    video_size_bytes: int = 0
    youtube_video_id: str | None = None
    youtube_url: str | None = None
    youtube_privacy_status: str | None = None
    active_stage: str | None = field(default=None, repr=False)
    """Stage currently executing. Internal bookkeeping, not part of the serialised manifest."""

    def to_dict(self) -> dict[str, Any]:
        """Render the manifest as a JSON-serialisable dictionary.

        Returns:
            A plain dictionary. Secrets are never recorded here by construction: only paths,
            durations, credits and public identifiers are stored.
        """
        return {
            "project_id": self.project_id,
            "status": self.status,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_seconds": round(self.duration_seconds, 2),
            "failed_stage": self.failed_stage,
            "error": self.error,
            "traceback_digest": self.traceback_digest,
            "video": {
                "resolution": self.resolution,
                "fps": self.fps,
                "duration_seconds": round(self.video_duration_seconds, 2),
                "size_bytes": self.video_size_bytes,
            },
            "voice": self.voice,
            "scenes": self.scenes,
            "credits": self.credits,
            "artifacts": self.artifacts,
            "stage_timings": {name: round(value, 2) for name, value in self.stage_timings.items()},
            "youtube": {
                "video_id": self.youtube_video_id,
                "url": self.youtube_url,
                "privacy_status": self.youtube_privacy_status,
            },
        }


class _StageTimer:
    """Context manager that records a stage's wall time into the manifest.

    A timing is stored only when the stage completes. A stage that raised must not look
    finished, because the failure report identifies the failing stage by finding the first one
    with no recorded timing.
    """

    def __init__(self, manifest: RunManifest, name: str) -> None:
        """Initialise the timer.

        Args:
            manifest: The manifest to record into.
            name: Stage name used as the key.
        """
        self._manifest = manifest
        self._name = name
        self._start = 0.0

    def __enter__(self) -> _StageTimer:
        """Start timing and mark this stage as the one in progress."""
        self._start = time.perf_counter()
        self._manifest.active_stage = self._name
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        """Record the elapsed time, but only on a clean exit."""
        if exc_type is None:
            self._manifest.stage_timings[self._name] = time.perf_counter() - self._start
            self._manifest.active_stage = None


class VideoPipeline:
    """Turns a validated scenario into a rendered, optionally published video."""

    def __init__(
        self,
        *,
        scenario: Scenario,
        settings: Settings,
        tts_engine: ITTSEngine,
        media_provider: IMediaProvider,
        subtitle_builder: ISubtitleBuilder,
        video_editor: IVideoEditor,
        thumbnail_builder: IThumbnailBuilder,
        uploader: IUploader | None = None,
        options: PipelineOptions | None = None,
    ) -> None:
        """Wire the pipeline from injected collaborators.

        Args:
            scenario: The validated project.
            settings: Runtime settings and paths.
            tts_engine: Speech synthesis implementation.
            media_provider: Stock footage implementation.
            subtitle_builder: Subtitle construction implementation.
            video_editor: Composition and encoding implementation.
            thumbnail_builder: Thumbnail generation implementation.
            uploader: Publishing implementation. ``None`` disables uploading entirely.
            options: Per-run switches.
        """
        self._scenario = scenario
        self._settings = settings
        self._tts = tts_engine
        self._media = media_provider
        self._subtitles = subtitle_builder
        self._editor = video_editor
        self._thumbnails = thumbnail_builder
        self._uploader = uploader
        self._options = options or PipelineOptions()

        self._manifest = RunManifest(
            project_id=scenario.project_id,
            started_at=datetime.now(UTC).isoformat(),
            resolution=list(scenario.video.resolution),
            fps=scenario.video.fps,
            voice=scenario.tts.voice,
        )
        self._credits: list[MediaCredit] = []
        self._tts_results: dict[int, TTSResult] = {}
        self._scene_cues: dict[int, list[SubtitleCue]] = {}
        self._timeline_cues: list[SubtitleCue] = []
        self._scene_media: dict[int, list[Path]] = {}
        self._story_photos: list[Path] = []
        self._scene_paths: list[Path] = []
        self._font_path: Path | None = None
        self._srt_path: Path | None = None
        self._scene_keep: int | None = None

    # ----------------------------------------------------------------------------------
    # Entry point
    # ----------------------------------------------------------------------------------

    def run(self) -> RunManifest:
        """Execute the pipeline.

        Returns:
            The run manifest, whose ``status`` reports the outcome.

        Raises:
            PipelineError: If any stage fails. The manifest is written first.
        """
        started = time.perf_counter()
        try:
            self._prepare()
            if self._options.dry_run:
                self._report_plan()
                self._manifest.status = "dry-run"
                return self._manifest

            self._stage_narration()
            self._fit_story_duration()
            self._stage_subtitles()
            if self._scenario.video.is_longform:
                if self._scenario.video.is_zenn:
                    log_info("Zenn stick-cut path: skipping MS Paint still fetch.")
                elif self._scenario.video.is_paint:
                    self._stage_paint_stills()
                else:
                    self._stage_story_photos()
                if self._scenario.video.is_zenn:
                    final_video = self._stage_zenn_assemble()
                else:
                    final_video = self._stage_story_assemble()
            else:
                self._stage_footage()
                self._stage_scenes()
                final_video = self._stage_assemble()
            thumbnail = self._stage_thumbnail(final_video)
            if self._scenario.video.is_paint:
                self._stage_studio_pack(final_video, thumbnail)
            self._stage_upload(final_video, thumbnail)

            self._manifest.status = "success"
            return self._manifest
        except PipelineError as exc:
            self._record_failure(exc)
            raise
        except KeyboardInterrupt:
            self._manifest.status = "interrupted"
            self._manifest.failed_stage = "user"
            self._manifest.error = "Interrupted by the user."
            raise
        except Exception as exc:
            self._record_failure(exc)
            raise
        finally:
            self._manifest.duration_seconds = time.perf_counter() - started
            self._manifest.finished_at = datetime.now(UTC).isoformat()
            self._write_manifest()
            if self._manifest.status == "success":
                self._report_summary()

    # ----------------------------------------------------------------------------------
    # Stages
    # ----------------------------------------------------------------------------------

    def _prepare(self) -> None:
        """Create directories and resolve the font before any expensive work starts."""
        self._settings.ensure_directories()

        if self._scenario.subtitles.enabled and self._scenario.subtitles.burn_in:
            requested = resolve_project_path(self._scenario.subtitles.font)
            self._font_path, warning = resolve_font(requested, fonts_dir=self._settings.fonts_dir)
            if warning:
                log_warn(warning)

    def _report_plan(self) -> None:
        """Print the resolved plan for a dry run, touching no network."""
        scenes = self._selected_scenes()
        width, height = self._scenario.video.resolution
        rows = [
            ("Project", self._scenario.project_id),
            ("Format", self._scenario.video.format),
            ("Scenes", str(len(scenes))),
            ("Resolution", f"{width}x{height} @ {self._scenario.video.fps}fps"),
            ("Estimated length", human_duration(self._scenario.estimated_narration_seconds())),
            ("Voice", f"{self._scenario.tts.voice} (rate {self._scenario.tts.rate})"),
            ("Subtitles", self._describe_subtitles()),
            ("Font", str(self._font_path) if self._font_path else "not needed"),
            ("Background music", self._describe_music()),
            ("Upload", self._describe_upload()),
            ("Output", str(self._final_video_path())),
        ]
        log_blank()
        log_renderable(summary_table("Resolved plan (dry run)", rows))
        log_blank()

        for scene in scenes:
            source = (
                f"local: {scene.local_media}"
                if scene.local_media
                else f"search: {', '.join(scene.search_terms)}"
            )
            log_info(
                f"Scene {scene.id}: {scene.clips_per_scene} clip(s), "
                f"{len(scene.narration)} chars, {source}"
            )

        log_success("Dry run complete. No network calls were made; only the manifest was written.")

    def _stage_narration(self) -> None:
        """Synthesize narration for every selected scene."""
        log_step(1, TOTAL_STAGES, "Narration")
        scenes = self._selected_scenes()

        with _StageTimer(self._manifest, "narration"):
            results = asyncio.run(self._synthesize_all(scenes))

        for scene, result in zip(scenes, results, strict=True):
            self._tts_results[scene.id] = result

        total = sum(result.duration for result in results)
        cached = sum(1 for result in results if result.cached)
        log_success(
            f"Narration ready: {len(results)} scene(s), {human_duration(total)} total"
            + (f", {cached} from cache" if cached else "")
        )

    def _fit_story_duration(self) -> None:
        """Drop trailing story chapters when measured speech overshoots ``--minutes``."""
        target = self._scenario.video.target_duration_seconds
        if not self._scenario.video.is_longform or target is None:
            return
        scenes = list(self._scenario.scenes)
        if self._options.scene_limit is not None:
            scenes = scenes[: max(1, self._options.scene_limit)]
        durations = [self._tts_results[scene.id].duration for scene in scenes]
        gap = self._scenario.video.scene_gap_seconds
        keep = keep_leading_scenes(durations, target, gap=gap)
        total = spoken_length(durations[:keep], gap)
        self._scene_keep = keep
        if keep < len(scenes):
            log_warn(
                f"Dropping {len(scenes) - keep} trailing chapter(s) so speech lands near "
                f"{human_duration(target)} (now {human_duration(total)})."
            )
        elif total + STORY_DURATION_TOLERANCE_SECONDS < target:
            log_warn(f"Narration is {human_duration(total)}; target was {human_duration(target)}.")

    async def _synthesize_all(self, scenes: list[Scene]) -> list[TTSResult]:
        """Synthesize every scene concurrently.

        The engine caps its own concurrency, so launching all scenes at once is safe.

        Args:
            scenes: Scenes to narrate.

        Returns:
            One result per scene, in scene order.
        """
        tasks = [
            self._tts.synthesize(
                scene.narration,
                self._settings.audio_dir() / f"scene_{scene.id:03d}.mp3",
                self._scenario.tts,
            )
            for scene in scenes
        ]
        return list(await asyncio.gather(*tasks))

    def _stage_subtitles(self) -> None:
        """Build per-scene cues and write the whole-video SRT sidecar."""
        log_step(2, TOTAL_STAGES, "Subtitles")

        if not self._scenario.subtitles.enabled:
            log_info("Subtitles are disabled in the scenario; skipping.")
            return

        srt_path = self._settings.subtitles_dir() / f"{self._scenario.project_id}.srt"

        with _StageTimer(self._manifest, "subtitles"):
            offset = 0.0
            timeline: list[list[SubtitleCue]] = []

            for scene in self._selected_scenes():
                result = self._tts_results[scene.id]
                scene_cues = self._build_scene_cues(result)
                self._scene_cues[scene.id] = scene_cues
                timeline.append([cue.shifted(offset) for cue in scene_cues])
                offset += result.duration + self._scenario.video.scene_gap_seconds

            merged = self._merge_cues(timeline)
            merged = self._subtitles.finish(merged, self._scenario.subtitles)
            self._timeline_cues = merged
            self._subtitles.write_srt(merged, srt_path)
            self._srt_path = srt_path
            self._manifest.artifacts["subtitles"] = str(srt_path)

        log_success(f"Wrote {len(merged)} subtitle cue(s) to {srt_path.name}")

    def _build_scene_cues(self, result: TTSResult) -> list[SubtitleCue]:
        """Build one scene's cues from its word timings.

        Args:
            result: The scene's synthesis result.

        Returns:
            Cues relative to the scene's own timeline.
        """
        return self._subtitles.build(result.word_cues, self._scenario.subtitles, 0.0)

    @staticmethod
    def _merge_cues(groups: list[list[SubtitleCue]]) -> list[SubtitleCue]:
        """Flatten and renumber per-scene cues onto one timeline.

        Args:
            groups: Per-scene cues, already offset.

        Returns:
            A single ordered, renumbered list.
        """
        flattened = [cue for group in groups for cue in group]
        flattened.sort(key=lambda cue: (cue.start, cue.end))
        return [cue.renumbered(index) for index, cue in enumerate(flattened, start=1)]

    def _stage_footage(self) -> None:
        """Find and download source clips for every scene."""
        log_step(3, TOTAL_STAGES, "Stock footage")
        scenes = self._selected_scenes()

        with _StageTimer(self._manifest, "footage"), make_step_progress() as progress:
            task = progress.add_task("Fetching footage", total=len(scenes))
            for scene in scenes:
                self._scene_media[scene.id] = self._gather_scene_media(scene)
                progress.advance(task)

        downloaded = sum(len(paths) for paths in self._scene_media.values())
        log_success(f"{downloaded} clip(s) ready across {len(scenes)} scene(s)")

    def _gather_scene_media(self, scene: Scene) -> list[Path]:
        """Resolve one scene's source clips, preferring a local override.

        Args:
            scene: The scene to source footage for.

        Returns:
            Local paths to the scene's clips.

        Raises:
            MediaNotFoundError: If no footage could be found for the scene.
        """
        local = scene.resolved_local_media
        if local is not None:
            logger.debug("Scene %d uses local media %s", scene.id, local.name)
            self._credits.append(
                MediaCredit(
                    provider=PROVIDER_LOCAL,
                    author_name="local file",
                    author_url="",
                    page_url=str(local.name),
                )
            )
            return [local]

        orientation = scene.orientation or self._scenario.video.orientation
        candidates = self._find_candidates(scene, orientation)

        paths: list[Path] = []
        for index, candidate in enumerate(candidates, start=1):
            destination = self._settings.clips_dir() / f"scene_{scene.id:03d}_{index:02d}.mp4"
            paths.append(self._media.download(candidate, destination))
            self._credits.append(candidate.credit())

        if not paths:
            raise MediaNotFoundError(
                f"No footage could be downloaded for scene {scene.id}.",
                hint="Broaden search_terms, or set local_media for this scene.",
            )
        return paths

    def _find_candidates(self, scene: Scene, orientation: str) -> list[MediaCandidate]:
        """Search for a scene's clips through the injected provider.

        Uses the provider's own multi-query search when it offers one, and otherwise falls
        back to the plain :meth:`IMediaProvider.search` contract. This keeps the orchestrator
        compatible with any provider, not just the composite one.

        Args:
            scene: The scene to source footage for.
            orientation: Desired orientation.

        Returns:
            The selected candidates.

        Raises:
            MediaNotFoundError: If the provider yields nothing usable.
        """
        find_best = getattr(self._media, "find_best", None)
        if callable(find_best):
            found: list[MediaCandidate] = find_best(
                scene.search_terms,
                orientation,
                scene.min_clip_duration,
                scene.clips_per_scene,
            )
            return list(found)

        candidates: list[MediaCandidate] = []
        for term in scene.search_terms:
            candidates.extend(
                self._media.search(
                    term, orientation, scene.min_clip_duration, scene.clips_per_scene
                )
            )
            if len(candidates) >= scene.clips_per_scene:
                break

        if not candidates:
            raise MediaNotFoundError(
                f"No footage found for scene {scene.id} ({', '.join(scene.search_terms)})."
            )
        return candidates[: scene.clips_per_scene]

    def _stage_story_photos(self) -> None:
        """Download the unique stills that make up the story visual track."""
        log_step(3, TOTAL_STAGES, "Stock stills")
        visual = self._scenario.video.story_visual
        queries: list[str] = []
        for scene in self._selected_scenes():
            queries.extend(scene.search_terms)

        with _StageTimer(self._manifest, "footage"):
            candidates = self._collect_story_stills(queries, visual.photo_count)
            paths: list[Path] = []
            for index, candidate in enumerate(candidates, start=1):
                destination = self._settings.clips_dir() / f"photo_{index:03d}.jpg"
                paths.append(self._media.download(candidate, destination))
                self._credits.append(candidate.credit())
            self._story_photos = paths

        log_success(f"{len(self._story_photos)} still(s) ready for the story visual track")

    def _stage_paint_stills(self) -> None:
        """Load agent-drawn MS Paint stills; never search Pexels."""
        log_step(3, TOTAL_STAGES, "Paint stills")
        beats = list(self._scenario.video.visual_beats)
        roots = self._paint_search_roots()
        with _StageTimer(self._manifest, "footage"):
            sources = resolve_paint_stills(
                beats,
                project_id=self._scenario.project_id,
                search_roots=roots,
            )
            self._story_photos = copy_paint_stills(sources, self._settings.clips_dir())
        log_success(f"{len(self._story_photos)} paint still(s) ready (no stock search)")

    def _paint_search_roots(self) -> list[Path]:
        """Folders the image agent may drop stills into."""
        storyboard = self._settings.storyboard_dir()
        project = self._scenario.project_id
        return [
            storyboard / project,
            storyboard,
            PROJECT_ROOT / "output" / "storyboard" / project,
            PROJECT_ROOT / "output" / "storyboard",
        ]

    def _collect_story_stills(self, queries: list[str], needed: int) -> list[MediaCandidate]:
        """Search the injected provider for ``needed`` distinct photographs.

        Args:
            queries: English search phrases from the chapters, early ones first.
            needed: How many unique stills to return.

        Returns:
            Candidates in selection order.

        Raises:
            MediaNotFoundError: If fewer than ``needed`` unique stills could be found.
        """
        orientation = self._scenario.video.orientation
        used: set[str] = set()
        chosen: list[MediaCandidate] = []
        ladder = [term.strip() for term in queries if term.strip()]
        for fallback in PHOTO_FALLBACK_QUERIES:
            if fallback not in ladder:
                ladder.append(fallback)

        for query in ladder:
            if len(chosen) >= needed:
                break
            found = self._media.search(query, orientation, 0.0, max(needed * 2, 15))
            for candidate in found:
                if candidate.dedup_key in used:
                    continue
                used.add(candidate.dedup_key)
                chosen.append(candidate)
                if len(chosen) >= needed:
                    break

        if len(chosen) < needed:
            raise MediaNotFoundError(
                f"Needed {needed} unique stills but only found {len(chosen)}.",
                hint="Broaden search_terms, or add PIXABAY_API_KEY as a photo fallback.",
            )
        return chosen[:needed]

    def _stage_story_assemble(self) -> Path:
        """Render the two-act stills track under concatenated narration."""
        log_step(5, TOTAL_STAGES, "Story render")
        scenes = self._selected_scenes()
        audio_paths = [self._tts_results[scene.id].audio_path for scene in scenes]
        audio_durations = [self._tts_results[scene.id].duration for scene in scenes]
        out_path = self._final_video_path()

        with _StageTimer(self._manifest, "assemble"):
            final = self._editor.build_photo_story(
                self._story_photos,
                audio_paths,
                audio_durations,
                self._timeline_cues,
                self._scenario,
                self._font_path,
                out_path,
            )

        size = final.stat().st_size if final.is_file() else 0
        self._manifest.artifacts["video"] = str(final)
        self._manifest.video_size_bytes = size
        self._manifest.video_duration_seconds = sum(
            self._tts_results[scene.id].duration + self._scenario.video.scene_gap_seconds
            for scene in scenes
        )
        for scene in scenes:
            result = self._tts_results[scene.id]
            self._manifest.scenes.append(
                {
                    "id": scene.id,
                    "narration_chars": len(scene.narration),
                    "audio_path": str(result.audio_path),
                    "audio_duration": round(result.duration, 2),
                    "total_duration": round(
                        result.duration + self._scenario.video.scene_gap_seconds, 2
                    ),
                    "clips": [str(path) for path in self._story_photos],
                    "subtitle_cues": len(self._scene_cues.get(scene.id, [])),
                    "scene_path": "",
                    "zoom_effect": True,
                }
            )
        log_success(f"Final video: {final.name} ({format_bytes(size)})")
        return final

    def _stage_zenn_assemble(self) -> Path:
        """Render programmatic stick-cut beats under concatenated narration."""
        log_step(5, TOTAL_STAGES, "Zenn render")
        scenes = self._selected_scenes()
        gap = self._scenario.video.scene_gap_seconds
        beats = story_beats(scenes, self._tts_results, gap)
        word_cues = collect_word_cues(scenes, self._tts_results, gap)
        width, height = self._scenario.video.resolution
        frames_dir = self._settings.clips_dir() / "zenn"
        frame_paths = render_beat_frames(beats, frames_dir, width=width, height=height)
        audio_paths = [self._tts_results[scene.id].audio_path for scene in scenes]
        audio_durations = [self._tts_results[scene.id].duration for scene in scenes]
        out_path = self._final_video_path()

        with _StageTimer(self._manifest, "assemble"):
            final = self._editor.build_zenn_story(
                beats,
                frame_paths,
                audio_paths,
                audio_durations,
                word_cues,
                self._scenario,
                self._font_path,
                out_path,
            )

        size = final.stat().st_size if final.is_file() else 0
        self._manifest.artifacts["video"] = str(final)
        self._manifest.video_size_bytes = size
        self._manifest.video_duration_seconds = sum(
            self._tts_results[scene.id].duration + gap for scene in scenes
        )
        self._manifest.artifacts["zenn_beats"] = str(len(beats))
        for scene in scenes:
            result = self._tts_results[scene.id]
            self._manifest.scenes.append(
                {
                    "id": scene.id,
                    "narration_chars": len(scene.narration),
                    "audio_path": str(result.audio_path),
                    "audio_duration": round(result.duration, 2),
                    "total_duration": round(result.duration + gap, 2),
                    "clips": [str(path) for path in frame_paths],
                    "subtitle_cues": len(self._scene_cues.get(scene.id, [])),
                    "scene_path": "",
                    "zoom_effect": False,
                }
            )
        log_success(f"Final video: {final.name} ({format_bytes(size)}, {len(beats)} beats)")
        return final

    def _stage_scenes(self) -> None:
        """Render each scene to its own file."""
        log_step(4, TOTAL_STAGES, "Scene rendering")
        scenes = self._selected_scenes()

        with _StageTimer(self._manifest, "scenes"), make_step_progress() as progress:
            task = progress.add_task("Rendering scenes", total=len(scenes))
            for scene in scenes:
                plan = self._build_scene_plan(scene)
                self._scene_paths.append(self._editor.build_scene(plan))
                self._manifest.scenes.append(
                    {
                        "id": scene.id,
                        "narration_chars": len(scene.narration),
                        "audio_path": str(plan.audio_path),
                        "audio_duration": round(plan.audio_duration, 2),
                        "total_duration": round(plan.total_duration, 2),
                        "clips": [str(path) for path in plan.media_paths],
                        "subtitle_cues": len(plan.subtitle_cues),
                        "scene_path": str(plan.output_path),
                        "zoom_effect": scene.zoom_effect,
                    }
                )
                progress.advance(task)

        log_success(f"Rendered {len(self._scene_paths)} scene file(s)")

    def _build_scene_plan(self, scene: Scene) -> ScenePlan:
        """Assemble everything the editor needs for one scene.

        Args:
            scene: The scene to plan.

        Returns:
            A fully resolved :class:`ScenePlan`.
        """
        result = self._tts_results[scene.id]
        return ScenePlan(
            scene=scene,
            audio_path=result.audio_path,
            audio_duration=result.duration,
            media_paths=self._scene_media[scene.id],
            subtitle_cues=self._scene_cues.get(scene.id, []),
            target_resolution=self._scenario.video.resolution,
            fps=self._scenario.video.fps,
            scene_gap_seconds=self._scenario.video.scene_gap_seconds,
            subtitles=self._scenario.subtitles,
            font_path=self._font_path,
            output_path=self._settings.scenes_dir() / f"scene_{scene.id:03d}.mp4",
            credits=list(self._credits),
        )

    def _stage_assemble(self) -> Path:
        """Concatenate the scenes into the finished video.

        Returns:
            Path to the final MP4.

        Raises:
            RenderError: If assembly fails.
        """
        log_step(5, TOTAL_STAGES, "Final assembly")
        out_path = self._final_video_path()

        with _StageTimer(self._manifest, "assemble"):
            final = self._editor.assemble(self._scene_paths, self._scenario, out_path)

        size = final.stat().st_size if final.is_file() else 0
        self._manifest.artifacts["video"] = str(final)
        self._manifest.video_size_bytes = size
        self._manifest.video_duration_seconds = sum(
            self._tts_results[scene.id].duration + self._scenario.video.scene_gap_seconds
            for scene in self._selected_scenes()
        )
        log_success(f"Final video: {final.name} ({format_bytes(size)})")
        return final

    def _stage_thumbnail(self, video_path: Path) -> Path | None:
        """Generate the thumbnail.

        A thumbnail failure is downgraded to a warning: the video itself is finished, and
        YouTube will auto-generate one.

        Args:
            video_path: The finished video.

        Returns:
            Path to the thumbnail, or ``None`` when disabled or generation failed.
        """
        log_step(6, TOTAL_STAGES, "Thumbnail")

        if not self._scenario.youtube.thumbnail_enabled:
            log_info("Thumbnails are disabled in the scenario; skipping.")
            return None

        out_path = self._settings.thumbnails_dir() / f"{self._scenario.project_id}.jpg"
        try:
            with _StageTimer(self._manifest, "thumbnail"):
                thumbnail = None
                if self._scenario.video.is_zenn:
                    hook = self._scenario.youtube.thumbnail_hook.strip()
                    if hook:
                        try:
                            thumbnail = build_zenn_thumbnail(
                                hook,
                                out_path,
                                font_path=self._font_path,
                            )
                        except RenderError as exc:
                            log_warn(
                                f"Zenn thumbnail template failed ({exc.message}); "
                                "falling back to a video frame."
                            )
                elif self._scenario.video.is_paint:
                    source = find_paint_thumbnail(self._paint_search_roots())
                    if source is not None:
                        try:
                            thumbnail = prepare_youtube_thumbnail(source, out_path)
                        except RenderError as exc:
                            log_warn(
                                f"Paint cover {source.name} could not be used ({exc.message}); "
                                "falling back to a video frame."
                            )
                if thumbnail is None:
                    thumbnail = self._thumbnails.build(
                        video_path, self._scenario.youtube.title, out_path
                    )
        except RenderError as exc:
            log_warn(f"Thumbnail generation failed, continuing without one: {exc.message}")
            return None

        self._manifest.artifacts["thumbnail"] = str(thumbnail)
        log_success(f"Thumbnail: {thumbnail.name}")
        return thumbnail

    def _stage_studio_pack(self, video_path: Path, thumbnail: Path | None) -> None:
        """Write a copy-paste YouTube Studio file for manual upload."""
        scenes = self._selected_scenes()
        durations = [self._tts_results[scene.id].duration for scene in scenes]
        out_dir = self._settings.studio_dir() / self._scenario.project_id
        try:
            path = write_studio_pack(
                self._scenario.model_copy(update={"scenes": scenes}),
                video_path=video_path,
                thumbnail_path=thumbnail,
                srt_path=self._srt_path,
                durations=durations,
                out_dir=out_dir,
            )
        except (OSError, ValueError) as exc:
            log_warn(f"Could not write the Studio pack: {exc}")
            return
        self._manifest.artifacts["studio"] = str(path)
        log_success(f"Studio pack: {path}")

    def _stage_upload(self, video_path: Path, thumbnail: Path | None) -> None:
        """Publish the video when uploading is enabled and permitted.

        Args:
            video_path: The finished video.
            thumbnail: Optional thumbnail to attach.
        """
        log_step(7, TOTAL_STAGES, "Upload")

        uploader = self._uploader
        if uploader is None or not self._should_upload():
            return

        with _StageTimer(self._manifest, "upload"):
            uploader.authenticate()
            result = uploader.upload(video_path, self._scenario.youtube, thumbnail)

        self._record_upload(result)
        log_success(f"Published: {result.url}")

    def _should_upload(self) -> bool:
        """Decide whether the upload stage should run.

        Returns:
            ``True`` when uploading is enabled, an uploader is wired, and the user has
            confirmed any public upload.
        """
        if self._options.no_upload:
            log_info("Upload skipped (--no-upload).")
            return False
        if not self._scenario.youtube.upload_enabled:
            log_info("Upload skipped (youtube.upload_enabled is false).")
            return False
        if self._uploader is None:
            log_warn("Upload requested but no uploader is configured; skipping.")
            return False
        if self._scenario.youtube.privacy_status == "public" and not self._options.assume_yes:
            log_warn("A public upload was requested without confirmation; skipping.")
            log_info("Re-run with --yes to publish publicly.")
            return False
        return True

    def _record_upload(self, result: UploadResult) -> None:
        """Store upload results in the manifest.

        Args:
            result: The uploader's result.
        """
        self._manifest.youtube_video_id = result.video_id
        self._manifest.youtube_url = result.url
        self._manifest.youtube_privacy_status = result.privacy_status

    # ----------------------------------------------------------------------------------
    # Manifest and reporting
    # ----------------------------------------------------------------------------------

    def _write_manifest(self) -> None:
        """Write the run manifest, even when the run failed.

        Manifest write failures are logged rather than raised, so they cannot mask the error
        that actually stopped the run.
        """
        log_step(TOTAL_STAGES, TOTAL_STAGES, "Manifest")

        self._manifest.credits = [
            {
                "provider": credit.provider,
                "author_name": credit.author_name,
                "author_url": credit.author_url,
                "page_url": credit.page_url,
            }
            for credit in self._unique_credits()
        ]

        path = self._settings.final_dir() / f"{self._scenario.project_id}_manifest.json"
        try:
            self._settings.final_dir().mkdir(parents=True, exist_ok=True)
            write_json(path, self._manifest.to_dict())
            self._manifest.artifacts["manifest"] = str(path)
            log_info(f"Manifest written to {path.name}")
        except OSError as exc:
            logger.error("Could not write the run manifest: %s", exc)

    def _record_failure(self, exc: BaseException) -> None:
        """Capture a failure into the manifest.

        Args:
            exc: The exception that stopped the run.
        """
        self._manifest.status = "failed"
        self._manifest.failed_stage = self._current_stage()
        self._manifest.error = str(exc)
        frames = traceback.format_exception(type(exc), exc, exc.__traceback__)
        self._manifest.traceback_digest = "".join(frames[-3:]).strip()

    def _current_stage(self) -> str:
        """Identify which stage was running when the failure occurred.

        Returns:
            The stage the timer marked as active, falling back to the first stage with no
            recorded timing for failures that happened outside a timed block.
        """
        if self._manifest.active_stage is not None:
            return self._manifest.active_stage

        order = ["narration", "subtitles", "footage", "scenes", "assemble", "thumbnail", "upload"]
        completed = set(self._manifest.stage_timings)
        for stage in order:
            if stage not in completed:
                return stage
        return "manifest"

    def _report_summary(self) -> None:
        """Print the end-of-run summary table."""
        rows = [
            ("Project", self._scenario.project_id),
            ("Scenes", str(len(self._scene_paths))),
            ("Resolution", f"{self._manifest.resolution[0]}x{self._manifest.resolution[1]}"),
            ("Frame rate", f"{self._manifest.fps} fps"),
            ("Duration", human_duration(self._manifest.video_duration_seconds)),
            ("File size", format_bytes(self._manifest.video_size_bytes)),
            ("Voice", self._manifest.voice),
            ("Wall time", human_duration(self._manifest.duration_seconds)),
        ]
        if self._manifest.youtube_url:
            rows.append(("YouTube", self._manifest.youtube_url))
            rows.append(("Privacy", self._manifest.youtube_privacy_status or "unknown"))

        log_blank()
        log_renderable(summary_table("Run summary", rows))

        for name, seconds in self._manifest.stage_timings.items():
            log_metric(name, f"{seconds:.1f}s")
        log_blank()

    # ----------------------------------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------------------------------

    def _selected_scenes(self) -> list[Scene]:
        """Return the scenes this run will process.

        Returns:
            All scenes, or the first ``scene_limit`` when one was set.
        """
        scenes = list(self._scenario.scenes)
        if self._scene_keep is not None:
            scenes = scenes[: max(1, self._scene_keep)]
        if self._options.scene_limit is None:
            return scenes
        return scenes[: max(1, self._options.scene_limit)]

    def _final_video_path(self) -> Path:
        """Return the destination path for the finished video."""
        return self._settings.final_dir() / f"{self._scenario.project_id}.mp4"

    def _unique_credits(self) -> list[MediaCredit]:
        """Deduplicate attribution records by contributor.

        Returns:
            One credit per contributor, in first-seen order.
        """
        seen: set[tuple[str, str]] = set()
        unique: list[MediaCredit] = []
        for credit in self._credits:
            key = credit.key()
            if key not in seen:
                seen.add(key)
                unique.append(credit)
        return unique

    @property
    def credits(self) -> list[MediaCredit]:
        """Attribution records collected so far."""
        return self._unique_credits()

    @property
    def subtitle_path(self) -> Path | None:
        """The whole-video SRT sidecar, once written."""
        return self._srt_path

    @property
    def manifest(self) -> RunManifest:
        """The run manifest."""
        return self._manifest

    def _describe_subtitles(self) -> str:
        """Describe the subtitle configuration for the plan table."""
        settings = self._scenario.subtitles
        if not settings.enabled:
            return "disabled"
        mode = "burned in" if settings.burn_in else "sidecar only"
        return f"{mode}, {settings.max_chars_per_line} chars x {settings.max_lines} lines"

    def _describe_music(self) -> str:
        """Describe the background music configuration for the plan table."""
        music = self._scenario.video.background_music
        if not music.enabled:
            return "disabled"
        return f"{music.file} at {music.volume:.2f} gain, ducking to {music.duck_to:.2f}"

    def _describe_upload(self) -> str:
        """Describe the upload configuration for the plan table."""
        if self._options.no_upload:
            return "disabled (--no-upload)"
        if not self._scenario.youtube.upload_enabled:
            return "disabled (upload_enabled is false)"
        return f"enabled, privacy '{self._scenario.youtube.privacy_status}'"
