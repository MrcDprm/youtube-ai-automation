"""Command-line entry point.

This file holds no business logic. It parses arguments, builds the concrete implementations,
injects them into :class:`~modules.pipeline.VideoPipeline`, and translates exceptions into
process exit codes. The composition root in :func:`_build_pipeline` is the single place that
knows which concrete classes exist, which is what keeps the orchestrator swappable.

Exit codes: 0 success, 1 configuration, 2 validation, 3 speech synthesis, 4 stock media,
5 rendering, 6 upload, 130 interrupted.
"""

from __future__ import annotations

import asyncio
import sys
from datetime import date
from pathlib import Path
from typing import Annotated, cast

import typer
from rich.markup import escape
from rich.table import Table

from config.constants import (
    DEFAULT_PAINT_TOPICS_FILE,
    ORIENTATION_RESOLUTIONS,
    PAINT_DEFAULT_MINUTES,
    PROJECT_ROOT,
    SCRIPT_DEFAULT_SCENES,
    SCRIPT_MAX_SCENES,
    SCRIPT_MIN_SCENES,
    STORY_DEFAULT_MINUTES,
    STORY_MAX_MINUTES,
    STORY_MIN_MINUTES,
    VALID_VIDEO_FORMATS,
    VIDEO_FORMAT_PAINT,
    VIDEO_FORMAT_STORY,
    ExitCode,
)
from config.settings import Settings, get_settings
from models.scenario import Orientation, Scenario
from modules.editor import MoviePyEditor
from modules.interfaces import IMediaProvider, IUploader, MediaCandidate
from modules.media_cache import MediaCache
from modules.paint_generator import OllamaPaintGenerator
from modules.photo_fetcher import PexelsPhotoProvider, PixabayPhotoProvider
from modules.pipeline import PipelineOptions, VideoPipeline
from modules.queue import (
    DailyLock,
    ScenarioQueue,
    SchedulerState,
    Topic,
    decide_daily_action,
    default_scene_count,
    load_state,
    load_topics,
    save_state,
)
from modules.scenario_builder import (
    build_paint_scenario,
    build_scenario,
    build_story_scenario,
    write_scenario,
)
from modules.scenario_loader import describe_scenario, load_scenario
from modules.scheduler import query_task, register_daily_task, unregister_daily_task
from modules.script_generator import OllamaScriptGenerator
from modules.story_generator import OllamaStoryGenerator
from modules.subtitle import SrtSubtitleBuilder
from modules.thumbnail import PillowThumbnailBuilder
from modules.tts import EdgeTTSEngine
from modules.uploader import YouTubeUploader
from modules.video_fetcher import (
    CompositeMediaProvider,
    PexelsVideoProvider,
    PixabayVideoProvider,
)
from utils.exceptions import ConfigurationError, MediaProviderError, PipelineError, SchedulerError
from utils.fs import clear_directory, download_default_font, format_bytes, resolve_font
from utils.logger import (
    console,
    log_error,
    log_info,
    log_metric,
    log_step,
    log_success,
    log_warn,
    register_secret,
    setup_logging,
    summary_table,
    table_box,
)
from utils.preflight import CheckResult, run_all_checks

app = typer.Typer(
    name="youtube-automation",
    help="Zero-cost, fully local automated video production pipeline.",
    add_completion=False,
    no_args_is_help=True,
)

DEFAULT_SCENARIO = Path("senaryo.json")
ORIENTATION_CHOICES = frozenset(ORIENTATION_RESOLUTIONS)


# --------------------------------------------------------------------------------------
# Shared helpers
# --------------------------------------------------------------------------------------


def _load_settings() -> Settings:
    """Load runtime settings and register secrets with the log redactor.

    Returns:
        The loaded settings.

    Raises:
        ConfigurationError: If the environment cannot be parsed.
    """
    settings = get_settings()
    for secret in settings.secret_values():
        register_secret(secret)
    return settings


def _resolve_scenario_path(scenario: Path) -> Path:
    """Resolve a scenario path against the project root when relative.

    Args:
        scenario: The path given on the command line.

    Returns:
        An absolute path.
    """
    return scenario if scenario.is_absolute() else (PROJECT_ROOT / scenario)


def _fail(exc: PipelineError) -> None:
    """Report a pipeline error and exit with its designated code.

    Args:
        exc: The error to report.

    Raises:
        typer.Exit: Always, carrying the exception's exit code.
    """
    log_error(exc.message)
    if exc.hint:
        console.print(f"  [warn]Hint:[/warn] {escape(exc.hint)}")
    raise typer.Exit(code=int(exc.exit_code))


class _DryRunMediaProvider(IMediaProvider):
    """Stand-in provider used during dry runs.

    A dry run stops before the footage stage, but the pipeline's constructor still requires an
    :class:`~modules.interfaces.IMediaProvider`. This satisfies the contract without needing an
    API key, and fails loudly if a future change ever reaches it.
    """

    @property
    def name(self) -> str:
        """The provider's short name."""
        return "dry-run"

    def search(
        self, query: str, orientation: str, min_duration: float, limit: int
    ) -> list[MediaCandidate]:
        """Refuse to search, since a dry run must not touch the network.

        Raises:
            MediaProviderError: Always.
        """
        raise MediaProviderError("A dry run must not search for stock footage.")

    def download(self, candidate: MediaCandidate, dest: Path) -> Path:
        """Refuse to download, since a dry run must not touch the network.

        Raises:
            MediaProviderError: Always.
        """
        raise MediaProviderError("A dry run must not download stock footage.")


