"""Gemini script generation: request shape, grounding sources, repair loop and errors."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import requests_mock as rm

from config.constants import GEMINI_API_BASE, GEMINI_DEFAULT_MODEL
from config.settings import Settings, get_settings
from models.scenario import Scenario
from modules.gemini_generator import GeminiScriptGenerator
from modules.scenario_builder import build_scenario
from modules.script_generator import OllamaScriptGenerator
from utils import preflight
from utils.exceptions import ConfigurationError, ScriptGenerationError

KEY = "test-key-never-real"
URL = f"{GEMINI_API_BASE}/models/{GEMINI_DEFAULT_MODEL}:generateContent"


def _script(scene_count: int = 2) -> dict[str, Any]:
    return {
        "title": "GTA 5 hakkında az bilinen bir detay",
        "description": "Kısa bir anlatım. Oyunda gizli bir ayrıntı.",
        "tags": ["gta 5", "gizli detay", "AI"],
        "scenes": [
            {
                "narration": f"Bu {index}. sahnede şaşırtıcı bir ayrıntı anlatılıyor.",
                "search_terms": ["city street at night", "sports car close up"],
            }
            for index in range(1, scene_count + 1)
        ],
    }


def _reply(text: str, chunks: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    candidate: dict[str, Any] = {
        "content": {"role": "model", "parts": [{"text": text}]},
        "finishReason": "STOP",
    }
    if chunks is not None:
        candidate["groundingMetadata"] = {
            "webSearchQueries": ["gta 5 gizli detay"],
            "groundingChunks": chunks,
        }
    return {"candidates": [candidate]}


def _web(uri: str, title: str = "") -> dict[str, Any]:
    return {"web": {"uri": uri, "title": title}}


def _generator(**overrides: Any) -> GeminiScriptGenerator:
    kwargs: dict[str, Any] = {"timeout": 5.0, "max_attempts": 3}
    kwargs.update(overrides)
    return GeminiScriptGenerator(KEY, **kwargs)


def _last_body(mock: rm.Mocker) -> dict[str, Any]:
    request = mock.last_request
    assert request is not None
    body: dict[str, Any] = request.json()
    return body


# --------------------------------------------------------------------------------------
# Request shape
# --------------------------------------------------------------------------------------


def test_the_key_travels_in_a_header_and_never_in_the_url(requests_mock: rm.Mocker) -> None:
    requests_mock.post(URL, json=_reply(json.dumps(_script()), chunks=[]))

    _generator().generate("GTA 5 gizli detaylar", scene_count=2)

    request = requests_mock.last_request
    assert request is not None
    assert request.headers["x-goog-api-key"] == KEY
    assert KEY not in request.url


def test_grounding_adds_google_search_and_the_fact_rules(requests_mock: rm.Mocker) -> None:
    requests_mock.post(URL, json=_reply(json.dumps(_script()), chunks=[]))

    _generator(grounding=True).generate("GTA 5 gizli detaylar", scene_count=2)

    body = _last_body(requests_mock)
    assert body["tools"] == [{"googleSearch": {}}]
    system = body["systemInstruction"]["parts"][0]["text"]
    assert "Google Search" in system
    assert "exactly 2 objects" in system
    assert "responseMimeType" not in body["generationConfig"]
    assert [content["role"] for content in body["contents"]] == ["user"]


def test_by_default_the_model_writes_only_what_it_is_sure_of(requests_mock: rm.Mocker) -> None:
    """Search is paid for new keys, so the free default forces JSON and asks for caution."""
    requests_mock.post(URL, json=_reply(json.dumps(_script())))

    _generator().generate("GTA 5 gizli detaylar", scene_count=2)

    body = _last_body(requests_mock)
    system = body["systemInstruction"]["parts"][0]["text"]
    assert "tools" not in body
    assert body["generationConfig"]["responseMimeType"] == "application/json"
    assert "Google Search" not in system
    assert "only facts you are certain of" in system


# --------------------------------------------------------------------------------------
# Drafts and sources
# --------------------------------------------------------------------------------------


def test_a_grounded_reply_becomes_a_draft_with_its_sources(requests_mock: rm.Mocker) -> None:
    """Sources are deduplicated, untitled ones get their domain, and non-web links are dropped."""
    chunks = [
        _web("https://www.gtabase.com/gta-5/guides/garage", "GTABase"),
        _web("https://www.gtabase.com/gta-5/guides/garage", "GTABase"),
        _web("https://gta.fandom.com/wiki/Garage"),
        _web("javascript:alert(1)", "bad"),
        {"retrievedContext": {"uri": "gs://bucket/file"}},
    ]
    requests_mock.post(URL, json=_reply(f"```json\n{json.dumps(_script())}\n```", chunks))

    draft = _generator(grounding=True).generate("GTA 5 gizli detaylar", scene_count=2)

    assert len(draft.scenes) == 2
    assert draft.tags == ("gta 5", "gizli detay", "ai")
    assert [(source.title, source.url) for source in draft.sources] == [
        ("GTABase", "https://www.gtabase.com/gta-5/guides/garage"),
        ("gta.fandom.com", "https://gta.fandom.com/wiki/Garage"),
    ]


def test_sources_reach_the_scenario_file_but_not_the_narration(requests_mock: rm.Mocker) -> None:
    chunks = [_web("https://www.gtabase.com/gta-5/guides/garage", "GTABase")]
    requests_mock.post(URL, json=_reply(json.dumps(_script()), chunks))
    draft = _generator(grounding=True).generate("GTA 5 gizli detaylar", scene_count=2)

    scenario = build_scenario(draft, topic="GTA 5 gizli detaylar")

    assert [source.url for source in scenario.sources] == [
        "https://www.gtabase.com/gta-5/guides/garage"
    ]
    assert all("gtabase" not in scene.narration.lower() for scene in scenario.scenes)
    assert "gtabase" not in scenario.youtube.description.lower()


def test_a_scenario_source_must_be_a_web_address() -> None:
    payload = {
        "project_id": "source-check",
        "youtube": {"title": "Kaynak denemesi"},
        "scenes": [{"id": 1, "narration": "Bir cümle.", "search_terms": ["city"]}],
        "sources": [{"title": "yerel dosya", "url": "file:///etc/passwd"}],
    }
    with pytest.raises(ValueError, match="http"):
        Scenario.model_validate(payload)


def test_a_rejected_reply_is_sent_back_as_the_model_turn(requests_mock: rm.Mocker) -> None:
    """The shared repair loop quotes the bad reply; Gemini calls that turn ``model``."""
    requests_mock.post(
        URL,
        [{"json": _reply("Bunu yazamadım.")}, {"json": _reply(json.dumps(_script()), [])}],
    )

    draft = _generator().generate("GTA 5 gizli detaylar", scene_count=2)

    assert len(draft.scenes) == 2
    retry_body = requests_mock.request_history[1].json()
    assert [content["role"] for content in retry_body["contents"]] == ["user", "model", "user"]
    assert retry_body["contents"][1]["parts"][0]["text"] == "Bunu yazamadım."


# --------------------------------------------------------------------------------------
# Errors
# --------------------------------------------------------------------------------------


def _error(status: int, message: str) -> dict[str, Any]:
    return {"status_code": status, "json": {"error": {"code": status, "message": message}}}


def test_a_bad_key_gets_a_key_hint_and_never_echoes_the_key(requests_mock: rm.Mocker) -> None:
    requests_mock.post(URL, **_error(400, "API key not valid. Please pass a valid API key."))

    with pytest.raises(ScriptGenerationError, match="rejected the API key") as caught:
        _generator().generate("GTA 5", scene_count=2)

    assert "GEMINI_API_KEY" in (caught.value.hint or "")
    assert KEY not in str(caught.value)


def test_an_unknown_model_names_the_model(requests_mock: rm.Mocker) -> None:
    url = f"{GEMINI_API_BASE}/models/gemini-0-yok:generateContent"
    requests_mock.post(url, **_error(404, "models/gemini-0-yok is not found"))

    with pytest.raises(ScriptGenerationError, match="gemini-0-yok"):
        _generator(model="gemini-0-yok").generate("GTA 5", scene_count=2)


def test_a_retired_model_passes_on_googles_suggestion(requests_mock: rm.Mocker) -> None:
    """Google uses 404 for retired models too, and only its message names the replacement."""
    url = f"{GEMINI_API_BASE}/models/gemini-2.5-flash-lite:generateContent"
    message = (
        "This model models/gemini-2.5-flash-lite is no longer available to new users. "
        "Please update your code to use models/gemini-3.5-flash-lite."
    )
    requests_mock.post(url, **_error(404, message))

    with pytest.raises(ScriptGenerationError, match="no longer available") as caught:
        _generator(model="gemini-2.5-flash-lite").generate("GTA 5", scene_count=2)

    assert "gemini-3.5-flash-lite" in str(caught.value)


@pytest.mark.parametrize(
    ("grounding", "expected_hint"),
    [(False, "Wait a minute"), (True, "GEMINI_GROUNDING=false")],
)
def test_a_used_up_quota_is_retried_then_explained(
    requests_mock: rm.Mocker,
    monkeypatch: pytest.MonkeyPatch,
    grounding: bool,
    expected_hint: str,
) -> None:
    """429 is worth a retry; after that, a grounded run learns that search is paid."""
    monkeypatch.setattr("time.sleep", lambda _seconds: None)
    requests_mock.post(URL, **_error(429, "Resource has been exhausted"))

    with pytest.raises(ScriptGenerationError, match="quota") as caught:
        _generator(grounding=grounding).generate("GTA 5", scene_count=2)

    assert requests_mock.call_count == 2
    assert expected_hint in (caught.value.hint or "")


def test_an_overloaded_model_says_so_after_retrying(
    requests_mock: rm.Mocker, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("time.sleep", lambda _seconds: None)
    requests_mock.post(URL, **_error(503, "This model is currently experiencing high demand."))

    with pytest.raises(ScriptGenerationError, match="overloaded") as caught:
        _generator().generate("GTA 5", scene_count=2)

    assert requests_mock.call_count == 2
    assert "GEMINI_MODEL" in (caught.value.hint or "")


# --------------------------------------------------------------------------------------
# Fallback models
# --------------------------------------------------------------------------------------

FIRST = f"{GEMINI_API_BASE}/models/model-a:generateContent"
SECOND = f"{GEMINI_API_BASE}/models/model-b:generateContent"


def _models_called(mock: rm.Mocker) -> list[str]:
    return [request.path.rsplit("/", 1)[-1].split(":")[0] for request in mock.request_history]


def test_a_busy_model_hands_over_and_the_answering_one_goes_first(
    requests_mock: rm.Mocker, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("time.sleep", lambda _seconds: None)
    requests_mock.post(FIRST, **_error(503, "This model is currently experiencing high demand."))
    requests_mock.post(SECOND, json=_reply(json.dumps(_script())))
    generator = _generator(model="model-a", fallback_models=["model-b"])

    first = generator.generate("GTA 5", scene_count=2)
    second = generator.generate("GTA 5", scene_count=2)

    assert len(first.scenes) == len(second.scenes) == 2
    assert _models_called(requests_mock) == ["model-a", "model-a", "model-b", "model-b"]


def test_a_retired_model_hands_over_without_retrying(requests_mock: rm.Mocker) -> None:
    requests_mock.post(FIRST, **_error(404, "This model is no longer available to new users."))
    requests_mock.post(SECOND, json=_reply(json.dumps(_script())))

    _generator(model="model-a", fallback_models=["model-b"]).generate("GTA 5", scene_count=2)

    assert _models_called(requests_mock) == ["model-a", "model-b"]


def test_a_rejected_key_does_not_try_the_other_models(requests_mock: rm.Mocker) -> None:
    """Every model would refuse the same key, so the next one is not worth a request."""
    requests_mock.post(FIRST, **_error(400, "API key not valid. Please pass a valid API key."))
    requests_mock.post(SECOND, json=_reply(json.dumps(_script())))

    with pytest.raises(ScriptGenerationError, match="API key"):
        _generator(model="model-a", fallback_models=["model-b"]).generate("GTA 5", scene_count=2)

    assert _models_called(requests_mock) == ["model-a"]


def test_when_every_model_fails_the_last_failure_is_reported(
    requests_mock: rm.Mocker, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("time.sleep", lambda _seconds: None)
    requests_mock.post(FIRST, **_error(503, "busy"))
    requests_mock.post(SECOND, **_error(429, "Resource has been exhausted"))

    with pytest.raises(ScriptGenerationError, match="quota"):
        _generator(model="model-a", fallback_models=["model-b"]).generate("GTA 5", scene_count=2)


def test_the_model_setting_is_a_clean_fallback_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_MODEL", " model-a , model-b,,model-a ")
    get_settings.cache_clear()
    assert get_settings().GEMINI_MODEL == "model-a,model-b"

    monkeypatch.setenv("GEMINI_MODEL", " , ")
    get_settings.cache_clear()
    with pytest.raises(ConfigurationError, match="at least one model"):
        get_settings()


def test_a_blocked_prompt_says_why(requests_mock: rm.Mocker) -> None:
    requests_mock.post(URL, json={"promptFeedback": {"blockReason": "SAFETY"}})

    with pytest.raises(ScriptGenerationError, match="SAFETY"):
        _generator().generate("GTA 5", scene_count=2)


def test_an_empty_answer_reports_the_finish_reason(requests_mock: rm.Mocker) -> None:
    empty = {"candidates": [{"content": {"parts": []}, "finishReason": "RECITATION"}]}
    requests_mock.post(URL, json=empty)

    with pytest.raises(ScriptGenerationError, match="RECITATION"):
        _generator().generate("GTA 5", scene_count=2)


@pytest.mark.parametrize(("key", "model"), [("", GEMINI_DEFAULT_MODEL), (KEY, "  ")])
def test_an_empty_key_or_model_is_refused_up_front(key: str, model: str) -> None:
    with pytest.raises(ScriptGenerationError, match="empty"):
        GeminiScriptGenerator(key, model)


def test_available_models_follow_pages_and_keep_text_models(requests_mock: rm.Mocker) -> None:
    first = {
        "models": [
            {
                "name": "models/gemini-2.5-flash-lite",
                "supportedGenerationMethods": ["generateContent"],
            },
            {"name": "models/text-embedding-004", "supportedGenerationMethods": ["embedContent"]},
        ],
        "nextPageToken": "page-2",
    }
    second = {
        "models": [
            {"name": "models/gemini-3.8-flash", "supportedGenerationMethods": ["generateContent"]}
        ]
    }
    requests_mock.get(f"{GEMINI_API_BASE}/models", [{"json": first}, {"json": second}])

    assert _generator().available_models() == ["gemini-2.5-flash-lite", "gemini-3.8-flash"]
    assert requests_mock.request_history[1].qs["pagetoken"] == ["page-2"]


# --------------------------------------------------------------------------------------
# Wiring and settings
# --------------------------------------------------------------------------------------


def test_the_default_provider_is_gemini_and_needs_a_key(settings: Settings) -> None:
    from main import _build_script_generator

    with pytest.raises(ConfigurationError, match="GEMINI_API_KEY"):
        _build_script_generator(settings)


def test_the_provider_setting_picks_the_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    from main import _build_script_generator

    monkeypatch.setenv("GEMINI_API_KEY", KEY)
    get_settings.cache_clear()
    assert isinstance(_build_script_generator(get_settings()), GeminiScriptGenerator)

    monkeypatch.setenv("SCRIPT_PROVIDER", "ollama")
    get_settings.cache_clear()
    assert isinstance(_build_script_generator(get_settings()), OllamaScriptGenerator)


def test_an_unknown_provider_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SCRIPT_PROVIDER", "chatgpt")
    get_settings.cache_clear()
    with pytest.raises(ConfigurationError, match="SCRIPT_PROVIDER"):
        get_settings()


def test_tests_never_see_the_developers_real_keys(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Settings read a .env file too; the isolated environment must still blank every key."""
    (tmp_path / ".env").write_text(
        "PEXELS_API_KEY=real-pexels\nPIXABAY_API_KEY=real-pixabay\nGEMINI_API_KEY=real-gemini\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    get_settings.cache_clear()

    loaded = get_settings()

    assert loaded.PEXELS_API_KEY == ""
    assert loaded.PIXABAY_API_KEY == ""
    assert loaded.GEMINI_API_KEY == ""


def test_the_gemini_key_is_redacted_from_logs(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", KEY)
    get_settings.cache_clear()
    assert KEY in get_settings().secret_values()


def test_doctor_checks_the_gemini_key_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    get_settings.cache_clear()
    missing = preflight._check_script_provider(get_settings())
    assert not missing.passed
    assert not missing.fatal

    monkeypatch.setenv("GEMINI_API_KEY", KEY)
    get_settings.cache_clear()
    present = preflight._check_script_provider(get_settings())
    assert present.passed
    assert GEMINI_DEFAULT_MODEL in present.detail
    assert "without search" in present.detail
