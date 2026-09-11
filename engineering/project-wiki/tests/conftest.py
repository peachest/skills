"""Shared fixtures for the project-wiki fail-closed test suite.

Runs both CLI runtimes (wiki.py / wiki.js) as subprocesses against
throwaway fixture projects, mirroring the way real consumers invoke them.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent
WIKI_PY = SKILL_DIR / "scripts" / "wiki.py"
WIKI_JS = SKILL_DIR / "scripts" / "wiki.js"

RUNTIMES = ["python", "node"]


def build_cmd(runtime: str, args: list[str]) -> list[str]:
    if runtime == "python":
        return [sys.executable, str(WIKI_PY), *args]
    if runtime == "node":
        return ["node", str(WIKI_JS), *args]
    raise ValueError(f"unknown runtime: {runtime}")


def run_wiki(runtime: str, args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Invoke the wiki CLI for one runtime and return the CompletedProcess."""
    proc = subprocess.run(
        build_cmd(runtime, args),
        capture_output=True,
        text=True,
        timeout=120,
    )
    if check and proc.returncode != 0:
        raise AssertionError(
            f"{runtime} {args} exited {proc.returncode}\n"
            f"stdout: {proc.stdout[-2000:]}\nstderr: {proc.stderr[-2000:]}"
        )
    return proc


def run_json(runtime: str, args: list[str]) -> dict:
    """Invoke the wiki CLI with --json appended and parse the JSON result."""
    proc = run_wiki(runtime, [*args, "--json"], check=False)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as err:
        raise AssertionError(
            f"{runtime} {args} --json did not emit valid JSON: {err}\n"
            f"stdout: {proc.stdout[-2000:]}\nstderr: {proc.stderr[-2000:]}"
        ) from err


def make_go_project(root: Path) -> Path:
    """Create a fixture Go project: modules auth, storage, root."""
    (root / "auth").mkdir(parents=True)
    (root / "auth" / "login.go").write_text("package auth\n")
    (root / "auth" / "jwt.go").write_text("package auth\n")
    (root / "storage").mkdir()
    (root / "storage" / "db.go").write_text("package storage\n")
    (root / "main.go").write_text("package main\n")
    return root


@pytest.fixture
def go_project(tmp_path: Path) -> Path:
    """A fresh fixture project per test."""
    return make_go_project(tmp_path)


@pytest.fixture
def initialized(go_project: Path):
    """Factory: run init (+update) with a chosen runtime, return the project root."""
    created = {}

    def _init(runtime: str, do_update: bool = True) -> Path:
        run_wiki(runtime, ["init", "--root", str(go_project)])
        if do_update:
            run_wiki(runtime, ["update", "--root", str(go_project)])
        created["runtime"] = runtime
        return go_project

    yield _init
    assert "runtime" in created, "fixture not initialized — call _init(runtime) in the test"


def wiki_dir(root: Path) -> Path:
    return root / "docs" / "project_wiki"


def load_cache(root: Path) -> dict:
    return json.loads((wiki_dir(root) / ".review_cache.json").read_text())
