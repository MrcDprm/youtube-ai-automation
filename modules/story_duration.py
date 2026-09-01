"""Fit measured story narration to a target runtime by dropping trailing chapters.

``run`` never calls an LLM. Extra speech is produced at ``generate`` time by writing until
the character estimate reaches ``--minutes``. If TTS still overshoots, this module drops
complete chapters from the end rather than cutting a sentence mid-audio.
"""

from __future__ import annotations

from config.constants import STORY_DURATION_TOLERANCE_SECONDS

__all__ = ["keep_leading_scenes", "spoken_length"]


def spoken_length(durations: list[float], gap: float) -> float:
    """Sum narration lengths plus the trailing gap after each chapter.

    Args:
        durations: Measured TTS lengths, in scene order.
        gap: Silence appended after every chapter.

    Returns:
        Total spoken timeline in seconds.
    """
    if not durations:
        return 0.0
    return sum(durations) + gap * len(durations)


def keep_leading_scenes(
    durations: list[float],
    target: float,
    *,
    tolerance: float = STORY_DURATION_TOLERANCE_SECONDS,
    gap: float = 0.3,
) -> int:
    """How many leading chapters to keep so the timeline is not far over ``target``.

    If the full list is already within ``target + tolerance``, every chapter is kept. If it
    overshoots, trailing chapters are dropped until the remainder fits, never below one
    chapter. Being *short* of ``target`` is left to the caller (generation already overshot
    the character budget).

    Args:
        durations: Measured TTS lengths, in scene order.
        target: Desired spoken length in seconds.
        tolerance: Allowed overshoot in seconds.
        gap: Silence after each chapter.

    Returns:
        Count of leading scenes to keep, ``0`` when ``durations`` is empty.
    """
    if not durations:
        return 0
    if spoken_length(durations, gap) <= target + tolerance:
        return len(durations)
    keep = len(durations)
    while keep > 1 and spoken_length(durations[:keep], gap) > target + tolerance:
        keep -= 1
    return keep
