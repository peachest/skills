#!/usr/bin/env python3
"""doc-usage.py — did the agent actually consume these project docs?

Two subcommands:

  matrix  — scan session logs, count per-target hits classified as
            READ-like / WRITE-like / MENTION. Verdict hints per target
            ("only maintained, never read" = sediment).
            Includes an escape-rate check: sessions showing action
            signatures (e.g. nvidia-smi) without ever touching a target.

  echo    — consumption verification beyond the read call: sample
            distinctive tokens from the doc file on disk, then check
            whether assistant text/thinking blocks echo them. A read
            call alone is weak evidence; an echo is strong.

Why not just count `read` tool calls: in real projects bash cat/grep
outnumbers the read tool by ~40x, and agents fall back to python one-
liners to edit files when `edit` fails. Both channels are classified
here. Session discovery is recursive (forks/, run-0/ subdirs included).

Usage:
  # matrix over a sessions dir, targets as substrings:
  python3 doc-usage.py matrix --sessions-dir DIR --patterns 'CONTEXT.md,gpu-ledger'

  # or a TSV targets file: name<TAB>pattern (pattern may contain | alternation)
  python3 doc-usage.py matrix --sessions-dir DIR --targets targets.tsv

  # escape check: action signature without target touch
  python3 doc-usage.py matrix ... --escape 'nvidia-smi|torchrun' --escape-min 3

  # consumption echo check for one doc:
  python3 doc-usage.py echo --doc /path/DOC.md --sessions-dir DIR --target 'DOC.md'

Output: JSON to stdout (--json) or a human table (default).
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

READ_TOOLS = {"read", "ctx_execute_file", "ctx_execute"}
WRITE_TOOLS = {"write", "edit"}

# bash prefixes that read a file
READ_BASH = ("cat ", "head ", "grep ", "rg ", "sed -n", "less ", "wc ", "tail ",
             "awk ", "find ", "ls ", "stat ", "diff ", "jq ", "yq ", "bat ")
# bash markers that write/mutate a file (checked first: a command can both read and write)
WRITE_BASH = ("sed -i", "perl -i", "tee ", "patch ", "> ", ">>", "mv ", "cp ",
              "rsync ", "touch ", "truncate ", "install ", "dd ")
HEREDOC_WRITE = (">", "<<")  # 'cat > f' / heredoc — write only when a redirect precedes target use

# python one-liner fallbacks inside bash: edit/read markers
PY_WRITE = (".replace(", "write_text", "write(", "'w'", '"w"', "shutil.", "os.rename",
            "os.replace", "makedirs", "remove(", "unlink(")
PY_READ = (".read(", "readlines", "read_text", "open(", "glob.", "json.load", "re.findall")

TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_-]{3,}|[\u4e00-\u9fff]{4,}")


def classify_bash(cmd: str) -> str:
    """Classify a bash command's intent toward whatever it names: read|write|mention."""
    # python fallback: agent edits via python when edit fails, or reads via python
    if re.search(r"\bpytho?n3?\b", cmd):
        if any(m in cmd for m in PY_WRITE):
            return "write"
        if any(m in cmd for m in PY_READ):
            return "read"
        return "mention"
    if any(m in cmd for m in WRITE_BASH):
        return "write"
    if "cat >" in cmd or "<<'EOF'" in cmd or '<<"EOF"' in cmd:
        return "write"
    if cmd.lstrip().startswith(READ_BASH):
        return "read"
    if any(m in cmd for m in READ_BASH):
        return "read"
    return "mention"


def iter_sessions(root: str) -> list[str]:
    """All session jsonl files under root, recursive — catches forks/ and run-0/."""
    return sorted(glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True))


def iter_tool_calls(path: str):
    """Yield (entry_idx, tool_name, args_dict, call_id) for every toolCall block."""
    with open(path, errors="replace") as fh:
        for i, line in enumerate(fh):
            if '"toolCall"' not in line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            m = e.get("message")
            if not isinstance(m, dict):
                continue
            for c in m.get("content", []):
                if isinstance(c, dict) and c.get("type") == "toolCall":
                    yield i, c.get("name") or "?", c.get("arguments") or {}, c.get("id")


def iter_texts(path: str, roles=("assistant",)):
    """Yield (entry_idx, role, kind, text) for text/thinking blocks of given roles."""
    with open(path, errors="replace") as fh:
        for i, line in enumerate(fh):
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            m = e.get("message")
            if not isinstance(m, dict) or m.get("role") not in roles:
                continue
            for c in m.get("content", []):
                if isinstance(c, dict) and c.get("type") in ("text", "thinking"):
                    yield i, m.get("role"), c.get("type"), c.get("text", "")