class _UnusedMediaProvider(IMediaProvider):
    """Stand-in when a paint project never searches stock libraries."""

    @property
    def name(self) -> str:
        return "local-paint"

    def search(
        self, query: str, orientation: str, min_duration: float, limit: int
    ) -> list[MediaCandidate]:
        del query, orientation, min_duration, limit
        return []

    def download(self, candidate: MediaCandidate, dest: Path) -> Path:
        del candidate, dest
        raise MediaProviderError("Paint format does not download stock media.")


def _build_media_provider(settings: Settings, scenario: Scenario, force: bool) -> IMediaProvider:
    """Construct the stock footage provider chain.

    Pexels is preferred and Pixabay is added as a fallback whenever its key is present. If a
    scenario sources every scene from ``local_media``, no key is required at all.

    Args:
        settings: Runtime settings holding the API keys.
        scenario: The project, for the target resolution.
        force: Whether to bypass the download cache.

    Returns:
        A provider implementing :class:`~modules.interfaces.IMediaProvider`.

    Raises:
        ConfigurationError: If footage is needed but no provider key is configured.
    """
    if scenario.video.is_paint:
        return _UnusedMediaProvider()

    cache = MediaCache(
        settings.media_cache_dir(),
        timeout=settings.HTTP_TIMEOUT,
        max_attempts=settings.MAX_RETRIES,
        force=force,
    )

    providers: list[IMediaProvider] = []
    use_photos = scenario.video.is_story
    if settings.PEXELS_API_KEY.strip():
        if use_photos:
            providers.append(
                PexelsPhotoProvider(
                    settings.PEXELS_API_KEY,
                    cache,
                    timeout=settings.HTTP_TIMEOUT,
                    max_attempts=settings.MAX_RETRIES,
                )
            )
        else:
            providers.append(
                PexelsVideoProvider(
                    settings.PEXELS_API_KEY,
                    cache,
                    timeout=settings.HTTP_TIMEOUT,
                    max_attempts=settings.MAX_RETRIES,
                )
            )
    if settings.PIXABAY_API_KEY.strip():
        if use_photos:
            providers.append(
                PixabayPhotoProvider(
                    settings.PIXABAY_API_KEY,
                    cache,
                    timeout=settings.HTTP_TIMEOUT,
                    max_attempts=settings.MAX_RETRIES,
                )
            )
        else:
            providers.append(
                PixabayVideoProvider(
                    settings.PIXABAY_API_KEY,
                    cache,
                    timeout=settings.HTTP_TIMEOUT,
                    max_attempts=settings.MAX_RETRIES,
                )
            )

    if not providers:
        needs_stock = any(scene.local_media is None for scene in scenario.scenes)
        if needs_stock:
            raise ConfigurationError(
                "No stock footage provider is configured, but some scenes need one.",
                hint=(
                    "Set PEXELS_API_KEY in .env (free at https://www.pexels.com/api/), or give "
                    "every scene a local_media path."
                ),
            )

    return CompositeMediaProvider(
        providers,
        target_resolution=scenario.video.resolution,
    )


def _build_uploader(settings: Settings, scenario: Scenario, srt_path: Path | None) -> IUploader:
    """Construct the YouTube uploader.

    Args:
        settings: Runtime settings holding the credential paths.
        scenario: The project, used to decide whether captions should be attached.
        srt_path: The subtitle sidecar, attached only when captions are not burned in.

    Returns:
        An uploader implementing :class:`~modules.interfaces.IUploader`.
    """
    attach_captions = (
        scenario.subtitles.enabled and not scenario.subtitles.burn_in and srt_path is not None
    )
    return YouTubeUploader(
        settings.client_secrets_path,
        settings.token_path,
        caption_file=srt_path if attach_captions else None,
    )


def _build_pipeline(
    scenario: Scenario,
    settings: Settings,
    options: PipelineOptions,
) -> VideoPipeline:
    """Compose the pipeline from concrete implementations.

    This is the only function in the project that names every concrete class. Swapping a
    provider or engine means editing this function alone.

    Args:
        scenario: The validated project.
        settings: Runtime settings.
        options: Per-run switches.

    Returns:
        A wired :class:`~modules.pipeline.VideoPipeline`.
    """
    font_path: Path | None = None
    if scenario.subtitles.enabled and scenario.subtitles.burn_in:
        font_path, _ = resolve_font(settings.font_path, fonts_dir=settings.fonts_dir)

    srt_path = settings.subtitles_dir() / f"{scenario.project_id}.srt"

    uploader: IUploader | None = None
    if scenario.youtube.upload_enabled and not options.no_upload and not options.dry_run:
        uploader = _build_uploader(settings, scenario, srt_path)

    media_provider: IMediaProvider = (
        _DryRunMediaProvider()
        if options.dry_run
        else _build_media_provider(settings, scenario, options.force)
    )

    return VideoPipeline(
        scenario=scenario,
        settings=settings,
        tts_engine=EdgeTTSEngine(
            settings.tts_cache_dir(),
            max_attempts=settings.MAX_RETRIES,
            force=options.force,
        ),
        media_provider=media_provider,
        subtitle_builder=SrtSubtitleBuilder(),
        video_editor=MoviePyEditor(
            temp_dir=settings.temp_dir(),
            threads=settings.FFMPEG_THREADS,
            crf=scenario.video.video_bitrate_crf,
            preset=scenario.video.preset,
            force=options.force,
        ),
        thumbnail_builder=PillowThumbnailBuilder(font_path),
        uploader=uploader,
        options=options,
    )


