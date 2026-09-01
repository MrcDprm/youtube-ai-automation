"""Runtime settings loaded from the environment and ``.env``.

All secrets enter the process here and nowhere else. Nothing in this module logs a value;
``utils.logger.SecretRedactingFilter`` consumes :func:`Settings.secret_values` to scrub
anything that slips into a log record.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.constants import (
    CACHE_SUBDIRECTORIES,
    DEFAULT_SCENARIOS_DIR,
    DEFAULT_TOPICS_FILE,
    OLLAMA_DEFAULT_HOST,
    OLLAMA_DEFAULT_MODEL,
    OUTPUT_SUBDIRECTORIES,
    PROJECT_ROOT,
    SCHEDULER_STATE_FILENAME,
    SCRIPT_DEFAULT_SCENES,
    SCRIPT_MAX_SCENES,
    SCRIPT_MIN_SCENES,
    VALID_ORIENTATIONS,
    VALID_VIDEO_FORMATS,
    VIDEO_FORMAT_SHORTS,
)
from utils.exceptions import ConfigurationError

__all__ = ["PROJECT_ROOT", "Settings", "get_settings"]


class Settings(BaseSettings):
    """Typed view of the process environment.

    Attributes are populated from, in order of precedence: real environment variables, the
    ``.env`` file, then the defaults declared here. Missing optional keys stay empty rather
    than raising, so ``doctor`` can report every problem at once instead of the first one.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Stock footage providers ---------------------------------------------------
    PEXELS_API_KEY: str = Field(default="")
    PIXABAY_API_KEY: str = Field(default="")

    # --- YouTube -------------------------------------------------------------------
    YOUTUBE_CLIENT_SECRETS_FILE: Path = Field(default=Path("secrets/client_secrets.json"))
    YOUTUBE_TOKEN_FILE: Path = Field(default=Path("secrets/token.json"))

    # --- Local script generation ----------------------------------------------------
    OLLAMA_HOST: str = Field(default=OLLAMA_DEFAULT_HOST)
    OLLAMA_MODEL: str = Field(default=OLLAMA_DEFAULT_MODEL)
    OLLAMA_TIMEOUT: float = Field(default=180.0, gt=0, le=3600)

    # --- Daily automation -----------------------------------------------------------
    DAILY_UPLOAD: bool = Field(default=False)
    DAILY_SCENES: int = Field(
        default=SCRIPT_DEFAULT_SCENES, ge=SCRIPT_MIN_SCENES, le=SCRIPT_MAX_SCENES
    )
    DAILY_LANGUAGE: str = Field(default="tr")
    DAILY_ORIENTATION: str = Field(default="portrait")
    VIDEO_FORMAT: str = Field(default=VIDEO_FORMAT_SHORTS)
    DAILY_TIME: str = Field(default="09:00")
    SCENARIOS_DIR: Path = Field(default=DEFAULT_SCENARIOS_DIR)

    # --- Runtime -------------------------------------------------------------------
    LOG_LEVEL: str = Field(default="INFO")
    OUTPUT_DIR: Path = Field(default=Path("output"))
    CACHE_DIR: Path = Field(default=Path(".cache"))
    HTTP_TIMEOUT: float = Field(default=30.0, gt=0, le=600)
    MAX_RETRIES: int = Field(default=4, ge=1, le=10)
    FFMPEG_THREADS: int = Field(default=4, ge=1, le=64)
    DEFAULT_FONT: Path = Field(default=Path("assets/fonts/Inter-Bold.ttf"))

    @field_validator("LOG_LEVEL")
    @classmethod
    def _validate_log_level(cls, value: str) -> str:
        """Accept any casing but store the canonical upper-case name."""
        allowed = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"}
        normalized = value.strip().upper()
        if normalized not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {sorted(allowed)}, got {value!r}")
        return normalized

    @field_validator("OLLAMA_HOST")
    @classmethod
    def _validate_ollama_host(cls, value: str) -> str:
        """Require a scheme and drop any trailing slash so path joining stays predictable."""
        cleaned = value.strip().rstrip("/")
        if not cleaned:
            raise ValueError("OLLAMA_HOST cannot be empty")
        if not cleaned.startswith(("http://", "https://")):
            raise ValueError(f"OLLAMA_HOST must start with http:// or https://, got {value!r}")
        return cleaned

    @field_validator("DAILY_ORIENTATION")
    @classmethod
    def _validate_daily_orientation(cls, value: str) -> str:
        """Accept only the three orientations the rest of the pipeline understands."""
        cleaned = value.strip().lower()
        if cleaned not in VALID_ORIENTATIONS:
            raise ValueError(
                f"DAILY_ORIENTATION must be one of {sorted(VALID_ORIENTATIONS)}, got {value!r}"
            )
        return cleaned

    @field_validator("VIDEO_FORMAT")
    @classmethod
    def _validate_video_format(cls, value: str) -> str:
        """Accept only the formats the pipeline knows how to render."""
        cleaned = value.strip().lower()
        if cleaned not in VALID_VIDEO_FORMATS:
            raise ValueError(
                f"VIDEO_FORMAT must be one of {sorted(VALID_VIDEO_FORMATS)}, got {value!r}"
            )
        return cleaned

    @field_validator("DAILY_TIME")
    @classmethod
    def _validate_daily_time(cls, value: str) -> str:
        """Require a 24-hour ``HH:MM`` clock time for the scheduled task."""
        cleaned = value.strip()
        if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", cleaned):
            raise ValueError(f"DAILY_TIME must look like '09:00', got {value!r}")
        return cleaned

    def ollama_url(self, path: str) -> str:
        """Build a full Ollama endpoint URL.

        Args:
            path: An endpoint path beginning with a slash, such as ``"/api/chat"``.

        Returns:
            The absolute URL.
        """
        return f"{self.OLLAMA_HOST}{path}"

    # --- Derived paths --------------------------------------------------------------

    @staticmethod
    def _absolute(path: Path) -> Path:
        """Resolve ``path`` against the project root when it is relative.

        Args:
            path: A possibly relative path from the environment.

        Returns:
            An absolute path, so behaviour does not depend on the working directory.
        """
        return path if path.is_absolute() else (PROJECT_ROOT / path)

    @property
    def output_dir(self) -> Path:
        """Absolute output directory."""
        return self._absolute(self.OUTPUT_DIR)

    @property
    def cache_dir(self) -> Path:
        """Absolute cache directory."""
        return self._absolute(self.CACHE_DIR)

    @property
    def font_path(self) -> Path:
        """Absolute path to the configured default font (may not exist yet)."""
        return self._absolute(self.DEFAULT_FONT)

    @property
    def client_secrets_path(self) -> Path:
        """Absolute path to the OAuth client secrets file (may not exist yet)."""
        return self._absolute(self.YOUTUBE_CLIENT_SECRETS_FILE)

    @property
    def token_path(self) -> Path:
        """Absolute path to the OAuth token cache (may not exist yet)."""
        return self._absolute(self.YOUTUBE_TOKEN_FILE)

    @property
    def fonts_dir(self) -> Path:
        """Directory holding bundled and downloaded fonts."""
        return PROJECT_ROOT / "assets" / "fonts"

    def audio_dir(self) -> Path:
        """Directory for synthesized narration files."""
        return self.output_dir / "audio"

    def clips_dir(self) -> Path:
        """Directory for downloaded stock clips."""
        return self.output_dir / "clips"

    def subtitles_dir(self) -> Path:
        """Directory for generated ``.srt`` files."""
        return self.output_dir / "subtitles"

    def scenes_dir(self) -> Path:
        """Directory for per-scene renders, which is what makes runs resumable."""
        return self.output_dir / "scenes"

    def final_dir(self) -> Path:
        """Directory for the finished video and its manifest."""
        return self.output_dir / "final"

    def thumbnails_dir(self) -> Path:
        """Directory for generated thumbnails."""
        return self.output_dir / "thumbnails"

    def storyboard_dir(self) -> Path:
        """Directory for Badly Drawn Why stills dropped by the image agent."""
        return self.output_dir / "storyboard"

    def studio_dir(self) -> Path:
        """Directory for YouTube Studio copy-paste packs."""
        return self.output_dir / "studio"

    def logs_dir(self) -> Path:
        """Directory for per-run log files."""
        return self.output_dir / "logs"

    def temp_dir(self) -> Path:
        """Directory for intermediate encoder scratch files."""
        return self.output_dir / "temp"

    def media_cache_dir(self) -> Path:
        """Cache for downloaded source media, keyed by URL hash."""
        return self.cache_dir / "media"

    def tts_cache_dir(self) -> Path:
        """Cache for synthesized narration, keyed by text and voice parameters."""
        return self.cache_dir / "tts"

    def scene_cache_dir(self) -> Path:
        """Cache index for rendered scenes, keyed by their full input fingerprint."""
        return self.cache_dir / "scenes"

    def scenarios_dir(self) -> Path:
        """Directory holding the inbox/done/failed queue and ``topics.json``."""
        return self._absolute(self.SCENARIOS_DIR)

    def topics_path(self) -> Path:
        """Path to the topic list the daily command consumes."""
        return self.scenarios_dir() / DEFAULT_TOPICS_FILE

    def scheduler_state_path(self) -> Path:
        """Path to the daily-run state file (last success date and used topics)."""
        return self.cache_dir / "scheduler" / SCHEDULER_STATE_FILENAME

    # --- Helpers ---------------------------------------------------------------------

    def ensure_directories(self) -> None:
        """Create every output and cache subdirectory.

        Raises:
            ConfigurationError: If a directory cannot be created.
        """
        targets = [self.output_dir / name for name in OUTPUT_SUBDIRECTORIES]
        targets += [self.cache_dir / name for name in CACHE_SUBDIRECTORIES]
        for target in targets:
            try:
                target.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                raise ConfigurationError(
                    f"Cannot create directory {target}: {exc}",
                    hint="Check filesystem permissions and that the drive is writable.",
                ) from exc

    def secret_values(self) -> list[str]:
        """Return every non-empty secret value, for log redaction.

        Returns:
            The literal secret strings currently loaded. Never log this list.
        """
        return [value for value in (self.PEXELS_API_KEY, self.PIXABAY_API_KEY) if value]

    def require(self, *names: str) -> None:
        """Assert that the named settings are non-empty.

        Args:
            *names: Attribute names on this model, for example ``"PEXELS_API_KEY"``.

        Raises:
            ConfigurationError: Naming every missing variable, never a raw ``KeyError``.
        """
        missing = [name for name in names if not str(getattr(self, name, "") or "").strip()]
        if missing:
            joined = ", ".join(missing)
            raise ConfigurationError(
                f"Missing required environment variable(s): {joined}",
                hint=(
                    "Copy .env.example to .env and fill the value(s) in. "
                    "See the README for where to obtain each key."
                ),
            )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load settings once per process.

    Returns:
        The cached :class:`Settings` instance.

    Raises:
        ConfigurationError: If a value in the environment cannot be coerced to its declared
            type, reported per field instead of as a raw ``ValidationError``.
    """
    try:
        return Settings()
    except ValidationError as exc:
        details = "; ".join(
            f"{'.'.join(str(part) for part in error['loc']) or '<root>'}: {error['msg']}"
            for error in exc.errors()
        )
        raise ConfigurationError(
            f"Invalid environment configuration: {details}",
            hint="Compare your .env against .env.example; check for typos and stray quotes.",
        ) from exc
