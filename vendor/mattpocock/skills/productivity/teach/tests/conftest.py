"""Fixtures for css-self-check tests.

The seam is the CLI: write a temp HTML file, run the script as a subprocess,
assert on exit code + stdout. No internal imports — tests observe behavior
through the public interface only.
"""
from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "assets" / "css-self-check.py"


@pytest.fixture
def run_check(tmp_path: Path):
    """Return a callable that writes HTML to a temp file and runs the checker."""

    def _run(html: str) -> subprocess.CompletedProcess[str]:
        f = tmp_path / "lesson.html"
        f.write_text(textwrap.dedent(html), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(f)],
            capture_output=True,
            text=True,
        )

    return _run
