#!/usr/bin/env python3
"""Extract query strings from pi session JSONLs for a given CLI tool.

Default regexes target the anysearch CLI; override with --regex (repeatable).
Output: stats header + '  N  query' lines sorted by frequency.
"""
import argparse, glob, json, os, re, sys
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("--match", default="anysearch_cli", help="substring to select candidate JSONL lines")
ap.add_argument("--regex", action="append", default=[
    r'\bsearch\s+"([^"]+)"',
    r'--query\s+"([^"]+)"',
], help="regex with ONE capture group for the query (repeatable)")
ap.add_argument("--sessions-glob", default=os.path.expanduser("~/.pi/agent/sessions/**/*.jsonl"))
ap.add_argument("--junk", default=r"^(q\d?|query\d?|test.*|\\)$", help="queries matching this are dropped")
ap.add_argument("--min-len", type=int, default=8)
args = ap.parse_args()

regs = [re.compile(r) for r in args.regex]
junk = re.compile(args.junk, re.I)
tool_re = re.compile(re.escape(args.match) + r"[.a-z]*\s+(search|batch_search)\b(.{0,2000})")
queries: Counter = Counter()
sessions: set = set()

for f in glob.glob(args.sessions_glob, recursive=True):
    try:
        fh = open(f, encoding="utf-8", errors="replace")
    except OSError:
        continue
    with fh:
        for line in fh:
            if args.match not in line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            m = e.get("message", {})
            content = m.get("content", []) if isinstance(m, dict) else []
            if not isinstance(content, list):
                continue
            for c in content:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "toolCall":
                    a = c.get("arguments", {})
                    txt = a.get("command", "") if isinstance(a, dict) else str(a)
                elif c.get("type") == "text":
                    txt = c.get("text", "")
                else:
                    continue
                if args.match not in txt:
                    continue
                for tm in tool_re.finditer(txt):
                    for reg in regs:
                        for q in reg.finditer(tm.group(2)):
                            queries[q.group(1)] += 1
                            sessions.add(f)

kept = [(q, n) for q, n in queries.most_common()
        if not junk.match(q.strip()) and len(q.strip()) >= args.min_len]
print(f"sessions with tool: {len(sessions)}", file=sys.stderr)
print(f"unique queries: {len(queries)} (kept {len(kept)})", file=sys.stderr)
for q, n in kept:
    print(f"{n:3d}  {q}")
