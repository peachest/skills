"""CLI-level tests for ocr-post-labels.py — ticket #58 (state-file foundation).

Covers: --classified <path> vs stdin transports (identical schema 2
validation), versionless/schema-1 hard-fail with filename + missing-field
list + rebuild hint, Q→Question normalization before label lookup, unknown
classification hard-fail with zero platform calls, priority string enum,
and the cwd/realpath .triage state-dir helper. Runs the real script as a
subprocess against the offline fake-curl stub; ids are synthetic.
"""

import hashlib
import json
import os

import pytest

from conftest import FIXTURES_DIR, read_api_log, run_post, run_verify

STATE_PATH = ".triage/123/classified.json"
DISC_Q = "a1b2c3d4e5f60718"
DISC_TP = "b2c3d4e5f6071819"


def anchor_of(body):
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


def schema2_entries():
    return [
        {"discussion_id": DISC_Q, "anchor": anchor_of("needs team input"),
         "classification": "Q", "reason": "needs team input"},
        {
            "discussion_id": DISC_TP,
            "anchor": anchor_of("real defect"),
            "classification": "TP",
            "reason": "real defect",
            "fix_plan": "add a guard clause",
            "priority": "high",
        },
    ]


def schema2_text():
    return json.dumps({"schema": 2, "entries": schema2_entries()})


@pytest.fixture(autouse=True)
def pull_state(tmp_path, monkeypatch):
    """Post joins every entry against the pull state file (#61): default cwd
    in a tmp checkout plus a pull file for the two fixture discussions. Tests
    that need other ids or a missing file write their own state under tmp_path."""
    monkeypatch.chdir(tmp_path)
    state_dir = tmp_path / ".triage" / "!123"
    state_dir.mkdir(parents=True)
    findings = [
        {"no": 1, "discussion_id": DISC_Q, "file": "src/app.py", "line": 1,
         "author": "ocr-bot", "body": "needs team input"},
        {"no": 2, "discussion_id": DISC_TP, "file": "src/app.py", "line": 2,
         "author": "ocr-bot", "body": "real defect"},
    ]
    (state_dir / "issues.json").write_text(json.dumps(findings), encoding="utf-8")


@pytest.fixture
def state_file(tmp_path):
    """Valid schema 2 state file at .triage/<MR>/classified.json under tmp."""
    path = tmp_path / STATE_PATH
    path.parent.mkdir(parents=True)
    path.write_text(schema2_text(), encoding="utf-8")
    return str(path)


@pytest.fixture
def api_log(tmp_path):
    return tmp_path / "api.jsonl"


def post_body(calls, disc_id):
    """Extract the reply note body posted to a given discussion."""
    posts = [c for c in calls if c["method"] == "POST" and disc_id in c["url"]]
    assert posts, f"no reply POST journaled for {disc_id}: {calls}"
    return json.loads(posts[0]["data"])["body"]


def assert_no_platform_calls(proc, api_log):
    """Validation must gate before platform detection and any API traffic."""
    assert "Detected platform" not in proc.stderr
    assert "Done:" not in proc.stderr
    assert read_api_log(api_log) == []


# ── Transport × valid schema 2 ──


def test_classified_file_schema2_posts_and_normalizes_q(state_file, api_log):
    proc = run_post("!123", "--classified", state_file, api_log=api_log)
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    # Q normalized before label lookup: needs-discussion label reached the body
    assert "⏸️ 需讨论" in post_body(calls, DISC_Q)
    assert "needs team input" in post_body(calls, DISC_Q)
    tp = post_body(calls, DISC_TP)
    assert "🚨 高" in tp and "修复方案" in tp
    # default mode: Question and TP both stay open → reply POSTs only, no resolve PUT
    assert not [c for c in calls if c["method"] == "PUT"]


def test_stdin_transport_schema2_accepted(api_log):
    proc = run_post("!123", stdin_text=schema2_text(), api_log=api_log)
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    assert "⏸️ 需讨论" in post_body(calls, DISC_Q)
    assert "🚨 高" in post_body(calls, DISC_TP)


