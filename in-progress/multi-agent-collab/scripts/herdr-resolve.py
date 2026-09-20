#!/usr/bin/env python3
"""herdr-resolve — resolve a peer address from any known fragment.

Input: session UUID (full or >=8-char prefix), session jsonl path, pane id,
cwd fragment, or terminal-title fragment. Output: canonical JSON of ALL matching
panes (one session may be attached to several panes).

Runtime-aware: herdr supports multiple named persistent runtimes (default/dev/agent,
`herdr session list`). By default ALL running runtimes are queried and every match
carries its `runtime` field (global addressing); --runtime <name> narrows to one.
Pane ids are runtime-local — the same "w1:p2" can exist in two runtimes (pitfall #27).

Exit codes: 0 found · 1 no match · 2 herdr error · 3 usage.

Replaces the error-prone inline pattern:
    herdr agent list | python3 -c "... parse envelope ... match agent_session.value"
which crashed for months on error envelopes (pitfalls #5/#7: KeyError 'result'/'agents').
"""
import json, os, re, subprocess, sys

HERDR = os.environ.get("HERDR_BIN", "herdr")


def fail(code, msg):
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(code)


def list_runtimes():
    try:
        raw = subprocess.run([HERDR, "session", "list"], capture_output=True,
                             text=True, timeout=30).stdout
    except subprocess.TimeoutExpired:
        fail(2, "herdr session list timed out")
    names = []
    for line in raw.splitlines():
        m = re.match(r'^(\S+)\s+(\S+)\s+', line)
        if m and m.group(2) == "running":
            names.append(m.group(1))
    return names or ["default"]


def query_runtime(runtime, query):
    # ALWAYS pass --session explicitly: a bare `herdr` follows HERDR_SOCKET_PATH,
    # which points at the CURRENT runtime — the "default" runtime would never be
    # queried from inside another runtime (bug found 2026-09-20: peer in agent
    # runtime resolved nothing because "default" silently aliased to agent).
    cmd = [HERDR, "--session", runtime, "agent", "list"]
    try:
        raw = subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout
    except subprocess.TimeoutExpired:
        return None, f"agent list timed out on runtime '{runtime}'"
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        return None, f"non-JSON from runtime '{runtime}': {raw[:200]}"
    if "error" in d:
        return None, f"herdr error on runtime '{runtime}': {d['error'].get('message', d['error'])}"
    agents = (d.get("result") or {}).get("agents")
    if agents is None:
        return None, f"unexpected envelope from runtime '{runtime}': {raw[:200]}"

    ql = query.lower()
    matches = []
    for a in agents:
        session_value = (a.get("agent_session") or {}).get("value", "")
        haystacks = {
            "pane_id": a.get("pane_id", ""),
            "workspace_id": a.get("workspace_id", ""),
            "tab_id": a.get("tab_id", ""),
            "cwd": a.get("cwd", ""),
            "terminal_title": a.get("terminal_title", ""),
            "agent_session": session_value,
        }
        where = [k for k, v in haystacks.items() if ql in v.lower()]
        if not where:
            continue
        m = {"runtime": runtime}
        m.update({k: a.get(k) for k in ("pane_id", "workspace_id", "tab_id", "cwd",
                                        "agent_status", "revision", "state_change_seq",
                                        "terminal_title")})
        m["session_uuid"] = ""
        mu = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
                       session_value)
        if mu:
            m["session_uuid"] = mu.group(1)
        m["session_jsonl"] = session_value
        m["matched_by"] = where
        matches.append(m)
    return matches, None


def main():
    argv = sys.argv[1:]
    full = "--full" in argv
    runtime = None
    if "--runtime" in argv:
        i = argv.index("--runtime")
        if i + 1 >= len(argv):
            fail(3, "--runtime requires a name (see: herdr session list)")
        runtime = argv[i + 1]
        del argv[i:i + 2]
    argv = [a for a in argv if a not in ("--all-runtimes", "--full")]  # --all-runtimes is now the default; accepted for compat
    if len(argv) != 1:
        print("usage: herdr-resolve.py <uuid|pane|cwd|title-fragment> "
              "[--runtime NAME] [--full]", file=sys.stderr)
        sys.exit(3)
    query = argv[0]

    runtimes = [runtime] if runtime else list_runtimes()
    matches, errors = [], []
    for rt in runtimes:
        res, err = query_runtime(rt, query)
        if err:
            errors.append(err)
        else:
            matches.extend(res)

    out = {"query": query, "runtimes_queried": runtimes,
           "count": len(matches), "matches": matches}
    if errors:
        out["errors"] = errors
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if not matches:
        # single-runtime query with a hard error → herdr problem (exit 2);
        # multi-runtime scan tolerates one down runtime (exit 1, errors in output)
        sys.exit(2 if errors and len(runtimes) == 1 else 1)


if __name__ == "__main__":
    main()
