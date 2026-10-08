"""Tests for anchor-check.py — synthetic anchors, no real paper content."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "assets" / "anchor-check.py"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True)


def make_env(tmp_path: Path, lesson_html: str, tex_lines: list[str],
             claims: list[dict], extra_sources: dict | None = None) -> tuple[Path, Path]:
    tex = tmp_path / "example_paper.tex"
    tex.write_text("\n".join(tex_lines))
    ledger = {
        "claims": claims,
        "sources": {"tex:1": {"path": str(tex), "kind": "tex"},
                    "tex:2": {"path": str(tex), "kind": "tex"}},
    }
    if extra_sources:
        ledger["sources"].update(extra_sources)
    aj = tmp_path / "anchors.json"
    aj.write_text(json.dumps(ledger, ensure_ascii=False))
    lesson = tmp_path / "lesson.html"
    lesson.write_text(lesson_html, encoding="utf-8")
    return aj, lesson


class TestVerbatimVerification:
    def test_matching_anchor_passes(self, tmp_path):
        aj, lesson = make_env(
            tmp_path,
            "<p>训练使用 70K 对话。</p>",
            ["we use 70K ShareGPT dialogues for training",
             r"\caption{The pipeline overview}"],
            [{"quote": "70K", "anchor": "tex:1"}])
        r = run(str(aj), str(lesson))
        assert r.returncode == 0, r.stdout
        assert "all anchors verified" in r.stdout

    def test_mismatched_line_fails(self, tmp_path):
        # anchor points at line 2 (caption) but quote is from line 1
        aj, lesson = make_env(
            tmp_path,
            "<p>训练使用 70K 对话。</p>",
            ["we use 70K ShareGPT dialogues for training",
             r"\caption{The pipeline overview}"],
            [{"quote": "70K", "anchor": "tex:2"}])
        r = run(str(aj), str(lesson))
        assert r.returncode == 1
        assert "MISMATCH" in r.stdout

    def test_missing_source_file_fails(self, tmp_path):
        tex = tmp_path / "gone.tex"
        tex.write_text("nothing")
        aj = tmp_path / "anchors.json"
        aj.write_text(json.dumps({
            "claims": [{"quote": "x", "anchor": "tex:1"}],
            "sources": {"tex:1": {"path": str(tmp_path / "missing.tex"), "kind": "tex"}}}))
        lesson = tmp_path / "l.html"
        lesson.write_text("<p>x</p>")
        r = run(str(aj), str(lesson))
        assert r.returncode == 1
        assert "BROKEN" in r.stdout

    def test_anchor_not_in_ledger_fails(self, tmp_path):
        # claim references an anchor absent from sources — must be named as
        # such, not collapsed into the generic UNANCHORED bucket
        aj, lesson = make_env(
            tmp_path, "<p>3.62x 加速。</p>",
            ["abstract claim 3.62x speedup"],
            [{"quote": "3.62x", "anchor": "tex:9"}])
        r = run(str(aj), str(lesson))
        assert r.returncode == 1
        assert "NO-SOURCE" in r.stdout


class TestFigureDrift:
    def test_lesson_citing_absent_figure_number_fails(self, tmp_path):
        aj, lesson = make_env(
            tmp_path,
            "<p>如图 7 所示，接受率下降。</p>",
            [r"\caption{Alpha sweep}" ],  # local tex has no "Figure 7" anywhere
            [])
        r = run(str(aj), str(lesson))
        assert r.returncode == 1
        assert "FIG-DRIFT" in r.stdout

    def test_figure_number_present_in_tex_passes(self, tmp_path):
        aj, lesson = make_env(
            tmp_path,
            "<p>如图 7 所示。</p>",
            ["As shown in Figure 7, the acceptance rate drops", r"\caption{x}"],
            [])
        r = run(str(aj), str(lesson))
        assert "FIG-DRIFT" not in r.stdout


class TestUnanchoredNumbers:
    def test_unanchored_distinctive_number_reported(self, tmp_path):
        aj, lesson = make_env(
            tmp_path,
            "<p>加速达到 4.26x。</p>",  # 4.26x anchored nowhere
            ["unrelated line", r"\caption{c}"],
            [])
        r = run(str(aj), str(lesson))
        assert r.returncode == 1
        assert "UNANCHORED" in r.stdout

    def test_anchored_number_not_double_reported(self, tmp_path):
        aj, lesson = make_env(
            tmp_path,
            "<p>加速达到 3.62x。</p>",
            ["abstract claim 3.62x speedup", r"\caption{c}"],
            [{"quote": "3.62x", "anchor": "tex:1"}])
        r = run(str(aj), str(lesson))
        assert r.returncode == 0, r.stdout

    def test_years_and_single_digits_exempt(self, tmp_path):
        aj, lesson = make_env(
            tmp_path,
            "<p>2024 年发表，第 3 节。</p>", ["line one", r"\caption{c}"],
            [])
        r = run(str(aj), str(lesson))
        assert "UNANCHORED" not in r.stdout


class TestUsage:
    def test_needs_two_args(self, tmp_path):
        r = run(str(tmp_path / "a.json"))
        assert r.returncode == 2
        assert "usage" in r.stderr

    def test_missing_lesson_file(self, tmp_path):
        aj = tmp_path / "anchors.json"
        aj.write_text("{}")
        r = run(str(aj), str(tmp_path / "nope.html"))
        assert r.returncode == 2


class TestRulings:
    """_rulings suppressions: adjudicated findings print but don't fail exit."""

    def test_ruled_finding_printed_but_exit_zero(self, tmp_path):
        tex = tmp_path / "p.tex"
        tex.write_text("unrelated")
        aj = tmp_path / "anchors.json"
        aj.write_text(json.dumps({
            "claims": [],
            "sources": {},
            "_rulings": ["UNANCHORED '100%': CSS width syntax, not a claim"]}))
        lesson = tmp_path / "l.html"
        lesson.write_text("<p>占比 100% 以上。</p>")
        r = run(str(aj), str(lesson))
        assert r.returncode == 0, r.stdout
        assert "ADJUDICATED (kept)" in r.stdout
        assert "0 open / 1 adjudicated" in r.stdout

    def test_unruled_similar_finding_still_fails(self, tmp_path):
        aj = tmp_path / "anchors.json"
        aj.write_text(json.dumps({
            "claims": [], "sources": {},
            "_rulings": ["UNANCHORED '100%': css"]}))
        lesson = tmp_path / "l.html"
        lesson.write_text("<p>达到 95% 以上。</p>")
        r = run(str(aj), str(lesson))
        assert r.returncode == 1


