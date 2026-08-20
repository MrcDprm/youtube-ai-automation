"""Narration synthesis with edge-tts.

A single streaming request yields both the MP3 bytes and the word-level timings, so subtitles
cost nothing extra: no Whisper, no second pass, no transcription API.

Two details of edge-tts 7.x drive this implementation. ``Communicate`` defaults to
``boundary="SentenceBoundary"``, so word timings only arrive when ``"WordBoundary"`` is
requested explicitly. And ``Communicate.stream()`` may be consumed only once per instance,
so every retry constructs a fresh object.
"""

from __future__ import annotations

import asyncio
import contextlib
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import edge_tts
from edge_tts.exceptions import EdgeTTSException

from config.constants import SYMBOL_EXPANSIONS, TURKISH_ABBREVIATIONS
from models.scenario import TTSSettings
from modules.interfaces import ITTSEngine, TTSResult, WordCue
from utils.exceptions import TTSError
from utils.fs import atomic_write_bytes, ensure_parent, hash_payload, read_json, write_json
from utils.logger import get_logger
from utils.media import probe_duration
from utils.retry import make_async_retrying

__all__ = ["EdgeTTSEngine", "normalize_narration"]

logger = get_logger(__name__)

TICKS_PER_SECOND = 10_000_000
"""edge-tts reports offsets in 100-nanosecond ticks."""

MIN_VALID_MP3_BYTES = 512
"""Anything smaller is a failed synthesis, not a short sentence."""

_EMOJI_PATTERN = re.compile(
    "["
    "\U0001f300-\U0001f5ff"
    "\U0001f600-\U0001f64f"
    "\U0001f680-\U0001f6ff"
    "\U0001f700-\U0001f77f"
    "\U0001f780-\U0001f7ff"
    "\U0001f800-\U0001f8ff"
    "\U0001f900-\U0001f9ff"
    "\U0001fa00-\U0001faff"
    "\u2600-\u26ff"
    "\u2700-\u27bf"
    "\u2b00-\u2bff"
    "\ufe0f"
    "]+",
    flags=re.UNICODE,
)

_MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
_MARKDOWN_EMPHASIS = re.compile(r"(\*{1,3}|_{1,3}|`{1,3}|~{2})")
_MARKDOWN_HEADING = re.compile(r"^\s{0,3}#{1,6}\s*", flags=re.MULTILINE)
_WHITESPACE = re.compile(r"\s+")
_SENTENCE_TERMINATORS = ".!?…:;"


def normalize_narration(text: str, *, expand_abbreviations: bool = True) -> str:
    """Clean narration text so the voice reads it naturally.

    Collapses whitespace, removes markdown and emoji that would otherwise be spelled out,
    expands common Turkish abbreviations and symbols, and guarantees terminal punctuation so
    the engine does not clip the final word.

    Args:
        text: Raw narration from the scenario.
        expand_abbreviations: Whether to expand abbreviations and symbols.

    Returns:
        Normalized text, ready to speak.

    Raises:
        TTSError: If nothing speakable remains after cleaning.
    """
    cleaned = _MARKDOWN_LINK.sub(r"\1", text)
    cleaned = _MARKDOWN_HEADING.sub("", cleaned)
    cleaned = _MARKDOWN_EMPHASIS.sub("", cleaned)
    cleaned = _EMOJI_PATTERN.sub(" ", cleaned)

    if expand_abbreviations:
        for abbreviation, expansion in TURKISH_ABBREVIATIONS.items():
            cleaned = cleaned.replace(abbreviation, expansion)
        for symbol, expansion in SYMBOL_EXPANSIONS.items():
            cleaned = cleaned.replace(symbol, expansion)

    cleaned = _WHITESPACE.sub(" ", cleaned).strip()

    if not cleaned:
        raise TTSError(
            "Narration is empty after normalization.",
            hint="The scene text contained only markup, emoji or whitespace.",
        )

    if cleaned[-1] not in _SENTENCE_TERMINATORS:
        cleaned += "."
    return cleaned


