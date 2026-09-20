#!/usr/bin/env python3
"""conservation.py — machine check for the information-conservation boundary
between an original document and its rewritten version.

The rewrite contract forbids adding or removing information: quotes, numbers,
hedges, and document structure must survive. This script is the pass/fail
gate — LOST items exit 1.

Checked (multiset diff orig -> new):
  code spans   `...` backtick spans
  quotes       "…" / "…" / 「…」 quoted spans
  numbers      12 / 3.5 / 87% tokens
  hedges       可能/或许/通常/据说/大概/往往/一般来说/在某些情况下 · may/might/possibly/perhaps/usually
  structure    heading counts per level, table rows, code fences, paragraphs

Usage:
  python3 conservation.py <orig> <new> [--json]
Exit codes: 0 = nothing lost; 1 = LOST items found; 2 = usage error.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

HEDGES = re.compile(
    r"可能|或许|通常|据说|大概|往往|一般来说|在某些情况下"
    r"|\b(?:may|might|possibly|perhaps|usually|sometimes|often)\b")


def spans(text: str, rx: re.Pattern) -> Counter:
    return Counter(m.group(1).strip() if m.groups() else m.group(0).strip()
                   for m in rx.finditer(text))


def diff(orig: Counter, new: Counter) -> tuple[Counter, Counter]:
    lost = orig - new
    added = new - orig
    return lost, added


def structure_counts(text: str) -> dict:
    lines = text.split("\n")
    levels = Counter()
    for ln in lines:
        m = re.match(r"^(#{1,6})\s", ln)
        if m:
            levels[len(m.group(1))] += 1
    return {
        "lines": len(lines),
        "headings": dict(levels),
        "heading_total": sum(levels.values()),
        "table_rows": sum(1 for ln in lines if ln.lstrip().startswith("|")),
        "code_fences": sum(1 for ln in lines if ln.lstrip().startswith("```")),
        "paragraphs": len(re.split(r"\n\s*\n", text.strip())),
    }


def check(orig_text: str, new_text: str) -> dict:
    report = {}

    lost, added = diff(spans(orig_text, re.compile(r"`([^`\n]+)`")),
                       spans(new_text, re.compile(r"`([^`\n]+)`")))
    if lost:
        report["code_spans_lost"] = list(lost.elements())
    if added:
        report["code_spans_added"] = list(added.elements())

    qrx = re.compile(r"[“\"]([^“”\"]{2,120})[”\"]|「([^」\n]{2,120})」")

    def quote_spans(t: str) -> Counter:
        c = Counter()
        for m in qrx.finditer(t):
            c[(m.group(1) or m.group(2)).strip()] += 1
        return c

    lost, added = diff(quote_spans(orig_text), quote_spans(new_text))
    if lost:
        report["quotes_lost"] = list(lost.elements())
    if added:
        report["quotes_added"] = list(added.elements())

    nrx = re.compile(r"\d+(?:\.\d+)?%?")
    lost, added = diff(spans(orig_text, nrx), spans(new_text, nrx))
    if lost:
        report["numbers_lost"] = list(lost.elements())
    if added:
        report["numbers_added"] = list(added.elements())

    lost, added = diff(spans(orig_text, HEDGES), spans(new_text, HEDGES))
    if lost:
        report["hedges_lost"] = list(lost.elements())
    if added:
        report["hedges_added"] = list(added.elements())

    so, sn = structure_counts(orig_text), structure_counts(new_text)
    struct = {}
    for key in ("lines", "heading_total", "table_rows", "code_fences", "paragraphs"):
        if sn[key] < so[key]:
            struct[key] = {"orig": so[key], "new": sn[key]}
    for lvl, n in so["headings"].items():
        if sn["headings"].get(lvl, 0) < n:
            struct[f"heading_level_{lvl}"] = {"orig": n, "new": sn["headings"].get(lvl, 0)}
    if struct:
        report["structure_shrunk"] = struct

    report["ok"] = not any(k.endswith("_lost") or k == "structure_shrunk"
                           for k in report)
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("orig")
    ap.add_argument("new")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    orig = Path(args.orig).read_text(encoding="utf-8")
    new = Path(args.new).read_text(encoding="utf-8")
    report = check(orig, new)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        status = "OK" if report["ok"] else "FAIL"
        print(f"conservation: {status}  ({args.orig} -> {args.new})")
        for k, v in report.items():
            if k == "ok":
                continue
            items = ", ".join(f"『{x}』×{n}" for x, n in sorted(Counter(v).items())) \
                if isinstance(v, list) else json.dumps(v, ensure_ascii=False)
            print(f"  {k}: {items}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