def test_triage_mode_resolves_tp_but_q_stays_open(state_file, api_log):
    proc = run_post("!123", "--mode", "triage", "--classified", state_file, api_log=api_log)
    assert proc.returncode == 0, proc.stderr
    resolves = [c for c in read_api_log(api_log) if c["method"] == "PUT"]
    # TP resolves in triage mode; normalized Question still stays open
    assert len(resolves) == 1
    assert DISC_TP in resolves[0]["url"]
    assert DISC_Q not in resolves[0]["url"]


def test_verdict_shaped_entry_digests_end_to_end(tmp_path, monkeypatch, api_log):
    """Entry shape verdict.py (#59) will write — extra no/anchor/posted fields — digests cleanly."""
    entry = {
        "discussion_id": DISC_Q,
        "no": 3,
        "anchor": "9f86d081884c7d65",
        "classification": "Q",
        "reason": "cannot determine from diff alone",
        "resolved": False,
        "posted": False,
    }
    path = tmp_path / STATE_PATH
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"schema": 2, "entries": [entry]}), encoding="utf-8")
    # anchor 9f86d081884c7d65 = sha256("test")[:16] — the pull file body must digest to it
    pull = tmp_path / ".triage" / "!123"
    pull.mkdir(parents=True, exist_ok=True)
    (pull / "issues.json").write_text(json.dumps(
        [{"no": 3, "discussion_id": DISC_Q, "file": "src/app.py", "line": 1,
          "author": "ocr-bot", "body": "test"}]), encoding="utf-8")
    proc = run_post("!123", "--mode", "triage", "--classified", str(path), api_log=api_log)
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    assert "⏸️ 需讨论" in post_body(calls, DISC_Q)
    assert not [c for c in calls if c["method"] == "PUT"]


# ── Versionless / schema-1 hard-fail (both transports) ──


def test_versionless_bare_array_rejected_from_file(tmp_path, api_log):
    path = tmp_path / "classified.json"
    path.write_text(json.dumps(schema2_entries()), encoding="utf-8")
    proc = run_post("!123", "--classified", str(path), api_log=api_log)
    assert proc.returncode == 1
    assert "classified.json" in proc.stderr
    assert "schema" in proc.stderr and "entries" in proc.stderr
    assert "Rebuild" in proc.stderr
    assert_no_platform_calls(proc, api_log)


def test_versionless_bare_array_rejected_from_stdin(api_log):
    proc = run_post("!123", stdin_text=json.dumps(schema2_entries()), api_log=api_log)
    assert proc.returncode == 1
    assert "<stdin>" in proc.stderr
    assert "schema" in proc.stderr and "entries" in proc.stderr
    assert_no_platform_calls(proc, api_log)


def test_schema1_rejected_with_version_in_error(tmp_path, api_log):
    path = tmp_path / "state.json"
    path.write_text(json.dumps({"schema": 1, "entries": schema2_entries()}), encoding="utf-8")
    proc = run_post("!123", "--classified", str(path), api_log=api_log)
    assert proc.returncode == 1
    assert "state.json" in proc.stderr
    assert "schema=1" in proc.stderr and "expected 2" in proc.stderr
    assert "Rebuild" in proc.stderr
    assert_no_platform_calls(proc, api_log)


def test_missing_entries_field_rejected(tmp_path, api_log):
    path = tmp_path / "state.json"
    path.write_text(json.dumps({"schema": 2}), encoding="utf-8")
    proc = run_post("!123", "--classified", str(path), api_log=api_log)
    assert proc.returncode == 1
    assert "state.json" in proc.stderr and "entries" in proc.stderr
    assert_no_platform_calls(proc, api_log)


def test_unreadable_classified_path_hard_fails(tmp_path, api_log):
    proc = run_post("!123", "--classified", str(tmp_path / "nope.json"), api_log=api_log)
    assert proc.returncode == 1
    assert "nope.json" in proc.stderr
    assert_no_platform_calls(proc, api_log)


# ── Classification vocabulary ──

