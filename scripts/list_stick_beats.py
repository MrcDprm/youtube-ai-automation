"""List stick episode beat filenames for a range."""
from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIO = PROJECT_ROOT / "senaryo-paint-stick.json"


def main() -> None:
    beats = json.loads(SCENARIO.read_text(encoding="utf-8"))["video"]["visual_beats"]
    for i in range(99, len(beats)):
        b = beats[i]
        print(f"{i + 1}\t{i + 1:02d}-{b['slug']}.png\t{b['prompt']}")


if __name__ == "__main__":
    main()
