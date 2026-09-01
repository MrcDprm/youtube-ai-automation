"""Write a YouTube Studio copy-paste pack so the human only uploads."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

from config.constants import (
    PAINT_PLAYLISTS,
    SYNTHETIC_DISCLOSURE_TEXT,
    THUMBNAIL_MIN_JPEG_QUALITY,
    THUMBNAIL_SIZE,
    YOUTUBE_DESCRIPTION_MAX_CHARS,
    YOUTUBE_THUMBNAIL_MAX_BYTES,
)
from models.scenario import Scenario, Scene
from modules.brand import BrandProfile, brand_for_scenario
from utils.exceptions import RenderError
from utils.fs import ensure_parent

__all__ = [
    "chapter_markers",
    "format_chapter_time",
    "prepare_youtube_thumbnail",
    "suggest_playlist",
    "write_studio_pack",
]


def format_chapter_time(seconds: float) -> str:
    """Format a timestamp the way YouTube chapters expect it."""
    total = max(0, int(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def chapter_title(narration: str, *, limit: int = 42) -> str:
    """Take the first sentence of a chapter, trimmed for the description."""
    text = " ".join(narration.split())
    for separator in (". ", "! ", "? "):
        if separator in text:
            text = text.split(separator, 1)[0]
            break
    if len(text) > limit:
        clipped = text[: limit - 1].rsplit(" ", 1)[0]
        text = (clipped or text[: limit - 1]) + "…"
    return text or "Chapter"


def chapter_markers(
    scenes: list[Scene],
    durations: list[float],
    *,
    gap: float = 0.3,
) -> list[tuple[str, str]]:
    """Build ``(timestamp, title)`` pairs from measured chapter audio.

    Args:
        scenes: Scenes in playback order.
        durations: Matching TTS durations in seconds.
        gap: Silence appended after each chapter.

    Returns:
        Markers whose first timestamp is always ``0:00``.
    """
    if len(scenes) != len(durations):
        raise ValueError("scenes and durations must be the same length")
    markers: list[tuple[str, str]] = []
    cursor = 0.0
    for index, (scene, duration) in enumerate(zip(scenes, durations, strict=True)):
        stamp = "0:00" if index == 0 else format_chapter_time(cursor)
        markers.append((stamp, chapter_title(scene.narration)))
        cursor += duration + gap
    return markers


def suggest_playlist(
    title: str,
    tags: list[str],
    *,
    brand: BrandProfile | None = None,
) -> str:
    """Pick a Studio playlist from title/tag words, or the brand's single list.

    Args:
        title: YouTube title.
        tags: YouTube tags.
        brand: When ``uses_paint_playlists`` is false, return that brand's default list.

    Returns:
        A playlist display name.
    """
    if brand is not None and not brand.uses_paint_playlists:
        return brand.default_playlist
    tokens = set(re.findall(r"[a-z0-9]+", f"{title} {' '.join(tags)}".lower()))
    mapping = (
        (("night", "sleep", "dark", "fire", "light", "sunset"), PAINT_PLAYLISTS[0]),
        (("body", "blood", "brain", "mosquito", "pain", "surgery"), PAINT_PLAYLISTS[1]),
        (("mind", "stupid", "memory", "dream", "peak", "age"), PAINT_PLAYLISTS[2]),
        (
            (
                "tech",
                "wheel",
                "machine",
                "electric",
                "edison",
                "tool",
                "car",
                "gas",
                "bumper",
                "gasoline",
                "wiper",
                "steering",
                "tire",
                "horsepower",
                "map",
                "passport",
            ),
            PAINT_PLAYLISTS[3],
        ),
    )
    for needles, playlist in mapping:
        if tokens.intersection(needles):
            return playlist
    return PAINT_PLAYLISTS[4]


def prepare_youtube_thumbnail(source: Path, out_path: Path) -> Path:
    """Fit an agent-drawn cover to YouTube's 1280x720 JPEG ceiling.

    Args:
        source: PNG or JPEG from the image agent.
        out_path: Destination ``.jpg``.

    Returns:
        ``out_path``.

    Raises:
        RenderError: If the image cannot be read or squeezed under 2 MB.
    """
    try:
        frame = Image.open(source).convert("RGB")
    except OSError as exc:
        raise RenderError(f"Could not read paint thumbnail {source}: {exc}") from exc

    canvas = _cover(frame, THUMBNAIL_SIZE)
    ensure_parent(out_path)
    quality = 90
    while quality >= THUMBNAIL_MIN_JPEG_QUALITY:
        try:
            canvas.save(out_path, format="JPEG", quality=quality, optimize=True, progressive=True)
        except OSError as exc:
            raise RenderError(f"Could not write thumbnail {out_path}: {exc}") from exc
        if out_path.stat().st_size <= YOUTUBE_THUMBNAIL_MAX_BYTES:
            return out_path
        quality -= 10
    raise RenderError(
        f"Paint thumbnail stayed above {YOUTUBE_THUMBNAIL_MAX_BYTES} bytes.",
        hint="Simplify the cover drawing and try again.",
    )


def find_paint_thumbnail(search_roots: list[Path]) -> Path | None:
    """Return the first ``thumbnail.png`` / ``cover.png`` in the storyboard folders."""
    names = ("thumbnail.png", "thumbnail.jpg", "cover.png", "cover.jpg", "00-thumbnail.png")
    for root in search_roots:
        if not root.is_dir():
            continue
        for name in names:
            candidate = root / name
            if candidate.is_file():
                return candidate
    return None


def write_studio_pack(
    scenario: Scenario,
    *,
    video_path: Path,
    thumbnail_path: Path | None,
    srt_path: Path | None,
    durations: list[float],
    out_dir: Path,
) -> Path:
    """Write ``STUDIO.txt`` for a finished paint (or longform) render.

    Args:
        scenario: The project metadata.
        video_path: Finished MP4.
        thumbnail_path: Optional JPEG cover.
        srt_path: Optional captions file.
        durations: Per-scene TTS lengths matching the kept scenes.
        out_dir: ``output/studio/{project_id}``.

    Returns:
        Path to ``STUDIO.txt``.
    """
    scenes = list(scenario.scenes)
    if len(durations) != len(scenes):
        scenes = scenes[: len(durations)]
    markers = chapter_markers(scenes, durations, gap=scenario.video.scene_gap_seconds)
    brand = brand_for_scenario(scenario)
    playlist = suggest_playlist(
        scenario.youtube.title, list(scenario.youtube.tags), brand=brand
    )
    hook = scenario.youtube.thumbnail_hook.strip()
    description = _build_description(scenario, markers, brand=brand)

    lines = [
        f"Channel: {brand.channel_name}",
        "",
        "=== Upload these files ===",
        f"Video: {video_path}",
        f"Thumbnail: {thumbnail_path or '(none — YouTube will auto-generate)'}",
        f"Captions: {srt_path or '(none)'}",
        "",
        "=== Title ===",
        scenario.youtube.title,
        "",
        "=== Description ===",
        description,
        "",
        "=== Tags ===",
        ", ".join(scenario.youtube.tags),
        "",
        f"=== {brand.thumbnail_hook_heading} ===",
        hook or "(not set — invent a short hook that is NOT the title)",
        "",
        "=== YouTube Studio checklist ===",
        f"Playlist: {playlist}",
        f"Category: {brand.category_label}",
        f"Language: {scenario.youtube.default_language}",
        "Audience: No, not made for kids",
        f"Altered / synthetic content: Yes ({brand.illustration_line})",
        "Visibility: Schedule in Studio for your daily publish time.",
        "Unlisted first only if you want a listing check before the timer.",
        "End screen / cards: add after upload (API cannot set these)",
        "Do not upload via this repo; paste the fields above in Studio.",
    ]
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "STUDIO.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _build_description(
    scenario: Scenario,
    markers: list[tuple[str, str]],
    *,
    brand: BrandProfile,
) -> str:
    """Compose a Studio description with chapters, under YouTube's character cap."""
    body = scenario.youtube.description.strip()
    chapter_block = "Chapters:\n" + "\n".join(f"{stamp} {title}" for stamp, title in markers)
    art_line = brand.description_art_line
    footer = f"{art_line}\n{SYNTHETIC_DISCLOSURE_TEXT}"
    parts = [body, "", chapter_block, "", footer]
    text = "\n".join(parts).strip()
    if len(text) <= YOUTUBE_DESCRIPTION_MAX_CHARS:
        return text
    overflow = len(text) - YOUTUBE_DESCRIPTION_MAX_CHARS
    trimmed = body[: max(0, len(body) - overflow - 1)].rstrip() + "…"
    return "\n".join([trimmed, "", chapter_block, "", footer]).strip()


def _cover(frame: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Scale and centre-crop to ``size``."""
    target_width, target_height = size
    source_width, source_height = frame.size
    scale = max(target_width / source_width, target_height / source_height)
    scaled = (
        max(target_width, int(round(source_width * scale))),
        max(target_height, int(round(source_height * scale))),
    )
    resized = frame.resize(scaled, Image.Resampling.LANCZOS)
    left = (scaled[0] - target_width) // 2
    top = (scaled[1] - target_height) // 2
    return resized.crop((left, top, left + target_width, top + target_height))