def load_targets(args) -> dict[str, list[str]]:
    if args.targets:
        targets = {}
        for ln in open(args.targets, errors="replace"):
            ln = ln.rstrip("\n")
            if not ln or ln.startswith("#"):
                continue
            name, _, pat = ln.partition("\t")
            targets[name.strip()] = [pat.strip()]
        return targets
    if args.patterns:
        return {p: [p] for p in args.patterns.split(",") if p}
    sys.exit(json.dumps({"error": "need --patterns or --targets"}))


def scan_matrix(session_files: list[str], targets: dict[str, list[str]],
                escape: str | None, escape_min: int) -> dict:
    stats = {t: Counter() for t in targets}
    sess_by_target = {t: set() for t in targets}
    read_with_result = {t: 0 for t in targets}
    escape_hits = []  # (file, sig_count, target_hits) where sig present, target absent

    for f in session_files:
        target_seen = {t: False for t in targets}
        sig_count = 0
        # pass 1: tool calls
        calls = list(iter_tool_calls(f))
        for _, tool, args_, _cid in calls:
            blob = json.dumps(args_, ensure_ascii=False)
            cmd = args_.get("command", "") if tool == "bash" else ""
            for t, pats in targets.items():
                hit = any(p in blob for p in pats) or (cmd and any(p in cmd for p in pats))
                if not hit:
                    continue
                if tool in WRITE_TOOLS or (tool == "bash" and classify_bash(cmd) == "write"):
                    stats[t]["WRITE"] += 1
                elif tool in READ_TOOLS or (tool == "bash" and classify_bash(cmd) == "read"):
                    stats[t]["READ"] += 1
                else:
                    stats[t]["MENTION"] += 1
                sess_by_target[t].add(os.path.basename(f))
                target_seen[t] = True  # any touch (even write) = not an escape
        # read hits need result evidence: pair via the paired-result pass
        results = {}
        with open(f, errors="replace") as fh:
            for line in fh:
                if '"toolResult"' not in line:
                    continue
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue
                m = e.get("message")
                if isinstance(m, dict) and m.get("role") == "toolResult":
                    txt = "\n".join(c.get("text", "") for c in m.get("content", [])
                                    if isinstance(c, dict) and c.get("type") == "text")
                    results[m.get("toolCallId")] = bool(txt.strip())
        for _, tool, args_, cid in calls:
            cmd = args_.get("command", "") if tool == "bash" else ""
            is_read = tool in READ_TOOLS or (tool == "bash" and classify_bash(cmd) == "read")
            if not is_read:
                continue
            blob = json.dumps(args_, ensure_ascii=False)
            for t, pats in targets.items():
                hit = any(p in blob for p in pats) or (cmd and any(p in cmd for p in pats))
                if hit and cid and results.get(cid):
                    read_with_result[t] += 1
        if escape:
            with open(f, errors="replace") as fh:
                body = fh.read()
            sig_count = len(re.findall(escape, body))
            if sig_count > escape_min and not any(target_seen.values()):
                escape_hits.append({"file": os.path.relpath(f), "sig_count": sig_count})

    per_target = []
    for t, c in stats.items():
        read, write = c["READ"], c["WRITE"]
        verdict = ""
        if read == 0 and write > 0:
            verdict = "only-maintained (fake-useful)"
        elif read == 0 and c["MENTION"] == 0:
            verdict = "never-touched"
        elif read < 3 and write >= read:
            verdict = "weak-read"
        elif read >= 3:
            verdict = "consumed"
        per_target.append({
            "target": t, "READ": read, "WRITE": write, "MENTION": c["MENTION"],
            "sessions": len(sess_by_target[t]),
            "read_with_result": read_with_result[t],
            "verdict": verdict,
        })
    return {"files": len(session_files), "targets": per_target, "escapes": escape_hits}


def distinctive_tokens(doc_text: str, limit: int = 200) -> list[str]:
    """Tokens frequent enough to be real, rare enough to be distinctive."""
    counts = Counter(m.group(0).lower() for m in TOKEN_RE.finditer(doc_text))
    real = [t for t, n in counts.items() if n >= 2 and len(t) >= 4]
    real.sort(key=lambda t: counts[t])  # rarest first — least likely to appear by chance
    return real[:limit]