@pytest.mark.parametrize("bad_anchor", [None, "", 123])
def test_missing_or_invalid_anchor_hard_fails(bad_anchor, api_log):
    """M6: the anchor is the proof the entry matches the pulled body — a valid
    nonempty anchor is required for every unposted entry. Missing/empty/non-
    string used to bypass validation entirely; without an anchor the reply
    also carries no dedup marker, so retries duplicate it."""
    entry = {"discussion_id": DISC_Q, "classification": "FP", "reason": "r"}
    if bad_anchor is not None:
        entry["anchor"] = bad_anchor
    proc = run_post("!123", stdin_text=json.dumps({"schema": 2, "entries": [entry]}),
                    api_log=api_log)
    assert proc.returncode == 1
    assert "anchor" in proc.stderr
    assert_no_platform_calls(proc, api_log)


@pytest.mark.parametrize("cls", ["Q", "Question"])
def test_q_and_question_both_accepted(cls, api_log):
    entry = {"discussion_id": DISC_Q, "anchor": anchor_of("needs team input"),
             "classification": cls, "reason": "unsure"}
    proc = run_post("!123", stdin_text=json.dumps({"schema": 2, "entries": [entry]}), api_log=api_log)
    assert proc.returncode == 0, proc.stderr  # a legal Q must not KeyError in label/resolved lookup
    calls = read_api_log(api_log)
    assert "⏸️ 需讨论" in post_body(calls, DISC_Q)
    # Question stays open in default mode → no resolve PUT
    assert not [c for c in calls if c["method"] == "PUT"]


@pytest.mark.parametrize("cls", ["tp", "bogus", ""])
def test_unknown_classification_hard_fails_with_zero_platform_calls(cls, api_log):
    entries = [
        {"discussion_id": DISC_TP, "classification": "TP", "reason": "ok", "fix_plan": "x", "priority": "low"},
        {"discussion_id": DISC_Q, "classification": cls, "reason": "??"},
    ]
    proc = run_post("!123", stdin_text=json.dumps({"schema": 2, "entries": entries}), api_log=api_log)
    assert proc.returncode == 1
    assert f"unknown classification {cls!r}" in proc.stderr
    assert "<stdin>" in proc.stderr
    assert_no_platform_calls(proc, api_log)  # the valid first entry must not have been posted


def test_missing_classification_hard_fails(api_log):
    entry = {"discussion_id": DISC_Q, "reason": "no verdict recorded"}
    proc = run_post("!123", stdin_text=json.dumps({"schema": 2, "entries": [entry]}), api_log=api_log)
    assert proc.returncode == 1
    assert "missing classification" in proc.stderr
    assert_no_platform_calls(proc, api_log)


# ── Priority string enum ──


@pytest.mark.parametrize("priority,mark", [("high", "🚨 高"), ("medium", "⚠️ 中"), ("low", "🟢 低")])
def test_priority_string_enum_accepted(priority, mark, api_log):
    entry = {"discussion_id": DISC_TP, "anchor": anchor_of("real defect"),
             "classification": "TP", "reason": "r", "fix_plan": "f", "priority": priority}
    proc = run_post("!123", stdin_text=json.dumps({"schema": 2, "entries": [entry]}), api_log=api_log)
    assert proc.returncode == 0, proc.stderr
    assert mark in post_body(read_api_log(api_log), DISC_TP)


@pytest.mark.parametrize("priority", [1, "critical", "High"])
def test_invalid_priority_hard_fails(priority, api_log):
    entry = {"discussion_id": DISC_TP, "classification": "TP", "reason": "r", "fix_plan": "f", "priority": priority}
    proc = run_post("!123", stdin_text=json.dumps({"schema": 2, "entries": [entry]}), api_log=api_log)
    assert proc.returncode == 1
    assert "priority" in proc.stderr and "<stdin>" in proc.stderr
    assert_no_platform_calls(proc, api_log)