def _execute_run(
    parsed: Scenario,
    settings: Settings,
    options: PipelineOptions,
    *,
    verbose: bool = False,
) -> None:
    """Run the pipeline for an already-loaded scenario.

    Shared by ``run`` and ``daily`` so the daily command cannot drift from the interactive one.

    Args:
        parsed: Validated scenario.
        settings: Runtime settings.
        options: Per-run switches.
        verbose: Console DEBUG logging.

    Raises:
        PipelineError: Propagated from composition or the pipeline itself.
        typer.Exit: On interrupt, matching ``run``.
    """
    log_path = setup_logging(
        level=settings.LOG_LEVEL,
        log_dir=settings.logs_dir(),
        project_id=parsed.project_id,
        secrets=settings.secret_values(),
        verbose=verbose,
    )
    pipeline = _build_pipeline(parsed, settings, options)
    try:
        pipeline.run()
    except PipelineError:
        if log_path is not None:
            log_info(f"Full log: {log_path}")
        raise
    except KeyboardInterrupt:
        log_warn("Interrupted. Completed work is cached; re-run to resume.")
        raise typer.Exit(code=int(ExitCode.INTERRUPTED)) from None

    if not options.keep_temp and not options.dry_run:
        clear_directory(settings.temp_dir())
    if log_path is not None:
        log_metric("log file", str(log_path))


def _with_upload(scenario: Scenario, enabled: bool) -> Scenario:
    """Return a copy whose YouTube upload flag matches ``enabled``.

    Args:
        scenario: The loaded scenario.
        enabled: Whether the pipeline should upload.

    Returns:
        The original object when the flag already matches, otherwise a copy.
    """
    if scenario.youtube.upload_enabled is enabled:
        return scenario
    youtube = scenario.youtube.model_copy(update={"upload_enabled": enabled})
    return scenario.model_copy(update={"youtube": youtube})


# --------------------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------------------


@app.command()
def doctor(
    fix: Annotated[
        bool,
        typer.Option("--fix", help="Download a default font if none is installed."),
    ] = False,
) -> None:
    """Run preflight checks and report each one individually."""
    try:
        settings = _load_settings()
    except ConfigurationError as exc:
        _fail(exc)
        return

    setup_logging(level=settings.LOG_LEVEL, secrets=settings.secret_values())

    if fix:
        _download_font(settings)

    results = run_all_checks(settings)
    _render_check_table(results)

    failures = [result for result in results if not result.passed and result.fatal]
    warnings = [result for result in results if not result.passed and not result.fatal]

    for result in failures + warnings:
        if result.hint:
            console.print(f"  [warn]{escape(result.name)}:[/warn] {escape(result.hint)}")

    console.print()
    if failures:
        log_error(f"{len(failures)} check(s) failed.")
        raise typer.Exit(code=int(ExitCode.CONFIG))
    if warnings:
        log_warn(f"All required checks passed, with {len(warnings)} warning(s).")
    else:
        log_success("All checks passed.")


def _download_font(settings: Settings) -> None:
    """Fetch a default font when the project font directory is empty.

    Args:
        settings: Runtime settings holding the font directory.
    """
    from utils.fs import available_fonts

    if available_fonts(settings.fonts_dir):
        log_info("A font is already installed; skipping the download.")
        return

    log_info("Downloading a default font (SIL Open Font License)...")
    try:
        path, source = download_default_font(settings.fonts_dir)
    except PipelineError as exc:
        log_warn(f"Could not download a font: {exc.message}")
        return
    log_success(f"Installed {path.name} - {source}")


def _render_check_table(results: list[CheckResult]) -> None:
    """Print preflight results as a table.

    Args:
        results: The checks to render.
    """
    table = Table(
        title="Preflight checks",
        title_style="step",
        header_style="step",
        box=table_box(),
    )
    table.add_column("Status", no_wrap=True)
    table.add_column("Check", style="metric", no_wrap=True)
    table.add_column("Detail", overflow="fold")

    styles = {
        "OK": "[success]OK[/success]",
        "WARN": "[warn]WARN[/warn]",
        "FAIL": "[failure]FAIL[/failure]",
    }
    for result in results:
        table.add_row(styles[result.status], escape(result.name), escape(result.detail))

    console.print()
    console.print(table)


