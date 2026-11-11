"""edge-tts failure handling: a rejected handshake fails fast with an actionable hint."""

from __future__ import annotations

import asyncio
from pathlib import Path

import aiohttp
import pytest
from multidict import CIMultiDict, CIMultiDictProxy
from yarl import URL

from models.scenario import TTSSettings
from modules.interfaces import WordCue
from modules.tts import EdgeTTSEngine, _is_retryable_tts_error
from utils.exceptions import TTSError

SPEECH_URL = URL("wss://speech.example.invalid/edge/v1?TrustedClientToken=secret-token")


def _handshake_error(status: int) -> aiohttp.WSServerHandshakeError:
    """Build the error aiohttp raises when the websocket upgrade is answered with ``status``."""
    headers = CIMultiDictProxy(CIMultiDict[str]())
    info = aiohttp.RequestInfo(SPEECH_URL, "GET", headers, SPEECH_URL)
    return aiohttp.WSServerHandshakeError(
        info, (), status=status, message="Invalid response status"
    )


def test_rejected_handshake_fails_after_one_attempt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """HTTP 403 means edge-tts is outdated; four attempts would only add delay."""
    engine = EdgeTTSEngine(tmp_path / "tts", max_attempts=4)
    calls = {"count": 0}

    async def rejected(text: str, tts: TTSSettings) -> tuple[bytes, list[WordCue]]:
        calls["count"] += 1
        raise _handshake_error(403)

    monkeypatch.setattr(engine, "_stream_once", rejected)

    with pytest.raises(TTSError, match="403") as caught:
        asyncio.run(engine._synthesize_with_retry("Merhaba.", TTSSettings()))

    assert calls["count"] == 1
    assert caught.value.hint is not None
    assert "pip install -U edge-tts" in caught.value.hint
    assert "secret-token" not in str(caught.value)


def test_only_the_rejected_handshake_skips_retries() -> None:
    """Other server answers and network errors are still treated as transient."""
    assert not _is_retryable_tts_error(_handshake_error(403))
    assert _is_retryable_tts_error(_handshake_error(503))
    assert _is_retryable_tts_error(ConnectionError("connection reset"))
