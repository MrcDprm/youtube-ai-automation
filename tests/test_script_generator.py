"""Local script generation: JSON recovery, output sanitising, repair loop and assembly.

Every test is offline. The Ollama HTTP endpoint is stubbed with ``requests_mock``, so no model
needs to be installed and nothing is ever generated for real.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
import requests
import requests_mock as rm

from config.constants import (
    SCRIPT_MAX_SEARCH_TERMS,
    SCRIPT_NARRATION_MAX_CHARS,
    YOUTUBE_TITLE_MAX_CHARS,
)
from models.scenario import Scenario
from modules.interfaces import DraftScene, DraftScript
from modules.scenario_builder import (
    build_scenario,
    estimate_total_seconds,
    make_project_id,
    slugify,
    write_scenario,
)
from modules.scenario_loader import load_scenario
from modules.script_generator import OllamaScriptGenerator, extract_json_object
from utils.exceptions import ScriptGenerationError

HOST = "http://localhost:11434"
MODEL = "qwen2.5:7b-instruct"
CHAT_URL = f"{HOST}/api/chat"
TAGS_URL = f"{HOST}/api/tags"

PROJECT_SLUG_PATTERN = re.compile(r"^[a-z0-9_-]{3,64}$")


def _generator(**overrides: Any) -> OllamaScriptGenerator:
    """Build a generator pointed at the stubbed endpoint."""
    kwargs: dict[str, Any] = {"timeout": 5.0, "max_attempts": 3}
    kwargs.update(overrides)
    return OllamaScriptGenerator(HOST, MODEL, **kwargs)


def _last_body(mock: rm.Mocker) -> dict[str, Any]:
    """Return the most recent request body, asserting one was actually sent."""
    request = mock.last_request
    assert request is not None
    body: dict[str, Any] = request.json()
    return body


def _reply(payload: Any) -> dict[str, Any]:
    """Wrap a payload in Ollama's chat response envelope."""
    content = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    return {"model": MODEL, "message": {"role": "assistant", "content": content}, "done": True}


def _script(scene_count: int = 3, **overrides: Any) -> dict[str, Any]:
    """Build a well-formed model payload."""
    payload: dict[str, Any] = {
        "title": "Yapay Zekanin Kisa Tarihi",
        "description": "Yapay zekanin gelisimi. Kisa bir bakis.",
        "tags": ["yapay zeka", "teknoloji", "bilim", "tarih", "ai"],
        "scenes": [
            {
                "narration": f"Bu {index}. sahnenin anlatimi burada yer aliyor.",
                "search_terms": ["vintage computer", "old typewriter close up"],
            }
            for index in range(1, scene_count + 1)
        ],
    }
    payload.update(overrides)
    return payload


def _draft(scene_count: int = 3, narration: str = "Kisa bir anlatim cumlesi.") -> DraftScript:
    """Build a draft script directly, bypassing the model."""
    return DraftScript(
        title="Test Basligi",
        description="Test aciklamasi.",
        tags=("test", "deneme"),
        scenes=tuple(
            DraftScene(narration=narration, search_terms=("city skyline",))
            for _ in range(scene_count)
        ),
    )


# --------------------------------------------------------------------------------------
# JSON recovery
# --------------------------------------------------------------------------------------


def test_plain_json_object_is_decoded() -> None:
    """A bare object decodes unchanged."""
    assert extract_json_object('{"a": 1}') == {"a": 1}


def test_code_fences_are_stripped() -> None:
    """Models often wrap JSON in a markdown fence despite being told not to."""
    assert extract_json_object('```json\n{"a": 1}\n```') == {"a": 1}


def test_surrounding_prose_is_ignored() -> None:
    """Commentary before and after the object is discarded."""
    text = 'Sure! Here is the script:\n{"a": 1}\nLet me know if you want changes.'

    assert extract_json_object(text) == {"a": 1}


