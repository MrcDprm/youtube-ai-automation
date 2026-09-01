"""Draft scripts from a topic using a locally hosted language model via Ollama.

This module is the one place in the project that talks to a language model, and it is
deliberately kept out of the render path. ``main.py generate`` calls it to author a scenario
file; ``main.py run`` then consumes that file and never contacts a model. Two consequences
follow from that split: the render pipeline keeps its guarantee of making no model calls, and a
bad generation can be inspected and edited as plain JSON before a single frame is encoded.

The model is asked for only the creative parts — narration, search terms, title, tags. Every
structural field is filled in deterministically by :mod:`modules.scenario_builder`, so a small
quantised model cannot corrupt the resolution, codec settings or subtitle styling.
"""

from __future__ import annotations

import json
import re
from typing import Any, Final

import requests

from config.constants import (
    OLLAMA_CHAT_PATH,
    OLLAMA_TAGS_PATH,
    SCRIPT_MAX_ATTEMPTS,
    SCRIPT_MAX_SEARCH_TERMS,
    SCRIPT_MAX_TAGS,
    SCRIPT_NARRATION_MAX_CHARS,
    USER_AGENT,
    YOUTUBE_DESCRIPTION_MAX_CHARS,
    YOUTUBE_TAGS_MAX_TOTAL_CHARS,
    YOUTUBE_TITLE_MAX_CHARS,
)
from modules.interfaces import DraftScene, DraftScript, IScriptGenerator
from utils.exceptions import ScriptGenerationError
from utils.logger import get_logger, log_info, log_warn
from utils.retry import retry_http_call

__all__ = ["OllamaScriptGenerator", "extract_json_object"]

logger = get_logger(__name__)

_LANGUAGE_NAMES: Final[dict[str, str]] = {
    "tr": "Turkish",
    "en": "English",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "it": "Italian",
    "ar": "Arabic",
    "ru": "Russian",
}

_MARKDOWN_CHARS: Final[re.Pattern[str]] = re.compile(r"[*_`#>\[\]]")
_LIST_PREFIX: Final[re.Pattern[str]] = re.compile(r"^\s*(?:\d+[.)]|[-–—•])\s*")
_SPEAKER_PREFIX: Final[re.Pattern[str]] = re.compile(
    r"^\s*(?:sahne|scene|narrator|anlat[ıi]c[ıi]|voice[- ]?over)\s*\d*\s*[:\-]\s*",
    re.IGNORECASE,
)
_WHITESPACE: Final[re.Pattern[str]] = re.compile(r"\s+")
_EMOJI: Final[re.Pattern[str]] = re.compile(
    "[\U0001f300-\U0001faff\U00002600-\U000027bf\U0001f000-\U0001f2ff\ufe0f]"
)

_SYSTEM_PROMPT: Final[str] = """\
You are a scriptwriter for short narrated documentary videos.

Reply with a single JSON object and nothing else. No prose, no markdown, no code fences.

Required shape:
{{
  "title": string,
  "description": string,
  "tags": [string],
  "scenes": [{{"narration": string, "search_terms": [string]}}]
}}

Rules:
- "scenes" must contain exactly {scene_count} objects, in narrative order.
- "narration" must be written in {language}. One or two spoken sentences, at most \
{narration_max} characters. Plain prose only: no markdown, no emoji, no numbering, no speaker \
labels, no stage directions.
- Each scene must advance the story. Never restate an earlier scene.
- "search_terms" must be in ENGLISH, {min_terms} to {max_terms} items, each 2 to 4 words \
naming a concrete filmable subject such as an object, place or action. These are queries sent \
to a stock footage library, so avoid abstract nouns that cannot be photographed.
- "title" must be in {language} and at most {title_max} characters.
- "description" must be in {language}, two or three sentences.
- "tags" must be 5 to {max_tags} short lowercase keywords in {language}.
"""


def extract_json_object(text: str) -> dict[str, Any]:
    """Pull the first complete JSON object out of a model response.

    Even when asked for pure JSON, models wrap output in code fences or add a sentence of
    commentary, so the raw text is scanned for the first brace-balanced object rather than
    handed straight to :func:`json.loads`.

    Args:
        text: The raw assistant message.

    Returns:
        The decoded object.

    Raises:
        ValueError: If no balanced JSON object is present, or it does not decode.
    """
    start = text.find("{")
    if start < 0:
        raise ValueError("the reply contained no JSON object")

    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                candidate = text[start : index + 1]
                try:
                    decoded = json.loads(candidate)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"the JSON object did not decode: {exc}") from exc
                if not isinstance(decoded, dict):
                    raise ValueError("the top level JSON value was not an object")
                return decoded

    raise ValueError("the JSON object was truncated before it closed")


