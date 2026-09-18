#!/usr/bin/env python3
"""reclean-en.py — re-clean a garbled zh ASR transcript against the original
English transcript (e.g. YouTube auto-subs of the same video).

For zh-dubbed videos with mixed English speech, plain ASR cleanup cannot fix
mangled proper nouns and terminology. This script feeds the raw ASR transcript
AND the English reference to the cleanup LLM per aligned chunk and rebuilds
each sentence from the English text.

Usage:
  python3 reclean-en.py <raw-transcript.(md|txt)> <english-reference.txt> \
      [--glossary glossary.txt] [--concurrency 3] [--chunk-chars 3000] [--out PATH]

Input raw transcript may be a clean-transcripts.py backup (transcript.raw.md,
header table before a --- divider) or plain ASR text.
Output: <stem>-reclean.md next to the input, unless --out.

Config (env or runtime.conf in the skill dir): CLEAN_LLM_BASEURL / CLEAN_LLM_MODEL
/ CLEAN_LLM_KEY — same endpoint as clean-transcripts.py.
"""
import argparse
import asyncio
import sys
from pathlib import Path

import re

import aiohttp

DIVIDER = re.compile("^---\s*$", re.M)

PROMPT = """你是一名专业转录校对员。下面提供：
1) 一段严重破损的中文 ASR 转录（源自中文配音视频，配音中夹杂英文原声，ASR 输出同音字错误、专名错译、句子残缺）。
2) 该视频的完整英文原版字幕，作为唯一可靠的语义参照。

任务：对照英文原稿，把中文转录重写为通顺、准确的简体中文转录稿。要求：
- 以英文原稿为准重建每一句话的意思；中文稿只用于保持分段顺序和口吻。
- 英文稿中出现的人名/项目名保留英文原文（如 Mike Hostetler、ASD-STE100）。
- ASR 完全无法恢复的句子，按英文稿意译补全，不要编造英文稿里没有的内容。
- 保留口语风格，不做润色拔高；禁止总结、删减任何论点、数字和例子。
- 按自然话题分段落；开头可能有配音重复句，去重。
- 只输出校对后的中文正文，不要任何说明。
{glossary}
=== 英文原版字幕 ===
{en}

=== 中文 ASR 破损转录 ===
{zh}

输出校对后的中文转录稿："""


def load_conf() -> dict:
    conf = {
        "CLEAN_LLM_BASEURL": "",
        "CLEAN_LLM_MODEL": "",
        "CLEAN_LLM_KEY": "",
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
        sys.exit(f"missing CLEAN_LLM config: {', '.join(missing)} (env or runtime.conf)")
    return conf


def split_body(text: str) -> str:
    """Strip a clean-transcripts.py header (everything before the first --- divider)."""
    m = DIVIDER.search(text)
    return text[m.end():].strip() if m else text.strip()


def chunk(text: str, size: int = 3000) -> list[str]:
    parts: list[str] = []
    while text:
        if len(text) <= size:
            parts.append(text)
            break
        cut = text.rfind("。", 0, size)
        cut = cut if cut > size // 2 else size
        parts.append(text[: cut + 1])
        text = text[cut + 1:]
    return parts


def align_slices(parts: list[str], ref: str) -> list[str]:
    """Proportionally slice the English reference to match zh chunk count."""
    n = len(parts)
    step = (len(ref) + n - 1) // n
    return [ref[i * step : (i + 1) * step] for i in range(n)]


async def clean_chunk(sess: aiohttp.ClientSession, conf: dict, prompt: str, sem: asyncio.Semaphore) -> str:
    async with sem:
        r = await sess.post(
            f"{conf['CLEAN_LLM_BASEURL']}/chat/completions",
            headers={"Authorization": f"Bearer {conf['CLEAN_LLM_KEY']}"} if conf["CLEAN_LLM_KEY"] else {},
            json={"model": conf["CLEAN_LLM_MODEL"], "temperature": 0.1,
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=aiohttp.ClientTimeout(total=900),
        )
        r.raise_for_status()
        return (await r.json())["choices"][0]["message"]["content"].strip()


async def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("raw", help="garbled raw transcript (.md with header, or .txt)")
    ap.add_argument("en_ref", help="original English transcript reference (.txt)")
    ap.add_argument("--glossary", help="optional glossary file (names/terms, one per line)")
    ap.add_argument("--chunk-chars", type=int, default=3000)
    ap.add_argument("--concurrency", type=int, default=3)
    ap.add_argument("--out", help="output path (default: <raw stem>-reclean.md beside input)")
    args = ap.parse_args()

    conf = load_conf()
    raw_path, en_path = Path(args.raw), Path(args.en_ref)
    zh = split_body(raw_path.read_text(encoding="utf-8"))
    en = en_path.read_text(encoding="utf-8").strip()
    glossary = ""
    if args.glossary:
        glossary = "\n术语对照（必须使用正确写法）：\n" + Path(args.glossary).read_text(encoding="utf-8").strip() + "\n"

    zh_parts = chunk(zh, args.chunk_chars)
    en_parts = align_slices(zh_parts, en)
    sem = asyncio.Semaphore(args.concurrency)
    out: list[str | None] = [None] * len(zh_parts)

    async with aiohttp.ClientSession() as sess:
        async def one(i: int) -> None:
            p = PROMPT.format(glossary=glossary, en=en_parts[i], zh=zh_parts[i])
            out[i] = await clean_chunk(sess, conf, p, sem)
            print(f"chunk {i + 1}/{len(zh_parts)} ok ({len(out[i])} chars)", file=sys.stderr)
        await asyncio.gather(*(one(i) for i in range(len(zh_parts))))

    text = "\n\n".join(out)
    if len(text) < 0.5 * len(zh):
        print(f"warning: output {len(text)} chars is under 50% of the zh raw body "
              f"({len(zh)} chars) — check for silent summarization", file=sys.stderr)

    out_path = Path(args.out) if args.out else raw_path.with_name(raw_path.stem + "-reclean.md")
    raw_text = raw_path.read_text(encoding="utf-8")
    header = DIVIDER.split(raw_text)[0] if raw_path.suffix == ".md" else ""
    note = (f"\n\n---\n\n> 校对说明：基于中文 ASR 原稿（{raw_path.name}）+ 英文原版字幕"
            f"（{en_path.name}）对照重洗（reclean-en.py）。\n")
    out_path.write_text(header + "---\n\n" + text + note, encoding="utf-8")
    print(f"saved {len(text)} chars -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