def test_nested_objects_are_matched_to_the_outer_brace() -> None:
    """Brace counting must not stop at the first inner closing brace."""
    payload = {"scenes": [{"narration": "x", "meta": {"depth": 2}}]}

    assert extract_json_object(json.dumps(payload)) == payload


def test_braces_inside_strings_do_not_end_the_object() -> None:
    """A brace or quote inside narration must not confuse the scanner."""
    payload = {"narration": 'He said "{not json}" loudly'}

    assert extract_json_object(json.dumps(payload)) == payload


def test_escaped_quote_inside_string_is_handled() -> None:
    """Backslash escapes are tracked so string state stays correct."""
    payload = {"narration": 'a \\" b'}

    assert extract_json_object(json.dumps(payload)) == payload


def test_missing_object_raises() -> None:
    """Text with no object at all is rejected."""
    with pytest.raises(ValueError, match="no JSON object"):
        extract_json_object("I cannot help with that.")


def test_truncated_object_raises() -> None:
    """An object cut off by a token limit is reported as truncated."""
    with pytest.raises(ValueError, match="truncated"):
        extract_json_object('{"scenes": [{"narration": "abc"')


def test_malformed_object_reports_a_decode_failure() -> None:
    """Balanced braces are not enough; the contents still have to be valid JSON."""
    with pytest.raises(ValueError, match="did not decode"):
        extract_json_object('{"a": }')


# --------------------------------------------------------------------------------------
# Construction
# --------------------------------------------------------------------------------------


def test_empty_host_is_rejected() -> None:
    """A blank host is a configuration error, caught before any request."""
    with pytest.raises(ScriptGenerationError, match="OLLAMA_HOST"):
        OllamaScriptGenerator("   ", MODEL)


def test_empty_model_is_rejected() -> None:
    """A blank model name is a configuration error."""
    with pytest.raises(ScriptGenerationError, match="OLLAMA_MODEL"):
        OllamaScriptGenerator(HOST, "  ")


def test_empty_topic_is_rejected(requests_mock: rm.Mocker) -> None:
    """A blank topic fails before the model is contacted."""
    with pytest.raises(ScriptGenerationError, match="topic is empty"):
        _generator().generate("   ", scene_count=3)

    assert requests_mock.call_count == 0


# --------------------------------------------------------------------------------------
# Happy path and request shape
# --------------------------------------------------------------------------------------


def test_valid_reply_becomes_a_draft(requests_mock: rm.Mocker) -> None:
    """A well-formed reply is converted into a draft script."""
    requests_mock.post(CHAT_URL, json=_reply(_script(3)))

    draft = _generator().generate("yapay zeka", scene_count=3)

    assert draft.title == "Yapay Zekanin Kisa Tarihi"
    assert len(draft.scenes) == 3
    assert draft.scenes[0].search_terms == ("vintage computer", "old typewriter close up")
    assert "yapay zeka" in draft.tags


def test_request_asks_for_json_and_disables_streaming(requests_mock: rm.Mocker) -> None:
    """The pipeline parses a single response body, so streaming must be off."""
    requests_mock.post(CHAT_URL, json=_reply(_script(2)))

    _generator().generate("konu", scene_count=2)

    body = _last_body(requests_mock)
    assert body["model"] == MODEL
    assert body["stream"] is False
    assert body["format"] == "json"
    assert body["messages"][0]["role"] == "system"
    assert "exactly 2 objects" in body["messages"][0]["content"]
    assert "konu" in body["messages"][1]["content"]


def test_extra_guidance_reaches_the_prompt(requests_mock: rm.Mocker) -> None:
    """Caller-supplied direction is appended to the user message."""
    requests_mock.post(CHAT_URL, json=_reply(_script(1)))

    _generator().generate("konu", scene_count=1, extra_guidance="kisa ve carpici olsun")

    assert "kisa ve carpici olsun" in _last_body(requests_mock)["messages"][1]["content"]


def test_language_name_is_spelled_out_for_the_model(requests_mock: rm.Mocker) -> None:
    """Language codes are mapped to names the model actually recognises."""
    requests_mock.post(CHAT_URL, json=_reply(_script(1)))

    _generator().generate("topic", scene_count=1, language="tr")

    assert "Turkish" in _last_body(requests_mock)["messages"][0]["content"]


