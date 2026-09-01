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
PEXELS_PHOTO_SEARCH_URL: Final[str] = "https://api.pexels.com/v1/search"
PEXELS_MAX_PER_PAGE: Final[int] = 80
"""Hard ceiling documented by the Pexels API."""

PEXELS_RATELIMIT_HEADER: Final[str] = "X-Ratelimit-Remaining"
PEXELS_RATELIMIT_LIMIT_HEADER: Final[str] = "X-Ratelimit-Limit"
PEXELS_RATELIMIT_RESET_HEADER: Final[str] = "X-Ratelimit-Reset"
PEXELS_RATELIMIT_WARN_THRESHOLD: Final[int] = 10
"""Emit a loud warning once the hourly remaining-request budget drops this low."""

PIXABAY_SEARCH_URL: Final[str] = "https://pixabay.com/api/videos/"
PIXABAY_PHOTO_SEARCH_URL: Final[str] = "https://pixabay.com/api/"
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

PHOTO_FALLBACK_QUERIES: Final[tuple[str, ...]] = (
    "nature landscape",
    "historic architecture",
    "old library books",
    "starry night sky",
    "vintage map",
)
"""Photo-search fallbacks: still subjects, not video tropes such as timelapse."""

VIDEO_FORMAT_SHORTS: Final[str] = "shorts"
VIDEO_FORMAT_STORY: Final[str] = "story"
VIDEO_FORMAT_PAINT: Final[str] = "paint"
VALID_VIDEO_FORMATS: Final[frozenset[str]] = frozenset(
    {VIDEO_FORMAT_SHORTS, VIDEO_FORMAT_STORY, VIDEO_FORMAT_PAINT}
)

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
MAX_CUE_DURATION: Final[float] = 2.5
CUE_GAP_SECONDS: Final[float] = 0.0
"""Extra separation between consecutive cues. Zero keeps captions on screen without a blink."""

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
# Local script generation (Ollama)
# --------------------------------------------------------------------------------------

OLLAMA_DEFAULT_HOST: Final[str] = "http://localhost:11434"
OLLAMA_CHAT_PATH: Final[str] = "/api/chat"
OLLAMA_TAGS_PATH: Final[str] = "/api/tags"
OLLAMA_DEFAULT_MODEL: Final[str] = "qwen2.5:7b-instruct"
"""Qwen2.5 handles Turkish noticeably better than similarly sized alternatives."""

SCRIPT_MIN_SCENES: Final[int] = 1
SCRIPT_MAX_SCENES: Final[int] = 60
SCRIPT_DEFAULT_SCENES: Final[int] = 8
SCRIPT_MAX_ATTEMPTS: Final[int] = 3
"""How many times to ask the model again when its output fails validation."""

SCRIPT_MAX_SEARCH_TERMS: Final[int] = 3
SCRIPT_MAX_TAGS: Final[int] = 12
SCRIPT_NARRATION_MAX_CHARS: Final[int] = 320
"""A single scene's narration ceiling. Longer text makes scenes drag and clips repeat."""

NARRATION_CHARS_PER_SECOND: Final[float] = 14.0
"""Rough Turkish neural-TTS reading speed, used only to size ``max_duration_seconds``.

The real duration is always measured from the synthesized audio; this estimate exists so a
generated scenario does not set a ceiling its own narration would exceed.
"""

DURATION_ESTIMATE_HEADROOM: Final[float] = 1.6
"""Multiplier applied to the estimated runtime when writing ``max_duration_seconds``."""

SCRIPT_STORY_DEFAULT_CHAPTERS: Final[int] = 12
"""Unused by story ``generate`` (which sizes to ``--minutes``); kept for Shorts-adjacent tests."""

SCRIPT_STORY_CHAPTER_MIN_SECONDS: Final[float] = 90.0
SCRIPT_STORY_CHAPTER_MAX_SECONDS: Final[float] = 110.0
"""Target spoken length per chapter. The real duration is measured from TTS audio."""

STORY_DEFAULT_MINUTES: Final[int] = 15
PAINT_DEFAULT_MINUTES: Final[int] = 11
"""Badly Drawn Why spoken-essay runtime. Story stays at 15."""

PAINT_STILL_SECONDS: Final[float] = 5.0
"""Target hold for each unique paint still so the picture refreshes about every five seconds."""

PAINT_MIN_BEATS: Final[int] = 60
PAINT_MAX_BEATS: Final[int] = 180
"""11-minute essays need 132 stills (660 / 5). Clamp keeps short and long targets in range."""

KEN_BURNS_WORKERS: Final[int] = 8
"""Parallel ffmpeg still encodes. Sequential 132-still Ken Burns is ~40 minutes."""


