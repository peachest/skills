#!/usr/bin/env python3
"""find-skill-sessions.py — locate pi sessions that invoked a given skill.

Usage:
  # Find every session that invoked the skill (marker = skill injection tag):
  python3 find-skill-sessions.py <skill-name> [--sessions-dir <dir>] [--json]

  # Resolve one explicit session id (reports even without the marker —
  # the user already knows it ran the skill):
  python3 find-skill-sessions.py <skill-name> --session <id-or-prefix>

  # Compact per-entry trace index for ONE session file (pass to analysis
  # sub-agents so they never read the raw multi-MB jsonl):
  python3 find-skill-sessions.py --index <session-file.jsonl>

Session log format: ~/.pi/agent/sessions/<cwd-slug>/<timestamp>_<session-id>.jsonl
The skill injection lives inside a JSON string, so the marker is the
backslash-escaped form `<skill name=\\"NAME\\"` — the raw string
`<skill name="NAME"` also matches when markers appear unescaped.

Output: JSON array (stdout), sorted by last activity. Exit 0 with results
(may be empty), exit 2 on bad usage / missing sessions dir.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

DEFAULT_SESSIONS_DIR = Path.home() / ".pi" / "agent" / "sessions"
RECENT_WINDOW_SEC = 30 * 60  # mtime within 30 min → likely still running


def scan_session_file(path: Path) -> dict | None:
    """Single pass over one session jsonl: collect header + trace stats."""
    meta: dict = {"file": str(path)}
    marker_count = 0
    first_ts = last_ts = None
    session_id = cwd = None
    msg_counts: dict[str, int] = {}
    tool_hist: dict[str, int] = {}
    usage = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}
    entry_count = 0

    try:
        fh = open(path, errors="replace")
    except OSError:
        return None
    with fh:
        for line in fh:
            entry_count += 1
            if '"<skill name=' in line or "<skill name=" in line:
                # Marker detection is done by the caller against the raw line
                # (needs the skill name); here we only note candidates cheaply.
                pass
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = e.get("timestamp")
            if ts:
                if first_ts is None:
                    first_ts = ts
                last_ts = ts
            t = e.get("type")
            if t == "session":
                session_id = e.get("id")
                cwd = e.get("cwd")
            elif t == "message":
                m = e.get("message", {})
                role = m.get("role", "?")
                msg_counts[role] = msg_counts.get(role, 0) + 1
                u = m.get("usage") or {}
                for k in usage:
                    usage[k] += u.get(k) or 0
                for c in m.get("content", []):
                    if isinstance(c, dict) and c.get("type") == "toolCall":
                        name = c.get("name", "?")
                        tool_hist[name] = tool_hist.get(name, 0) + 1

    mtime = path.stat().st_mtime
    meta.update({
        "session_id": session_id,
        "cwd": cwd,
        "first_timestamp": first_ts,
        "last_timestamp": last_ts,
        "entries": entry_count,
        "messages": msg_counts,
        "tool_calls": dict(sorted(tool_hist.items(), key=lambda kv: -kv[1])),
        "usage": usage,
        "size_bytes": path.stat().st_size,
        "mtime_age_min": round((time.time() - mtime) / 60, 1),
        "likely_running": (time.time() - mtime) < RECENT_WINDOW_SEC,
    })
    return meta


def marker_hits(path: Path, markers: list[str]) -> int:
    """Count lines containing any raw marker string (escaped or plain)."""
    hits = 0
    with open(path, errors="replace") as f:
        for line in f:
            if any(m in line for m in markers):
                hits += 1
    return hits


def cmd_index(path: Path, cap: int = 600) -> None:
    """Per-entry one-line index: the map analysis sub-agents navigate with."""
    lines: list[str] = []
    truncated = False
    with open(path, errors="replace") as f:
        for i, line in enumerate(f):
            if len(lines) >= cap:
                truncated = True
                break
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = e.get("type", "?")
            ts = (e.get("timestamp") or "")[11:19]  # HH:MM:SS
            desc = t
            if t == "message":
                m = e.get("message", {})
                role = m.get("role", "?")
                parts = []
                for c in m.get("content", []):
                    if not isinstance(c, dict):
                        continue
                    ct = c.get("type")
                    if ct == "text":
                        parts.append(f"text:{len(c.get('text', ''))}")
                    elif ct == "thinking":
                        parts.append("think")
                    elif ct == "toolCall":
                        args = c.get("arguments") or {}
                        parts.append(f"CALL {c.get('name', '?')} argLen={len(json.dumps(args))}")
                    elif ct == "toolResult":
                        parts.append(f"RESULT len={len(str(c.get('content', '')))}")
                u = m.get("usage") or {}
                us = f" in={u.get('input', 0)} cacheR={u.get('cacheRead', 0)} out={u.get('output', 0)}" if role == "assistant" else ""
                desc = f"msg[{role}] {' | '.join(parts)}{us}"
            lines.append(f"[{i}] {ts} {desc}")
    print(json.dumps({"file": str(path), "entries_indexed": len(lines),
                      "truncated": truncated, "index": lines}, ensure_ascii=False))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_name", nargs="?", help="skill name as written in its SKILL.md frontmatter")
    ap.add_argument("--session", help="explicit session id or filename prefix")
    ap.add_argument("--sessions-dir", default=str(DEFAULT_SESSIONS_DIR))
    ap.add_argument("--index", help="print per-entry trace index for this session file instead of searching")
    args = ap.parse_args()

    if args.index:
        p = Path(args.index)
        if not p.is_file():
            print(json.dumps({"error": f"session file not found: {p}"}), file=sys.stderr)
            sys.exit(2)
        cmd_index(p)
        return

    if not args.skill_name:
        print(json.dumps({"error": "usage: find-skill-sessions.py <skill-name> [--session <id>] | --index <file>"}), file=sys.stderr)
        sys.exit(2)

    root = Path(args.sessions_dir)
    if not root.is_dir():
        print(json.dumps({"error": f"sessions dir not found: {root}"}), file=sys.stderr)
        sys.exit(2)

    # Raw markers to search in file text: JSON-escaped and plain forms.
    markers = [f'<skill name=\\"{args.skill_name}\\"', f'<skill name="{args.skill_name}"']

    results = []
    explicit_hit = False
    for path in sorted(root.rglob("*.jsonl")):
        if args.session:
            if args.session not in path.name:
                continue
            explicit_hit = True
            meta = scan_session_file(path)
            if meta:
                meta["marker_count"] = marker_hits(path, markers)
                meta["selected_via"] = "explicit-id"
                results.append(meta)
            continue
        # cheap prefilter: marker must appear somewhere in the file
        text_ok = False
        with open(path, errors="replace") as f:
            for line in f:
                if any(m in line for m in markers):
                    text_ok = True
                    break
        if not text_ok:
            continue
        meta = scan_session_file(path)
        if meta:
            meta["marker_count"] = marker_hits(path, markers)
            meta["selected_via"] = "marker"
            results.append(meta)

    if args.session and not explicit_hit:
        print(json.dumps({"error": f"no session file matches id/prefix: {args.session}"}), file=sys.stderr)
        sys.exit(1)

    results.sort(key=lambda m: m.get("last_timestamp") or "")
    print(json.dumps({
        "skill": args.skill_name,
        "sessions_dir": str(root),
        "matches": len(results),
        "sessions": results,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
