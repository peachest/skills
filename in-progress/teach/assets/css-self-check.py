#!/usr/bin/env python3
"""CSS self-check for teach lessons and reference documents.

Flags bare literal font-size/padding/margin/line-height values inside inline
<style> blocks and inline style="" attributes — they should reference the
base.css token system via var(). See CSS-CONVENTIONS.md.

Absolute px/rem/pt and bare numbers are violations. Zero violations = exit 0; any = exit 1.

KaTeX dependency check: if the visible prose contains math delimiters ($...$,
$$...$$, \(...\), \[...\]) but the head does not reference the KaTeX bundle
(katex.min.css / katex.min.js / auto-render.min.js / render.js), the formulas
render as raw source — FAIL and print the exact lines to add (reference
paradigm: spec-decoding lessons/0003-eagle1.html).
"""
from __future__ import annotations

import pathlib
import re
import sys

PROPERTIES = ("font-size", "padding", "margin", "line-height")
# a value is relative (outside the token system) if every space-separated
# token is an em/% value or the literal "0"
_RELATIVE = re.compile(r"^[\d.]+(em|%)$")

# KaTeX bundle: (basename to look for, the exact line to add when missing)
KATEX_ASSETS = (
    ("katex.min.css", '<link rel="stylesheet" href="../assets/katex.min.css">'),
    ("katex.min.js", '<script src="../assets/katex.min.js" defer></script>'),
    ("auto-render.min.js", '<script src="../assets/auto-render.min.js" defer></script>'),
    ("render.js", '<script src="../assets/render.js" defer></script>'),
)
# a $...$ span counts as math if it has a latin letter / backslash / math char
# and no CJK (filters out prose like "100$ 到 200$")
_MATH_INNER = re.compile(r"[A-Za-z\\^_={]"), re.compile(r"[\u4e00-\u9fff]")


def visible_prose(text: str) -> str:
    """Strip script/style/code/pre and tags so code samples ($ npm i) and
    attributes don't trigger the math detection."""
    text = re.sub(r"<(script|style|code|pre)[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    return re.sub(r"<[^>]+>", " ", text)


def has_math(text: str) -> bool:
    prose = visible_prose(text)
    if re.search(r"\\\(|\\\[", prose):
        return True
    prose = re.sub(r"\$\$.*?\$\$", " ", prose, flags=re.S)  # display math always counts
    for m in re.finditer(r"\$([^$\n]{1,200})\$", prose):
        inner = m.group(1)
        if inner.strip() and _MATH_INNER[0].search(inner) and not _MATH_INNER[1].search(inner):
            return True
    return False


def katex_missing(text: str) -> list[str]:
    """Return the KaTeX bundle files not referenced, if the lesson has math."""
    # frozen scoped blocks are prototype artifacts — same exemption as the CSS scan
    text = re.sub(r"<style[^>]*\bdata-frozen\b[^>]*>.*?</style>", " ", text, flags=re.S | re.I)
    if not has_math(text):
        return []
    return [name for name, _ in KATEX_ASSETS if name not in text]


def _is_relative(value: str) -> bool:
    parts = value.split()
    if not parts:
        return False
    return all(_RELATIVE.match(p) or p == "0" for p in parts)


def check(text: str) -> list[str]:
    """Return a list of violation strings for the given HTML text."""
    # frozen scoped blocks (e.g. an inlined prototype with its own self-contained
    # styling domain) are exempt: their literals are part of a frozen artifact,
    # adjudicated once at prototype acceptance, not per lesson edit. Mark with
    # <style data-frozen> — the attribute is the opt-in.
    text = re.sub(r"<style[^>]*\bdata-frozen\b[^>]*>.*?</style>", " ", text, flags=re.S | re.I)
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", text, flags=re.S)
    blocks += re.findall(r'style="([^"]*)"', text)
    violations: list[str] = []
    for block in blocks:
        for prop in PROPERTIES:
            for m in re.finditer(prop + r":\s*([^;}\"]+)", block):
                val = m.group(1).strip()
                if "var(" in val or val == "0" or _is_relative(val):
                    continue
                violations.append(f"{prop}: {val}")
    return violations


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: css-self-check.py <html-file>", file=sys.stderr)
        return 2
    path = pathlib.Path(argv[1])
    text = path.read_text(encoding="utf-8")
    violations = check(text)
    if violations:
        print(f"{path}: {len(violations)} bare literal(s) — replace with var(--token):")
        for v in violations:
            print(f"  {v}")
    missing = katex_missing(text)
    if missing:
        print(f"{path}: KaTeX 依赖缺失 — 正文含数学定界符但未引用 {', '.join(missing)}，"
              f"公式会显示为裸源码（若正文确无公式，改写掉 $ 符号即可）")
        print("  在 </head> 前补（缺哪个补哪个，路径按工作区 assets 约定 ../assets/）：")
        for name, snippet in KATEX_ASSETS:
            if name in missing:
                print(f"    {snippet}")
    if violations or missing:
        return 1
    print(f"{path}: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
