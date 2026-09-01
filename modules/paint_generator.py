"""Spoken-essay generation for Badly Drawn Why (paint format).

Shorts stay in :mod:`modules.script_generator`. Photo stories stay in
:mod:`modules.story_generator`. This module writes a retention-shaped English essay and a
list of MS Paint beats. ``run`` never calls it.
"""

from __future__ import annotations

import re
from typing import Any, Final

from config.constants import (
    PAINT_DEFAULT_MINUTES,
    PAINT_MAX_BEATS,
    PAINT_MIN_BEATS,
    PAINT_PLACEHOLDER_SEARCH_TERMS,
    SCRIPT_MAX_ATTEMPTS,
    SCRIPT_MAX_TAGS,
    SCRIPT_STORY_CHAPTER_MAX_SECONDS,
    SCRIPT_STORY_CHAPTER_MIN_SECONDS,
    STORY_MAX_CHAPTERS,
    YOUTUBE_DESCRIPTION_MAX_CHARS,
    YOUTUBE_TITLE_MAX_CHARS,
    paint_beat_count,
)
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.language import chars_per_second_for, language_display_name
from modules.scenario_builder import slugify
from modules.script_generator import OllamaScriptGenerator, extract_json_object
from utils.exceptions import ScriptGenerationError
from utils.logger import get_logger, log_info, log_warn

__all__ = ["OllamaPaintGenerator"]

logger = get_logger(__name__)

_BANNED_PHRASES: Final[tuple[str, ...]] = (
    "welcome back",
    "in this video",
    "don't forget to subscribe",
    "like and subscribe",
    "in this chapter we will",
)

_META_PROMPT: Final[str] = """\
You write spoken essays for the YouTube channel Badly Drawn Why. Stick-figure MS Paint \
drawings will play under the voice. Reply with a single JSON object and nothing else.

Required shape:
{{
  "title": string,
  "description": string,
  "tags": [string],
  "thumbnail_hook": string,
  "narration": string,
  "summary": string
}}

Rules:
- Write "narration", "title" and "description" in {language}.
- "title" is 45 to {title_max} characters. Use a curiosity question or forbidden-knowledge \
hook (Why / What / Would you). Do not put the channel name in the title. Do not write \
school-report titles like "The history of X" or "Interesting facts about Y".
- "thumbnail_hook" is 2 to 4 words, ALL CAPS, a punchy translation of the title, NOT the \
title itself (example: title about first and second sleep -> "2 AM?" or "FIRST SLEEP?").
- "narration" is chapter 1 of a spoken {minutes}-minute essay. This chapter is the COLD OPEN \
and OPEN LOOP: start in second person with a physical action in the first two sentences; \
promise that the answer changes what we think about sleep, storytelling, or being human \
(or the real stakes of THIS topic). No subscribe ask.
- Write the way a person talks: short sentences, contractions. No "in this video", \
"welcome back", scene numbers, speaker labels, markdown, or emoji.
- Spell years and large numbers as words in {language}.
- Name a specific place, person, or number as soon as the origin starts.
- About {min_chars} to {max_chars} characters of narration.
- "summary" is two sentences covering this chapter for the next writer.
- "tags" are 5 to {max_tags} lowercase English keywords.
- "description" is two hook sentences for YouTube, not a table of contents.
"""

_CHAPTER_PROMPT: Final[str] = """\
You are continuing a Badly Drawn Why spoken essay. Reply with a single JSON object and \
nothing else.

Required shape:
{{
  "narration": string,
  "summary": string
}}

Rules:
- Write "narration" in {language}. This is chapter {chapter_index} of a spoken \
{minutes}-minute essay. Role for this chapter: {role}
- Stay in second person often enough that the viewer feels seen. Short sentences. \
No "in this video", "in this chapter", subscribe asks, scene numbers, speaker labels, \
markdown, or emoji.
- Spell years and large numbers as words in {language}. Prefer named studies, places, \
and numbers over "scientists say".
- About {min_chars} to {max_chars} characters. Advance the argument; do not repeat.
- "summary" is two sentences covering this chapter only.
"""

