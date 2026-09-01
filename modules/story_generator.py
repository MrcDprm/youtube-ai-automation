"""Chaptered longform script generation via the same local Ollama server.

Shorts generation stays in :mod:`modules.script_generator`. This module asks for one spoken
chapter at a time, carrying a rolling summary so a 7B model can hold a 15-minute story
without emitting one giant JSON object. Chapter count follows ``--minutes``, not ``-n``.
"""

from __future__ import annotations

from typing import Any, Final

from config.constants import (
    SCRIPT_MAX_ATTEMPTS,
    SCRIPT_MAX_SEARCH_TERMS,
    SCRIPT_MAX_TAGS,
    SCRIPT_STORY_CHAPTER_MAX_SECONDS,
    SCRIPT_STORY_CHAPTER_MIN_SECONDS,
    STORY_MAX_CHAPTERS,
    YOUTUBE_DESCRIPTION_MAX_CHARS,
    YOUTUBE_TITLE_MAX_CHARS,
)
from modules.interfaces import DraftScene, DraftScript
from modules.language import chars_per_second_for, language_display_name
from modules.script_generator import OllamaScriptGenerator, extract_json_object
from utils.exceptions import ScriptGenerationError
from utils.logger import get_logger, log_info, log_warn

__all__ = ["OllamaStoryGenerator"]

logger = get_logger(__name__)

_META_PROMPT: Final[str] = """\
You are a novelist-narrator writing a long spoken story that will be read aloud over still \
photographs. Reply with a single JSON object and nothing else.

Required shape:
{{
  "title": string,
  "description": string,
  "tags": [string],
  "narration": string,
  "search_terms": [string],
  "summary": string
}}

Rules:
- Write "narration", "title" and "description" in {language}.
- "narration" is chapter 1 of a spoken {minutes}-minute story. Write the way a person talks: \
short sentences, contractions, no lecture framing such as "in this chapter we will". \
No scene numbers, no speaker labels, no markdown, no emoji.
- Spell years and large numbers as words in {language} (for example 1956 as words, not digits).
- About {min_chars} to {max_chars} characters of narration.
- "search_terms" must be in ENGLISH, 2 to {max_terms} concrete photographable subjects.
- "summary" is two sentences in {language} covering what happened in this chapter, for the \
next chapter's writer.
- "tags" are 5 to {max_tags} lowercase keywords in {language}.
- "title" at most {title_max} characters.
"""

_CHAPTER_PROMPT: Final[str] = """\
You are continuing a long spoken story that will be read aloud. Reply with a single JSON \
object and nothing else.

Required shape:
{{
  "narration": string,
  "search_terms": [string],
  "summary": string
}}

Rules:
- Write "narration" in {language}. This is chapter {chapter_index} of a spoken \
{minutes}-minute story.
- Write the way a person talks: short sentences, no "in this chapter we will", no scene \
numbers, no speaker labels, no markdown, no emoji.
- Spell years and large numbers as words in {language}.
- About {min_chars} to {max_chars} characters. Advance the story; do not repeat earlier events.
- "search_terms" in ENGLISH, 2 to {max_terms} concrete photographable subjects.
- "summary" is two sentences in {language} covering this chapter only.
"""


