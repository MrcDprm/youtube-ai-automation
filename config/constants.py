"""Immutable project-wide constants: endpoints, limits, codec defaults and exit codes.

Nothing in this module reads the environment or performs I/O, so it is safe to import from
anywhere, including from ``utils.exceptions``.
"""

from __future__ import annotations

from enum import IntEnum
from pathlib import Path
from typing import Final

# --------------------------------------------------------------------------------------
# Locations
# --------------------------------------------------------------------------------------

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
"""Repository root.

Defined in this leaf module rather than in ``config.settings`` so that ``utils`` helpers can
resolve project-relative paths without importing settings, which would create an import cycle
(``config.settings`` itself imports ``utils.exceptions``).
"""

# --------------------------------------------------------------------------------------
# Process exit codes
# --------------------------------------------------------------------------------------


class ExitCode(IntEnum):
    """Process exit codes, one per failure domain.

    These are contractual: shell scripts and CI wrappers branch on them.
    """

    OK = 0
    CONFIG = 1
    VALIDATION = 2
    TTS = 3
    MEDIA = 4
    RENDER = 5
    UPLOAD = 6
    INTERRUPTED = 130


# --------------------------------------------------------------------------------------
# Stock footage providers
# --------------------------------------------------------------------------------------

PEXELS_SEARCH_URL: Final[str] = "https://api.pexels.com/videos/search"
PEXELS_VIDEO_URL: Final[str] = "https://api.pexels.com/videos/videos"
PEXELS_MAX_PER_PAGE: Final[int] = 80
"""Hard ceiling documented by the Pexels API."""

PEXELS_RATELIMIT_HEADER: Final[str] = "X-Ratelimit-Remaining"
PEXELS_RATELIMIT_LIMIT_HEADER: Final[str] = "X-Ratelimit-Limit"
PEXELS_RATELIMIT_RESET_HEADER: Final[str] = "X-Ratelimit-Reset"
PEXELS_RATELIMIT_WARN_THRESHOLD: Final[int] = 10
"""Emit a loud warning once the hourly remaining-request budget drops this low."""

PIXABAY_SEARCH_URL: Final[str] = "https://pixabay.com/api/videos/"
PIXABAY_MAX_PER_PAGE: Final[int] = 200

PROVIDER_PEXELS: Final[str] = "pexels"
PROVIDER_PIXABAY: Final[str] = "pixabay"
PROVIDER_LOCAL: Final[str] = "local"

FALLBACK_QUERIES: Final[tuple[str, ...]] = (
    "abstract background",
    "nature landscape",
    "city timelapse",
    "technology abstract",
    "slow motion clouds",
)
"""Last rung of the query-degradation ladder: generic terms that always return results."""

VALID_ORIENTATIONS: Final[frozenset[str]] = frozenset({"portrait", "landscape", "square"})

ORIENTATION_RESOLUTIONS: Final[dict[str, tuple[int, int]]] = {
    "portrait": (1080, 1920),
    "landscape": (1920, 1080),
    "square": (1080, 1080),
}
"""Canonical resolution per orientation, used when the scenario omits ``resolution``."""

ORIENTATION_TOLERANCE: Final[float] = 0.02
"""Allowed relative deviation when checking that a resolution matches its orientation."""

# --------------------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------------------

RETRYABLE_STATUS_CODES: Final[frozenset[int]] = frozenset({408, 425, 429, 500, 502, 503, 504})
"""Only these justify a retry. Everything else is a caller error and must surface at once."""

DOWNLOAD_CHUNK_SIZE: Final[int] = 1 << 20
"""1 MiB streaming chunk for media downloads."""

USER_AGENT: Final[str] = "youtube-automation/1.0 (+local pipeline; python-requests)"

# --------------------------------------------------------------------------------------
# Encoding / rendering defaults
# --------------------------------------------------------------------------------------

