"""dual-transcribe.py — pure-function tests (segments, windows, parse, assemble)."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "dual-transcribe.py"
spec = importlib.util.spec_from_file_location("dt", SCRIPT)
dt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dt)


def _chunk(path: Path, segs, chunk_no=0):
    path.write_text(__import__("json").dumps({
        "language": None,
        "segments": [{"start": s, "end": e, "text": t} for s, e, t in segs],
    }), encoding="utf-8")


def test_load_segments_global_offsets(tmp_path):
    d = tmp_path / "chunks" / "transcripts"
    d.mkdir(parents=True)
    _chunk(d / "chunk_000.json", [(0.0, 10.0, "甲"), (10.0, 29.8, "乙")])
    _chunk(d / "chunk_001.json", [(0.0, 5.0, "丙")])  # chunk-relative restart
    segs = dt.load_segments(d)
    assert segs[0]["start"] == 0.0
    assert segs[1]["end"] == 29.8
    # chunk 1 offset by 29.8 (prev chunk last end)
    assert segs[2]["start"] == 29.8
    assert segs[2]["end"] == 34.8
    assert segs[2]["text"] == "丙"


def test_load_segments_skips_empty_text(tmp_path):
    d = tmp_path / "chunks" / "transcripts"
    d.mkdir(parents=True)
    _chunk(d / "chunk_000.json", [(0.0, 5.0, ""), (5.0, 8.0, "字")])
    segs = dt.load_segments(d)
    assert len(segs) == 1 and segs[0]["text"] == "字"


def test_group_windows_partition_and_assignment():
    zh = [{"start": 0, "end": 50, "text": "中文一"}, {"start": 80, "end": 120, "text": "中文二"}]
    en = [{"start": 0, "end": 50, "text": "english one"}]
    ws = dt.group_windows(zh, en, window_sec=90)
    assert len(ws) == 2
    assert ws[0]["start"] == 0 and ws[0]["end"] == 90
    assert len(ws[0]["zh"]) == 1 and len(ws[0]["en"]) == 1
    assert ws[1]["zh"][0]["text"] == "中文二" and ws[1]["en"] == []


def test_classify_window():
    zh_seg = [{"start": 0, "end": 5, "text": "中文"}]
    en_seg = [{"start": 0, "end": 5, "text": "english text here"}]
    assert dt.classify_window({"zh": zh_seg, "en": en_seg}) == "pair"
    assert dt.classify_window({"zh": zh_seg, "en": []}) == "zh_only"
    # English bleed inside the zh pass still counts as en material
    assert dt.classify_window({"zh": en_seg, "en": []}) == "en_only"
    assert dt.classify_window({"zh": [{"start": 0, "end": 1, "text": "…"}], "en": []}) == "zh_only"
    assert dt.classify_window({"zh": [], "en": []}) == "empty"


def test_parse_merge_output():
    out = "@@W1@@\n中文一\n\n> **EN 原声（译文）**：翻译\n\n@@W2@@\n中文二"
    got = dt.parse_merge_output(out, 2)
    assert "中文一" in got[0] and "翻译" in got[0]
    assert got[1].strip() == "中文二"
    # missing marker -> empty slot
    got2 = dt.parse_merge_output("@@W1@@\n只有一", 2)
    assert got2[1] == ""


def test_assemble_interleaved_format():
    windows = [
        {"start": 320, "end": 370, "zh": [], "en": []},
        {"start": 370, "end": 422, "zh": [], "en": []},
    ]
    bodies = ["第一窗内容\n\n> **EN 原声（译文）**：foo", ""]
    out = dt.assemble(windows, bodies, "# 元信息\n---\n")
    assert "## [05:20 - 06:10]" in out
    assert "## [06:10 - 07:02]" not in out  # empty body window skipped
    assert out.startswith("# 元信息")
    assert "**EN 原声（译文）**：foo" in out


def test_fmt_mmss():
    assert dt.fmt_mmss(320) == "05:20"
    assert dt.fmt_mmss(0) == "00:00"
    assert dt.fmt_mmss(3661) == "61:01"