@app.command()
def voices(
    locale: Annotated[
        str | None,
        typer.Option("--locale", help="Filter by locale, for example tr-TR or en."),
    ] = None,
) -> None:
    """List the voices available from edge-tts."""
    try:
        settings = _load_settings()
    except ConfigurationError as exc:
        _fail(exc)
        return

    setup_logging(level=settings.LOG_LEVEL, secrets=settings.secret_values())
    engine = EdgeTTSEngine(settings.tts_cache_dir())

    try:
        found = asyncio.run(engine.list_voices(locale))
    except PipelineError as exc:
        _fail(exc)
        return

    if not found:
        log_warn(f"No voices matched {locale!r}.")
        raise typer.Exit(code=int(ExitCode.OK))

    table = Table(
        title=f"edge-tts voices ({len(found)})",
        title_style="step",
        header_style="step",
        box=table_box(),
    )
    table.add_column("Short name", style="metric", no_wrap=True)
    table.add_column("Gender", no_wrap=True)
    table.add_column("Locale", no_wrap=True)
    table.add_column("Personality", overflow="fold")

    for voice in found:
        tag = voice.get("VoiceTag") or {}
        personalities = tag.get("VoicePersonalities") if isinstance(tag, dict) else None
        table.add_row(
            escape(str(voice.get("ShortName", ""))),
            escape(str(voice.get("Gender", ""))),
            escape(str(voice.get("Locale", ""))),
            escape(", ".join(personalities)) if personalities else "",
        )

    console.print()
    console.print(table)
    console.print()


@app.command()
def auth() -> None:
    """Run the one-time YouTube OAuth consent flow."""
    try:
        settings = _load_settings()
    except ConfigurationError as exc:
        _fail(exc)
        return

    setup_logging(level=settings.LOG_LEVEL, secrets=settings.secret_values())

    uploader = YouTubeUploader(settings.client_secrets_path, settings.token_path)
    try:
        uploader.authenticate()
    except PipelineError as exc:
        _fail(exc)
        return

    log_success(f"Authorized. Token saved to {settings.token_path}")
    log_info(
        "While the OAuth consent screen is in Testing, this token expires after 7 days and "
        "uploads stay private until the app is verified."
    )


@app.command()
def validate(
    scenario: Annotated[
        Path,
        typer.Option("--scenario", "-s", help="Path to the scenario JSON file."),
    ] = DEFAULT_SCENARIO,
) -> None:
    """Validate a scenario file against the schema."""
    try:
        _load_settings()
    except ConfigurationError as exc:
        _fail(exc)
        return

    path = _resolve_scenario_path(scenario)
    try:
        parsed = load_scenario(path)
    except PipelineError as exc:
        _fail(exc)
        return

    describe_scenario(parsed)

    rows = [
        ("Project", parsed.project_id),
        ("Scenes", str(parsed.total_scenes)),
        ("Resolution", f"{parsed.video.width}x{parsed.video.height}"),
        ("Frame rate", f"{parsed.video.fps} fps"),
        ("Estimated length", f"{parsed.estimated_narration_seconds():.0f}s"),
        ("Voice", parsed.tts.voice),
        ("Title", parsed.youtube.title),
        ("Upload", "enabled" if parsed.youtube.upload_enabled else "disabled"),
        ("Privacy", parsed.youtube.privacy_status),
    ]
    console.print()
    console.print(summary_table(f"{path.name}", rows))
    console.print()