def scan_echo(session_files: list[str], target: str, doc_path: str) -> dict:
    doc_text = Path(doc_path).read_text(errors="replace")
    tokens = distinctive_tokens(doc_text)
    lowered = [t.lower() for t in tokens]
    events = []
    no_read_anchor = 0
    for f in session_files:
        read_entries, any_entries = [], []
        for i, tool, a, _ in iter_tool_calls(f):
            blob = json.dumps(a, ensure_ascii=False)
            if target not in blob:
                continue
            any_entries.append(i)
            cmd = a.get("command", "") if tool == "bash" else ""
            if tool in READ_TOOLS or (tool == "bash" and classify_bash(cmd) == "read"):
                read_entries.append(i)
        if not any_entries:
            continue
        # anchor on a read-like event; an any-touch anchor would let a write-only
        # session echo its own content (false positive)
        anchored, kind = (min(read_entries), "read-like") if read_entries else (None, None)
        if anchored is None:
            no_read_anchor += 1
            continue
        echoed, samples = set(), []
        for i, role, kind_, text in iter_texts(f):
            if i < anchored:
                continue  # echo only counts after the first read-like touch
            low = text.lower()
            hit = [t for t in lowered if t in low]
            if hit:
                echoed.update(hit)
                samples.append({"entry": i, "role": role, "kind": kind_,
                                "matched": hit[:5], "ts": None})
        if echoed:
            events.append({
                "file": os.path.relpath(f),
                "first_target_entry": anchored,
                "anchor": kind,
                "echoed_tokens": len(echoed),
                "token_coverage": round(len(echoed) / max(len(lowered), 1), 3),
                "samples": samples[:3],
            })
    events.sort(key=lambda e: -e["echoed_tokens"])
    verdict = "consumed (echo evidence)" if events and events[0]["token_coverage"] >= 0.05 \
        else "weak-echo" if events else "no-echo-evidence"
    return {"doc": doc_path, "target": target, "tokens_sampled": len(lowered),
            "sessions_with_echo": len(events),
            "sessions_touch_but_no_read": no_read_anchor,
            "verdict": verdict, "events": events}


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("matrix")
    m.add_argument("--sessions-dir", required=True)
    m.add_argument("--patterns", help="comma-separated target substrings")
    m.add_argument("--targets", help="TSV file: name<TAB>pattern")
    m.add_argument("--escape", help="regex of action signatures (e.g. 'nvidia-smi|torchrun')")
    m.add_argument("--escape-min", type=int, default=3)
    m.add_argument("--json", action="store_true")

    e = sub.add_parser("echo")
    e.add_argument("--doc", required=True, help="path to the actual doc file on disk")
    e.add_argument("--sessions-dir", required=True)
    e.add_argument("--target", required=True, help="substring identifying the doc in tool args")
    e.add_argument("--json", action="store_true")

    args = ap.parse_args()
    files = iter_sessions(args.sessions_dir)
    if not files:
        sys.exit(json.dumps({"error": f"no jsonl under {args.sessions_dir}"}))
    if args.cmd == "matrix":
        out = scan_matrix(files, load_targets(args), args.escape, args.escape_min)
    else:
        out = scan_echo(files, args.target, args.doc)
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        if args.cmd == "matrix":
            print(f"jsonl files (nested included): {out['files']}\n")
            print(f"  {'target':<28}{'READ':>6}{'WRITE':>7}{'MENTION':>9}{'sess':>6}{'read+res':>10}  verdict")
            for t in out["targets"]:
                print(f"  {t['target']:<28}{t['READ']:>6}{t['WRITE']:>7}{t['MENTION']:>9}"
                      f"{t['sessions']:>6}{t['read_with_result']:>10}  {t['verdict']}")
            if out["escapes"]:
                print(f"\nescape-rate hits (action w/o any target): {len(out['escapes'])}")
                for x in out["escapes"][:10]:
                    print(f"  {x['file']}  sig={x['sig_count']}")
        else:
            r = out
            print(f"doc: {r['doc']}  target: {r['target']}  tokens: {r['tokens_sampled']}")
            print(f"verdict: {r['verdict']}  sessions with echo: {r['sessions_with_echo']}")
            for ev in r["events"][:10]:
                print(f"  {ev['file']}  entry>={ev['first_target_entry']}  "
                      f"echoed={ev['echoed_tokens']} cov={ev['token_coverage']}")


if __name__ == "__main__":
    main()
