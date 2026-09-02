#!/usr/bin/env python3
"""nav-chain-check.py — verify lesson navigation chain integrity.

Orders lessons/*.html by leading number and verifies each lesson links to
both neighbours: lesson i must reference lesson i+1's filename (next link)
and lesson i-1's filename (back link). The first lesson needs no back link;
the last needs no next link.

Exit 0 if the chain is unbroken, 1 with a report otherwise.
"""

import re
import sys
from pathlib import Path


def check(lessons_dir: str) -> tuple[list[str], int]:
    d = Path(lessons_dir)
    numbered: list[tuple[int, Path]] = []
    for f in sorted(d.glob("*.html")):
        m = re.match(r"(\d+)-", f.name)
        if m:
            numbered.append((int(m.group(1)), f))
    numbered.sort()

    names = [f.name for _, f in numbered]
    errors: list[str] = []
    for i, (_, f) in enumerate(numbered):
        html = f.read_text(encoding="utf-8")
        for j, direction in ((i + 1, "next"), (i - 1, "back")):
            if 0 <= j < len(names) and names[j] not in html:
                errors.append(f"{f.name}: missing {direction} link to {names[j]}")
    return errors, len(names)


def main() -> int:
    lessons_dir = sys.argv[1] if len(sys.argv) > 1 else "lessons"
    errors, count = check(lessons_dir)
    if errors:
        print("NAV CHAIN BROKEN:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"nav chain OK: {count} lesson(s), every neighbour pair linked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
