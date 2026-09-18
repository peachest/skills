#!/usr/bin/env python3
"""Scan Go files for functions whose doc comment is as long as or longer
than the function body.

Usage:
    python3 scan.py <files-or-dirs>... [--ratio N] [--all]

--ratio N   flag functions where comment_lines >= body_lines * N (default 1)
--all       also print functions with no comment issue (default: flagged only)

Output: one line per function, "comment=N body=N ⚠️ func signature".
Exit code is always 0; the caller reads the output.
"""
import argparse
import os
import re
import sys


def scan_file(path, ratio):
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except (OSError, UnicodeDecodeError) as e:
        print(f"skip {path}: {e}", file=sys.stderr)
        return
    i = 0
    while i < len(lines):
        m = re.match(r"^func\s", lines[i])
        if not m:
            i += 1
            continue
        # collect doc comment directly above
        j, comment_start = i - 1, i
        while j >= 0 and lines[j].startswith("//"):
            comment_start = j
            j -= 1
        comment_len = i - comment_start
        # find function body end via brace balancing from the signature line
        k, depth = i, 0
        while k < len(lines):
            depth += lines[k].count("{") - lines[k].count("}")
            if depth <= 0 and k > i:
                break
            k += 1
        body_len = k - i
        yield comment_len, body_len, lines[i]
        i = k + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--ratio", type=float, default=1.0)
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    files = []
    for p in args.paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                files += [os.path.join(root, n) for n in names if n.endswith(".go")]
        else:
            files.append(p)

    for f in files:
        for c, b, sig in scan_file(f, args.ratio):
            flagged = c >= b * args.ratio and c > 0
            if not (flagged or args.all):
                continue
            mark = "⚠️" if flagged else "  "
            print(f"{os.path.relpath(f)}: comment={c:2d} body={b:2d} {mark} {sig[:70]}")


if __name__ == "__main__":
    main()
