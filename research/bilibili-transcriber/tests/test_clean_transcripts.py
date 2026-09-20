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


def test_detect_lang_zh_en():
    zh = "这是一段中文转录文本，讨论检索与代理搜索的技术话题。" * 5
    en = "So great being here today to talk about the unreasonable effectiveness of BM25 for agentic search. " * 5
    assert ct.detect_lang(zh, {}) == "zh"
    assert ct.detect_lang(en, {}) == "en"
    # forced override wins
    assert ct.detect_lang(zh, {"CLEAN_LANG": "en"}) == "en"
    assert ct.detect_lang(en, {"CLEAN_LANG": "zh"}) == "zh"
    # empty/other values fall back to detection
    assert ct.detect_lang(en, {"CLEAN_LANG": ""}) == "en"


def test_detect_lang_mixed_dub_goes_zh():
    # bilingual dual-audio: majority zh with sprinkled EN terms -> zh prompt
    mixed = "这是一个中文为主的转录，夹杂 BM25 和 agentic search 等术语。" * 20
    assert ct.detect_lang(mixed, {}) == "zh"


def test_detect_lang_empty_body():
    # empty body never reaches detect_lang in the real flow (clean_transcript
    # returns early); degenerate latin check yields en — pin the behavior
    assert ct.detect_lang("", {}) == "en"


def test_has_repeated_sentences():
    assert not ct.has_repeated_sentences("One short. " + "A long enough sentence to pass the threshold. " * 1)
    looped = "The frontier LLM companies are optimizing their models for coding and tool use. " * 3
    assert ct.has_repeated_sentences(looped)
    assert not ct.has_repeated_sentences("")
