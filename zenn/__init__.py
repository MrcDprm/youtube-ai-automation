"""Free stick-cut sidecar: Edge TTS word timings to ~2s visual beats."""

from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT: Path = Path(__file__).resolve().parent
CONFIG_DIR: Path = PACKAGE_ROOT / "config"

__all__ = ["CONFIG_DIR", "PACKAGE_ROOT"]
