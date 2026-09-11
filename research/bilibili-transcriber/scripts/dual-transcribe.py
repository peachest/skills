#!/usr/bin/env python3
"""dual-transcribe.py — bilingual dual-audio transcript reconciliation.

For videos whose audio mixes the original English voice with a condensed
Chinese voice-over dub (96 of our corpus), a single zh-hinted ASR pass
bleeds both languages into one messy text. This pipeline reconciles:

  1. zh side: reuse the existing workspace chunk JSONs (zh-hinted pass;
     per-segment timestamps, chunk-relative -> global offsets applied).
  2. en side: re-run transcribe.sh with WHISPER_LANG=en in a scratch root
     (symlinked audio, CWD=scratch so references never collide), harvest
     its chunk JSONs into <ws>/faster-whisper-en/.
  3. align both segment timelines into ~90s windows (interval overlap,
     slack for dub lag).
  4. LLM merge (OpenAI-compatible endpoint): clean the zh side, translate
     the en side, flag divergences -> [对照存疑].
  5. assemble the interleaved transcript.md the user chose:

         ## [mm:ss - mm:ss]
         zh cleaned paragraphs
         > **EN 原声（译文）**： ... (blockquote)
         `[对照存疑： ...]` (when flagged)

     previous mixed text is preserved as transcript.mixed.md.

Resumable per video: stage markers in <transcript-dir>/dual-state.json.
Usage:
  dual-transcribe.py <targets.json> [--concurrency 8] [--window-sec 90]
targets.json: [{"dir": "<transcript dir>", "workspace": "<ws dir>", "title": ...}, ...]
Config via runtime.conf (same as clean-transcripts.py): CLEAN_LLM_* keys.
"""

import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# aiohttp imported lazily in the async entrypoints so the pure functions
# (segments/windows/assembly) stay importable without it — see tests.

SKILL_DIR = Path(__file__).resolve().parent.parent
TRANSCRIBE_SH = SKILL_DIR / "scripts" / "transcribe.sh"


# ────────────────────── segment loading ──────────────────────

