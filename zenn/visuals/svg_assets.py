"""Write bundled SVG pose and background assets (black / white / yellow)."""

from __future__ import annotations

from pathlib import Path

from zenn import PACKAGE_ROOT

ASSETS_DIR = PACKAGE_ROOT / "visuals" / "assets"
POSE_DIR = ASSETS_DIR / "poses"
BG_DIR = ASSETS_DIR / "backgrounds"

_SVG_HEAD = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 560" fill="none">\n'
    '  <rect width="320" height="560" fill="#000000"/>\n'
)

_POSE_BODIES: dict[str, str] = {
    "standing": (
        '  <circle cx="160" cy="70" r="28" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="98" x2="160" y2="280" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="110" y2="200" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="210" y2="200" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="130" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="190" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
    ),
    "running": (
        '  <circle cx="160" cy="70" r="28" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="98" x2="160" y2="280" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="105" y2="105" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="205" y2="165" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="225" y2="355" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="115" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
    ),
    "scared": (
        '  <circle cx="160" cy="70" r="28" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <circle cx="145" cy="65" r="6" fill="#FFD600"/><circle cx="175" cy="65" r="6" fill="#FFD600"/>\n'
        '  <path d="M145 88 Q160 98 175 88" stroke="#FFD600" stroke-width="4"/>\n'
        '  <line x1="160" y1="98" x2="160" y2="280" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="125" y2="85" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="195" y2="85" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="140" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="180" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
    ),
    "shocked": (
        '  <circle cx="160" cy="70" r="28" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <circle cx="145" cy="65" r="9" stroke="#FFD600" stroke-width="4"/>\n'
        '  <circle cx="175" cy="65" r="9" stroke="#FFD600" stroke-width="4"/>\n'
        '  <ellipse cx="160" cy="92" rx="10" ry="14" fill="#FFD600"/>\n'
        '  <line x1="160" y1="98" x2="160" y2="280" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="110" y2="130" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="210" y2="130" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="138" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="182" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
    ),
    "thinking": (
        '  <circle cx="160" cy="70" r="28" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="98" x2="160" y2="280" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="115" y2="155" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="195" y2="85" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <ellipse cx="215" cy="55" rx="22" ry="18" stroke="#FFD600" stroke-width="4"/>\n'
        '  <line x1="160" y1="280" x2="140" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="180" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
    ),
    "pointing": (
        '  <circle cx="160" cy="70" r="28" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="98" x2="160" y2="280" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="120" y2="165" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="235" y2="125" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <circle cx="240" cy="120" r="8" fill="#FFD600"/>\n'
        '  <line x1="160" y1="280" x2="140" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="180" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
    ),
    "sitting": (
        '  <circle cx="160" cy="70" r="28" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="98" x2="160" y2="250" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="120" y2="150" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="200" y2="150" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="105" y1="345" x2="215" y2="345" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="250" x2="115" y2="375" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="250" x2="205" y2="375" stroke="#FFFFFF" stroke-width="6"/>\n'
    ),
    "driving": (
        '  <circle cx="160" cy="70" r="28" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="98" x2="160" y2="280" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <path d="M190 170 A45 45 0 0 1 230 220" stroke="#FFD600" stroke-width="7"/>\n'
        '  <line x1="160" y1="140" x2="185" y2="190" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="215" y2="205" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="135" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="185" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
    ),
    "working": (
        '  <circle cx="160" cy="70" r="28" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="98" x2="160" y2="280" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="215" y2="175" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="215" y1="175" x2="250" y2="210" stroke="#FFD600" stroke-width="7"/>\n'
        '  <circle cx="245" cy="215" r="12" stroke="#FFD600" stroke-width="4"/>\n'
        '  <line x1="160" y1="140" x2="115" y2="160" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="140" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="180" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
    ),
    "reading": (
        '  <circle cx="160" cy="70" r="28" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <rect x="125" y="140" width="70" height="50" stroke="#FFD600" stroke-width="5"/>\n'
        '  <line x1="160" y1="140" x2="160" y2="190" stroke="#FFD600" stroke-width="3"/>\n'
        '  <line x1="160" y1="98" x2="160" y2="280" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="120" y2="160" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="200" y2="160" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="140" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="180" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
    ),
    "waiting": (
        '  <circle cx="160" cy="70" r="28" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="98" x2="160" y2="280" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="130" y2="175" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="140" x2="190" y2="175" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <path d="M215 60 A25 25 0 0 1 240 95" stroke="#FFD600" stroke-width="5"/>\n'
        '  <line x1="160" y1="280" x2="142" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="160" y1="280" x2="178" y2="380" stroke="#FFFFFF" stroke-width="6"/>\n'
    ),
    "falling": (
        '  <circle cx="190" cy="120" r="28" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="190" y1="148" x2="150" y2="230" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="170" y1="170" x2="240" y2="140" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="170" y1="170" x2="110" y2="210" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="150" y1="230" x2="200" y2="320" stroke="#FFFFFF" stroke-width="6"/>\n'
        '  <line x1="150" y1="230" x2="70" y2="300" stroke="#FFFFFF" stroke-width="6"/>\n'
    ),
}

