"""Dependency-injection wiring, orchestration flow and TTS behaviour.

The architectural guarantee this project makes is that ``modules.pipeline`` depends only on
abstractions. The first tests below enforce that by parsing the orchestrator's own AST, so the
rule cannot rot as the code changes.
"""

from __future__ import annotations

import ast
import asyncio
import inspect
from pathlib import Path
from typing import Any

import pytest

from config.constants import PROJECT_ROOT
from config.settings import Settings
from models.scenario import Scenario, SubtitleSettings, TTSSettings, YouTubeSettings
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
from modules.pipeline import PipelineOptions, RunManifest, VideoPipeline
from modules.tts import EdgeTTSEngine, attach_punctuation, normalize_narration, year_to_turkish
from modules.uploader import build_description
from utils.exceptions import TTSError

PIPELINE_SOURCE = PROJECT_ROOT / "modules" / "pipeline.py"

FORBIDDEN_CONCRETE_NAMES = {
    "EdgeTTSEngine",
    "PexelsVideoProvider",
    "PexelsPhotoProvider",
    "PixabayVideoProvider",
    "PixabayPhotoProvider",
    "CompositeMediaProvider",
    "MoviePyEditor",
    "PillowThumbnailBuilder",
    "YouTubeUploader",
    "SrtSubtitleBuilder",
    "MediaCache",
}

FORBIDDEN_CONCRETE_MODULES = {
    "modules.tts",
    "modules.video_fetcher",
    "modules.photo_fetcher",
    "modules.editor",
    "modules.thumbnail",
    "modules.uploader",
    "modules.subtitle",
    "modules.media_cache",
    "modules.story_generator",
}


# --------------------------------------------------------------------------------------
# Architectural guarantees
# --------------------------------------------------------------------------------------


