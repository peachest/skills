"""reclean-en.py — pure-function tests (split, chunk, align, prompt)."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "reclean-en.py"
spec = importlib.util.spec_from_file_location("rc", SCRIPT)
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)


def test_split_body_strips_header():
    doc = "# 转录结果\n\n| 字段 | 值 |\n|---|---|\n\n---\n\n正文开始"
    assert rc.split_body(doc) == "正文开始"


def test_split_body_no_divider_returns_all():
    assert rc.split_body("plain text") == "plain text"


def test_chunk_respects_boundary():
    text = "。" * 10 + "尾巴"
    parts = rc.chunk(text, size=6)
    assert all(len(p) <= 6 for p in parts)
    assert "".join(parts) == text


def test_chunk_short_text_single():
    assert rc.chunk("短文本", size=3000) == ["短文本"]


def test_align_slices_count_matches():
    parts = rc.chunk("句。" * 500, size=50)
    slices = rc.align_slices(parts, "a" * 1000)
    assert len(slices) == len(parts)
    assert "".join(slices) == "a" * 1000


def test_prompt_contains_reference_and_glossary():
    p = rc.PROMPT.format(glossary="\n术语：X\n", en="EN REF", zh="ZH RAW")
    assert "EN REF" in p and "ZH RAW" in p and "术语：X" in p


def test_clean_chunk_sends_configured_model():
    import asyncio

    captured = {}

    class FakeResp:
        def raise_for_status(self):
            pass

        async def json(self):
            return {"choices": [{"message": {"content": " cleaned "}}]}

    class FakeSession:
        async def post(self, url, headers=None, json=None, timeout=None):
            captured.update(url=url, json=json, headers=headers)
            return FakeResp()

    conf = {"CLEAN_LLM_BASEURL": "http://x/v1", "CLEAN_LLM_MODEL": "m1", "CLEAN_LLM_KEY": ""}
    out = asyncio.run(rc.clean_chunk(FakeSession(), conf, "prompt", asyncio.Semaphore(1)))
    assert out == "cleaned"
    assert captured["json"]["model"] == "m1"
    assert "Authorization" not in captured["headers"]