def paint_beat_count(target_seconds: float) -> int:
    """How many unique stills an essay of ``target_seconds`` needs at the 5s cadence.

    Args:
        target_seconds: Desired spoken length, usually ``PAINT_DEFAULT_MINUTES * 60``.

    Returns:
        A count between ``PAINT_MIN_BEATS`` and ``PAINT_MAX_BEATS``.
    """
    if target_seconds <= 0:
        return PAINT_MIN_BEATS
    raw = int(round(float(target_seconds) / PAINT_STILL_SECONDS))
    return max(PAINT_MIN_BEATS, min(PAINT_MAX_BEATS, raw))


PAINT_CHANNEL_NAME: Final[str] = "Badly Drawn Why"
PAINT_PLACEHOLDER_SEARCH_TERMS: Final[tuple[str, ...]] = (
    "stickman drawing",
    "ms paint illustration",
)
PAINT_PLAYLISTS: Final[tuple[str, ...]] = (
    "The Human Night",
    "The Body",
    "The Mind",
    "Lost Tech",
    "Everyday Weird",
)
DEFAULT_PAINT_TOPICS_FILE: Final[str] = "topics-paint.json"

BRAND_BADLY_DRAWN_WHY: Final[str] = "badly-drawn-why"
FILE_BRAND_ID: Final[str] = "after-hours-file"
FILE_CHANNEL_NAME: Final[str] = "After Hours File"
FILE_PLAYLIST: Final[str] = "Closed Files"
FILE_TTS_VOICE: Final[str] = "en-GB-RyanNeural"
FILE_TTS_VOICE_FALLBACK: Final[str] = "en-GB-ThomasNeural"
FILE_TTS_RATE: Final[str] = "-12%"
FILE_CATEGORY_ID: Final[str] = "24"
FILE_DEFAULT_MINUTES: Final[int] = 10
FILE_STILL_SECONDS: Final[float] = 10.0
FILE_MIN_BEATS: Final[int] = 40
FILE_MAX_BEATS: Final[int] = 80
FILE_SUBTITLE_FONT_SIZE: Final[int] = 42
FILE_SUBTITLE_POSITION_RATIO: Final[float] = 0.86
DEFAULT_FILE_TOPICS_FILE: Final[str] = "topics-file.json"

DRAWN_BRAND_ID: Final[str] = "drawn-anyway"
DRAWN_CHANNEL_NAME: Final[str] = "Drawn Anyway"
DRAWN_PLAYLIST: Final[str] = "One True Story"
DRAWN_TTS_VOICE: Final[str] = "en-AU-WilliamNeural"
DRAWN_TTS_VOICE_FALLBACK: Final[str] = "en-US-GuyNeural"
DRAWN_TTS_RATE: Final[str] = "+4%"
DRAWN_CATEGORY_ID: Final[str] = "24"
DRAWN_DEFAULT_MINUTES: Final[int] = 8
DRAWN_MIN_MINUTES: Final[int] = 8
DRAWN_MAX_MINUTES: Final[int] = 11
DRAWN_BLOCK_SECONDS: Final[float] = 10.0
DRAWN_MIN_BEATS: Final[int] = 48
DRAWN_MAX_BEATS: Final[int] = 66
DRAWN_SUBTITLE_FONT_SIZE: Final[int] = 46
DRAWN_SUBTITLE_POSITION_RATIO: Final[float] = 0.84
DRAWN_ZOOM_END: Final[float] = 1.16
DEFAULT_DRAWN_TOPICS_FILE: Final[str] = "topics-drawn.json"
DRAWN_PLACEHOLDER_SEARCH_TERMS: Final[tuple[str, ...]] = (
    "cartoon illustration",
    "storytime cartoon",
)
YOUTUBE_CATEGORY_LABELS: Final[dict[str, str]] = {
    "24": "Entertainment (24)",
    "27": "Education (27)",
}


def file_beat_count(target_seconds: float) -> int:
    """How many illustrated stills a closed-file essay needs at the 10s cadence.

    Args:
        target_seconds: Desired spoken length, usually ``FILE_DEFAULT_MINUTES * 60``.

    Returns:
        A count between ``FILE_MIN_BEATS`` and ``FILE_MAX_BEATS``.
    """
    if target_seconds <= 0:
        return FILE_MIN_BEATS
    raw = int(round(float(target_seconds) / FILE_STILL_SECONDS))
    return max(FILE_MIN_BEATS, min(FILE_MAX_BEATS, raw))