def _is_retryable_tts_error(exc: BaseException) -> bool:
    """Classify an edge-tts failure as transient.

    Args:
        exc: The exception raised during synthesis.

    Returns:
        ``True`` for websocket, network and empty-response failures, which usually succeed on
        a second attempt against Microsoft's free endpoint.
    """
    if isinstance(exc, EdgeTTSException | TimeoutError | ConnectionError | OSError):
        return True
    # aiohttp errors surface as their own hierarchy; match by module to avoid a hard import.
    return type(exc).__module__.startswith("aiohttp")


class EdgeTTSEngine(ITTSEngine):
    """Synthesizes narration with Microsoft Edge's free online voices.

    Results are cached under ``<cache_dir>/tts`` keyed by a SHA-256 of the text and every
    prosody parameter, so re-runs and crash recovery never re-synthesize unchanged scenes.
    Word timings are cached alongside the audio; without that, a cache hit would silently
    produce a video with no subtitles.
    """

    def __init__(
        self,
        cache_dir: Path,
        *,
        max_concurrency: int = 3,
        max_attempts: int = 4,
        force: bool = False,
    ) -> None:
        """Initialise the engine.

        Args:
            cache_dir: Directory for cached audio and timing sidecars.
            max_concurrency: Simultaneous synthesis requests. Microsoft throttles aggressive
                clients, so this stays low even when many scenes are queued.
            max_attempts: Total attempts per scene, including the first.
            force: When true, ignore cached results and re-synthesize.
        """
        self._cache_dir = cache_dir
        self._max_attempts = max_attempts
        self._force = force
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    # -- Public API ---------------------------------------------------------------------

    async def synthesize(self, text: str, out_path: Path, tts: TTSSettings) -> TTSResult:
        """Synthesize one narration segment.

        Concurrency is capped inside this method, so callers may launch every scene at once
        with ``asyncio.gather`` and still respect the engine's limit.

        Args:
            text: The narration to speak.
            out_path: Destination MP3 path.
            tts: Voice and prosody settings.

        Returns:
            The audio path, its measured duration and word-level timings.

        Raises:
            TTSError: If synthesis fails, or produces empty or implausibly small audio.
        """
        spoken = normalize_narration(text, expand_abbreviations=tts.normalize_text)
        cache_key = hash_payload("edge-tts-v1", spoken, tts.voice, tts.rate, tts.volume, tts.pitch)

        cached = self._load_from_cache(cache_key, out_path, tts.voice)
        if cached is not None:
            logger.debug("TTS cache hit %s for %s", cache_key[:12], out_path.name)
            return cached

        async with self._semaphore:
            audio, word_cues = await self._synthesize_with_retry(spoken, tts)

        self._validate_audio(audio, out_path)
        ensure_parent(out_path)
        atomic_write_bytes(out_path, audio)
        duration = probe_duration(out_path)

        self._store_in_cache(cache_key, audio, word_cues, duration, tts.voice)

        logger.info(
            "Synthesized %s: %.2fs, %d word cue(s), %d bytes",
            out_path.name,
            duration,
            len(word_cues),
            len(audio),
        )
        if not word_cues:
            logger.warning(
                "No word boundaries returned for %s; subtitles for this scene will be "
                "estimated from the audio duration instead.",
                out_path.name,
            )

        return TTSResult(
            audio_path=out_path,
            duration=duration,
            word_cues=word_cues,
            voice=tts.voice,
            cached=False,
        )

    async def list_voices(self, locale: str | None = None) -> list[dict[str, Any]]:
        """List the voices edge-tts offers.

        Args:
            locale: Optional filter. Accepts a full locale such as ``"tr-TR"`` or a bare
                language code such as ``"tr"``; matching is case-insensitive.

        Returns:
            Voice descriptors, sorted by short name.

        Raises:
            TTSError: If the voice list cannot be retrieved.
        """
        try:
            voices = await edge_tts.list_voices()
        except Exception as exc:
            raise TTSError(
                f"Could not retrieve the edge-tts voice list: {exc}",
                hint="This command needs internet access. Check your connection or proxy.",
            ) from exc

        # edge-tts yields TypedDict rows; copy them into plain dicts so callers can treat the
        # result as ordinary JSON-ish data.
        results: list[dict[str, Any]] = [dict(voice) for voice in voices]
        if locale:
            needle = locale.strip().lower()
            results = [
                voice
                for voice in results
                if str(voice.get("Locale", "")).lower() == needle
                or str(voice.get("Locale", "")).lower().startswith(f"{needle}-")
                or str(voice.get("ShortName", "")).lower().startswith(needle)
            ]
        return sorted(results, key=lambda voice: str(voice.get("ShortName", "")))

    # -- Synthesis ----------------------------------------------------------------------

    async def _synthesize_with_retry(
        self, text: str, tts: TTSSettings
    ) -> tuple[bytes, list[WordCue]]:
        """Run the streaming synthesis under the shared retry policy.

        A new ``Communicate`` is built inside each attempt because its stream can only be
        consumed once.

        Args:
            text: Normalized narration.
            tts: Voice and prosody settings.

        Returns:
            The raw MP3 bytes and the collected word cues.

        Raises:
            TTSError: If every attempt fails.
        """
        controller = make_async_retrying(
            max_attempts=self._max_attempts,
            predicate=_is_retryable_tts_error,
        )
        try:
            async for attempt in controller:
                with attempt:
                    return await self._stream_once(text, tts)
        except EdgeTTSException as exc:
            raise TTSError(
                f"edge-tts failed after {self._max_attempts} attempts: {exc}",
                hint=(
                    "Microsoft's free endpoint occasionally rejects clients. Retry in a "
                    "minute, or pick a different voice with 'python main.py voices'."
                ),
            ) from exc
        except Exception as exc:
            raise TTSError(
                f"Speech synthesis failed after {self._max_attempts} attempts: {exc}",
                hint="Check your internet connection and any proxy or firewall rules.",
            ) from exc

        raise TTSError("Speech synthesis produced no result.")

    async def _stream_once(self, text: str, tts: TTSSettings) -> tuple[bytes, list[WordCue]]:
        """Perform one streaming synthesis request.

        Args:
            text: Normalized narration.
            tts: Voice and prosody settings.

        Returns:
            The raw MP3 bytes and the word cues parsed from boundary events.

        Raises:
            TTSError: If edge-tts rejects the prosody arguments.
        """
        try:
            communicate = edge_tts.Communicate(
                text,
                voice=tts.voice,
                rate=tts.rate,
                volume=tts.volume,
                pitch=tts.pitch,
                boundary="WordBoundary",
            )
        except (ValueError, TypeError) as exc:
            raise TTSError(
                f"edge-tts rejected the voice settings: {exc}",
                hint=(
                    "rate and volume must look like '+8%' or '-10%', and pitch like '+0Hz'. "
                    f"Got rate={tts.rate!r}, volume={tts.volume!r}, pitch={tts.pitch!r}."
                ),
            ) from exc

        chunks: list[bytes] = []
        word_cues: list[WordCue] = []

        async for chunk in communicate.stream():
            kind = chunk.get("type")
            if kind == "audio":
                data = chunk.get("data")
                if data:
                    chunks.append(data)
            elif kind == "WordBoundary":
                cue = self._parse_word_boundary(chunk)
                if cue is not None:
                    word_cues.append(cue)

        return b"".join(chunks), word_cues

    @staticmethod
    def _parse_word_boundary(chunk: Mapping[str, Any]) -> WordCue | None:
        """Convert a boundary event into a :class:`WordCue`.

        Args:
            chunk: A ``WordBoundary`` chunk from the edge-tts stream.

        Returns:
            The parsed cue, or ``None`` when the event carries no usable text or timing.
        """
        text = str(chunk.get("text", "")).strip()
        if not text:
            return None
        try:
            offset = float(chunk["offset"]) / TICKS_PER_SECOND
            duration = float(chunk.get("duration", 0)) / TICKS_PER_SECOND
        except (KeyError, TypeError, ValueError):
            return None
        return WordCue(text=text, start=offset, end=offset + duration)

    @staticmethod
    def _validate_audio(audio: bytes, out_path: Path) -> None:
        """Reject empty or implausibly small synthesis output.

        A zero-byte MP3 is the classic silent edge-tts failure. Letting it through would
        produce a video with a silent scene and no error anywhere.

        Args:
            audio: The synthesized bytes.
            out_path: Destination path, named in the error message.

        Raises:
            TTSError: If the audio is empty or below the minimum plausible size.
        """
        if not audio:
            raise TTSError(
                f"edge-tts returned zero bytes of audio for {out_path.name}.",
                hint=(
                    "This usually means the voice name is wrong or the service refused the "
                    "request. Verify the voice with 'python main.py voices --locale tr-TR'."
                ),
            )
        if len(audio) < MIN_VALID_MP3_BYTES:
            raise TTSError(
                f"edge-tts returned only {len(audio)} bytes for {out_path.name}, "
                "which is too small to be valid speech.",
                hint="Retry the run; if it persists, try a different voice.",
            )

    # -- Cache --------------------------------------------------------------------------

    def _audio_cache_path(self, key: str) -> Path:
        """Return the cached MP3 path for a key."""
        return self._cache_dir / f"{key}.mp3"

    def _meta_cache_path(self, key: str) -> Path:
        """Return the cached timing sidecar path for a key."""
        return self._cache_dir / f"{key}.json"

    def _load_from_cache(self, key: str, out_path: Path, voice: str) -> TTSResult | None:
        """Return a cached synthesis, copying the audio into place.

        Args:
            key: Cache key.
            out_path: Where the caller expects the audio to live.
            voice: Voice name recorded on the result.

        Returns:
            The cached result, or ``None`` on a miss or when ``force`` is set.
        """
        if self._force:
            return None

        audio_path = self._audio_cache_path(key)
        meta_path = self._meta_cache_path(key)
        if not audio_path.is_file() or not meta_path.is_file():
            return None
        if audio_path.stat().st_size < MIN_VALID_MP3_BYTES:
            audio_path.unlink(missing_ok=True)
            meta_path.unlink(missing_ok=True)
            return None

        try:
            meta = read_json(meta_path)
            duration = float(meta["duration"])
            word_cues = [
                WordCue(text=item["text"], start=float(item["start"]), end=float(item["end"]))
                for item in meta.get("word_cues", [])
            ]
        except (OSError, KeyError, TypeError, ValueError) as exc:
            logger.debug("Discarding unreadable TTS cache entry %s: %s", key[:12], exc)
            meta_path.unlink(missing_ok=True)
            return None

        ensure_parent(out_path)
        atomic_write_bytes(out_path, audio_path.read_bytes())

        return TTSResult(
            audio_path=out_path,
            duration=duration,
            word_cues=word_cues,
            voice=voice,
            cached=True,
        )

    def _store_in_cache(
        self,
        key: str,
        audio: bytes,
        word_cues: list[WordCue],
        duration: float,
        voice: str,
    ) -> None:
        """Persist a synthesis result for future runs.

        Cache failures are logged and swallowed: a full disk should slow the next run down,
        not abort this one.

        Args:
            key: Cache key.
            audio: The synthesized MP3 bytes.
            word_cues: Word timings to store alongside the audio.
            duration: Measured audio duration.
            voice: Voice used, recorded for debugging.
        """
        try:
            atomic_write_bytes(self._audio_cache_path(key), audio)
            write_json(
                self._meta_cache_path(key),
                {
                    "voice": voice,
                    "duration": duration,
                    "word_cues": [
                        {"text": cue.text, "start": cue.start, "end": cue.end} for cue in word_cues
                    ],
                },
            )
        except OSError as exc:
            logger.warning("Could not write the TTS cache entry %s: %s", key[:12], exc)
            with contextlib.suppress(OSError):
                self._audio_cache_path(key).unlink(missing_ok=True)
                self._meta_cache_path(key).unlink(missing_ok=True)
