"""E2E fixtures for the multi-agent-collab herdr peer loop.

Isolation model: every run bootstraps a DEDICATED herdr runtime session
(`collab-e2e`) via the pty-attach trick (the TUI dies on a zero-size grid but
the server persists — verified 2026-09-23), so tests never touch the
default/dev/agent runtimes or their real peers. Teardown stops the session,
which kills every pane/agent created during the run.

Peer pi sessions boot idle and cost nothing until a prompt reaches them; the
LLM-round tests are marked slow and gated behind RUN_SLOW_E2E=1.
"""

import json
import os
import pty
import re
import subprocess
import time
import uuid

import pytest

RUNTIME = f"collab-e2e-{uuid.uuid4().hex[:8]}"  # one-shot runtime per test run
PEER_BOOT_TIMEOUT = 60_000  # ms, for pi to boot in the pane


def _clean_env():
    """Strip HERDR_* so the harness talks to runtimes explicitly via --session."""
    env = dict(os.environ)
    for k in list(env):
        if k.startswith("HERDR_"):
            del env[k]
    return env


def herdr(args, session=RUNTIME, timeout=60):
    """Run a one-shot herdr CLI command against the test runtime. Returns CompletedProcess."""
    cmd = ["herdr"]
    if session:
        cmd += ["--session", session]
    cmd += args
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=_clean_env())


def herdr_json(args, session=RUNTIME, timeout=60):
    r = herdr(args, session=session, timeout=timeout)
    try:
        return json.loads(r.stdout.strip() or r.stderr.strip())
    except json.JSONDecodeError:
        raise AssertionError(f"herdr {args} returned non-JSON (exit {r.returncode}): {(r.stdout or r.stderr)[:300]}")


def server_running(session=RUNTIME):
    out = subprocess.run(["herdr", "session", "list"], capture_output=True, text=True, env=_clean_env()).stdout
    return bool(re.search(rf"^{re.escape(session)}\s+running", out, re.M))


def bootstrap_runtime(session=RUNTIME):
    """Start the session server headlessly: pty attach (TUI dies on zero-grid, server persists)."""
    if server_running(session):
        return False
    scratch = "/tmp"
    cmd = f'env -u HERDR_ENV -u HERDR_PANE_ID -u HERDR_SESSION -u HERDR_SOCKET_PATH -u HERDR_WORKSPACE_ID -u HERDR_TAB_ID herdr session attach {session}'
    # cwd matters: the initial pane inherits it — use a neutral dir
    pty.spawn(["bash", "-c", f"cd {scratch} && {cmd}"])
    deadline = time.time() + 20
    while time.time() < deadline:
        if server_running(session):
            return True
        time.sleep(0.5)
    raise AssertionError(f"runtime {session} did not come up after pty attach")


def initial_pane(session=RUNTIME):
    d = herdr_json(["pane", "list"], session=session)
    panes = (d.get("result") or {}).get("panes") or []
    assert panes, "runtime has no initial pane"
    return panes[0]["pane_id"]


def fresh_pane(cwd, session=RUNTIME):
    """Split a fresh shell pane off the initial one (herdr sessions persist their
    pane/agent layout across server restarts — a reused pane is never an
    'available shell' again, verified 2026-09-23)."""
    # NOTE: the positional PANE_ID documented in --help is rejected at runtime
    # ("unknown option") — split always branches off the focused pane.
    d = herdr_json(["pane", "split", "--direction", "right", "--cwd", cwd], session=session)
    return ((d.get("result") or {}).get("pane") or {})["pane_id"]


