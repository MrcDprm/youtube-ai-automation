"""Every package can be the first one a program imports.

Each import runs in a fresh interpreter, because inside the test session every module is
already loaded and an import cycle would never show.
"""

from __future__ import annotations

import subprocess
import sys

import pytest

from config.constants import PROJECT_ROOT


@pytest.mark.parametrize(
    "module",
    ["utils.media", "utils.exceptions", "utils.preflight", "models.scenario", "config.settings"],
)
def test_the_module_imports_first_without_a_cycle(module: str) -> None:
    result = subprocess.run(
        [sys.executable, "-c", f"import {module}"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    assert result.returncode == 0, result.stderr[-1000:]