VIDEO_CODEC: Final[str] = "libx264"
AUDIO_CODEC: Final[str] = "aac"
AUDIO_BITRATE: Final[str] = "192k"
PIXEL_FORMAT: Final[str] = "yuv420p"
MIN_CRF: Final[int] = 16
MAX_CRF: Final[int] = 28
MIN_FPS: Final[int] = 24
MAX_FPS: Final[int] = 60

FIRST_FRAMES_SKIP_SECONDS: Final[float] = 0.5
"""Stock clips frequently open on a fade; skip this much before sampling a segment."""

ZOOM_START_SCALE: Final[float] = 1.00
ZOOM_END_SCALE: Final[float] = 1.06
"""Ken Burns endpoints. Kept subtle so the crop never reveals an edge."""

SUBTITLE_WIDTH_RATIO: Final[float] = 0.86
"""Burned-in caption box width as a fraction of the frame width."""

# --------------------------------------------------------------------------------------
# Subtitles
# --------------------------------------------------------------------------------------

MIN_CUE_DURATION: Final[float] = 0.6
MAX_CUE_DURATION: Final[float] = 5.0
CUE_GAP_SECONDS: Final[float] = 0.04
"""Minimum separation between consecutive cues so timestamps stay strictly monotonic."""

SENTENCE_END_CHARS: Final[frozenset[str]] = frozenset({".", "!", "?", "…"})
CLAUSE_END_CHARS: Final[frozenset[str]] = frozenset({",", ";", ":", "—", "–"})

# --------------------------------------------------------------------------------------
# Text normalization (Turkish-first, harmless for other locales)
# --------------------------------------------------------------------------------------

TURKISH_ABBREVIATIONS: Final[dict[str, str]] = {
    "vb.": "ve benzeri",
    "vs.": "vesaire",
    "yy.": "yüzyıl",
    "Dr.": "Doktor",
    "Prof.": "Profesör",
    "Doç.": "Doçent",
    "Av.": "Avukat",
    "Sn.": "Sayın",
    "Bkz.": "bakınız",
    "bkz.": "bakınız",
    "örn.": "örneğin",
    "Örn.": "Örneğin",
    "M.Ö.": "milattan önce",
    "M.S.": "milattan sonra",
    "TL": "Türk Lirası",
}

SYMBOL_EXPANSIONS: Final[dict[str, str]] = {
    "%": " yüzde ",
    "&": " ve ",
    "@": " at ",
    "+": " artı ",
    "=": " eşittir ",
}

# --------------------------------------------------------------------------------------
# YouTube Data API v3
# --------------------------------------------------------------------------------------

YOUTUBE_API_SERVICE_NAME: Final[str] = "youtube"
YOUTUBE_API_VERSION: Final[str] = "v3"

YOUTUBE_SCOPES: Final[tuple[str, ...]] = (
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
)

YOUTUBE_UPLOAD_CHUNK_SIZE: Final[int] = 8 * 1024 * 1024
YOUTUBE_TITLE_MAX_CHARS: Final[int] = 100
YOUTUBE_DESCRIPTION_MAX_CHARS: Final[int] = 5000
YOUTUBE_TAGS_MAX_TOTAL_CHARS: Final[int] = 450
YOUTUBE_THUMBNAIL_MAX_BYTES: Final[int] = 2 * 1024 * 1024
YOUTUBE_WATCH_URL_TEMPLATE: Final[str] = "https://www.youtube.com/watch?v={video_id}"

YOUTUBE_RETRIABLE_STATUS_CODES: Final[frozenset[int]] = frozenset({500, 502, 503, 504})
YOUTUBE_RETRIABLE_REASONS: Final[frozenset[str]] = frozenset(
    {"rateLimitExceeded", "backendError", "internalError", "userRateLimitExceeded"}
)
YOUTUBE_FATAL_REASONS: Final[frozenset[str]] = frozenset(
    {"quotaExceeded", "forbidden", "authError", "uploadLimitExceeded"}
)

YOUTUBE_UPLOAD_QUOTA_COST: Final[int] = 1600
YOUTUBE_DAILY_QUOTA_DEFAULT: Final[int] = 10_000

