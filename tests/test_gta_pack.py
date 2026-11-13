"""The Turkish GTA 5 Shorts pack: checked facts in, a Short scenario over gameplay out.

The writer is driven by a scripted chat model, so every rule it enforces can be broken on
purpose and the rewrite request inspected. The command-line tests run ``generate`` and
``daily`` with that same model and a fake gameplay folder.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

import main
from config.constants import (
    GTA_BASE_TAGS,
    GTA_MAX_WORDS,
    GTA_MIN_WORDS,
    GTA_PLACEHOLDER_SEARCH_TERMS,
    PROJECT_ROOT,
)
from config.settings import get_settings
from models.scenario import Scenario
from modules.gta_writer import GtaShortsWriter, count_words
from modules.interfaces import DraftSource
from modules.queue import Topic, load_topics
from modules.scenario_builder import build_gta_scenario
from modules.script_generator import ChatScriptGenerator
from utils.exceptions import ConfigurationError, ScriptGenerationError
from utils.fs import write_json
from utils.text import upper_text

runner = CliRunner()

TOPIC = "Fort Zancudo'ya izinsiz girmek"
FACT = (
    "Fort Zancudo, GTA 5'teki askeri üs. Hikaye modunda üsse karadan izinsiz girer ve "
    "içerideki askerlere görünürsen hemen 4 yıldız aranma seviyesi alırsın. Uçakla üssün "
    "hava sahasına girersen önce telsizden uyarı gelir."
)
SOURCES = (
    DraftSource(title="Grand Theft Wiki", url="https://www.grandtheftwiki.com/Fort_Zancudo"),
    DraftSource(title="GTA Wiki", url="https://gta.wiki/w/Fort_Zancudo"),
)
GOOD_SCENES = [
    "Fort Zancudo'nun çitini geçtiğin an oyun seni affetmiyor.",
    "Burası GTA 5'teki askeri üs ve hikaye modunda içeri izinsiz giriyorsun.",
    "İçerideki askerlerden biri seni gördüğü anda hemen 4 yıldız aranma seviyesi alıyorsun.",
    "Gökyüzünden gelmeyi düşünüyorsan önce telsizden bir uyarı duyuyorsun, çünkü üssün hava "
    "sahası da korunuyor.",
    "Yani bu üsse sessizce girmek diye bir şey yok, bir asker seni gördüğü an iş bitiyor.",
]
TITLE = "GTA 5'te Fort Zancudo'ya izinsiz girersen ne olur"


def _reply(
    scenes: list[str] | None = None,
    *,
    title: str = TITLE,
    description: str = "Fort Zancudo askeri üssüne izinsiz girmenin hikaye modundaki karşılığı.",
    tags: Any = ("fort zancudo", "askeri üs", "gta 5"),
) -> str:
    return json.dumps(
        {
            "title": title,
            "description": description,
            "tags": list(tags) if isinstance(tags, tuple) else tags,
            "scenes": [{"narration": text} for text in (scenes or GOOD_SCENES)],
        },
        ensure_ascii=False,
    )


class ScriptedChat(ChatScriptGenerator):
    """Answers with prepared replies and records every conversation it receives."""

    def __init__(self, *replies: str) -> None:
        super().__init__("scripted")
        self.replies = list(replies)
        self.calls: list[tuple[list[dict[str, str]], int]] = []

    def available_models(self) -> list[str]:
        return ["scripted"]

    def _chat(self, messages: list[dict[str, str]], scene_count: int) -> str:
        self.calls.append((list(messages), scene_count))
        if not self.replies:
            raise AssertionError("the writer asked more often than the test expected")
        return self.replies.pop(0)


def _write(chat: ScriptedChat, **kwargs: Any) -> Any:
    return GtaShortsWriter(chat).generate(TOPIC, FACT, sources=SOURCES, **kwargs)


def _rewrite_request(chat: ScriptedChat, attempt: int = 2) -> str:
    """The message that asked for the given attempt, which explains the rejection."""
    return chat.calls[attempt - 1][0][-1]["content"]


# --------------------------------------------------------------------------------------
# The writer
# --------------------------------------------------------------------------------------


def test_the_sample_narration_fits_the_length_rule() -> None:
    assert GTA_MIN_WORDS <= count_words(" ".join(GOOD_SCENES)) <= GTA_MAX_WORDS


def test_a_reply_within_the_rules_becomes_the_draft() -> None:
    chat = ScriptedChat(_reply())

    draft = _write(chat)

    assert len(chat.calls) == 1
    assert [scene.narration for scene in draft.scenes] == GOOD_SCENES
    assert all(scene.search_terms == GTA_PLACEHOLDER_SEARCH_TERMS for scene in draft.scenes)
    assert draft.title == TITLE
    assert draft.tags[: len(GTA_BASE_TAGS)] == GTA_BASE_TAGS
    assert draft.tags.count("gta 5") == 1
    assert "fort zancudo" in draft.tags
    assert draft.sources == SOURCES


def test_the_brief_carries_the_fact_and_the_rules() -> None:
    chat = ScriptedChat(_reply())

    _write(chat, extra_guidance="Kancayı 4 yıldız üzerine kur.")

    messages, scene_count = chat.calls[0]
    system, brief = messages[0]["content"], messages[1]["content"]
    assert scene_count == 5
    assert "exactly 5 objects" in system
    assert f"{GTA_MIN_WORDS} to {GTA_MAX_WORDS} words" in system
    assert "inanılmaz" in system
    assert "Use only the fact in the brief" in system
    assert f"Topic: {TOPIC}" in brief
    assert f"Fact: {FACT}" in brief
    assert "Additional direction: Kancayı 4 yıldız üzerine kur." in brief


@pytest.mark.parametrize(("asked", "sent"), [(1, 3), (20, 8), (6, 6)])
def test_the_scene_count_stays_within_the_pack_limits(asked: int, sent: int) -> None:
    chat = ScriptedChat(_reply())

    _write(chat, scene_count=asked)

    assert chat.calls[0][1] == sent
    assert f"exactly {sent} objects" in chat.calls[0][0][0]["content"]


def test_a_short_narration_is_sent_back_with_its_word_count() -> None:
    short = ["Fort Zancudo çok sıkı korunuyor.", "Girersen 4 yıldız alırsın.", "Dikkat et."]
    chat = ScriptedChat(_reply(short), _reply())

    draft = _write(chat)

    assert len(chat.calls) == 2
    request = _rewrite_request(chat)
    assert f"the narration was {count_words(' '.join(short))} words" in request
    assert f"{GTA_MIN_WORDS} to {GTA_MAX_WORDS} words" in request
    assert [scene.narration for scene in draft.scenes] == GOOD_SCENES


def test_a_number_the_fact_does_not_give_is_sent_back() -> None:
    invented = [*GOOD_SCENES[:-1], "Bu kural oyun 2013'te çıktığından beri hiç değişmedi."]
    chat = ScriptedChat(_reply(invented), _reply())

    _write(chat)

    assert "numbers the fact does not give: 2013" in _rewrite_request(chat)


def test_numbers_from_the_fact_and_the_game_name_pass() -> None:
    """The fact gives 4, the game's name gives 5, and 04 is the same number as 4."""
    scenes = [*GOOD_SCENES[:-1], "Kısacası 04 yıldızla GTA 5'in en sert cezası burada."]
    chat = ScriptedChat(_reply(scenes))

    _write(chat)

    assert len(chat.calls) == 1