# --------------------------------------------------------------------------------------
# Output sanitising
# --------------------------------------------------------------------------------------


def test_markdown_and_emoji_are_stripped_from_narration(requests_mock: rm.Mocker) -> None:
    """Narration is spoken aloud, so formatting characters must not survive."""
    payload = _script(1)
    payload["scenes"][0]["narration"] = "**Merhaba** _dunya_ 🚀 `kod` #baslik"
    requests_mock.post(CHAT_URL, json=_reply(payload))

    draft = _generator().generate("konu", scene_count=1)

    assert draft.scenes[0].narration == "Merhaba dunya kod baslik"


def test_speaker_and_list_prefixes_are_removed(requests_mock: rm.Mocker) -> None:
    """Models like to prefix lines with 'Sahne 1:' or a bullet."""
    payload = _script(1)
    payload["scenes"][0]["narration"] = "Sahne 1: Anlatim burada."
    requests_mock.post(CHAT_URL, json=_reply(payload))

    draft = _generator().generate("konu", scene_count=1)

    assert draft.scenes[0].narration == "Anlatim burada."


def test_long_narration_is_cut_at_a_sentence_boundary(requests_mock: rm.Mocker) -> None:
    """Truncation must not leave a half-finished sentence mid-word."""
    first = "Bu ilk cumle. "
    payload = _script(1)
    payload["scenes"][0]["narration"] = first + ("uzun kelime " * 60)
    requests_mock.post(CHAT_URL, json=_reply(payload))

    narration = _generator().generate("konu", scene_count=1).scenes[0].narration

    assert len(narration) <= SCRIPT_NARRATION_MAX_CHARS
    assert not narration.endswith("kelim")


def test_search_terms_are_deduplicated_and_capped(requests_mock: rm.Mocker) -> None:
    """Repeated or excessive terms would waste provider requests."""
    payload = _script(1)
    payload["scenes"][0]["search_terms"] = [
        "city skyline",
        "CITY SKYLINE",
        "night street",
        "rainy window",
        "busy market",
        "ab",
    ]
    requests_mock.post(CHAT_URL, json=_reply(payload))

    terms = _generator().generate("konu", scene_count=1).scenes[0].search_terms

    assert len(terms) == SCRIPT_MAX_SEARCH_TERMS
    assert terms[0] == "city skyline"
    assert "ab" not in terms


def test_search_terms_given_as_a_string_are_accepted(requests_mock: rm.Mocker) -> None:
    """A single string instead of an array is coerced rather than rejected."""
    payload = _script(1)
    payload["scenes"][0]["search_terms"] = "lone mountain peak"
    requests_mock.post(CHAT_URL, json=_reply(payload))

    assert _generator().generate("konu", scene_count=1).scenes[0].search_terms == (
        "lone mountain peak",
    )


def test_tags_are_lowercased_and_deduplicated(requests_mock: rm.Mocker) -> None:
    """Tag casing is irrelevant to YouTube, so duplicates are collapsed."""
    requests_mock.post(CHAT_URL, json=_reply(_script(1, tags=["AI", "ai", "Bilim", "bilim"])))

    assert _generator().generate("konu", scene_count=1).tags == ("ai", "bilim")


def test_tag_budget_is_respected(requests_mock: rm.Mocker) -> None:
    """The combined tag length must stay inside YouTube's limit."""
    bloated = [f"etiket{n}" * 8 for n in range(40)]
    requests_mock.post(CHAT_URL, json=_reply(_script(1, tags=bloated)))

    tags = _generator().generate("konu", scene_count=1).tags

    assert sum(len(tag) + 1 for tag in tags) <= 450


def test_overlong_title_is_truncated(requests_mock: rm.Mocker) -> None:
    """A title over the API limit is trimmed instead of failing validation later."""
    requests_mock.post(CHAT_URL, json=_reply(_script(1, title="A" * 300)))

    assert len(_generator().generate("konu", scene_count=1).title) == YOUTUBE_TITLE_MAX_CHARS


