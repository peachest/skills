"""E2E tests: the multi-agent-collab herdr peer loop, exercised for real.

Note: a freshly spawned peer pi creates its session JSONL lazily (first user
message), and spends its first seconds indexing sessions — delivery assertions
therefore use a 90s window.

Every test runs against an isolated herdr runtime (collab-e2e, see conftest).
Ground truth for delivery = the user-role injection in the PEER's session
JSONL (pitfall #11/#30: CLI receipts are not enough — verify the landing).

Fast tests (no LLM rounds) run always. Tests that make a peer actually
think are marked slow and need RUN_SLOW_E2E=1.
"""

import json
import os
import subprocess
import uuid

import pytest

from conftest import peer_session_file, peer_user_injections, wait_for

RUN_SLOW = os.environ.get("RUN_SLOW_E2E") == "1"

slow = pytest.mark.slow


def _send(scripts_dir, pane, message, extra=None, env=None):
    """Run herdr-send.py against a message file. Returns (exit, stdout_json_or_text)."""
    import tempfile
    d = tempfile.mkdtemp(prefix="e2e-msg-")
    f = os.path.join(d, "msg.md")
    with open(f, "w") as fh:
        fh.write(message)
    cmd = ["python3", os.path.join(scripts_dir, "herdr-send.py"), pane, f] + (extra or [])
    e = dict(os.environ)
    if env:
        e.update(env)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=e)
    out = r.stdout.strip() or r.stderr.strip()
    try:
        return r.returncode, json.loads(out)
    except json.JSONDecodeError:
        return r.returncode, out


def test_resolve_scans_all_runtimes(peer, scripts_dir, e2e_runtime):
    """herdr-resolve.py finds a peer by UUID prefix across runtimes, tagging the runtime."""
    p = peer("e2e-resolve")
    r = subprocess.run(
        ["python3", os.path.join(scripts_dir, "herdr-resolve.py"), p["pane"]],
        capture_output=True, text=True, timeout=60,
    )
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        raise AssertionError(
            f"resolve returned non-JSON (exit {r.returncode}): "
            f"stdout={r.stdout[:200]!r} stderr={r.stderr[:400]!r}"
        )
    assert d["count"] >= 1
    mine = [m for m in d["matches"] if m["runtime"] == e2e_runtime]
    assert mine, "peer in collab-e2e runtime not found in the all-runtime scan"
    assert mine[0]["agent_status"] in ("idle", "working", "done")


def test_send_followup_delivers_with_identity(peer, scripts_dir, e2e_runtime):
    """followUp send to an idle peer: exit 0, level-1 receipt, and the message
    lands in the peer's session JSONL with a runtime-qualified caller identity."""
    p = peer("e2e-send")
    marker = f"E2E-DELIVERY-{uuid.uuid4().hex[:8]}"
    code, receipt = _send(
        scripts_dir, p["pane"],
        f"[context] {marker}\n[tasks] 无任务——这是投递验证。收到即可，无需回复。",
        extra=["--from", "e2e-harness (w9:p9)"],
        env={"HERDR_SESSION": e2e_runtime},
    )
    if code != 0:
        agents = subprocess.run(["herdr", "--session", e2e_runtime, "agent", "list"],
                                capture_output=True, text=True, timeout=30)
        probe = subprocess.run(["herdr", "--session", e2e_runtime, "agent", "get", p["pane"]],
                               capture_output=True, text=True, timeout=30)
        raise AssertionError(f"send failed (exit {code}): {receipt}\n"
                             f"runtime={e2e_runtime} pane_of_peer={p['pane']} agent list panes: {[a.get('pane_id') for a in json.loads(agents.stdout)['result']['agents']] if agents.stdout.strip().startswith('{') else agents.stdout[:300]}\n agent get: {probe.stdout[:250]} {probe.stderr[:150]}")
    assert receipt["delivered"] is True
    assert "agent_status" in receipt and "revision" in receipt  # level-1 evidence

    # ground truth: the injection carries the runtime-qualified identity
    sf = peer_session_file(p["pane"])
    hits = wait_for(
        lambda: [b for t, b in peer_user_injections(sf, contains=marker)],
        timeout_s=90,
    )
    assert hits, f"{marker} never injected into the peer session"
    body = hits[0]
    assert "[caller identity]" in body
    assert re.search(r"herdr:[\w-]+:w9:p9", body), f"identity not runtime-qualified: {body[:200]}"


