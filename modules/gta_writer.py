"""Turkish GTA 5 Shorts written from one checked fact.

The model never decides what is true. Every topic in ``scenarios/topics-gta.json`` carries a
fact that was checked against at least two sources, and the model only turns it into spoken
Turkish: a hook, the fact, and a payoff. What a model tends to get wrong is checked in code and
sent back for a rewrite: the length, hype words, calls to action, numbers the fact never gave,
and a title that does not name the game.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any, Final

from config.constants import (
    GTA_BASE_TAGS,
    GTA_DEFAULT_SCENES,
    GTA_MAX_SCENES,
    GTA_MAX_WORDS,
    GTA_MIN_SCENES,
    GTA_MIN_WORDS,
    GTA_PLACEHOLDER_SEARCH_TERMS,
    GTA_WORD_TOLERANCE,
    SCRIPT_MAX_ATTEMPTS,
    SCRIPT_MAX_TAGS,
    YOUTUBE_DESCRIPTION_MAX_CHARS,
    YOUTUBE_TITLE_MAX_CHARS,
)
from modules.interfaces import DraftScene, DraftScript, DraftSource
from modules.script_generator import ChatScriptGenerator, extract_json_object
from utils.exceptions import ScriptGenerationError
from utils.logger import get_logger, log_info, log_warn
from utils.text import upper_text

__all__ = ["BANNED_PHRASES", "GtaShortsWriter", "count_words"]

logger = get_logger(__name__)

BANNED_PHRASES: Final[tuple[str, ...]] = (
    # Hype words, which the channel's writing rules leave out.
    "inanılmaz",
    "efsane",
    "şok",
    "çılgın",
    "müthiş",
    "muhteşem",
    "akıl almaz",
    "harika",
    "mükemmel",
    "devrim",
    "devasa",
    "olağanüstü",
    # The opener and the calls to action that every other Short already uses.
    "biliyor muydun",
    "abone",
    "beğenmeyi unutma",
    "yorumlara yaz",
    "bildirimleri aç",
)
"""Matched at the start of a word, so suffixed forms such as ``efsanevi`` count too."""

_BANNED: Final[re.Pattern[str]] = re.compile(
    r"\b(?:" + "|".join(re.escape(phrase) for phrase in BANNED_PHRASES) + ")"
)
_NUMBER: Final[re.Pattern[str]] = re.compile(r"\d+")
_EXCLAMATION: Final[re.Pattern[str]] = re.compile(r"[!¡]+")
_DOUBLED_STOP: Final[re.Pattern[str]] = re.compile(r"([.?])\.+")
_UNSPOKEN: Final[re.Pattern[str]] = re.compile(r"[()\[\]{}\"“”«»#]")
_GAME_NAME: Final[re.Pattern[str]] = re.compile(r"\bgta\b(\s*v\b)?", re.IGNORECASE)
_DETACHED_SUFFIX: Final[re.Pattern[str]] = re.compile(
    r"\b([A-ZÇĞİÖŞÜ][\wçğıöşü]*|\d+) "
    r"(nun|nın|nin|nün|te|ta|den|dan|deki|daki|teki|taki)\b"
)
"""A name or number with its suffix split off by a space, as in UFO nun or GTA 5 te. Only
suffixes that are never words of their own are joined back, so de and da stay apart."""
_GAME_NUMBERS: Final[frozenset[int]] = frozenset({5})
"""Always allowed, because the game's own name is GTA 5."""
_TURKISH_LETTERS: Final[frozenset[str]] = frozenset("çğıöşüÇĞİÖŞÜ")
"""A reply of fifty Turkish words without any of these was typed in plain ASCII, which the
voice mispronounces and the captions misspell, for example yuzde instead of yüzde."""
_SENTENCE_END: Final[tuple[str, ...]] = (".", "?", "…")

