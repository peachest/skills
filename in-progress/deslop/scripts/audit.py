#!/usr/bin/env python3
"""audit.py — bilingual (zh/en) AI-slop audit. Flag-only, read-only.

Audit-first: run this BEFORE any rewrite. Every hit is a flag awaiting
adjudication (load-bearing stays, decorative gets a minimal fix) — a flag
never authorizes an edit by itself. Below the verdict floor, the verdict is
"skip: not worth a rewrite".

Language is decided per paragraph (CJK ratio); a mixed document yields zh
flags on zh paragraphs and en flags on en paragraphs. Code fences, inline
code spans, and frontmatter are masked before scanning but keep their line
numbers.

Usage:
  python3 audit.py <file.md> [--mode flavor|strict] [--json] [--force]
Exit codes: 0 = report produced (verdict may still be "skip"); 2 = usage error.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ── zh rules — trigger markers from lieflat-less-ai-tone (corpus-validated;
#    check-translationese.py BASELINE/MARKERS) plus its SKILL.md rules 4-9. ──
ZH_RULES = [
    ("ZH-1", "翻案腔",
     r"(?:不是|并非)[^，。\n]{0,20}，?而是|与其说[^，。\n]{1,20}不如说"
     r"|看似[^，。\n]{1,12}实则|表面[^，。\n]{1,12}实际|你以为[^，。\n]{1,20}其实"
     r"|说到底|答案恰恰相反"),
    ("ZH-2", "顿号罗列",
     r"(?:[^，。\n、]{1,10}、){2,}[^，。\n、]{1,10}"),
    ("ZH-4", "破折号",
     r"——"),
    ("ZH-5", "提示性冒号",
     r"(?:一句话(?:总结|说|概括)|简单说|说白了|总结|小结|结论|核心(?:是|在于|观点)?"
     r"|关键(?:是|在于)?|重点(?:是)?|原因(?:如下|有|在于)?|问题(?:是|在于)?"
     r"|答案(?:是)?|本质(?:是|上)?|定义(?:是)?|具体(?:来说|如下|包括)?"
     r"|举例(?:来说)?|换句话说|也就是说|我的(?:观点|判断|结论)|建议(?:是)?)[：:]"),
    ("ZH-7", "拟人喻体",
     r"(?:像|如同|相当于|就好比)(?:一个|一位|个)[一-鿿]{0,4}"
     r"(?:导师|秘书|助手|顾问|管家|审查员|实习生|参谋|哨兵|卫士)"),
    ("ZH-8", "概括盖数据",
     r"(?:显著提升|大幅增长|明显改善|显著下降|大幅提升|效率的提升|大量的|众多)"),
    ("ZH-9", "起手式",
     r"(?:说白了|说穿了|先说结论)"),
    ("ZH-10a", "翻译腔·当…时",
     r"(?:^|\n)\s*当[^，。\n]{2,20}(?:的时候|时)，"),
    ("ZH-10b", "翻译腔·话题壳",
     r"(?:对于[^，。\n]{2,15}来说|对[^，。\n]{2,15}而言|就[^，。\n]{2,15}而言|在[^，。\n]{2,12}方面)"),
    ("ZH-10c", "翻译腔·句首连接词",
     r"(?:^|\n)\s*(?:然而|因此|此外|与此同时|换言之|总而言之)[，、]"),
    ("ZH-10d", "翻译腔·这意味着",
     r"(?:这意味着|这表明|这说明|换句话说)"),
    ("ZH-11", "段首零主语",
     r"(?:^|\n)\s*(?:听起来|看起来|值得注意的是|更重要的是|关键在于|问题在于|不难看出)"),
]

# ── en rules — mechanical subset of ASD-STE100 (sentence caps, punctuation,
#    modals) plus the video's slop habits #1/#3/#4/#6. No 900-word dictionary
#    lock: for general prose that is noise (measured on a technical wiki,
#    rule-1.1 was 87% of hits). ──
EN_RULES = [
    ("EN-2", "semicolon", r";"),
    ("EN-3", "ambiguous modal (may/might)",
     r"\b(?:may|might)\b"),
    ("EN-4", "marketing adjective",
     r"\b(?:seamless(?:ly)?|robust(?:ness)?|powerful|cutting-edge|effortless(?:ly)?"
     r"|blazing(?:ly)?|enterprise-grade|game-changing|revolutionary|best-in-class|world-class)\b"),
    ("EN-5", "chatty phrasal verb",
     r"\b(?:spin(?:s|ning)? up|reach(?:es|ed)? out|div(?:e|ing) into|delv(?:e|es|ing)(?: into)?"
     r"|kick(?:s|ed)? off|touch base|leverage[sd]?)\b"),
    ("EN-6", "nominalized verb",
     r"\bperform(?:s|ed)?\s+(?:an\s+|a\s+)?analysis\s+(?:of|on)\b"
     r"|\bprovid(?:e|es|ed)\s+assistance\b"
     r"|\bmak(?:e|es|ing)\s+(?:a\s+)?decision\b"
     r"|\bmak(?:e|es|ing)\s+use\s+of\b"
     r"|\bconduct(?:s|ed)?\s+(?:a\s+)?(?:review|study)\s+of\b"),
    ("EN-7", "em-dash", r"[—–]"),
]

SENT_END_ZH = r"[。！？!?…]"
SENT_END_EN = r"[.!?](?:\s|$)"

CJK = re.compile(r"[一-鿿]")
HEDGES_ZH = re.compile(r"可能|或许|通常|据说|大概|往往|一般来说|在某些情况下")
HEDGES_EN = re.compile(r"\b(?:may|might|possibly|perhaps|usually|sometimes|often)\b")

# verdict floor: flags per 100 sentences at or above which a rewrite is
# warranted. Calibrate on real before/after pairs before touching.
FLOOR_PER_100 = 3.0
DASH_DENSITY_PER_100_LINES = 25.0  # teach-prose-freq calibration: slop 30.3, clean 23.6


def mask_code(text: str) -> str:
    """Blank code fences and inline code spans, preserving newlines/length."""
    def keep_nl(s: str) -> str:
        return re.sub(r"[^\n]", " ", s)
    if text.startswith("---"):  # frontmatter only, never mid-file dividers
        end = re.search(r"^---\s*$", text[3:], flags=re.M)
        if end:
            text = keep_nl(text[: 3 + end.end()]) + text[3 + end.end():]
    text = re.sub(r"```.*?```", lambda m: keep_nl(m.group(0)), text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", lambda m: keep_nl(m.group(0)), text)
    return text


def split_paragraphs(text: str):
    paras, start = [], 0
    for m in re.finditer(r"\n\s*\n", text):
        paras.append((start, m.start()))
        start = m.end()
    if start < len(text):
        paras.append((start, len(text)))
    return [(a, text[a:b]) for a, b in paras if text[a:b].strip()]


def lang_of(chunk: str) -> str:
    cjk = len(CJK.findall(chunk))
    letters = len(re.findall(r"[A-Za-z]", chunk))
    return "zh" if cjk * 2 > letters else "en"


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def sentences(chunk: str, lang: str):
    pat = SENT_END_ZH if lang == "zh" else SENT_END_EN
    return [s for s in re.split(pat, chunk) if s.strip()]


SENT_SPLIT = re.compile(r"([。！？!?…]+|[.]+(?=\s|$))")


def bilingual_sentences(chunk: str):
    """Split on both zh and en terminators; classify each sentence by its
    own CJK ratio. Mixed paragraphs (zh prose with en terms) route per
    sentence, not per paragraph."""
    out = []
    for part in SENT_SPLIT.split(chunk):
        if part and SENT_SPLIT.fullmatch(part):
            continue
        s = part.strip()
        if s:
            out.append((s, lang_of(s)))
    return out


def numbered_heading_run(text: str) -> list[tuple[int, str]]:
    """ZH-6: >=3 consecutive numbered headings (一、二、… / 第一，第二…).

    Consecutive means no unnumbered heading between them; prose or blank
    lines in between are fine.
    """
    all_rx = re.compile(r"^(#{1,6})\s*(.*)$", re.M)
    num_rx = re.compile(r"[一二三四五六七八九十]+、|第[一二三四五六七八九十]+[，、]")
    hits, run = [], 0
    for m in all_rx.finditer(text):
        numbered = bool(num_rx.match(m.group(2).strip()))
        run = run + 1 if numbered else 0
        if run >= 3:
            hits.append((line_of(text, m.start()), m.group(0).strip()))
    return hits


def idle_colon_lines(text: str) -> list[tuple[int, str]]:
    """ZH-5b: a line ending in ： that only announces the list below it."""
    hits = []
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.endswith("：") and len(s) <= 40:
            nxt = next((lines[j].lstrip() for j in range(i + 1, len(lines))
                        if lines[j].strip()), "")
            if nxt.startswith(("-", "*")) or re.match(r"^\d+[.、)]", nxt):
                hits.append((i + 1, s))
    return hits


def audit_text(text: str, mode: str = "flavor") -> dict:
    masked = mask_code(text)
    flags = []  # {rule, name, lang, line, match}
    n_sentences = 0

    for _, para in split_paragraphs(masked):
        n_sentences += len(bilingual_sentences(para))

    # regex rules, matched per sentence with that sentence's language
    for start, para in split_paragraphs(masked):
        pos = start
        for s, lang in bilingual_sentences(para):
            offset = masked.find(s, pos)
            if offset < 0:
                offset = pos
            pos = offset + len(s)
            rules = ZH_RULES if lang == "zh" else EN_RULES
            for rid, name, pat in rules:
                for m in re.finditer(pat, s):
                    flags.append({"rule": rid, "name": name, "lang": lang,
                                  "line": line_of(text, offset + m.start()),
                                  "match": m.group(0).strip()[:60]})

    # en sentence-length (EN-1): threshold by mode, STE 5.1/6.3
    limit = 20 if mode == "strict" else 25
    for start, para in split_paragraphs(masked):
        pos = start
        for s, lang in bilingual_sentences(para):
            if lang != "en":
                continue
            offset = masked.find(s, pos)
            if offset < 0:
                offset = pos
            pos = offset + len(s)
            words = len(re.findall(r"[A-Za-z0-9']+", s))
            if words > limit:
                flags.append({"rule": "EN-1", "name": f"sentence >{limit} words",
                              "lang": "en", "line": line_of(text, offset),
                              "match": f"{words} words: {s.strip()[:50]}…"})

    # zh structural rules that need code, not regex
    for ln, m in numbered_heading_run(masked):
        flags.append({"rule": "ZH-6", "name": "序数词当小标题", "lang": "zh",
                      "line": ln, "match": m})
    for ln, m in idle_colon_lines(masked):
        flags.append({"rule": "ZH-5b", "name": "空转句引出列表", "lang": "zh",
                      "line": ln, "match": m})

    # ZH-4 density guard (teach-calibrated): dense dash prose is a rewrite
    # candidate even when individual dashes look defensible
    prose_lines = sum(1 for ln in masked.split("\n") if ln.strip())
    zh_text = "".join(s for _, p in split_paragraphs(masked) for s, l in bilingual_sentences(p) if l == "zh")
    dash_density = zh_text.count("——") * 100 / max(prose_lines, 1)

    per_rule = {}
    for f in flags:
        per_rule[f["rule"]] = per_rule.get(f["rule"], 0) + 1

    score = len(flags) * 100 / max(n_sentences, 1)
    verdict = "rewrite-warranted" if len(flags) >= FLOOR_PER_100 or dash_density > DASH_DENSITY_PER_100_LINES \
        else "skip: below floor"
    return {
        "file_hits": len(flags),
        "sentences": n_sentences,
        "score_per_100_sentences": round(score, 1),
        "dash_density_per_100_lines": round(dash_density, 1),
        "verdict": verdict,
        "per_rule": dict(sorted(per_rule.items())),
        "flags": flags,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file")
    ap.add_argument("--mode", choices=["flavor", "strict"], default="flavor")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="proceed past a below-floor verdict (recorded in output)")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    report = audit_text(text, args.mode)
    if args.force and report["verdict"].startswith("skip"):
        report["verdict"] = "skip-overridden (--force)"
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return 0

    print(f"deslop audit: {args.file}  mode={args.mode}")
    print(f"sentences={report['sentences']}  hits={report['file_hits']}  "
          f"score={report['score_per_100_sentences']}/100 sentences  "
          f"dash-density={report['dash_density_per_100_lines']}/100 lines")
    print(f"verdict: {report['verdict']}")
    for rid, n in report["per_rule"].items():
        print(f"  {rid}: {n}")
    for f in report["flags"]:
        print(f"  [{f['rule']}] L{f['line']} ({f['lang']}) {f['name']}: {f['match']}")
    print("\nflag-only: every flag needs adjudication (load-bearing stays, "
          "decorative gets a minimal fix); a flag never authorizes an edit by itself.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
