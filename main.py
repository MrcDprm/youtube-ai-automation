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
from pathlib import Path
from typing import Annotated

import typer
from rich.markup import escape
from rich.table import Table

from config.constants import PROJECT_ROOT, ExitCode
from config.settings import Settings, get_settings
from models.scenario import Scenario
from modules.editor import MoviePyEditor
from modules.interfaces import IMediaProvider, IUploader, MediaCandidate
from modules.media_cache import MediaCache
from modules.pipeline import PipelineOptions, VideoPipeline
from modules.scenario_loader import describe_scenario, load_scenario
from modules.subtitle import SrtSubtitleBuilder
from modules.thumbnail import PillowThumbnailBuilder
from modules.tts import EdgeTTSEngine
from modules.uploader import YouTubeUploader
from modules.video_fetcher import (
    CompositeMediaProvider,
    PexelsVideoProvider,
    PixabayVideoProvider,
)
from utils.exceptions import ConfigurationError, MediaProviderError, PipelineError
from utils.fs import clear_directory, download_default_font, format_bytes, resolve_font
from utils.logger import (
    console,
    log_error,
    log_info,
    log_metric,
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
    cache = MediaCache(
        settings.media_cache_dir(),
        timeout=settings.HTTP_TIMEOUT,
        max_attempts=settings.MAX_RETRIES,
        force=force,
    )

    providers: list[IMediaProvider] = []
    if settings.PEXELS_API_KEY.strip():
        providers.append(
            PexelsVideoProvider(
                settings.PEXELS_API_KEY,
                cache,
                timeout=settings.HTTP_TIMEOUT,
                max_attempts=settings.MAX_RETRIES,
            )
        )
    if settings.PIXABAY_API_KEY.strip():
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

    log_path = setup_logging(
        level=settings.LOG_LEVEL,
        log_dir=settings.logs_dir(),
        project_id=parsed.project_id,
        secrets=settings.secret_values(),
        verbose=verbose,
    )

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
        pipeline = _build_pipeline(parsed, settings, options)
    except PipelineError as exc:
        _fail(exc)
        return

    try:
        pipeline.run()
    except PipelineError as exc:
        if log_path is not None:
            log_info(f"Full log: {log_path}")
        _fail(exc)
        return
    except KeyboardInterrupt:
        log_warn("Interrupted. Completed work is cached; re-run to resume.")
        raise typer.Exit(code=int(ExitCode.INTERRUPTED)) from None

    if not keep_temp and not dry_run:
        clear_directory(settings.temp_dir())

    if log_path is not None:
        log_metric("log file", str(log_path))


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
