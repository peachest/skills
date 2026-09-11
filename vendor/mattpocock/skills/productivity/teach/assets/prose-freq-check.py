#!/usr/bin/env python3
"""prose-freq-check.py — flag stylistic tics in lesson prose (Chinese).

Extracts visible text from an HTML lesson (style/script/svg/head/comments
stripped), counts known tics and dash density, and prints a report.

FLAG-ONLY: a flag prompts contextual adjudication, never authorizes an edit.
Load-bearing uses stay (mathematical 恰好 = exactness, safety-rule 永远);
decorative uses get minimal fixes. Exit code is 0 for any completed report —
the completion criterion is "every flag adjudicated", not "zero flags".
"""

import html as htmllib
import re
import sys
from pathlib import Path

# tic -> flag when count > threshold
TICS: dict[str, int] = {
    "恰好": 5,   # keep only where it carries mathematical exactness
    "永远": 2,   # keep only in safety rules / invariants
    "不多不少": 0,  # stacked-decorator pattern
    "同一件事": 0,  # "X、Y、Z——同一件事" coda
    "都只是": 0,   # "后面的一切都只是" scaffold
}
DASH = "——"
DASH_DENSITY = 25  # per 100 prose lines; calibrated on a real lesson's
# before/after de-slop pair (slop 30.3 vs clean 23.6)


def extract_text(path: Path) -> str:
    h = path.read_text(encoding="utf-8")
    h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    h = re.sub(r"<(style|script|svg|head)\b.*?</\1>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    return htmllib.unescape(h)


def report(path: Path) -> None:
    text = extract_text(path)
    lines = [ln for ln in text.splitlines() if ln.strip()]
    n_lines = max(len(lines), 1)
    print(f"prose freq: {path.name} ({n_lines} prose lines)")
    for tic, threshold in TICS.items():
        count = text.count(tic)
        if count > threshold:
            print(
                f"  FLAG {tic}: {count} (threshold {threshold})"
                " — adjudicate each: load-bearing stays, decorative is fixed"
            )
        else:
            print(f"  ok   {tic}: {count}")
    density = text.count(DASH) * 100 / n_lines
    if density > DASH_DENSITY:
        print(f"  FLAG {DASH} density: {density:.1f}/100 lines (threshold {DASH_DENSITY})")
    else:
        print(f"  ok   {DASH} density: {density:.1f}/100 lines")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: prose-freq-check.py <lesson.html> [more.html ...]", file=sys.stderr)
        return 2
    for arg in sys.argv[1:]:
        report(Path(arg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