def test_the_game_name_may_be_said_even_when_the_fact_has_no_number() -> None:
    """GTA 5 is the game's name, not a claim, so its 5 never needs the fact's backing."""
    scenes = [scene.replace("hemen 4 yıldız", "hemen dört yıldız") for scene in GOOD_SCENES]
    fact = "Fort Zancudo, izinsiz girenlere hikaye modunda aranma seviyesi verir."
    chat = ScriptedChat(_reply(scenes))

    GtaShortsWriter(chat).generate(TOPIC, fact)

    assert len(chat.calls) == 1


@pytest.mark.parametrize(
    ("word", "reported"),
    [("İNANILMAZ", "inanılmaz"), ("efsanevi", "efsane"), ("Abone olmayı", "abone")],
)
def test_banned_words_are_caught_in_capitals_and_with_suffixes(word: str, reported: str) -> None:
    scenes = [*GOOD_SCENES[:-1], f"Bu {word} kural yüzünden iş hemen bitiyor, sessiz kal."]
    chat = ScriptedChat(_reply(scenes), _reply())

    _write(chat)

    assert f"the text used banned words: {reported}" in _rewrite_request(chat)


def test_banned_words_in_the_title_are_caught_too() -> None:
    chat = ScriptedChat(_reply(title="GTA 5'in efsane askeri üssü"), _reply())

    _write(chat)

    assert "banned words: efsane" in _rewrite_request(chat)