_BEATS_PROMPT: Final[str] = """\
You storyboard Badly Drawn Why. Reply with a single JSON object and nothing else.

Required shape:
{{
  "beats": [
    {{"slug": string, "covers": string, "prompt": string}}
  ]
}}

Rules:
- Produce about {target_beats} unique beats (one still every five seconds of speech). \
Stay between {min_beats} and {max_beats}. Cover the essay in order. No duplicate scenes.
- "slug" is lowercase hyphenated ascii, 2 to 6 words, unique (example: "light-switch").
- "covers" is a short verbatim-ish excerpt of the narration this still matches.
- "prompt" describes one amateur MS Paint / stickman 16:9 frame: white background, wobbly \
thick black outlines, round-head stickman, flat colors, no 3D, no realistic humans, no anime. \
The drawing must show the idea in "covers", not a decorative landscape.
- PG-13. No gore, no nudity.
"""

_ROLE_COLD: Final[str] = (
    "Continue the mechanism: origin story with named people, places, and numbers. "
    "Do not close the open loop yet."
)
_ROLE_EVIDENCE: Final[str] = (
    "Evidence chapter. Include a contrast pair (then vs now, day vs night, myth vs record). "
    "Midway, plant a rehook: the weirdest part is still ahead."
)
_ROLE_YOU: Final[str] = (
    "Modern 'this is you' chapter. Connect the history to a habit the viewer has tonight. "
    "Still do not dump a new topic."
)
_ROLE_CLOSE: Final[str] = (
    "Close the open loop. Callback to the cold-open image in the last few sentences. "
    "One loss or trade-off. Do not start a new mystery."
)