class TestFalsePositiveFamilies:
    """Field-identified FP classes (specforge ~56% of UNANCHORED lines)."""

    def test_citation_line_number_excluded(self, tmp_path):
        aj = tmp_path / "anchors.json"
        aj.write_text(json.dumps({"claims": [], "sources": {}}))
        lesson = tmp_path / "l.html"
        lesson.write_text("<p>见 tex:147 与 paper.tex:513 的原文。</p>")
        r = run(str(aj), str(lesson))
        assert r.returncode == 0, r.stdout

    def test_css_media_context_excluded(self, tmp_path):
        aj = tmp_path / "anchors.json"
        aj.write_text(json.dumps({"claims": [], "sources": {}}))
        lesson = tmp_path / "l.html"
        lesson.write_text('<style>@media (max-width: 800px) { .x { color: #fff } }</style>')
        r = run(str(aj), str(lesson))
        assert r.returncode == 0, r.stdout


def test_rulings_dict_shape_also_accepted(tmp_path):
    aj = tmp_path / "anchors.json"
    aj.write_text(json.dumps({
        "claims": [], "sources": {},
        "_rulings": {"UNANCHORED '100%'": "css width syntax"}}))
    lesson = tmp_path / "l.html"
    lesson.write_text("<p>占比 100% 以上。</p>")
    r = run(str(aj), str(lesson))
    assert r.returncode == 0, r.stdout
