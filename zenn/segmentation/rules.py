"""Keyword pose/background assignment from ``pose-rules.json``."""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from zenn import CONFIG_DIR

PoseFallback = Callable[[str], tuple[str, str]]

_DEFAULT_POSE = "standing"
_DEFAULT_BG = "blank"

__all__ = [
    "PoseFallback",
    "assign_tags",
    "load_pose_rules",
    "visual_prompt_for",
]


def load_pose_rules(path: Path | None = None) -> dict[str, Any]:
    """Load the pose/background keyword table.

    Args:
        path: Override JSON path. ``None`` uses ``zenn/config/pose-rules.json``.

    Returns:
        Parsed object with ``defaults``, ``poses``, and ``backgrounds``.
    """
    target = path or (CONFIG_DIR / "pose-rules.json")
    return json.loads(target.read_text(encoding="utf-8"))


def assign_tags(
    text: str,
    rules: Mapping[str, Any] | None = None,
    fallback: PoseFallback | None = None,
) -> tuple[str, str]:
    """Pick ``(pose_tag, bg_tag)`` for a beat.

    Scoring is whole-word, case-insensitive. The row with the most hits wins;
    ties keep the earlier row. Score zero uses ``defaults``, then ``fallback``.

    Args:
        text: Spoken beat text.
        rules: Preloaded table; loaded from disk when omitted.
        fallback: Optional ``(pose, bg)`` predictor. Never a paid API unless the
            caller injects one.

    Returns:
        Pose tag and background tag.
    """
    table = dict(rules) if rules is not None else load_pose_rules()
    defaults = table.get("defaults") if isinstance(table.get("defaults"), Mapping) else {}
    pose_default = str(defaults.get("pose", _DEFAULT_POSE))
    bg_default = str(defaults.get("bg", _DEFAULT_BG))

    pose = _best_tag(text, table.get("poses"), pose_default)
    bg = _best_tag(text, table.get("backgrounds"), bg_default)
    if pose != pose_default or bg != bg_default or fallback is None:
        return pose, bg
    pred_pose, pred_bg = fallback(text)
    return str(pred_pose or pose_default), str(pred_bg or bg_default)


def visual_prompt_for(text: str, pose_tag: str, bg_tag: str) -> str:
    """Build a short stick-figure prompt from tags and beat text.

    Args:
        text: Spoken words in this beat.
        pose_tag: Chosen pose.
        bg_tag: Chosen background.

    Returns:
        One-line visual description for a later SVG or still renderer.
    """
    snippet = re.sub(r"\s+", " ", text).strip()
    if len(snippet) > 80:
        snippet = snippet[:77].rstrip() + "..."
    return (
        f"Stick figure, pose {pose_tag}, background {bg_tag}, "
        f"black white yellow palette. {snippet}"
    )


def _best_tag(text: str, rows: object, default: str) -> str:
    """Return the tag with the highest keyword hit count, or ``default``."""
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
        return default
    haystack = text.casefold()
    best_tag = default
    best_score = 0
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        tag = str(row.get("tag", "")).strip()
        if not tag:
            continue
        raw_keys = row.get("keywords")
        if not isinstance(raw_keys, Sequence) or isinstance(raw_keys, (str, bytes)):
            continue
        score = 0
        for keyword in raw_keys:
            token = str(keyword).strip()
            if token and _word_in(haystack, token.casefold()):
                score += 1
        if score > best_score:
            best_score = score
            best_tag = tag
    return best_tag if best_score > 0 else default


def _word_in(haystack: str, keyword: str) -> bool:
    """True when ``keyword`` appears as a whole word (digits allowed, e.g. 1908)."""
    if not keyword:
        return False
    pattern = r"(?<![0-9a-zçğıöşü])" + re.escape(keyword) + r"(?![0-9a-zçğıöşü])"
    return re.search(pattern, haystack, flags=re.IGNORECASE) is not None
