"""Subtitle construction from word-level TTS timings.

Word cues arrive from edge-tts as one event per spoken word. This module groups them into
readable cues, wraps them to the configured line budget, and enforces the timing invariants
that both SRT players and MoviePy's compositor depend on: strictly increasing, non-overlapping
timestamps with sane minimum and maximum display durations.
"""

from __future__ import annotations

from pathlib import Path

from config.constants import (
    CLAUSE_END_CHARS,
    CUE_GAP_SECONDS,
    MAX_CUE_DURATION,
    MIN_CUE_DURATION,
    SENTENCE_END_CHARS,
)
from models.scenario import SubtitleSettings
from modules.interfaces import ISubtitleBuilder, SubtitleCue, WordCue
from utils.exceptions import SubtitleError
from utils.fs import atomic_write_text
from utils.logger import get_logger

__all__ = ["SrtSubtitleBuilder", "format_timestamp", "wrap_words"]

logger = get_logger(__name__)


def format_timestamp(seconds: float) -> str:
    """Format a time offset as an SRT timestamp.

    Args:
        seconds: Offset from the start of the media. Negative values clamp to zero.

    Returns:
        A timestamp in ``HH:MM:SS,mmm`` form.
    """
    total_ms = int(round(max(0.0, seconds) * 1000))
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def wrap_words(words: list[str], max_chars_per_line: int, max_lines: int) -> str:
    """Wrap words into at most ``max_lines`` lines.

    Words are never split. If the text cannot fit, the surplus is appended to the final line
    rather than being dropped, because silently losing narration is worse than one long line.

    Args:
        words: The words to lay out.
        max_chars_per_line: Soft character budget per line.
        max_lines: Maximum number of lines.

    Returns:
        The wrapped text with ``\\n`` between lines.
    """
    if not words:
        return ""

    lines: list[str] = []
    current: list[str] = []

    for word in words:
        candidate = " ".join([*current, word])
        if current and len(candidate) > max_chars_per_line and len(lines) < max_lines - 1:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)

    if current:
        lines.append(" ".join(current))

    if len(lines) > max_lines:
        head = lines[: max_lines - 1]
        tail = " ".join(lines[max_lines - 1 :])
        lines = [*head, tail]

    return "\n".join(lines)