def test_extra_scenes_are_trimmed_to_the_request(requests_mock: rm.Mocker) -> None:
    """A model that overshoots is trimmed rather than retried."""
    requests_mock.post(CHAT_URL, json=_reply(_script(9)))

    assert len(_generator().generate("konu", scene_count=4).scenes) == 4


# --------------------------------------------------------------------------------------
# Repair loop
# --------------------------------------------------------------------------------------


def test_bad_reply_is_retried_with_the_error_fed_back(requests_mock: rm.Mocker) -> None:
    """The second attempt is told exactly why the first was rejected."""
    requests_mock.post(
        CHAT_URL,
        [
            {"json": _reply("I am afraid I cannot do that.")},
            {"json": _reply(_script(2))},
        ],
    )

    draft = _generator().generate("konu", scene_count=2)

    assert len(draft.scenes) == 2
    assert requests_mock.call_count == 2
    repair_prompt = requests_mock.request_history[-1].json()["messages"][-1]["content"]
    assert "rejected because" in repair_prompt


def test_scene_with_empty_narration_triggers_a_retry(requests_mock: rm.Mocker) -> None:
    """An empty narration line is unusable and must be regenerated."""
    broken = _script(2)
    broken["scenes"][1]["narration"] = "   "
    requests_mock.post(CHAT_URL, [{"json": _reply(broken)}, {"json": _reply(_script(2))}])

    assert len(_generator().generate("konu", scene_count=2).scenes) == 2
    assert requests_mock.call_count == 2


def test_too_few_scenes_triggers_a_retry(requests_mock: rm.Mocker) -> None:
    """A short script is retried while attempts remain."""
    requests_mock.post(CHAT_URL, [{"json": _reply(_script(1))}, {"json": _reply(_script(5))}])

    assert len(_generator().generate("konu", scene_count=5).scenes) == 5
    assert requests_mock.call_count == 2


def test_short_script_is_accepted_on_the_final_attempt(requests_mock: rm.Mocker) -> None:
    """Rather than fail outright, the last attempt keeps what the model managed."""
    requests_mock.post(CHAT_URL, json=_reply(_script(2)))

    draft = _generator(max_attempts=2).generate("konu", scene_count=6)

    assert len(draft.scenes) == 2
    assert requests_mock.call_count == 2


def test_exhausted_attempts_raise_with_the_last_reason(requests_mock: rm.Mocker) -> None:
    """After the final attempt the failure names what was wrong."""
    requests_mock.post(CHAT_URL, json=_reply("no json here"))

    with pytest.raises(ScriptGenerationError, match="did not return a usable script"):
        _generator(max_attempts=2).generate("konu", scene_count=2)

    assert requests_mock.call_count == 2


# --------------------------------------------------------------------------------------
# Transport failures
# --------------------------------------------------------------------------------------


def test_missing_model_points_at_ollama_pull(requests_mock: rm.Mocker) -> None:
    """A 404 means the tag was never pulled, which has a one-line fix."""
    requests_mock.post(CHAT_URL, status_code=404, json={"error": "model not found"})

    with pytest.raises(ScriptGenerationError) as excinfo:
        _generator().generate("konu", scene_count=2)

    assert "ollama pull" in (excinfo.value.hint or "")


def test_unreachable_server_is_reported_clearly(requests_mock: rm.Mocker) -> None:
    """A refused connection usually means the service is not running."""
    requests_mock.post(CHAT_URL, exc=requests.ConnectionError("refused"))

    with pytest.raises(ScriptGenerationError, match="Could not reach Ollama"):
        _generator().generate("konu", scene_count=2)


def test_empty_message_content_is_rejected(requests_mock: rm.Mocker) -> None:
    """An empty completion usually means the model ran out of memory."""
    requests_mock.post(CHAT_URL, json={"message": {"role": "assistant", "content": ""}})

    with pytest.raises(ScriptGenerationError, match="empty message"):
        _generator().generate("konu", scene_count=2)