def load_segments(chunks_dir: Path) -> list[dict]:
    """Load chunk JSONs into one globally-timestamped segment list.
    Chunk timestamps are chunk-relative; global offset = cumulative
    last-segment-end of previous chunks. Direct mode (no chunking) writes a
    single direct.json with already-global timestamps."""
    files = sorted(chunks_dir.glob("chunk_*.json"))
    if not files:
        direct = chunks_dir / "direct.json"
        if direct.is_file():
            data = json.loads(direct.read_text(encoding="utf-8"))
            return [s for s in (
                {"start": x["start"], "end": x["end"], "text": x["text"].strip()}
                for x in data.get("segments", [])) if s["text"]]
        return []
    segs, offset = [], 0.0
    for f in sorted(chunks_dir.glob("chunk_*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        chunk_segs = data.get("segments", [])
        if not chunk_segs:
            continue
        for s in chunk_segs:
            segs.append({
                "start": s["start"] + offset,
                "end": s["end"] + offset,
                "text": s["text"].strip(),
            })
        offset += chunk_segs[-1]["end"]
    return [s for s in segs if s["text"]]


def is_en(text: str) -> bool:
    if not text:
        return False
    return sum(1 for c in text if ord(c) < 128) / len(text) > 0.7


# ────────────────────── alignment ──────────────────────

def group_windows(zh: list[dict], en: list[dict], window_sec: float) -> list[dict]:
    """Cut [0, total] into windows of ~window_sec. Each window carries the
    zh segments and en segments overlapping it. Segments straddling a
    boundary go to the window containing their midpoint."""
    if not zh and not en:
        return []
    total = max((s["end"] for s in zh + en), default=0)
    windows = []
    t = 0.0
    while t < total:
        t2 = min(t + window_sec, total)
        w = {"start": t, "end": t2, "zh": [], "en": []}
        for s in zh:
            mid = (s["start"] + s["end"]) / 2
            if t <= mid < t2 or (t2 == total and mid >= t):
                w["zh"].append(s)
        for s in en:
            mid = (s["start"] + s["end"]) / 2
            if t <= mid < t2 or (t2 == total and mid >= t):
                w["en"].append(s)
        windows.append(w)
        t = t2
    return windows


def classify_window(w: dict) -> str:
    """pair | en_only | zh_only | empty"""
    has_zh = any(not is_en(s["text"]) for s in w["zh"])
    has_en = bool(w["en"]) or any(is_en(s["text"]) for s in w["zh"])
    if has_zh and has_en:
        return "pair"
    if has_en:
        return "en_only"
    if has_zh:
        return "zh_only"
    return "empty"


# ────────────────────── LLM merge ──────────────────────

MERGE_PROMPT = """你是双语音频转录整合助手。下面是同一个视频同一段时间窗口内的两条 ASR 原文：
- 【中文配音】：来自中文配音音轨（可能有同音字错误、无标点、口语化）
- 【英文原声】：来自英文原声音轨（ASR 可能有小错误）

对每个窗口输出（用 @@W{{n}}@@ 行分隔，严格遵守）：
@@W{{n}}@@
<中文配音部分：修正错别字与 ASR 误听（可参照英文原声确认专有名词，如人名/地名/术语）；加中文标点；按语义分段；逐句对应，不删除不概括>
> **EN 原声（译文）**：<英文原声完整翻译成流畅中文，忠实不缩写；若本窗口无英文原声则此行省略>
`[对照存疑： <实质性分歧与修正记录：配音跳过/省略的句子、语义冲突、已参照原声修正的误听项，一行>]`（无分歧且无修正则省略此行）

窗口数据：
{windows}"""


def fmt_mmss(t: float) -> str:
    m, s = int(t) // 60, int(t) % 60
    return f"{m:02d}:{s:02d}"


def build_merge_input(windows: list[dict]) -> str:
    parts = []
    for i, w in enumerate(windows, 1):
        zh_txt = "\n".join(s["text"] for s in w["zh"]) or "（无）"
        en_txt = "\n".join(s["text"] for s in w["en"]) or "（无）"
        parts.append(f"### 窗口{i} [{fmt_mmss(w['start'])}-{fmt_mmss(w['end'])}]\n【中文配音】\n{zh_txt}\n\n【英文原声】\n{en_txt}")
    return "\n\n".join(parts)


def parse_merge_output(out: str, n: int) -> list[str]:
    """Split the LLM reply on @@W{n}@@ markers; tolerate missing markers."""
    pieces = re.split(r"^@@W(\d+)@@\s*$", out, flags=re.M)
    # pieces = [pre, n1, body1, n2, body2, ...]
    bodies = {}
    for i in range(1, len(pieces) - 1, 2):
        try:
            bodies[int(pieces[i])] = pieces[i + 1].strip()
        except ValueError:
            continue
    return [bodies.get(i, "") for i in range(1, n + 1)]


# ────────────────────── assembly ──────────────────────

def assemble(windows: list[dict], merged_bodies: list[str], header_meta: str) -> str:
    lines = [header_meta, ""]
    for w, body in zip(windows, merged_bodies):
        if not body:
            continue
        lines.append(f"## [{fmt_mmss(w['start'])} - {fmt_mmss(w['end'])}]")
        lines.append("")
        lines.append(body.strip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ────────────────────── per-video pipeline ──────────────────────

def read_state(tdir: Path) -> dict:
    f = tdir / "dual-state.json"
    return json.loads(f.read_text()) if f.is_file() else {}


def write_state(tdir: Path, **kv):
    st = read_state(tdir)
    st.update(kv)
    (tdir / "dual-state.json").write_text(json.dumps(st, ensure_ascii=False, indent=1))


def run_en_pass(ws: Path) -> bool:
    """Run transcribe.sh with WHISPER_LANG=en in a scratch root; harvest
    chunk JSONs into ws/faster-whisper-en/. Returns success."""
    dest = ws / "faster-whisper-en"
    if (dest / "chunks" / "transcripts").is_dir() and list((dest / "chunks" / "transcripts").glob("chunk_*.json")):
        return True  # harvested previously
    scratch = ws.parent / f"{ws.name}-enroot"
    ws_en = scratch / ws.name
    ws_en.mkdir(parents=True, exist_ok=True)
    # symlink audio, copy metadata (transcribe.sh needs audio.mp4)
    audio = ws_en / "audio.mp4"
    if not audio.exists():
        audio.symlink_to(ws / "audio.mp4")
    meta_src = ws / "metadata.json"
    if meta_src.is_file() and not (ws_en / "metadata.json").is_file():
        shutil.copy(meta_src, ws_en / "metadata.json")
    env = dict(os.environ, WHISPER_LANG="en")
    r = subprocess.run(
        ["bash", str(TRANSCRIBE_SH), ws_en.name],
        cwd=scratch, env=env, stdin=subprocess.DEVNULL,
        capture_output=True, text=True, timeout=7200,
    )
    src = ws_en / "faster-whisper" / "chunks" / "transcripts"
    ok = r.returncode == 0 and src.is_dir() and \
        (list(src.glob("chunk_*.json")) or (src / "direct.json").is_file())
    if not ok:
        print(f"[en-pass-err] {ws.name}: rc={r.returncode} "
              f"{(r.stderr or r.stdout or '')[-400:]}", flush=True)
    if ok:
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dest / "chunks" / "transcripts", dirs_exist_ok=True)
    shutil.rmtree(scratch, ignore_errors=True)
    return bool(ok)


def load_conf() -> dict:
    conf = {
        "CLEAN_LLM_BASEURL": os.environ.get("CLEAN_LLM_BASEURL", ""),
        "CLEAN_LLM_MODEL": os.environ.get("CLEAN_LLM_MODEL", ""),
        "CLEAN_LLM_KEY": os.environ.get("CLEAN_LLM_KEY", ""),
        "CLEAN_LLM_EFFORT": os.environ.get("CLEAN_LLM_EFFORT", ""),
    }
    rc = SKILL_DIR / "runtime.conf"
    if rc.is_file():
        for line in rc.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k in conf and not conf[k]:
                conf[k] = v
    if not conf["CLEAN_LLM_BASEURL"] or not conf["CLEAN_LLM_MODEL"]:
        sys.exit("FAIL missing CLEAN_LLM_* config")
    return conf


async def llm_merge_batch(sess, conf, windows: list[dict], sem) -> list[str]:
    """Merge a batch of windows in one LLM call."""
    import aiohttp
    payload = {
        "model": conf["CLEAN_LLM_MODEL"],
        "messages": [{"role": "user", "content": MERGE_PROMPT.format(windows=build_merge_input(windows))}],
        "temperature": 0.0,
        "max_tokens": 32000,
    }
    # GLM-5.3 reasoning knob: thinking cannot be disabled; low effort is the
    # only speed lever (5.5x measured). Omitted for non-glm53 models.
    if conf.get("CLEAN_LLM_EFFORT"):
        payload["chat_template_kwargs"] = {"reasoning_effort": conf["CLEAN_LLM_EFFORT"]}
    headers = {"Content-Type": "application/json"}
    if conf["CLEAN_LLM_KEY"]:
        headers["Authorization"] = f"Bearer {conf['CLEAN_LLM_KEY']}"
    url = conf["CLEAN_LLM_BASEURL"].rstrip("/") + "/chat/completions"
    async with sem:
        for attempt in range(3):
            try:
                async with sess.post(url, json=payload, headers=headers,
                                     timeout=aiohttp.ClientTimeout(total=300)) as r:
                    if r.status != 200:
                        raise RuntimeError(f"HTTP {r.status}")
                    out = (await r.json())["choices"][0]["message"]["content"].strip()
                return parse_merge_output(out, len(windows))
            except Exception:
                if attempt == 2:
                    raise
                await asyncio.sleep(3 * (attempt + 1))


async def process_target(item: dict, sess, conf, args, sem, asr_sem, stats, lock):
    tdir, ws = Path(item["dir"]), Path(item["workspace"])
    if read_state(tdir).get("merged"):
        return
    # 1. en pass — ASR must stay single-stream (shared whisper service)
    def _en():
        return run_en_pass(ws)
    async with asr_sem:
        ok_en = await asyncio.to_thread(_en)
    if not ok_en:
        async with lock:
            stats["failed"].append({"dir": str(tdir), "error": "en pass failed"})
        print(f"[FAILED] {tdir.name}: en ASR pass failed", flush=True)
        return
    write_state(tdir, en_done=True)
    # 2. load segments
    zh = load_segments(ws / "faster-whisper" / "chunks" / "transcripts")
    en = load_segments(ws / "faster-whisper-en" / "chunks" / "transcripts")
    windows = [w for w in group_windows(zh, en, args.window_sec) if classify_window(w) != "empty"]
    if not windows:
        async with lock:
            stats["failed"].append({"dir": str(tdir), "error": "no segments"})
        return
    # 3. LLM merge in batches of 4 windows
    bodies: list[str] = []
    for i in range(0, len(windows), 4):
        batch = windows[i:i + 4]
        got = await llm_merge_batch(sess, conf, batch, sem)
        # per-window sanity: zh part non-empty for pair/zh_only windows
        for w, b in zip(batch, got):
            if classify_window(w) in ("pair", "zh_only") and len(b) < 10:
                b = "".join(s["text"] for s in w["zh"])  # fallback: raw concat
        bodies.extend(got)
    # 4. assemble + swap files — transcript.mixed.md keeps the FIRST pre-dual
    # text (never overwrite: a re-merge must not replace the original backup)
    old = (tdir / "transcript.md")
    text = old.read_text(encoding="utf-8") if old.is_file() else ""
    header = "# 双语对照转录\n\n" if not text else text.split("---")[0].rstrip() + "\n---\n"
    out = assemble(windows, bodies, header)
    if old.is_file() and not (tdir / "transcript.mixed.md").is_file():
        (tdir / "transcript.mixed.md").write_text(text, encoding="utf-8")
    old.write_text(out, encoding="utf-8")
    write_state(tdir, merged=True)
    async with lock:
        stats["ok"] += 1
    print(f"[ok] {tdir.name}: {len(windows)} windows", flush=True)


async def main() -> int:
    import aiohttp
    ap = argparse.ArgumentParser()
    ap.add_argument("targets")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--asr-workers", type=int, default=1)
    ap.add_argument("--window-sec", type=float, default=90)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    targets = json.loads(Path(args.targets).read_text(encoding="utf-8"))
    if args.limit:
        targets = targets[: args.limit]
    conf = load_conf()
    stats = {"ok": 0, "failed": []}
    lock = asyncio.Lock()
    sem = asyncio.Semaphore(args.concurrency)      # LLM calls
    asr_sem = asyncio.Semaphore(args.asr_workers)  # whisper passes
    t0 = time.time()
    async with aiohttp.ClientSession() as sess:
        async def run_one(item):
            try:
                await process_target(item, sess, conf, args, sem, asr_sem, stats, lock)
            except Exception as e:
                async with lock:
                    stats["failed"].append({"dir": item["dir"], "error": str(e)[:300]})
                print(f"[FAILED] {Path(item['dir']).name}: {e}", flush=True)

        await asyncio.gather(*(run_one(t) for t in targets))

    print(f"DUAL DONE: ok={stats['ok']} failed={len(stats['failed'])} elapsed={time.time()-t0:.0f}s")
    if stats["failed"]:
        Path("dual-failures.json").write_text(json.dumps(stats["failed"], ensure_ascii=False, indent=1))
    return 0 if not stats["failed"] else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
