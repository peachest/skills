"""slides-extract.py / merge-slides.py — pure-function tests."""

import importlib.util
from pathlib import Path

import pytest


def load(name):
    script = Path(__file__).parent.parent / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_").replace(".py", ""), script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


se = load("slides-extract.py")
ms = load("merge-slides.py")


# ── slides-extract ──

def test_parse_showinfo_pts():
    stderr = (
        '[Parsed_showinfo_1 @ 0x55] n:   0 pts:12345 pts_time:12.345\n'
        '[Parsed_showinfo_1 @ 0x55] n:   1 pts:23456 pts_time:23.456\n'
    )
    assert se.parse_showinfo_pts(stderr) == [12.345, 23.456]


def test_parse_showinfo_pts_empty():
    assert se.parse_showinfo_pts("no showinfo here") == []


def test_dhash_stable_and_different():
    import io
    from PIL import Image
    a = Image.new("L", (64, 64), 0)
    # half-black / half-white split → strong horizontal gradient
    for x in range(32, 64):
        for y in range(64):
            a.putpixel((x, y), 255)
    b = Image.new("L", (64, 64), 0)
    for x in range(0, 32):
        for y in range(64):
            b.putpixel((x, y), 255)
    ha, hb = se.dhash(a), se.dhash(b)
    assert ha == se.dhash(a)          # deterministic
    assert se.hamming(ha, hb) > 8     # mirror images differ substantially


def test_dedup_adjacent_keeps_first_of_run():
    from PIL import Image

    def split_img(vertical: bool) -> Image.Image:
        img = Image.new("L", (32, 32), 0)
        px = img.load()
        for x in range(32):
            for y in range(32):
                if (x >= 16) if vertical else (y >= 16):
                    px[x, y] = 255
        return img

    import tempfile
    frames = []
    with tempfile.TemporaryDirectory() as d:
        for i, vertical in enumerate([True, True, False]):
            p = Path(d) / f"f{i}.jpg"
            split_img(vertical).save(p)
            frames.append({"file": str(p), "time_sec": float(i)})
        kept = se.dedup_adjacent(frames, threshold=8)
    assert len(kept) == 2  # A, A, B → A + B
    assert kept[0]["time_sec"] == 0.0 and kept[1]["time_sec"] == 2.0


def test_timecode():
    assert se.timecode(0) == "00:00"
    assert se.timecode(155) == "02:35"
    assert se.timecode(3725) == "62:05"


# ── merge-slides ──

SEGS = [
    {"start": 0.0, "end": 5.0, "text": "开场介绍"},
    {"start": 6.0, "end": 10.0, "text": "第二句话"},
    {"start": 150.0, "end": 155.0, "text": "讲到重点了"},
]


def test_format_timeline_interleaves_slides():
    slides = [
        {"time_sec": 155.0, "text": "架构图：三阶段流水线"},
        {"time_sec": 7.0, "text": "[非幻灯片]"},  # filtered by usable_slides
    ]
    out = ms.format_timeline(SEGS, ms.usable_slides(slides))
    assert "**[00:00]** 开场介绍 第二句话" in out
    assert "## [02:35 幻灯片]" in out
    assert "架构图" in out
    # slide at 155s lands after the segment that spans 150–155
    assert out.index("## [02:35 幻灯片]") > out.index("讲到重点了")
    assert "[非幻灯片]" not in out


def test_format_timeline_no_slides():
    out = ms.format_timeline(SEGS, [])
    assert "幻灯片" not in out
    assert "讲到重点了" in out


def test_format_timeline_slide_at_zero():
    out = ms.format_timeline(SEGS, [{"time_sec": 0.0, "text": "封面标题页"}])
    assert out.startswith("## [00:00 幻灯片]")


def test_usable_slides_filters_errors():
    slides = [
        {"time_sec": 1.0, "text": ""},
        {"time_sec": 2.0, "text": "[非幻灯片]"},
        {"time_sec": 3.0, "text": "error: timeout"},
        {"time_sec": 4.0, "text": "真实内容"},
    ]
    assert [s["text"] for s in ms.usable_slides(slides)] == ["真实内容"]


def test_transcript_body_splits_divider():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "transcript.md"
        p.write_text("# 转录结果\n\n| 字段 | 值 |\n\n---\n\n正文内容", encoding="utf-8")
        assert ms.transcript_body(p) == "正文内容"


def test_upscale_2x(tmp_path):
    from PIL import Image
    src = tmp_path / "f.jpg"
    Image.new("RGB", (10, 8), "white").save(src)
    out = se.upscale(str(src))
    assert Path(out).exists() and Path(out) != src
    assert Image.open(out).size == (20, 16)
    Path(out).unlink()


def test_upscale_missing_source(tmp_path):
    import PIL
    with pytest.raises(FileNotFoundError):
        se.upscale(str(tmp_path / "nope.jpg"))