class OllamaStoryGenerator:
    """Produces a :class:`DraftScript` as sequential chapters."""

    def __init__(self, generator: OllamaScriptGenerator) -> None:
        """Wrap the Shorts generator so HTTP and sanitizers stay in one place.

        Args:
            generator: A configured :class:`OllamaScriptGenerator`.
        """
        self._inner = generator

    def generate(
        self,
        topic: str,
        *,
        chapter_count: int | None = None,
        target_seconds: float | None = None,
        language: str = "tr",
        extra_guidance: str | None = None,
        max_chapters: int = STORY_MAX_CHAPTERS,
    ) -> DraftScript:
        """Draft a longform story until the spoken estimate hits a runtime, or a count.

        Args:
            topic: The subject of the video.
            chapter_count: Exact chapter count. Ignored when ``target_seconds`` is set.
            target_seconds: Keep writing chapters until estimated speech reaches this.
            language: Narration language code.
            extra_guidance: Optional extra steering.
            max_chapters: Safety cap when sizing to a duration.

        Returns:
            A draft whose scenes are the chapters, in order.

        Raises:
            ScriptGenerationError: If a chapter cannot be produced, or neither count nor
                duration was given.
        """
        if target_seconds is None and (chapter_count is None or chapter_count < 1):
            raise ScriptGenerationError("Provide chapter_count or target_seconds.")
        if target_seconds is not None and target_seconds <= 0:
            raise ScriptGenerationError("target_seconds must be positive.")

        cps = chars_per_second_for(language)
        min_chars = max(400, int(cps * SCRIPT_STORY_CHAPTER_MIN_SECONDS))
        max_chars = max(min_chars + 100, int(cps * SCRIPT_STORY_CHAPTER_MAX_SECONDS))
        language_name = language_display_name(language)
        minutes = max(1, round((target_seconds or (chapter_count or 1) * 100) / 60))
        limit = (
            max_chapters
            if target_seconds is not None
            else max(1, min(chapter_count or 1, max_chapters))
        )

        scenes: list[DraftScene] = []
        title = ""
        description = ""
        tags: tuple[str, ...] = ()
        rolling_summary = ""
        estimated = 0.0
        gap = 0.3

        for index in range(1, limit + 1):
            log_info(f"Drafting story chapter {index}...")
            payload = self._ask_chapter(
                topic=topic,
                chapter_index=index,
                minutes=minutes,
                language_name=language_name,
                min_chars=min_chars,
                max_chars=max_chars,
                extra_guidance=extra_guidance,
                previous_summary=rolling_summary,
                need_meta=index == 1,
            )
            narration = self._inner._clean_narration(
                str(payload.get("narration", "")), max_chars=max_chars
            )
            if not narration:
                raise ScriptGenerationError(f"Chapter {index} had empty narration.")
            terms = self._inner._clean_terms(payload.get("search_terms"))
            if not terms:
                terms = ("artificial intelligence history", "computer laboratory")
                log_warn(f"Chapter {index} had no search_terms; using fallbacks.")
            scenes.append(DraftScene(narration=narration, search_terms=terms))
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
            if target_seconds is not None and estimated >= target_seconds:
                break

        if target_seconds is not None and estimated < target_seconds:
            log_warn(
                f"Reached {limit} chapters with about {estimated:.0f}s of speech; "
                f"target was {target_seconds:.0f}s."
            )

        if not title:
            title = topic.strip()[:YOUTUBE_TITLE_MAX_CHARS]
        if not description:
            description = title
        if not tags:
            tags = self._inner._clean_tags(None)

        return DraftScript(
            title=title,
            description=description,
            tags=tags,
            scenes=tuple(scenes),
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
        need_meta: bool,
    ) -> dict[str, Any]:
        """Ask the model for one chapter, with a repair loop."""
        if need_meta:
            system = _META_PROMPT.format(
                language=language_name,
                minutes=minutes,
                min_chars=min_chars,
                max_chars=max_chars,
                max_terms=SCRIPT_MAX_SEARCH_TERMS,
                max_tags=SCRIPT_MAX_TAGS,
                title_max=YOUTUBE_TITLE_MAX_CHARS,
            )
            user = f"Write chapter 1 of a long spoken story about: {topic.strip()}"
        else:
            system = _CHAPTER_PROMPT.format(
                language=language_name,
                chapter_index=chapter_index,
                minutes=minutes,
                min_chars=min_chars,
                max_chars=max_chars,
                max_terms=SCRIPT_MAX_SEARCH_TERMS,
            )
            user = (
                f"Topic: {topic.strip()}\n"
                f"What happened so far: {previous_summary or '(nothing yet)'}\n"
                f"Write chapter {chapter_index} only."
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
                if not isinstance(payload, dict):
                    raise ValueError("the JSON root was not an object")
                narration = str(payload.get("narration", "")).strip()
                if not narration:
                    raise ValueError('"narration" was empty')
                if need_meta and not str(payload.get("title", "")).strip():
                    raise ValueError('"title" was empty')
                if attempt < SCRIPT_MAX_ATTEMPTS and len(narration) < min_chars // 2:
                    raise ValueError(
                        f"narration was only {len(narration)} characters; "
                        f"need about {min_chars}"
                    )
                return payload
            except ValueError as exc:
                last_error = str(exc)
                if attempt == SCRIPT_MAX_ATTEMPTS:
                    break
                log_warn(f"Chapter {chapter_index} was unusable ({last_error}). Asking again.")
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
            f"Chapter {chapter_index} failed after {SCRIPT_MAX_ATTEMPTS} attempt(s): {last_error}",
            hint="Try a larger model, fewer minutes, or a more concrete topic.",
        )
