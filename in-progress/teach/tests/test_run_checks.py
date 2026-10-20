"""Tests for run-checks.sh — the battery orchestrator.

The seam is the CLI over a synthetic workspace: lessons/ dir with tiny HTML
files plus a hand-written anchors.json. Verified per the field-proven contract
(SKILL.md Navigation Self-Check section + script header):

  - per-family exit matrix: fix-class findings → exit 1; adjudication-class
    (beat/prose) always exit 0 (kept-with-reason is a PASS); anchor exit 1
    only on open findings
  - verdict table is the LAST output line, so `| tail -1` recovers the true
    status even when the pipe eats the exit code
  - --only / --lesson subset selection; --lesson writes checks-<N>.txt
  - anchors.json absent → anchor SKIP with note, battery still exits per the
    remaining checks
  - full findings file is check-prefixed
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "assets" / "run-checks.sh"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["bash", str(SCRIPT), *args],
                          capture_output=True, text=True)


def make_workspace(tmp_path: Path, lessons: dict[str, str],
                   anchors: str | None = None) -> Path:
    ws = tmp_path / "course"
    (ws / "lessons").mkdir(parents=True)
    for name, html in lessons.items():
        (ws / "lessons" / name).write_text(html, encoding="utf-8")
    if anchors is not None:
        (ws / "anchors.json").write_text(anchors, encoding="utf-8")
    return ws


# minimal well-formed lesson: css uses tokens, prose is short (SKIP threshold),
# neighbour links (nav-chain requires the pair linked), no figures
CLEAN = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>t</title></head>
<body><h1>标题</h1><p>一句话。{%s}</p><a href="{sibling}">{sibling}</a></body></html>"""

# css violation: bare px literal
CSS_DIRTY = CLEAN % ""

CSS_BAD = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>t</title>
<style>.x { font-size: 13px; }</style></head>
<body><h1>标题</h1><p>一句话。</p></body></html>"""


@pytest.fixture
def short_course(tmp_path: Path):
    """Two lessons, one numbered 0001 (for --lesson tests)."""
    return make_workspace(tmp_path, {
        "0001-a.html": (CLEAN % "abc").replace("{sibling}", "0002-b.html"),
        "0002-b.html": (CLEAN % "def").replace("{sibling}", "0001-a.html"),
    })


class TestCleanPass:
    def test_clean_course_exit0_all_verdicts_pass(self, short_course):
        r = run(str(short_course / "lessons"))
        assert r.returncode == 0, r.stdout
        assert "css=PASS" in r.stdout and "nav=PASS" in r.stdout
        assert "beat=PASS" in r.stdout and "prose=PASS" in r.stdout


class TestExitMatrix:
    def test_css_finding_fails_battery(self, tmp_path):
        make_workspace(tmp_path, {"0001-a.html": CSS_BAD})
        r = run(str(tmp_path / "course" / "lessons"))
        assert r.returncode == 1
        assert "css=FAIL" in r.stdout

    def test_adjudication_finding_never_fails_battery(self, tmp_path):
        # prose flag (恰好 overuse) → FLAG, exit 0: kept-with-reason is a PASS
        dirty = (CLEAN % ("恰好" * 6)).replace("{sibling}", "0001-a.html")
        make_workspace(tmp_path, {"0001-a.html": dirty})
        r = run(str(tmp_path / "course" / "lessons"))
        assert "prose=FLAG" in r.stdout
        assert r.returncode == 0, r.stdout


class TestVerdictLastLine:
    def test_tail_minus_one_recovers_true_status(self, short_course):
        r = run(str(short_course / "lessons"))
        last = r.stdout.strip().splitlines()[-1]
        assert last.startswith("CHECKS:") and "PASS" in last
        # findings file path must NOT be the last line (it precedes the table)
        assert "full findings:" not in last

    def test_failing_course_tail_still_shows_fail(self, tmp_path):
        make_workspace(tmp_path, {"0001-a.html": CSS_BAD})
        r = run(str(tmp_path / "course" / "lessons"))
        last = r.stdout.strip().splitlines()[-1]
        assert "css=FAIL" in last  # survives | tail -1


class TestSubset:
    def test_only_css_beat_runs_subset(self, short_course):
        r = run("--only", "css,beat", str(short_course / "lessons"))
        assert r.returncode == 0
        assert "css=PASS" in r.stdout and "beat=PASS" in r.stdout
        assert "nav=" not in r.stdout and "prose=" not in r.stdout


class TestLessonFilter:
    def test_lesson_filter_writes_numbered_report(self, short_course):
        r = run("--lesson", "1", str(short_course / "lessons"))
        assert r.returncode == 0
        report = short_course / "reviews" / "checks-1.txt"
        assert report.exists()
        assert "checks-1.txt" in r.stdout
        assert (short_course / "course" / "reviews" / "checks-all.txt").exists() is False


class TestAnchorHandling:
    def test_no_anchors_json_skips_with_note(self, short_course):
        r = run("--only", "anchor", str(short_course / "lessons"))
        assert r.returncode == 0
        assert "SKIP" in r.stdout
        assert "anchor=SKIP" in r.stdout

    def test_open_anchor_finding_fails(self, tmp_path):
        lesson = (CLEAN % "达到 4.26x 加速。").replace("{sibling}", "0001-a.html")
        make_workspace(tmp_path, {"0001-a.html": lesson},
                       anchors='{"claims": [], "sources": {}}')
        r = run("--only", "anchor", str(tmp_path / "course" / "lessons"))
        assert r.returncode == 1

    def test_ruled_anchor_finding_passes(self, tmp_path):
        make_workspace(
            tmp_path, {"lesson-a.html": (CLEAN % "达到 4.26x 加速。").replace("{sibling}", "")},
            anchors=json_ruled())
        r = run("--only", "anchor", str(tmp_path / "course" / "lessons"))
        assert r.returncode == 0, r.stdout
        assert "anchor=PASS" in r.stdout


def json_ruled() -> str:
    import json
    return json.dumps({
        "claims": [], "sources": {},
        "_rulings": ["UNANCHORED '4.26x': benchmark eyeball from Fig.1, "
                     "adjudicated kept (plot-read)"]}, ensure_ascii=False)


class TestFindingsFile:
    def test_findings_are_check_prefixed(self, tmp_path):
        make_workspace(tmp_path, {"0001-a.html": CSS_BAD})
        run(str(tmp_path / "course" / "lessons"))
        report = tmp_path / "course" / "reviews" / "checks-all.txt"
        content = report.read_text()
        assert any(line.startswith("css:") for line in content.splitlines())

    def test_usage_no_dir(self):
        r = run()
        assert r.returncode == 2
