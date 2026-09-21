#!/usr/bin/env python3
"""herdr-send — deliver a prompt to a peer pane with quoting + envelope + receipt handled.

  herdr-send.py <pane-id> <message-file | -> [--steer] [--wait MS] [--runtime NAME]
                 [--from "name (pane)"]

FollowUp is the DEFAULT: poll the peer until idle/done (bounded, default 30min,
HERDR_FOLLOWUP_MS to override), then deliver as a clean new task. Designed to run
under bg_run — the whole command blocks until delivery, the agent turn stays free.
Timeout: exit 4, message NOT sent. Pass --steer to skip the gate and deliver
immediately mid-task — for corrections/blockers/answers where you WANT it seen now
(pitfall #24).

Message is read from a file (temp-file two-step quoting built in — pitfalls #1/#3) or
stdin ('-'). The reply envelope is parsed with error-first branching (pitfall #5) and a
machine-checkable receipt is printed on stdout.

Exit codes: 0 delivered · 1 usage · 2 herdr error / bad envelope · 3 rejected
(agent_blocked etc. — inspect the peer's UI, do not resend, pitfall #13) ·
4 followup timeout (peer still busy, not sent).

Note: a --wait timeout is reported as timeout, NOT failure — the message is already
queued in the peer's steering queue (pitfall #11); recovery is agent get + read.
"""
import json, os, re, subprocess, sys

HERDR = os.environ.get("HERDR_BIN", "herdr")


def fail(code, msg):
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(code)


def main():
    args = sys.argv[1:]
    wait_ms = None
    echo_reply = "--echo-reply-cmd" in args
    runtime = None
    followup = "--steer" not in args  # followUp is the default; --steer opts out
    args = [a for a in args if a not in ("--echo-reply-cmd", "--steer")]
    if "--runtime" in args:
        i = args.index("--runtime")
        if i + 1 >= len(args):
            fail(1, "--runtime requires a name (see: herdr session list)")
        runtime = args[i + 1]
        del args[i:i + 2]
    if "--wait" in args:
        i = args.index("--wait")
        if i + 1 >= len(args):
            fail(1, "--wait requires a millisecond value (pitfall #12: it is a valued flag)")
        wait_ms = args[i + 1]
        del args[i:i + 2]
    from_id = None
    if "--from" in args:
        i = args.index("--from")
        if i + 1 >= len(args):
            fail(1, '--from requires "name (pane)" — the pane lets the peer reply')
        from_id = args[i + 1]
        del args[i:i + 2]
    if len(args) != 2:
        print("usage: herdr-send.py <pane-id> <message-file | -> [--steer] [--wait MS] "
              "[--runtime NAME] [--from \"name (pane)\"]", file=sys.stderr)
        sys.exit(1)
    target, source = args

    if from_id:
        # protocol shape guard (pitfall #28): prepend the caller-identity section
        # so improvised dispatches can't drop it; reply path comes from the pane.
        mm = re.search(r'\(([^)]+)\)', from_id)
        pane = mm.group(1) if mm else "?"

    if source == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(source, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as ex:
            fail(1, f"cannot read message file: {ex}")
    if not text.strip():
        fail(1, "empty message")
    if from_id:
        # protocol shape guard (pitfall #28): identity + reply path must both land.
        # Fail fast on a pane-less --from: the reply command would be unwritable.
        mm = re.search(r'\(([^)]+)\)', from_id)
        if not mm:
            fail(1, f'--from must be "name (pane)" — got {from_id!r} without a pane; '
                    'the peer could not reply')
        pane = mm.group(1)
        text = (f"[caller identity] I am {from_id}; reach me at pane {pane}\n\n"
                + text
                + f"\n\n[output + reply] reply via: herdr agent prompt {pane} \"<summary + artifact path>\"")

    session_args = ["--session", runtime] if runtime else []

    if followup:  # followUp: idle/done gate BEFORE send (pitfall #24 mitigation)
        fu_ms = int(os.environ.get("HERDR_FOLLOWUP_MS", "1800000"))
        wcmd = [HERDR] + session_args + ["agent", "wait", target,
               "--until", "idle", "--until", "done", "--timeout", str(fu_ms)]
        try:
            w = subprocess.run(wcmd, capture_output=True, text=True,
                               timeout=fu_ms / 1000 + 60)
        except subprocess.TimeoutExpired:
            fail(4, f"bash-level timeout during followup wait ({fu_ms}ms)")
        try:
            wd = json.loads(w.stdout.strip() or w.stderr.strip())
        except json.JSONDecodeError:
            fail(2, f"non-JSON from agent wait: {(w.stdout or w.stderr)[:300]}")
        if "error" in wd:  # error-first (pitfall #5); note: `wait` exits 0 even on error
            wcode = (wd["error"] or {}).get("code", "")
            if wcode == "timeout":
                fail(4, f"peer still busy after {fu_ms}ms — NOT sent; pass --steer to "
                        "deliver mid-task deliberately")
            fail(2, f"agent wait error: {wd['error'].get('message', wd['error'])}")

    cmd = [HERDR]
    if runtime:
        cmd += ["--session", runtime]   # cross-runtime: pane ids are runtime-local (pitfall #27)
    cmd += ["agent", "prompt", target, text]
    if wait_ms is not None:
        cmd += ["--wait", "--timeout", str(wait_ms)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=(int(wait_ms) / 1000 + 60) if wait_ms else 60)
    except subprocess.TimeoutExpired:
        # bash-level timeout, not a delivery verdict: message is queued (pitfall #11)
        print(json.dumps({"delivered": "unknown", "reason": "bash timeout while waiting",
                          "recovery": "herdr agent get <target> + agent read"}))
        sys.exit(0)

    raw = proc.stdout.strip() or proc.stderr.strip()
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        fail(2, f"non-JSON output: {raw[:300]}")
    if "error" in d:  # branch FIRST (pitfall #5)
        code = (d["error"] or {}).get("code", "")
        fail(3 if code == "agent_blocked" else 2,
             f"herdr error: {d['error'].get('message', d['error'])}")

    agent = ((d.get("result") or {}).get("agent") or {})
    receipt = {
        "delivered": True,
        "target": f"{runtime}:{target}" if runtime else target,
        "agent_status": agent.get("agent_status"),
        "revision": agent.get("revision"),
        "state_change_seq": agent.get("state_change_seq"),
        "bytes": len(text),
    }
    if wait_ms is not None:
        receipt["waited_ms"] = int(wait_ms)
    if echo_reply:
        receipt["reply_cmd_hint"] = (
            f'herdr agent prompt {target} "<peer-name> ({target}) → <summary + artifact path>"')
    print(json.dumps(receipt, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