@app.command()
def generate(
    topic: Annotated[str, typer.Argument(help="What the video should be about.")],
    scenes: Annotated[
        int | None,
        typer.Option("--scenes", "-n", min=SCRIPT_MIN_SCENES, max=SCRIPT_MAX_SCENES),
    ] = None,
    out: Annotated[
        Path | None,
        typer.Option("--out", "-o", help="Where to write the scenario. Defaults to senaryo.json."),
    ] = None,
    video_format: Annotated[
        str,
        typer.Option(
            "--format",
            help="shorts (default), story (photo narrative), or paint (Badly Drawn Why).",
        ),
    ] = "shorts",
    minutes: Annotated[
        int | None,
        typer.Option(
            "--minutes",
            min=STORY_MIN_MINUTES,
            max=STORY_MAX_MINUTES,
            help="Longform runtime in minutes. Ignored for Shorts. Story default 15, paint 11.",
        ),
    ] = None,
    orientation: Annotated[
        str | None,
        typer.Option(
            "--orientation",
            help="portrait, landscape or square. Story and paint default to landscape.",
        ),
    ] = None,
    language: Annotated[
        str | None,
        typer.Option("--language", help="Narration language code. Paint defaults to en."),
    ] = None,
    voice: Annotated[
        str | None, typer.Option("--voice", help="Override the edge-tts voice.")
    ] = None,
    model: Annotated[
        str | None, typer.Option("--model", help="Override OLLAMA_MODEL for this run.")
    ] = None,
    guidance: Annotated[
        str | None, typer.Option("--guidance", help="Extra direction, e.g. a tone or angle.")
    ] = None,
    no_burn_in: Annotated[
        bool, typer.Option("--no-burn-in", help="Write an SRT sidecar instead of burning in.")
    ] = False,
    overwrite: Annotated[
        bool, typer.Option("--overwrite", help="Replace the output file if it already exists.")
    ] = False,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Log at DEBUG level on the console.")
    ] = False,
) -> None:
    """Draft a scenario from a topic using a local Ollama model.

    Renders nothing and uploads nothing: it only writes a scenario file for you to review and
    then feed to ``run``. Uploading stays disabled in the generated file on purpose.
    """
    try:
        settings = _load_settings()
    except ConfigurationError as exc:
        _fail(exc)
        return

    fmt = video_format.strip().lower()
    if fmt not in VALID_VIDEO_FORMATS:
        _fail(
            ConfigurationError(
                f"Unknown format {video_format!r}.",
                hint=f"Choose one of: {', '.join(sorted(VALID_VIDEO_FORMATS))}.",
            )
        )
        return

    resolved_orientation = orientation or (
        "landscape" if fmt in {VIDEO_FORMAT_STORY, VIDEO_FORMAT_PAINT} else "portrait"
    )
    if resolved_orientation not in ORIENTATION_CHOICES:
        _fail(
            ConfigurationError(
                f"Unknown orientation {resolved_orientation!r}.",
                hint=f"Choose one of: {', '.join(sorted(ORIENTATION_CHOICES))}.",
            )
        )
        return

    resolved_language = language or ("en" if fmt == VIDEO_FORMAT_PAINT else "tr")
    chapter_count = scenes
    if chapter_count is None:
        chapter_count = SCRIPT_DEFAULT_SCENES
    if fmt == VIDEO_FORMAT_PAINT:
        story_minutes = minutes if minutes is not None else PAINT_DEFAULT_MINUTES
    else:
        story_minutes = minutes if minutes is not None else STORY_DEFAULT_MINUTES
    target_seconds = float(story_minutes * 60)

    destination = (out or DEFAULT_SCENARIO).expanduser()
    if not destination.is_absolute():
        destination = PROJECT_ROOT / destination
    if destination.exists() and not overwrite:
        _fail(
            ConfigurationError(
                f"{destination} already exists.",
                hint="Pass --overwrite to replace it, or choose another path with --out.",
            )
        )
        return

    setup_logging(
        level=settings.LOG_LEVEL,
        log_dir=settings.logs_dir(),
        project_id="generate",
        secrets=settings.secret_values(),
        verbose=verbose,
    )

    generator = OllamaScriptGenerator(
        settings.OLLAMA_HOST,
        model or settings.OLLAMA_MODEL,
        timeout=settings.OLLAMA_TIMEOUT,
    )

    kind = "chapter(s)" if fmt in {VIDEO_FORMAT_STORY, VIDEO_FORMAT_PAINT} else "scene(s)"
    if fmt == VIDEO_FORMAT_PAINT:
        log_step(1, 2, f"Drafting a {story_minutes}-minute Badly Drawn Why essay on '{topic}'")
    elif fmt == VIDEO_FORMAT_STORY:
        log_step(1, 2, f"Drafting a {story_minutes}-minute story on '{topic}'")
    else:
        log_step(1, 2, f"Drafting {chapter_count} {kind} on '{topic}'")
    try:
        if fmt == VIDEO_FORMAT_PAINT:
            if scenes is not None:
                log_warn("Paint generate ignores --scenes/-n; use --minutes for length.")
            draft = OllamaPaintGenerator(generator).generate(
                topic,
                target_seconds=target_seconds,
                language=resolved_language,
                extra_guidance=guidance,
            )
        elif fmt == VIDEO_FORMAT_STORY:
            if scenes is not None:
                log_warn("Story generate ignores --scenes/-n; use --minutes for length.")
            draft = OllamaStoryGenerator(generator).generate(
                topic,
                target_seconds=target_seconds,
                language=resolved_language,
                extra_guidance=guidance,
            )
        else:
            draft = generator.generate(
                topic,
                scene_count=chapter_count,
                language=resolved_language,
                extra_guidance=guidance,
            )
    except PipelineError as exc:
        _fail(exc)
        return

    log_step(2, 2, "Assembling the scenario")
    try:
        if fmt == VIDEO_FORMAT_PAINT:
            scenario = build_paint_scenario(
                draft,
                topic=topic,
                orientation=cast(Orientation, resolved_orientation),
                voice=voice,
                language=resolved_language,
                burn_in=not no_burn_in,
                target_seconds=target_seconds,
                minutes=story_minutes,
            )
        elif fmt == VIDEO_FORMAT_STORY:
            scenario = build_story_scenario(
                draft,
                topic=topic,
                orientation=cast(Orientation, resolved_orientation),
                voice=voice,
                language=resolved_language,
                burn_in=not no_burn_in,
                target_seconds=target_seconds,
                minutes=story_minutes,
            )
        else:
            scenario = build_scenario(
                draft,
                topic=topic,
                orientation=cast(Orientation, resolved_orientation),
                voice=voice,
                language=resolved_language,
                burn_in=not no_burn_in,
            )
        write_scenario(scenario, destination)
    except PipelineError as exc:
        _fail(exc)
        return

    log_success(f"Wrote {destination.name} with {scenario.total_scenes} scene(s)")

    rows = [
        ("Project", scenario.project_id),
        ("Title", scenario.youtube.title),
        ("Format", scenario.video.format),
        ("Scenes", str(scenario.total_scenes)),
        ("Beats", str(len(scenario.video.visual_beats)) if scenario.video.is_paint else "—"),
        ("Resolution", f"{scenario.video.width}x{scenario.video.height}"),
        ("Estimated length", f"{scenario.estimated_narration_seconds():.0f}s"),
        ("Voice", scenario.tts.voice),
        ("Tags", ", ".join(scenario.youtube.tags) or "none"),
        ("File", str(destination)),
    ]
    console.print()
    console.print(summary_table("Generated scenario", rows))
    console.print()
    log_info("Review the narration, then render it with:")
    if scenario.video.is_paint:
        log_info(
            f"Draw {len(scenario.video.visual_beats)} 16:9 MS Paint stills into "
            f"output/storyboard/{scenario.project_id}/ as NN-slug.png"
        )
        log_info(f"  python main.py run --scenario {destination.name} --no-upload")
        log_info("Then paste output/studio/<project>/STUDIO.txt into YouTube Studio.")
    else:
        log_info(f"  python main.py run --scenario {destination.name}")