_SYSTEM_PROMPT: Final[str] = """\
You write Turkish narration for YouTube Shorts about the video game GTA 5. A text-to-speech \
voice reads it over gameplay footage.

Reply with a single JSON object and nothing else. No prose, no markdown, no code fences.

Required shape:
{{
  "title": string,
  "description": string,
  "tags": [string],
  "scenes": [{{"narration": string}}]
}}

Content:
- Use only the fact in the brief. Do not add other facts, numbers, dates, names or places. \
Leave out anything the brief does not say. When the fact runs out, end the Short; never pad \
it with details of your own.
- Scene 1 is the hook: one short sentence, built from the most surprising part of the fact, \
that makes a GTA player want to hear the rest. Open with what happens or what is strange, \
never with a definition such as a place being a military base. No greeting and no question \
about whether the viewer knew it.
- The middle scenes explain the fact concretely: where it happens in the game and what the \
player does or sees.
- The last scene is the payoff: the detail that makes the fact worth sharing. End on it, with \
no call to action.

Style:
- Everyday spoken Turkish that addresses the viewer as sen. Short sentences.
- Proper Turkish spelling with its own letters ç, ğ, ı, ö, ş and ü, a capital letter at the \
start of every sentence and a full stop at its end.
- Write numbers with digits, the way the fact does, because they appear in the captions.
- All scenes together must be {min_words} to {max_words} words long.
- "scenes" must contain exactly {scene_count} objects, each one or two sentences.
- Never use these words or phrases: {banned}.
- No exclamation marks, parentheses, quotation marks, emoji or hashtags. Keep the apostrophe \
Turkish puts between a name and its suffix, for example UFO'nun, GTA 5'te or Los Santos'ta.
- Write names and abbreviations as the game does, for example Los Santos, Mount Chiliad, \
Franklin, UFO or FIB.

Metadata:
- "title": Turkish, at most {title_max} characters. Say plainly what the video is about and \
name GTA 5. No clickbait, no emoji, no hashtags and no words in capitals for emphasis.
- "description": Turkish, one or two plain sentences.
- "tags": 5 to {max_tags} lowercase keywords about GTA 5 and the topic.

The shape of a good Short, shown on a different fact. Never reuse its wording:
Fact: Outside missions, the player can switch between Michael, Franklin and Trevor at any time.
"scenes": [
  {{"narration": "GTA 5'te tek tuşla bambaşka bir hayatın ortasına düşebilirsin."}},
  {{"narration": "Hikayede Michael, Franklin ve Trevor diye üç ana karakter var."}},
  {{"narration": "Görev dışındayken istediğin an bu üçü arasında geçiş yapıyorsun."}},
  {{"narration": "Kamera havalanıyor ve seni seçtiğin karakterin yanına indiriyor."}},
  {{"narration": "Yani oyunda aynı anda üç ayrı hikaye akıp gidiyor."}}
]
"""


def count_words(text: str) -> int:
    """Count spoken words the way the length rule does: runs separated by whitespace.

    Args:
        text: Narration text.

    Returns:
        The number of words.
    """
    return len(text.split())


def _turkish_lower(text: str) -> str:
    """Lowercase with Turkish dotted and dotless i, so banned words match in capitals too."""
    return text.replace("I", "ı").replace("İ", "i").lower()


def _numbers(text: str) -> set[int]:
    """The integers written with digits in ``text``, so 03 and 3 count as the same number."""
    return {int(match) for match in _NUMBER.findall(text)}


def _tidy(text: str) -> str:
    """Drop the marks the style rules forbid, which a voice would not say anyway."""
    text = _EXCLAMATION.sub(".", text)
    text = _DOUBLED_STOP.sub(r"\1", text)
    text = _GAME_NAME.sub(lambda match: match.group(0).upper(), text)
    text = ChatScriptGenerator._collapse(_UNSPOKEN.sub("", text))
    return _DETACHED_SUFFIX.sub(r"\1'\2", text)


def _capitalised(text: str) -> str:
    """Start with a capital, the Turkish way, so a leading i becomes İ."""
    return upper_text(text[:1], "tr") + text[1:]


def _as_sentence(text: str) -> str:
    """A capital at the start and a full stop at the end, which the voice uses for pauses."""
    text = _capitalised(text.rstrip(",;: "))
    return text if text.endswith(_SENTENCE_END) else f"{text}."


