"""Background video library: reservations, the ledger and frame-accurate cuts."""

from __future__ import annotations

import json
import random
import subprocess
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from config.constants import BACKGROUND_CLIP_MARGIN_SECONDS
from config.settings import Settings
from models.scenario import VideoSettings
from modules.background_library import BackgroundLibrary, cut_with_ffmpeg, free_stretches
from utils.exceptions import ConfigurationError, MediaNotFoundError, RenderError
from utils.media import ffmpeg_executable, probe_duration

EDGE = 5.0


class RecordingCutter:
    """Stands in for ffmpeg: records every cut and writes a small placeholder clip."""

    def __init__(self) -> None:
        self.cuts: list[tuple[str, float, float]] = []

    def __call__(self, source: Path, start: float, length: float, dest: Path) -> None:
        self.cuts.append((source.name, start, length))
        dest.write_bytes(b"clip")


def _library(
    tmp_path: Path,
    videos: dict[str, float],
    *,
    seed: int = 7,
) -> tuple[BackgroundLibrary, RecordingCutter]:
    """Build a library over placeholder files whose durations come from ``videos``."""
    folder = tmp_path / "videos"
    folder.mkdir(exist_ok=True)
    for name in videos:
        (folder / name).write_bytes(b"video")
    cutter = RecordingCutter()

    def probe(path: Path) -> float:
        return videos[path.name]

    library = BackgroundLibrary(
        folder,
        tmp_path / "ledger.json",
        rng=random.Random(seed),
        probe=probe,
        cutter=cutter,
        edge_skip=EDGE,
    )
    return library, cutter


def _ledger(tmp_path: Path) -> dict[str, dict[str, Any]]:
    reservations: dict[str, dict[str, Any]] = json.loads(
        (tmp_path / "ledger.json").read_text(encoding="utf-8")
    )["reservations"]
    return reservations


# --------------------------------------------------------------------------------------
# Free stretches
# --------------------------------------------------------------------------------------


def test_free_stretches_without_reservations_skip_the_edges() -> None:
    assert free_stretches(60.0, [], edge=5.0) == [(5.0, 55.0)]


def test_free_stretches_merge_overlapping_reservations() -> None:
    taken = [(30.0, 40.0), (10.0, 20.0), (15.0, 25.0)]
    assert free_stretches(60.0, taken, edge=5.0) == [(5.0, 10.0), (25.0, 30.0), (40.0, 55.0)]


def test_free_stretches_ignore_reservations_outside_the_usable_part() -> None:
    assert free_stretches(60.0, [(0.0, 3.0), (57.0, 60.0)], edge=5.0) == [(5.0, 55.0)]


def test_a_video_shorter_than_both_edges_has_no_free_stretch() -> None:
    assert free_stretches(8.0, [], edge=5.0) == []


# --------------------------------------------------------------------------------------
# Reservations and cuts
# --------------------------------------------------------------------------------------


def test_scene_clips_follow_each_other_in_one_stretch(tmp_path: Path) -> None:
    """Back to back clips are what make the background look like a single take."""
    library, cutter = _library(tmp_path, {"drive.mp4": 300.0})
    durations = [3.0, 2.5, 4.0]

    cut = library.cut("first-video", durations, tmp_path / "clips")

    assert len(cut.clips) == len(durations)
    starts = [start for _, start, _ in cutter.cuts]
    lengths = [length for _, _, length in cutter.cuts]
    for index in range(len(durations) - 1):
        assert starts[index + 1] == pytest.approx(starts[index] + durations[index])
    assert lengths == pytest.approx([d + BACKGROUND_CLIP_MARGIN_SECONDS for d in durations])
    assert starts[0] == pytest.approx(cut.start)
    assert cut.start >= EDGE
    assert cut.end <= 300.0 - EDGE
    assert cut.end - cut.start == pytest.approx(sum(durations) + BACKGROUND_CLIP_MARGIN_SECONDS)


def test_the_reservation_is_recorded_in_the_ledger(tmp_path: Path) -> None:
    library, _ = _library(tmp_path, {"drive.mp4": 300.0})

    cut = library.cut("first-video", [3.0, 4.0], tmp_path / "clips")

    entry = _ledger(tmp_path)["first-video"]
    assert entry["file"] == "drive.mp4"
    assert entry["start"] == pytest.approx(cut.start)
    assert entry["end"] == pytest.approx(cut.end)


