"""Abstract interfaces and the data contracts that flow between pipeline stages.

``modules.pipeline`` depends on this module and on :mod:`models` alone. It never imports a
concrete implementation, so replacing Pexels with Pixabay, or edge-tts with any other engine,
is a change to the composition root in ``main.py`` and to nothing else.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from models.scenario import Scenario, Scene, SubtitleSettings, TTSSettings, YouTubeSettings

__all__ = [
    "IMediaProvider",
    "ISubtitleBuilder",
    "ITTSEngine",
    "IThumbnailBuilder",
    "IUploader",
    "IVideoEditor",
    "MediaCandidate",
    "MediaCredit",
    "ScenePlan",
    "SubtitleCue",
    "TTSResult",
    "UploadResult",
    "WordCue",
]


# --------------------------------------------------------------------------------------
# Data contracts
# --------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class WordCue:
    """A single word with its spoken time range.

    Attributes:
        text: The word as the engine pronounced it.
        start: Seconds from the start of the narration clip.
        end: Seconds from the start of the narration clip.
    """

    text: str
    start: float
    end: float

    @property
    def duration(self) -> float:
        """Length of the word in seconds, never negative."""
        return max(0.0, self.end - self.start)

    def shifted(self, offset: float) -> WordCue:
        """Return a copy moved along the timeline.

        Args:
            offset: Seconds to add to both endpoints.

        Returns:
            A new :class:`WordCue`.
        """
        return WordCue(text=self.text, start=self.start + offset, end=self.end + offset)


@dataclass(frozen=True, slots=True)
class SubtitleCue:
    """A displayable subtitle, already wrapped to its final line layout.

    Attributes:
        index: 1-based cue number as it appears in the SRT file.
        start: Display start time in seconds.
        end: Display end time in seconds.
        text: Cue text, with ``\\n`` separating lines.
    """

    index: int
    start: float
    end: float
    text: str

    @property
    def duration(self) -> float:
        """Time the cue stays on screen, in seconds."""
        return max(0.0, self.end - self.start)

    @property
    def lines(self) -> list[str]:
        """The cue split into its individual display lines."""
        return self.text.split("\n")

    def shifted(self, offset: float) -> SubtitleCue:
        """Return a copy moved along the timeline.

        Args:
            offset: Seconds to add to both endpoints.

        Returns:
            A new :class:`SubtitleCue` with the same index and text.
        """
        return SubtitleCue(
            index=self.index,
            start=self.start + offset,
            end=self.end + offset,
            text=self.text,
        )

    def renumbered(self, index: int) -> SubtitleCue:
        """Return a copy with a new cue number.

        Args:
            index: The new 1-based index.

        Returns:
            A new :class:`SubtitleCue`.
        """
        return SubtitleCue(index=index, start=self.start, end=self.end, text=self.text)


@dataclass(frozen=True, slots=True)
class TTSResult:
    """Everything one narration synthesis produced.

    Attributes:
        audio_path: Path to the written MP3.
        duration: Measured audio duration in seconds.
        word_cues: Word-level timings, empty when the engine reported no boundaries.
        voice: The voice actually used, recorded for the manifest.
        cached: Whether this result came from the cache instead of the network.
    """

    audio_path: Path
    duration: float
    word_cues: list[WordCue] = field(default_factory=list)
    voice: str = ""
    cached: bool = False


@dataclass(frozen=True, slots=True)
class MediaCredit:
    """Attribution for one piece of stock footage.

    Attributes:
        provider: Provider name, for example ``pexels``.
        author_name: The contributor's display name.
        author_url: Link to the contributor's profile.
        page_url: Link to the media's own page.
    """

    provider: str
    author_name: str
    author_url: str
    page_url: str

    def as_line(self, template: str) -> str:
        """Render this credit into a description line.

        Args:
            template: A format string accepting ``provider``, ``author`` and ``page_url``.

        Returns:
            The formatted attribution line.
        """
        return template.format(
            provider=self.provider.capitalize(),
            author=self.author_name,
            page_url=self.page_url,
        )

    def key(self) -> tuple[str, str]:
        """Return a deduplication key, so one contributor is credited once.

        Returns:
            A ``(provider, author_name)`` tuple.
        """
        return (self.provider, self.author_name)


@dataclass(frozen=True, slots=True)
class MediaCandidate:
    """One downloadable stock clip returned by a provider search.

    Attributes:
        provider: Provider name, for example ``pexels``.
        media_id: Provider-scoped identifier, used for run-wide deduplication.
        width: Native width in pixels.
        height: Native height in pixels.
        fps: Native frame rate, ``0.0`` when the provider does not report one.
        duration: Clip length in seconds.
        download_url: Direct link to the media file.
        author_name: Contributor's display name.
        author_url: Contributor's profile link.
        page_url: The clip's page on the provider's site.
        file_type: MIME type reported by the provider.
        quality: Provider quality label, for example ``hd``.
    """

    provider: str
    media_id: str
    width: int
    height: int
    fps: float
    duration: float
    download_url: str
    author_name: str
    author_url: str
    page_url: str
    file_type: str = "video/mp4"
    quality: str = ""

    @property
    def aspect(self) -> float:
        """Width-to-height ratio, ``0.0`` for a degenerate frame."""
        return self.width / self.height if self.height else 0.0

    @property
    def pixels(self) -> int:
        """Total pixel count, used as a resolution tie-breaker."""
        return self.width * self.height

    @property
    def dedup_key(self) -> str:
        """Run-scoped identity, so the same clip is never used twice in one video."""
        return f"{self.provider}:{self.media_id}"

    def credit(self) -> MediaCredit:
        """Build the attribution record for this clip.

        Returns:
            A :class:`MediaCredit` naming the contributor.
        """
        return MediaCredit(
            provider=self.provider,
            author_name=self.author_name,
            author_url=self.author_url,
            page_url=self.page_url,
        )


@dataclass(frozen=True, slots=True)
class ScenePlan:
    """Everything the editor needs to render one scene, resolved and ready.

    The plan is built by the orchestrator so the editor performs no lookups of its own and can
    be unit-tested with synthetic inputs.

    Attributes:
        scene: The scenario scene this plan renders.
        audio_path: Narration audio for the scene.
        audio_duration: Measured narration length in seconds.
        media_paths: Source clips, in the order they should appear.
        subtitle_cues: Cues relative to the scene's own timeline, already wrapped.
        target_resolution: Exact output frame size.
        fps: Output frame rate.
        scene_gap_seconds: Silence appended after the narration.
        subtitles: Subtitle appearance settings.
        font_path: The resolved font file for burn-in.
        output_path: Where the rendered scene is written.
        credits: Attribution for every source clip used.
    """

    scene: Scene
    audio_path: Path
    audio_duration: float
    media_paths: list[Path]
    subtitle_cues: list[SubtitleCue]
    target_resolution: tuple[int, int]
    fps: int
    scene_gap_seconds: float
    subtitles: SubtitleSettings
    font_path: Path | None
    output_path: Path
    credits: list[MediaCredit] = field(default_factory=list)

    @property
    def total_duration(self) -> float:
        """Narration length plus the trailing gap."""
        return self.audio_duration + self.scene_gap_seconds

    @property
    def width(self) -> int:
        """Output frame width."""
        return self.target_resolution[0]

    @property
    def height(self) -> int:
        """Output frame height."""
        return self.target_resolution[1]

    @property
    def burn_subtitles(self) -> bool:
        """Whether captions should be composited into the frame for this scene."""
        return bool(
            self.subtitles.enabled
            and self.subtitles.burn_in
            and self.subtitle_cues
            and self.font_path is not None
        )


@dataclass(frozen=True, slots=True)
class UploadResult:
    """The outcome of a successful YouTube upload.

    Attributes:
        video_id: The new video's id.
        url: Public watch URL.
        privacy_status: Privacy the API actually applied, which can differ from the request
            while the OAuth app is unverified.
        thumbnail_set: Whether a custom thumbnail was accepted.
        playlist_id: Playlist the video was added to, when requested.
        caption_uploaded: Whether an SRT caption track was attached.
    """

    video_id: str
    url: str
    privacy_status: str
    thumbnail_set: bool = False
    playlist_id: str | None = None
    caption_uploaded: bool = False


# --------------------------------------------------------------------------------------
# Interfaces
# --------------------------------------------------------------------------------------


class ITTSEngine(ABC):
    """Turns narration text into audio plus word-level timings."""

    @abstractmethod
    async def synthesize(self, text: str, out_path: Path, tts: TTSSettings) -> TTSResult:
        """Synthesize narration audio.

        Args:
            text: The narration to speak.
            out_path: Destination MP3 path.
            tts: Voice and prosody settings.

        Returns:
            The written audio, its measured duration and any word timings.

        Raises:
            TTSError: If synthesis fails or produces empty audio.
        """

    @abstractmethod
    async def list_voices(self, locale: str | None = None) -> list[dict[str, Any]]:
        """List the voices the engine offers.

        Args:
            locale: Optional locale filter such as ``"tr-TR"``. Matching is case-insensitive
                and also accepts a bare language code such as ``"tr"``.

        Returns:
            Voice descriptors as returned by the engine.

        Raises:
            TTSError: If the voice list cannot be retrieved.
        """


class IMediaProvider(ABC):
    """Searches for and downloads stock footage."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The provider's short name, used in logs and attribution."""

    @abstractmethod
    def search(
        self,
        query: str,
        orientation: str,
        min_duration: float,
        limit: int,
    ) -> list[MediaCandidate]:
        """Search for clips matching a query.

        Args:
            query: Search phrase, in English for best stock-library results.
            orientation: ``portrait``, ``landscape`` or ``square``.
            min_duration: Shortest acceptable clip length in seconds.
            limit: Maximum number of candidates to return.

        Returns:
            Candidates ordered best-first, possibly empty.

        Raises:
            MediaProviderError: If the provider returns an unrecoverable error.
        """

    @abstractmethod
    def download(self, candidate: MediaCandidate, dest: Path) -> Path:
        """Download a candidate to disk.

        Args:
            candidate: The clip to fetch.
            dest: Destination file path.

        Returns:
            The path to the downloaded file, which may be a cache hit rather than ``dest``.

        Raises:
            MediaDownloadError: If the download fails or arrives truncated.
        """