class SrtSubtitleBuilder(ISubtitleBuilder):
    """Groups word cues into subtitle cues and writes SRT files."""

    def __init__(
        self,
        *,
        min_duration: float = MIN_CUE_DURATION,
        max_duration: float = MAX_CUE_DURATION,
        gap: float = CUE_GAP_SECONDS,
    ) -> None:
        """Initialise the builder.

        Args:
            min_duration: Shortest time a cue may stay on screen.
            max_duration: Longest time a cue may stay on screen.
            gap: Minimum separation enforced between consecutive cues.
        """
        self._min_duration = min_duration
        self._max_duration = max_duration
        self._gap = gap

    # -- Public API ---------------------------------------------------------------------

    def build(
        self,
        cues: list[WordCue],
        settings: SubtitleSettings,
        offset: float = 0.0,
    ) -> list[SubtitleCue]:
        """Group word cues into displayable subtitle cues.

        Grouping prefers to break at sentence ends, then at clause punctuation, and only then
        at the character budget, which keeps phrases intact.

        Args:
            cues: Word-level timings, assumed to be in chronological order.
            settings: Line-length, casing and layout constraints.
            offset: Seconds added to every timestamp, used to place a scene's cues onto the
                whole-video timeline.

        Returns:
            Cues with monotonic, non-overlapping timestamps, numbered from 1.
        """
        if not cues:
            return []

        ordered = sorted(cues, key=lambda cue: cue.start)
        groups = self._group_words(ordered, settings)
        built = self._materialize(groups, settings, offset)
        return self._enforce_timing(built)

    def build_from_duration(
        self,
        text: str,
        duration: float,
        settings: SubtitleSettings,
        offset: float = 0.0,
    ) -> list[SubtitleCue]:
        """Build cues by distributing text evenly across a known duration.

        The fallback for when the TTS engine returned no word boundaries. Timings are
        approximate but proportional to each chunk's character count, which tracks speech
        pacing closely enough for short-form video.

        Args:
            text: The narration that was spoken.
            duration: Measured audio duration in seconds.
            settings: Line-length and layout constraints.
            offset: Seconds added to every timestamp.

        Returns:
            Evenly distributed cues, or an empty list when there is nothing to show.
        """
        words = text.split()
        if not words or duration <= 0:
            return []

        synthetic: list[WordCue] = []
        total_chars = sum(len(word) for word in words) or 1
        cursor = 0.0
        for word in words:
            share = duration * (len(word) / total_chars)
            synthetic.append(WordCue(text=word, start=cursor, end=cursor + share))
            cursor += share

        return self.build(synthetic, settings, offset)

    def write_srt(self, cues: list[SubtitleCue], out_path: Path) -> Path:
        """Write cues to a UTF-8 SRT file with no byte-order mark.

        Args:
            cues: Cues to serialise.
            out_path: Destination ``.srt`` path.

        Returns:
            The written path.

        Raises:
            SubtitleError: If the file cannot be written.
        """
        blocks = [
            f"{cue.index}\n"
            f"{format_timestamp(cue.start)} --> {format_timestamp(cue.end)}\n"
            f"{cue.text}"
            for cue in cues
        ]
        payload = "\n\n".join(blocks) + ("\n" if blocks else "")
        try:
            atomic_write_text(out_path, payload, encoding="utf-8")
        except OSError as exc:
            raise SubtitleError(
                f"Could not write subtitles to {out_path}: {exc}",
                hint="Check that the output directory exists and is writable.",
            ) from exc
        logger.debug("Wrote %d cue(s) to %s", len(cues), out_path.name)
        return out_path

    def merge(self, groups: list[list[SubtitleCue]]) -> list[SubtitleCue]:
        """Flatten per-scene cue lists into one renumbered timeline.

        Args:
            groups: Per-scene cues, already offset onto the whole-video timeline.

        Returns:
            A single list, ordered by start time and renumbered from 1.
        """
        flattened = [cue for group in groups for cue in group]
        flattened.sort(key=lambda cue: (cue.start, cue.end))
        return [cue.renumbered(index) for index, cue in enumerate(flattened, start=1)]

    # -- Grouping -----------------------------------------------------------------------

    def _group_words(self, words: list[WordCue], settings: SubtitleSettings) -> list[list[WordCue]]:
        """Split a word stream into per-cue groups.

        Args:
            words: Chronologically ordered word cues.
            settings: Line-length constraints.

        Returns:
            Groups of words, each destined for one cue.
        """
        budget = settings.max_chars_per_cue
        groups: list[list[WordCue]] = []
        current: list[WordCue] = []
        current_length = 0

        for word in words:
            addition = len(word.text) + (1 if current else 0)
            exceeds_budget = current and current_length + addition > budget
            exceeds_duration = current and (word.end - current[0].start) > self._max_duration

            if exceeds_budget or exceeds_duration:
                groups.append(current)
                current = [word]
                current_length = len(word.text)
                continue

            current.append(word)
            current_length += addition

            # A finished sentence always ends its cue: one sentence per cue reads best in
            # short-form video, and _enforce_timing extends anything too brief to linger.
            # A clause break is weaker, so it only applies once the cue is nearly full.
            if self._ends_sentence(word.text) or (
                self._ends_clause(word.text) and current_length >= budget * 0.6
            ):
                groups.append(current)
                current = []
                current_length = 0

        if current:
            groups.append(current)
        return groups

    @staticmethod
    def _ends_sentence(word: str) -> bool:
        """Report whether a word terminates a sentence."""
        return bool(word) and word[-1] in SENTENCE_END_CHARS

    @staticmethod
    def _ends_clause(word: str) -> bool:
        """Report whether a word terminates a clause."""
        return bool(word) and word[-1] in CLAUSE_END_CHARS

    def _materialize(
        self,
        groups: list[list[WordCue]],
        settings: SubtitleSettings,
        offset: float,
    ) -> list[SubtitleCue]:
        """Turn word groups into wrapped, offset subtitle cues.

        Args:
            groups: Word groups from :meth:`_group_words`.
            settings: Layout and casing settings.
            offset: Seconds added to every timestamp.

        Returns:
            Cues numbered from 1, before timing normalization.
        """
        cues: list[SubtitleCue] = []
        for index, group in enumerate(groups, start=1):
            if not group:
                continue
            words = [word.text for word in group]
            text = wrap_words(words, settings.max_chars_per_line, settings.max_lines)
            if settings.uppercase:
                text = text.upper()
            cues.append(
                SubtitleCue(
                    index=index,
                    start=group[0].start + offset,
                    end=group[-1].end + offset,
                    text=text,
                )
            )
        return cues

    def _enforce_timing(self, cues: list[SubtitleCue]) -> list[SubtitleCue]:
        """Normalize cue timings so they are monotonic and never overlap.

        Each cue is clamped to the configured duration range, then pushed forward if it would
        otherwise start before the previous cue ended. A cue is never allowed to extend past
        the start of the next one.

        Args:
            cues: Cues in chronological order.

        Returns:
            Cues with valid, renumbered timings.
        """
        if not cues:
            return []

        adjusted: list[SubtitleCue] = []
        previous_end = 0.0

        for position, cue in enumerate(cues):
            start = max(cue.start, previous_end + self._gap if adjusted else cue.start)
            end = max(cue.end, start + self._min_duration)
            end = min(end, start + self._max_duration)

            next_start = cues[position + 1].start if position + 1 < len(cues) else None
            if next_start is not None and end > next_start - self._gap:
                end = max(start + 0.05, next_start - self._gap)

            adjusted.append(
                SubtitleCue(index=len(adjusted) + 1, start=start, end=end, text=cue.text)
            )
            previous_end = end

        return adjusted