class OllamaPaintGenerator:
    """Produces a :class:`DraftScript` plus drawing beats for format=paint."""

    def __init__(self, generator: OllamaScriptGenerator) -> None:
        """Wrap the Shorts generator so HTTP and sanitizers stay in one place."""
        self._inner = generator

    def generate(
        self,
        topic: str,
        *,
        target_seconds: float,
        language: str = "en",
        extra_guidance: str | None = None,
        max_chapters: int = STORY_MAX_CHAPTERS,
    ) -> DraftScript:
        """Draft a retention-shaped essay until the spoken estimate hits ``target_seconds``."""
        if target_seconds <= 0:
            raise ScriptGenerationError("target_seconds must be positive.")

        cps = chars_per_second_for(language)
        min_chars = max(400, int(cps * SCRIPT_STORY_CHAPTER_MIN_SECONDS))
        max_chars = max(min_chars + 100, int(cps * SCRIPT_STORY_CHAPTER_MAX_SECONDS))
        language_name = language_display_name(language)
        minutes = max(1, round(target_seconds / 60))

        scenes: list[DraftScene] = []
        title = ""
        description = ""
        tags: tuple[str, ...] = ()
        thumbnail_hook = ""
        rolling_summary = ""
        estimated = 0.0
        gap = 0.3

        for index in range(1, max_chapters + 1):
            role = _chapter_role(index, estimated, target_seconds)
            log_info(f"Drafting paint chapter {index} ({role.split()[0].lower()})...")
            payload = self._ask_chapter(
                topic=topic,
                chapter_index=index,
                minutes=minutes,
                language_name=language_name,
                min_chars=min_chars,
                max_chars=max_chars,
                extra_guidance=extra_guidance,
                previous_summary=rolling_summary,
                role=role,
                need_meta=index == 1,
            )
            narration = self._inner._clean_narration(
                str(payload.get("narration", "")), max_chars=max_chars
            )
            narration = _strip_banned(narration)
            if not narration:
                raise ScriptGenerationError(f"Chapter {index} had empty narration.")
            scenes.append(
                DraftScene(narration=narration, search_terms=PAINT_PLACEHOLDER_SEARCH_TERMS)
            )
            estimated += len(narration) / cps + gap
            rolling_summary = self._inner._collapse(str(payload.get("summary", "")))[:600]
            if index == 1:
                title = self._inner._collapse(str(payload.get("title", "")))[
                    :YOUTUBE_TITLE_MAX_CHARS
                ].strip()
                description = str(payload.get("description", "")).strip()[
                    :YOUTUBE_DESCRIPTION_MAX_CHARS
                ]
                tags = self._inner._clean_tags(payload.get("tags"))
                thumbnail_hook = _clean_hook(str(payload.get("thumbnail_hook", "")))
            if estimated >= target_seconds:
                break

        if estimated < target_seconds:
            log_warn(
                f"Reached {len(scenes)} chapters with about {estimated:.0f}s of speech; "
                f"target was {target_seconds:.0f}s."
            )

        if not title:
            title = topic.strip()[:YOUTUBE_TITLE_MAX_CHARS]
        if not description:
            description = title
        if not tags:
            tags = self._inner._clean_tags(None)

        full_text = " ".join(scene.narration for scene in scenes)
        wanted = paint_beat_count(target_seconds)
        beats = self._try_beats(full_text, wanted=wanted) or _beats_from_narration(
            full_text, target=wanted
        )
        log_info(f"Paint storyboard: {len(beats)} visual beat(s)")

        return DraftScript(
            title=title,
            description=description,
            tags=tags,
            scenes=tuple(scenes),
            visual_beats=beats,
            thumbnail_hook=thumbnail_hook,
        )

    def _ask_chapter(
        self,
        *,
        topic: str,
        chapter_index: int,
        minutes: int,
        language_name: str,
        min_chars: int,
        max_chars: int,
        extra_guidance: str | None,
        previous_summary: str,
        role: str,
        need_meta: bool,
    ) -> dict[str, Any]:
        """Ask the model for one essay chapter, with a repair loop."""
        if need_meta:
            system = _META_PROMPT.format(
                language=language_name,
                minutes=minutes,
                min_chars=min_chars,
                max_chars=max_chars,
                max_tags=SCRIPT_MAX_TAGS,
                title_max=YOUTUBE_TITLE_MAX_CHARS,
            )
            user = (
                f"Write chapter 1 of a Badly Drawn Why essay about: {topic.strip()}\n"
                "Remember: cold open in YOU-language, then an open loop. No subscribe ask."
            )
        else:
            system = _CHAPTER_PROMPT.format(
                language=language_name,
                chapter_index=chapter_index,
                minutes=minutes,
                min_chars=min_chars,
                max_chars=max_chars,
                role=role,
            )
            user = (
                f"Topic: {topic.strip()}\n"
                f"What happened so far: {previous_summary or '(nothing yet)'}\n"
                f"Write chapter {chapter_index} only. Role: {role}"
            )
        if extra_guidance and extra_guidance.strip():
            user += f"\n\nAdditional direction: {extra_guidance.strip()}"

        messages: list[dict[str, str]] = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        last_error = "no attempt was made"

        for attempt in range(1, SCRIPT_MAX_ATTEMPTS + 1):
            reply = self._inner._chat(messages, scene_count=max(12, chapter_index))
            try:
                payload = extract_json_object(reply)
                narration = str(payload.get("narration", "")).strip()
                if not narration:
                    raise ValueError('"narration" was empty')
                if need_meta and not str(payload.get("title", "")).strip():
                    raise ValueError('"title" was empty')
                if attempt < SCRIPT_MAX_ATTEMPTS and len(narration) < min_chars // 2:
                    raise ValueError(
                        f"narration was only {len(narration)} characters; need about {min_chars}"
                    )
                return payload
            except ValueError as exc:
                last_error = str(exc)
                if attempt == SCRIPT_MAX_ATTEMPTS:
                    break
                log_warn(
                    f"Paint chapter {chapter_index} was unusable ({last_error}). Asking again."
                )
                messages = [
                    *messages,
                    {"role": "assistant", "content": reply[:2000]},
                    {
                        "role": "user",
                        "content": (
                            f"That reply was rejected because {last_error}. "
                            "Send the corrected JSON object only."
                        ),
                    },
                ]

        raise ScriptGenerationError(
            f"Paint chapter {chapter_index} failed after {SCRIPT_MAX_ATTEMPTS} "
            f"attempt(s): {last_error}",
            hint="Try a larger model, or a more concrete why-question topic.",
        )

    def _try_beats(self, transcript: str, *, wanted: int) -> tuple[DraftVisualBeat, ...]:
        """Ask once for a beat list; return empty on any failure so a heuristic can run."""
        excerpt = transcript[:8000]
        system = _BEATS_PROMPT.format(
            min_beats=PAINT_MIN_BEATS,
            max_beats=PAINT_MAX_BEATS,
            target_beats=wanted,
        )
        user = f"Storyboard this essay:\n{excerpt}"
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        try:
            reply = self._inner._chat(messages, scene_count=wanted)
            payload = extract_json_object(reply)
        except (ValueError, ScriptGenerationError) as exc:
            log_warn(f"Paint beat pass failed ({exc}); using heuristic stills.")
            return ()

        raw = payload.get("beats")
        if not isinstance(raw, list):
            return ()
        beats: list[DraftVisualBeat] = []
        used: set[str] = set()
        for index, item in enumerate(raw, start=1):
            if not isinstance(item, dict):
                continue
            covers = str(item.get("covers", "")).strip()[:400]
            prompt = str(item.get("prompt", "")).strip()
            slug = slugify(str(item.get("slug", "")) or covers or f"beat-{index}")[:40]
            if not slug or slug in used:
                slug = f"{index:02d}-{slug or 'beat'}"[:40]
            used.add(slug)
            if len(prompt) < 8:
                prompt = (
                    "White background, beginner MS Paint, wobbly black outlines, round-head "
                    f"stickman acting out: {covers or slug}. Flat colors, no shading."
                )
            beats.append(DraftVisualBeat(slug=slug, prompt=prompt, covers=covers))
        if len(beats) < 2:
            return ()
        return tuple(beats[:PAINT_MAX_BEATS])


