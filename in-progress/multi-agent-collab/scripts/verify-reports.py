#!/usr/bin/env python3
"""verify-reports.py — parent-side mechanical verification of subagent report files.

Why: a subagent's "REPORT_WRITTEN / 已写入 X" claim is declarative — it proves
what the child believes, not what the filesystem holds. Mined evidence
(2026-10-22 researcher x3; 2026-10-26 brainstorm 3/4 + phaseA 4/5, with
REPORT_WRITTEN true in only 1/5): reports drift into the managed artifacts
directory while the child still claims success. Root cause: a path mentioned
in task text is instruction only and does not override runtime output routing
— the API-level fix is binding `output` on the launch itself (see
references/report-verify.md). This script is the parent-side backstop.

Usage:
  python3 verify-reports.py manifest.json          # {"key": "/abs/path.md", ...}
  ... | python3 verify-reports.py -                # manifest on stdin
  python3 verify-reports.py manifest.json --window 48

Exit 0 = every declared path exists and is non-empty.
Exit 1 = at least one missing; candidates from subagent-artifacts are listed
        for recovery (回捞) — copy them to the declared path after eyeballing.
Other = script error (env broken), never a silent pass.
"""
from __future__ import annotations

import glob
import json
import os
import sys
import time

SESSIONS_DIR = os.environ.get(
    "PI_SESSIONS_DIR", os.path.expanduser("~/.pi/agent/sessions")
)
PREVIEW_CHARS = 96


def load_manifest(arg: str) -> dict:
    raw = sys.stdin.read() if arg == "-" else open(arg, encoding="utf-8").read()
    data = json.loads(raw)
    if isinstance(data, list):  # bare path list → synthetic keys
        return {os.path.basename(p): p for p in data}
    if not isinstance(data, dict):
        raise ValueError("manifest must be an object {key: abs_path} or a list of paths")
    return data


def artifact_candidates(window_hours: float) -> list[tuple[float, str, int, str]]:
    """Files the runtime may have caught instead: <runid>_<agent>_output.md,
    newest first, within the window. Input/meta/transcript files excluded."""
    cutoff = time.time() - window_hours * 3600
    hits = []
    pattern = os.path.join(SESSIONS_DIR, "subagent-artifacts", "*_output.md")
    for path in glob.glob(pattern):
        try:
            st = os.stat(path)
        except OSError:
            continue
        if st.st_mtime < cutoff or st.st_size == 0:
            continue
        with open(path, encoding="utf-8", errors="replace") as f:
            preview = f.read(PREVIEW_CHARS).replace("\n", " ")
        hits.append((st.st_mtime, path, st.st_size, preview))
    hits.sort(reverse=True)
    return hits


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    window = 24.0
    if "--window" in sys.argv:
        window = float(sys.argv[sys.argv.index("--window") + 1])
    manifest = load_manifest(sys.argv[1])

    missing = []
    print(f"{'status':<8} {'size':>9}  key -> path")
    for key, path in manifest.items():
        if os.path.isfile(path) and os.path.getsize(path) > 0:
            print(f"{'OK':<8} {os.path.getsize(path):>9}  {key} -> {path}")
        else:
            print(f"{'MISSING':<8} {'-':>9}  {key} -> {path}")
            missing.append((key, path))

    if not missing:
        return 0

    print(f"\n== recovery candidates (subagent-artifacts, last {window:g}h, newest first) ==")
    cands = artifact_candidates(window)
    if not cands:
        print("  none — nothing landed in artifacts either; the child likely never wrote.")
    for mtime, path, size, preview in cands[:10]:
        stamp = time.strftime("%m-%d %H:%M", time.localtime(mtime))
        print(f"  {stamp}  {size:>8}B  {path}")
        print(f"            └ {preview}")

    print(
        "\nclaim≠written: verify manually (head each candidate), then copy to the"
        "\ndeclared path, or relaunch with output: bound (references/report-verify.md)."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
