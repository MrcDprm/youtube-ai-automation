"""Split Edge TTS ``WordCue`` timings into 1–4 second visual beats."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from modules.interfaces import WordCue
from zenn import CONFIG_DIR
from zenn.segmentation.rules import PoseFallback, assign_tags, visual_prompt_for

_DEFAULT_POSE = "standing"
_DEFAULT_BG = "road"
_BLANK_BGS = frozenset({"", "blank"})

_SENTENCE_END = frozenset(".!?…")

__all__ = ["Beat", "apply_scene_visuals", "cues_to_beats", "load_style"]


@dataclass(frozen=True, slots=True)
class Beat:
    """One on-screen hold aligned to real speech.

    Attributes:
        start_ms: Inclusive start on the narration timeline.
        end_ms: Exclusive-feeling end (last word's end), milliseconds.
        text: Spoken words in this hold, joined with spaces.
        visual_prompt: Stick-figure prompt for a later renderer.
        pose_tag: Pose from the rule table.
        bg_tag: Background from the rule table.
    """

    start_ms: int
    end_ms: int
    text: str
    visual_prompt: str
    pose_tag: str
    bg_tag: str

    @property
    def duration_ms(self) -> int:
        """Hold length in milliseconds, never negative."""
        return max(0, self.end_ms - self.start_ms)


def load_style(path: Path | None = None) -> dict[str, float]:
    """Return beat min / target / max seconds from ``style.json``.

    Args:
        path: Override JSON path.

    Returns:
        Mapping with ``min_seconds``, ``target_seconds``, ``max_seconds``.
    """
    target = path or (CONFIG_DIR / "style.json")
    payload = json.loads(target.read_text(encoding="utf-8"))
    beat = payload.get("beat") if isinstance(payload.get("beat"), dict) else {}
    return {
        "min_seconds": float(beat.get("min_seconds", 1.0)),
        "target_seconds": float(beat.get("target_seconds", 2.2)),
        "max_seconds": float(beat.get("max_seconds", 4.0)),
    }


def cues_to_beats(
    cues: list[WordCue],
    *,
    min_seconds: float | None = None,
    target_seconds: float | None = None,
    max_seconds: float | None = None,
    fallback: PoseFallback | None = None,
) -> list[Beat]:
    """Pack word timings into beats using **measured** start/end, not word counts.

    Args:
        cues: Edge TTS word cues in time order.
        min_seconds: Floor hold. ``None`` reads ``style.json``.
        target_seconds: Preferred cut. ``None`` reads ``style.json``.
        max_seconds: Ceiling except a single over-long word.
        fallback: Optional pose/bg predictor when keywords miss.

    Returns:
        Beats covering the cues. Empty input yields an empty list.
    """
    if not cues:
        return []

    style = load_style()
    min_s = float(style["min_seconds"] if min_seconds is None else min_seconds)
    target_s = float(style["target_seconds"] if target_seconds is None else target_seconds)
    max_s = float(style["max_seconds"] if max_seconds is None else max_seconds)
    if min_s <= 0 or target_s < min_s or max_s < target_s:
        raise ValueError("need 0 < min_seconds <= target_seconds <= max_seconds")

    groups: list[list[WordCue]] = []
    current: list[WordCue] = []

    def duration_of(words: list[WordCue]) -> float:
        return max(0.0, words[-1].end - words[0].start)

    for cue in cues:
        if not current:
            current = [cue]
            held = duration_of(current)
            if held >= max_s or (_ends_sentence(cue.text) and held >= min_s) or held >= target_s:
                groups.append(current)
                current = []
            continue
        proposed = duration_of([*current, cue])
        if proposed > max_s:
            groups.append(current)
            current = [cue]
            continue
        current.append(cue)
        held = duration_of(current)
        if held >= max_s:
            groups.append(current)
            current = []
            continue
        if _ends_sentence(cue.text) and held >= min_s:
            groups.append(current)
            current = []
            continue
        if held >= target_s:
            groups.append(current)
            current = []

    if current:
        groups.append(current)

    if len(groups) >= 2 and duration_of(groups[-1]) < min_s:
        groups[-2].extend(groups[-1])
        groups.pop()

    beats: list[Beat] = []
    last_bg = _DEFAULT_BG
    for words in groups:
        text = " ".join(word.text for word in words).strip()
        pose, bg = assign_tags(text, fallback=fallback)
        if bg in _BLANK_BGS:
            bg = last_bg
        else:
            last_bg = bg
        start_ms = _to_ms(words[0].start)
        end_ms = _to_ms(words[-1].end)
        beats.append(
            Beat(
                start_ms=start_ms,
                end_ms=max(end_ms, start_ms),
                text=text,
                visual_prompt=visual_prompt_for(text, pose, bg),
                pose_tag=pose,
                bg_tag=bg,
            )
        )
    return beats


def apply_scene_visuals(beats: list[Beat], chapter_text: str) -> list[Beat]:
    """Seed and carry backgrounds from chapter context so holds are not plain black."""
    from dataclasses import replace

    _, chapter_bg = assign_tags(chapter_text)
    last_bg = chapter_bg if chapter_bg not in _BLANK_BGS else _DEFAULT_BG
    enriched: list[Beat] = []
    for beat in beats:
        bg = beat.bg_tag if beat.bg_tag not in _BLANK_BGS else last_bg
        last_bg = bg
        pose = beat.pose_tag
        enriched.append(
            replace(
                beat,
                pose_tag=pose,
                bg_tag=bg,
                visual_prompt=visual_prompt_for(beat.text, pose, bg),
            )
        )
    return enriched


def _ends_sentence(word: str) -> bool:
    """True when the cue's last letter-like character is a sentence stopper."""
    stripped = word.rstrip("\"')]}»”’")
    return bool(stripped) and stripped[-1] in _SENTENCE_END


def _to_ms(seconds: float) -> int:
    """Round seconds to a non-negative millisecond timestamp."""
    return max(0, int(round(seconds * 1000.0)))
