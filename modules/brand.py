"""Active YouTube brand profile (Badly Drawn Why, After Hours File, Drawn Anyway, Every Level POV)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from config.constants import (
    BRAND_BADLY_DRAWN_WHY,
    DRAWN_BRAND_ID,
    DRAWN_CATEGORY_ID,
    DRAWN_CHANNEL_NAME,
    DRAWN_PLAYLIST,
    DRAWN_TTS_VOICE,
    EVERY_LEVEL_POV_BRAND_ID,
    FILE_BRAND_ID,
    FILE_CATEGORY_ID,
    FILE_CHANNEL_NAME,
    FILE_PLAYLIST,
    FILE_TTS_VOICE,
    PAINT_CHANNEL_NAME,
    POV_CHANNEL_NAME,
    POV_PLAYLIST,
    PROJECT_ROOT,
    YOUTUBE_CATEGORY_LABELS,
)
from models.scenario import Scenario

__all__ = [
    "BrandProfile",
    "brand_for_scenario",
    "load_active_brand",
    "load_active_brand_id",
]


@dataclass(frozen=True, slots=True)
class BrandProfile:
    """How Studio copy and agent dispatch differ per channel.

    Attributes:
        id: Value stored in ``brands/active.json``.
        channel_name: Line written at the top of ``STUDIO.txt``.
        category_id: YouTube category as a digit string.
        default_playlist: Studio playlist checklist line.
        illustration_line: Synthetic-content sentence in Studio and the description footer.
        thumbnail_hook_heading: Label above the hook in ``STUDIO.txt``.
        uses_paint_playlists: When true, title/tag needles pick a Badly Drawn Why list.
        description_art_line: Footer sentence above the TTS disclosure.
    """

    id: str
    channel_name: str
    category_id: str
    default_playlist: str
    illustration_line: str
    thumbnail_hook_heading: str
    uses_paint_playlists: bool
    description_art_line: str

    @property
    def category_label(self) -> str:
        """Human Studio checklist label such as ``Education (27)``."""
        return YOUTUBE_CATEGORY_LABELS.get(
            self.category_id, f"Category ({self.category_id})"
        )


BADLY_DRAWN_WHY: BrandProfile = BrandProfile(
    id=BRAND_BADLY_DRAWN_WHY,
    channel_name=PAINT_CHANNEL_NAME,
    category_id="27",
    default_playlist="Everyday Weird",
    illustration_line="stick-figure illustrations + TTS",
    thumbnail_hook_heading="Thumbnail hook (yellow 2-4 words)",
    uses_paint_playlists=True,
    description_art_line="Illustrations: original stick-figure art. Narration: synthesized.",
)

AFTER_HOURS_FILE: BrandProfile = BrandProfile(
    id=FILE_BRAND_ID,
    channel_name=FILE_CHANNEL_NAME,
    category_id=FILE_CATEGORY_ID,
    default_playlist=FILE_PLAYLIST,
    illustration_line="illustrated stills + TTS",
    thumbnail_hook_heading="Thumbnail hook (dark 3-5 words, not yellow)",
    uses_paint_playlists=False,
    description_art_line="Illustrations: original still art. Narration: synthesized.",
)

DRAWN_ANYWAY: BrandProfile = BrandProfile(
    id=DRAWN_BRAND_ID,
    channel_name=DRAWN_CHANNEL_NAME,
    category_id=DRAWN_CATEGORY_ID,
    default_playlist=DRAWN_PLAYLIST,
    illustration_line="cartoon animation + TTS",
    thumbnail_hook_heading="Thumbnail hook (bold 3-4 words, cartoon)",
    uses_paint_playlists=False,
    description_art_line="Cartoons: original character animation. Narration: synthesized.",
)

EVERY_LEVEL_POV: BrandProfile = BrandProfile(
    id=EVERY_LEVEL_POV_BRAND_ID,
    channel_name=POV_CHANNEL_NAME,
    category_id="24",
    default_playlist=POV_PLAYLIST,
    illustration_line="cartoon POV illustrations + TTS",
    thumbnail_hook_heading="Thumbnail hook (red 3-4 words, POV character)",
    uses_paint_playlists=False,
    description_art_line="Illustrations: original cartoon POV art. Narration: synthesized.",
)

_BRANDS: dict[str, BrandProfile] = {
    BADLY_DRAWN_WHY.id: BADLY_DRAWN_WHY,
    AFTER_HOURS_FILE.id: AFTER_HOURS_FILE,
    DRAWN_ANYWAY.id: DRAWN_ANYWAY,
    EVERY_LEVEL_POV.id: EVERY_LEVEL_POV,
}


def load_active_brand_id(root: Path | None = None) -> str:
    """Return the brand id from ``brands/active.json``, defaulting to Badly Drawn Why.

    Args:
        root: Repository root. ``PROJECT_ROOT`` when omitted.

    Returns:
        A known brand id.
    """
    path = (root or PROJECT_ROOT) / "brands" / "active.json"
    if not path.is_file():
        return BRAND_BADLY_DRAWN_WHY
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return BRAND_BADLY_DRAWN_WHY
    if not isinstance(payload, dict):
        return BRAND_BADLY_DRAWN_WHY
    brand_id = str(payload.get("id") or "").strip()
    if brand_id in _BRANDS:
        return brand_id
    return BRAND_BADLY_DRAWN_WHY


def load_active_brand(root: Path | None = None) -> BrandProfile:
    """Return the active :class:`BrandProfile`.

    Args:
        root: Repository root. ``PROJECT_ROOT`` when omitted.

    Returns:
        The matching profile, or Badly Drawn Why when the file is missing or unknown.
    """
    return _BRANDS[load_active_brand_id(root)]


def brand_for_scenario(scenario: Scenario) -> BrandProfile:
    """Pick a profile from the scenario so Studio copy does not depend on disk state.

    ``youtube.brand_id`` wins when set, so Drawn Anyway can change Edge voice
    without Studio flipping to After Hours File (both use category ``24``).
    Legacy files without ``brand_id`` still match on WilliamNeural or RyanNeural.

    Args:
        scenario: The assembled project.

    Returns:
        The matching :class:`BrandProfile`.
    """
    stamped = (scenario.youtube.brand_id or "").strip()
    if stamped in _BRANDS:
        return _BRANDS[stamped]
    if scenario.tts.voice == DRAWN_TTS_VOICE:
        return DRAWN_ANYWAY
    if scenario.tts.voice == FILE_TTS_VOICE:
        return AFTER_HOURS_FILE
    if scenario.youtube.category_id == FILE_CATEGORY_ID:
        return AFTER_HOURS_FILE
    return BADLY_DRAWN_WHY
