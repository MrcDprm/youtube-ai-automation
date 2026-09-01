"""Pydantic v2 models that define the ``senaryo.json`` schema.

Every model sets ``extra="forbid"`` so a typo in the scenario file fails validation loudly
instead of being silently dropped. Cross-field rules that cannot be expressed as simple field
constraints live in ``model_validator`` hooks at the end of each class.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)

from config.constants import (
    MAX_CRF,
    MAX_FPS,
    MIN_CRF,
    MIN_FPS,
    ORIENTATION_RESOLUTIONS,
    ORIENTATION_TOLERANCE,
    PAINT_MAX_BEATS,
    STORY_DEFAULT_OPENING_HOLD_SECONDS,
    STORY_DEFAULT_OPENING_PHOTO_COUNT,
    STORY_DEFAULT_OPENING_SECONDS,
    STORY_DEFAULT_PHOTO_COUNT,
    STORY_ZOOM_BODY_END,
    STORY_ZOOM_OPENING_END,
    YOUTUBE_DESCRIPTION_MAX_CHARS,
    YOUTUBE_TAGS_MAX_TOTAL_CHARS,
    YOUTUBE_TITLE_MAX_CHARS,
)
from config.settings import PROJECT_ROOT, get_settings
from utils.fs import font_is_resolvable

__all__ = [
    "BackgroundMusic",
    "Orientation",
    "Scenario",
    "Scene",
    "StoryVisualSettings",
    "SubtitleSettings",
    "TTSSettings",
    "VideoFormat",
    "VideoSettings",
    "VisualBeat",
    "YouTubeSettings",
    "resolve_project_path",
]

Orientation = Literal["portrait", "landscape", "square"]
VideoFormat = Literal["shorts", "story", "paint"]
PrivacyStatus = Literal["private", "unlisted", "public"]
FfmpegPreset = Literal["ultrafast", "veryfast", "faster", "fast", "medium", "slow"]

HexColor = Annotated[str, Field(pattern=r"^#[0-9A-Fa-f]{6}$")]
PercentString = Annotated[str, Field(pattern=r"^[+-]\d{1,3}%$")]
HertzString = Annotated[str, Field(pattern=r"^[+-]\d{1,3}Hz$")]
ProjectSlug = Annotated[str, Field(pattern=r"^[a-z0-9_-]{3,64}$")]


def resolve_project_path(path: Path) -> Path:
    """Resolve a scenario-supplied path against the project root.

    Scenario files use repository-relative paths such as ``assets/music/loop.mp3`` so they stay
    portable. Resolving against the project root rather than the working directory means the
    pipeline behaves identically no matter where it is invoked from.

    Args:
        path: A relative or absolute path taken from the scenario.

    Returns:
        An absolute path. The file is not required to exist.
    """
    return path if path.is_absolute() else (PROJECT_ROOT / path)


class StrictModel(BaseModel):
    """Base model that rejects unknown keys and strips surrounding whitespace."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class BackgroundMusic(StrictModel):
    """Optional music bed mixed under the narration."""

    enabled: bool = False
    file: Path | None = None
    volume: float = Field(default=0.08, ge=0.0, le=1.0)
    fade_in_seconds: float = Field(default=1.5, ge=0.0, le=30.0)
    fade_out_seconds: float = Field(default=2.5, ge=0.0, le=30.0)
    duck_to: float = Field(default=0.5, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def _check_file_present_when_enabled(self) -> BackgroundMusic:
        """Require an existing audio file whenever music is switched on.

        Raises:
            ValueError: If ``enabled`` is true but ``file`` is unset or missing on disk.
        """
        if not self.enabled:
            return self
        if self.file is None:
            raise ValueError(
                "background_music.file is required when background_music.enabled is true"
            )
        resolved = resolve_project_path(self.file)
        if not resolved.is_file():
            raise ValueError(
                f"background_music.file does not exist: {resolved}. "
                "Drop a licensed audio file there or set enabled to false."
            )
        return self

    @property
    def resolved_file(self) -> Path | None:
        """Absolute path to the music file, or ``None`` when unset."""
        return resolve_project_path(self.file) if self.file is not None else None


class StoryVisualSettings(StrictModel):
    """Equal-time stills track used when ``video.format`` is ``story``.

    Ignored for Shorts. Opening-cycle fields stay on the schema so older JSON still loads;
    the editor ignores them and gives every photo the same slow zoom.
    """

    photo_count: int = Field(default=STORY_DEFAULT_PHOTO_COUNT, ge=2, le=PAINT_MAX_BEATS)
    opening_seconds: float = Field(default=STORY_DEFAULT_OPENING_SECONDS, gt=0.0, le=1_200.0)
    opening_photo_count: int = Field(default=STORY_DEFAULT_OPENING_PHOTO_COUNT, ge=1, le=40)
    opening_hold_seconds: float = Field(default=STORY_DEFAULT_OPENING_HOLD_SECONDS, gt=0.2, le=30.0)
    zoom_opening_end: float = Field(default=STORY_ZOOM_OPENING_END, ge=1.0, le=1.4)
    zoom_body_end: float = Field(default=STORY_ZOOM_BODY_END, ge=1.0, le=1.5)
    zenn_enabled: bool = False

    @model_validator(mode="after")
    def _check_opening_fits_photos(self) -> StoryVisualSettings:
        """Require at least one body photo after the opening set."""
        if self.opening_photo_count >= self.photo_count:
            raise ValueError(
                "story_visual.opening_photo_count must be smaller than story_visual.photo_count "
                "so the body band has photos left."
            )
        return self


class VisualBeat(StrictModel):
    """One MS Paint still timed against the spoken essay.

    ``image`` is optional at generate time. ``run`` resolves files from the storyboard
    folder when the path is omitted. Existence is checked only when a path is set.
    """

    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+){0,8}$", min_length=2, max_length=48)
    prompt: str = Field(min_length=8, max_length=1600)
    covers: str = Field(default="", max_length=500)
    image: Path | None = None

    @field_validator("covers")
    @classmethod
    def _strip_covers(cls, value: str) -> str:
        """Allow a blank covers line; strip accidental whitespace."""
        return value.strip()

    @field_validator("image")
    @classmethod
    def _check_image_exists(cls, value: Path | None) -> Path | None:
        """Require a beat image to exist only when the scenario points at one."""
        if value is None:
            return None
        resolved = resolve_project_path(value)
        if not resolved.is_file():
            raise ValueError(f"visual_beats.image does not exist: {resolved}")
        return value

    @property
    def resolved_image(self) -> Path | None:
        """Absolute path to a declared beat image, or ``None``."""
        return resolve_project_path(self.image) if self.image is not None else None

    @property
    def weight(self) -> float:
        """Relative hold length; falls back to 1 when ``covers`` is empty."""
        return float(max(1, len(self.covers)))


