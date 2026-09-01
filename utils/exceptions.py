"""Custom exception hierarchy.

Every exception carries the process :class:`~config.constants.ExitCode` that ``main.py``
should terminate with, so the CLI never has to map exception types to numbers itself.
"""

from __future__ import annotations

from config.constants import ExitCode

__all__ = [
    "ConfigurationError",
    "DiskSpaceError",
    "FontNotFoundError",
    "MediaDownloadError",
    "MediaNotFoundError",
    "MediaProviderError",
    "PipelineError",
    "PreflightError",
    "RenderError",
    "ScenarioValidationError",
    "SchedulerError",
    "ScriptGenerationError",
    "SubtitleError",
    "TTSError",
    "UploadAuthError",
    "UploadError",
    "UploadQuotaError",
]


class PipelineError(Exception):
    """Base class for every error this project raises deliberately.

    Args:
        message: Human-readable description shown to the user.
        hint: Optional actionable next step, rendered on its own line by the CLI.
    """

    exit_code: ExitCode = ExitCode.CONFIG

    def __init__(self, message: str, hint: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint

    def __str__(self) -> str:
        if self.hint:
            return f"{self.message}\nHint: {self.hint}"
        return self.message


# --------------------------------------------------------------------------------------
# Configuration and preflight (exit code 1)
# --------------------------------------------------------------------------------------


class ConfigurationError(PipelineError):
    """A required setting is missing, unreadable or malformed."""

    exit_code = ExitCode.CONFIG


class PreflightError(PipelineError):
    """One or more ``doctor`` checks failed."""

    exit_code = ExitCode.CONFIG


class DiskSpaceError(PreflightError):
    """Not enough free disk space to render safely."""

    exit_code = ExitCode.CONFIG


class FontNotFoundError(ConfigurationError):
    """No usable font file could be resolved for text rendering."""

    exit_code = ExitCode.CONFIG


# --------------------------------------------------------------------------------------
# Scenario validation (exit code 2)
# --------------------------------------------------------------------------------------


class ScenarioValidationError(PipelineError):
    """``senaryo.json`` is missing, is not valid JSON, or violates the schema."""

    exit_code = ExitCode.VALIDATION


class ScriptGenerationError(PipelineError):
    """The local language model could not produce a usable scenario.

    Shares the validation exit code because the failed artifact is a scenario; callers that
    branch on exit codes do not need to learn a new one.
    """

    exit_code = ExitCode.VALIDATION


class SchedulerError(PipelineError):
    """The OS task scheduler could not be queried or updated."""

    exit_code = ExitCode.CONFIG


# --------------------------------------------------------------------------------------
# Speech synthesis (exit code 3)
# --------------------------------------------------------------------------------------


class TTSError(PipelineError):
    """Speech synthesis failed or produced empty audio."""

    exit_code = ExitCode.TTS


class SubtitleError(PipelineError):
    """Subtitle cues could not be built or written."""

    exit_code = ExitCode.TTS


# --------------------------------------------------------------------------------------
# Stock media (exit code 4)
# --------------------------------------------------------------------------------------


class MediaProviderError(PipelineError):
    """A stock footage provider returned an error or an unusable payload."""

    exit_code = ExitCode.MEDIA


class MediaNotFoundError(MediaProviderError):
    """No provider yielded a usable clip, even after query degradation."""

    exit_code = ExitCode.MEDIA


class MediaDownloadError(MediaProviderError):
    """A clip was located but could not be downloaded intact."""

    exit_code = ExitCode.MEDIA


# --------------------------------------------------------------------------------------
# Rendering (exit code 5)
# --------------------------------------------------------------------------------------


class RenderError(PipelineError):
    """Scene composition, assembly or encoding failed."""

    exit_code = ExitCode.RENDER


# --------------------------------------------------------------------------------------
# Upload (exit code 6)
# --------------------------------------------------------------------------------------


class UploadError(PipelineError):
    """The YouTube upload failed."""

    exit_code = ExitCode.UPLOAD


class UploadAuthError(UploadError):
    """OAuth credentials are missing, invalid or could not be refreshed."""

    exit_code = ExitCode.UPLOAD


class UploadQuotaError(UploadError):
    """The daily YouTube API quota is exhausted; retrying today will not help."""

    exit_code = ExitCode.UPLOAD
