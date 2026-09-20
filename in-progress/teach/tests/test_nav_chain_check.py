"""Tests for nav-chain-check.py — lesson navigation chain integrity."""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "assets" / "nav-chain-check.py"


def make_lessons(tmp_path: Path, files: dict[str, list[str]]) -> Path:
    d = tmp_path / "lessons"
    d.mkdir()
    for name, links in files.items():
        body = "".join(f'<a href="{l}">{l}</a>' for l in links)
        (d / name).write_text(f"<html>{body}</html>", encoding="utf-8")
    return d


def run(d: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(d)], capture_output=True, text=True
    )


def test_unbroken_chain_passes(tmp_path):
    d = make_lessons(
        tmp_path,
        {
            "0001-a.html": ["0002-b.html"],
            "0002-b.html": ["0001-a.html", "0003-c.html"],
            "0003-c.html": ["0002-b.html"],
        },
    )
    r = run(d)
    assert r.returncode == 0, r.stdout


def test_stale_next_link_fails(tmp_path):
    # 0002 shipped but 0001's next link never updated — the reported friction case
    d = make_lessons(
        tmp_path,
        {
            "0001-a.html": [],
            "0002-b.html": ["0001-a.html"],
        },
    )
    r = run(d)
    assert r.returncode == 1
    assert "0001-a.html" in r.stdout and "next" in r.stdout


def test_missing_back_link_fails(tmp_path):
    d = make_lessons(
        tmp_path,
        {
            "0001-a.html": ["0002-b.html"],
            "0002-b.html": [],
        },
    )
    r = run(d)
    assert r.returncode == 1
    assert "0002-b.html" in r.stdout and "back" in r.stdout


def test_single_lesson_passes(tmp_path):
    d = make_lessons(tmp_path, {"0001-a.html": []})
    r = run(d)
    assert r.returncode == 0, r.stdout


def test_nonnumbered_html_ignored(tmp_path):
    d = make_lessons(
        tmp_path,
        {"index.html": [], "0001-a.html": []},
    )
    r = run(d)
    assert r.returncode == 0, r.stdout
