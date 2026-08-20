"""Pipeline modules: interfaces, concrete implementations and the orchestrator.

``modules.pipeline`` deliberately imports none of the concrete classes re-exported here. It
depends on the abstractions in ``modules.interfaces`` alone, and the composition root in
``main.py`` decides which implementations to inject.
"""

from modules.editor import MoviePyEditor
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
    WordCue,
)
from modules.media_cache import MediaCache
from modules.pipeline import PipelineOptions, RunManifest, VideoPipeline
from modules.scenario_loader import ScenarioLoader, load_scenario
from modules.subtitle import SrtSubtitleBuilder, format_timestamp, wrap_words
from modules.thumbnail import PillowThumbnailBuilder
from modules.tts import EdgeTTSEngine, normalize_narration
from modules.uploader import YouTubeUploader, build_description
from modules.video_fetcher import (
    CompositeMediaProvider,
    PexelsVideoProvider,
    PixabayVideoProvider,
    build_query_ladder,
    score_candidate,
)

__all__ = [
    "CompositeMediaProvider",
    "EdgeTTSEngine",
    "IMediaProvider",
    "ISubtitleBuilder",
    "ITTSEngine",
    "IThumbnailBuilder",
    "IUploader",
    "IVideoEditor",
    "MediaCache",
    "MediaCandidate",
    "MediaCredit",
    "MoviePyEditor",
    "PexelsVideoProvider",
    "PillowThumbnailBuilder",
    "PipelineOptions",
    "PixabayVideoProvider",
    "RunManifest",
    "ScenarioLoader",
    "ScenePlan",
    "SrtSubtitleBuilder",
    "SubtitleCue",
    "TTSResult",
    "UploadResult",
    "VideoPipeline",
    "WordCue",
    "YouTubeUploader",
    "build_description",
    "build_query_ladder",
    "format_timestamp",
    "load_scenario",
    "normalize_narration",
    "score_candidate",
    "wrap_words",
]
