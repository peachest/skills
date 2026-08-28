#!/usr/bin/env python3
"""CSS self-check for teach lessons and reference documents.

Flags bare literal font-size/padding/margin/line-height values inside inline
<style> blocks and inline style="" attributes — they should reference the
base.css token system via var(). See CSS-CONVENTIONS.md.

Relative em/% values pass (outside the token system). Absolute px/rem/pt and
bare numbers are violations. Zero violations = exit 0; any = exit 1.
"""
from __future__ import annotations

import pathlib
import re
import sys

PROPERTIES = ("font-size", "padding", "margin", "line-height")
# a value is relative (outside the token system) if every space-separated
# token is an em/% value or the literal "0"
_RELATIVE = re.compile(r"^[\d.]+(em|%)$")


def _is_relative(value: str) -> bool:
    parts = value.split()
    if not parts:
        return False
    return all(_RELATIVE.match(p) or p == "0" for p in parts)


def check(text: str) -> list[str]:
    """Return a list of violation strings for the given HTML text."""
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", text, re.S)
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
        return 1
    print(f"{path}: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
