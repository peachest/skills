#!/usr/bin/env python3
"""mine-herdr-ops — audit herdr CLI usage over pi session logs.

Answers: which subcommands are frequent, which fail, and what the failure
classes are (envelope parse vs quoting vs stale addressing vs user-aborts).
Built 2026-09-20 from a ~1100-call / 146-session audit that motivated the
scripts/herdr-* tools; re-run to diff against that baseline
(see mining-evidence-2026-09-20.md).

Usage:
  mine-herdr-ops.py [--sessions-dir DIR] [--top N] [--json]

Output: per-subcommand table (calls/errs/err%/sessions) + per-op-class table
+ error samples. Standalone, py3 only, no deps.
"""
import argparse, glob, json, os, re
from collections import defaultdict, Counter

UUID_RE = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')


def subcmd(cmd):
    """Extract 'herdr <sub> [<sub2>]' from a bash command line."""
    for m in re.finditer(r'(?<![\w./-])herdr\s+(.*)', cmd):
        parts = m.group(1).split()
        while parts and parts[0].startswith('-'):
            parts = parts[1:]
        sc = []
        for p in parts:
            if p in ('|', '&&', ';', '>') or '|' in p or '&&' in p:
                break
            sc.append(p.strip('"\''))
            if len(sc) == 2:
                break
        return " ".join(sc) if sc else "herdr(bare)"
    return None


def op_class(cmd):
    """Coarser classification: what was the agent trying to do."""
    if 'herdr agent list' in cmd and UUID_RE.search(cmd):
        return 'resolve: agent list with UUID'
    if 'agent_session' in cmd and 'herdr' in cmd:
        return 'resolve: agent_session field parse'
    if 'HERDR_PANE_ID' in cmd:
        return 'resolve: self address'
    if 'herdr agent prompt' in cmd and 'python' in cmd:
        return 'send: prompt via python wrapper'
    if 'herdr agent prompt' in cmd:
        return 'send: herdr agent prompt direct'
    if re.search(r'herdr agent (get|read|wait)', cmd):
        return 'verify: agent get/read/wait'
    if re.search(r'herdr (workspace|pane) create', cmd):
        return 'create: workspace/pane'
    return None


def scan(sessions_dir):
    files = glob.glob(os.path.join(sessions_dir, "**", "*.jsonl"), recursive=True)
    sub_stats = defaultdict(lambda: {"n": 0, "err": 0, "samples": [], "sessions": set()})
    cls_stats = defaultdict(lambda: {"calls": 0, "err": 0})
    list_shapes = Counter()
    total = 0

    for f in files:
        calls, results = {}, []   # callId -> (subcmd, class)
        try:
            with open(f, encoding="utf-8", errors="ignore") as fh:
                for line in fh:
                    if 'herdr' not in line and '"toolResult"' not in line:
                        continue
                    try:
                        e = json.loads(line)
                    except Exception:
                        continue
                    if e.get("type") != "message":
                        continue
                    m = e.get("message") or {}
                    if m.get("role") == "assistant":
                        for c in (m.get("content") or []):
                            if isinstance(c, dict) and c.get("type") == "toolCall" \
                                    and c.get("name") == "bash":
                                cmd = (c.get("arguments") or {}).get("command", "")
                                sc = subcmd(cmd)
                                if sc:
                                    k = op_class(cmd)
                                    calls[c.get("id")] = (sc, k)
                                    if k:
                                        cls_stats[k]["calls"] += 1
                                    if 'herdr agent list' in cmd:
                                        if '| grep' in cmd or 'python' in cmd or 'jq' in cmd:
                                            list_shapes['piped-to-parser'] += 1
                                        elif '|' not in cmd:
                                            list_shapes['bare'] += 1
                                        else:
                                            list_shapes['other/complex'] += 1
                    elif m.get("role") == "toolResult":
                        cid = m.get("toolCallId")
                        if cid in calls:
                            text = " ".join(x.get("text", "") for x in
                                            (m.get("content") or []) if isinstance(x, dict))
                            results.append((cid, bool(m.get("isError")), text))
        except Exception:
            continue
        for cid, is_err, text in results:
            sc, k = calls[cid]
            total += 1
            s = sub_stats[sc]
            s["n"] += 1
            s["sessions"].add(os.path.basename(f)[:20])
            if is_err:
                s["err"] += 1
                if k:
                    cls_stats[k]["err"] += 1
                if len(s["samples"]) < 4:
                    s["samples"].append(text[:200].replace("\n", " | "))
    return total, sub_stats, cls_stats, list_shapes, len(files)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions-dir", default=os.path.expanduser("~/.pi/agent/sessions"))
    ap.add_argument("--top", type=int, default=35)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    total, sub_stats, cls_stats, list_shapes, nfiles = scan(args.sessions_dir)
    rows = sorted(sub_stats.items(), key=lambda kv: (-kv[1]["err"], -kv[1]["n"]))

    if args.json:
        print(json.dumps({
            "sessions_scanned": nfiles, "total_paired_calls": total,
            "agent_list_shapes": dict(list_shapes),
            "subcommands": {k: {"n": v["n"], "err": v["err"], "samples": v["samples"]}
                            for k, v in rows},
            "op_classes": {k: dict(v) for k, v in cls_stats.items()},
        }, ensure_ascii=False, indent=2))
        return

    print(f"{'subcommand':<32} {'calls':>5} {'errs':>5} {'err%':>5} {'sess':>5}")
    for sc, s in rows[:args.top]:
        print(f"{sc:<32} {s['n']:>5} {s['err']:>5} {100*s['err']/max(s['n'],1):>4.0f}% {len(s['sessions']):>5}")
    print(f"\nTOTAL paired herdr bash calls: {total} across {nfiles} sessions")
    print(f"agent list shapes: {dict(list_shapes)}")
    print("\n=== op classes (calls / errors) ===")
    for k, v in sorted(cls_stats.items(), key=lambda kv: -kv[1]["calls"]):
        print(f"{k:<38} {v['calls']:>5} {v['err']:>5}")
    print("\n=== top error samples ===")
    for sc, s in rows[:14]:
        if s["samples"]:
            print(f"\n[{sc}] err={s['err']}/{s['n']}")
            for t in s["samples"][:2]:
                print("  -", t[:170])


if __name__ == "__main__":
    main()
