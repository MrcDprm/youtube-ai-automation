"""Resize and validate Every Level POV YouTube channel assets to exact Studio sizes."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

PROJECT_ROOT = Path(__file__).resolve().parents[1]

BANNER_SIZE = (2560, 1440)
PROFILE_SIZE = (800, 800)
TV_SAFE = (1235, 338)
WIDE_SAFE = (1546, 423)


def _center_box(canvas: tuple[int, int], inner: tuple[int, int]) -> tuple[int, int, int, int]:
    cw, ch = canvas
    iw, ih = inner
    left = (cw - iw) // 2
    top = (ch - ih) // 2
    return left, top, left + iw, top + ih


def compose_banner(source: Path, dest: Path, *, draw_guides: bool = False) -> None:
    """Fit ``source`` to 2560x1440 with center crop; optional safe-zone guides."""
    img = Image.open(source).convert("RGB")
    target_w, target_h = BANNER_SIZE
    scale = max(target_w / img.width, target_h / img.height)
    resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    cropped = resized.crop((left, top, left + target_w, top + target_h))
    if draw_guides:
        draw = ImageDraw.Draw(cropped, "RGBA")
        for box, color in ((TV_SAFE, (255, 59, 48, 80)), (WIDE_SAFE, (255, 200, 0, 50))):
            draw.rectangle(_center_box(BANNER_SIZE, box), outline=color, width=4)
    dest.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(dest, format="PNG", optimize=True)


def compose_profile(source: Path, dest: Path) -> None:
    """Center-crop ``source`` to 800x800 for YouTube profile."""
    img = Image.open(source).convert("RGB")
    side = min(img.width, img.height)
    left = (img.width - side) // 2
    top = (img.height - side) // 2
    square = img.crop((left, top, left + side, top + side))
    dest.parent.mkdir(parents=True, exist_ok=True)
    square.resize(PROFILE_SIZE, Image.Resampling.LANCZOS).save(dest, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kit", type=Path, default=PROJECT_ROOT / "brands" / "every-level-pov-kit.png")
    parser.add_argument("--banner-src", type=Path, default=None)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=PROJECT_ROOT / "brands" / "assets" / "every-level-pov",
    )
    parser.add_argument("--guides", action="store_true", help="Draw safe-zone rectangles on banner.")
    args = parser.parse_args()
    banner_src = args.banner_src or args.kit
    compose_profile(args.kit, args.out_dir / "profile-800.png")
    compose_banner(banner_src, args.out_dir / "banner-2560x1440.png", draw_guides=args.guides)
    print("profile", args.out_dir / "profile-800.png")
    print("banner", args.out_dir / "banner-2560x1440.png")


if __name__ == "__main__":
    main()
