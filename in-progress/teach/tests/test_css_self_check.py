"""Tests for css-self-check.py — verify through the CLI seam.

Each test writes an HTML temp file and runs the script as a subprocess,
asserting on exit code and stdout. The script is a linter; its public
interface is (file path) -> (exit 0/1, stdout listing violations).
"""
from __future__ import annotations


class TestCleanFiles:
    """Files with no violations exit 0 and print OK."""

    def test_all_var_tokens(self, run_check):
        html = """
        <html><head><style>
        .x { font-size: var(--fs-small); padding: var(--sp-4); line-height: var(--lh-body); }
        </style></head><body></body></html>
        """
        r = run_check(html)
        assert r.returncode == 0
        assert "OK" in r.stdout

    def test_no_style_block(self, run_check):
        html = "<html><body><p>no styles here</p></body></html>"
        r = run_check(html)
        assert r.returncode == 0
        assert "OK" in r.stdout

    def test_empty_style_block(self, run_check):
        html = "<html><head><style></style></head><body></body></html>"
        r = run_check(html)
        assert r.returncode == 0


class TestRelativeValuesPass:
    """em/% and 0 are outside the token system and pass."""

    def test_single_em(self, run_check):
        html = "<style>.x { font-size: 0.88em; }</style>"
        assert run_check(html).returncode == 0

    def test_multi_value_em(self, run_check):
        """Regression: multi-value em (e.g. padding: 0.15em 0.35em) must pass.

        The original single-value regex ^[\\d.]+(em|%)$ flagged this; the fix
        splits on whitespace and passes if every token is em/%/0.
        """
        html = "<style>.x { padding: 0.15em 0.35em; }</style>"
        assert run_check(html).returncode == 0

    def test_zero_value(self, run_check):
        html = "<style>.x { padding: 0; margin: 0; }</style>"
        assert run_check(html).returncode == 0

    def test_percent_value(self, run_check):
        html = "<style>.x { width: 50%; padding: 2%; }</style>"
        assert run_check(html).returncode == 0


class TestAbsoluteLiteralsFlagged:
    """px/rem/pt and bare numbers are violations -> exit 1."""

    def test_bare_px_font_size(self, run_check):
        r = run_check("<style>.x { font-size: 13px; }</style>")
        assert r.returncode == 1
        assert "font-size: 13px" in r.stdout

    def test_bare_rem_padding(self, run_check):
        r = run_check("<style>.x { padding: 1rem; }</style>")
        assert r.returncode == 1
        assert "padding: 1rem" in r.stdout

    def test_bare_number_line_height(self, run_check):
        r = run_check("<style>.x { line-height: 1.8; }</style>")
        assert r.returncode == 1
        assert "line-height: 1.8" in r.stdout

    def test_pt_unit_flagged(self, run_check):
        r = run_check("<style>.x { font-size: 12pt; }</style>")
        assert r.returncode == 1
        assert "12pt" in r.stdout

    def test_multi_value_with_px_flagged(self, run_check):
        r = run_check("<style>.x { margin: 12px 0; }</style>")
        assert r.returncode == 1
        assert "margin: 12px 0" in r.stdout


class TestInlineStyleAttribute:
    """Inline style="" attributes are scanned too."""

    def test_inline_bare_flagged(self, run_check):
        html = '<p style="font-size: 14px;">hi</p>'
        r = run_check(html)
        assert r.returncode == 1
        assert "font-size: 14px" in r.stdout

    def test_inline_var_passes(self, run_check):
        html = '<p style="color: var(--accent);">hi</p>'
        assert run_check(html).returncode == 0


class TestMultipleViolations:
    """All violations in a file are reported, not just the first."""

    def test_reports_all(self, run_check):
        html = """
        <style>
        .a { font-size: 13px; padding: 16px; }
        .b { line-height: 1.8; }
        </style>
        """
        r = run_check(html)
        assert r.returncode == 1
        assert "font-size: 13px" in r.stdout
        assert "padding: 16px" in r.stdout
        assert "line-height: 1.8" in r.stdout
        assert "3 bare literal(s)" in r.stdout


class TestKatexDependencies:
    """Math in prose but KaTeX bundle not referenced -> exit 1 with the
    exact lines to add (spec-decoding lesson-0005 friction, commit 93e78fe).
    Fixture convention here is inline HTML, same as the classes above."""

    HEAD = '''<head>
  <link rel="stylesheet" href="../assets/katex.min.css">
  <script src="../assets/katex.min.js" defer></script>
  <script src="../assets/auto-render.min.js" defer></script>
  <script src="../assets/render.js" defer></script>
</head>'''

    def test_math_without_bundle_fails(self, run_check):
        html = "<html><head><title>t</title></head><body><p>设 $k$ 为层数，$$V_i=\\prod_j p_j$$。</p></body></html>"
        r = run_check(html)
        assert r.returncode == 1
        assert "KaTeX 依赖缺失" in r.stdout
        assert "katex.min.css" in r.stdout
        assert '<script src="../assets/render.js" defer></script>' in r.stdout

    def test_math_with_full_bundle_passes(self, run_check):
        html = f"<html>{self.HEAD}<body><p>设 $k$ 为层数。</p></body></html>"
        r = run_check(html)
        assert r.returncode == 0
        assert "OK" in r.stdout

    def test_partial_bundle_lists_only_missing(self, run_check):
        html = ('<html><head><script src="../assets/katex.min.js" defer></script></head>'
                '<body><p>$p_j$ 是概率。</p></body></html>')
        r = run_check(html)
        assert r.returncode == 1
        assert "render.js" in r.stdout
        assert "katex.min.js" not in r.stdout

    def test_no_math_no_requirement(self, run_check):
        html = "<html><head></head><body><p>纯文字，无公式。</p></body></html>"
        assert run_check(html).returncode == 0

    def test_shell_prompt_dollar_not_math(self, run_check):
        # $ npm i ... $ in <code>/<pre> must not count as math
        html = ("<html><head></head><body>"
                "<pre><code>$ npm install\n$ npm run build</code></pre>"
                "<p>价格是 100$ 到 200$ 之间。</p></body></html>")
        assert run_check(html).returncode == 0

    def test_paren_delimiters_count(self, run_check):
        html = '<html><head></head><body><p>其中 \\(C = 2nds\\) 为缓存。</p></body></html>'
        r = run_check(html)
        assert r.returncode == 1
        assert "KaTeX 依赖缺失" in r.stdout


class TestUsageError:
    def test_no_arg_exits_2(self, run_check, tmp_path):
        import subprocess
        import sys
        from pathlib import Path

        script = Path(__file__).resolve().parent.parent / "assets" / "css-self-check.py"
        r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        assert r.returncode == 2
        assert "usage" in r.stderr
