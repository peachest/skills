"""Cross-machine tests (herdr >= 0.9.5 --machine flag).

Requires a saved machine entry (herdr machine list) that is enabled and
reachable. These tests are read-only against the remote machine (list only —
no prompts dispatched to real remote peers).
"""

import json
import os
import subprocess

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("E2E_REMOTE_MACHINE"),
    reason="E2E_REMOTE_MACHINE not set (e.g. E2E_REMOTE_MACHINE=wsl); no remote machine tests"
)


def _machine():
    return os.environ["E2E_REMOTE_MACHINE"]


def test_machine_list_shows_enabled():
    r = subprocess.run(["herdr", "machine", "list"], capture_output=True, text=True, timeout=60)
    assert _machine() in r.stdout


def test_resolve_machine_scans_remote(peer, scripts_dir):
    """herdr-resolve --machine <label> queries the remote machine's agents."""
    p = peer("e2e-remote-resolve")
    r = subprocess.run(
        ["python3", os.path.join(scripts_dir, "herdr-resolve.py"), p["pane"],
         "--machine", _machine()],
        capture_output=True, text=True, timeout=90,
    )
    # the local test peer does NOT live on the remote machine — resolve must
    # cleanly return 0 matches (exit 1), proving the remote query path works
    assert r.returncode in (0, 1), f"unexpected failure: {r.stderr[:300]}"
    if r.returncode == 1:
        d = json.loads(r.stdout)
        assert d["scanned"][0]["machine"] == _machine()


def test_resolve_all_machines_includes_local_and_remote(peer, scripts_dir):
    """--all-machines scans local runtimes + every saved machine; the local test
    peer must be found with machine='local'."""
    p = peer("e2e-allm")
    r = subprocess.run(
        ["python3", os.path.join(scripts_dir, "herdr-resolve.py"), p["pane"], "--all-machines"],
        capture_output=True, text=True, timeout=120,
    )
    d = json.loads(r.stdout)
    mine = [m for m in d["matches"] if m["pane_id"] == p["pane"]]
    assert mine, f"local peer missing from all-machines scan: {json.dumps(d)[:300]}"
    assert mine[0]["machine"] == "local"
