"""Draft scripts with Google's Gemini API.

Gemini is reached over plain REST with ``requests``, the way the rest of the project talks to
web services, so no extra SDK is needed and tests stub HTTP with ``requests-mock``. The API key
travels in the ``x-goog-api-key`` header and never in the URL, because URLs end up in logs and
exception messages.

By default the model writes from what it knows and is told to leave out anything it is not
sure of. Grounding with Google Search is an opt-in: since November 2026 it needs Gemini's paid
tier for new keys. With it on, Gemini searches while it writes and reports the pages it relied
on; those pages are kept on the draft as sources for the author to check, listed in the
scenario file but never spoken and never published.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from typing import Any, Final
from urllib.parse import quote, urlparse

import requests

from config.constants import (
    GEMINI_API_BASE,
    GEMINI_DEFAULT_MODEL,
    SCRIPT_MAX_ATTEMPTS,
    SCRIPT_MAX_SOURCES,
    SOURCE_TITLE_MAX_CHARS,
    SOURCE_URL_MAX_CHARS,
    USER_AGENT,
)
from modules.interfaces import DraftScript, DraftSource
from modules.script_generator import ChatScriptGenerator
from utils.exceptions import ScriptGenerationError
from utils.logger import get_logger, log_info, log_warn
from utils.retry import retry_http_call

__all__ = ["GeminiScriptGenerator"]

logger = get_logger(__name__)

KEY_PAGE: Final[str] = "https://aistudio.google.com/apikey"
ERROR_DETAIL_MAX_CHARS: Final[int] = 300
MODEL_LIST_MAX_PAGES: Final[int] = 10

_FALLBACK_STATUSES: Final[frozenset[int]] = frozenset({404, 408, 429, 500, 502, 503, 504})
"""Failures that belong to one model, so the next model in the list is worth a try."""


class _ModelUnavailableError(Exception):
    """One model could not answer; carries the error to raise if no other model can."""

    def __init__(self, error: ScriptGenerationError) -> None:
        super().__init__(error.message)
        self.error = error


_GROUNDING_RULES: Final[str] = """\
Fact checking:
- Use Google Search to confirm every factual claim before you write it.
- Leave out anything you cannot confirm from a reliable source. Never present a rumour, a mod
or a guess as fact.
- Still reply with the single JSON object described above and nothing else."""

_MEMORY_RULES: Final[str] = """\
Facts:
- You cannot search the web, so use only facts you are certain of.
- If you are unsure of a detail, leave it out instead of guessing. Never present a rumour, a mod
or a guess as fact, and never invent numbers, dates or names."""


class GeminiScriptGenerator(ChatScriptGenerator):
    """Drafts scripts with Gemini, optionally grounding every fact in Google Search."""

    def __init__(
        self,
        api_key: str,
        model: str = GEMINI_DEFAULT_MODEL,
        *,
        fallback_models: Sequence[str] = (),
        grounding: bool = False,
        timeout: float = 60.0,
        max_attempts: int = SCRIPT_MAX_ATTEMPTS,
        temperature: float = 0.7,
        session: requests.Session | None = None,
    ) -> None:
        """Initialise the generator.

        Args:
            api_key: A Gemini API key from Google AI Studio.
            model: The model to run, for example ``"gemini-3.5-flash-lite"``.
            fallback_models: Models to try, in order, when the current one is busy, out of
                quota, retired or too slow. Free-tier capacity changes by the hour.
            grounding: Let the model check facts with Google Search and report its sources.
                Needs Gemini's paid tier for new keys.
            timeout: Per-request timeout, kept short so a stuck model hands over quickly.
            max_attempts: How many times to ask before giving up, counting the first try.
            temperature: Sampling temperature. Newer models ignore it.
            session: Optional shared HTTP session.

        Raises:
            ScriptGenerationError: If ``api_key`` or ``model`` is empty.
        """
        if not api_key.strip():
            raise ScriptGenerationError(
                "GEMINI_API_KEY is empty.",
                hint=f"Create a free key at {KEY_PAGE} and add it to .env.",
            )
        if not model.strip():
            raise ScriptGenerationError(
                "GEMINI_MODEL is empty.",
                hint=f"Set GEMINI_MODEL in .env, for example {GEMINI_DEFAULT_MODEL}.",
            )
        super().__init__(model, max_attempts=max_attempts)
        fallbacks = (name.strip() for name in fallback_models if name.strip())
        self._models = list(dict.fromkeys([self._model, *fallbacks]))
        # The key goes on each Gemini request, not on the session, so a shared session can
        # never carry it to another host.
        self._headers = {"x-goog-api-key": api_key.strip()}
        self._grounding = grounding
        self._timeout = timeout
        self._temperature = temperature
        self._session = session or requests.Session()
        self._session.headers.update({"User-Agent": USER_AGENT})
        self._sources: list[DraftSource] = []

    # -- Public API ---------------------------------------------------------------------

    def generate(
        self,
        topic: str,
        *,
        scene_count: int,
        language: str = "tr",
        extra_guidance: str | None = None,
    ) -> DraftScript:
        """Draft a script and attach the pages Gemini relied on.

        Args:
            topic: What the video should be about.
            scene_count: How many scenes to produce.
            language: Narration language code, for example ``"tr"``.
            extra_guidance: Optional extra steering appended to the request.

        Returns:
            A validated draft whose ``sources`` come from the accepted reply.

        Raises:
            ScriptGenerationError: If the topic is blank, the API fails, or no attempt
                yields usable output.
        """
        self._sources = []
        draft = super().generate(
            topic, scene_count=scene_count, language=language, extra_guidance=extra_guidance
        )
        return replace(draft, sources=tuple(self._sources))

    def available_models(self) -> list[str]:
        """List the models this key may use to generate text.

        Returns:
            Model ids such as ``"gemini-2.5-flash-lite"``.

        Raises:
            ScriptGenerationError: If the API cannot be reached or rejects the key.
        """
        names: list[str] = []
        token: str | None = None
        for _ in range(MODEL_LIST_MAX_PAGES):
            params: dict[str, Any] = {"pageSize": 100}
            if token:
                params["pageToken"] = token
            try:
                response = self._session.get(
                    f"{GEMINI_API_BASE}/models",
                    params=params,
                    headers=self._headers,
                    timeout=min(self._timeout, 15.0),
                )
                response.raise_for_status()
                payload = response.json()
            except requests.HTTPError as exc:
                raise self._http_error(exc) from exc
            except requests.RequestException as exc:
                raise ScriptGenerationError(
                    f"Could not reach the Gemini API: {exc}",
                    hint="Check your internet connection and any proxy or firewall rules.",
                ) from exc
            except ValueError as exc:
                raise ScriptGenerationError(
                    "The Gemini API returned a non-JSON model list."
                ) from exc

            entries = payload.get("models") if isinstance(payload, dict) else None
            for entry in entries if isinstance(entries, list) else []:
                if not isinstance(entry, dict):
                    continue
                methods = entry.get("supportedGenerationMethods") or []
                name = str(entry.get("name", "")).removeprefix("models/")
                if name and "generateContent" in methods:
                    names.append(name)
            token = payload.get("nextPageToken") if isinstance(payload, dict) else None
            if not token:
                break
        return names

    # -- Transport ----------------------------------------------------------------------

    def _chat(self, messages: list[dict[str, str]], scene_count: int) -> str:
        """Send the conversation to Gemini and return its text, falling back across models.

        The model that answered last is tried first, then the others in their configured
        order. A model is skipped when it is busy, out of quota, retired or too slow; any
        other failure, such as a rejected key or a blocked prompt, stops at once, because the
        next model would fail the same way.

        Args:
            messages: The conversation so far.
            scene_count: Unused: Gemini's default output budget fits every scene count.

        Returns:
            The reply text, with the reply's grounding sources stored for :meth:`generate`.

        Raises:
            ScriptGenerationError: If no model answers, or the answer is blocked or empty.
        """
        del scene_count
        body = self._request_body(messages)
        order = [self._model, *(model for model in self._models if model != self._model)]
        failure: ScriptGenerationError | None = None
        for index, model in enumerate(order):
            try:
                envelope = self._post_model(model, body)
            except _ModelUnavailableError as exc:
                failure = exc.error
                if index + 1 < len(order):
                    log_warn(
                        f"{model} is unavailable ({exc.error.message}). Trying {order[index + 1]}."
                    )
                continue
            if model != self._model:
                log_info(f"{model} answered; it goes first from now on.")
                self._model = model
            return self._read_reply(envelope)

        assert failure is not None
        raise failure

    def _post_model(self, model: str, body: dict[str, Any]) -> Any:
        """Send one request to one model and decode the reply.

        Args:
            model: The model to call.
            body: The JSON request body.

        Returns:
            The decoded response envelope.

        Raises:
            _ModelUnavailableError: If this model is busy, out of quota, retired or too slow.
            ScriptGenerationError: For failures another model would hit too.
        """
        url = f"{GEMINI_API_BASE}/models/{quote(model, safe='')}:generateContent"
        try:
            response = retry_http_call(self._post_once, url, body, max_attempts=2)
        except requests.HTTPError as exc:
            error = self._http_error(exc, model)
            status = exc.response.status_code if exc.response is not None else 0
            if status in _FALLBACK_STATUSES:
                raise _ModelUnavailableError(error) from exc
            raise error from exc
        except requests.RequestException as exc:
            raise _ModelUnavailableError(
                ScriptGenerationError(
                    f"Could not get an answer from {model}: {exc}",
                    hint="Check your internet connection and any proxy or firewall rules.",
                )
            ) from exc

        try:
            return response.json()
        except ValueError as exc:
            raise ScriptGenerationError("The Gemini API returned a non-JSON response.") from exc

    def _request_body(self, messages: list[dict[str, str]]) -> dict[str, Any]:
        """Translate the shared chat messages into Gemini's request shape.

        System messages become the system instruction, and ``assistant`` turns become
        Gemini's ``model`` role, which the repair loop needs when it quotes a rejected reply.

        Args:
            messages: The conversation so far.

        Returns:
            The JSON body for ``generateContent``.
        """
        system = [message["content"] for message in messages if message["role"] == "system"]
        system.append(_GROUNDING_RULES if self._grounding else _MEMORY_RULES)
        body: dict[str, Any] = {
            "contents": [
                {
                    "role": "model" if message["role"] == "assistant" else "user",
                    "parts": [{"text": message["content"]}],
                }
                for message in messages
                if message["role"] != "system"
            ],
            "generationConfig": {"temperature": self._temperature},
        }
        if system:
            body["systemInstruction"] = {"parts": [{"text": "\n\n".join(system)}]}
        if self._grounding:
            body["tools"] = [{"googleSearch": {}}]
        else:
            # Strict JSON output cannot be combined with search, so it is used only without it.
            body["generationConfig"]["responseMimeType"] = "application/json"
        return body

    def _post_once(self, url: str, body: dict[str, Any]) -> requests.Response:
        """Perform one POST, surfacing non-success statuses as exceptions.

        Args:
            url: The ``generateContent`` endpoint.
            body: The JSON request body.

        Returns:
            The successful response.

        Raises:
            requests.HTTPError: On any non-success status.
        """
        response = self._session.post(url, json=body, headers=self._headers, timeout=self._timeout)
        response.raise_for_status()
        return response

    def _read_reply(self, envelope: Any) -> str:
        """Pull the text and the grounding sources out of a ``generateContent`` reply.

        Args:
            envelope: The decoded response body.

        Returns:
            The reply text.

        Raises:
            ScriptGenerationError: If the prompt was blocked or no text came back.
        """
        if not isinstance(envelope, dict):
            raise ScriptGenerationError("The Gemini API returned a non-object response.")

        feedback = envelope.get("promptFeedback")
        if isinstance(feedback, dict) and feedback.get("blockReason"):
            raise ScriptGenerationError(
                f"Gemini refused the request ({feedback['blockReason']}).",
                hint="Rephrase the topic or the guidance.",
            )

        candidates = envelope.get("candidates")
        candidate = candidates[0] if isinstance(candidates, list) and candidates else None
        if not isinstance(candidate, dict):
            raise ScriptGenerationError(
                "Gemini returned no answer.", hint="Try again, or rephrase the topic."
            )

        content = candidate.get("content")
        parts = content.get("parts") if isinstance(content, dict) else None
        text = "".join(
            str(part.get("text", ""))
            for part in (parts if isinstance(parts, list) else [])
            if isinstance(part, dict) and not part.get("thought")
        )
        if not text.strip():
            reason = candidate.get("finishReason") or "unknown"
            raise ScriptGenerationError(
                f"Gemini returned an empty answer (finish reason {reason}).",
                hint="Try again. A SAFETY finish reason means the topic was filtered.",
            )

        self._sources = _grounding_sources(candidate.get("groundingMetadata"))
        if self._grounding and not self._sources:
            logger.warning("Gemini answered without citing any web page.")
        return text

    def _http_error(
        self, exc: requests.HTTPError, model: str | None = None
    ) -> ScriptGenerationError:
        """Translate an HTTP failure into a diagnosis the user can act on.

        Args:
            exc: The raised HTTP error.
            model: The model that was called, when the request named one.

        Returns:
            The error to raise. It never contains the API key, which only travels in a header.
        """
        status = exc.response.status_code if exc.response is not None else 0
        detail = _api_error_message(exc.response)
        if "api key" in detail.lower() or status == 401:
            return ScriptGenerationError(
                "Gemini rejected the API key.",
                hint=f"Check GEMINI_API_KEY in .env, or create a new free key at {KEY_PAGE}.",
            )
        if status == 404:
            # Google answers 404 both for unknown models and for retired ones, and only the
            # message says which, often naming the replacement, so it is passed on as is.
            return ScriptGenerationError(
                f"Gemini cannot run the model '{model or self._model}': {detail}",
                hint=f"Set GEMINI_MODEL in .env, for example {GEMINI_DEFAULT_MODEL}.",
            )
        if status == 429:
            hint = "Wait a minute for the per-minute limit, or until tomorrow for the daily one."
            if self._grounding:
                hint = (
                    "Google Search grounding needs Gemini's paid tier for new keys. Set "
                    "GEMINI_GROUNDING=false to write without it."
                )
            return ScriptGenerationError(f"Gemini's quota is used up: {detail}", hint=hint)
        if status == 503:
            return ScriptGenerationError(
                f"Gemini is overloaded right now: {detail}",
                hint=(
                    "Try again in a few minutes, or list more models in GEMINI_MODEL, separated "
                    "by commas, so a busy one is skipped."
                ),
            )
        if status == 403:
            return ScriptGenerationError(
                f"Gemini refused access: {detail}",
                hint="Check that the key's project has the Gemini API enabled.",
            )
        return ScriptGenerationError(f"Gemini rejected the request with HTTP {status}: {detail}")


def _api_error_message(response: requests.Response | None) -> str:
    """Read the human-readable message from a Gemini error body.

    Args:
        response: The failed response, if any.

    Returns:
        The message, shortened, or a placeholder when the body has none.
    """
    if response is None:
        return "no response"
    try:
        payload = response.json()
    except ValueError:
        return (response.text or "no details").strip()[:ERROR_DETAIL_MAX_CHARS]
    error = payload.get("error") if isinstance(payload, dict) else None
    message = error.get("message") if isinstance(error, dict) else None
    return str(message or "no details").strip()[:ERROR_DETAIL_MAX_CHARS]


def _grounding_sources(metadata: Any) -> list[DraftSource]:
    """Collect the web pages a grounded reply relied on.

    Model output is not trusted: only http and https links survive, duplicates are dropped,
    titles are trimmed, and the list is capped.

    Args:
        metadata: The candidate's ``groundingMetadata``.

    Returns:
        Up to ``SCRIPT_MAX_SOURCES`` sources, in the order Gemini listed them.
    """
    chunks = metadata.get("groundingChunks") if isinstance(metadata, dict) else None
    sources: list[DraftSource] = []
    seen: set[str] = set()
    for chunk in chunks if isinstance(chunks, list) else []:
        web = chunk.get("web") if isinstance(chunk, dict) else None
        if not isinstance(web, dict):
            continue
        url = str(web.get("uri") or "").strip()
        if not url.startswith(("https://", "http://")) or len(url) > SOURCE_URL_MAX_CHARS:
            continue
        if url in seen:
            continue
        title = " ".join(str(web.get("title") or "").split()) or urlparse(url).netloc
        seen.add(url)
        sources.append(DraftSource(title=title[:SOURCE_TITLE_MAX_CHARS], url=url))
        if len(sources) >= SCRIPT_MAX_SOURCES:
            break
    return sources
