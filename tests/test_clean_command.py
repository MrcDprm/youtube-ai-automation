"""clean empties only folders of generated files, and asks before it does.

Dangerous targets are checked through the pure ``_unsafe_to_clear`` function. The command-line
tests aim at a fake project inside ``tmp_path``, so a broken guard could only ever delete
temporary files, never the real repository or a drive.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

import main
from config.settings import get_settings

runner = CliRunner()


@pytest.fixture
def fake_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    project = tmp_path / "project"
    (project / ".git").mkdir(parents=True)
    (project / "main.py").write_text("print('source')\n", encoding="utf-8")
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setattr(main, "PROJECT_ROOT", project)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    return project


def test_dangerous_folders_are_named_with_a_reason(fake_project: Path, tmp_path: Path) -> None:
    sources = tmp_path / "modules"
    sources.mkdir()
    (sources / "editor.py").write_text("", encoding="utf-8")

    assert main._unsafe_to_clear(Path(tmp_path.anchor)) == "it is the root of a drive"
    assert main._unsafe_to_clear(fake_project) == "it holds the project itself"
    assert main._unsafe_to_clear(tmp_path) == "it holds the project itself"
    assert main._unsafe_to_clear(tmp_path / "home") == "it holds your home folder"
    assert main._unsafe_to_clear(sources) == "it holds source files"
    assert main._unsafe_to_clear(fake_project / "output") is None


def test_clean_refuses_the_project_folder_and_deletes_nothing(
    fake_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OUTPUT_DIR", str(fake_project))
    get_settings.cache_clear()

    result = runner.invoke(main.app, ["clean", "--output", "--yes"])

    assert result.exit_code == 1, result.output
    assert "Refusing to empty" in result.output
    assert (fake_project / "main.py").is_file()
    assert (fake_project / ".git").is_dir()


@pytest.fixture
def generated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    out = tmp_path / "out"
    out.mkdir()
    (out / "video.mp4").write_bytes(b"video")
    monkeypatch.setenv("OUTPUT_DIR", str(out))
    get_settings.cache_clear()
    return out


def test_clean_keeps_everything_when_the_answer_is_no(generated: Path) -> None:
    result = runner.invoke(main.app, ["clean", "--output"], input="n\n")

    assert result.exit_code == 0, result.output
    assert "Delete everything inside" in result.output
    assert (generated / "video.mp4").is_file()


def test_clean_deletes_after_a_yes(generated: Path) -> None:
    result = runner.invoke(main.app, ["clean", "--output"], input="y\n")

    assert result.exit_code == 0, result.output
    assert not (generated / "video.mp4").exists()


def test_the_yes_flag_skips_the_question(generated: Path) -> None:
    result = runner.invoke(main.app, ["clean", "--output", "--yes"])

    assert result.exit_code == 0, result.output
    assert "Delete everything inside" not in result.output
    assert not (generated / "video.mp4").exists()
