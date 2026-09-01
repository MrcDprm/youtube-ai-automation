"""Turn a generated draft into a schema-valid scenario file.

Everything a language model is unreliable at lives here instead of in the prompt: the project
slug, resolution, frame rate, codec settings, voice, subtitle styling and the duration ceiling
are all computed deterministically. The model only ever supplies prose.

The result is validated through :class:`~models.scenario.Scenario` before being written, so
``generate`` can never emit a file that ``run`` would later reject.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from config.constants import (
    BRAND_BADLY_DRAWN_WHY,
    DRAWN_BRAND_ID,
    DRAWN_CATEGORY_ID,
    DRAWN_DEFAULT_MINUTES,
    DRAWN_PLACEHOLDER_SEARCH_TERMS,
    DRAWN_SUBTITLE_FONT_SIZE,
    DRAWN_SUBTITLE_POSITION_RATIO,
    DRAWN_TTS_RATE,
    DRAWN_TTS_VOICE,
    DRAWN_ZOOM_END,
    DURATION_ESTIMATE_HEADROOM,
    EVERY_LEVEL_POV_BRAND_ID,
    FILE_BRAND_ID,
    FILE_CATEGORY_ID,
    FILE_DEFAULT_MINUTES,
    FILE_SUBTITLE_FONT_SIZE,
    FILE_SUBTITLE_POSITION_RATIO,
    FILE_TTS_RATE,
    FILE_TTS_VOICE,
    NARRATION_CHARS_PER_SECOND,
    PAINT_PLACEHOLDER_SEARCH_TERMS,
    POV_CATEGORY_ID,
    POV_DEFAULT_MINUTES,
    POV_PLACEHOLDER_SEARCH_TERMS,
    POV_SUBTITLE_COLOR,
    POV_SUBTITLE_FONT_SIZE,
    POV_SUBTITLE_POSITION_RATIO,
    POV_SUBTITLE_STROKE,
    POV_TTS_RATE,
    POV_TTS_VOICE,
    POV_ZOOM_END,
    STORY_DEFAULT_MAX_DURATION,
    STORY_SUBTITLE_FONT_SIZE,
    STORY_SUBTITLE_MAX_CHARS,
    STORY_SUBTITLE_POSITION_RATIO,
    STORY_TTS_RATE,
    TURKISH_SLUG_MAP,
    VIDEO_FORMAT_PAINT,
    VIDEO_FORMAT_STORY,
)
from models.scenario import Orientation, Scenario
from modules.interfaces import DraftScript
from modules.language import chars_per_second_for, get_language_pack, pick_voice
from utils.exceptions import ScriptGenerationError
from utils.fs import write_json

__all__ = [
    "build_drawn_scenario",
    "build_file_scenario",
    "build_paint_scenario",
    "build_pov_scenario",
    "build_scenario",
    "build_story_scenario",
    "estimate_total_seconds",
    "slugify",
    "write_scenario",
]

_NON_SLUG_CHARS = re.compile(r"[^a-z0-9]+")

_MIN_SLUG_LENGTH = 3
_MAX_SLUG_LENGTH = 64
_MAX_TOPIC_SLUG_LENGTH = 45
"""Leaves room for the ``-YYYYMMDD`` suffix inside the 64-character schema limit."""

_MIN_SCENE_SECONDS = 2.5
_MIN_MAX_DURATION = 60.0
_MAX_MAX_DURATION = 43_200.0


def slugify(text: str, *, fallback: str = "video") -> str:
    """Convert arbitrary text into a lowercase hyphenated slug.

    Turkish letters are transliterated before ASCII folding because characters such as ``ı``
    and ``ş`` have no Unicode decomposition and would otherwise simply vanish.

    Args:
        text: Arbitrary text, typically a topic or title.
        fallback: Returned when nothing usable survives cleaning.

    Returns:
        A slug matching ``[a-z0-9-]+``, never empty.
    """
    mapped = "".join(TURKISH_SLUG_MAP.get(char, char) for char in text)
    folded = unicodedata.normalize("NFKD", mapped)
    ascii_only = folded.encode("ascii", "ignore").decode("ascii").lower()
    cleaned = _NON_SLUG_CHARS.sub("-", ascii_only).strip("-")
    return cleaned or fallback


def make_project_id(topic: str, *, now: datetime | None = None) -> str:
    """Derive a unique, schema-valid project id from a topic.

    Args:
        topic: The video's subject.
        now: Timestamp used for the date suffix; defaults to the current UTC time.

    Returns:
        A slug matching ``^[a-z0-9_-]{3,64}$``.
    """
    stamp = (now or datetime.now(UTC)).strftime("%Y%m%d")
    base = slugify(topic)[:_MAX_TOPIC_SLUG_LENGTH].strip("-")
    if len(base) < _MIN_SLUG_LENGTH:
        base = "video"
    return f"{base}-{stamp}"[:_MAX_SLUG_LENGTH].strip("-")


def estimate_scene_seconds(narration: str, scene_gap: float) -> float:
    """Estimate how long a scene will run, before the audio actually exists.

    Args:
        narration: The scene's spoken text.
        scene_gap: Silence appended after the narration.

    Returns:
        An estimated duration in seconds.
    """
    spoken = len(narration) / NARRATION_CHARS_PER_SECOND
    return max(_MIN_SCENE_SECONDS, spoken) + scene_gap


def estimate_total_seconds(draft: DraftScript, scene_gap: float) -> float:
    """Estimate the finished video's runtime.

    Args:
        draft: The generated script.
        scene_gap: Silence appended after each scene.

    Returns:
        The summed estimate in seconds.
    """
    return sum(estimate_scene_seconds(scene.narration, scene_gap) for scene in draft.scenes)


def _clips_for(seconds: float) -> int:
    """Choose how many stock clips a scene should cut between.

    A single clip stretched over a long narration looks static, so longer scenes get more cuts.

    Args:
        seconds: The scene's estimated duration.

    Returns:
        A clip count within the schema's 1-4 range.
    """
    if seconds < 9.0:
        return 1
    if seconds < 18.0:
        return 2
    return 3


def build_scenario(
    draft: DraftScript,
    *,
    topic: str,
    project_id: str | None = None,
    orientation: Orientation = "portrait",
    voice: str | None = None,
    language: str = "tr",
    upload_enabled: bool = False,
    burn_in: bool = True,
    scene_gap: float = 0.3,
    music_file: Path | None = None,
    now: datetime | None = None,
) -> Scenario:
    """Assemble and validate a complete scenario from a draft.

    Args:
        draft: The generated creative content.
        topic: The original topic, used for the project id when none is given.
        project_id: Explicit project id; derived from ``topic`` when omitted.
        orientation: Target frame orientation. The resolution is derived from it.
        voice: edge-tts voice name; the schema default applies when omitted.
        language: BCP-47 language code recorded as the video's default language.
        upload_enabled: Whether ``run`` should upload. Off by default so a generated file
            never publishes something nobody has read.
        burn_in: Whether to burn subtitles into the frame.
        scene_gap: Silence appended after each scene's narration.
        music_file: Optional background music track to enable.
        now: Timestamp used for the project id suffix.

    Returns:
        A validated :class:`~models.scenario.Scenario`.

    Raises:
        ScriptGenerationError: If the draft has no scenes, or the assembled payload somehow
            violates the schema, reported per field.
    """
    if not draft.scenes:
        raise ScriptGenerationError("The draft contains no scenes.")

    scenes: list[dict[str, Any]] = []
    for index, scene in enumerate(draft.scenes, start=1):
        seconds = estimate_scene_seconds(scene.narration, scene_gap)
        scenes.append(
            {
                "id": index,
                "narration": scene.narration,
                "search_terms": list(scene.search_terms),
                "clips_per_scene": _clips_for(seconds),
                "min_clip_duration": 3.0,
                "zoom_effect": True,
            }
        )

    estimated = estimate_total_seconds(draft, scene_gap)
    ceiling = min(
        _MAX_MAX_DURATION, max(_MIN_MAX_DURATION, round(estimated * DURATION_ESTIMATE_HEADROOM))
    )

    video: dict[str, Any] = {
        "orientation": orientation,
        "fps": 30,
        "max_duration_seconds": ceiling,
        "scene_gap_seconds": scene_gap,
        # Zero means a straight concatenation, which is both faster and immune to the
        # "crossfade longer than the shortest scene" rule.
        "crossfade_seconds": 0.0,
        "video_bitrate_crf": 20,
        "preset": "medium",
    }
    if music_file is not None:
        video["background_music"] = {
            "enabled": True,
            "file": str(music_file),
            "volume": 0.08,
            "fade_in_seconds": 1.5,
            "fade_out_seconds": 2.5,
            "duck_to": 0.5,
        }

    tts: dict[str, Any] = {"rate": "+8%", "normalize_text": True, "language": language}
    if voice:
        tts["voice"] = voice

    payload: dict[str, Any] = {
        "project_id": project_id or make_project_id(topic, now=now),
        "video": video,
        "tts": tts,
        "subtitles": {
            "enabled": True,
            "burn_in": burn_in,
            "max_chars_per_line": 30,
            "max_lines": 2,
            "font_size": 62,
            "position_ratio": 0.72,
        },
        "youtube": {
            "upload_enabled": upload_enabled,
            "title": draft.title,
            "description": draft.description,
            "tags": list(draft.tags),
            "category_id": "27",
            "privacy_status": "private",
            "made_for_kids": False,
            "synthetic_content_disclosure": True,
            "default_language": language,
            "thumbnail_enabled": True,
        },
        "scenes": scenes,
    }

    try:
        return Scenario.model_validate(payload)
    except Exception as exc:  # pragma: no cover - guards against a schema drift regression
        raise ScriptGenerationError(
            f"The assembled scenario failed its own schema validation: {exc}",
            hint="This is a bug in modules/scenario_builder.py, not in your topic.",
        ) from exc


def build_story_scenario(
    draft: DraftScript,
    *,
    topic: str,
    project_id: str | None = None,
    orientation: Orientation = "landscape",
    voice: str | None = None,
    language: str = "tr",
    upload_enabled: bool = False,
    burn_in: bool = True,
    scene_gap: float = 0.3,
    music_file: Path | None = None,
    now: datetime | None = None,
    target_seconds: float | None = None,
    minutes: int | None = None,
) -> Scenario:
    """Assemble a longform photo-story scenario from a chaptered draft.

    Shorts continues to use :func:`build_scenario`. This path sets ``format`` to ``story``,
    landscape by default, story subtitle styling, and a voice from the language pack.

    Args:
        draft: The generated creative content (one scene per chapter).
        topic: The original topic, used for the project id when none is given.
        project_id: Explicit project id; derived from ``topic`` when omitted.
        orientation: Target frame orientation.
        voice: edge-tts voice name; a language-pack voice is chosen when omitted.
        language: Narration language code.
        upload_enabled: Whether ``run`` should upload.
        burn_in: Whether to burn subtitles into the frame.
        scene_gap: Silence appended after each chapter's narration.
        music_file: Optional background music track to enable.
        now: Timestamp used for the project id suffix.
        target_seconds: Desired spoken length; stored on the scenario for ``run`` trimming.
        minutes: When set, the project id includes ``{minutes}dk`` so a re-render does not
            overwrite an older cut.

    Returns:
        A validated :class:`~models.scenario.Scenario`.

    Raises:
        ScriptGenerationError: If the draft has no scenes, or the assembled payload
            violates the schema.
    """
    if not draft.scenes:
        raise ScriptGenerationError("The draft contains no scenes.")

    if project_id:
        resolved_id = project_id
    elif minutes is not None:
        stamp = (now or datetime.now(UTC)).strftime("%Y%m%d")
        base = slugify(topic)[:_MAX_TOPIC_SLUG_LENGTH].strip("-") or "video"
        resolved_id = f"{base}-{int(minutes)}dk-{stamp}"[:_MAX_SLUG_LENGTH].strip("-")
    else:
        resolved_id = make_project_id(topic, now=now)
    pack = get_language_pack(language)
    resolved_voice = pick_voice(language, resolved_id, override=voice)
    cps = chars_per_second_for(language)

    scenes: list[dict[str, Any]] = []
    for index, scene in enumerate(draft.scenes, start=1):
        scenes.append(
            {
                "id": index,
                "narration": scene.narration,
                "search_terms": list(scene.search_terms),
                "clips_per_scene": 1,
                "min_clip_duration": 3.0,
                "zoom_effect": True,
            }
        )

    spoken = sum(len(scene.narration) / cps for scene in draft.scenes)
    estimated = spoken + scene_gap * len(draft.scenes)
    desired = target_seconds if target_seconds is not None else estimated
    ceiling = min(
        _MAX_MAX_DURATION,
        max(
            STORY_DEFAULT_MAX_DURATION,
            round(max(desired, estimated) * DURATION_ESTIMATE_HEADROOM),
        ),
    )

    video: dict[str, Any] = {
        "format": VIDEO_FORMAT_STORY,
        "orientation": orientation,
        "fps": 30,
        "max_duration_seconds": ceiling,
        "scene_gap_seconds": scene_gap,
        "crossfade_seconds": 0.0,
        "video_bitrate_crf": 20,
        "preset": "medium",
        "story_visual": {},
    }
    if target_seconds is not None:
        video["target_duration_seconds"] = round(desired, 1)
    if music_file is not None:
        video["background_music"] = {
            "enabled": True,
            "file": str(music_file),
            "volume": 0.08,
            "fade_in_seconds": 1.5,
            "fade_out_seconds": 2.5,
            "duck_to": 0.5,
        }

    payload: dict[str, Any] = {
        "project_id": resolved_id,
        "video": video,
        "tts": {
            "voice": resolved_voice,
            "rate": STORY_TTS_RATE,
            "normalize_text": True,
            "language": language,
        },
        "subtitles": {
            "enabled": True,
            "burn_in": burn_in,
            "max_chars_per_line": STORY_SUBTITLE_MAX_CHARS,
            "max_lines": 2,
            "font_size": STORY_SUBTITLE_FONT_SIZE,
            "position_ratio": STORY_SUBTITLE_POSITION_RATIO,
            "color": "#FFFFFF",
            "accent_color": "#FFD34F",
        },
        "youtube": {
            "upload_enabled": upload_enabled,
            "title": draft.title,
            "description": draft.description,
            "tags": list(draft.tags),
            "category_id": "27",
            "privacy_status": "private",
            "made_for_kids": False,
            "synthetic_content_disclosure": True,
            "default_language": pack.youtube_language,
            "thumbnail_enabled": True,
        },
        "scenes": scenes,
    }

    try:
        return Scenario.model_validate(payload)
    except Exception as exc:  # pragma: no cover - guards against a schema drift regression
        raise ScriptGenerationError(
            f"The assembled story scenario failed its own schema validation: {exc}",
            hint="This is a bug in modules/scenario_builder.py, not in your topic.",
        ) from exc


def build_paint_scenario(
    draft: DraftScript,
    *,
    topic: str,
    project_id: str | None = None,
    orientation: Orientation = "landscape",
    voice: str | None = None,
    language: str = "en",
    upload_enabled: bool = False,
    burn_in: bool = True,
    scene_gap: float = 0.3,
    music_file: Path | None = None,
    now: datetime | None = None,
    target_seconds: float | None = None,
    minutes: int | None = None,
    tts_rate: str | None = None,
    category_id: str | None = None,
    subtitle_font_size: int | None = None,
    subtitle_position_ratio: float | None = None,
    placeholder_search_terms: tuple[str, ...] | None = None,
    zoom_opening_end: float | None = None,
    zoom_body_end: float | None = None,
    brand_id: str | None = None,
    subtitle_color: str | None = None,
    subtitle_accent: str | None = None,
    subtitle_stroke: str | None = None,
    numeral_display: bool = False,
    use_zenn: bool | None = None,
) -> Scenario:
    """Assemble a Badly Drawn Why scenario: spoken essay + drawing beats, no Pexels.

    Args:
        draft: Chapters plus ``visual_beats``.
        topic: Original subject, used in the project id.
        project_id: Explicit id; derived when omitted.
        orientation: Frame orientation, landscape by default.
        voice: edge-tts voice; language-pack default when omitted.
        language: Narration language code.
        upload_enabled: Whether ``run`` should upload.
        burn_in: Whether to burn subtitles into the frame.
        scene_gap: Silence after each chapter.
        music_file: Optional music bed.
        now: Timestamp for the project id suffix.
        target_seconds: Desired spoken length, stored for ``run`` trimming.
        minutes: When set, the project id includes ``{minutes}dk``.
        tts_rate: Edge TTS rate; ``STORY_TTS_RATE`` when omitted.
        category_id: YouTube category; Education ``27`` when omitted.
        subtitle_font_size: Burn-in size; story default when omitted.
        subtitle_position_ratio: Caption vertical ratio; story default when omitted.
        placeholder_search_terms: Unused clip queries stored on scenes (paint never searches).
        zoom_opening_end: Ken Burns end scale for the opening still.
        zoom_body_end: Ken Burns end scale for remaining stills.
        brand_id: Stamped onto ``youtube.brand_id`` so Studio can tell brands apart.
        subtitle_color: Burn-in fill; white when omitted.
        subtitle_accent: Optional caption accent.
        subtitle_stroke: Outline colour; default stroke when omitted.
        numeral_display: When true, years and large counts show as digits in captions.
        use_zenn: Stick-cut Zenn renderer (~2s programmatic beats). Defaults to false;
            legacy MS Paint stills need ``visual_beats`` and ``use_zenn=False``.

    Returns:
        A validated paint scenario.

    Raises:
        ScriptGenerationError: If the draft has no scenes or fewer than two beats.
    """
    if not draft.scenes:
        raise ScriptGenerationError("The draft contains no scenes.")

    resolved_brand = brand_id or BRAND_BADLY_DRAWN_WHY
    zenn = use_zenn if use_zenn is not None else False
    if not zenn and len(draft.visual_beats) < 2:
        raise ScriptGenerationError(
            "Paint format needs at least two visual beats.",
            hint="Re-run generate --format paint or pass use_zenn=True.",
        )

    if project_id:
        resolved_id = project_id
    elif minutes is not None:
        stamp = (now or datetime.now(UTC)).strftime("%Y%m%d")
        base = slugify(topic)[:_MAX_TOPIC_SLUG_LENGTH].strip("-") or "video"
        resolved_id = f"{base}-{int(minutes)}dk-{stamp}"[:_MAX_SLUG_LENGTH].strip("-")
    else:
        resolved_id = make_project_id(topic, now=now)
    pack = get_language_pack(language)
    resolved_voice = pick_voice(language, resolved_id, override=voice)
    cps = chars_per_second_for(language)

    default_terms = placeholder_search_terms or PAINT_PLACEHOLDER_SEARCH_TERMS
    scenes: list[dict[str, Any]] = []
    for index, scene in enumerate(draft.scenes, start=1):
        terms = list(scene.search_terms) or list(default_terms)
        scenes.append(
            {
                "id": index,
                "narration": scene.narration,
                "search_terms": terms,
                "clips_per_scene": 1,
                "min_clip_duration": 3.0,
                "zoom_effect": True,
            }
        )

    beats: list[dict[str, Any]] = []
    used_slugs: set[str] = set()
    for index, beat in enumerate(draft.visual_beats, start=1):
        slug = slugify(beat.slug)[:40] or f"beat-{index:02d}"
        if len(slug) < 2:
            slug = f"beat-{index:02d}"
        if slug in used_slugs:
            slug = f"{index:02d}-{slug}"[:48]
        used_slugs.add(slug)
        beats.append(
            {
                "slug": slug,
                "prompt": beat.prompt[:1600],
                "covers": (beat.covers or "")[:500],
            }
        )

    spoken = sum(len(scene.narration) / cps for scene in draft.scenes)
    estimated = spoken + scene_gap * len(draft.scenes)
    desired = target_seconds if target_seconds is not None else estimated
    ceiling = min(
        _MAX_MAX_DURATION,
        max(
            STORY_DEFAULT_MAX_DURATION,
            round(max(desired, estimated) * DURATION_ESTIMATE_HEADROOM),
        ),
    )
    photo_count = 2 if zenn else max(2, len(beats))

    story_visual: dict[str, Any] = {
        "photo_count": photo_count,
        "opening_photo_count": 1,
        "zenn_enabled": zenn,
    }
    if zoom_opening_end is not None:
        story_visual["zoom_opening_end"] = zoom_opening_end
    if zoom_body_end is not None:
        story_visual["zoom_body_end"] = zoom_body_end

    video: dict[str, Any] = {
        "format": VIDEO_FORMAT_PAINT,
        "orientation": orientation,
        "fps": 30,
        "max_duration_seconds": ceiling,
        "scene_gap_seconds": scene_gap,
        "crossfade_seconds": 0.0,
        "video_bitrate_crf": 20,
        "preset": "medium",
        "story_visual": story_visual,
        "visual_beats": beats,
    }
    if target_seconds is not None:
        video["target_duration_seconds"] = round(desired, 1)
    if music_file is not None:
        video["background_music"] = {
            "enabled": True,
            "file": str(music_file),
            "volume": 0.08,
            "fade_in_seconds": 1.5,
            "fade_out_seconds": 2.5,
            "duck_to": 0.5,
        }

    hook = (draft.thumbnail_hook or "").strip()[:40]
    payload: dict[str, Any] = {
        "project_id": resolved_id,
        "video": video,
        "tts": {
            "voice": resolved_voice,
            "rate": tts_rate or STORY_TTS_RATE,
            "normalize_text": True,
            "language": language,
        },
        "subtitles": {
            "enabled": True,
            "burn_in": burn_in,
            "max_chars_per_line": STORY_SUBTITLE_MAX_CHARS,
            "max_lines": 2,
            "font_size": subtitle_font_size or STORY_SUBTITLE_FONT_SIZE,
            "position_ratio": subtitle_position_ratio or STORY_SUBTITLE_POSITION_RATIO,
            "color": subtitle_color or "#FFFFFF",
            "stroke_width": 5,
            **({"stroke_color": subtitle_stroke} if subtitle_stroke else {}),
            **({"accent_color": subtitle_accent or "#FFD600"} if zenn or subtitle_accent else {}),
            **({"numeral_display": True} if numeral_display else {}),
        },
        "youtube": {
            "upload_enabled": upload_enabled,
            "title": draft.title,
            "description": draft.description,
            "tags": list(draft.tags),
            "category_id": category_id or "27",
            "privacy_status": "unlisted",
            "made_for_kids": False,
            "synthetic_content_disclosure": True,
            "default_language": pack.youtube_language,
            "thumbnail_enabled": True,
            "thumbnail_hook": hook,
            **({"brand_id": brand_id or resolved_brand} if (brand_id or zenn) else {}),
        },
        "scenes": scenes,
    }

    try:
        return Scenario.model_validate(payload)
    except Exception as exc:  # pragma: no cover - guards against a schema drift regression
        raise ScriptGenerationError(
            f"The assembled paint scenario failed its own schema validation: {exc}",
            hint="This is a bug in modules/scenario_builder.py, not in your topic.",
        ) from exc


def build_file_scenario(
    draft: DraftScript,
    *,
    topic: str,
    project_id: str | None = None,
    voice: str | None = None,
    language: str = "en",
    upload_enabled: bool = False,
    now: datetime | None = None,
    target_seconds: float | None = None,
    minutes: int | None = None,
) -> Scenario:
    """Assemble an After Hours File scenario: one closed case, illustrated stills, no Pexels.

    Same paint render path as Badly Drawn Why with slower British TTS, Entertainment
    category, and slightly lower captions.

    Args:
        draft: Chapters plus ``visual_beats``.
        topic: Original subject, used in the project id.
        project_id: Explicit id; derived when omitted.
        voice: edge-tts voice; ``FILE_TTS_VOICE`` when omitted.
        language: Narration language code.
        upload_enabled: Whether ``run`` should upload.
        now: Timestamp for the project id suffix.
        target_seconds: Desired spoken length, stored for ``run`` trimming.
        minutes: When set, the project id includes ``{minutes}dk``.

    Returns:
        A validated paint-format scenario with After Hours File defaults.
    """
    return build_paint_scenario(
        draft,
        topic=topic,
        project_id=project_id,
        voice=voice or FILE_TTS_VOICE,
        language=language,
        upload_enabled=upload_enabled,
        now=now,
        target_seconds=target_seconds,
        minutes=FILE_DEFAULT_MINUTES if minutes is None else minutes,
        tts_rate=FILE_TTS_RATE,
        category_id=FILE_CATEGORY_ID,
        subtitle_font_size=FILE_SUBTITLE_FONT_SIZE,
        subtitle_position_ratio=FILE_SUBTITLE_POSITION_RATIO,
        brand_id=FILE_BRAND_ID,
    )


def build_drawn_scenario(
    draft: DraftScript,
    *,
    topic: str,
    project_id: str | None = None,
    voice: str | None = None,
    language: str = "en",
    upload_enabled: bool = False,
    now: datetime | None = None,
    target_seconds: float | None = None,
    minutes: int | None = None,
    tts_rate: str | None = None,
    subtitle_font_size: int | None = None,
    subtitle_position_ratio: float | None = None,
    subtitle_color: str | None = None,
    subtitle_accent: str | None = None,
    subtitle_stroke: str | None = None,
) -> Scenario:
    """Assemble a Drawn Anyway scenario: one true story, cartoon beats, no Pexels.

    Same paint render path as the other brands, Entertainment category, and a
    slightly stronger Ken Burns zoom. Voice, rate, and caption colours may vary
    per episode; ``youtube.brand_id`` stays Drawn Anyway.

    Args:
        draft: Chapters plus ``visual_beats``.
        topic: Original subject, used in the project id.
        project_id: Explicit id; derived when omitted.
        voice: edge-tts voice; ``DRAWN_TTS_VOICE`` when omitted.
        language: Narration language code.
        upload_enabled: Whether ``run`` should upload.
        now: Timestamp for the project id suffix.
        target_seconds: Desired spoken length, stored for ``run`` trimming.
        minutes: When set, the project id includes ``{minutes}dk``.
        tts_rate: Edge TTS rate; ``DRAWN_TTS_RATE`` when omitted.
        subtitle_font_size: Burn-in size; Drawn default when omitted.
        subtitle_position_ratio: Caption vertical ratio.
        subtitle_color: Burn-in fill colour.
        subtitle_accent: Optional caption accent.
        subtitle_stroke: Outline colour.

    Returns:
        A validated paint-format scenario with Drawn Anyway defaults.
    """
    return build_paint_scenario(
        draft,
        topic=topic,
        project_id=project_id,
        voice=voice or DRAWN_TTS_VOICE,
        language=language,
        upload_enabled=upload_enabled,
        now=now,
        target_seconds=target_seconds,
        minutes=DRAWN_DEFAULT_MINUTES if minutes is None else minutes,
        tts_rate=tts_rate or DRAWN_TTS_RATE,
        category_id=DRAWN_CATEGORY_ID,
        subtitle_font_size=subtitle_font_size or DRAWN_SUBTITLE_FONT_SIZE,
        subtitle_position_ratio=subtitle_position_ratio or DRAWN_SUBTITLE_POSITION_RATIO,
        placeholder_search_terms=DRAWN_PLACEHOLDER_SEARCH_TERMS,
        zoom_opening_end=DRAWN_ZOOM_END,
        zoom_body_end=DRAWN_ZOOM_END,
        brand_id=DRAWN_BRAND_ID,
        subtitle_color=subtitle_color,
        subtitle_accent=None if subtitle_accent is None else subtitle_accent,
        subtitle_stroke=subtitle_stroke,
        numeral_display=True,
    )


def build_pov_scenario(
    draft: DraftScript,
    *,
    topic: str,
    project_id: str | None = None,
    voice: str | None = None,
    language: str = "en",
    upload_enabled: bool = False,
    now: datetime | None = None,
    target_seconds: float | None = None,
    minutes: int | None = None,
    tts_rate: str | None = None,
    subtitle_font_size: int | None = None,
    subtitle_position_ratio: float | None = None,
    subtitle_color: str | None = None,
    subtitle_stroke: str | None = None,
) -> Scenario:
    """Assemble an Every Level POV scenario: rank progression, cartoon beats, no Pexels.

    Same paint render path as Drawn Anyway with POV-specific voice, captions, and brand id.

    Args:
        draft: Rank chapters plus ``visual_beats``.
        topic: Original subject, used in the project id.
        project_id: Explicit id; derived when omitted.
        voice: edge-tts voice; ``POV_TTS_VOICE`` when omitted.
        language: Narration language code.
        upload_enabled: Whether ``run`` should upload.
        now: Timestamp for the project id suffix.
        target_seconds: Desired spoken length, stored for ``run`` trimming.
        minutes: When set, the project id includes ``{minutes}dk``.
        tts_rate: Edge TTS rate; ``POV_TTS_RATE`` when omitted.
        subtitle_font_size: Burn-in size; POV default when omitted.
        subtitle_position_ratio: Caption vertical ratio.
        subtitle_color: Burn-in fill colour.
        subtitle_stroke: Outline colour.

    Returns:
        A validated paint-format scenario with Every Level POV defaults.
    """
    return build_paint_scenario(
        draft,
        topic=topic,
        project_id=project_id,
        voice=voice or POV_TTS_VOICE,
        language=language,
        upload_enabled=upload_enabled,
        now=now,
        target_seconds=target_seconds,
        minutes=POV_DEFAULT_MINUTES if minutes is None else minutes,
        tts_rate=tts_rate or POV_TTS_RATE,
        category_id=POV_CATEGORY_ID,
        subtitle_font_size=subtitle_font_size or POV_SUBTITLE_FONT_SIZE,
        subtitle_position_ratio=subtitle_position_ratio or POV_SUBTITLE_POSITION_RATIO,
        placeholder_search_terms=POV_PLACEHOLDER_SEARCH_TERMS,
        zoom_opening_end=POV_ZOOM_END,
        zoom_body_end=POV_ZOOM_END,
        brand_id=EVERY_LEVEL_POV_BRAND_ID,
        subtitle_color=subtitle_color or POV_SUBTITLE_COLOR,
        subtitle_accent=None,
        subtitle_stroke=subtitle_stroke or POV_SUBTITLE_STROKE,
        numeral_display=True,
    )


def _jsonable(value: Any) -> Any:
    """Convert a dumped scenario into JSON-safe values with portable paths.

    Pydantic's JSON mode renders a ``Path`` in the host platform's native form, which would bake
    Windows backslashes into a file that is meant to be shareable. Paths are emitted in POSIX
    form instead, which ``pathlib`` reads correctly on every platform.

    Args:
        value: Any node of the dumped scenario tree.

    Returns:
        The node with paths and timestamps converted to strings.
    """
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_jsonable(item) for item in value]
    return value


def write_scenario(scenario: Scenario, path: Path) -> Path:
    """Serialise a scenario to disk as UTF-8 JSON.

    Args:
        scenario: The validated scenario.
        path: Destination file.

    Returns:
        The written path.
    """
    return write_json(path, _jsonable(scenario.model_dump(mode="python")))