THUMBNAIL_SIZE: Final[tuple[int, int]] = (1280, 720)
THUMBNAIL_FRAME_RATIO: Final[float] = 0.15
"""Grab the thumbnail source frame this far into the video."""

THUMBNAIL_JPEG_QUALITY: Final[int] = 90
THUMBNAIL_MIN_JPEG_QUALITY: Final[int] = 55

# --------------------------------------------------------------------------------------
# Attribution
# --------------------------------------------------------------------------------------

ATTRIBUTION_HEADER: Final[str] = "---"
ATTRIBUTION_LINE_TEMPLATE: Final[str] = "Footage: {provider} — {author} ({page_url})"
SYNTHETIC_DISCLOSURE_TEXT: Final[str] = (
    "Bu videonun anlatimi yapay ses sentezi (text-to-speech) ile uretilmistir. "
    "/ This video's narration was produced with synthetic text-to-speech audio."
)

# --------------------------------------------------------------------------------------
# Fonts
# --------------------------------------------------------------------------------------

FONT_EXTENSIONS: Final[tuple[str, ...]] = (".ttf", ".otf", ".ttc")

INTER_ZIP_URL: Final[str] = "https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip"
INTER_ZIP_MEMBER_CANDIDATES: Final[tuple[str, ...]] = (
    "Inter-Bold.ttf",
    "Inter_18pt-Bold.ttf",
    "Inter_24pt-Bold.ttf",
    "Inter_28pt-Bold.ttf",
)
"""Static bold faces to look for inside the Inter release archive, best first."""

ANTON_TTF_URL: Final[str] = (
    "https://raw.githubusercontent.com/google/fonts/main/ofl/anton/Anton-Regular.ttf"
)
ANTON_FILENAME: Final[str] = "Anton-Regular.ttf"

SYSTEM_FONT_DIRECTORIES: Final[dict[str, tuple[str, ...]]] = {
    "win32": (r"C:\Windows\Fonts",),
    "darwin": ("/System/Library/Fonts", "/Library/Fonts", "~/Library/Fonts"),
    "linux": ("/usr/share/fonts", "/usr/local/share/fonts", "~/.fonts", "~/.local/share/fonts"),
}

SYSTEM_FONT_PREFERENCES: Final[tuple[str, ...]] = (
    "DejaVuSans-Bold.ttf",
    "DejaVuSans.ttf",
    "LiberationSans-Bold.ttf",
    "arialbd.ttf",
    "Arial Bold.ttf",
    "arial.ttf",
    "Arial.ttf",
    "segoeuib.ttf",
    "segoeui.ttf",
    "HelveticaNeue.ttc",
    "Helvetica.ttc",
    "NotoSans-Bold.ttf",
    "NotoSans-Regular.ttf",
)
"""Preferred system faces, best first. All of them cover the Turkish alphabet."""

# --------------------------------------------------------------------------------------
# Preflight
# --------------------------------------------------------------------------------------

MIN_PYTHON_VERSION: Final[tuple[int, int]] = (3, 10)
MIN_FREE_DISK_BYTES: Final[int] = 2 * 1024 * 1024 * 1024

OUTPUT_SUBDIRECTORIES: Final[tuple[str, ...]] = (
    "audio",
    "clips",
    "subtitles",
    "scenes",
    "final",
    "thumbnails",
    "logs",
    "temp",
)

CACHE_SUBDIRECTORIES: Final[tuple[str, ...]] = ("media", "tts", "scenes")

# --------------------------------------------------------------------------------------
# Secret redaction
# --------------------------------------------------------------------------------------

SECRET_ENV_VARS: Final[tuple[str, ...]] = (
    "PEXELS_API_KEY",
    "PIXABAY_API_KEY",
    "YOUTUBE_CLIENT_SECRET",
    "GOOGLE_CLIENT_SECRET",
)

REDACTION_PLACEHOLDER: Final[str] = "***REDACTED***"
MIN_REDACTABLE_SECRET_LENGTH: Final[int] = 8
"""Shorter values are too generic to blanket-replace without mangling ordinary log text."""
