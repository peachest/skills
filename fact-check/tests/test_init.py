"""Integration tests for scripts/init.sh.

Seam: bash scripts/init.sh <path> [project-root] → stdout JSON
  {document_key, mode, repo, session_tag, is_directory}

Tests use the real skill repo (which is a git repo at parent levels).
For tests requiring git remote, a temp git repo is created.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def run_init(path: str, project_root: str | None = None) -> tuple[dict, int]:
    """Run init.sh and return (parsed stdout JSON, exit code)."""
    args = ["bash", str(SCRIPTS_DIR / "init.sh"), path]
    if project_root:
        args.append(project_root)
    result = subprocess.run(args, capture_output=True, text=True, timeout=10)
    return json.loads(result.stdout), result.returncode


def _make_git_repo(tmp: str, remote_url: str = "https://github.com/test-org/test-repo.git") -> str:
    """Create a temp git repo with one commit, return path."""
    import os
    os.chdir(tmp)
    subprocess.run(["git", "init"], capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", remote_url], capture_output=True)
    (Path(tmp) / "README.md").write_text("# Test\n")
    subprocess.run(["git", "add", "README.md"], capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], capture_output=True)
    subprocess.run(["git", "checkout", "-b", "feat-test"], capture_output=True)
    return tmp


# ---------------------------------------------------------------------------
# init.sh tests
# ---------------------------------------------------------------------------


class TestInitBasic:
    """Tests that work against any directory (git or not)."""

    def test_returns_valid_json(self):
        repo = str(SCRIPTS_DIR.parent)
        doc = str(SCRIPTS_DIR.parent / "SKILL.md")
        data, code = run_init(doc, repo)
        assert code == 0
        assert "document_key" in data
        assert "mode" in data
        assert "repo" in data
        assert "session_tag" in data
        assert "is_directory" in data

    def test_is_directory_false_for_file(self):
        repo = str(SCRIPTS_DIR.parent)
        doc = str(SCRIPTS_DIR.parent / "SKILL.md")
        data, code = run_init(doc, repo)
        assert code == 0
        assert data["is_directory"] is False

    def test_is_directory_true_for_dir(self):
        repo = str(SCRIPTS_DIR.parent)
        doc = str(SCRIPTS_DIR.parent / "prompts")
        data, code = run_init(doc, repo)
        assert code == 0
        assert data["is_directory"] is True

    def test_mode_full_when_no_ledger(self):
        repo = str(SCRIPTS_DIR.parent)
        doc = str(SCRIPTS_DIR.parent / "SKILL.md")
        data, code = run_init(doc, repo)
        assert code == 0
        assert data["mode"] == "full"

    def test_document_key_double_dash(self):
        repo = str(SCRIPTS_DIR.parent)
        doc = str(SCRIPTS_DIR.parent / "prompts" / "extract-claims.md")
        data, code = run_init(doc, repo)
        assert code == 0
        assert data["document_key"].startswith("prompts--")
        assert "extract-claims.md" in data["document_key"]


class TestInitGitRepo:
    """Tests requiring a real git repo with remote."""

    def test_repo_extracted_from_git_remote(self):
        with tempfile.TemporaryDirectory() as tmp:
            _make_git_repo(tmp)
            doc = str(Path(tmp) / "README.md")
            data, code = run_init(doc, tmp)
            assert code == 0
            assert data["repo"] == "test-org/test-repo"

    def test_session_tag_is_branch_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            _make_git_repo(tmp)
            doc = str(Path(tmp) / "README.md")
            data, code = run_init(doc, tmp)
            assert code == 0
            assert data["session_tag"] == "feat-test"

    def test_mode_incremental_when_ledger_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            _make_git_repo(tmp)
            # Create a mock ledger file
            ledger_dir = Path(tmp) / "fact-check" / "documents" / "README.md"
            ledger_dir.mkdir(parents=True)
            (ledger_dir / "ledger.jsonl").write_text('{"vid":"abc"}\n')
            doc = str(Path(tmp) / "README.md")
            data, code = run_init(doc, tmp)
            assert code == 0
            assert data["mode"] == "incremental"


class TestInitNonGit:
    """Tests against non-git directories."""

    def test_non_git_repo_is_no_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "test.md"
            doc.write_text("# Hello\nWorld")
            data, code = run_init(str(doc), tmp)
            assert code == 0
            assert data["repo"] == "NO_REPO"

    def test_non_git_markdown_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            subdir = Path(tmp) / "docs"
            subdir.mkdir()
            (subdir / "a.md").write_text("# A")
            data, code = run_init(str(subdir), tmp)
            assert code == 0
            assert data["is_directory"] is True