def drawn_beat_count(target_seconds: float) -> int:
    """How many 10-second cartoon beats a Drawn Anyway episode needs.

    Args:
        target_seconds: Desired spoken length, usually ``DRAWN_DEFAULT_MINUTES * 60``.

    Returns:
        A count between ``DRAWN_MIN_BEATS`` and ``DRAWN_MAX_BEATS`` (48 at 8:00, 66 at 11:00).
    """
    if target_seconds <= 0:
        return DRAWN_MIN_BEATS
    raw = int(round(float(target_seconds) / DRAWN_BLOCK_SECONDS))
    return max(DRAWN_MIN_BEATS, min(DRAWN_MAX_BEATS, raw))

STORY_MIN_MINUTES: Final[int] = 5
STORY_MAX_MINUTES: Final[int] = 40
STORY_MAX_CHAPTERS: Final[int] = 40
STORY_DURATION_TOLERANCE_SECONDS: Final[float] = 45.0
"""``run`` keeps or drops trailing chapters so measured speech lands in target ± this window."""

STORY_TTS_RATE: Final[str] = "-4%"
"""Slightly slower Neural speech for longform; Shorts keeps ``+8%`` / ``+0%``."""

STORY_DEFAULT_MAX_DURATION: Final[float] = 1_500.0
"""Ceiling floor for generated story scenarios; raised when ``--minutes`` needs more headroom."""

STORY_DEFAULT_PHOTO_COUNT: Final[int] = 20
STORY_DEFAULT_OPENING_SECONDS: Final[float] = 210.0
STORY_DEFAULT_OPENING_PHOTO_COUNT: Final[int] = 10
STORY_DEFAULT_OPENING_HOLD_SECONDS: Final[float] = 2.5
STORY_ZOOM_OPENING_END: Final[float] = 1.08
STORY_ZOOM_BODY_END: Final[float] = 1.08
"""Equal slow zoom on every still. Opening-cycle fields remain on the schema but are unused."""

KEN_BURNS_UPSCALE: Final[int] = 4
"""Scale the fitted frame by this before zoompan so each zoom step is sub-pixel at 1920×1080."""

SUBTITLE_BOTTOM_MARGIN_RATIO: Final[float] = 0.075
"""Keep the caption box this fraction of the frame height above the bottom edge."""

STORY_SUBTITLE_PRIMARY: Final[str] = "#FFFFFF"
STORY_SUBTITLE_ACCENT: Final[str] = "#FFD34F"
STORY_SUBTITLE_FONT_SIZE: Final[int] = 48
STORY_SUBTITLE_POSITION_RATIO: Final[float] = 0.82
STORY_SUBTITLE_MAX_CHARS: Final[int] = 32
STORY_SUBTITLE_MARGIN_V: Final[int] = 80
"""ASS ``MarginV`` in pixels for bottom-centered story captions."""

TURKISH_SLUG_MAP: Final[dict[str, str]] = {
    "ı": "i",
    "İ": "i",
    "ş": "s",
    "Ş": "s",
    "ğ": "g",
    "Ğ": "g",
    "ü": "u",
    "Ü": "u",
    "ö": "o",
    "Ö": "o",
    "ç": "c",
    "Ç": "c",
    "â": "a",
    "î": "i",
    "û": "u",
}
"""Turkish letters have no Unicode decomposition, so ASCII folding alone would drop them."""

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
    "studio",
    "storyboard",
)

CACHE_SUBDIRECTORIES: Final[tuple[str, ...]] = ("media", "tts", "scenes", "scheduler")

# --------------------------------------------------------------------------------------
# Daily queue and Windows/POSIX scheduler
# --------------------------------------------------------------------------------------

SCENARIO_QUEUE_SUBDIRECTORIES: Final[tuple[str, ...]] = ("inbox", "processing", "done", "failed")
"""Relative to ``scenarios/``. Inbox is for hand-dropped files; the rest are machine-managed."""

DEFAULT_SCENARIOS_DIR: Final[Path] = Path("scenarios")
DEFAULT_TOPICS_FILE: Final[str] = "topics.json"
SCHEDULER_STATE_FILENAME: Final[str] = "state.json"
DAILY_LOCK_FILENAME: Final[str] = "daily.lock"
DAILY_LOCK_STALE_SECONDS: Final[int] = 6 * 60 * 60
"""A lock older than this is assumed to belong to a crashed run and is stolen."""

SCHEDULER_TASK_NAME: Final[str] = "youtube-automation-daily"
SCHEDULER_DEFAULT_TIME: Final[str] = "09:00"
SCHEDULER_EXECUTION_LIMIT: Final[str] = "PT6H"
"""ISO-8601 duration: a hung daily run is killed after six hours."""

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
