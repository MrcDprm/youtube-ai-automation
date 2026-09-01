"""Copy paint stills from assets into storyboard by exact beats.tsv filenames."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path(
    r"C:\Users\mirac\.cursor\projects\c-Users-mirac-Desktop-youtube-automation\assets"
)


def sync(project_id: str, *, thumb_name: str = "thumbnail.png") -> tuple[int, int]:
    board = PROJECT_ROOT / "output" / "storyboard" / project_id
    tsv = board / "beats.tsv"
    if not tsv.is_file():
        raise SystemExit(f"missing beats.tsv for {project_id}")

    lines = tsv.read_text(encoding="utf-8").splitlines()[1:]
    names = [line.split("\t")[1].strip() for line in lines if line.strip()]
    copied = 0
    missing: list[str] = []
    board.mkdir(parents=True, exist_ok=True)
    for name in names:
        src = ASSETS / name
        dest = board / name
        if src.is_file():
            shutil.copy2(src, dest)
            copied += 1
        else:
            missing.append(name)

    for candidate in (
        f"thumbnail-{project_id.split('-11dk-')[0]}.png",
        "thumbnail-rain.png",
        "thumbnail-hour.png",
        "thumbnail-stick.png",
        "thumbnail-weekdays.png",
        "thumbnail.png",
    ):
        src = ASSETS / candidate
        if src.is_file():
            shutil.copy2(src, board / thumb_name)
            break

    return copied, len(missing)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: sync_paint_stills.py <project_id>")
    copied, missing = sync(sys.argv[1])
    print("copied", copied)
    print("missing", missing)


if __name__ == "__main__":
    main()