@app.command()
def topics(
    paint: Annotated[
        bool,
        typer.Option("--paint", help="List the Badly Drawn Why English topic bank."),
    ] = False,
) -> None:
    """Print the topic bank used by daily production or the paint channel."""
    try:
        settings = _load_settings()
    except ConfigurationError as exc:
        _fail(exc)
        return

    from utils.fs import read_json

    path = settings.scenarios_dir() / DEFAULT_PAINT_TOPICS_FILE if paint else settings.topics_path()
    if not path.is_file():
        _fail(
            ConfigurationError(
                f"Topic file not found: {path}",
                hint="Add scenarios/topics.json or scenarios/topics-paint.json.",
            )
        )
        return
    payload = read_json(path)
    raw = payload.get("topics", payload) if isinstance(payload, dict) else payload
    if not isinstance(raw, list):
        _fail(ConfigurationError(f"{path.name} does not contain a topic list."))
        return
    table = Table(title=path.name, box=table_box())
    table.add_column("#", justify="right")
    table.add_column("Topic")
    for index, item in enumerate(raw, start=1):
        label = item["topic"] if isinstance(item, dict) else str(item)
        table.add_row(str(index), label)
    console.print(table)


@app.command()
def daily(
    force: Annotated[
        bool, typer.Option("--force", help="Produce even if a video was already made today.")
    ] = False,
    upload: Annotated[
        bool, typer.Option("--upload", help="Enable YouTube upload for this run.")
    ] = False,
    no_upload: Annotated[
        bool, typer.Option("--no-upload", help="Render but never upload, overriding DAILY_UPLOAD.")
    ] = False,
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Print the plan without generating or rendering.")
    ] = False,
    yes: Annotated[
        bool, typer.Option("--yes", "-y", help="Confirm a public upload without prompting.")
    ] = False,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Log at DEBUG level on the console.")
    ] = False,
) -> None:
    """Produce at most one video: inbox first, otherwise the next unused topic.

    Intended for Task Scheduler / cron. A missed day (PC off) produces one video when the
    command next runs, never a backlog burst.
    """
    try:
        settings = _load_settings()
    except ConfigurationError as exc:
        _fail(exc)
        return

    setup_logging(
        level=settings.LOG_LEVEL,
        log_dir=settings.logs_dir(),
        project_id="daily",
        secrets=settings.secret_values(),
        verbose=verbose,
    )

    do_upload = False if no_upload else (upload or settings.DAILY_UPLOAD)
    queue = ScenarioQueue(settings.scenarios_dir())
    queue.ensure()
    state_path = settings.scheduler_state_path()
    today = date.today()

    try:
        topics = load_topics(settings.topics_path()) if settings.topics_path().is_file() else []
    except PipelineError as exc:
        _fail(exc)
        return

    try:
        with DailyLock(state_path.parent):
            state = load_state(state_path)
            action = decide_daily_action(
                queue=queue, topics=topics, state=state, today=today, force=force
            )
            log_info(action.reason)

            if action.kind in {"skip", "idle"}:
                if not dry_run:
                    state.record(status="skipped", today=today, detail=action.reason)
                    save_state(state_path, state)
                raise typer.Exit(code=int(ExitCode.OK))

            if dry_run:
                log_success("Daily dry run. Nothing was generated or rendered.")
                raise typer.Exit(code=int(ExitCode.OK))

            if action.kind == "inbox" and action.inbox_path is not None:
                _daily_from_inbox(
                    action.inbox_path, queue, settings, state, state_path, today, do_upload, yes
                )
            elif action.kind == "generate" and action.topic is not None:
                _daily_from_topic(
                    action.topic, queue, settings, state, state_path, today, do_upload, yes
                )
            else:
                raise ConfigurationError(f"Daily action {action.kind!r} is missing its payload.")
    except typer.Exit:
        raise
    except PipelineError as exc:
        _fail(exc)


def _daily_from_inbox(
    inbox_path: Path,
    queue: ScenarioQueue,
    settings: Settings,
    state: SchedulerState,
    state_path: Path,
    today: date,
    do_upload: bool,
    yes: bool,
) -> None:
    """Claim an inbox scenario, render it, and record the outcome.

    Args:
        inbox_path: File in ``scenarios/inbox/``.
        queue: The folder queue.
        settings: Runtime settings.
        state: Persisted daily state.
        state_path: Where to write ``state``.
        today: Local calendar date.
        do_upload: Whether to enable upload for this run.
        yes: Skip the public-upload prompt.
    """
    claimed = queue.claim(inbox_path)
    log_step(1, 2, f"Inbox scenario {claimed.name}")
    parsed: Scenario | None = None
    try:
        parsed = _with_upload(load_scenario(claimed), do_upload)
        options = PipelineOptions(no_upload=not do_upload, assume_yes=yes)
        log_step(2, 2, "Render")
        _execute_run(parsed, settings, options)
    except PipelineError as exc:
        queue.complete(claimed, ok=False)
        state.record(
            status="failed",
            today=today,
            detail=exc.message,
            project_id=parsed.project_id if parsed is not None else claimed.stem,
        )
        save_state(state_path, state)
        raise
    queue.complete(claimed, ok=True)
    state.record(status="success", today=today, project_id=parsed.project_id, detail=claimed.name)
    save_state(state_path, state)
    log_success(f"Daily inbox job finished: {parsed.project_id}")


