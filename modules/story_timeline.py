"""Pure timing math for the longform photo-story visual track.

The narration timeline is independent of the pictures. Story format still uses twenty unique
photos sharing the runtime equally. Paint format uses one unique still about every five
seconds (132 for an 11-minute essay), each with the same slow Ken Burns zoom. A fast opening
cycle used to flash stills every few seconds; that read as shake, so it is gone.

Nothing here opens a file or talks to MoviePy, so the layout can be unit-tested with a
stopwatch rather than a renderer.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from models.scenario import StoryVisualSettings

__all__ = ["PhotoSlot", "StoryVisualPlan", "plan_story_visual", "plan_weighted_visual"]


@dataclass(frozen=True, slots=True)
class PhotoSlot:
    """One unique photo encode.

    Attributes:
        photo_index: Index into the photo list (0-based).
        duration: How long this encode lasts, in seconds.
        zoom_end: Ken Burns end scale; start is always 1.0.
        band: Always ``body`` (kept so existing editor code can key temp files).
    """

    photo_index: int
    duration: float
    zoom_end: float
    band: str


@dataclass(frozen=True, slots=True)
class StoryVisualPlan:
    """Everything the editor needs to build the stills track.

    Attributes:
        total_duration: Matches the narration timeline (audio + gaps).
        opening_duration: Always ``0``; the opening cycle was removed.
        opening_cycle_duration: Always ``0``.
        opening_slots: Empty. All stills live in ``body_slots``.
        body_slots: One slot per photo, equal duration, same zoom.
    """

    total_duration: float
    opening_duration: float
    opening_cycle_duration: float
    opening_slots: tuple[PhotoSlot, ...]
    body_slots: tuple[PhotoSlot, ...]

    @property
    def body_duration(self) -> float:
        """Seconds covered by the photo track (the whole video)."""
        return max(0.0, self.total_duration - self.opening_duration)


def plan_story_visual(total_duration: float, visual: StoryVisualSettings) -> StoryVisualPlan:
    """Lay out equal-time stills for a finished narration length.

    Args:
        total_duration: Narration plus inter-scene gaps, in seconds.
        visual: Photo count and zoom endpoint from the scenario.

    Returns:
        A plan whose slot durations sum to ``total_duration``.

    Raises:
        ValueError: If ``total_duration`` is not positive, or there are fewer than two photos.
    """
    if total_duration <= 0:
        raise ValueError(f"total_duration must be positive, got {total_duration}")

    photo_count = visual.photo_count
    if photo_count < 2:
        raise ValueError(f"Need at least two photos; got photo_count={photo_count}.")

    each = total_duration / photo_count
    body_slots = tuple(
        PhotoSlot(
            photo_index=index,
            duration=each,
            zoom_end=visual.zoom_body_end,
            band="body",
        )
        for index in range(photo_count)
    )
    return StoryVisualPlan(
        total_duration=total_duration,
        opening_duration=0.0,
        opening_cycle_duration=0.0,
        opening_slots=(),
        body_slots=body_slots,
    )


def plan_weighted_visual(
    total_duration: float,
    weights: Sequence[float],
    *,
    zoom_end: float,
) -> StoryVisualPlan:
    """Lay out stills so hold time follows transcript coverage weights.

    Args:
        total_duration: Narration plus inter-scene gaps, in seconds.
        weights: Relative hold for each still; zeros are treated as 1.
        zoom_end: Ken Burns end scale for every slot.

    Returns:
        A plan whose slot durations sum to ``total_duration``.

    Raises:
        ValueError: If duration is not positive or there are fewer than two weights.
    """
    if total_duration <= 0:
        raise ValueError(f"total_duration must be positive, got {total_duration}")
    if len(weights) < 2:
        raise ValueError(f"Need at least two stills; got {len(weights)}.")

    cleaned = [max(1.0, float(weight)) for weight in weights]
    total_weight = sum(cleaned)
    durations = [total_duration * (weight / total_weight) for weight in cleaned]
    drift = total_duration - sum(durations)
    durations[-1] += drift

    body_slots = tuple(
        PhotoSlot(
            photo_index=index,
            duration=duration,
            zoom_end=zoom_end,
            band="body",
        )
        for index, duration in enumerate(durations)
    )
    return StoryVisualPlan(
        total_duration=total_duration,
        opening_duration=0.0,
        opening_cycle_duration=0.0,
        opening_slots=(),
        body_slots=body_slots,
    )