class VideoSettings(StrictModel):
    """Geometry, pacing and encoder settings for the finished video."""

    orientation: Orientation = "portrait"
    resolution: tuple[int, int] = (1080, 1920)
    fps: int = Field(default=30, ge=MIN_FPS, le=MAX_FPS)
    max_duration_seconds: float = Field(default=175.0, gt=0.0, le=43_200.0)
    scene_gap_seconds: float = Field(default=0.30, ge=0.0, le=2.0)
    crossfade_seconds: float = Field(default=0.0, ge=0.0, le=5.0)
    video_bitrate_crf: int = Field(default=20, ge=MIN_CRF, le=MAX_CRF)
    preset: FfmpegPreset = "medium"
    background_music: BackgroundMusic = Field(default_factory=BackgroundMusic)
    format: VideoFormat = "shorts"
    story_visual: StoryVisualSettings = Field(default_factory=StoryVisualSettings)
    visual_beats: list[VisualBeat] = Field(default_factory=list)
    target_duration_seconds: float | None = Field(default=None, ge=60.0, le=43_200.0)

    @model_validator(mode="before")
    @classmethod
    def _derive_resolution(cls, data: Any) -> Any:
        """Fill ``resolution`` from ``orientation`` when the key is absent.

        Args:
            data: Raw input mapping, or any other value which is passed through untouched.

        Returns:
            The input with ``resolution`` populated when it was omitted.
        """
        if isinstance(data, dict) and data.get("resolution") is None:
            orientation = data.get("orientation", "portrait")
            if orientation in ORIENTATION_RESOLUTIONS:
                data = {**data, "resolution": ORIENTATION_RESOLUTIONS[orientation]}
        return data

    @field_validator("resolution")
    @classmethod
    def _check_resolution_sane(cls, value: tuple[int, int]) -> tuple[int, int]:
        """Reject non-positive or odd dimensions.

        H.264 with ``yuv420p`` chroma subsampling requires even width and height.
        """
        width, height = value
        if width <= 0 or height <= 0:
            raise ValueError(f"resolution must be positive, got {width}x{height}")
        if width % 2 or height % 2:
            raise ValueError(
                f"resolution must have even dimensions for yuv420p, got {width}x{height}"
            )
        return value

    @model_validator(mode="after")
    def _check_resolution_matches_orientation(self) -> VideoSettings:
        """Ensure the declared resolution actually has the declared orientation.

        Raises:
            ValueError: If, for example, ``orientation`` is ``portrait`` but the resolution is
                wider than it is tall.
        """
        width, height = self.resolution
        actual = width / height
        expected_w, expected_h = ORIENTATION_RESOLUTIONS[self.orientation]
        expected = expected_w / expected_h
        if abs(actual - expected) / expected > ORIENTATION_TOLERANCE:
            raise ValueError(
                f"resolution {width}x{height} (aspect {actual:.3f}) does not match "
                f"orientation '{self.orientation}' (expected aspect ~{expected:.3f}). "
                f"Use {expected_w}x{expected_h} or change the orientation."
            )
        return self

    @property
    def width(self) -> int:
        """Target frame width in pixels."""
        return self.resolution[0]

    @property
    def height(self) -> int:
        """Target frame height in pixels."""
        return self.resolution[1]

    @property
    def is_story(self) -> bool:
        """Whether this project uses the longform photo-story (Pexels stills) path."""
        return self.format == "story"

    @property
    def is_paint(self) -> bool:
        """Whether this project uses agent-drawn MS Paint stills."""
        return self.format == "paint"

    @property
    def is_zenn(self) -> bool:
        """Whether this paint project uses programmatic stick-cut beats."""
        return self.is_paint and self.story_visual.zenn_enabled

    @property
    def is_longform(self) -> bool:
        """Whether this project is a landscape stills essay (story or paint)."""
        return self.format in {"story", "paint"}


