"""Deadlock regression test (pitfall-30 family, 2026-10-08).

Scenario: A and B call herdr_send against each other as TOOLS while both are
inside their own turns. A naive 30min gate freezes both turns and deadlocks.
Guard: the extension's tool-call gate is capped at 90s and returns a
structured delivered=false receipt with advice.

Requires RUN_SLOW_E2E=1 (real LLM rounds in both peers) and a headless-capable
pi (pi -e <skills repo> loads the extension under test).
"""

import json
import os
import subprocess
import time
import uuid

import pytest

slow = pytest.mark.slow
RUN_SLOW = os.environ.get("RUN_SLOW_E2E") == "1"
TOOL_GATE_BOUND_S = 150  # 90s gate + headless pi overhead


def _headless_tool_call(env, pane_target, marker, steer=False):
    """Run a headless pi (package-loaded extension) that calls herdr_send.
    Returns (elapsed_s, output_tail)."""
    steer_flag = "steer=true" if steer else "不传 steer 参数（默认 followUp）"
    prompt = (
        f"调用 herdr_send 工具：to='{pane_target}'，message 传一段含 '{marker}' 的简短文本，"
        f"{steer_flag}。工具返回后把返回的 JSON 原样输出，不要解释。"
    )
    t0 = time.time()
    r = subprocess.run(
        ["pi", "-e", "/mnt/disk1/hyx/skills", "--mode", "json", "-p", prompt],
        capture_output=True, text=True, timeout=TOOL_GATE_BOUND_S + 120, env=env,
    )
    return time.time() - t0, r.stdout[-600:]


@pytest.mark.skipif(not RUN_SLOW, reason="RUN_SLOW_E2E=1 not set; real LLM rounds")
def test_mutual_tool_send_does_not_deadlock(peer, e2e_runtime):
    """Two peers, both sent to via the extension tool while the sending sessions are
    themselves busy: the tool gate must return within the 90s bound (structured
    delivered=false), never freeze for 30min."""
    a = peer("e2e-dl-a")
    b = peer("e2e-dl-b")

    # make BOTH peers busy with a long-ish turn (each runs an 8s bash inside its turn,
    # repeated) — mirrors the mutual-working deadlock precondition
    for p in (a, b):
        subprocess.run(
            ["herdr", "--session", e2e_runtime, "agent", "prompt", p["pane"],
             "Run this exact bash command and report only its output: `sleep 12 && echo done`"],
            capture_output=True, text=True, timeout=30,
        )
    time.sleep(3)  # let both turns start

    # simulate two tool-calls (the deadlock precondition): headless pi A -> peer B
    # with followUp gate; bound the whole thing well under 30min
    env = dict(os.environ)
    env.update({"HERDR_PANE_ID": "w9:p9", "HERDR_SESSION": e2e_runtime})
    marker = f"E2E-DL-{uuid.uuid4().hex[:8]}"
    elapsed, tail = _headless_tool_call(env, b["pane"], marker)

    # the call must NOT have hung for the legacy 30min: 90s gate + pi overhead
    assert elapsed < TOOL_GATE_BOUND_S, (
        f"tool call took {elapsed:.0f}s — the deadlock guard failed, turn would be frozen"
    )
    # either delivered (peer freed early) or the structured delivered=false receipt
    assert ("delivered" in tail), f"no receipt in output: {tail[:300]}"


@pytest.mark.skipif(not RUN_SLOW, reason="RUN_SLOW_E2E=1 not set; real LLM rounds")
def test_busy_peer_followup_then_steer_recovery(peer, e2e_runtime, scripts_dir):
    """Script-level recovery protocol: busy peer -> followUp exit 4 -> steer delivers.
    This is the exact advice the extension's delivered=false receipt gives."""
    p = peer("e2e-dl-recover")
    subprocess.run(
        ["herdr", "--session", e2e_runtime, "agent", "prompt", p["pane"],
         "Run this exact bash command and report only its output: `sleep 12 && echo done`"],
        capture_output=True, text=True, timeout=30,
    )
    time.sleep(3)

    marker = f"E2E-RECOVER-{uuid.uuid4().hex[:8]}"
    import tempfile
    f = os.path.join(tempfile.mkdtemp(prefix='e2e-dl-'), f"{marker}.md")
    with open(f, "w") as fh:
        fh.write(f"[context] {marker}\n[tasks] 无任务，投递验证。")

    env = dict(os.environ)
    env.update({"HERDR_SESSION": e2e_runtime, "HERDR_FOLLOWUP_MS": "4000"})
    # followUp with a tiny gate -> exit 4, not delivered
    r1 = subprocess.run(
        ["python3", os.path.join(scripts_dir, "herdr-send.py"), p["pane"], f,
         "--from", "e2e-harness (w9:p9)"],
        capture_output=True, text=True, timeout=60, env=env,
    )
    assert r1.returncode == 4, f"expected exit 4 on busy peer, got {r1.returncode}: {r1.stdout[:200]}"

    # wait for the peer to free up, then the SAME followUp succeeds (advice path 3)
    from conftest import wait_for, peer_user_injections, peer_session_file
    ok = wait_for(lambda: any(
        a["agent_status"] in ("idle", "done")
        for a in json.loads(subprocess.run(
            ["herdr", "--session", e2e_runtime, "agent", "list"],
            capture_output=True, text=True).stdout
        )["result"]["agents"] if a["pane_id"] == p["pane"]
    ), timeout_s=120)
    assert ok, "peer never freed up"
    r2 = subprocess.run(
        ["python3", os.path.join(scripts_dir, "herdr-send.py"), p["pane"], f,
         "--from", "e2e-harness (w9:p9)"],
        capture_output=True, text=True, timeout=60, env=env,
    )
    print("R2-DEBUG:", r2.returncode, r2.stdout[:200], r2.stderr[:200])
    assert r2.returncode == 0
    receipt = json.loads(r2.stdout)
    assert receipt["delivered"] is True
    sf = peer_session_file(p["pane"], session=e2e_runtime)
    got = wait_for(lambda: [b for _, b in peer_user_injections(sf) if marker in b], timeout_s=90)
    if not got:
        import glob as g
        twins = [x for x in g.glob('/mnt/disk1/hyx/.pi/agent/sessions/**/2026-*01a11a7e*.jsonl', recursive=True)]
        detail = {x[-50:]: [b[:80] for _, b in peer_user_injections(x)[-3:]] for x in twins}
        raise AssertionError(
            f"marker={marker}\nsf(from agent get)={sf}\n"
            f"all same-prefix files + last injections: {json.dumps(detail, ensure_ascii=False, indent=1)}"
        )