_BG_BODIES: dict[str, str] = {
    "garage": (
        '  <rect y="460" width="320" height="100" fill="#111111" stroke="#FFFFFF" stroke-width="3"/>\n'
        '  <rect x="95" y="200" width="130" height="260" stroke="#FFFFFF" stroke-width="4"/>\n'
        '  <rect x="40" y="400" width="70" height="35" rx="8" stroke="#FFD600" stroke-width="4"/>\n'
    ),
    "road": (
        '  <rect y="460" width="320" height="100" fill="#151515"/>\n'
        '  <line x1="0" y1="460" x2="320" y2="460" stroke="#FFFFFF" stroke-width="4"/>\n'
        '  <rect x="20" y="280" width="50" height="8" fill="#FFD600"/>\n'
        '  <rect x="120" y="280" width="50" height="8" fill="#FFD600"/>\n'
        '  <rect x="220" y="280" width="50" height="8" fill="#FFD600"/>\n'
    ),
    "factory": (
        '  <rect y="460" width="320" height="100" fill="#101010"/>\n'
        '  <rect x="30" y="300" width="70" height="160" stroke="#FFFFFF" stroke-width="4"/>\n'
        '  <rect x="125" y="260" width="70" height="200" stroke="#FFFFFF" stroke-width="4"/>\n'
        '  <rect x="220" y="320" width="70" height="140" stroke="#FFFFFF" stroke-width="4"/>\n'
        '  <rect x="145" y="220" width="20" height="40" fill="#FFFFFF"/>\n'
        '  <circle cx="155" cy="210" r="14" stroke="#FFD600" stroke-width="3"/>\n'
    ),
    "office": (
        '  <rect y="460" width="320" height="100" fill="#121212"/>\n'
        '  <rect x="70" y="380" width="180" height="80" stroke="#FFFFFF" stroke-width="4"/>\n'
        '  <rect x="90" y="300" width="140" height="80" stroke="#FFD600" stroke-width="3"/>\n'
        '  <rect x="25" y="80" width="60" height="70" stroke="#FFFFFF" stroke-width="3"/>\n'
    ),
    "old_city": (
        '  <rect y="460" width="320" height="100" fill="#0d0d0d"/>\n'
        '  <rect x="20" y="350" width="50" height="110" stroke="#FFFFFF" stroke-width="3"/>\n'
        '  <rect x="85" y="310" width="45" height="150" stroke="#FFFFFF" stroke-width="3"/>\n'
        '  <rect x="150" y="330" width="55" height="130" stroke="#FFFFFF" stroke-width="3"/>\n'
        '  <rect x="220" y="360" width="40" height="100" stroke="#FFFFFF" stroke-width="3"/>\n'
        '  <rect x="165" y="350" width="20" height="20" fill="#FFD600"/>\n'
        '  <line x1="0" y1="100" x2="320" y2="100" stroke="#FFFFFF" stroke-width="2"/>\n'
    ),
    "cave": (
        '  <path d="M0 460 L0 280 Q160 180 320 280 L320 460 Z" stroke="#FFFFFF" stroke-width="4"/>\n'
        '  <ellipse cx="240" cy="410" rx="28" ry="22" fill="#FFD600" stroke="#FFFFFF" stroke-width="2"/>\n'
        '  <polygon points="240,360 228,400 252,400" fill="#FFD600"/>\n'
    ),
}


def write_svg_assets() -> list[Path]:
    """Write all pose and background SVG files; return written paths."""
    written: list[Path] = []
    POSE_DIR.mkdir(parents=True, exist_ok=True)
    BG_DIR.mkdir(parents=True, exist_ok=True)
    for tag, body in _POSE_BODIES.items():
        path = POSE_DIR / f"{tag}.svg"
        path.write_text(_SVG_HEAD + body + "</svg>\n", encoding="utf-8")
        written.append(path)
    for tag, body in _BG_BODIES.items():
        path = BG_DIR / f"{tag}.svg"
        path.write_text(_SVG_HEAD + body + "</svg>\n", encoding="utf-8")
        written.append(path)
    return written


if __name__ == "__main__":
    paths = write_svg_assets()
    print(f"Wrote {len(paths)} SVG asset(s) under {ASSETS_DIR}")