def _pipeline_imports() -> list[tuple[str, str]]:
    """Parse every import in ``pipeline.py``.

    Returns:
        ``(module, imported_name)`` pairs for both import forms.
    """
    tree = ast.parse(PIPELINE_SOURCE.read_text(encoding="utf-8"))
    found: list[tuple[str, str]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.append((alias.name, alias.name))
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                found.append((node.module, alias.name))

    return found


def test_pipeline_imports_no_concrete_implementation() -> None:
    """The orchestrator must not name a single concrete collaborator."""
    offenders = [
        f"{module}.{name}"
        for module, name in _pipeline_imports()
        if name in FORBIDDEN_CONCRETE_NAMES or module in FORBIDDEN_CONCRETE_MODULES
    ]

    assert not offenders, (
        "modules/pipeline.py must depend only on interfaces, but it imports: "
        + ", ".join(offenders)
    )


def test_pipeline_never_instantiates_a_provider() -> None:
    """No concrete class is constructed anywhere in the orchestrator's body."""
    tree = ast.parse(PIPELINE_SOURCE.read_text(encoding="utf-8"))
    constructed = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert not (constructed & FORBIDDEN_CONCRETE_NAMES)


def test_pipeline_constructor_accepts_only_interfaces() -> None:
    """Every collaborator parameter is annotated with an abstract type."""
    signature = inspect.signature(VideoPipeline.__init__)
    expected = {
        "tts_engine": ITTSEngine,
        "media_provider": IMediaProvider,
        "subtitle_builder": ISubtitleBuilder,
        "video_editor": IVideoEditor,
        "thumbnail_builder": IThumbnailBuilder,
    }

    for name, interface in expected.items():
        assert name in signature.parameters, f"{name} is not injected"
        assert interface.__name__ in str(signature.parameters[name].annotation)

    assert "IUploader" in str(signature.parameters["uploader"].annotation)


def test_all_collaborators_are_keyword_only() -> None:
    """Keyword-only injection stops callers from silently swapping two collaborators."""
    signature = inspect.signature(VideoPipeline.__init__)

    for name, parameter in signature.parameters.items():
        if name == "self":
            continue
        assert parameter.kind is inspect.Parameter.KEYWORD_ONLY


def test_interfaces_are_abstract() -> None:
    """None of the interfaces can be instantiated directly."""
    for interface in (
        ITTSEngine,
        IMediaProvider,
        ISubtitleBuilder,
        IVideoEditor,
        IThumbnailBuilder,
        IUploader,
    ):
        with pytest.raises(TypeError):
            interface()  # type: ignore[abstract]


# --------------------------------------------------------------------------------------
# Fakes
# --------------------------------------------------------------------------------------


class FakeTTS(ITTSEngine):
    """Writes a plausible MP3-sized placeholder and returns fixed word timings."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    async def synthesize(self, text: str, out_path: Path, tts: TTSSettings) -> TTSResult:
        self.calls.append(text)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(b"\x00" * 2048)
        words = text.split()
        cues = [
            WordCue(text=word, start=index * 0.4, end=index * 0.4 + 0.4)
            for index, word in enumerate(words)
        ]
        return TTSResult(
            audio_path=out_path,
            duration=max(1.0, len(words) * 0.4),
            word_cues=cues,
            voice=tts.voice,
        )

    async def list_voices(self, locale: str | None = None) -> list[dict[str, Any]]:
        return [{"ShortName": "tr-TR-AhmetNeural", "Locale": "tr-TR"}]


class FakeProvider(IMediaProvider):
    """Returns one candidate per query and writes placeholder files on download."""

    def __init__(self) -> None:
        self.searches: list[str] = []
        self.downloads: list[Path] = []
        self._counter = 0

    @property
    def name(self) -> str:
        return "fake"

    def search(
        self, query: str, orientation: str, min_duration: float, limit: int
    ) -> list[MediaCandidate]:
        self.searches.append(query)
        batch: list[MediaCandidate] = []
        for _ in range(max(1, limit)):
            self._counter += 1
            batch.append(
                MediaCandidate(
                    provider="fake",
                    media_id=str(self._counter),
                    width=1080,
                    height=1920,
                    fps=30.0,
                    duration=12.0,
                    download_url=f"https://fake.invalid/{self._counter}.mp4",
                    author_name=f"Author {self._counter}",
                    author_url="https://fake.invalid/author",
                    page_url=f"https://fake.invalid/video/{self._counter}",
                )
            )
        return batch

    def download(self, candidate: MediaCandidate, dest: Path) -> Path:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b"video bytes")
        self.downloads.append(dest)
        return dest


class FakeEditor(IVideoEditor):
    """Records the plans it receives and writes placeholder scene files."""

    def __init__(self) -> None:
        self.plans: list[ScenePlan] = []
        self.assembled: list[Path] = []

    def build_scene(self, plan: ScenePlan) -> Path:
        self.plans.append(plan)
        plan.output_path.parent.mkdir(parents=True, exist_ok=True)
        plan.output_path.write_bytes(b"scene")
        return plan.output_path

    def assemble(self, scene_paths: list[Path], scenario: Scenario, out_path: Path) -> Path:
        self.assembled = list(scene_paths)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(b"final video")
        return out_path

    def build_photo_story(
        self,
        photo_paths: list[Path],
        audio_paths: list[Path],
        audio_durations: list[float],
        subtitle_cues: object,
        scenario: Scenario,
        font_path: Path | None,
        out_path: Path,
    ) -> Path:
        del audio_paths, audio_durations, subtitle_cues, scenario, font_path
        self.assembled = list(photo_paths)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(b"story video")
        return out_path


class FakeThumbnail(IThumbnailBuilder):
    """Writes a placeholder thumbnail."""

    def build(self, video_path: Path, title: str, out_path: Path) -> Path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(b"jpeg")
        return out_path


class FakeUploader(IUploader):
    """Records upload calls without touching the network."""

    def __init__(self) -> None:
        self.authenticated = False
        self.uploads: list[Path] = []

    def authenticate(self) -> None:
        self.authenticated = True

    def upload(
        self, video_path: Path, meta: YouTubeSettings, thumbnail: Path | None
    ) -> UploadResult:
        self.uploads.append(video_path)
        return UploadResult(
            video_id="abc123",
            url="https://www.youtube.com/watch?v=abc123",
            privacy_status=meta.privacy_status,
        )


def _scenario(**overrides: Any) -> Scenario:
    """Build a small scenario suitable for wiring tests."""
    payload: dict[str, Any] = {
        "project_id": "wiring-test",
        "video": {"orientation": "portrait", "fps": 30, "crossfade_seconds": 0.0},
        "subtitles": {"enabled": True, "burn_in": False},
        "youtube": {"title": "Wiring Test", "upload_enabled": False},
        "scenes": [
            {"id": 1, "narration": "Birinci sahne metni.", "search_terms": ["ocean"]},
            {"id": 2, "narration": "Ikinci sahne metni.", "search_terms": ["forest"]},
        ],
    }
    payload.update(overrides)
    return Scenario.model_validate(payload)


def _pipeline(
    settings: Settings,
    scenario: Scenario | None = None,
    options: PipelineOptions | None = None,
    uploader: IUploader | None = None,
) -> tuple[VideoPipeline, dict[str, Any]]:
    """Build a pipeline wired entirely from fakes.

    Returns:
        The pipeline and a dictionary of the fakes, for assertions.
    """
    from modules.subtitle import SrtSubtitleBuilder

    fakes: dict[str, Any] = {
        "tts": FakeTTS(),
        "media": FakeProvider(),
        "editor": FakeEditor(),
        "thumbnail": FakeThumbnail(),
        "uploader": uploader,
    }

    pipeline = VideoPipeline(
        scenario=scenario or _scenario(),
        settings=settings,
        tts_engine=fakes["tts"],
        media_provider=fakes["media"],
        subtitle_builder=SrtSubtitleBuilder(),
        video_editor=fakes["editor"],
        thumbnail_builder=fakes["thumbnail"],
        uploader=uploader,
        options=options or PipelineOptions(),
    )
    return pipeline, fakes


# --------------------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------------------


def test_full_run_uses_only_injected_collaborators(settings: Settings) -> None:
    """A complete run drives every injected fake and produces a manifest."""
    pipeline, fakes = _pipeline(settings)

    manifest = pipeline.run()

    assert manifest.status == "success"
    assert len(fakes["tts"].calls) == 2
    assert len(fakes["editor"].plans) == 2
    assert len(fakes["editor"].assembled) == 2
    assert manifest.artifacts["video"].endswith("wiring-test.mp4")
    assert manifest.artifacts["thumbnail"].endswith("wiring-test.jpg")


def test_story_run_skips_per_scene_render(settings: Settings) -> None:
    """A story scenario downloads stills and calls build_photo_story, not build_scene."""
    scenario = _scenario(
        video={
            "format": "story",
            "orientation": "landscape",
            "crossfade_seconds": 0.0,
            "max_duration_seconds": 1500,
        },
        subtitles={"enabled": True, "burn_in": False, "accent_color": "#FFD34F"},
    )
    pipeline, fakes = _pipeline(settings, scenario=scenario)
    manifest = pipeline.run()

    assert manifest.status == "success"
    assert fakes["editor"].plans == []
    assert len(fakes["editor"].assembled) == 20
    assert manifest.artifacts["video"].endswith("wiring-test.mp4")


def test_paint_run_skips_stock_search(settings: Settings) -> None:
    """Paint stills come from the storyboard folder; Pexels is never queried."""
    board = settings.storyboard_dir() / "wiring-test"
    board.mkdir(parents=True, exist_ok=True)
    (board / "01-light-switch.png").write_bytes(b"png-bytes")
    (board / "02-dark-sky.png").write_bytes(b"png-bytes")
    scenario = _scenario(
        video={
            "format": "paint",
            "orientation": "landscape",
            "crossfade_seconds": 0.0,
            "max_duration_seconds": 1500,
            "story_visual": {"photo_count": 2, "opening_photo_count": 1},
            "visual_beats": [
                {
                    "slug": "light-switch",
                    "prompt": "Stickman flips a yellow light switch on a white page.",
                    "covers": "You flip a switch.",
                },
                {
                    "slug": "dark-sky",
                    "prompt": "Stickman stands under a black sky with three stars.",
                    "covers": "The world goes dark.",
                },
            ],
        },
        subtitles={"enabled": True, "burn_in": False, "accent_color": "#FFD34F"},
    )
    pipeline, fakes = _pipeline(settings, scenario=scenario)
    manifest = pipeline.run()

    assert manifest.status == "success"
    assert fakes["media"].searches == []
    assert fakes["editor"].plans == []
    assert len(fakes["editor"].assembled) == 2
    studio = Path(manifest.artifacts["studio"])
    assert studio.is_file()
    text = studio.read_text(encoding="utf-8")
    assert "Badly Drawn Why" in text
    assert "Chapters:" in text
    assert "0:00" in text


def test_manifest_is_written_to_disk(settings: Settings) -> None:
    """The manifest lands in the final output directory."""
    pipeline, _ = _pipeline(settings)
    pipeline.run()

    path = settings.final_dir() / "wiring-test_manifest.json"
    assert path.is_file()

    import json

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["status"] == "success"
    assert payload["video"]["resolution"] == [1080, 1920]
    assert len(payload["scenes"]) == 2


def test_manifest_is_written_even_when_a_stage_fails(settings: Settings) -> None:
    """A crash still leaves a diagnosable record behind."""

    class ExplodingEditor(FakeEditor):
        def build_scene(self, plan: ScenePlan) -> Path:
            from utils.exceptions import RenderError

            raise RenderError("scene render exploded")

    from modules.subtitle import SrtSubtitleBuilder
    from utils.exceptions import RenderError

    pipeline = VideoPipeline(
        scenario=_scenario(),
        settings=settings,
        tts_engine=FakeTTS(),
        media_provider=FakeProvider(),
        subtitle_builder=SrtSubtitleBuilder(),
        video_editor=ExplodingEditor(),
        thumbnail_builder=FakeThumbnail(),
        options=PipelineOptions(),
    )

    with pytest.raises(RenderError):
        pipeline.run()

    import json

    payload = json.loads(
        (settings.final_dir() / "wiring-test_manifest.json").read_text(encoding="utf-8")
    )
    assert payload["status"] == "failed"
    assert payload["failed_stage"] == "scenes"
    assert "exploded" in payload["error"]
    assert payload["traceback_digest"]


def test_dry_run_touches_nothing(settings: Settings) -> None:
    """A dry run plans only: no synthesis, no search, no render."""
    pipeline, fakes = _pipeline(settings, options=PipelineOptions(dry_run=True))

    manifest = pipeline.run()

    assert manifest.status == "dry-run"
    assert fakes["tts"].calls == []
    assert fakes["media"].searches == []
    assert fakes["editor"].plans == []


def test_scene_limit_restricts_the_run(settings: Settings) -> None:
    """Only the first N scenes are processed."""
    pipeline, fakes = _pipeline(settings, options=PipelineOptions(scene_limit=1))

    pipeline.run()

    assert len(fakes["tts"].calls) == 1
    assert len(fakes["editor"].plans) == 1


def test_upload_is_skipped_when_disabled_in_the_scenario(settings: Settings) -> None:
    """``upload_enabled`` defaults to false and is honoured."""
    uploader = FakeUploader()
    pipeline, _ = _pipeline(settings, uploader=uploader)

    pipeline.run()

    assert uploader.uploads == []


def test_no_upload_flag_overrides_the_scenario(settings: Settings) -> None:
    """``--no-upload`` wins even when the scenario asks to publish."""
    uploader = FakeUploader()
    scenario = _scenario(
        youtube={"title": "Wiring Test", "upload_enabled": True, "privacy_status": "private"}
    )
    pipeline, _ = _pipeline(
        settings, scenario=scenario, options=PipelineOptions(no_upload=True), uploader=uploader
    )

    pipeline.run()

    assert uploader.uploads == []


def test_upload_runs_when_enabled(settings: Settings) -> None:
    """An enabled private upload proceeds and is recorded in the manifest."""
    uploader = FakeUploader()
    scenario = _scenario(
        youtube={"title": "Wiring Test", "upload_enabled": True, "privacy_status": "private"}
    )
    pipeline, _ = _pipeline(settings, scenario=scenario, uploader=uploader)

    manifest = pipeline.run()

    assert uploader.authenticated is True
    assert len(uploader.uploads) == 1
    assert manifest.youtube_video_id == "abc123"
    assert manifest.youtube_privacy_status == "private"


def test_public_upload_requires_confirmation(settings: Settings) -> None:
    """A public upload without confirmation is skipped rather than silently published."""
    uploader = FakeUploader()
    scenario = _scenario(
        youtube={"title": "Wiring Test", "upload_enabled": True, "privacy_status": "public"}
    )
    pipeline, _ = _pipeline(settings, scenario=scenario, uploader=uploader)

    pipeline.run()

    assert uploader.uploads == []


def test_confirmed_public_upload_proceeds(settings: Settings) -> None:
    """With confirmation, the public upload runs."""
    uploader = FakeUploader()
    scenario = _scenario(
        youtube={"title": "Wiring Test", "upload_enabled": True, "privacy_status": "public"}
    )
    pipeline, _ = _pipeline(
        settings,
        scenario=scenario,
        options=PipelineOptions(assume_yes=True),
        uploader=uploader,
    )

    pipeline.run()

    assert len(uploader.uploads) == 1


def test_credits_are_collected_and_deduplicated(settings: Settings) -> None:
    """Each contributor is credited once, no matter how many clips they supplied."""
    pipeline, _ = _pipeline(settings)
    pipeline.run()

    keys = [credit.key() for credit in pipeline.credits]
    assert len(keys) == len(set(keys))
    assert keys


def test_subtitle_sidecar_covers_the_whole_video(settings: Settings) -> None:
    """Per-scene cues are offset onto one continuous timeline."""
    pipeline, _ = _pipeline(settings)
    pipeline.run()

    assert pipeline.subtitle_path is not None
    text = pipeline.subtitle_path.read_text(encoding="utf-8")

    assert text.strip()
    assert "-->" in text
    assert text.strip().split("\n")[0] == "1"


def test_stage_timings_are_recorded(settings: Settings) -> None:
    """Each completed stage records its wall time."""
    pipeline, _ = _pipeline(settings)
    manifest = pipeline.run()

    for stage in ("narration", "subtitles", "footage", "scenes", "assemble"):
        assert stage in manifest.stage_timings


def test_scene_plan_carries_resolved_inputs(settings: Settings) -> None:
    """The editor receives a fully resolved plan and performs no lookups itself."""
    pipeline, fakes = _pipeline(settings)
    pipeline.run()

    plan = fakes["editor"].plans[0]
    assert plan.target_resolution == (1080, 1920)
    assert plan.fps == 30
    assert plan.audio_path.is_file()
    assert plan.media_paths
    assert plan.total_duration == pytest.approx(plan.audio_duration + plan.scene_gap_seconds)


def test_manifest_records_no_secrets(settings: Settings) -> None:
    """The manifest holds paths and credits, never credentials."""
    pipeline, _ = _pipeline(settings)
    manifest = pipeline.run()

    serialised = str(manifest.to_dict()).lower()
    for forbidden in ("api_key", "client_secret", "refresh_token", "authorization"):
        assert forbidden not in serialised


def test_run_manifest_defaults_are_serialisable() -> None:
    """A fresh manifest serialises without any pipeline run."""
    payload = RunManifest(project_id="x", started_at="now").to_dict()

    assert payload["status"] == "running"
    assert payload["youtube"]["video_id"] is None


# --------------------------------------------------------------------------------------
# TTS behaviour, without touching the network
# --------------------------------------------------------------------------------------


def test_normalize_expands_symbols_and_abbreviations() -> None:
    """Symbols and Turkish abbreviations are spoken as words."""
    assert "yüzde" in normalize_narration("Oran %50 arttı")
    assert "ve benzeri" in normalize_narration("elmalar, armutlar vb.")
    assert year_to_turkish(1956) == "bin dokuz yüz elli altı"
    spoken = normalize_narration("1956 yılında McCarthy Dartmouth'ta konuştu")
    assert "bin dokuz yüz elli altı" in spoken
    assert "Mekarti" in spoken
    assert "Dartmut" in spoken


def test_normalize_strips_markdown_and_emoji() -> None:
    """Markup and emoji would otherwise be read aloud."""
    cleaned = normalize_narration("**Kalin** ve _egik_ metin 🎉 [link](https://a.b)")

    assert "*" not in cleaned
    assert "_" not in cleaned
    assert "🎉" not in cleaned
    assert "link" in cleaned


def test_normalize_collapses_whitespace_and_adds_punctuation() -> None:
    """Terminal punctuation stops the voice clipping the final word."""
    assert normalize_narration("  bir   iki   uc  ") == "bir iki uc."
    assert normalize_narration("Zaten var!") == "Zaten var!"


def test_normalize_rejects_unspeakable_text() -> None:
    """Text that reduces to nothing is an error, not silent output."""
    with pytest.raises(TTSError):
        normalize_narration("   ")
    with pytest.raises(TTSError):
        normalize_narration("***")


def test_empty_audio_is_rejected(tmp_path: Path) -> None:
    """A zero-byte MP3 is the classic silent edge-tts failure and must not pass."""
    engine = EdgeTTSEngine(tmp_path / "tts")

    with pytest.raises(TTSError, match="zero bytes"):
        engine._validate_audio(b"", tmp_path / "scene.mp3")

    with pytest.raises(TTSError, match="too small"):
        engine._validate_audio(b"tiny", tmp_path / "scene.mp3")


def test_word_boundary_parsing_converts_ticks() -> None:
    """edge-tts reports 100-nanosecond ticks, which become seconds."""
    cue = EdgeTTSEngine._parse_word_boundary(
        {"type": "WordBoundary", "text": "merhaba", "offset": 10_000_000, "duration": 5_000_000}
    )

    assert cue is not None
    assert cue.text == "merhaba"
    assert cue.start == pytest.approx(1.0)
    assert cue.end == pytest.approx(1.5)


def test_malformed_word_boundary_is_ignored() -> None:
    """A boundary event with no text or timing is dropped rather than crashing."""
    assert EdgeTTSEngine._parse_word_boundary({"type": "WordBoundary", "text": ""}) is None
    assert EdgeTTSEngine._parse_word_boundary({"type": "WordBoundary", "text": "x"}) is None


def test_attach_punctuation_restores_a_period() -> None:
    """Edge TTS strips the stop; grouping needs it back on the cue."""
    spoken = normalize_narration("Hello.", language="en")
    cues = attach_punctuation(spoken, [WordCue(text="Hello", start=0.0, end=0.4)])

    assert spoken == "Hello."
    assert cues[0].text == "Hello."
    assert cues[0].start == pytest.approx(0.0)
    assert cues[0].end == pytest.approx(0.4)


def test_attach_punctuation_restores_two_sentence_stops() -> None:
    """Each spoken token keeps the punctuation that followed it in the essay."""
    spoken = normalize_narration("Soup. Beans.", language="en")
    cues = attach_punctuation(
        spoken,
        [
            WordCue(text="Soup", start=0.0, end=0.3),
            WordCue(text="Beans", start=0.3, end=0.6),
        ],
    )

    assert [cue.text for cue in cues] == ["Soup.", "Beans."]


def test_attach_punctuation_leaves_cues_unchanged_on_mismatch() -> None:
    """A word the narration does not contain is not rewritten."""
    cues = attach_punctuation("Hello world.", [WordCue(text="zzz", start=0.0, end=0.2)])

    assert cues[0].text == "zzz"


def test_synthesize_attaches_narration_punctuation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Fresh synthesis and a cache hit both restore periods onto word cues."""
    engine = EdgeTTSEngine(tmp_path / "tts")
    settings = TTSSettings(language="en")
    calls = {"count": 0}

    async def fake_stream(text: str, tts: TTSSettings) -> tuple[bytes, list[WordCue]]:
        calls["count"] += 1
        return b"\x00" * 4096, [WordCue(text="Hello", start=0.0, end=0.4)]

    monkeypatch.setattr(engine, "_synthesize_with_retry", fake_stream)
    monkeypatch.setattr("modules.tts.probe_duration", lambda _path: 0.5)

    out_path = tmp_path / "scene_001.mp3"
    first = asyncio.run(engine.synthesize("Hello.", out_path, settings))
    second = asyncio.run(engine.synthesize("Hello.", out_path, settings))

    assert calls["count"] == 1
    assert first.word_cues[0].text == "Hello."
    assert second.cached is True
    assert second.word_cues[0].text == "Hello."


def test_tts_cache_round_trip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A second synthesis of the same text is served from cache without a network call."""
    engine = EdgeTTSEngine(tmp_path / "tts")
    settings = TTSSettings()
    calls = {"count": 0}

    async def fake_stream(text: str, tts: TTSSettings) -> tuple[bytes, list[WordCue]]:
        calls["count"] += 1
        return b"\x00" * 4096, [WordCue(text="merhaba", start=0.0, end=0.5)]

    monkeypatch.setattr(engine, "_synthesize_with_retry", fake_stream)
    monkeypatch.setattr("modules.tts.probe_duration", lambda _path: 1.25)

    out_path = tmp_path / "scene_001.mp3"
    first = asyncio.run(engine.synthesize("Merhaba dunya", out_path, settings))
    second = asyncio.run(engine.synthesize("Merhaba dunya", out_path, settings))

    assert calls["count"] == 1
    assert first.cached is False
    assert second.cached is True
    assert second.duration == pytest.approx(1.25)
    assert [cue.text for cue in second.word_cues] == ["merhaba"]


def test_force_bypasses_the_tts_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """``--force`` re-synthesizes even when a cache entry exists."""
    settings = TTSSettings()
    calls = {"count": 0}

    async def fake_stream(text: str, tts: TTSSettings) -> tuple[bytes, list[WordCue]]:
        calls["count"] += 1
        return b"\x00" * 4096, []

    cache_dir = tmp_path / "tts"
    monkeypatch.setattr("modules.tts.probe_duration", lambda _path: 1.0)

    warm = EdgeTTSEngine(cache_dir)
    monkeypatch.setattr(warm, "_synthesize_with_retry", fake_stream)
    asyncio.run(warm.synthesize("Merhaba", tmp_path / "a.mp3", settings))

    forced = EdgeTTSEngine(cache_dir, force=True)
    monkeypatch.setattr(forced, "_synthesize_with_retry", fake_stream)
    asyncio.run(forced.synthesize("Merhaba", tmp_path / "a.mp3", settings))

    assert calls["count"] == 2


# --------------------------------------------------------------------------------------
# Attribution
# --------------------------------------------------------------------------------------


def _credit(author: str) -> MediaCredit:
    """Build a credit for attribution tests."""
    return MediaCredit(
        provider="pexels",
        author_name=author,
        author_url=f"https://pexels.com/@{author}",
        page_url=f"https://pexels.com/video/{author}",
    )


def test_attribution_is_appended_and_deduplicated() -> None:
    """Each contributor is credited exactly once."""
    description = build_description(
        "My video.",
        [_credit("Ada"), _credit("Ada"), _credit("Grace")],
        synthetic_disclosure=False,
    )

    assert description.startswith("My video.")
    assert description.count("Ada") == 2  # once in the name, once in the profile URL
    assert "Grace" in description


def test_synthetic_disclosure_is_added_when_requested() -> None:
    """The AI-audio disclosure is appended when the scenario asks for it."""
    description = build_description("Body.", [], synthetic_disclosure=True)

    assert "synthetic" in description.lower()


def test_description_without_credits_or_disclosure_is_untouched() -> None:
    """Nothing is appended when there is nothing to disclose."""
    assert build_description("Body.", [], synthetic_disclosure=False) == "Body."


def test_attribution_survives_truncation() -> None:
    """When the limit bites, the legally required block is kept and the body is trimmed."""
    description = build_description(
        "x" * 4990, [_credit("Ada")], synthetic_disclosure=True, max_chars=5000
    )

    assert len(description) <= 5000
    assert "Ada" in description
    assert "synthetic" in description.lower()


def test_description_never_exceeds_the_limit() -> None:
    """Even an absurd number of credits stays within the API limit."""
    credits = [_credit(f"Author{index}") for index in range(400)]
    description = build_description("Body.", credits, synthetic_disclosure=True, max_chars=5000)

    assert len(description) <= 5000


# --------------------------------------------------------------------------------------
# Interface data contracts
# --------------------------------------------------------------------------------------


def test_subtitle_cue_helpers() -> None:
    """Cue helpers shift, renumber and split as documented."""
    cue = SubtitleCue(index=1, start=1.0, end=2.0, text="first\nsecond")

    assert cue.duration == pytest.approx(1.0)
    assert cue.lines == ["first", "second"]
    assert cue.shifted(5.0).start == pytest.approx(6.0)
    assert cue.renumbered(9).index == 9


def test_media_candidate_helpers() -> None:
    """Candidate helpers expose the values used for scoring and deduplication."""
    candidate = MediaCandidate(
        provider="pexels",
        media_id="42",
        width=1080,
        height=1920,
        fps=30.0,
        duration=8.0,
        download_url="https://x.invalid/a.mp4",
        author_name="Ada",
        author_url="https://x.invalid/@ada",
        page_url="https://x.invalid/video/42",
    )

    assert candidate.aspect == pytest.approx(1080 / 1920)
    assert candidate.pixels == 1080 * 1920
    assert candidate.dedup_key == "pexels:42"
    assert candidate.credit().author_name == "Ada"


def test_word_cue_shift_preserves_duration() -> None:
    """Shifting a word cue moves it without changing its length."""
    cue = WordCue(text="merhaba", start=1.0, end=1.5).shifted(2.0)

    assert cue.start == pytest.approx(3.0)
    assert cue.duration == pytest.approx(0.5)


def test_scene_plan_burn_flag_requires_a_font() -> None:
    """Burn-in is skipped when no font could be resolved."""
    scenario = _scenario()
    plan = ScenePlan(
        scene=scenario.scenes[0],
        audio_path=Path("a.mp3"),
        audio_duration=2.0,
        media_paths=[Path("clip.mp4")],
        subtitle_cues=[SubtitleCue(index=1, start=0.0, end=1.0, text="hi")],
        target_resolution=(1080, 1920),
        fps=30,
        scene_gap_seconds=0.3,
        subtitles=SubtitleSettings(enabled=True, burn_in=False),
        font_path=None,
        output_path=Path("scene.mp4"),
    )

    assert plan.burn_subtitles is False
    assert plan.total_duration == pytest.approx(2.3)
    assert plan.width == 1080
