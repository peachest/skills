"""clean-transcripts.py — pure-function tests (split, chunk, cleaned-guard)."""

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "clean-transcripts.py"
spec = importlib.util.spec_from_file_location("ct", SCRIPT)
ct = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ct)


DOC = """# 转录结果

| 字段 | 值 |
|------|-----|
| 音频时长 | 535.4s |

---

正文第一段没有标点的原始文本
正文第二行连续不断
"""


def test_split_body_header_and_body():
    header, body = ct.split_body(DOC)
    assert header.rstrip().endswith("---")
    assert body.startswith("正文第一段")
    assert "535.4" in header and "535.4" not in body


def test_split_body_no_divider_returns_all_as_body():
    header, body = ct.split_body("只有正文")
    assert header == ""
    assert body == "只有正文"


def test_chunk_respects_boundaries():
    text = "字" * 2500 + "\n" + "行" * 2500 + "\n" + "尾" * 500
    parts = ct.chunk(text, 3000)
    assert len(parts) == 3
    assert parts[0].startswith("字") and len(parts[0]) <= 3000
    assert parts[1].startswith("行")
    assert parts[2] == "尾" * 500


def test_chunk_short_text_single():
    assert ct.chunk("短文本", 3000) == ["短文本"]


def test_is_cleaned_markers(tmp_path):
    # raw backup marker
    (tmp_path / "transcript.raw.md").write_text("x", encoding="utf-8")
    assert ct.is_cleaned(tmp_path)
    # dual merged state
    tmp2 = tmp_path / "d2"
    tmp2.mkdir()
    (tmp2 / "dual-state.json").write_text(json.dumps({"merged": True}), encoding="utf-8")
    assert ct.is_cleaned(tmp2)
    # dual en-only state is NOT cleaned (still needs merge)
    tmp3 = tmp_path / "d3"
    tmp3.mkdir()
    (tmp3 / "dual-state.json").write_text(json.dumps({"en_done": True}), encoding="utf-8")
    assert not ct.is_cleaned(tmp3)
    # untouched
    tmp4 = tmp_path / "d4"
    tmp4.mkdir()
    assert not ct.is_cleaned(tmp4)