def test_the_same_project_gets_the_same_stretch_and_reuses_its_clips(tmp_path: Path) -> None:
    """Re-running a video must not move its footage or cut the clips again."""
    library, cutter = _library(tmp_path, {"drive.mp4": 300.0})
    first = library.cut("first-video", [3.0, 4.0], tmp_path / "clips")

    again, again_cutter = _library(tmp_path, {"drive.mp4": 300.0}, seed=99)
    second = again.cut("first-video", [3.0, 4.0], tmp_path / "clips")

    assert second.start == pytest.approx(first.start)
    assert second.clips == first.clips
    assert len(cutter.cuts) == 2
    assert again_cutter.cuts == []


def test_different_projects_never_share_footage(tmp_path: Path) -> None:
    library, _ = _library(tmp_path, {"drive.mp4": 60.0})

    first = library.cut("first-video", [10.0, 10.0], tmp_path / "clips")
    second = library.cut("second-video", [10.0, 10.0], tmp_path / "clips")

    assert first.end <= second.start or second.end <= first.start


def test_a_full_library_says_how_much_is_left(tmp_path: Path) -> None:
    """50 usable seconds hold two 20 s videos; the third cannot fit anywhere."""
    library, _ = _library(tmp_path, {"drive.mp4": 60.0})
    library.cut("first-video", [20.0], tmp_path / "clips")
    library.cut("second-video", [20.0], tmp_path / "clips")

    with pytest.raises(MediaNotFoundError, match="longest free stretch") as caught:
        library.cut("third-video", [20.0], tmp_path / "clips")

    assert caught.value.hint is not None
    assert "ledger.json" in caught.value.hint


def test_a_longer_request_moves_the_project_to_a_new_stretch(tmp_path: Path) -> None:
    library, _ = _library(tmp_path, {"drive.mp4": 300.0})
    library.cut("first-video", [5.0], tmp_path / "clips")

    longer = library.cut("first-video", [5.0, 10.0], tmp_path / "clips")

    entry = _ledger(tmp_path)["first-video"]
    assert entry["end"] - entry["start"] == pytest.approx(15.0 + BACKGROUND_CLIP_MARGIN_SECONDS)
    assert entry["start"] == pytest.approx(longer.start)


def test_unreadable_and_non_video_files_are_skipped(tmp_path: Path) -> None:
    folder = tmp_path / "videos"
    folder.mkdir()
    (folder / "broken.mp4").write_bytes(b"x")
    (folder / "good.mp4").write_bytes(b"x")
    (folder / "notes.txt").write_text("not a video", encoding="utf-8")
    probed: list[str] = []

    def probe(path: Path) -> float:
        probed.append(path.name)
        if path.name == "broken.mp4":
            raise RenderError("cannot read")
        return 120.0

    library = BackgroundLibrary(
        folder, tmp_path / "ledger.json", probe=probe, cutter=RecordingCutter()
    )
    cut = library.cut("first-video", [4.0], tmp_path / "clips")

    assert cut.source.name == "good.mp4"
    assert "notes.txt" not in probed


def test_a_missing_folder_is_a_configuration_error(tmp_path: Path) -> None:
    library = BackgroundLibrary(tmp_path / "nowhere", tmp_path / "ledger.json")
    with pytest.raises(ConfigurationError, match="folder not found"):
        library.cut("first-video", [4.0], tmp_path / "clips")


def test_a_folder_without_videos_says_so(tmp_path: Path) -> None:
    library, _ = _library(tmp_path, {})
    with pytest.raises(MediaNotFoundError, match="No playable video"):
        library.cut("first-video", [4.0], tmp_path / "clips")


@pytest.mark.parametrize("durations", [[], [3.0, 0.0], [-1.0]])
def test_empty_or_non_positive_durations_are_rejected(
    tmp_path: Path, durations: list[float]
) -> None:
    library, _ = _library(tmp_path, {"drive.mp4": 300.0})
    with pytest.raises(ValueError, match="positive"):
        library.cut("first-video", durations, tmp_path / "clips")


# --------------------------------------------------------------------------------------
# Ledger robustness
# --------------------------------------------------------------------------------------


def test_an_unreadable_ledger_is_replaced_instead_of_crashing(tmp_path: Path) -> None:
    library, _ = _library(tmp_path, {"drive.mp4": 300.0})
    (tmp_path / "ledger.json").write_text("{not json", encoding="utf-8")

    library.cut("first-video", [4.0], tmp_path / "clips")

    assert "first-video" in _ledger(tmp_path)


