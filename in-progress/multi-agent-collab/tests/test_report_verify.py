"""Unit tests for scripts/verify-reports.py — parent-side report verification.

Uses a fake sessions dir via PI_SESSIONS_DIR so no real session data is read.
"""

import json
import os
import subprocess
import time

import pytest

SCRIPT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "scripts", "verify-reports.py",
)


@pytest.fixture()
def fake_sessions(tmp_path, monkeypatch):
    sessions = tmp_path / "sessions" / "proj-a"
    arts = sessions / "subagent-artifacts"
    arts.mkdir(parents=True)
    monkeypatch.setenv("PI_SESSIONS_DIR", str(sessions))
    return arts


def _run(manifest, fake_sessions):
    return subprocess.run(
        ["python3", SCRIPT, "-"],
        input=json.dumps(manifest),
        capture_output=True, text=True,
    )


def test_all_present_exits_zero(tmp_path, fake_sessions):
    good = tmp_path / "report-a.md"
    good.write_text("# real content", encoding="utf-8")
    r = _run({"a": str(good)}, fake_sessions)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "OK" in r.stdout


def test_empty_file_counts_as_missing(tmp_path, fake_sessions):
    empty = tmp_path / "empty.md"
    empty.write_text("", encoding="utf-8")
    r = _run({"e": str(empty)}, fake_sessions)
    assert r.returncode == 1
    assert "MISSING" in r.stdout


def test_missing_lists_artifact_candidates_for_recovery(tmp_path, fake_sessions):
    # a drifted artifact: written by the runtime, not at the declared path
    drift = fake_sessions / "runid1_worker_output.md"
    drift.write_text("# the actual report body", encoding="utf-8")
    # an empty artifact and an input file must not appear as candidates
    (fake_sessions / "runid2_worker_output.md").write_text("", encoding="utf-8")
    (fake_sessions / "runid3_worker_input.md").write_text("noise", encoding="utf-8")
    declared = tmp_path / "report-b.md"  # never written
    r = _run({"b": str(declared)}, fake_sessions)
    assert r.returncode == 1
    assert "recovery candidates" in r.stdout
    assert "runid1_worker_output.md" in r.stdout
    assert "runid2" not in r.stdout and "runid3" not in r.stdout


def test_stale_artifacts_outside_window_excluded(tmp_path, fake_sessions, monkeypatch):
    drift = fake_sessions / "old_worker_output.md"
    drift.write_text("old body", encoding="utf-8")
    old = time.time() - 72 * 3600
    os.utime(drift, (old, old))
    r = _run({"x": str(tmp_path / "nope.md")}, fake_sessions)
    assert r.returncode == 1
    assert "old_worker_output.md" not in r.stdout


def test_list_manifest_form(tmp_path, fake_sessions):
    good = tmp_path / "r.md"
    good.write_text("x", encoding="utf-8")
    r = _run([str(good)], fake_sessions)
    assert r.returncode == 0