def _daily_from_topic(
    topic: Topic,
    queue: ScenarioQueue,
    settings: Settings,
    state: SchedulerState,
    state_path: Path,
    today: date,
    do_upload: bool,
    yes: bool,
) -> None:
    """Generate a scenario from a topic, render it, and record the outcome.

    Args:
        topic: The next unused topic.
        queue: The folder queue.
        settings: Runtime settings.
        state: Persisted daily state.
        state_path: Where to write ``state``.
        today: Local calendar date.
        do_upload: Whether the generated scenario should upload.
        yes: Skip the public-upload prompt.
    """
    orientation = settings.DAILY_ORIENTATION
    fmt = settings.VIDEO_FORMAT
    if fmt in {VIDEO_FORMAT_STORY, VIDEO_FORMAT_PAINT} and orientation == "portrait":
        orientation = "landscape"
    if orientation not in ORIENTATION_CHOICES:
        raise ConfigurationError(f"DAILY_ORIENTATION {orientation!r} is not valid.")

    language = topic.language or settings.DAILY_LANGUAGE
    if fmt == VIDEO_FORMAT_PAINT:
        if not topic.language and language == "tr":
            language = "en"
        story_minutes = PAINT_DEFAULT_MINUTES
        target_seconds = float(story_minutes * 60)
        log_step(1, 3, f"Drafting a {story_minutes}-minute paint essay on '{topic.topic}'")
    elif fmt == VIDEO_FORMAT_STORY:
        story_minutes = STORY_DEFAULT_MINUTES
        target_seconds = float(story_minutes * 60)
        log_step(1, 3, f"Drafting a {story_minutes}-minute story on '{topic.topic}'")
    else:
        scene_count = default_scene_count(topic, settings.DAILY_SCENES)
        log_step(1, 3, f"Drafting {scene_count} scene(s) on '{topic.topic}'")

    generator = OllamaScriptGenerator(
        settings.OLLAMA_HOST, settings.OLLAMA_MODEL, timeout=settings.OLLAMA_TIMEOUT
    )
    if fmt == VIDEO_FORMAT_PAINT:
        draft = OllamaPaintGenerator(generator).generate(
            topic.topic,
            target_seconds=target_seconds,
            language=language,
            extra_guidance=topic.guidance,
        )
        parsed = build_paint_scenario(
            draft,
            topic=topic.topic,
            orientation=cast(Orientation, orientation),
            language=language,
            upload_enabled=do_upload,
            target_seconds=target_seconds,
            minutes=story_minutes,
        )
    elif fmt == VIDEO_FORMAT_STORY:
        draft = OllamaStoryGenerator(generator).generate(
            topic.topic,
            target_seconds=target_seconds,
            language=language,
            extra_guidance=topic.guidance,
        )
        parsed = build_story_scenario(
            draft,
            topic=topic.topic,
            orientation=cast(Orientation, orientation),
            language=language,
            upload_enabled=do_upload,
            target_seconds=target_seconds,
            minutes=story_minutes,
        )
    else:
        draft = generator.generate(
            topic.topic,
            scene_count=scene_count,
            language=language,
            extra_guidance=topic.guidance,
        )
        parsed = build_scenario(
            draft,
            topic=topic.topic,
            orientation=cast(Orientation, orientation),
            language=language,
            upload_enabled=do_upload,
        )

    queue.ensure()
    destination = queue.processing / f"{parsed.project_id}.json"
    if destination.exists():
        destination = queue.processing / f"{parsed.project_id}-{today.isoformat()}.json"
    write_scenario(parsed, destination)
    log_step(2, 3, f"Wrote {destination.name}")

    try:
        log_step(3, 3, "Render")
        _execute_run(parsed, settings, PipelineOptions(no_upload=not do_upload, assume_yes=yes))
    except PipelineError as exc:
        queue.complete(destination, ok=False)
        state.record(
            status="failed",
            today=today,
            project_id=parsed.project_id,
            topic=topic.topic,
            detail=exc.message,
        )
        save_state(state_path, state)
        raise

    queue.complete(destination, ok=True)
    state.record(status="success", today=today, project_id=parsed.project_id, topic=topic.topic)
    save_state(state_path, state)
    log_success(f"Daily topic job finished: {parsed.project_id}")


