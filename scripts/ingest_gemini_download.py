"""Move the newest Gemini web download into a storyboard slot as PNG.

Used by the still-generation loop: after clicking "download" in the Gemini web UI, this
waits for a genuinely NEW download to land (not a leftover file already sitting in
Downloads), converts it to PNG, writes it to the given destination, and removes the
original download so the next round never picks up a stale file.

Waiting for a file newer than the moment this script started (rather than just "the
newest file present") matters: on a slow connection the download can still be in flight
when this runs, and grabbing "newest so far" would silently hand back a stale image from
an earlier beat.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from PIL import Image

DOWNLOADS = Path.home() / "Downloads"
POLL_SECONDS = 0.5
TIMEOUT_SECONDS = 25.0
SETTLE_SECONDS = 0.6  # let Chrome finish writing before we read the file


def _candidates(since: float) -> list[Path]:
    return sorted(
        (
            p
            for p in DOWNLOADS.glob("Gemini_Generated_Image*")
            if p.is_file() and p.stat().st_mtime >= since
        ),
        key=lambda p: p.stat().st_mtime,
    )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: ingest_gemini_download.py <dest_png_path>")
    dest = Path(sys.argv[1])
    dest.parent.mkdir(parents=True, exist_ok=True)

    started = time.time() - 2.0  # small backdate so a just-finished download still counts
    deadline = time.time() + TIMEOUT_SECONDS
    src: Path | None = None
    while time.time() < deadline:
        found = _candidates(started)
        if found:
            src = found[-1]
            break
        time.sleep(POLL_SECONDS)

    if src is None:
        raise SystemExit(
            f"No new Gemini_Generated_Image* file appeared in {DOWNLOADS} within "
            f"{TIMEOUT_SECONDS:.0f}s. Was the download actually clicked?"
        )

    time.sleep(SETTLE_SECONDS)
    with Image.open(src) as img:
        img.convert("RGB").save(dest, "PNG")
    src.unlink()
    print(f"{src.name} -> {dest}")


if __name__ == "__main__":
    main()
