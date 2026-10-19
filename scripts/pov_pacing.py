"""Per-episode still hold weights and chapter energy profiles for Rank Run POV."""

from __future__ import annotations

# ``covers`` length drives ``VisualBeat.weight`` in the editor (via plan_weighted_visual).
FLASH = "!"
QUICK = "snap"
MID = "hold beat mid"
LONG = "linger on this frame for tension and breath"
SLOW = "slow lingering hold on this emotional story beat x"

_CHAPTER_WEIGHTS: dict[str, tuple[str, ...]] = {
    "slow": (SLOW, LONG, MID, MID, MID, LONG),
    "mid": (MID, MID, MID, MID, MID, MID),
    "fast": (FLASH, QUICK, QUICK, FLASH, QUICK, QUICK),
    "pulse": (MID, FLASH, MID, FLASH, QUICK, FLASH),
    "climax": (QUICK, QUICK, FLASH, FLASH, QUICK, LONG),
}


def beat_covers(energy: str, beat_index: int) -> str:
    """Return a ``covers`` string for beat ``beat_index`` (1-based) in a chapter."""
    pattern = _CHAPTER_WEIGHTS.get(energy, _CHAPTER_WEIGHTS["mid"])
    return pattern[(beat_index - 1) % len(pattern)]


# One energy label per rank chapter (14 chapters).
EPISODE_CHAPTER_ENERGY: dict[str, tuple[str, ...]] = {
    "football-levels": (
        "slow", "mid", "mid", "mid", "mid", "mid", "mid", "mid",
        "fast", "fast", "climax", "climax", "fast", "slow",
    ),
    "cl-matchday": (
        "mid", "fast", "mid", "mid", "fast", "fast", "climax", "climax",
        "pulse", "fast", "mid", "slow", "climax", "slow",
    ),
    "sunday-premier": (
        "slow", "slow", "mid", "mid", "mid", "fast", "fast", "fast",
        "climax", "climax", "fast", "mid", "slow", "slow",
    ),
    "positions": (
        "mid", "slow", "mid", "fast", "mid", "pulse", "fast", "fast",
        "pulse", "fast", "mid", "mid", "fast", "slow",
    ),
    "transfer-window": (
        "pulse", "fast", "mid", "mid", "mid", "pulse", "slow", "slow",
        "climax", "fast", "mid", "mid", "slow", "slow",
    ),
    "bench-substitute": (
        "slow", "mid", "mid", "fast", "pulse", "mid", "pulse", "mid",
        "fast", "pulse", "mid", "climax", "climax", "slow",
    ),
}
