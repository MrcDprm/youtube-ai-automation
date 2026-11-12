"""Editor: footage keeps its own sound only when the scenario asks for it.

These tests render real, tiny scenes with MoviePy and measure the result with ffmpeg's
``volumedetect``: a silent narration over a clip with a loud tone shows exactly how much of
the clip's sound made it into the scene.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

from models.scenario import Scene, SubtitleSettings
from modules.editor import MoviePyEditor
from modules.interfaces import ScenePlan
from utils.media import ffmpeg_executable


def _ffmpeg(*args: str) -> str:
    """Run ffmpeg and return its log, which is where ``volumedetect`` reports."""
    result = subprocess.run(
        [str(ffmpeg_executable()), "-hide_banner", "-y", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return result.stderr


def _mean_volume(path: Path) -> float:
    log = _ffmpeg("-i", str(path), "-af", "volumedetect", "-f", "null", "-")
    match = re.search(r"mean_volume: (-?[\d.]+|-inf) dB", log)
    assert match is not None, log[-500:]
    return float("-inf") if match.group(1) == "-inf" else float(match.group(1))


@pytest.fixture
def inputs(tmp_path: Path) -> tuple[Path, Path]:
    """A silent narration and a clip with a steady tone, like gameplay with engine noise."""
    narration = tmp_path / "narration.wav"
    _ffmpeg("-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "1.0", str(narration))
    clip = tmp_path / "clip.mp4"
    _ffmpeg(
        "-f",
        "lavfi",
        "-i",
        "testsrc2=size=64x112:rate=30:duration=1.5",
        "-f",
        "lavfi",
        "-i",
        "sine=frequency=440:duration=1.5",
        "-shortest",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        str(clip),
    )
    return narration, clip


def _render(tmp_path: Path, inputs: tuple[Path, Path], volume: float, name: str) -> Path:
    narration, clip = inputs
    plan = ScenePlan(
        scene=Scene(id=1, narration="Deneme.", search_terms=["test"], zoom_effect=False),
        audio_path=narration,
        audio_duration=1.0,
        media_paths=[clip],
        subtitle_cues=[],
        target_resolution=(64, 112),
        fps=30,
        scene_gap_seconds=0.2,
        subtitles=SubtitleSettings(enabled=False),
        font_path=None,
        output_path=tmp_path / f"{name}.mp4",
        background_audio_volume=volume,
    )
    editor = MoviePyEditor(temp_dir=tmp_path / "temp", threads=1, preset="ultrafast")
    return editor.build_scene(plan)


def test_footage_sound_is_dropped_by_default(tmp_path: Path, inputs: tuple[Path, Path]) -> None:
    """Stock clips and silent-by-default background footage leave only the narration."""
    assert _mean_volume(_render(tmp_path, inputs, 0.0, "silent")) < -60


def test_background_volume_mixes_the_footage_sound_under_the_voice(
    tmp_path: Path, inputs: tuple[Path, Path]
) -> None:
    silent = _mean_volume(_render(tmp_path, inputs, 0.0, "silent"))
    mixed = _mean_volume(_render(tmp_path, inputs, 0.5, "mixed"))

    assert mixed > silent + 30