class TTSSettings(StrictModel):
    """Voice selection and prosody for edge-tts."""

    voice: str = Field(default="tr-TR-AhmetNeural", min_length=3)
    rate: PercentString = "+0%"
    volume: PercentString = "+0%"
    pitch: HertzString = "+0Hz"
    normalize_text: bool = True
    language: str = Field(default="tr", min_length=2, max_length=16)


def _default_font() -> Path:
    """Return the font configured in the environment.

    Returns:
        The ``DEFAULT_FONT`` path from settings, used when the scenario omits ``subtitles.font``.
    """
    return get_settings().DEFAULT_FONT


class SubtitleSettings(StrictModel):
    """Subtitle generation and burn-in appearance."""

    enabled: bool = True
    burn_in: bool = True
    max_chars_per_line: int = Field(default=32, ge=10, le=120)
    max_lines: int = Field(default=2, ge=1, le=4)
    font: Path = Field(default_factory=_default_font)
    font_size: int = Field(default=60, ge=8, le=400)
    color: HexColor = "#FFFFFF"
    accent_color: HexColor | None = None
    stroke_color: HexColor = "#000000"
    stroke_width: int = Field(default=3, ge=0, le=40)
    position_ratio: float = Field(default=0.72, ge=0.0, le=1.0)
    uppercase: bool = False
    numeral_display: bool = False

    @model_validator(mode="after")
    def _check_font_available_for_burn_in(self) -> SubtitleSettings:
        """Ensure some usable font exists when captions are burned into the frame.

        The configured path does not have to exist: ``utils.fs.resolve_font`` falls back to
        other fonts in ``assets/fonts/`` and then to the platform's font directories. Only a
        total absence of usable fonts is a validation error.

        Raises:
            ValueError: If ``burn_in`` is true and no font can be resolved at all.
        """
        if not self.enabled or not self.burn_in:
            return self
        if not font_is_resolvable(resolve_project_path(self.font)):
            raise ValueError(
                f"subtitles.font could not be resolved: {self.font}. "
                "Run 'python main.py doctor --fix' to download a font, or drop a .ttf into "
                "assets/fonts/ and point subtitles.font at it. "
                "Set subtitles.burn_in to false to write only the .srt sidecar."
            )
        return self

    @property
    def max_chars_per_cue(self) -> int:
        """Maximum characters a single cue may hold across all of its lines."""
        return self.max_chars_per_line * self.max_lines


