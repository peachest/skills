"""Tests for resource-check.py — synthetic fixtures, tmp_path trees."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "assets" / "resource-check.py"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True)


def make_workspace(tmp_path: Path, lesson: str, files: dict[str, str]) -> Path:
    (tmp_path / "lessons").mkdir(parents=True, exist_ok=True)
    (tmp_path / "lessons" / "0001-a.html").write_text(lesson, encoding="utf-8")
    for name, content in files.items():
        p = tmp_path / "lessons" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return tmp_path


class TestResolution:
    def test_all_refs_resolve(self, tmp_path):
        make_workspace(tmp_path,
            ('<link rel="stylesheet" href="../assets/base.css">'
             '<script src="../assets/quiz.js"></script>'
             '<img src="img/fig1.png" alt="f">'
             '<a href="0002-b.html">next</a>'),
            {"0002-b.html": "<p>x</p>",
             "../assets/base.css": "body{}", "../assets/quiz.js": "// js",
             "img/fig1.png": "png"})
        r = run(str(tmp_path / "lessons"))
        assert r.returncode == 0, r.stdout
        assert "all relative references resolve" in r.stdout

    def test_broken_relative_flagged(self, tmp_path):
        make_workspace(tmp_path, '<img src="img/nope.png">', {})
        r = run(str(tmp_path / "lessons"))
        assert r.returncode == 1
        assert "nope.png" in r.stdout
        assert "0001-a.html" in r.stdout

    def test_deep_relative_path(self, tmp_path):
        # the state_event shape: ../../../okb/... deep backtrack
        make_workspace(tmp_path, '<a href="../../../okb/silver/t/e.md">n</a>', {})
        r = run(str(tmp_path / "lessons"))
        assert r.returncode == 1


class TestSkips:
    def test_skips_external_and_data(self, tmp_path):
        make_workspace(tmp_path,
            ('<a href="https://arxiv.org/abs/2401.15077">p</a>'
             '<a href="mailto:x@y.z">m</a>'
             '<img src="data:image/png;base64,AAAA">'
             '<a href="#section1">jump</a>'
             '<a href="0001-a.html#refs">self-frag</a>'),
            {})
        r = run(str(tmp_path / "lessons"))
        assert r.returncode == 0, r.stdout

    def test_fragment_on_real_path_resolves_by_path(self, tmp_path):
        make_workspace(tmp_path, '<a href="../assets/base.css#tokens">c</a>',
                       {"../assets/base.css": "body{}"})
        r = run(str(tmp_path / "lessons"))
        assert r.returncode == 0

    def test_query_string_stripped(self, tmp_path):
        make_workspace(tmp_path, '<img src="img/f.png?v=2">', {"img/f.png": "p"})
        r = run(str(tmp_path / "lessons"))
        assert r.returncode == 0

    def test_srcset_multi_candidate(self, tmp_path):
        make_workspace(tmp_path, '<img srcset="img/a.png 1x, img/missing.png 2x">',
                       {"img/a.png": "a"})
        r = run(str(tmp_path / "lessons"))
        assert r.returncode == 1
        assert "missing.png" in r.stdout
        assert "a.png" not in r.stdout.split("broken")[1].splitlines()[0] if True else True


class TestInlineStyles:
    def test_css_url_checked(self, tmp_path):
        make_workspace(tmp_path,
            '<style>.hero { background: url("../assets/bg.png"); }</style>',
            {"../assets/bg.png": "b"})
        r = run(str(tmp_path / "lessons"))
        assert r.returncode == 0

    def test_css_url_missing_flagged(self, tmp_path):
        make_workspace(tmp_path, '<style>.h { background: url(img/none.png); }</style>', {})
        r = run(str(tmp_path / "lessons"))
        assert r.returncode == 1


class TestUsage:
    def test_dir_and_file_mixed(self, tmp_path):
        make_workspace(tmp_path, "<p>x</p>", {})
        r = run(str(tmp_path / "lessons"), str(tmp_path / "lessons" / "0001-a.html"))
        assert r.returncode == 0

    def test_no_args_usage(self, tmp_path):
        r = run()
        assert r.returncode == 2
        assert "usage" in r.stderr

    def test_nonexistent_arg(self, tmp_path):
        r = run(str(tmp_path / "nope"))
        assert r.returncode == 2
