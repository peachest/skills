#!/usr/bin/env python3
"""resource-check.py — verify every relative href/src in lesson HTML resolves.

The nav-chain check verifies lesson-to-lesson links; this check covers every
other relative reference — stylesheets, scripts, images, okb paths. A lesson
chain whose CSS or figure assets 404 renders broken for the learner even
with a perfect nav chain (spec-decoding state_event: a directory re-shuffle
broke relative hrefs across 10 files; no check in the family noticed).

Skips absolute URLs (http/https/mailto), data: URIs, and pure anchors
(#foo) — those are not filesystem reachability claims. Fragment-carrying
paths resolve on the path part.

Usage:
  python3 resource-check.py <lesson-dir-or-file> [<more>...]
Exit 0 = all relative references resolve; 1 = missing; 2 = usage error.
"""
from __future__ import annotations

import pathlib
import re
import sys

REF_RE = re.compile(r"""(?:src|href|poster|srcset)=["']([^"'#]+)(?:#[^"']*)?["']""", re.I)
SKIP_SCHEMES = ("http://", "https://", "mailto:", "data:", "//")
# url(...) inside inline styles too (background images in <style> blocks)
CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^'\")]+?)['\"]?\s*\)")


def collect_refs(text: str) -> list[str]:
    refs = [m.group(1) for m in REF_RE.finditer(text)]
    for style in re.findall(r"<style[^>]*>(.*?)</style>", text, re.S):
        refs += [m.group(1) for m in CSS_URL_RE.finditer(style)]
    for style in re.findall(r'style="([^"]*)"', text):
        refs += [m.group(1) for m in CSS_URL_RE.finditer(style)]
    return refs


def check_file(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    base = path.parent
    missing = []
    seen: set[str] = set()
    for ref in collect_refs(text):
        ref = ref.strip()
        if not ref or ref in seen:
            continue
        seen.add(ref)
        if ref.startswith(SKIP_SCHEMES):
            continue
        # srcset may carry multiple candidates with width descriptors
        candidates = [c.split()[0] for c in ref.split(",") if c.strip()]
        for cand in candidates:
            if cand.startswith(SKIP_SCHEMES) or not cand:
                continue
            # query strings are not filesystem paths
            target = base / cand.split("?")[0]
            if not target.exists():
                missing.append(f"  {path.name} → {ref}")
    return missing


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("usage: resource-check.py <lesson-dir-or-file> [...]", file=sys.stderr)
        return 2
    files: list[pathlib.Path] = []
    for a in args:
        p = pathlib.Path(a)
        if p.is_dir():
            files += sorted(p.glob("*.html"))
        elif p.exists():
            files.append(p)
        else:
            print(f"FAIL: not found: {a}", file=sys.stderr)
            return 2
    if not files:
        print("no html files found")
        return 0
    all_missing: list[str] = []
    for f in files:
        all_missing += check_file(f)
    if all_missing:
        print(f"RESOURCE CHECK: {len(all_missing)} broken reference(s)")
        for m in all_missing:
            print(m)
        return 1
    print(f"RESOURCE CHECK: all relative references resolve ({len(files)} file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