class GtaShortsWriter:
    """Writes a Turkish GTA 5 Short around one checked fact."""

    def __init__(self, generator: ChatScriptGenerator) -> None:
        """Wrap a script generator, so Gemini and Ollama both work through one chat interface.

        Args:
            generator: The backend that sends the conversation and returns the model's text.
        """
        self._inner = generator

    def generate(
        self,
        topic: str,
        fact: str,
        *,
        scene_count: int = GTA_DEFAULT_SCENES,
        sources: Sequence[DraftSource] = (),
        extra_guidance: str | None = None,
    ) -> DraftScript:
        """Draft a Short, asking again with the reason whenever a reply breaks a rule.

        Args:
            topic: The short subject line, for example the place the fact is about.
            fact: The checked statement the narration must stay within.
            scene_count: How many narration chunks to ask for, kept between the pack's limits.
            sources: Pages the fact was checked against, carried onto the draft for review.
            extra_guidance: Optional extra steering appended to the request.

        Returns:
            A draft whose scenes hold the narration and whose sources are ``sources``.

        Raises:
            ScriptGenerationError: If the topic or fact is blank, or no attempt yields a reply
                that passes every rule.
        """
        if not topic.strip():
            raise ScriptGenerationError("The topic is empty; there is nothing to write about.")
        if not fact.strip():
            raise ScriptGenerationError(
                f"The GTA topic {topic.strip()} has no fact to write from.",
                hint="Give every entry in scenarios/topics-gta.json a checked fact field.",
            )

        wanted = max(GTA_MIN_SCENES, min(GTA_MAX_SCENES, scene_count))
        messages = self._build_messages(topic, fact, wanted, extra_guidance)
        allowed_numbers = _numbers(f"{topic} {fact}") | _GAME_NUMBERS
        last_error = "no attempt was made"

        for attempt in range(1, SCRIPT_MAX_ATTEMPTS + 1):
            log_info(f"Writing the GTA 5 Short on '{topic}' ({attempt}/{SCRIPT_MAX_ATTEMPTS})...")
            reply = self._inner._chat(messages, wanted)
            try:
                payload = extract_json_object(reply)
                return self._coerce(payload, allowed_numbers=allowed_numbers, sources=sources)
            except ValueError as exc:
                last_error = str(exc)
                logger.debug("GTA attempt %d was rejected: %s", attempt, last_error)
                if attempt == SCRIPT_MAX_ATTEMPTS:
                    break
                log_warn(f"The reply broke a rule ({last_error}). Asking again.")
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
            f"No usable GTA 5 Short after {SCRIPT_MAX_ATTEMPTS} attempt(s): {last_error}",
            hint="Run it again, or shorten the fact so it fits a 30-second Short.",
        )

    @staticmethod
    def _build_messages(
        topic: str,
        fact: str,
        scene_count: int,
        extra_guidance: str | None,
    ) -> list[dict[str, str]]:
        """Assemble the system rules and the brief.

        Args:
            topic: The subject line.
            fact: The checked statement.
            scene_count: How many scenes to ask for.
            extra_guidance: Optional extra steering.

        Returns:
            The message list to send.
        """
        system = _SYSTEM_PROMPT.format(
            min_words=GTA_MIN_WORDS,
            max_words=GTA_MAX_WORDS,
            scene_count=scene_count,
            banned=", ".join(BANNED_PHRASES),
            title_max=YOUTUBE_TITLE_MAX_CHARS,
            max_tags=SCRIPT_MAX_TAGS,
        )
        brief = f"Topic: {topic.strip()}\nFact: {fact.strip()}"
        if extra_guidance and extra_guidance.strip():
            brief += f"\nAdditional direction: {extra_guidance.strip()}"
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": brief},
        ]

    def _coerce(
        self,
        payload: dict[str, Any],
        *,
        allowed_numbers: set[int],
        sources: Sequence[DraftSource],
    ) -> DraftScript:
        """Clean a decoded reply and check it against every rule.

        Args:
            payload: The decoded JSON object.
            allowed_numbers: Numbers the topic and fact give; the narration may use no others.
            sources: Pages the fact was checked against.

        Returns:
            The draft.

        Raises:
            ValueError: With the reason phrased for the model, so the rewrite request is exact.
        """
        raw_scenes = payload.get("scenes")
        if not isinstance(raw_scenes, list) or not raw_scenes:
            raise ValueError('"scenes" was missing or not a non-empty array')

        narrations: list[str] = []
        for index, entry in enumerate(raw_scenes[:GTA_MAX_SCENES], start=1):
            raw = entry.get("narration", "") if isinstance(entry, dict) else entry
            narration = _tidy(self._inner._clean_narration(str(raw)))
            if not narration:
                raise ValueError(f'scene {index} had an empty "narration"')
            narrations.append(_as_sentence(narration))
        if len(narrations) < GTA_MIN_SCENES:
            raise ValueError(
                f"only {len(narrations)} scene(s) came back; write at least {GTA_MIN_SCENES}"
            )

        spoken = " ".join(narrations)
        if not _TURKISH_LETTERS.intersection(spoken):
            raise ValueError(
                "the narration was typed without Turkish letters; write proper Turkish with "
                "ç, ğ, ı, ö, ş and ü"
            )
        words = count_words(spoken)
        if not GTA_MIN_WORDS - GTA_WORD_TOLERANCE <= words <= GTA_MAX_WORDS + GTA_WORD_TOLERANCE:
            raise ValueError(
                f"the narration was {words} words; all scenes together must be "
                f"{GTA_MIN_WORDS} to {GTA_MAX_WORDS} words"
            )

        invented = sorted(_numbers(spoken) - allowed_numbers)
        if invented:
            raise ValueError(
                "the narration has numbers the fact does not give: "
                f"{', '.join(map(str, invented))}. Use only numbers from the fact"
            )

        title = _capitalised(
            _tidy(
                self._inner._clean_narration(
                    str(payload.get("title", "")), max_chars=YOUTUBE_TITLE_MAX_CHARS
                )
            )
        )
        if not title:
            raise ValueError('"title" was empty')
        if "gta" not in title.lower():
            raise ValueError('"title" must name GTA 5')

        description = _capitalised(
            _tidy(str(payload.get("description", "")))[:YOUTUBE_DESCRIPTION_MAX_CHARS]
        )

        found = sorted(set(_BANNED.findall(_turkish_lower(f"{spoken} {title} {description}"))))
        if found:
            raise ValueError(f"the text used banned words: {', '.join(found)}")

        raw_tags = payload.get("tags")
        if isinstance(raw_tags, str):
            raw_tags = raw_tags.split(",")
        model_tags = raw_tags if isinstance(raw_tags, list) else []
        tags = self._inner._clean_tags([*GTA_BASE_TAGS, *model_tags])

        return DraftScript(
            title=title,
            description=description,
            tags=tags,
            scenes=tuple(
                DraftScene(narration=narration, search_terms=GTA_PLACEHOLDER_SEARCH_TERMS)
                for narration in narrations
            ),
            sources=tuple(sources),
        )