def test_malformed_ledger_entries_are_ignored_and_dropped(tmp_path: Path) -> None:
    """A hand-edited ledger cannot point outside the folder or break the arithmetic."""
    library, _ = _library(tmp_path, {"drive.mp4": 60.0})
    ledger = {
        "version": 1,
        "reservations": {
            "kept": {"file": "drive.mp4", "start": 5.0, "end": 25.0},
            "escape": {"file": "../../secret.mp4", "start": 30.0, "end": 40.0},
            "backwards": {"file": "drive.mp4", "start": 50.0, "end": 45.0},
            "boolean": {"file": "drive.mp4", "start": True, "end": 40.0},
            "missing": {"file": "drive.mp4"},
            "not-a-dict": "drive.mp4",
        },
    }
    (tmp_path / "ledger.json").write_text(json.dumps(ledger), encoding="utf-8")

    cut = library.cut("first-video", [20.0], tmp_path / "clips")

    assert cut.start >= 25.0
    assert set(_ledger(tmp_path)) == {"kept", "first-video"}


def test_every_folder_gets_its_own_ledger(settings: Settings, tmp_path: Path) -> None:
    """Folders holding files with the same name must not block each other's footage."""
    first = settings.background_ledger_path(tmp_path / "gta" / "videos")
    second = settings.background_ledger_path(tmp_path / "parkour" / "videos")

    assert first != second
    assert first == settings.background_ledger_path(tmp_path / "gta" / "videos")
    assert first.parent == settings.cache_dir / "background"
    assert first.name.startswith("videos-")


# --------------------------------------------------------------------------------------
# Scenario settings
# --------------------------------------------------------------------------------------


def test_background_video_needs_a_folder_when_enabled() -> None:
    with pytest.raises(ValidationError, match="folder is required"):
        VideoSettings.model_validate({"background_video": {"enabled": True}})


def test_background_video_folder_must_exist(tmp_path: Path) -> None:
    with pytest.raises(ValidationError, match="does not exist"):
        VideoSettings.model_validate(
            {"background_video": {"enabled": True, "folder": str(tmp_path / "nowhere")}}
        )


def test_background_video_is_for_shorts_only(tmp_path: Path) -> None:
    with pytest.raises(ValidationError, match="shorts format only"):
        VideoSettings.model_validate(
            {
                "orientation": "landscape",
                "format": "story",
                "background_video": {"enabled": True, "folder": str(tmp_path)},
            }
        )


def test_game_audio_volume_stays_between_zero_and_one(tmp_path: Path) -> None:
    with pytest.raises(ValidationError):
        VideoSettings.model_validate(
            {"background_video": {"folder": str(tmp_path), "game_audio_volume": 1.5}}
        )


# --------------------------------------------------------------------------------------
# Real ffmpeg
# --------------------------------------------------------------------------------------


def _make_source_video(path: Path, seconds: int) -> None:
    """Render a small test-pattern video with a tone, like a gameplay clip with sound."""
    subprocess.run(
        [
            str(ffmpeg_executable()),
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"testsrc2=size=320x180:rate=30:duration={seconds}",
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=440:duration={seconds}",
            "-shortest",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            str(path),
        ],
        check=True,
        capture_output=True,
    )


def test_ffmpeg_cuts_clips_of_the_requested_length(tmp_path: Path) -> None:
    folder = tmp_path / "videos"
    folder.mkdir()
    _make_source_video(folder / "drive.mp4", seconds=12)
    library = BackgroundLibrary(
        folder, tmp_path / "ledger.json", rng=random.Random(3), edge_skip=1.0
    )

    cut = library.cut("first-video", [2.0, 3.0], tmp_path / "clips")

    margin = BACKGROUND_CLIP_MARGIN_SECONDS
    assert [path.is_file() for path in cut.clips] == [True, True]
    assert probe_duration(cut.clips[0]) == pytest.approx(2.0 + margin, abs=0.1)
    assert probe_duration(cut.clips[1]) == pytest.approx(3.0 + margin, abs=0.1)
    assert not list((tmp_path / "clips").glob("*.part.mp4"))


def test_a_failed_cut_leaves_no_half_written_clip(tmp_path: Path) -> None:
    broken = tmp_path / "broken.mp4"
    broken.write_bytes(b"this is not a video")
    dest = tmp_path / "clip.mp4"

    with pytest.raises(RenderError, match="could not cut"):
        cut_with_ffmpeg(broken, 0.0, 1.0, dest)

    assert not dest.exists()
    assert not (tmp_path / "clip.part.mp4").exists()