def test_malformed_envelope_is_rejected(requests_mock: rm.Mocker) -> None:
    """A response without a message object is a protocol error, not a bad script."""
    requests_mock.post(CHAT_URL, json=["not", "an", "object"])

    with pytest.raises(ScriptGenerationError, match="non-object response envelope"):
        _generator().generate("konu", scene_count=2)


def test_available_models_lists_installed_tags(requests_mock: rm.Mocker) -> None:
    """The tag endpoint is parsed into plain model names."""
    requests_mock.get(TAGS_URL, json={"models": [{"name": "a:latest"}, {"name": "b:7b"}, {}]})

    assert _generator().available_models() == ["a:latest", "b:7b"]


def test_available_models_reports_an_unreachable_server(requests_mock: rm.Mocker) -> None:
    """Listing models is the cheapest reachability probe, so its error must be clear."""
    requests_mock.get(TAGS_URL, exc=requests.ConnectionError("refused"))

    with pytest.raises(ScriptGenerationError, match="Could not reach Ollama"):
        _generator().available_models()


# --------------------------------------------------------------------------------------
# Slugs and project ids
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Yapay Zekanın Tarihi", "yapay-zekanin-tarihi"),
        ("İstanbul'un Şehirleri", "istanbul-un-sehirleri"),
        ("Çöp Güneş Ötesi", "cop-gunes-otesi"),
        ("  multiple   spaces  ", "multiple-spaces"),
        ("Hello, World! 2026", "hello-world-2026"),
    ],
)
def test_slugify_transliterates_turkish(text: str, expected: str) -> None:
    """Turkish letters have no decomposition, so they are mapped before ASCII folding."""
    assert slugify(text) == expected


def test_slugify_falls_back_when_nothing_survives() -> None:
    """Text with no alphanumerics still yields a usable slug."""
    assert slugify("!!! ???", fallback="video") == "video"


def test_project_id_matches_the_schema_pattern() -> None:
    """The generated id must satisfy the scenario schema's own regex."""
    project_id = make_project_id("Yapay Zekanın Kısa Tarihi", now=datetime(2026, 8, 20, tzinfo=UTC))

    assert project_id == "yapay-zekanin-kisa-tarihi-20260820"
    assert PROJECT_SLUG_PATTERN.match(project_id)


def test_project_id_stays_within_the_length_limit() -> None:
    """A very long topic is truncated rather than producing an invalid id."""
    project_id = make_project_id("kelime " * 40)

    assert PROJECT_SLUG_PATTERN.match(project_id)
    assert len(project_id) <= 64


def test_project_id_survives_an_unusable_topic() -> None:
    """A topic with no usable characters still yields a valid id."""
    assert PROJECT_SLUG_PATTERN.match(make_project_id("!!!"))


# --------------------------------------------------------------------------------------
# Scenario assembly
# --------------------------------------------------------------------------------------


def test_build_scenario_produces_a_valid_scenario() -> None:
    """Assembly output is validated by the real schema, not a lookalike."""
    scenario = build_scenario(_draft(3), topic="yapay zeka")

    assert isinstance(scenario, Scenario)
    assert scenario.total_scenes == 3
    assert [scene.id for scene in scenario.scenes] == [1, 2, 3]


def test_generated_scenario_never_enables_upload_by_default() -> None:
    """Nothing should publish before a human has read the narration."""
    scenario = build_scenario(_draft(), topic="konu")

    assert scenario.youtube.upload_enabled is False
    assert scenario.youtube.privacy_status == "private"


def test_synthetic_disclosure_is_on_by_default() -> None:
    """The narration is synthetic, so the disclosure stays enabled."""
    assert build_scenario(_draft(), topic="konu").youtube.synthetic_content_disclosure is True