@app.command()
def schedule(
    remove: Annotated[
        bool, typer.Option("--remove", help="Delete the daily scheduled task.")
    ] = False,
    status: Annotated[
        bool, typer.Option("--status", help="Show whether the daily task is registered.")
    ] = False,
    at: Annotated[str | None, typer.Option("--at", help="Daily time as HH:MM (24-hour).")] = None,
    upload: Annotated[
        bool, typer.Option("--upload", help="Scheduled runs pass --upload to daily.")
    ] = False,
) -> None:
    """Register, inspect or remove the OS task that runs ``daily`` once a day."""
    try:
        settings = _load_settings()
    except ConfigurationError as exc:
        _fail(exc)
        return

    setup_logging(level=settings.LOG_LEVEL, secrets=settings.secret_values())
    time_of_day = at or settings.DAILY_TIME
    do_upload = upload or settings.DAILY_UPLOAD

    try:
        if status:
            info = query_task(time_of_day=time_of_day, upload=do_upload)
            if info.registered:
                log_success("Daily task is registered.")
            else:
                log_warn("Daily task is not registered.")
            log_info(info.detail.splitlines()[0] if info.detail else "")
            log_metric("command", info.command)
            return
        if remove:
            log_success(unregister_daily_task())
            return
        log_success(register_daily_task(time_of_day=time_of_day, upload=do_upload))
        log_info("Missed triggers run when this PC is next available (StartWhenAvailable).")
        log_info("The machine must be on (or asleep with wake-timers enabled).")
        log_warn("Uploads stay off unless you pass --upload or set DAILY_UPLOAD=true.")
    except SchedulerError as exc:
        _fail(exc)


@app.command()
def run(
    scenario: Annotated[
        Path, typer.Option("--scenario", "-s", help="Path to the scenario JSON file.")
    ] = DEFAULT_SCENARIO,
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Print the plan without touching the network.")
    ] = False,
    no_upload: Annotated[
        bool, typer.Option("--no-upload", help="Render everything but never upload.")
    ] = False,
    force: Annotated[
        bool, typer.Option("--force", help="Ignore caches and redo every step.")
    ] = False,
    scene_limit: Annotated[
        int | None, typer.Option("--scene-limit", help="Render only the first N scenes.")
    ] = None,
    keep_temp: Annotated[
        bool, typer.Option("--keep-temp", help="Keep intermediate files for inspection.")
    ] = False,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Log at DEBUG level on the console.")
    ] = False,
    output_dir: Annotated[
        Path | None, typer.Option("--output-dir", help="Override the output directory.")
    ] = None,
    yes: Annotated[
        bool, typer.Option("--yes", "-y", help="Confirm a public upload without prompting.")
    ] = False,
) -> None:
    """Render a video from a scenario, and optionally publish it."""
    try:
        settings = _load_settings()
    except ConfigurationError as exc:
        _fail(exc)
        return

    if output_dir is not None:
        settings.OUTPUT_DIR = output_dir

    path = _resolve_scenario_path(scenario)

    try:
        parsed = load_scenario(path)
    except PipelineError as exc:
        _fail(exc)
        return

    confirmed = yes
    if (
        parsed.youtube.upload_enabled
        and parsed.youtube.privacy_status == "public"
        and not dry_run
        and not no_upload
        and not yes
    ):
        confirmed = typer.confirm(
            f"This will publish '{parsed.youtube.title}' PUBLICLY to YouTube. Continue?",
            default=False,
        )
        if not confirmed:
            log_warn("Public upload declined. Rendering will continue without uploading.")

    options = PipelineOptions(
        dry_run=dry_run,
        no_upload=no_upload,
        force=force,
        scene_limit=scene_limit,
        keep_temp=keep_temp,
        assume_yes=confirmed,
    )

    try:
        _execute_run(parsed, settings, options, verbose=verbose)
    except PipelineError as exc:
        _fail(exc)
        return


@app.command()
def clean(
    cache: Annotated[
        bool, typer.Option("--cache", help="Delete the download and TTS caches.")
    ] = False,
    output: Annotated[
        bool, typer.Option("--output", help="Delete generated output files.")
    ] = False,
    all_: Annotated[bool, typer.Option("--all", help="Delete both caches and output.")] = False,
) -> None:
    """Delete generated files and caches."""
    try:
        settings = _load_settings()
    except ConfigurationError as exc:
        _fail(exc)
        return

    setup_logging(level=settings.LOG_LEVEL, secrets=settings.secret_values())

    if not (cache or output or all_):
        log_warn("Nothing selected. Pass --cache, --output or --all.")
        raise typer.Exit(code=int(ExitCode.OK))

    removed = 0
    if cache or all_:
        freed = _directory_size(settings.cache_dir)
        removed += clear_directory(settings.cache_dir)
        log_success(f"Cleared the cache ({format_bytes(freed)} freed)")

    if output or all_:
        freed = _directory_size(settings.output_dir)
        removed += clear_directory(settings.output_dir)
        settings.ensure_directories()
        log_success(f"Cleared the output directory ({format_bytes(freed)} freed)")

    log_info(f"Removed {removed} entr{'y' if removed == 1 else 'ies'}.")


def _directory_size(directory: Path) -> int:
    """Sum the size of every file under a directory.

    Args:
        directory: Directory to measure.

    Returns:
        Total bytes, or ``0`` when the directory does not exist.
    """
    if not directory.is_dir():
        return 0
    return sum(item.stat().st_size for item in directory.rglob("*") if item.is_file())


def main() -> None:
    """Run the CLI, mapping uncaught pipeline errors onto exit codes."""
    try:
        app()
    except PipelineError as exc:
        log_error(exc.message)
        if exc.hint:
            console.print(f"  [warn]Hint:[/warn] {escape(exc.hint)}")
        sys.exit(int(exc.exit_code))
    except KeyboardInterrupt:
        console.print()
        log_warn("Interrupted.")
        sys.exit(int(ExitCode.INTERRUPTED))


if __name__ == "__main__":
    main()