@pytest.mark.parametrize("priority", [None, ["high"], {"p": 1}])
def test_null_or_collection_priority_hard_fails(priority, api_log):
    """ocr r1 F3: explicit null bypassed the `is not None` gate (rendered a
    label-less body); collections raised uncaught TypeError at the `in` check.
    A *supplied* priority must be a valid enum string — omitted stays legal."""
    entry = {"discussion_id": DISC_TP, "classification": "TP", "reason": "r", "fix_plan": "f", "priority": priority}
    proc = run_post("!123", stdin_text=json.dumps({"schema": 2, "entries": [entry]}), api_log=api_log)
    assert proc.returncode == 1
    assert "priority" in proc.stderr and "<stdin>" in proc.stderr
    assert "TypeError" not in proc.stderr and "Traceback" not in proc.stderr
    assert_no_platform_calls(proc, api_log)


def test_missing_priority_on_tp_defaults_medium(api_log):
    entry = {"discussion_id": DISC_TP, "anchor": anchor_of("real defect"),
             "classification": "TP", "reason": "r", "fix_plan": "f"}
    proc = run_post("!123", stdin_text=json.dumps({"schema": 2, "entries": [entry]}), api_log=api_log)
    assert proc.returncode == 0, proc.stderr
    assert "⚠️ 中" in post_body(read_api_log(api_log), DISC_TP)


# ── GitHub side: same hard-fail discipline, zero traffic ──


def test_unknown_classification_zero_calls_on_github(api_log):
    entry = {"discussion_id": "123456788", "classification": "tp", "reason": "?"}
    proc = run_post("1", stdin_text=json.dumps({"schema": 2, "entries": [entry]}), platform="github", api_log=api_log)
    assert proc.returncode == 1
    assert "unknown classification 'tp'" in proc.stderr
    assert_no_platform_calls(proc, api_log)


# ── .triage state-path helper (cwd/realpath, never $HOME) ──


def test_fixture_env_scrubs_inherited_ocr_remote(tmp_path, monkeypatch):
    """M8: the shared fixture env must scrub OCR_REMOTE (and pin
    CI_SERVER_URL) — an inherited OCR_REMOTE=origin pointed at a remote the
    tmp cwd does not have, so fixture runs died with the exit-2 config error
    before ever reaching the offline fixtures."""
    monkeypatch.setenv("OCR_REMOTE", "origin")
    monkeypatch.chdir(tmp_path)
    proc = run_verify("!9")  # default routes: unresolved threads → exit 1
    assert proc.returncode == 1, proc.stderr
    assert "OCR_REMOTE" not in proc.stderr


def test_triage_state_dir_resolves_cwd_realpath_not_home(monkeypatch, tmp_path):
    import ocr_platform

    real = tmp_path / "checkout"
    real.mkdir()
    link = tmp_path / "link-to-checkout"
    link.symlink_to(real)
    monkeypatch.chdir(link)  # cwd goes through a symlink
    monkeypatch.setenv("HOME", str(tmp_path / "somewhere-else"))

    state_dir = ocr_platform.triage_state_dir()
    assert state_dir == os.path.join(str(real), ".triage")
    assert not state_dir.startswith(str(tmp_path / "somewhere-else"))


def test_triage_state_dir_per_mr_subdir(monkeypatch, tmp_path):
    import ocr_platform

    monkeypatch.chdir(tmp_path)
    assert ocr_platform.triage_state_dir("!123") == os.path.join(str(tmp_path), ".triage", "!123")
    assert ocr_platform.triage_state_dir() == os.path.join(str(tmp_path), ".triage")


# ── Fixtures sanity (offline contract) ──


def test_post_fixture_responses_are_canned_and_host_free():
    routes = json.loads((FIXTURES_DIR / "gitlab" / "post_routes.json").read_text())
    body = json.loads((FIXTURES_DIR / "gitlab" / "post_thread.json").read_text())
    assert "/discussions" in routes
    assert isinstance(body.get("notes"), list)  # sweep sees no open notes
    for path in (FIXTURES_DIR / "gitlab").glob("*.json"):
        text = path.read_text().lower()
        assert "git" + "blue" not in text  # no internal hostnames in fixtures