def test_resolution_follows_the_requested_orientation() -> None:
    """Resolution is derived, so it can never contradict the orientation."""
    portrait = build_scenario(_draft(), topic="konu", orientation="portrait")
    landscape = build_scenario(_draft(), topic="konu", orientation="landscape")

    assert (portrait.video.width, portrait.video.height) == (1080, 1920)
    assert (landscape.video.width, landscape.video.height) == (1920, 1080)


def test_duration_ceiling_exceeds_the_estimate() -> None:
    """A generated scenario must not cap itself below its own narration length."""
    draft = _draft(8, narration="Bu cumle biraz daha uzun olsun ki sure tahmini artsin. " * 3)
    scenario = build_scenario(draft, topic="konu")

    assert scenario.video.max_duration_seconds > estimate_total_seconds(draft, 0.3)


def test_clip_count_grows_with_narration_length() -> None:
    """A long narration over one static clip looks lifeless, so it gets more cuts."""
    short = build_scenario(_draft(1, narration="Kisa cumle."), topic="konu")
    long = build_scenario(_draft(1, narration="x" * 300), topic="konu")

    assert short.scenes[0].clips_per_scene == 1
    assert long.scenes[0].clips_per_scene == 3


def test_voice_override_is_applied() -> None:
    """An explicit voice replaces the schema default."""
    scenario = build_scenario(_draft(), topic="konu", voice="tr-TR-EmelNeural")

    assert scenario.tts.voice == "tr-TR-EmelNeural"


def test_omitted_voice_uses_the_schema_default() -> None:
    """Leaving the voice unset keeps a single source of truth for the default."""
    assert build_scenario(_draft(), topic="konu").tts.voice == "tr-TR-AhmetNeural"


def test_burn_in_can_be_disabled() -> None:
    """Turning off burn-in still leaves subtitles enabled for the sidecar."""
    scenario = build_scenario(_draft(), topic="konu", burn_in=False)

    assert scenario.subtitles.enabled is True
    assert scenario.subtitles.burn_in is False


def test_empty_draft_is_rejected() -> None:
    """A draft with no scenes cannot become a video."""
    empty = DraftScript(title="t", description="d", tags=(), scenes=())

    with pytest.raises(ScriptGenerationError, match="no scenes"):
        build_scenario(empty, topic="konu")


# --------------------------------------------------------------------------------------
# Round trip: what generate writes, run must be able to load
# --------------------------------------------------------------------------------------


def test_written_scenario_loads_through_the_real_loader(tmp_path: Path) -> None:
    """The end-to-end contract: a generated file is accepted by ``run`` unmodified."""
    scenario = build_scenario(_draft(4), topic="Yapay Zekanın Tarihi")
    destination = tmp_path / "generated.json"

    write_scenario(scenario, destination)
    reloaded = load_scenario(destination)

    assert reloaded.project_id == scenario.project_id
    assert reloaded.total_scenes == 4
    assert reloaded.youtube.title == scenario.youtube.title


def test_written_paths_use_forward_slashes(tmp_path: Path) -> None:
    """A generated scenario must stay readable on a platform other than the one that wrote it."""
    destination = tmp_path / "paths.json"

    write_scenario(build_scenario(_draft(), topic="konu"), destination)
    payload = json.loads(destination.read_text(encoding="utf-8"))

    assert "\\" not in payload["subtitles"]["font"]
    assert payload["subtitles"]["font"].endswith("Inter-Bold.ttf")


def test_written_scenario_is_utf8_without_a_bom(tmp_path: Path) -> None:
    """Turkish characters must survive the round trip as real UTF-8."""
    draft = DraftScript(
        title="Şafak Vakti Güneş",
        description="Çok kısa bir açıklama.",
        tags=("şafak",),
        scenes=(DraftScene(narration="Işık doğudan yükselir.", search_terms=("sunrise",)),),
    )
    destination = tmp_path / "turkish.json"

    write_scenario(build_scenario(draft, topic="şafak"), destination)
    raw = destination.read_bytes()

    assert not raw.startswith(b"\xef\xbb\xbf")
    assert "Işık doğudan yükselir." in raw.decode("utf-8")
