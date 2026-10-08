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


def _ruling_for(detail: str, rulings: list[str]) -> str | None:
    """Match a finding against _rulings entries: a ruling matches when it
    contains the finding's quoted token (signature-style key or free text)."""
    m = re.search(r"['\"]([^'\"]+)['\"]", detail)
    if not m:
        return None
    token = m.group(1)
    for entry in rulings:
        if token in entry:
            return entry
    return None


def check_anchors(ledger: dict, lessons: list[pathlib.Path]) -> list[str]:
    findings: list[str] = []
    sources = ledger.get("sources", {})
    # _rulings: adjudicated suppressions from the course ledger (field-proven in
    # specforge-training before landing here). Two shapes exist in the wild:
    #   dict  {"UNANCHORED '100%'": "reason"}            (keyed by signature)
    #   list  ["UNANCHORED '100%' ... — reason", ...]     (free-text lines)
    # Both accepted: a ruling matches a finding when the ruling text contains
    # the finding's quoted token. Matching findings are printed as ADJUDICATED
    # (kept) and do not count toward exit.
    rulings_list = ledger.get("_rulings") or []
    if isinstance(rulings_list, dict):
        rulings_list = [f"{k}: {v}" for k, v in rulings_list.items()]
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
        # FP-exclusion contexts (specforge field data: ~56% of UNANCHORED lines
        # were token-internal): identifier:line citation references (tex:123),
        # CSS/media-query values, percentages inside <style>-adjacent markup
        CTX_REF_RE = re.compile(r"(?:tex|paper|source|fig|file|line|commit)[\w.\-]*:\s*\d", re.I)
        CSS_CTX_RE = re.compile(r"@media|max-width|min-width|width:\s*\d|height:\s*\d|px\b")
        for m in NUM_RE.finditer(prose):
            ctx = prose[max(0, m.start() - 30):m.end() + 10]
            if "var(" in ctx or "katex" in ctx.lower() or CSS_CTX_RE.search(ctx):
                continue
            if CTX_REF_RE.search(ctx):
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
    rulings_list = [str(x) for x in (ledger.get("_rulings") or [])]
    if findings:
        open_findings = []
        for f in findings:
            kind = f.split(" — ")[0].split(": ")[-2] if ": " in f else f.split(":")[1].strip()
            r = _ruling_for(f, rulings_list)
            if r:
                print(f"  ADJUDICATED (kept): {f.split(' — ')[-1][:70]} — {r[:60]}")
            else:
                open_findings.append(f)
        print(f"ANCHOR CHECK: {len(open_findings)} open / "
              f"{len(findings) - len(open_findings)} adjudicated")
        for f in open_findings[:40]:
            print(f"  - {f}")
        if len(open_findings) > 40:
            print(f"  … and {len(open_findings) - 40} more")
        print("每条 open finding 需就地裁定：补锚点、修正引用、确认无锚（回 okb 补 bronze 摘录），"
              "或写入 _rulings（ledger 抑制，带理由）")
        return 1 if open_findings else 0
    print("ANCHOR CHECK: all anchors verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