class YouTubeSettings(StrictModel):
    """Upload metadata and destination settings."""

    upload_enabled: bool = False
    title: str = Field(min_length=1, max_length=YOUTUBE_TITLE_MAX_CHARS)
    description: str = Field(default="", max_length=YOUTUBE_DESCRIPTION_MAX_CHARS)
    tags: list[str] = Field(default_factory=list)
    category_id: str = Field(default="27", pattern=r"^\d{1,3}$")
    privacy_status: PrivacyStatus = "private"
    made_for_kids: bool = False
    synthetic_content_disclosure: bool = True
    publish_at: datetime | None = None
    playlist_id: str | None = None
    default_language: str = Field(default="tr", pattern=r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$")
    thumbnail_enabled: bool = True
    thumbnail_hook: str = Field(default="", max_length=40)
    brand_id: str = Field(default="", max_length=64)

    @field_validator("title")
    @classmethod
    def _check_title_not_blank(cls, value: str) -> str:
        """Reject titles that are empty once whitespace is removed.

        Also rejects the angle brackets YouTube forbids in titles.
        """
        if not value.strip():
            raise ValueError("youtube.title must not be blank")
        if "<" in value or ">" in value:
            raise ValueError("youtube.title must not contain '<' or '>' characters")
        return value

    @field_validator("tags")
    @classmethod
    def _check_tags_budget(cls, value: list[str]) -> list[str]:
        """Enforce YouTube's aggregate tag length budget.

        Raises:
            ValueError: If any tag is blank or the joined length exceeds the API limit.
        """
        cleaned = [tag.strip() for tag in value]
        if any(not tag for tag in cleaned):
            raise ValueError("youtube.tags must not contain empty entries")
        total = sum(len(tag) for tag in cleaned) + max(0, len(cleaned) - 1)
        if total > YOUTUBE_TAGS_MAX_TOTAL_CHARS:
            raise ValueError(
                f"youtube.tags joined length is {total} characters, over the "
                f"{YOUTUBE_TAGS_MAX_TOTAL_CHARS} character limit. Remove some tags."
            )
        return cleaned

    @field_validator("publish_at")
    @classmethod
    def _normalize_publish_at(cls, value: datetime | None) -> datetime | None:
        """Attach UTC to naive datetimes so comparisons and RFC 3339 output are unambiguous."""
        if value is None:
            return None
        return value.replace(tzinfo=UTC) if value.tzinfo is None else value

    @model_validator(mode="after")
    def _check_schedule(self) -> YouTubeSettings:
        """Validate scheduled publishing.

        Raises:
            ValueError: If ``publish_at`` is in the past, or is combined with a
                ``privacy_status`` other than ``private``, which the API rejects.
        """
        if self.publish_at is None:
            return self
        if self.publish_at <= datetime.now(UTC):
            raise ValueError(
                f"youtube.publish_at must be in the future, got {self.publish_at.isoformat()}"
            )
        if self.privacy_status != "private":
            raise ValueError(
                "youtube.publish_at requires youtube.privacy_status to be 'private'; "
                f"got '{self.privacy_status}'. YouTube flips it to public at the scheduled time."
            )
        return self


class Scene(StrictModel):
    """One narrated beat of the video."""

    id: int = Field(gt=0)
    narration: str = Field(min_length=1)
    search_terms: list[str] = Field(min_length=1)
    orientation: Orientation | None = None
    clips_per_scene: int = Field(default=1, ge=1, le=4)
    min_clip_duration: float = Field(default=3.0, gt=0.0, le=120.0)
    local_media: Path | None = None
    pexels_video_id: int | None = Field(default=None, gt=0)
    zoom_effect: bool = True

    @field_validator("narration")
    @classmethod
    def _check_narration_not_blank(cls, value: str) -> str:
        """Reject narration that is empty once stripped."""
        if not value.strip():
            raise ValueError("scene.narration must not be blank")
        return value

    @field_validator("search_terms")
    @classmethod
    def _check_search_terms(cls, value: list[str]) -> list[str]:
        """Reject blank search terms, which would degrade to an empty stock query."""
        cleaned = [term.strip() for term in value]
        if any(not term for term in cleaned):
            raise ValueError("scene.search_terms must not contain empty strings")
        return cleaned

    @field_validator("local_media")
    @classmethod
    def _check_local_media_exists(cls, value: Path | None, info: ValidationInfo) -> Path | None:
        """Require the local media override to exist on disk.

        Args:
            value: The configured path, or ``None``.
            info: Validation context supplied by pydantic.

        Returns:
            The unchanged value.

        Raises:
            ValueError: If the path is set but missing.
        """
        if value is None:
            return None
        resolved = resolve_project_path(value)
        if not resolved.is_file():
            field = info.field_name or "local_media"
            raise ValueError(f"scene.{field} does not exist: {resolved}")
        return value

    @property
    def resolved_local_media(self) -> Path | None:
        """Absolute path to the local media override, or ``None``."""
        return resolve_project_path(self.local_media) if self.local_media else None

    @property
    def primary_search_term(self) -> str:
        """The first, most specific search term."""
        return self.search_terms[0]


class Scenario(StrictModel):
    """A complete, validated video project."""

    project_id: ProjectSlug
    video: VideoSettings = Field(default_factory=VideoSettings)
    tts: TTSSettings = Field(default_factory=TTSSettings)
    subtitles: SubtitleSettings = Field(default_factory=SubtitleSettings)
    youtube: YouTubeSettings
    scenes: list[Scene] = Field(min_length=1)

    @field_validator("scenes")
    @classmethod
    def _check_unique_scene_ids(cls, value: list[Scene]) -> list[Scene]:
        """Reject duplicate scene ids, which would collide on cache and output filenames.

        Raises:
            ValueError: Listing every duplicated id.
        """
        seen: set[int] = set()
        duplicates: list[int] = []
        for scene in value:
            if scene.id in seen:
                duplicates.append(scene.id)
            seen.add(scene.id)
        if duplicates:
            unique = sorted(set(duplicates))
            raise ValueError(
                f"scene ids must be unique; duplicated: {unique}. "
                "Scene ids name the cached audio and rendered scene files."
            )
        return value

    @model_validator(mode="after")
    def _check_crossfade_fits(self) -> Scenario:
        """Ensure the crossfade is short enough for the shortest scene.

        A crossfade consumes ``crossfade_seconds`` from the tail of one scene and the head of
        the next, so twice its length must stay under the shortest clip.

        Raises:
            ValueError: If the crossfade would consume a whole scene.
        """
        crossfade = self.video.crossfade_seconds
        if crossfade <= 0:
            return self
        shortest = min(scene.min_clip_duration for scene in self.scenes)
        if crossfade * 2 >= shortest:
            raise ValueError(
                f"video.crossfade_seconds ({crossfade}) is too long: twice the crossfade "
                f"({crossfade * 2}) must be under the shortest scene.min_clip_duration "
                f"({shortest}). Lower the crossfade or raise min_clip_duration."
            )
        return self

    @model_validator(mode="after")
    def _check_orientation_overrides(self) -> Scenario:
        """Reject per-scene orientations that disagree with the video's aspect ratio.

        Mixing orientations inside one render would force letterboxing, which the editor
        deliberately never does.

        Raises:
            ValueError: If a scene overrides the orientation to a different aspect ratio.
        """
        offenders = [
            scene.id
            for scene in self.scenes
            if scene.orientation is not None and scene.orientation != self.video.orientation
        ]
        if offenders:
            raise ValueError(
                f"scene(s) {offenders} override orientation to a value different from "
                f"video.orientation ('{self.video.orientation}'). A single render cannot mix "
                "aspect ratios without letterboxing. Remove the per-scene override, or split "
                "the project into separate scenario files."
            )
        return self

    @property
    def total_scenes(self) -> int:
        """Number of scenes in the project."""
        return len(self.scenes)

    def estimated_narration_seconds(self) -> float:
        """Estimate total narration length before any synthesis happens.

        Uses a conservative 15 characters per second, roughly the pace of Turkish neural
        voices at ``+0%`` rate, plus the configured inter-scene gaps.

        Returns:
            Estimated total duration in seconds.
        """
        chars_per_second = 15.0
        spoken = sum(len(scene.narration) for scene in self.scenes) / chars_per_second
        gaps = self.video.scene_gap_seconds * len(self.scenes)
        return spoken + gaps

    def scene_by_id(self, scene_id: int) -> Scene:
        """Look up a scene by its id.

        Args:
            scene_id: The scene identifier.

        Returns:
            The matching :class:`Scene`.

        Raises:
            KeyError: If no scene has that id.
        """
        for scene in self.scenes:
            if scene.id == scene_id:
                return scene
        raise KeyError(f"No scene with id {scene_id}")
