"""Copy weekdays episode stills from assets into storyboard by beats.tsv names only."""

from __future__ import annotations

import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ID = "why-your-week-has-seven-days-11dk-20260828"
BOARD = PROJECT_ROOT / "output" / "storyboard" / PROJECT_ID
ASSETS = Path(
    r"C:\Users\mirac\.cursor\projects\c-Users-mirac-Desktop-youtube-automation\assets"
)
TSV = BOARD / "beats.tsv"


def main() -> None:
    lines = TSV.read_text(encoding="utf-8").splitlines()[1:]
    names = [line.split("\t")[1].strip() for line in lines if line.strip()]
    copied = 0
    missing: list[str] = []
    for name in names:
        dest = BOARD / name
        src = ASSETS / name
        if src.is_file():
            shutil.copy2(src, dest)
            copied += 1
        else:
            missing.append(name)
    thumb_src = ASSETS / "thumbnail-weekdays.png"
    thumb_dest = BOARD / "thumbnail.png"
    if thumb_src.is_file():
        shutil.copy2(thumb_src, thumb_dest)
    print("expected", len(names))
    print("copied", copied)
    print("missing", len(missing))
    if missing[:10]:
        print("first_missing", missing[:10])


if __name__ == "__main__":
    main()