class OllamaScriptGenerator(IScriptGenerator):
    """Drafts scripts with a model served by a local Ollama instance."""

    def __init__(
        self,
        host: str,
        model: str,
        *,
        timeout: float = 180.0,
        max_attempts: int = SCRIPT_MAX_ATTEMPTS,
        temperature: float = 0.8,
        session: requests.Session | None = None,
    ) -> None:
        """Initialise the generator.

        Args:
            host: Base URL of the Ollama server, without a trailing slash.
            model: Model tag to run, for example ``"qwen2.5:7b-instruct"``.
            timeout: Per-request timeout. Local generation on CPU is slow, so this is generous.
            max_attempts: How many times to ask before giving up, counting the first try.
            temperature: Sampling temperature; higher values vary the wording more.
            session: Optional shared HTTP session.

        Raises:
            ScriptGenerationError: If ``host`` or ``model`` is empty.
        """
        if not host.strip():
            raise ScriptGenerationError("OLLAMA_HOST is empty.")
        if not model.strip():
            raise ScriptGenerationError(
                "OLLAMA_MODEL is empty.",
                hint="Set OLLAMA_MODEL in .env, for example qwen2.5:7b-instruct.",
            )

        self._host = host.rstrip("/")
        self._model = model.strip()
        self._timeout = timeout
        self._max_attempts = max(1, max_attempts)
        self._temperature = temperature
        self._session = session or requests.Session()
        self._session.headers.update({"User-Agent": USER_AGENT})

    # -- Public API ----------------------------------------------------------------------

    def available_models(self) -> list[str]:
        """List models installed on the Ollama server.

        Returns:
            Model tags, empty when the server is running but has nothing pulled.

        Raises:
            ScriptGenerationError: If the server cannot be reached.
        """
        url = f"{self._host}{OLLAMA_TAGS_PATH}"
        try:
            response = self._session.get(url, timeout=min(self._timeout, 10.0))
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as exc:
            raise ScriptGenerationError(
                f"Could not reach Ollama at {self._host}: {exc}",
                hint=(
                    "Install it from https://ollama.com and make sure the service is running. "
                    "Check with 'ollama list'."
                ),
            ) from exc
        except ValueError as exc:
            raise ScriptGenerationError(
                f"Ollama returned a non-JSON model list from {url}."
            ) from exc

        if not isinstance(payload, dict):
            return []
        models = payload.get("models")
        if not isinstance(models, list):
            return []
        return [
            str(entry["name"]) for entry in models if isinstance(entry, dict) and entry.get("name")
        ]

    def generate(
        self,
        topic: str,
        *,
        scene_count: int,
        language: str = "tr",
        extra_guidance: str | None = None,
    ) -> DraftScript:
        """Draft a script, re-prompting with the validation error when output is unusable.

        Args:
            topic: What the video should be about.
            scene_count: How many scenes to produce.
            language: Narration language code, for example ``"tr"``.
            extra_guidance: Optional extra steering appended to the request.

        Returns:
            A validated draft script.

        Raises:
            ScriptGenerationError: If the topic is blank, or no attempt yields usable output.
        """
        if not topic.strip():
            raise ScriptGenerationError("The topic is empty; there is nothing to write about.")

        messages = self._build_messages(topic, scene_count, language, extra_guidance)
        last_error = "no attempt was made"

        for attempt in range(1, self._max_attempts + 1):
            log_info(
                f"Asking {self._model} for {scene_count} scene(s) "
                f"(attempt {attempt}/{self._max_attempts})..."
            )
            reply = self._chat(messages, scene_count)

            try:
                payload = extract_json_object(reply)
                return self._coerce(
                    payload,
                    scene_count=scene_count,
                    accept_short=attempt == self._max_attempts,
                )
            except ValueError as exc:
                last_error = str(exc)
                logger.debug("Attempt %d produced unusable output: %s", attempt, last_error)
                if attempt == self._max_attempts:
                    break
                log_warn(f"The model's reply was unusable ({last_error}). Asking again.")
                messages = [
                    *messages,
                    {"role": "assistant", "content": reply[:2000]},
                    {
                        "role": "user",
                        "content": (
                            f"That reply was rejected because {last_error}. "
                            "Send the corrected JSON object only, with no other text."
                        ),
                    },
                ]

        raise ScriptGenerationError(
            f"{self._model} did not return a usable script after "
            f"{self._max_attempts} attempt(s): {last_error}",
            hint=(
                "Try a larger or instruction-tuned model, lower the scene count, or rephrase "
                "the topic. Smaller quantised models often struggle to hold a JSON shape."
            ),
        )

    # -- Prompting -----------------------------------------------------------------------

    @staticmethod
    def _build_messages(
        topic: str,
        scene_count: int,
        language: str,
        extra_guidance: str | None,
    ) -> list[dict[str, str]]:
        """Assemble the chat messages for a generation request.

        Args:
            topic: The subject of the video.
            scene_count: Requested number of scenes.
            language: Narration language code.
            extra_guidance: Optional extra steering.

        Returns:
            The message list to post.
        """
        language_name = _LANGUAGE_NAMES.get(language.lower(), language)
        system = _SYSTEM_PROMPT.format(
            scene_count=scene_count,
            language=language_name,
            narration_max=SCRIPT_NARRATION_MAX_CHARS,
            min_terms=min(2, SCRIPT_MAX_SEARCH_TERMS),
            max_terms=SCRIPT_MAX_SEARCH_TERMS,
            title_max=YOUTUBE_TITLE_MAX_CHARS,
            max_tags=SCRIPT_MAX_TAGS,
        )

        request = f"Write the script for a short video about: {topic.strip()}"
        if extra_guidance and extra_guidance.strip():
            request += f"\n\nAdditional direction: {extra_guidance.strip()}"

        return [
            {"role": "system", "content": system},
            {"role": "user", "content": request},
        ]

    def _chat(self, messages: list[dict[str, str]], scene_count: int) -> str:
        """Send one chat completion request and return the assistant's text.

        Args:
            messages: The conversation so far.
            scene_count: Used to size the output token budget.

        Returns:
            The raw assistant message content.

        Raises:
            ScriptGenerationError: If the server is unreachable, the model is missing, or the
                response envelope is malformed.
        """
        payload: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "stream": False,
            # Constrains sampling to syntactically valid JSON on Ollama builds that support it;
            # older builds ignore it, which is why extract_json_object still repairs the text.
            "format": "json",
            "options": {
                "temperature": self._temperature,
                "num_predict": min(8192, 400 + scene_count * 200),
            },
        }

        try:
            response = retry_http_call(
                self._post_once,
                f"{self._host}{OLLAMA_CHAT_PATH}",
                payload,
                max_attempts=2,
            )
        except requests.HTTPError as exc:
            raise self._http_error(exc) from exc
        except requests.RequestException as exc:
            raise ScriptGenerationError(
                f"Could not reach Ollama at {self._host}: {exc}",
                hint=(
                    "Start the Ollama service and confirm the model is pulled with "
                    f"'ollama pull {self._model}'."
                ),
            ) from exc

        try:
            envelope = response.json()
        except ValueError as exc:
            raise ScriptGenerationError("Ollama returned a non-JSON response envelope.") from exc

        if not isinstance(envelope, dict):
            raise ScriptGenerationError("Ollama returned a non-object response envelope.")

        message = envelope.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, str) or not content.strip():
            raise ScriptGenerationError(
                "Ollama returned an empty message.",
                hint=(
                    "This usually means the model was still loading or ran out of memory. "
                    "Try a smaller model."
                ),
            )
        return content

    def _post_once(self, url: str, payload: dict[str, Any]) -> requests.Response:
        """Perform one POST, surfacing non-success statuses as exceptions.

        Args:
            url: The chat endpoint.
            payload: The JSON request body.

        Returns:
            The successful response.

        Raises:
            requests.HTTPError: On any non-success status.
        """
        response = self._session.post(url, json=payload, timeout=self._timeout)
        response.raise_for_status()
        return response

    def _http_error(self, exc: requests.HTTPError) -> ScriptGenerationError:
        """Translate an HTTP failure into a diagnosis the user can act on.

        Args:
            exc: The raised HTTP error.

        Returns:
            The error to raise.
        """
        status = exc.response.status_code if exc.response is not None else 0
        if status == 404:
            return ScriptGenerationError(
                f"Ollama does not have the model '{self._model}'.",
                hint=f"Pull it first: ollama pull {self._model}",
            )
        return ScriptGenerationError(
            f"Ollama rejected the request with HTTP {status}.",
            hint="Run 'ollama list' to confirm the server is healthy and the model is present.",
        )

    # -- Validation and cleanup ----------------------------------------------------------

    def _coerce(
        self,
        payload: dict[str, Any],
        *,
        scene_count: int,
        accept_short: bool,
    ) -> DraftScript:
        """Clean and validate a decoded model payload.

        Args:
            payload: The decoded JSON object.
            scene_count: How many scenes were requested.
            accept_short: On the final attempt, take fewer scenes than requested rather than
                discarding an otherwise usable script.

        Returns:
            The validated draft.

        Raises:
            ValueError: With a message phrased for the model, so the repair prompt is specific.
        """
        raw_scenes = payload.get("scenes")
        if not isinstance(raw_scenes, list) or not raw_scenes:
            raise ValueError('"scenes" was missing or not a non-empty array')

        scenes: list[DraftScene] = []
        for index, entry in enumerate(raw_scenes[:scene_count], start=1):
            if not isinstance(entry, dict):
                raise ValueError(f"scene {index} was not an object")

            narration = self._clean_narration(str(entry.get("narration", "")))
            if not narration:
                raise ValueError(f'scene {index} had an empty "narration"')

            terms = self._clean_terms(entry.get("search_terms"))
            if not terms:
                raise ValueError(f'scene {index} had no usable English "search_terms"')

            scenes.append(DraftScene(narration=narration, search_terms=terms))

        if len(scenes) < scene_count and not accept_short:
            raise ValueError(
                f"only {len(scenes)} scene(s) were returned but exactly {scene_count} are required"
            )

        title = self._collapse(str(payload.get("title", "")))[:YOUTUBE_TITLE_MAX_CHARS].strip()
        if not title:
            raise ValueError('"title" was empty')

        description = str(payload.get("description", "")).strip()[:YOUTUBE_DESCRIPTION_MAX_CHARS]

        if len(scenes) < scene_count:
            log_warn(
                f"The model returned {len(scenes)} scene(s) instead of {scene_count}. "
                "Continuing with what it produced."
            )

        return DraftScript(
            title=title,
            description=description,
            tags=self._clean_tags(payload.get("tags")),
            scenes=tuple(scenes),
        )

    @staticmethod
    def _collapse(text: str) -> str:
        """Collapse all whitespace runs into single spaces.

        Args:
            text: Arbitrary text.

        Returns:
            The text with normalised spacing.
        """
        return _WHITESPACE.sub(" ", text).strip()

    @classmethod
    def _clean_narration(cls, text: str, *, max_chars: int = SCRIPT_NARRATION_MAX_CHARS) -> str:
        """Strip model artefacts from a narration line and cap its length.

        Args:
            text: The raw narration.
            max_chars: Soft ceiling. Story chapters pass a much larger value; Shorts keeps 320.

        Returns:
            Speakable prose, truncated at a sentence or word boundary when over the ceiling.
        """
        cleaned = _EMOJI.sub("", text)
        cleaned = _SPEAKER_PREFIX.sub("", cleaned)
        cleaned = _LIST_PREFIX.sub("", cleaned)
        cleaned = _MARKDOWN_CHARS.sub("", cleaned)
        cleaned = cls._collapse(cleaned).strip('"“”')

        if len(cleaned) <= max_chars:
            return cleaned

        window = cleaned[:max_chars]
        for boundary in (". ", "! ", "? "):
            cut = window.rfind(boundary)
            if cut > max_chars // 2:
                return window[: cut + 1].strip()
        cut = window.rfind(" ")
        return (window[:cut] if cut > 0 else window).strip()

    @classmethod
    def _clean_terms(cls, raw: Any) -> tuple[str, ...]:
        """Normalise the search-term list, dropping anything unusable.

        Args:
            raw: The value the model supplied for ``search_terms``.

        Returns:
            Up to :data:`SCRIPT_MAX_SEARCH_TERMS` distinct terms, possibly empty.
        """
        if isinstance(raw, str):
            raw = [raw]
        if not isinstance(raw, list):
            return ()

        seen: set[str] = set()
        terms: list[str] = []
        for item in raw:
            term = cls._collapse(_MARKDOWN_CHARS.sub("", str(item)))
            if not term or len(term) < 3:
                continue
            key = term.lower()
            if key in seen:
                continue
            seen.add(key)
            terms.append(term)
            if len(terms) >= SCRIPT_MAX_SEARCH_TERMS:
                break
        return tuple(terms)

    @classmethod
    def _clean_tags(cls, raw: Any) -> tuple[str, ...]:
        """Normalise tags, deduplicating and honouring YouTube's total length budget.

        Args:
            raw: The value the model supplied for ``tags``.

        Returns:
            Tags that fit within the API's combined character limit.
        """
        if isinstance(raw, str):
            raw = [part.strip() for part in raw.split(",")]
        if not isinstance(raw, list):
            return ()

        seen: set[str] = set()
        tags: list[str] = []
        budget = 0
        for item in raw:
            tag = cls._collapse(_MARKDOWN_CHARS.sub("", str(item))).lower()
            if not tag or tag in seen:
                continue
            # Mirrors the scenario validator's accounting so a generated file never trips it.
            cost = len(tag) + 1
            if budget + cost > YOUTUBE_TAGS_MAX_TOTAL_CHARS:
                break
            seen.add(tag)
            tags.append(tag)
            budget += cost
            if len(tags) >= SCRIPT_MAX_TAGS:
                break
        return tuple(tags)
