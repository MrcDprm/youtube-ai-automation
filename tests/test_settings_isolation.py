"""The tests never read the developer's .env file, only environment variables."""

from __future__ import annotations

from pathlib import Path

import pytest

from config.settings import get_settings


def test_a_dotenv_file_in_the_working_folder_is_ignored(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / ".env").write_text(
        "VIDEO_FORMAT=gta\nDAILY_TIME=23:45\nGTA_BACKGROUND_DIR=D:/elsewhere\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    get_settings.cache_clear()

    loaded = get_settings()

    assert loaded.VIDEO_FORMAT == "shorts"
    assert loaded.DAILY_TIME == "09:00"
    assert loaded.GTA_BACKGROUND_DIR.as_posix() == "assets/background/gta5"


def test_environment_variables_still_apply(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DAILY_TIME", "07:30")
    get_settings.cache_clear()

    assert get_settings().DAILY_TIME == "07:30"
