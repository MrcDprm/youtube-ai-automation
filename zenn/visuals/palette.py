"""Load the Zenn black / white / yellow palette from ``style.json``."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from zenn import CONFIG_DIR

__all__ = ["Palette", "load_palette"]


@dataclass(frozen=True, slots=True)
class Palette:
    """Named colours for stick figures and captions."""

    background: str = "#000000"
    line: str = "#FFFFFF"
    accent: str = "#FFD600"
    alert: str = "#FF3B30"


def load_palette(path: Path | None = None) -> Palette:
    """Return palette colours from ``style.json``.

    Args:
        path: Override JSON path.

    Returns:
        Parsed :class:`Palette`.
    """
    target = path or (CONFIG_DIR / "style.json")
    payload = json.loads(target.read_text(encoding="utf-8"))
    raw = payload.get("palette") if isinstance(payload.get("palette"), dict) else {}
    return Palette(
        background=str(raw.get("background", "#000000")),
        line=str(raw.get("line", "#FFFFFF")),
        accent=str(raw.get("accent", "#FFD600")),
        alert=str(raw.get("alert", "#FF3B30")),
    )
