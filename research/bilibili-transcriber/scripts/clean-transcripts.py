#!/usr/bin/env python3
"""clean-transcripts.py — Step 3 (LLM cleanup) automation for the transcriber.

Cleans raw ASR transcripts (no punctuation, homophone errors) into readable
Chinese text via an OpenAI-compatible chat endpoint. Per-transcript flow:

  read transcript.md -> backup to transcript.raw.md -> chunk body (~3000
  chars, split at natural boundaries) -> clean each chunk with the LLM ->
  validate length (+/-25% per chunk; rejects silent truncation/summarizing)
  -> write metadata table + cleaned body back to transcript.md.

Resumable: a transcript is skipped when transcript.raw.md already exists
(i.e. it has been through this script). Failures leave transcript.raw.md
absent so a rerun retries them.

Config (env or runtime.conf in the script's skill dir):
  CLEAN_LLM_BASEURL  OpenAI-compatible base URL (e.g. http://host:8000/v1)
  CLEAN_LLM_MODEL    model id
  CLEAN_LLM_KEY      api key (optional)

Usage:
  clean-transcripts.py <manifest.json>          # items: [{"dir": ...}, ...]
  clean-transcripts.py <transcript-dir> ...     # one or more transcript dirs
Options: --concurrency 8 --chunk-chars 3000 --limit N --dry-run
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path


import aiohttp

DIVIDER = re.compile(r"^---\s*$", re.M)


def load_conf() -> dict:
    conf = {
        "CLEAN_LLM_BASEURL": os.environ.get("CLEAN_LLM_BASEURL", ""),
        "CLEAN_LLM_MODEL": os.environ.get("CLEAN_LLM_MODEL", ""),
        "CLEAN_LLM_KEY": os.environ.get("CLEAN_LLM_KEY", ""),
        "CLEAN_LLM_FALLBACK": os.environ.get("CLEAN_LLM_FALLBACK", ""),
        "CLEAN_LLM_EFFORT": os.environ.get("CLEAN_LLM_EFFORT", ""),
    }
    rc = Path(__file__).resolve().parent.parent / "runtime.conf"
    if rc.is_file():
        for line in rc.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k in conf and not conf[k]:
                conf[k] = v
    missing = [k for k in ("CLEAN_LLM_BASEURL", "CLEAN_LLM_MODEL") if not conf[k]]
    if missing:
        sys.exit(f"FAIL missing config: {missing} (env or runtime.conf)")
    return conf


def split_body(text: str) -> tuple[str, str]:
    """Return (header, body): header is everything up to and including the
    last standalone `---` divider line; body is the rest."""
    matches = list(DIVIDER.finditer(text))
    if not matches:
        return "", text
    last = matches[-1]
    return text[: last.end()], text[last.end():].strip()


def chunk(text: str, size: int) -> list[str]:
    """Split at ~size chars, adjusted to the nearest newline/space before it."""
    out = []
    i = 0
    while i < len(text):
        j = min(i + size, len(text))
        if j < len(text):
            window = text[i:j]
            cut = max(window.rfind("\n"), window.rfind(" "))
            if cut > size // 2:
                j = i + cut + 1
        out.append(text[i:j].strip())
        i = j
    return [c for c in out if c]


PROMPT_TMPL = (
    "你是中文技术/科普演讲转录校对助手。\n"
    "主题：{title}\n\n"
    "规则：\n"
    "1. 修正同音字/错别字错误（结合主题语境，如专业术语、人名、产品名）\n"
    "2. 添加中文标点符号\n"
    "3. 在语义自然处分段（段落间空一行）\n"
    "4. 不要改变原意，不要添加信息，不要删除内容，不要总结或缩写\n"
    "5. 输出必须逐句对应原文，字符数与输入基本相同（标点约占额外 10-15%），"
    "不得跳过、概括或合并任何句子\n"
    "6. 直接输出校对后的文本——不要任何前言、解释、编号或代码块标记\n\n"
    "原始文本：\n{raw}"
)


async def clean_one_chunk(sess, conf, title, raw, sem, retries=3, model=None, temp=0.0, fp=0.3):
    async with sem:
        payload = {
            "model": model or conf["CLEAN_LLM_MODEL"],
            "messages": [{"role": "user", "content": PROMPT_TMPL.format(title=title, raw=raw)}],
            "temperature": temp,
            "frequency_penalty": fp,
            "max_tokens": 32000,
        }
        # GLM-5.3 reasoning knob: thinking cannot be disabled; low effort is
        # the only speed lever (5.5x measured). Harmless to omit for flash.
        if conf.get("CLEAN_LLM_EFFORT"):
            payload["chat_template_kwargs"] = {"reasoning_effort": conf["CLEAN_LLM_EFFORT"]}
        headers = {"Content-Type": "application/json"}
        if conf["CLEAN_LLM_KEY"]:
            headers["Authorization"] = f"Bearer {conf['CLEAN_LLM_KEY']}"
        url = conf["CLEAN_LLM_BASEURL"].rstrip("/") + "/chat/completions"
        for attempt in range(retries):
            try:
                async with sess.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=300)) as r:
                    if r.status != 200:
                        raise RuntimeError(f"HTTP {r.status}: {(await r.text())[:200]}")
                    data = await r.json()
                    out = data["choices"][0]["message"]["content"].strip()
                    if out.startswith("```"):
                        out = out.strip("`").lstrip("\n")
                    return out
            except Exception:
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(2 * (attempt + 1))


def is_cleaned(d: Path) -> bool:
    # transcript.raw.md = went through this script; dual-state merged = went
    # through dual-transcribe.py (interleaved bilingual format — must not be
    # re-"cleaned" as plain text)
    return (d / "transcript.raw.md").is_file() or \
        ((d / "dual-state.json").is_file() and
         json.loads((d / "dual-state.json").read_text(encoding="utf-8")).get("merged"))


async def _clean_with_ladder(sess, conf, title, raw, args):
    """Escalation ladder for a failing chunk:
    1. primary model, full chunk (lo, hi ratio)
    2. primary model, chunk split in half (looser ratio per half)
    3. fallback model (glm reasoning, slow), bilingual-lenient ratio
    Returns (cleaned text or None, used_fallback). Rationale: flash models
    deterministically repetition-loop on some dense philosophical chunks
    (boom) and compress bilingual dual-audio chunks (loss); halving breaks
    loops, the reasoning fallback handles bilingual audio where one track
    is inevitably folded."""
    fallback = conf.get("CLEAN_LLM_FALLBACK", "")
    out = await clean_one_chunk(sess, conf, title, raw, args._sem)
    if 0.75 * len(raw) <= len(out) <= 1.25 * len(raw):
        return out, False
    halves = chunk(raw, max(200, len(raw) // 2))
    outs = []
    for h in halves:
        o = await clean_one_chunk(sess, conf, title, h, args._sem)
        if not (0.70 * len(h) <= len(o) <= 1.30 * len(h)):
            outs = []
            break
        outs.append(o)
    if outs:
        return "\n\n".join(outs), False
    # sampling escape: flash models deterministically repetition-loop on some
    # dense chunks at temp 0; high-temp + strong freq penalty breaks the loop
    for temp, fp, lo, hi in ((0.7, 0.6, 0.75, 1.25), (1.0, 0.8, 0.75, 1.30)):
        out = await clean_one_chunk(sess, conf, title, raw, args._sem, temp=temp, fp=fp)
        if lo * len(raw) <= len(out) <= hi * len(raw):
            return out, False
    if fallback:
        out = await clean_one_chunk(sess, conf, title, raw, args._sem, model=fallback)
        if 0.60 * len(raw) <= len(out) <= 1.50 * len(raw):
            return out, True
    return None, False


async def clean_transcript(d: Path, sess, conf, args, stats, stats_lock) -> bool:
    tp = d / "transcript.md"
    if not tp.is_file():
        return False
    if is_cleaned(d):
        return True  # already done
    text = tp.read_text(encoding="utf-8")
    header, body = split_body(text)
    if not body:
        return False
    chunks = chunk(body, args.chunk_chars)
    cleaned_parts = []
    for idx, c in enumerate(chunks):
        out, used_fb = await _clean_with_ladder(sess, conf, d.name, c, args)
        if out is None:
            raise RuntimeError(
                f"ladder exhausted: chunk {idx + 1}/{len(chunks)} raw={len(c)}"
            )
        cleaned_parts.append(out)
        if used_fb:
            print(f"[warn] {d.name}: chunk {idx + 1} needed fallback model", flush=True)
    if args.dry_run:
        print(f"[dry-run] {d.name}: {len(chunks)} chunks OK")
        return True
    (d / "transcript.raw.md").write_text(text, encoding="utf-8")
    tp.write_text(header.rstrip("\n") + "\n\n" + "\n\n".join(cleaned_parts) + "\n", encoding="utf-8")
    async with stats_lock:
        stats["ok"] += 1
        stats["chars"] += len(body)
    print(f"[ok] {d.name} ({len(chunks)} chunks, {len(body)} chars)", flush=True)
    return True


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+", help="manifest.json or transcript dirs")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--chunk-chars", type=int, default=3000)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    args._sem = asyncio.Semaphore(args.concurrency)

    dirs: list[Path] = []
    for t in args.targets:
        p = Path(t)
        if p.suffix == ".json":
            for item in json.loads(p.read_text(encoding="utf-8")):
                dirs.append(Path(item["dir"]))
        else:
            dirs.append(p)
    if args.limit:
        dirs = dirs[: args.limit]

    conf = load_conf()
    todo = [d for d in dirs if not is_cleaned(d)]
    print(f"{len(dirs)} listed, {len(dirs) - len(todo)} already cleaned, {len(todo)} to clean")

    stats = {"ok": 0, "chars": 0, "failed": []}
    stats_lock = asyncio.Lock()
    t0 = time.time()
    async with aiohttp.ClientSession() as sess:
        async def run_one(d):
            try:
                await clean_transcript(d, sess, conf, args, stats, stats_lock)
            except Exception as e:
                async with stats_lock:
                    stats["failed"].append({"dir": str(d), "error": str(e)[:300]})
                print(f"[FAILED] {d.name}: {e}", flush=True)

        await asyncio.gather(*(run_one(d) for d in todo))

    print(f"CLEAN DONE: ok={stats['ok']} failed={len(stats['failed'])} "
          f"chars={stats['chars']} elapsed={time.time() - t0:.0f}s")
    if stats["failed"]:
        out = Path("clean-failures.json")
        out.write_text(json.dumps(stats["failed"], ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"failures -> {out.resolve()}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
