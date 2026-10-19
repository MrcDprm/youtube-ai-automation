"""Regenerate JPEG thumbnails for episodes that received the rain cover by mistake."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path(
    r"C:\Users\mirac\.cursor\projects\c-Users-mirac-Desktop-youtube-automation\assets"
)
STORYBOARD = PROJECT_ROOT / "output" / "storyboard"
THUMBS = PROJECT_ROOT / "output" / "thumbnails"
RAIN_PNG_BYTES = 1_337_936

# Storyboards confirmed to hold a copied rain PNG (1337936 bytes).
AFFECTED: tuple[str, ...] = (
    "why-a-booklet-lets-you-cross-a-line-11dk-20260901",
    "why-a-cup-holder-beat-horsepower-11dk-20260901",
    "why-a-number-plate-is-a-tax-receipt-11dk-20260829",
    "why-north-won-the-map-11dk-20260829",
    "why-nothing-became-a-number-11dk-20260829",
    "why-you-stab-dinner-with-a-fork-11dk-20260901",
    "why-you-wear-a-strap-to-sit-still-11dk-20260831",
    "why-your-bumper-became-a-costume-11dk-20260901",
    "your-life-from-sunday-league-to-the-premier-l-14dk-20260902",
)

SCENARIO_GLOBS = ("senaryo-paint*.json", "senaryo-pov*.json", "senaryo-pov.json")


def _hook_for(project_id: str) -> str:
    for pattern in SCENARIO_GLOBS:
        for path in PROJECT_ROOT.glob(pattern):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if data.get("project_id") == project_id:
                return str(data.get("youtube", {}).get("thumbnail_hook") or "").strip()
    slug = project_id.rsplit("-", 2)[0]
    raise SystemExit(f"no thumbnail_hook found for {project_id} (slug {slug})")


def repair(project_id: str, source: Path) -> Path:
    from modules.studio_pack import prepare_youtube_thumbnail

    board = STORYBOARD / project_id
    board.mkdir(parents=True, exist_ok=True)
    dest_png = board / "thumbnail.png"
    if source.resolve() != dest_png.resolve():
        dest_png.write_bytes(source.read_bytes())

    out_jpg = THUMBS / f"{project_id}.jpg"
    THUMBS.mkdir(parents=True, exist_ok=True)
    prepare_youtube_thumbnail(dest_png, out_jpg)
    return out_jpg


def main() -> None:
    from modules.studio_pack import resolve_episode_thumbnail_source

    targets = sys.argv[1:] or list(AFFECTED)
    for project_id in targets:
        hook = _hook_for(project_id)
        src = resolve_episode_thumbnail_source(
            project_id,
            assets_dir=ASSETS,
            prefer_assets=True,
        )
        if src is None:
            print(f"SKIP {project_id}: no asset thumbnail (hook {hook!r})")
            continue
        if project_id != "why-rain-needed-a-rubber-arm-11dk-20260829" and src.stat().st_size == RAIN_PNG_BYTES:
            print(f"SKIP {project_id}: resolved asset is still rain PNG — generate thumbnail-{project_id}.png")
            continue
        out = repair(project_id, src)
        print(f"OK {project_id} hook={hook!r} src={src.name} -> {out.name} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
