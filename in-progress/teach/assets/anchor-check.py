#!/usr/bin/env python3
"""anchor-check.py — mechanically re-verify a lesson's source anchors.

Input: one or more lesson HTML files plus a anchors JSON file (exported from
okb bronze — the claim→anchor ledger). For every anchor, re-reads the cited
origin line and checks the lesson's quoted material appears there verbatim
(numbers exact, text normalized). Reports:

  - UNANCHORED: a numeric claim in the lesson with no anchor covering it
  - MISMATCH: the anchor's cited line does not contain the quoted value
  - FIG-DRIFT: a figure number the lesson cites that differs from the local
    tex's literal numbering (e.g. lesson says Fig. 7, tex says Figure 4 for
    the same caption)

Anchor shapes (see references/source-extraction.md):
  {"claims": [{"quote": "3.62x", "anchor": "tex:147"},
              {"quote": "25 nodes", "anchor": "2320d52:eagle/model/choices.py:1"},
              {"quote": "同一位置的接受率方差很大", "anchor": "p/839661630#para3"}],
   "sources": {"tex:147": {"path": ".../example_paper.tex", "kind": "tex"},
               "2320d52:...:1": {"path": ".../choices.py", "kind": "code",
                                 "commit": "2320d52"},
               "p/839661630#para3": {"path": ".../zhihu-text-839661630.txt",
                                     "kind": "interpretation", "locator": "para3"}}}

Usage:
  python3 anchor-check.py <anchors.json> <lesson.html> [<lesson.html>...]
Exit 0 = all anchors verified; 1 = findings; 2 = usage error.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

NUM_RE = re.compile(r"\d+(?:\.\d+)?(?:x|%|×|倍|节点|tokens?)?", re.I)
# "Fig. 7", "Figure 7", "图 7", "图7"
FIGREF_RE = re.compile(r"(?:Fig(?:ure)?\.?|图)\s*(\d+)", re.I)
LINE_SPLIT = re.compile(r"\r?\n")


def _normalize(s: str) -> str:
    return re.sub(r"\s+", "", s)


def resolve_line(src: dict, anchor: str) -> tuple[str | None, str | None]:
    """Return the cited line's text (or None) for the anchor's file:line part."""
    path = src.get("path")
    if not path:
        return None, "anchor source lacks 'path'"
    p = pathlib.Path(path)
    if not p.exists():
        return None, f"source file missing: {path}"
    text = p.read_text(errors="ignore")
    m = re.search(r":(\d+)$", anchor)
    if not m:
        return text, None  # no line component: search whole text
    n = int(m.group(1))
    lines = LINE_SPLIT.split(text)
    if not 1 <= n <= len(lines):
        return None, f"line {n} out of range ({len(lines)} lines)"
    return lines[n - 1], None


def check_anchors(ledger: dict, lessons: list[pathlib.Path]) -> list[str]:
    findings: list[str] = []
    sources = ledger.get("sources", {})
    for lesson in lessons:
        html = lesson.read_text(encoding="utf-8", errors="ignore")
        # strip markup for quote matching
        prose = re.sub(r"<[^>]+>", " ", html)
        anchored_quotes = {_normalize(c.get("quote", ""))
                           for c in ledger.get("claims", [])}
        for claim in ledger.get("claims", []):
            quote, anchor = claim.get("quote", ""), claim.get("anchor", "")
            src = sources.get(anchor)
            if src is None:
                findings.append(f"{lesson.name}: NO-SOURCE anchor {anchor!r} "
                                f"(quote {quote[:30]!r}) — not in ledger sources")
                continue
            anchored_quotes.add(_normalize(quote))
            line, err = resolve_line(src, anchor)
            if err:
                findings.append(f"{lesson.name}: BROKEN {anchor} — {err}")
                continue
            norm_quote = _normalize(quote)
            norm_line = _normalize(line or "")
            if norm_quote not in norm_line:
                findings.append(
                    f"{lesson.name}: MISMATCH {anchor} — quote {quote[:40]!r} "
                    f"not found verbatim in cited line")
        # figure-number drift vs the local tex, when a tex source is known
        tex = next((s for s in sources.values() if s.get("kind") == "tex"), None)
        if tex and tex.get("path") and pathlib.Path(tex["path"]).exists():
            tex_text = pathlib.Path(tex["path"]).read_text(errors="ignore")
            for num in set(FIGREF_RE.findall(prose)):
                # the lesson cites Fig N; require the tex to mention Figure N
                # (literal caption text or a label/ref), else version renumbering
                if not re.search(rf"Figure\s*{num}\b", tex_text, re.I) and \
                   not re.search(rf"\\label\{{fig:[^}}]*{num}[^}}]*\}}", tex_text):
                    findings.append(
                        f"{lesson.name}: FIG-DRIFT — cites Fig. {num} but the local "
                        f"tex never mentions Figure {num} (version renumbering?)")
        # numeric claims with no anchor at all (spot-check level, not exhaustive)
        for m in NUM_RE.finditer(prose):
            ctx = prose[max(0, m.start() - 30):m.end() + 10]
            if "var(" in ctx or "katex" in ctx.lower():
                continue
            val = _normalize(m.group(0))
            # only report distinctive values (skip years, indices)
            if (len(val) >= 2 and not any(val in q for q in anchored_quotes)
                    and not re.fullmatch(r"(19|20)\d{2}|\d", val)):
                    findings.append(
                        f"{lesson.name}: UNANCHORED number {m.group(0)!r} "
                        f"(context: …{ctx[-40:].strip()})")
    return findings


def main() -> int:
    args = sys.argv[1:]
    if len(args) < 2:
        print("usage: anchor-check.py <anchors.json> <lesson.html> [...]", file=sys.stderr)
        return 2
    ledger = json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8"))
    lessons = [pathlib.Path(a) for a in args[1:]]
    for lesson in lessons:
        if not lesson.exists():
            print(f"FAIL: lesson not found: {lesson}", file=sys.stderr)
            return 2
    findings = check_anchors(ledger, lessons)
    if findings:
        print(f"ANCHOR CHECK: {len(findings)} finding(s)")
        for f in findings[:40]:
            print(f"  - {f}")
        if len(findings) > 40:
            print(f"  … and {len(findings) - 40} more")
        print("每条 finding 需就地裁定：补锚点、修正引用，或确认无锚（回 okb 补 bronze 摘录）")
        return 1
    print("ANCHOR CHECK: all anchors verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