def test_send_not_found_is_exit2(peer, scripts_dir, e2e_runtime):
    """A stale/unreachable pane yields exit 2 with an agent_not_found envelope —
    never a silent pass (pitfall #29/#30 guardrail)."""
    code, receipt = _send(scripts_dir, "w99:p99", "probe", env={"HERDR_SESSION": e2e_runtime})
    assert code == 2
    assert "agent_not_found" in json.dumps(receipt) or "not found" in json.dumps(receipt)


def test_resolve_empty_query_rejected(scripts_dir):
    r = subprocess.run(
        ["python3", os.path.join(scripts_dir, "herdr-resolve.py"), ""],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 3  # usage


import re  # noqa: E402  (used by identity assertion above)


@pytest.mark.skipif(not RUN_SLOW, reason="RUN_SLOW_E2E=1 not set; triggers a real LLM round in the peer")
def test_send_followup_gates_on_busy_peer(peer, scripts_dir, e2e_runtime):
    """pitfall #30 guardrail: while the peer is genuinely working, followUp with a
    short timeout must exit 4 and NOT deliver; steer delivers mid-task."""
    p = peer("e2e-busy")
    # make the peer busy with a real (short) LLM turn
    subprocess.run(
        ["herdr", "--session", e2e_runtime, "agent", "prompt", p["pane"],
         "Count slowly from 1 to 5, one number per line, nothing else."],
        capture_output=True, text=True, timeout=30,
    )
    busy = wait_for(
        lambda: any(
            a["pane_id"] == p["pane"] and a["agent_status"] == "working"
            for a in json.loads(
                subprocess.run(["herdr", "--session", e2e_runtime, "agent", "list"],
                               capture_output=True, text=True).stdout
            )["result"]["agents"]
        ),
        timeout_s=30,
    )
    assert busy, "peer never entered working state; cannot test the gate"

    marker = f"E2E-BUSY-{uuid.uuid4().hex[:8]}"
    code, receipt = _send(
        scripts_dir, p["pane"], f"[context] {marker}\n[tasks] ignore",
        extra=["--from", "e2e-harness (w9:p9)"],
        env={"HERDR_SESSION": e2e_runtime, "HERDR_FOLLOWUP_MS": "3000"},
    )
    assert code == 4, f"expected followup-timeout exit 4, got {code}: {receipt}"
    assert not peer_user_injections(peer_session_file(p["pane"]), contains=marker), \
        "gate timed out but the message was delivered anyway — followUp gate is broken"

    # steer bypasses the gate and delivers mid-task (documented steer semantics)
    code2, receipt2 = _send(
        scripts_dir, p["pane"], f"[context] steer-probe-{marker}",
        extra=["--steer", "--from", "e2e-harness (w9:p9)"],
        env={"HERDR_SESSION": e2e_runtime},
    )
    assert code2 == 0 and receipt2.get("delivered") is True


@pytest.mark.skipif(not RUN_SLOW, reason="RUN_SLOW_E2E=1 not set; triggers a real LLM round in the peer")
def test_extension_tool_herdr_send_end_to_end(peer, e2e_runtime):
    """Full loop through the pi extension: a headless pi (package-loaded) uses the
    herdr_send TOOL to deliver; the peer's session shows the auto-injected
    runtime-qualified identity. This is the layer that failed as 'non-JSON'."""
    p = peer("e2e-ext")
    marker = f"E2E-EXT-{uuid.uuid4().hex[:8]}"
    repo = "/mnt/disk1/hyx/skills"
    env = dict(os.environ)
    env.update({
        "HERDR_PANE_ID": "w9:p9",          # fake sender pane (structured identity source)
        "HERDR_SESSION": e2e_runtime,      # sender runtime
        "RUN_SLOW_E2E": "1",
    })
    prompt = (
        f"Use the herdr_send tool: to={p['pane']}, message='[context] {marker}\\n"
        f"[tasks] 无任务，投递验证，无需回复。'（不要 steer，其余参数默认）。"
        f"工具返回后，把 receipt JSON 原样输出。"
    )
    r = subprocess.run(
        ["pi", "-e", repo, "--mode", "json", "-p", prompt],
        capture_output=True, text=True, timeout=300, env=env,
    )
    # the tool receipt is echoed by the model; the real assertion is the landing
    sf = peer_session_file(p["pane"])
    hits = wait_for(
        lambda: [b for t, b in peer_user_injections(sf, contains=marker)],
        timeout_s=90,
    )
    assert hits, f"tool-dispatched message never landed; pi output tail: {r.stdout[-400:]}"
    body = hits[0]
    assert re.search(r"herdr:collab-e2e[\w-]*:w9:p9", body), \
        f"identity not auto-injected with sender runtime: {body[:200]}"