def test_a_title_that_does_not_name_the_game_is_sent_back() -> None:
    chat = ScriptedChat(_reply(title="Askeri üsse girersen ne olur"), _reply())

    _write(chat)

    assert '"title" must name GTA 5' in _rewrite_request(chat)


def test_too_few_scenes_are_sent_back() -> None:
    chat = ScriptedChat(_reply([" ".join(GOOD_SCENES)]), _reply())

    _write(chat)

    assert "only 1 scene(s) came back; write at least 3" in _rewrite_request(chat)


def test_marks_a_voice_would_not_say_are_removed_but_apostrophes_stay() -> None:
    scenes = [
        "Fort Zancudo'nun çitini geçtiğin an oyun seni affetmiyor!",
        'Burası "GTA 5\'teki" askeri üs (hikaye modunda) ve içeri izinsiz giriyorsun.',
        *GOOD_SCENES[2:],
    ]
    chat = ScriptedChat(_reply(scenes, title="GTA 5'te #Fort Zancudo!"))

    draft = _write(chat)

    first, second = draft.scenes[0].narration, draft.scenes[1].narration
    assert first == "Fort Zancudo'nun çitini geçtiğin an oyun seni affetmiyor."
    assert second == "Burası GTA 5'teki askeri üs hikaye modunda ve içeri izinsiz giriyorsun."
    assert draft.title == "GTA 5'te Fort Zancudo."


def test_a_narration_typed_without_turkish_letters_is_sent_back() -> None:
    """Gemini once answered in plain ASCII: yuzde yuz instead of yüzde yüz."""
    ascii_only = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    chat = ScriptedChat(_reply([scene.translate(ascii_only) for scene in GOOD_SCENES]), _reply())

    _write(chat)

    assert "typed without Turkish letters" in _rewrite_request(chat)


def test_every_scene_becomes_a_sentence_with_a_turkish_capital() -> None:
    scenes = [
        "fort Zancudo'nun çitini geçtiğin an oyun seni affetmiyor",
        GOOD_SCENES[1],
        "içerideki askerlerden biri seni gördüğü anda hemen 4 yıldız aranma seviyesi alıyorsun,",
        *GOOD_SCENES[3:],
    ]
    chat = ScriptedChat(_reply(scenes))

    draft = _write(chat)

    assert draft.scenes[0].narration == "Fort Zancudo'nun çitini geçtiğin an oyun seni affetmiyor."
    assert draft.scenes[2].narration == GOOD_SCENES[2]


def test_a_suffix_split_from_its_name_gets_its_apostrophe_back() -> None:
    """Gemini wrote UFO nun and GTA 5 te; de and da can be words, so they stay apart."""
    scenes = [
        "Fort Zancudo nun çitini geçtiğin an oyun seni affetmiyor, Franklin de bunu biliyor.",
        "Burası GTA 5 teki askeri üs ve hikaye modunda içeri izinsiz giriyorsun.",
        *GOOD_SCENES[2:],
    ]
    chat = ScriptedChat(_reply(scenes, description="GTA 5 te Fort Zancudo da ne olur."))

    draft = _write(chat)

    assert draft.scenes[0].narration == (
        "Fort Zancudo'nun çitini geçtiğin an oyun seni affetmiyor, Franklin de bunu biliyor."
    )
    assert draft.scenes[1].narration == GOOD_SCENES[1]
    assert draft.description == "GTA 5'te Fort Zancudo da ne olur."


