#!/usr/bin/env python3
"""merge-slides.py — merge ASR transcript + extracted slides into one markdown.

Output (transcript.final.md in the video's transcript dir):
  ## 文稿                  — cleaned transcript (or raw blob when uncleaned)
  ## 时间轴（幻灯片穿插）   — raw ASR segments grouped into timestamped paragraphs,
                             each slide's OCR text inserted at its timeline
                             position as `## [mm:ss 幻灯片]`

Inputs (all discovered from the workspace):
  <workspace>/metadata.json                        — title/bvid
  <workspace>/slides/slides.json                   — slides-extract.py output
  <project-root>/references/transcripts/**/<bvid>*/ — transcript.md + chunks

Usage (from the project root, like transcribe.sh):
  uv run python scripts/merge-slides.py <workspace-dir>
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DIVIDER = re.compile(r"^---\s*$", re.M)


def timecode(sec: float) -> str:
    s = int(sec)
    return f"{s // 60:02d}:{s % 60:02d}"


def load_segments(workspace: Path) -> list[dict]:
    """Harvest verbose_json segments from <workspace>/<method>/chunks/transcripts/*.json."""
    segs: list[dict] = []
    for jf in sorted(workspace.glob("*/chunks/transcripts/*.json")):
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        segs.extend(data.get("segments") or [])
    return sorted(segs, key=lambda s: s.get("start", 0))


def transcript_body(md_path: Path) -> str:
    """Body text below the header table + --- divider of transcript.md."""
    text = md_path.read_text(encoding="utf-8")
    parts = DIVIDER.split(text, maxsplit=1)
    return parts[1].strip() if len(parts) == 2 else text.strip()


def usable_slides(slides: list[dict]) -> list[dict]:
    """Slide blocks worth interleaving: real OCR text, not a non-slide shot."""
    out = []
    for s in slides:
        t = (s.get("text") or "").strip()
        if t and t != "[非幻灯片]" and not t.startswith("error"):
            out.append(s)
    return out


def format_timeline(segments: list[dict], slides: list[dict]) -> str:
    """Timestamped paragraphs of ASR text with slide blocks interleaved.
    Paragraph boundary: >3s gap between segments or ~40s of accumulated text."""
    by_time = sorted(slides, key=lambda s: s["time_sec"])
    lines: list[str] = []
    para: list[str] = []
    para_start: float | None = None
    para_end: float = 0.0

    def flush():
        nonlocal para, para_start
        if para:
            lines.append(f"**[{timecode(para_start)}]** " + " ".join(para))
            lines.append("")
            para, para_start = [], None

    for seg in segments:
        st, txt = float(seg.get("start", 0)), (seg.get("text") or "").strip()
        if not txt:
            continue
        # slides starting before this segment get inserted first
        while by_time and by_time[0]["time_sec"] <= st:
            flush()
            s = by_time.pop(0)
            lines.append(f"## [{timecode(s['time_sec'])} 幻灯片]")
            lines.append("")
            lines.append(s["text"].strip())
            lines.append("")
        gap = st - para_end > 3.0 if para_end else True
        length = sum(len(p) for p in para)
        if para_start is None or gap or length > 400:
            flush()
            para_start = st
        para.append(txt)
        para_end = float(seg.get("end", st))
    while by_time:
        flush()
        s = by_time.pop(0)
        lines.append(f"## [{timecode(s['time_sec'])} 幻灯片]")
        lines.append("")
        lines.append(s["text"].strip())
        lines.append("")
    flush()
    return "\n".join(lines).strip()


def build_manifest(workspace: Path, td: Path) -> list[tuple[str, str, Path]]:
    """(artifact, producer, path) rows for the report manifest table."""
    rows = [
        ("元数据", "fetch-article (bilibili adapter)", workspace / "metadata.json"),
        ("视频上下文（简介+评论）", "fetch-article (bilibili adapter)", workspace / "context.md"),
        ("原始 ASR segments", "chunk_transcribe.py", workspace / "chunks" / "transcripts"),
        ("转写稿", "transcribe.sh", td / "transcript.md"),
        ("清洗前留档", "clean-transcripts.py", td / "transcript.raw.md"),
        ("LLM 改写日志", "clean/dual/reclean", td / "llm-changes.jsonl"),
        ("幻灯片 OCR", "slides-extract.py", workspace / "slides" / "slides.json"),
        ("融合稿", "merge-slides.py", td / "transcript.final.md"),
    ]
    return rows


def render_report(workspace: Path, td: Path, title: str, final_body: str) -> str:
    lines = [f"# {title}", "",
             "## 产物清单（追溯用）", "",
             "| 产物 | 生成者 | 状态 |", "|---|---|---|"]
    for name, producer, path in build_manifest(workspace, td):
        status = f"存在（{path.stat().st_size // 1024}KB）" if path.is_file() or path.is_dir() else "未生成"
        lines.append(f"| {name} | {producer} | {status} |")
    lines += ["", "---", "", final_body, ""]
    ctx = workspace / "context.md"
    if ctx.is_file():
        ctx_body = ctx.read_text(encoding="utf-8")
        ctx_body = ctx_body.split("\n", 1)[1] if ctx_body.startswith("# ") else ctx_body
        snap = datetime.fromtimestamp(ctx.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        lines += ["---", "", f"## 附录：视频上下文（简介与评论）· 快照于 {snap}", "", ctx_body.strip(), ""]
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} <workspace-dir> [--transcript-dir <dir>]")
    workspace = Path(sys.argv[1])
    if not workspace.is_dir():
        sys.exit(f"FAIL workspace not found: {workspace}")
    args = sys.argv[2:]
    if "--transcript-dir" in args:
        i = args.index("--transcript-dir")
        td = Path(args[i + 1]) if i + 1 < len(args) else None
        if not td or not td.is_dir():
            sys.exit(f"FAIL --transcript-dir not a directory: {td}")
    else:
        # no silent cwd-dependent fallback: state the expectation and fail
        meta0 = json.loads((workspace / "metadata.json").read_text(encoding="utf-8"))
        sys.exit(f"FAIL --transcript-dir required (expected the "
                 f"references/transcripts/**/{meta0.get('bvid', '?')} dir "
                 f"written by transcribe.sh; cwd-dependent lookup removed)")
    meta = json.loads((workspace / "metadata.json").read_text(encoding="utf-8"))
    bvid = meta.get("bvid", "")
    title = meta.get("title", bvid)
    slides_path = workspace / "slides" / "slides.json"
    if not slides_path.is_file():
        sys.exit("FAIL no slides/slides.json — run slides-extract.py first")
    slides = json.loads(slides_path.read_text(encoding="utf-8"))

    segments = load_segments(workspace)
    if not segments:
        sys.exit(f"FAIL no verbose_json segments under {workspace}/*/chunks/transcripts/")

    out = [f"# {title}", ""]
    cleaned = td / "transcript.md"
    if cleaned.is_file():
        out += ["## 文稿", "", transcript_body(cleaned), ""]
        src = "cleaned transcript.md"
    else:
        raw = next(iter(sorted(workspace.glob("*/transcript.md"))), None)
        if raw:
            out += ["## 文稿", "", transcript_body(raw), ""]
            src = "raw transcript"
        else:
            src = "(no transcript.md found)"
    out += ["## 时间轴（幻灯片穿插）", ""]
    body = format_timeline(segments, usable_slides(slides))
    out += [body, ""]

    dest = td / "transcript.final.md"
    dest.write_text("\n".join(out), encoding="utf-8")
    report = td / "report.md"
    report.write_text(render_report(workspace, td, title, "\n".join(out)), encoding="utf-8")
    used = len(usable_slides(slides))
    print(f"done: {dest}")
    print(f"  report     : {report}")
    print(f"  transcript source: {src}; segments: {len(segments)}; slides interleaved: {used}/{len(slides)}")


if __name__ == "__main__":
    main()
