"""Shared fixtures.

The autouse ``isolated_environment`` fixture strips real credentials from the environment and
redirects every output and cache path into a temporary directory, so the suite can never touch
a developer's real keys, caches or rendered videos.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from config.settings import Settings, get_settings

FIXTURES_DIR = Path(__file__).parent / "fixtures"

SECRET_ENV_KEYS = (
    "PEXELS_API_KEY",
    "PIXABAY_API_KEY",
    "YOUTUBE_CLIENT_SECRETS_FILE",
    "YOUTUBE_TOKEN_FILE",
    "LOG_LEVEL",
    "OUTPUT_DIR",
    "CACHE_DIR",
    "HTTP_TIMEOUT",
    "MAX_RETRIES",
    "FFMPEG_THREADS",
    "DEFAULT_FONT",
)


@pytest.fixture(autouse=True)
def isolated_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Remove real credentials and redirect all paths into ``tmp_path``.

    Args:
        tmp_path: pytest's per-test temporary directory.
        monkeypatch: pytest's environment patcher.

    Yields:
        ``None``. The environment is restored automatically afterwards.
    """
    for key in SECRET_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)

    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path / "output"))
    monkeypatch.setenv("CACHE_DIR", str(tmp_path / "cache"))
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def settings(isolated_environment: None) -> Settings:
    """Return settings bound to the isolated temporary directories.

    Args:
        isolated_environment: Ensures the environment is patched first.

    Returns:
        A fresh :class:`~config.settings.Settings`.
    """
    loaded = get_settings()
    loaded.ensure_directories()
    return loaded


@pytest.fixture
def fonts_dir(tmp_path: Path) -> Path:
    """Create a directory holding one real, loadable TrueType font.

    Several validators and the thumbnail builder need a font that Pillow can actually parse,
    so a synthetic file will not do. The project's own downloaded font is reused when present,
    and otherwise a system font is copied in.

    Args:
        tmp_path: pytest's per-test temporary directory.

    Returns:
        A directory containing at least one usable font.
    """
    target = tmp_path / "fonts"
    target.mkdir(parents=True, exist_ok=True)

    from utils.fs import default_fonts_dir, resolve_font

    source, _ = resolve_font(default_fonts_dir() / "Inter-Bold.ttf")
    (target / source.name).write_bytes(source.read_bytes())
    return target


@pytest.fixture
def valid_scenario_dict() -> dict[str, Any]:
    """Load the valid scenario fixture as a plain dictionary.

    Returns:
        The decoded fixture.
    """
    return json.loads((FIXTURES_DIR / "senaryo_valid.json").read_text(encoding="utf-8"))


@pytest.fixture
def invalid_scenario_path() -> Path:
    """Return the path to the deliberately broken scenario fixture.

    Returns:
        The fixture path.
    """
    return FIXTURES_DIR / "senaryo_invalid.json"


@pytest.fixture
def valid_scenario_path() -> Path:
    """Return the path to the valid scenario fixture.

    Returns:
        The fixture path.
    """
    return FIXTURES_DIR / "senaryo_valid.json"


@pytest.fixture
def pexels_response() -> dict[str, Any]:
    """Load the recorded Pexels search response.

    Returns:
        The decoded fixture.
    """
    return json.loads((FIXTURES_DIR / "pexels_search_response.json").read_text(encoding="utf-8"))


@pytest.fixture
def pixabay_response() -> dict[str, Any]:
    """Build a minimal Pixabay search response.

    Returns:
        A payload shaped like the real API's.
    """
    return {
        "total": 1,
        "totalHits": 1,
        "hits": [
            {
                "id": 55555,
                "pageURL": "https://pixabay.com/videos/id-55555/",
                "duration": 12,
                "user": "PixabayUser",
                "user_id": 999,
                "videos": {
                    "large": {
                        "url": "https://cdn.pixabay.com/large.mp4",
                        "width": 1080,
                        "height": 1920,
                    },
                    "medium": {
                        "url": "https://cdn.pixabay.com/medium.mp4",
                        "width": 1920,
                        "height": 1080,
                    },
                },
            }
        ],
    }