def test_the_game_name_is_written_in_capitals() -> None:
    scenes = [GOOD_SCENES[0].replace("oyun", "gta v"), *GOOD_SCENES[1:]]
    chat = ScriptedChat(_reply(scenes, title="gta 5'te Fort Zancudo kuralı"))

    draft = _write(chat)

    assert draft.title == "GTA 5'te Fort Zancudo kuralı"
    assert "an GTA V seni affetmiyor" in draft.scenes[0].narration


def test_the_writer_gives_up_with_the_last_reason() -> None:
    bad = _reply(title="Başlıksız bir video")
    chat = ScriptedChat(bad, bad, bad)

    with pytest.raises(ScriptGenerationError, match="must name GTA 5"):
        _write(chat)

    assert len(chat.calls) == 3


@pytest.mark.parametrize(("topic", "fact"), [("", FACT), (TOPIC, ""), (TOPIC, "   ")])
def test_a_blank_topic_or_fact_is_refused_before_any_request(topic: str, fact: str) -> None:
    chat = ScriptedChat()

    with pytest.raises(ScriptGenerationError):
        GtaShortsWriter(chat).generate(topic, fact)

    assert chat.calls == []


# --------------------------------------------------------------------------------------
# The scenario
# --------------------------------------------------------------------------------------


def _draft() -> Any:
    return _write(ScriptedChat(_reply()))


def test_the_scenario_is_a_portrait_short_over_muted_gameplay(tmp_path: Path) -> None:
    folder = tmp_path / "gta5"
    folder.mkdir()

    scenario = build_gta_scenario(_draft(), topic=TOPIC, background_folder=folder)

    video = scenario.video
    assert video.format == "shorts"
    assert (video.width, video.height) == (1080, 1920)
    assert video.background_video.enabled
    assert video.background_video.resolved_folder == folder
    assert video.background_video.game_audio_volume == 0.0
    assert video.crossfade_seconds == 0.0
    assert video.scene_gap_seconds == pytest.approx(0.1)
    assert video.max_duration_seconds >= 60
    assert all(not scene.zoom_effect for scene in scenario.scenes)
    assert scenario.tts.voice == "tr-TR-AhmetNeural"
    assert scenario.tts.rate == "+10%"
    assert scenario.tts.trim_trailing_silence is True


def test_the_captions_highlight_each_word_in_capitals(tmp_path: Path) -> None:
    folder = tmp_path / "gta5"
    folder.mkdir()

    subtitles = build_gta_scenario(_draft(), topic=TOPIC, background_folder=folder).subtitles

    assert subtitles.karaoke and subtitles.uppercase and subtitles.burn_in
    assert subtitles.font.name == "Anton-Regular.ttf"
    assert subtitles.font_size == 92
    assert subtitles.max_chars_per_line == 18
    assert subtitles.accent_color == "#FFD600"
    assert subtitles.position_ratio == pytest.approx(0.62)


def test_the_upload_metadata_is_turkish_gaming_with_the_fact_sources(tmp_path: Path) -> None:
    folder = tmp_path / "gta5"
    folder.mkdir()

    scenario = build_gta_scenario(_draft(), topic=TOPIC, background_folder=folder)

    youtube = scenario.youtube
    assert youtube.category_id == "20"
    assert youtube.default_language == "tr"
    assert youtube.privacy_status == "private"
    assert youtube.upload_enabled is False
    assert youtube.synthetic_content_disclosure is True
    assert youtube.title == TITLE
    assert [(source.title, source.url) for source in scenario.sources] == [
        (source.title, source.url) for source in SOURCES
    ]
    assert scenario.project_id.startswith("fort-zancudo-ya-izinsiz-girmek-")


def test_a_missing_gameplay_folder_is_named_in_the_error(tmp_path: Path) -> None:
    with pytest.raises(ScriptGenerationError, match="does not exist") as caught:
        build_gta_scenario(_draft(), topic=TOPIC, background_folder=tmp_path / "missing")

    assert caught.value.hint is not None
    assert "gameplay folder" in caught.value.hint


# --------------------------------------------------------------------------------------
# The topic list
# --------------------------------------------------------------------------------------


