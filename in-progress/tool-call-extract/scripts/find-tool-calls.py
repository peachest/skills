#!/usr/bin/env python3
"""find-tool-calls.py — locate pi sessions calling a tool; dump paired call/result records.

Usage:
  # Search sessions for calls of a tool. Filters:
  #   --args-contains  only calls whose serialized arguments contain SUBSTR
  #                    (e.g. 'glab api' inside bash commands)
  #   --errors-only    only calls whose toolResult has isError: true
  python3 find-tool-calls.py <tool-name> [--args-contains SUBSTR] [--errors-only]
                             [--sessions-dir <dir>]

  # Dump paired call/result records for ONE session file — the artifact
  # tool-call-diagnose's axis sub-agents consume instead of the raw jsonl:
  python3 find-tool-calls.py <tool-name> --dump <session-file.jsonl>
                             [--args-contains SUBSTR] [--errors-only]
                             [--arg-chars N] [--result-chars N] [--full-args]

Session log format: ~/.pi/agent/sessions/<cwd-slug>/<timestamp>_<session-id>.jsonl
  - assistant message content block: {type: "toolCall", id, name, arguments}
  - toolResult message: {role: "toolResult", toolCallId, toolName,
                         content: [{type: "text", text}], isError, timestamp}
  Calls pair with results by id; a call with no result (session cut short)
  keeps result_entry: null and is excluded by --errors-only.

Output: JSON to stdout. Exit 0 with results (may be empty), exit 2 on bad
usage / missing paths, exit 1 when --dump's session file matches no call.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

DEFAULT_SESSIONS_DIR = Path.home() / ".pi" / "agent" / "sessions"
RECENT_WINDOW_SEC = 30 * 60


def _result_text(m: dict) -> str:
    parts = []
    for c in m.get("content", []):
        if isinstance(c, dict) and c.get("type") == "text":
            parts.append(c.get("text", ""))
    return "\n".join(parts)


def _clip(s: str, n: int | None) -> str:
    if n is None or len(s) <= n:
        return s
    return s[:n] + f"...[clipped {len(s) - n} chars]"


class SessionScan:
    """Single pass over one jsonl, pairing calls of one tool with their results."""

    def __init__(self, tool: str, substr: str | None):
        self.tool = tool
        self.substr = substr
        self.calls: dict[str, dict] = {}  # toolCallId -> call record
        self.order: list[dict] = []
        self.all_calls = 0  # every call of this tool, ignoring the substring filter
        self.session_id = None
        self.cwd = None
        self.first_ts = None
        self.last_ts = None

    def feed(self, entry_idx: int, line: str) -> None:
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            return
        ts = e.get("timestamp")
        if ts:
            self.first_ts = self.first_ts or ts
            self.last_ts = ts
        m = e.get("message")
        if not isinstance(m, dict):
            return
        role = m.get("role")
        if role == "toolResult":
            if m.get("toolName") != self.tool:
                return
            rec = self.calls.get(m.get("toolCallId"))
            if rec is not None:
                rec["result_entry"] = entry_idx
                rec["is_error"] = bool(m.get("isError"))
                rec["result"] = _result_text(m)
                rec["ts_result"] = m.get("timestamp")
        else:
            for c in m.get("content", []):
                if not (isinstance(c, dict) and c.get("type") == "toolCall"
                        and c.get("name") == self.tool):
                    continue
                self.all_calls += 1
                args = c.get("arguments")
                args_str = json.dumps(args, ensure_ascii=False) if isinstance(args, (dict, list)) else str(args)
                if self.substr and self.substr not in args_str:
                    continue
                rec = {
                    "call_entry": entry_idx,
                    "result_entry": None,
                    "id": c.get("id"),
                    "args": args_str,
                    "is_error": None,  # unknown until result arrives
                    "result": None,
                    "ts_call": ts,
                    "ts_result": None,
                }
                self.calls[c.get("id")] = rec
                self.order.append(rec)
        if e.get("type") == "session":
            self.session_id = e.get("id")
            self.cwd = e.get("cwd")

    def matches(self, errors_only: bool) -> list[dict]:
        if errors_only:
            return [r for r in self.order if r["is_error"]]
        return list(self.order)


def scan_file(path: Path, tool: str, substr: str | None, errors_only: bool):
    """Return (meta, matched_records) for one session file, or None on no match."""
    needle = f'"{tool}"'
    scan = SessionScan(tool, substr)
    try:
        with open(path, errors="replace") as f:
            for i, line in enumerate(f):
                if needle not in line:
                    continue
                scan.feed(i, line)
    except OSError:
        return None
    matched = scan.matches(errors_only)
    if not scan.all_calls:
        return None  # tool never called in this session
    total_calls = scan.all_calls
    matched_errs = [r for r in matched if r["is_error"]]
    meta = {
        "file": str(path),
        "session_id": scan.session_id,
        "cwd": scan.cwd,
        "first_timestamp": scan.first_ts,
        "last_timestamp": scan.last_ts,
        "tool_total_calls": total_calls,
        "matched_calls": len(matched),
        "matched_errors": len(matched_errs),
        "last_match_error": bool(matched_errs and matched[-1]["is_error"]),
        "sample_error_texts": [_clip(r["result"], 200) for r in matched_errs[:3]],
        "size_bytes": path.stat().st_size,
        "mtime_age_min": round((time.time() - path.stat().st_mtime) / 60, 1),
        "likely_running": (time.time() - path.stat().st_mtime) < RECENT_WINDOW_SEC,
    }
    return meta, matched


def cmd_search(args) -> None:
    root = Path(args.sessions_dir)
    if not root.is_dir():
        print(json.dumps({"error": f"sessions dir not found: {root}"}), file=sys.stderr)
        sys.exit(2)
    results = []
    for path in sorted(root.rglob("*.jsonl")):
        got = scan_file(path, args.tool, args.args_contains, args.errors_only)
        if got and got[0]["matched_calls"]:
            results.append(got[0])
    results.sort(key=lambda m: m.get("last_timestamp") or "")
    filt = {"tool": args.tool}
    if args.args_contains:
        filt["args_contains"] = args.args_contains
    if args.errors_only:
        filt["errors_only"] = True
    print(json.dumps({
        "filter": filt,
        "sessions_dir": str(root),
        "matches": len(results),
        "sessions": results,
    }, ensure_ascii=False, indent=2))


def cmd_dump(args) -> None:
    p = Path(args.dump)
    if not p.is_file():
        print(json.dumps({"error": f"session file not found: {p}"}), file=sys.stderr)
        sys.exit(2)
    got = scan_file(p, args.tool, args.args_contains, args.errors_only)
    if not got:
        print(json.dumps({"error": "no matching calls in this session",
                          "filter": {"tool": args.tool}}), file=sys.stderr)
        sys.exit(1)
    meta, matched = got
    arg_chars = None if args.full_args else args.arg_chars
    calls = []
    for r in matched:
        calls.append({
            "call_entry": r["call_entry"],
            "result_entry": r["result_entry"],
            "id": r["id"],
            "arg_len": len(r["args"]),
            "args": _clip(r["args"], arg_chars),
            "is_error": r["is_error"],
            "result": _clip(r["result"] or "", args.result_chars),
            "ts_call": r["ts_call"],
            "ts_result": r["ts_result"],
        })
    print(json.dumps({
        "file": str(p),
        "session_id": meta["session_id"],
        "filter": {"tool": args.tool,
                   "args_contains": args.args_contains,
                   "errors_only": args.errors_only},
        "matched_calls": len(calls),
        "arg_clip": (None if arg_chars is None else f"first {arg_chars} chars"),
        "calls": calls,
    }, ensure_ascii=False, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tool", nargs="?", help="tool name, e.g. bash / subagent / edit")
    ap.add_argument("--args-contains", help="only calls whose serialized args contain this substring")
    ap.add_argument("--errors-only", action="store_true", help="only calls with isError results")
    ap.add_argument("--sessions-dir", default=str(DEFAULT_SESSIONS_DIR))
    ap.add_argument("--dump", help="dump paired call/result records for this session file")
    ap.add_argument("--arg-chars", type=int, default=4000, help="clip args to N chars (dump mode)")
    ap.add_argument("--result-chars", type=int, default=1500, help="clip result text to N chars (dump mode)")
    ap.add_argument("--full-args", action="store_true", help="no args clipping (dump mode)")
    args = ap.parse_args()

    if args.dump:
        if not args.tool:
            print(json.dumps({"error": "--dump requires the tool name (positional)"}), file=sys.stderr)
            sys.exit(2)
        cmd_dump(args)
        return

    if not args.tool:
        print(json.dumps({"error": "usage: find-tool-calls.py <tool-name> [--args-contains S] [--errors-only] | --dump <file> --tool <name>"}), file=sys.stderr)
        sys.exit(2)
    cmd_search(args)


if __name__ == "__main__":
    main()