def spawn_peer(name, cwd):
    """Start a real pi agent in a FRESH split pane. Returns (pane_id, session_file_placeholder).

    herdr agent start on an occupied/persisted pane errors agent_pane_busy
    (verified 2026-09-23) — every peer gets its own split pane.
    """
    pane = fresh_pane(cwd)
    d = herdr_json(["agent", "start", name, "--kind", "pi", "--pane", pane], timeout=90)
    agent = (d.get("result") or {}).get("agent") or {}
    assert agent.get("interactive_ready") or agent.get("agent_status"), \
        f"agent start did not reach interactive: {json.dumps(d)[:300]}"
    # wait for pi to boot to idle, then wait until the agent is promptable:
    # `agent wait --until idle` can return before herdr finishes prompt routing —
    # a prompt sent in that window errors agent_not_found (intermittent, verified 2026-09-23)
    herdr_json(["agent", "wait", pane, "--until", "idle", "--timeout", str(PEER_BOOT_TIMEOUT)], timeout=90)
    deadline = time.time() + 20
    last = None
    while time.time() < deadline:
        d = herdr_json(["agent", "get", pane], timeout=15)
        last = d
        if "error" not in d:
            break
        time.sleep(0.5)
    else:
        raise AssertionError(f"agent on {pane} never became promptable: {json.dumps(last)[:300]}")
    # pitfall #17 sibling: herdr marks idle while pi boots, and pi enters its
    # "Indexing N sessions..." phase ASYNCHRONOUSLY after boot — text typed before
    # or during indexing is swallowed with no error. Require TWO consecutive clean
    # pane reads >=3s apart (indexing must have started AND finished).
    def pane_clean():
        r = herdr(["agent", "read", pane], timeout=30)
        return "Indexing" not in (r.stdout or "")
    if not pane_clean():  # indexing already running -> just wait it out
        wait_for(pane_clean, timeout_s=90, interval=2)
    time.sleep(3)
    if not pane_clean():
        wait_for(pane_clean, timeout_s=90, interval=2)
    return pane


def peer_session_file(pane, session=RUNTIME, timeout_s=30):
    """Poll agent get until herdr resolves the peer's session JSONL path (it appears
    lazily — pi creates the file on its first message, herdr picks the path up
    shortly after)."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        d = herdr_json(["agent", "get", pane], session=session, timeout=15)
        val = ((d.get("result") or {}).get("agent") or {}).get("agent_session", {}).get("value", "")
        if val:
            return val
        time.sleep(1)
    raise AssertionError(f"peer {pane} never got a session path")


UUID_RE = re.compile(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})')
SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")


def peer_user_injections(session_file, contains=None, since_ts=None):
    """Read user-role injections from a peer session JSONL (ground truth for delivery).
    Missing file is fine — pi creates its session JSONL lazily on the first message."""
    hits = []
    if not os.path.exists(session_file):
        return hits
    for line in open(session_file, encoding="utf-8", errors="ignore"):
        if contains and contains not in line:
            continue
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("type") != "message":
            continue
        m = e.get("message") or {}
        if m.get("role") != "user":
            continue
        c = m.get("content")
        body = c if isinstance(c, str) else " ".join(x.get("text", "") for x in (c or []) if isinstance(x, dict))
        if body.strip():
            hits.append((e["timestamp"], body))
    return hits


def wait_for(condition, timeout_s, interval=1.0):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        v = condition()
        if v:
            return v
        time.sleep(interval)
    return None


@pytest.fixture(scope="session")
def e2e_runtime():
    """One-shot isolated runtime per test run (unique name → no persisted pane
    layout from previous runs). Teardown stops AND deletes it — zero residue."""
    bootstrap_runtime(RUNTIME)
    yield RUNTIME
    subprocess.run(["herdr", "session", "stop", RUNTIME], capture_output=True, env=_clean_env(), timeout=30)
    subprocess.run(["herdr", "session", "delete", RUNTIME], capture_output=True, env=_clean_env(), timeout=30)


@pytest.fixture()
def peer(e2e_runtime, tmp_path):
    """Factory: spawn a named peer pi in the test runtime; auto-registered for teardown info."""
    created = []

    def _spawn(name="e2e-peer"):
        pane = spawn_peer(name, str(tmp_path))
        created.append(pane)
        return {"pane": pane, "name": name}

    yield _spawn
    # teardown: no agent-stop verb exists; the session stop in e2e_runtime teardown
    # kills everything. Nothing per-peer to do here (kept for future fine-grained cleanup).


@pytest.fixture(scope="session")
def scripts_dir():
    return SCRIPTS