def test_topics_carry_their_fact_and_sources(tmp_path: Path) -> None:
    path = tmp_path / "topics-gta.json"
    write_json(
        path,
        {
            "topics": [
                {
                    "topic": TOPIC,
                    "fact": f"  {FACT}  ",
                    "sources": [
                        "https://gta.wiki/w/Fort_Zancudo",
                        {"title": "Grand Theft Wiki", "url": "https://www.grandtheftwiki.com/X"},
                    ],
                },
                {"topic": "Bilgisiz konu", "fact": "   "},
            ]
        },
    )

    first, second = load_topics(path)

    assert first.fact == FACT
    assert [(source.title, source.url) for source in first.sources] == [
        ("gta.wiki", "https://gta.wiki/w/Fort_Zancudo"),
        ("Grand Theft Wiki", "https://www.grandtheftwiki.com/X"),
    ]
    assert second.fact is None
    assert second.sources == ()


@pytest.mark.parametrize(
    "sources",
    [["file:///C:/secret.txt"], ["gta.wiki/w/UFOs"], [{"title": "Başlık"}], [42], "https://x.y"],
)
def test_a_source_that_is_not_a_web_address_is_refused(tmp_path: Path, sources: Any) -> None:
    path = tmp_path / "topics-gta.json"
    write_json(path, {"topics": [{"topic": TOPIC, "fact": FACT, "sources": sources}]})

    with pytest.raises(ConfigurationError, match="topic 1"):
        load_topics(path)


def test_every_bundled_fact_is_backed_by_two_sources_and_follows_the_style() -> None:
    """The shipped list is the product's ground truth, so its own rules are checked too."""
    topics = load_topics(PROJECT_ROOT / "scenarios" / "topics-gta.json")

    assert len(topics) >= 10
    assert len({topic.topic.casefold() for topic in topics}) == len(topics)
    for topic in topics:
        assert topic.fact, topic.topic
        assert len(topic.sources) >= 2, topic.topic
        assert len({source.url for source in topic.sources}) == len(topic.sources), topic.topic
        assert all(source.url.startswith("https://") for source in topic.sources), topic.topic
        assert not re.search(r"[()\"“”«»âîû]", f"{topic.topic} {topic.fact}"), topic.topic


# --------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------


@pytest.fixture
def gta_setup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    """A topic list with one fact and a gameplay folder holding one recording."""
    scenarios = tmp_path / "scenarios"
    scenarios.mkdir()
    write_json(
        scenarios / "topics-gta.json",
        {
            "topics": [
                {
                    "topic": TOPIC,
                    "fact": FACT,
                    "sources": [{"title": source.title, "url": source.url} for source in SOURCES],
                }
            ]
        },
    )
    gameplay = tmp_path / "gameplay"
    gameplay.mkdir()
    (gameplay / "ride.mkv").write_bytes(b"\x00")
    monkeypatch.setenv("SCENARIOS_DIR", str(scenarios))
    monkeypatch.setenv("GTA_BACKGROUND_DIR", str(gameplay))
    monkeypatch.setenv("VIDEO_FORMAT", "shorts")
    get_settings.cache_clear()
    return {"scenarios": scenarios, "gameplay": gameplay}


def _use_model(monkeypatch: pytest.MonkeyPatch, chat: ScriptedChat) -> list[str]:
    """Hand ``chat`` to the CLI instead of Gemini and record when it is built."""
    built: list[str] = []

    def build(settings: Any, model: str | None = None) -> ScriptedChat:
        built.append(model or "")
        return chat

    monkeypatch.setattr(main, "_build_script_generator", build)
    return built