def _chapter_role(index: int, estimated: float, target: float) -> str:
    """Pick the retention job for this chapter from elapsed vs target speech."""
    if index == 1:
        return "cold open and open loop"
    fraction = estimated / target if target else 0.0
    if fraction < 0.28:
        return _ROLE_COLD
    if fraction < 0.58:
        return _ROLE_EVIDENCE
    if fraction < 0.82:
        return _ROLE_YOU
    return _ROLE_CLOSE


def _strip_banned(text: str) -> str:
    """Drop lecture/subscribe framing if the model sneaks it in."""
    lowered = text.lower()
    if not any(phrase in lowered for phrase in _BANNED_PHRASES):
        return text
    kept: list[str] = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        blob = sentence.lower()
        if any(phrase in blob for phrase in _BANNED_PHRASES):
            continue
        kept.append(sentence)
    return " ".join(kept).strip() or text


def _clean_hook(raw: str) -> str:
    """Keep a short ALL CAPS cover line."""
    cleaned = re.sub(r"[^A-Za-z0-9 ?!'/-]+", " ", raw).strip()
    words = cleaned.split()
    if len(words) < 2:
        return ""
    return " ".join(words[:4]).upper()[:40]


def _beats_from_narration(text: str, target: int | None = None) -> tuple[DraftVisualBeat, ...]:
    """Split the essay into evenly grouped sentence stills when the model beat pass fails."""
    if target is None:
        target = paint_beat_count(PAINT_DEFAULT_MINUTES * 60)
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
    if len(sentences) < 2:
        chunk = 160
        sentences = [text[index : index + chunk].strip() for index in range(0, len(text), chunk)]
        sentences = [part for part in sentences if part]
    if len(sentences) < 2:
        sentences = [text or "A stickman stands on a white page.", "The stickman looks at you."]
    target = max(2, min(PAINT_MAX_BEATS, target))
    if len(sentences) < target:
        target = max(2, len(sentences))
    size = max(1, (len(sentences) + target - 1) // target)
    groups: list[str] = []
    for index in range(0, len(sentences), size):
        groups.append(" ".join(sentences[index : index + size]))
    groups = groups[:PAINT_MAX_BEATS]
    beats: list[DraftVisualBeat] = []
    used: set[str] = set()
    for index, covers in enumerate(groups, start=1):
        words = covers.split()[:6]
        slug = slugify(" ".join(words) if words else f"beat-{index:02d}")[:32]
        if len(slug) < 2:
            slug = f"beat-{index:02d}"
        if slug in used:
            slug = f"{index:02d}-{slug}"[:40]
        used.add(slug)
        prompt = (
            "White background, extremely simple beginner MS Paint drawing, wobbly thick "
            "uneven black outlines, stickman with round head and line body, flat colors only, "
            "no shading, no 3D, no realistic humans, no anime, lots of empty white space, "
            f"16:9. Scene: {covers[:400]}"
        )
        beats.append(DraftVisualBeat(slug=slug, prompt=prompt, covers=covers[:400]))
    return tuple(beats)
