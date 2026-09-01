"""Build a global beat timeline from per-scene TTS results."""

from __future__ import annotations

from dataclasses import replace

from models.scenario import Scene
from modules.interfaces import TTSResult, WordCue
from zenn.segmentation.beats import Beat, apply_scene_visuals, cues_to_beats

__all__ = ["collect_word_cues", "story_beats"]


def collect_word_cues(
    scenes: list[Scene],
    tts_results: dict[int, TTSResult],
    gap: float,
) -> list[WordCue]:
    """Flatten scene word cues onto one narration timeline including chapter gaps.

    Args:
        scenes: Selected scenes in playback order.
        tts_results: Measured synthesis results keyed by scene id.
        gap: Silence inserted after each chapter except the last.

    Returns:
        Word cues with offsets applied.
    """
    offset = 0.0
    merged: list[WordCue] = []
    for index, scene in enumerate(scenes):
        result = tts_results[scene.id]
        merged.extend(cue.shifted(offset) for cue in result.word_cues)
        offset += result.duration
        if index < len(scenes) - 1:
            offset += gap
    return merged


def story_beats(
    scenes: list[Scene],
    tts_results: dict[int, TTSResult],
    gap: float,
) -> list[Beat]:
    """Pack beats per scene, offset them globally, and insert gap holds.

    Args:
        scenes: Selected scenes in playback order.
        tts_results: Measured synthesis results keyed by scene id.
        gap: Silence after each chapter except the last.

    Returns:
        Timeline-ordered beats covering speech and inter-chapter holds.
    """
    timeline: list[Beat] = []
    offset_ms = 0
    for index, scene in enumerate(scenes):
        result = tts_results[scene.id]
        scene_beats = apply_scene_visuals(cues_to_beats(result.word_cues), scene.narration)
        scene_end_ms = int(round(result.duration * 1000.0))
        scene_beats = _close_beat_gaps(scene_beats, scene_end_ms)
        for beat in scene_beats:
            timeline.append(
                replace(
                    beat,
                    start_ms=offset_ms + beat.start_ms,
                    end_ms=offset_ms + beat.end_ms,
                )
            )
        offset_ms += int(round(result.duration * 1000.0))
        if index >= len(scenes) - 1 or gap <= 0:
            continue
        hold_ms = int(round(gap * 1000.0))
        if hold_ms <= 0 or not timeline:
            offset_ms += hold_ms
            continue
        last = timeline[-1]
        timeline.append(
            Beat(
                start_ms=offset_ms,
                end_ms=offset_ms + hold_ms,
                text="",
                visual_prompt=last.visual_prompt,
                pose_tag=last.pose_tag,
                bg_tag=last.bg_tag,
            )
        )
        offset_ms += hold_ms
    return timeline


def _close_beat_gaps(beats: list[Beat], scene_end_ms: int) -> list[Beat]:
    """Extend each hold through pauses until the next beat or scene end."""
    if not beats:
        return beats
    closed: list[Beat] = []
    for index, beat in enumerate(beats):
        if index + 1 < len(beats):
            end_ms = beats[index + 1].start_ms
        else:
            end_ms = scene_end_ms
        closed.append(replace(beat, end_ms=max(beat.end_ms, end_ms)))
    return closed
