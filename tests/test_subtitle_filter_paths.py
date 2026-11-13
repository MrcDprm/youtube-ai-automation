"""ffmpeg's subtitle filter finds the captions and the font in any folder name.

A user folder such as ``C:/Users/O'Neil`` used to break the filter: the apostrophe ended the
quoted path, and ffmpeg stopped with a parse error before drawing a frame.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from config.constants import PROJECT_ROOT
from modules.editor import MoviePyEditor
from utils.media import ffmpeg_executable

ASS = """[Script Info]
ScriptType: v4.00+
PlayResX: 320
PlayResY: 240

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, \
Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, \
Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: A,Anton,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,A,,0,0,0,,TEST
"""


@pytest.mark.parametrize("folder_name", ["O'Neil", "kurgu, [son] hali", "Ayşe'nin videoları"])
def test_captions_burn_from_a_folder_with_quotes_and_commas(
    tmp_path: Path, folder_name: str
) -> None:
    folder = tmp_path / folder_name
    folder.mkdir()
    shutil.copy(PROJECT_ROOT / "assets" / "fonts" / "Anton-Regular.ttf", folder)
    ass = folder / "captions.ass"
    ass.write_text(ASS, encoding="utf-8")

    result = subprocess.run(
        [
            str(ffmpeg_executable()),
            "-v",
            "error",
            "-f",
            "lavfi",
            "-i",
            "color=c=black:size=320x240:duration=0.2",
            "-vf",
            MoviePyEditor._ass_filter(ass, folder),
            "-frames:v",
            "1",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "gray",
            "-",
        ],
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr.decode("utf-8", "replace")[-500:]
    assert sum(1 for value in result.stdout if value > 128) > 200, "no caption was drawn"
