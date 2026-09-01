"""Six Zenn backgrounds plus road fallback — high-contrast black / white / yellow."""

from __future__ import annotations

from PIL import ImageDraw

from zenn.visuals.palette import Palette

BACKGROUND_TAGS: tuple[str, ...] = (
    "garage",
    "road",
    "factory",
    "office",
    "old_city",
    "cave",
    "night",
)

_VISIBLE_BGS: frozenset[str] = frozenset({"garage", "road", "factory", "office", "old_city", "cave", "night"})

__all__ = ["BACKGROUND_TAGS", "draw_background", "normalize_bg"]


def normalize_bg(tag: str) -> str:
    """Map blank or unknown tags to a visible background."""
    cleaned = (tag or "").strip().lower()
    if cleaned in _VISIBLE_BGS:
        return cleaned
    return "road"


def draw_background(
    draw: ImageDraw.ImageDraw,
    tag: str,
    width: int,
    height: int,
    palette: Palette,
) -> None:
    """Paint a readable background scene behind the stick figure."""
    tag = normalize_bg(tag)
    line = palette.line
    accent = palette.accent
    floor_y = int(height * 0.78)
    horizon = int(height * 0.52)

    if tag == "garage":
        draw.rectangle((0, 0, width, floor_y), fill="#1e2433")
        draw.rectangle((0, floor_y, width, height), fill="#3a3a3a", outline=line, width=4)
        door_w = int(width * 0.42)
        door_x = (width - door_w) // 2
        door_top = int(height * 0.28)
        draw.rectangle((door_x, door_top, door_x + door_w, floor_y), fill="#2b2b2b", outline=accent, width=6)
        for stripe in range(5):
            y = door_top + stripe * int((floor_y - door_top) / 5)
            draw.line((door_x + 12, y, door_x + door_w - 12, y), fill=line, width=3)
        car_w = int(width * 0.26)
        car_x = int(width * 0.08)
        draw.rounded_rectangle(
            (car_x, floor_y - int(height * 0.11), car_x + car_w, floor_y - int(height * 0.02)),
            radius=12,
            outline=accent,
            width=5,
        )
        draw.ellipse((car_x + 10, floor_y - 18, car_x + 34, floor_y + 4), outline=line, width=4)
        draw.ellipse((car_x + car_w - 34, floor_y - 18, car_x + car_w - 10, floor_y + 4), outline=line, width=4)

    elif tag == "road":
        draw.rectangle((0, 0, width, horizon), fill="#243047")
        draw.rectangle((0, horizon, width, floor_y), fill="#4a4a4a")
        draw.rectangle((0, floor_y, width, height), fill="#2f2f2f", outline=line, width=4)
        for x in range(-30, width + 60, 140):
            draw.rectangle((x, int(height * 0.56), x + 70, int(height * 0.56) + 10), fill=accent)
        draw.line((0, floor_y, width, floor_y), fill=line, width=5)

    elif tag == "factory":
        draw.rectangle((0, 0, width, floor_y), fill="#1a1f28")
        draw.rectangle((0, floor_y, width, height), fill="#333333", outline=line, width=4)
        base_x = int(width * 0.06)
        for index in range(3):
            bx = base_x + index * int(width * 0.3)
            bw = int(width * 0.2)
            bh = int(height * 0.38)
            draw.rectangle((bx, floor_y - bh, bx + bw, floor_y), fill="#252525", outline=line, width=5)
            for win_y in range(floor_y - bh + 30, floor_y - 40, 55):
                draw.rectangle((bx + 16, win_y, bx + bw - 16, win_y + 28), fill=accent)
            stack_x = bx + bw // 3
            draw.rectangle((stack_x, floor_y - bh - int(height * 0.14), stack_x + 24, floor_y - bh), fill=line)
            draw.ellipse(
                (stack_x - 14, floor_y - bh - int(height * 0.18), stack_x + 38, floor_y - bh - 10),
                outline=accent,
                width=3,
            )

    elif tag == "office":
        draw.rectangle((0, 0, width, floor_y), fill="#222831")
        draw.rectangle((0, floor_y, width, height), fill="#3d3d3d", outline=line, width=4)
        win_x = int(width * 0.06)
        draw.rectangle((win_x, int(height * 0.1), win_x + int(width * 0.22), int(height * 0.34)), outline=accent, width=5)
        draw.line(
            (win_x + int(width * 0.11), int(height * 0.1), win_x + int(width * 0.11), int(height * 0.34)),
            fill=accent,
            width=3,
        )
        desk_w = int(width * 0.58)
        desk_x = (width - desk_w) // 2
        draw.rectangle((desk_x, floor_y - int(height * 0.07), desk_x + desk_w, floor_y), outline=line, width=5)
        draw.rectangle(
            (desk_x + 50, floor_y - int(height * 0.24), desk_x + desk_w - 50, floor_y - int(height * 0.07)),
            outline=accent,
            width=4,
        )

    elif tag == "old_city":
        draw.rectangle((0, 0, width, int(height * 0.2)), fill="#1a2744")
        draw.rectangle((0, int(height * 0.2), width, floor_y), fill="#2a3548")
        draw.rectangle((0, floor_y, width, height), fill="#353535", outline=line, width=4)
        x = int(width * 0.04)
        while x < width - 40:
            bw = int(width * 0.07) + (x % 4) * 18
            bh = int(height * 0.18) + (x % 6) * 22
            draw.rectangle((x, floor_y - bh, x + bw, floor_y), fill="#1f1f1f", outline=line, width=3)
            draw.rectangle((x + 10, floor_y - bh + 24, x + bw - 10, floor_y - bh + 48), fill=accent)
            x += bw + 14

    elif tag == "cave":
        draw.rectangle((0, 0, width, floor_y), fill="#0f0f12")
        arch_top = int(height * 0.18)
        draw.polygon(
            [
                (0, floor_y),
                (0, arch_top + 90),
                (width // 2, arch_top),
                (width, arch_top + 90),
                (width, floor_y),
            ],
            fill="#1a1a1a",
            outline=line,
        )
        draw.line([(0, arch_top + 90), (width, arch_top + 90)], fill=line, width=4)
        fire_x = int(width * 0.68)
        fire_y = floor_y - 24
        draw.ellipse((fire_x - 36, fire_y - 58, fire_x + 36, fire_y + 12), fill=accent, outline=line, width=3)
        for flicker in (-22, 0, 22):
            draw.polygon(
                [
                    (fire_x + flicker, fire_y - 82),
                    (fire_x + flicker - 16, fire_y - 22),
                    (fire_x + flicker + 16, fire_y - 22),
                ],
                fill=accent,
            )

    elif tag == "night":
        draw.rectangle((0, 0, width, floor_y), fill="#0a0e18")
        for sx, sy, sr in ((120, 80, 3), (340, 140, 2), (560, 60, 3), (780, 110, 2), (980, 90, 3), (1500, 130, 2)):
            if sx < width:
                draw.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=line)
        moon_x = int(width * 0.82)
        draw.ellipse((moon_x - 40, 70, moon_x + 40, 150), fill=accent, outline=line, width=3)
        draw.rectangle((0, floor_y, width, height), fill="#1c1c1c", outline=line, width=4)

    else:
        draw_background(draw, "road", width, height, palette)
