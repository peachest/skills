"""Tests for the UTF-8-safe slug helper (fixes illegal-byte truncation)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
SLUGIFY_PY = SCRIPTS_DIR / "slugify.py"


def _slug(raw: str) -> str:
    r = subprocess.run(
        ["python3", str(SLUGIFY_PY)],
        input=raw.encode("utf-8"), capture_output=True, timeout=30,
    )
    assert r.returncode == 0, r.stderr.decode()
    return r.stdout.decode("utf-8").strip()


class TestIllegalFilenameChars:
    @pytest.mark.parametrize("bad", ["a/b", "a\\b", "a:b", "a*b", "a?b",
                                     'a"b', "a<b", "a>b", "a|b",
                                     "a\tb\nc"])
    def test_illegal_chars_replaced(self, bad):
        out = _slug(bad)
        assert "/" not in out and "\\" not in out and ":" not in out, \
            f"illegal chars survived: {bad!r} -> {out!r}"
        assert "*" not in out and "?" not in out and '"' not in out


class TestUTF8SafeTruncation:
    def test_never_splits_multibyte(self):
        """60 emoji (each 4 UTF-8 bytes) truncated at byte 60 would cut one
        in half. Code-point truncation must never do that."""
        title = "🎉" * 100  # 100 code points, 400 bytes
        out = _slug(title)
        assert len(out) == 60, f"slug longer than 60 code points: {len(out)}"
        out.encode("utf-8").decode("utf-8")  # round-trips => legal UTF-8
        assert "\ufffd" not in out, "replacement char in slug"

    def test_cjk_title_truncated_safely(self):
        """Chinese chars are 3 bytes each; byte-truncation at byte 60 would
        cut a char. Code-point truncation keeps the first 60 chars."""
        title = "测" * 80
        out = _slug(title)
        assert len(out) == 60
        out.encode("utf-8").decode("utf-8")

    def test_mixed_ascii_cjk_bytes(self):
        """Long mixed titles stay valid after truncation; the slug must be a
        byte-valid filename usable as a directory name."""
        title = "Anthropic开始授课-从入门到入土-所有AI课程免费学啊" * 4
        out = _slug(title)
        assert len(out) == 60
        b = out.encode("utf-8")
        b.decode("utf-8")  # must not raise


class TestEmpty:
    def test_empty_input_unknown(self):
        assert _slug("") == "unknown"
        assert _slug("\n  \t") == "unknown"
        assert _slug("   ") == "unknown"
        assert _slug("\x00") == "unknown"


class TestRealWorldTitle:
    def test_actual_bilibili_title(self):
        """真题库读取: 现有 `references/transcripts/bilibili/...` 目录名生成逻辑."""
        out = _slug("Anthropic开始授课-从入门到入土-所有AI课程免费学")
        assert "/" not in out and "\\" not in out
        assert out == out.strip()

    def test_slug_usable_as_directory_name(self, tmp_path):
        """The slug must be directly usable as a directory component."""
        out = _slug("A🎉B:C*D?E<F>G|H\\I/J\"K")
        d = tmp_path / out
        d.mkdir()
        assert d.exists()
        assert len(list(tmp_path.iterdir())) == 1