class ISubtitleBuilder(ABC):
    """Groups word timings into displayable cues and writes SRT files."""

    @abstractmethod
    def build(
        self,
        cues: list[WordCue],
        settings: SubtitleSettings,
        offset: float = 0.0,
    ) -> list[SubtitleCue]:
        """Group word cues into subtitle cues.

        Args:
            cues: Word-level timings from the TTS engine.
            settings: Line-length and layout constraints.
            offset: Seconds to add to every timestamp, used to place a scene's cues on the
                whole-video timeline.

        Returns:
            Non-overlapping cues with monotonically increasing timestamps.
        """

    @abstractmethod
    def write_srt(self, cues: list[SubtitleCue], out_path: Path) -> Path:
        """Write cues to a UTF-8 SRT file without a byte-order mark.

        Args:
            cues: Cues to serialise.
            out_path: Destination ``.srt`` path.

        Returns:
            The written path.

        Raises:
            SubtitleError: If the file cannot be written.
        """


class IVideoEditor(ABC):
    """Composes scenes and assembles the finished video."""

    @abstractmethod
    def build_scene(self, plan: ScenePlan) -> Path:
        """Render one scene to its own video file.

        Rendering per scene is what makes a run resumable: a crash during assembly never
        forces the completed scenes to be rebuilt.

        Args:
            plan: The fully resolved scene plan.

        Returns:
            Path to the rendered scene file.

        Raises:
            RenderError: If composition or encoding fails.
        """

    @abstractmethod
    def assemble(self, scene_paths: list[Path], scenario: Scenario, out_path: Path) -> Path:
        """Concatenate rendered scenes into the final video.

        Args:
            scene_paths: Scene files in playback order.
            scenario: The project, for crossfade, music and encoder settings.
            out_path: Destination MP4 path.

        Returns:
            The written path.

        Raises:
            RenderError: If assembly or encoding fails, or the result exceeds
                ``video.max_duration_seconds``.
        """


class IThumbnailBuilder(ABC):
    """Generates a video thumbnail."""

    @abstractmethod
    def build(self, video_path: Path, title: str, out_path: Path) -> Path:
        """Create a thumbnail from a frame of the finished video.

        Args:
            video_path: The rendered video to sample.
            title: Text to overlay.
            out_path: Destination JPEG path.

        Returns:
            The written path.

        Raises:
            RenderError: If the frame cannot be extracted or the image cannot be written.
        """


class IUploader(ABC):
    """Publishes the finished video."""

    @abstractmethod
    def authenticate(self) -> None:
        """Establish credentials, running an interactive consent flow if required.

        Raises:
            UploadAuthError: If credentials are missing or cannot be refreshed.
        """

    @abstractmethod
    def upload(
        self,
        video_path: Path,
        meta: YouTubeSettings,
        thumbnail: Path | None,
    ) -> UploadResult:
        """Upload a video and apply its metadata.

        Args:
            video_path: The MP4 to publish.
            meta: Title, description, tags and privacy settings.
            thumbnail: Optional custom thumbnail.

        Returns:
            The new video's id, URL and applied privacy status.

        Raises:
            UploadError: If the upload fails.
            UploadQuotaError: If the daily API quota is exhausted.
        """