@pytest.mark.parametrize(
    "choice", ["1", TOPIC.upper(), upper_text(TOPIC, "tr"), "fort zancudo'ya ızınsız girmek"]
)
def test_generate_writes_a_gta_scenario_from_the_list(
    gta_setup: dict[str, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    choice: str,
) -> None:
    _use_model(monkeypatch, ScriptedChat(_reply()))
    out = tmp_path / "gta.json"

    result = runner.invoke(main.app, ["generate", "--format", "gta", choice, "--out", str(out)])

    assert result.exit_code == 0, result.output
    scenario = Scenario.model_validate(json.loads(out.read_text(encoding="utf-8")))
    assert scenario.video.background_video.resolved_folder == gta_setup["gameplay"]
    assert scenario.subtitles.karaoke
    assert scenario.youtube.category_id == "20"
    assert [source.url for source in scenario.sources] == [source.url for source in SOURCES]


def test_generate_takes_a_new_topic_with_its_own_fact(
    gta_setup: dict[str, Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    chat = ScriptedChat(_reply())
    _use_model(monkeypatch, chat)
    out = tmp_path / "gta.json"

    result = runner.invoke(
        main.app,
        ["generate", "--format", "gta", "Yeni konu", "--fact", FACT, "--out", str(out)],
    )

    assert result.exit_code == 0, result.output
    assert "Topic: Yeni konu" in chat.calls[0][0][1]["content"]
    assert json.loads(out.read_text(encoding="utf-8"))["sources"] == []


@pytest.mark.parametrize("case", ["no-folder", "no-video", "unknown-topic"])
def test_generate_stops_before_asking_the_model(
    gta_setup: dict[str, Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch, case: str
) -> None:
    built = _use_model(monkeypatch, ScriptedChat())
    topic = "1"
    if case == "no-folder":
        monkeypatch.setenv("GTA_BACKGROUND_DIR", str(tmp_path / "missing"))
    elif case == "no-video":
        (gta_setup["gameplay"] / "ride.mkv").unlink()
        (gta_setup["gameplay"] / "notes.txt").write_text("not a video", encoding="utf-8")
    else:
        topic = "Listede olmayan konu"
    get_settings.cache_clear()

    result = runner.invoke(
        main.app, ["generate", "--format", "gta", topic, "--out", str(tmp_path / "gta.json")]
    )

    assert result.exit_code == 1, result.output
    assert built == []
    assert not (tmp_path / "gta.json").exists()


def test_topics_lists_the_gta_facts(gta_setup: dict[str, Path]) -> None:
    result = runner.invoke(main.app, ["topics", "--gta"])

    assert result.exit_code == 0, result.output
    assert "Fort Zancudo" in result.output


def test_daily_with_the_gta_format_writes_and_renders_a_gta_short(
    gta_setup: dict[str, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    _use_model(monkeypatch, ScriptedChat(_reply()))
    rendered: list[Scenario] = []
    monkeypatch.setattr(
        main, "_execute_run", lambda parsed, settings, options, **_: rendered.append(parsed)
    )
    monkeypatch.setenv("VIDEO_FORMAT", "gta")
    get_settings.cache_clear()

    result = runner.invoke(main.app, ["daily"])

    assert result.exit_code == 0, result.output
    assert len(rendered) == 1
    assert rendered[0].subtitles.karaoke
    assert rendered[0].video.background_video.resolved_folder == gta_setup["gameplay"]
    done = list((gta_setup["scenarios"] / "done").glob("*.json"))
    assert [path.stem for path in done] == [rendered[0].project_id]


def test_daily_dry_run_reads_the_gta_list(
    gta_setup: dict[str, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("VIDEO_FORMAT", "gta")
    get_settings.cache_clear()

    result = runner.invoke(main.app, ["daily", "--dry-run"])

    assert result.exit_code == 0, result.output
    assert "Fort Zancudo" in result.output


def test_settings_accept_the_gta_format_in_any_case(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VIDEO_FORMAT", " GTA ")
    get_settings.cache_clear()

    assert get_settings().VIDEO_FORMAT == "gta"


def test_a_relative_gameplay_folder_resolves_against_the_project(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GTA_BACKGROUND_DIR", "assets/background/gta5")
    get_settings.cache_clear()

    assert get_settings().gta_background_dir() == PROJECT_ROOT / "assets" / "background" / "gta5"


def test_pick_a_topic_by_number_title_or_own_fact(gta_setup: dict[str, Path]) -> None:
    settings = get_settings()

    by_number = main._pick_gta_topic(settings, " 1 ", None)
    by_title = main._pick_gta_topic(settings, upper_text(TOPIC, "tr"), None)
    own = main._pick_gta_topic(settings, "Yeni", "  Bir bilgi.  ")

    assert by_number == by_title
    assert by_number.fact == FACT
    assert own == Topic(topic="Yeni", fact="Bir bilgi.")
    with pytest.raises(ConfigurationError):
        main._pick_gta_topic(settings, "2", None)
