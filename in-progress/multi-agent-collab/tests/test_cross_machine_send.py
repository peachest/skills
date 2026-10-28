"""Unit test: machine-mode send must NOT inherit $HERDR_SESSION (b9b8fec regression).

Before b9b8fec (2026-10-21) every in-herdr cross-machine send failed the
--machine/--runtime mutual-exclusion check because the script defaulted the
target runtime to $HERDR_SESSION, which is always set inside a herdr pane.
This test pins the fixed behavior with a fake herdr binary (HERDR_BIN) that
records its argv as JSON — no live herdr runtime needed, safe to run in CI.
"""

import json
import os
import subprocess

import pytest

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
SEND = os.path.join(SCRIPTS, "herdr-send.py")

RECEIPT = json.dumps({"result": {"agent": {"agent_status": "idle", "revision": 1,
                                           "state_change_seq": 1}}})

SHIM = """#!/usr/bin/env python3
import sys, json
open(%r, 'w').write(json.dumps(sys.argv[1:]))
print(%r)
"""


@pytest.fixture
def fake_herdr(tmp_path):
    """Fake herdr binary: answers with a valid receipt, logs argv as a JSON list."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    argv_log = tmp_path / "argv.json"
    shim = bin_dir / "herdr"
    shim.write_text(SHIM % (str(argv_log), RECEIPT))
    shim.chmod(0o755)
    return {"bin": str(shim), "log": str(argv_log)}


def _send(machine_args, env_extra, fake_herdr, tmp_path):
    msg = tmp_path / "msg.md"
    msg.write_text("[caller identity] t\n[context] c\n[tasks] t\n[output + reply] r\n")
    env = dict(os.environ)
    for k in ("HERDR_SESSION", "HERDR_SOCKET_PATH"):
        env.pop(k, None)
    env["HERDR_BIN"] = fake_herdr["bin"]
    env.update(env_extra)
    return subprocess.run(
        ["python3", SEND, "w9:p9", str(msg), "--from", "tester (w0:p0)"] + machine_args,
        capture_output=True, text=True, timeout=60, env=env,
    )


def _cli_flags(argv):
    """argv elements outside the prompt TEXT (the element right after 'prompt')."""
    i = argv.index("prompt")
    return argv[:i] + argv[i + 2:]


def test_machine_send_ignores_herdr_session(fake_herdr, tmp_path):
    """--machine wsl with HERDR_SESSION=default must deliver, not exit with the
    mutual-exclusion error (the every-first-try failure mined 2026-10-28)."""
    r = _send(["--machine", "wsl"], {"HERDR_SESSION": "default"}, fake_herdr, tmp_path)
    assert r.returncode == 0, f"exit {r.returncode}: {r.stderr[:300]}"
    out = json.loads(r.stdout)
    assert out["delivered"] is True
    assert "mutually exclusive" not in (r.stderr + r.stdout)
    flags = _cli_flags(json.load(open(fake_herdr["log"])))
    assert "--machine" in flags
    assert "--session" not in flags  # a machine pins its own session


def test_machine_send_with_explicit_runtime_still_fails(fake_herdr, tmp_path):
    """--runtime alongside --machine must fail loudly, not silently drop --runtime
    (regression found 2026-10-28: b9b8fec made the guard dead code)."""
    r = _send(["--machine", "wsl", "--runtime", "dev"],
              {"HERDR_SESSION": "default"}, fake_herdr, tmp_path)
    assert r.returncode != 0
    assert "mutually exclusive" in r.stderr
