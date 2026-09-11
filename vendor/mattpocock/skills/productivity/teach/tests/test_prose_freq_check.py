"""Tests for prose-freq-check.py — Chinese stylistic-tic frequency audit.

The two real-data fixtures are the same lesson before and after a human-approved
de-slop pass (spec-decoding lesson 0001, commit f3ea426): the pre-fix version
must flag, the post-fix version must pass. Thresholds are calibrated on this
pair — if these tests break after a threshold change, the calibration is gone.
"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "assets" / "prose-freq-check.py"
FIXTURES = Path(__file__).parent / "fixtures"


def run(*files: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *[str(f) for f in files]],
        capture_output=True,
        text=True,
    )


def test_real_prefix_slop_fixture_flags():
    r = run(FIXTURES / "lesson-0001-prefix-slop.html")
    assert r.returncode == 0
    assert "FLAG 恰好: 9" in r.stdout
    assert "FLAG 永远: 4" in r.stdout
    assert "FLAG 不多不少: 1" in r.stdout
    assert "FLAG 同一件事: 1" in r.stdout
    assert "FLAG 都只是: 2" in r.stdout
    assert "FLAG —— density: 30.3" in r.stdout


def test_real_post_deslop_fixture_passes():
    r = run(FIXTURES / "lesson-0001-post-deslop.html")
    assert r.returncode == 0
    assert "ok   恰好: 4" in r.stdout
    assert "ok   永远: 2" in r.stdout
    assert "ok   不多不少: 0" in r.stdout
    assert "ok   同一件事: 0" in r.stdout
    assert "ok   都只是: 0" in r.stdout
    assert "FLAG —— density" not in r.stdout


def test_clean_synthetic_prose_passes(tmp_path):
    f = tmp_path / "0001-x.html"
    f.write_text("<html><body><p>恰好一次采样即为接受。</p></body></html>", encoding="utf-8")
    r = run(f)
    assert r.returncode == 0
    assert "FLAG" not in r.stdout


def test_tic_over_threshold_flags(tmp_path):
    f = tmp_path / "0001-x.html"
    body = "<p>这里的恰好恰好恰好恰好恰好恰好是六次。</p>"
    f.write_text(f"<html><body>{body}</body></html>", encoding="utf-8")
    r = run(f)
    assert r.returncode == 0
    assert "FLAG 恰好: 6" in r.stdout


def test_style_and_script_ignored(tmp_path):
    f = tmp_path / "0001-x.html"
    f.write_text(
        "<html><head><style>.x::after{content:'同一件事'}</style></head>"
        "<body><script>var s='不多不少都只是';</script><p>正常的正文。</p></body></html>",
        encoding="utf-8",
    )
    r = run(f)
    assert r.returncode == 0
    assert "FLAG" not in r.stdout
