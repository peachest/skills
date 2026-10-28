"""Script environment drift tests — contract comments vs implementation.

Regression class (2026-10-21): transcribe.sh's comment said "point PYTHON at a
python with numpy" while its default was bare `python3` (no numpy) — the ASR
stage died with ModuleNotFoundError after a full download, wasting a run.
These tests pin stage-script environment contracts so drift fails fast.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
SKILL_DIR = Path(__file__).parent.parent


def _sh_default(var: str, script: Path) -> str | None:
    """Extract ${VAR:-default} from a script and expand $SKILL_DIR refs."""
    text = script.read_text(encoding="utf-8")
    m = re.search(rf'{var}="\${{{var}:-(.*?)}}"', text)
    if not m:
        return None
    return m.group(1).replace("$SKILL_DIR", str(SKILL_DIR))


class TestTranscribePythonEnv:
    """transcribe.sh invokes chunk_transcribe.py (imports numpy)."""

    def test_python_default_can_import_chunk_deps(self):
        default = _sh_default("PYTHON", SCRIPTS_DIR / "transcribe.sh")
        assert default is not None, "PYTHON default assignment missing from transcribe.sh"
        assert "python3" != default.strip(), (
            "transcribe.sh PYTHON defaults to bare python3 — chunk_transcribe.py "
            "needs numpy which the system python lacks; point at the skill venv"
        )
        r = subprocess.run(
            [default, "-c", "import numpy"],
            capture_output=True, timeout=30,
        )
        assert r.returncode == 0, (
            f"transcribe.sh PYTHON default ({default}) cannot import numpy — "
            "stage would die mid-pipeline after download (2026-10-21 regression)"
        )

    def test_run_sh_bootstraps_venv_before_transcribe(self):
        """run.sh must guarantee the venv exists before any stage runs."""
        text = (SCRIPTS_DIR / "run.sh").read_text(encoding="utf-8")
        bootstrap_idx = text.find("uv sync")
        transcribe_idx = text.find("transcribe.sh")
        assert bootstrap_idx != -1, "run.sh has no venv bootstrap (uv sync)"
        assert transcribe_idx != -1, "run.sh never invokes transcribe.sh"
        assert bootstrap_idx < transcribe_idx, (
            "run.sh must uv-sync the venv before calling transcribe.sh — "
            "the venv-backed PYTHON default depends on it"
        )
