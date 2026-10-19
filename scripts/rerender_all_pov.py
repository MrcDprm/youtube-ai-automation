"""Regenerate scenarios and re-render all shipped Rank Run POV (every-level-pov) episodes."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYTHON = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"

EPISODES: tuple[tuple[str, str], ...] = (
    ("scripts/author_pov_football_levels.py", "senaryo-pov-football-levels.json"),
    ("scripts/author_pov_cl_matchday.py", "senaryo-pov-cl-matchday.json"),
    ("scripts/author_pov_sunday_premier.py", "senaryo-pov-sunday-premier.json"),
    ("scripts/author_pov_positions.py", "senaryo-pov-positions.json"),
    ("scripts/author_pov_transfer_window.py", "senaryo-pov-transfer-window.json"),
)


def _run(args: list[str]) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run(args, cwd=PROJECT_ROOT, check=True)


def main() -> None:
    py = str(PYTHON if PYTHON.is_file() else sys.executable)
    for author, scenario in EPISODES:
        print(f"\n=== {author} ===", flush=True)
        _run([py, str(PROJECT_ROOT / author)])
        _run([py, "main.py", "run", "--scenario", scenario, "--no-upload"])
    print("\nAll POV episodes re-rendered.", flush=True)


if __name__ == "__main__":
    main()
