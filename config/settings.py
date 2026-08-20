"""Runtime settings loaded from the environment and ``.env``.

All secrets enter the process here and nowhere else. Nothing in this module logs a value;
``utils.logger.SecretRedactingFilter`` consumes :func:`Settings.secret_values` to scrub
anything that slips into a log record.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.constants import CACHE_SUBDIRECTORIES, OUTPUT_SUBDIRECTORIES, PROJECT_ROOT
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
