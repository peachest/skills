#!/usr/bin/env python3
# provenance: session 01a1636b (2026-10-22), baseline in recheck/INDEX.md
# verifies: subagent (pi-subagents) tool usage portrait drift vs 2026-10-22;
#           reports, diff manually — exit 0 always (portrait, not pass/fail).
#
# Baseline lesson baked in: pi session files carry fork-inherited copies — a
# fork session duplicates the parent's whole history (same millisecond ts +
# identical args). Raw file counts overstate real calls by ~75% in fork-heavy
# windows. Dedup key = (ts, canonical args JSON). Also: isError systematically
# understates failures — async workflow runtime errors return ok "Detached"
# and flow back via subagent-notify, never touching isError.
#
# Outputs: raw vs deduped call counts, agent histogram, action histogram,
# error count, monthly trend. Writes nothing outside ~/tmp/recheck/.

import collections
import glob
import json
import os
import sys

SESSIONS_DIR = os.path.expanduser("~/.pi/agent/sessions")
OUT_DIR = os.path.expanduser("~/tmp/recheck/subagent-calls-scan")


def canon_args(args):
    return json.dumps(args, sort_keys=True, ensure_ascii=False)


def main():
    raw = dup = 0
    errors = 0
    no_result = 0
    agents = collections.Counter()
    actions = collections.Counter()
    by_month = collections.Counter()
    seen = set()

    os.makedirs(OUT_DIR, exist_ok=True)
    dump_path = os.path.join(OUT_DIR, "calls-dedup.jsonl")
    dump = open(dump_path, "w", encoding="utf-8")

    for path in sorted(glob.glob(os.path.join(SESSIONS_DIR, "*", "**", "*.jsonl"), recursive=True)):
        calls = {}
        results = {}
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    if '"subagent"' not in line:
                        continue
                    try:
                        e = json.loads(line)
                    except Exception:
                        continue
                    m = e.get("message", e)
                    if m.get("role") == "assistant":
                        for c in m.get("content", []):
                            if isinstance(c, dict) and c.get("type") == "toolCall" and c.get("name") == "subagent":
                                calls[c.get("id")] = {
                                    "args": c.get("arguments") or {},
                                    "ts": e.get("timestamp") or m.get("timestamp"),
                                }
                    elif m.get("role") == "toolResult" and m.get("toolName") == "subagent":
                        results[m.get("toolCallId")] = m
        except Exception:
            continue
        for cid, call in calls.items():
            raw += 1
            key = (call["ts"], canon_args(call["args"]))
            if key in seen:
                dup += 1
                continue
            seen.add(key)
            r = results.get(cid)
            is_err = bool(r and r.get("isError"))
            if r is None:
                no_result += 1
            elif is_err:
                errors += 1
            a = call["args"]
            if a.get("agent"):
                agents[a["agent"]] += 1
            if a.get("action"):
                actions[a["action"]] += 1
            by_month[(call["ts"] or "")[:7]] += 1
            dump.write(json.dumps({
                "file": os.path.basename(path), "ts": call["ts"],
                "args": a, "isError": is_err,
            }, ensure_ascii=False) + "\n")
    dump.close()

    unique = raw - dup
    print(f"subagent toolCall: raw={raw} deduped={unique} (fork-inherited dup={dup})")
    print(f"errors (isError only — async runtime failures invisible): {errors}  no_result: {no_result}")
    print(f"dump: {dump_path}")
    print("\n== top agents (deduped) ==")
    for k, n in agents.most_common(15):
        print(f"{n:5d}  {k}")
    print("\n== top actions (deduped) ==")
    for k, n in actions.most_common(10):
        print(f"{n:5d}  {k}")
    print("\n== by month (deduped) ==")
    for k in sorted(by_month):
        print(f"{k}: {by_month[k]}")

    # Portrait script: report-only. Exit 0 regardless; compare manually.
    return 0


if __name__ == "__main__":
    sys.exit(main())
