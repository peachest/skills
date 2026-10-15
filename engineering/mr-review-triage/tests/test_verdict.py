"""CLI-level tests for verdict.py — ticket #59 (classified.json sole writer).

Covers: byte-exact discussion_id copy from the pull state file, body anchor
(sha256(body)[:16]), per-item resolved semantics (spec #57 Amendment R2
修订 A: the close-after-verification decision is made at verdict time and
stored per item — Edge defaults resolved=true, Q defaults open, TP/FP/OOS
leave the field unset so post applies its mode map), incremental append
preserving prior entries, --force overwrite without stale fields, the full
exit-code contract (0 ok / 1 state / 2 usage), display discipline (the
discussion_id never reaches human-readable output), and the Q end-to-end
acceptance through ocr-post-labels.py recorded in #58. verdict.py is a pure
local state script — the standalone cases need no platform API; the e2e
cases reuse the offline fake-curl harness. Ids are synthetic.
"""

import hashlib
import json

import pytest
from conftest import read_api_log, run_post, run_pull, run_verdict

MR = "!9"
DISC_A = "E5f6071819a1b2c3d4e5"  # mixed-case 20 chars — byte-exactness is observable
DISC_B = "c3d4e5f607181920bbbb"
BODY_A = "Use a named constant for the retry limit instead of a literal"
BODY_B_FIRST = "Consider splitting this module before the next feature lands"
BODY_B = BODY_B_FIRST + "\nwith a follow-up refactor"
AUTHOR_A = "ocr-bot"
AUTHOR_B = "human-reviewer"
PULL_BODY_A = "Replace the retry loop with tenacity"


def findings_two():
    return [
        {"discussion_id": DISC_A, "file": "src/app.py", "line": 42,
         "body": BODY_A, "author": AUTHOR_A, "no": 1},
        {"discussion_id": DISC_B, "file": "src/big.py", "line": 7,
         "body": BODY_B, "author": AUTHOR_B, "no": 2},
    ]


def write_pull(tmp_path, findings, mr=MR):
    state_dir = tmp_path / ".triage" / mr
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "issues.json").write_text(
        json.dumps(findings, ensure_ascii=False), encoding="utf-8")
    return state_dir


def read_classified(state_dir):
    return json.loads((state_dir / "classified.json").read_text(encoding="utf-8"))


def reply_body(calls, disc_id):
    posts = [c for c in calls if c["method"] == "POST" and disc_id in c["url"]]
    assert posts, f"no reply POST journaled for {disc_id}: {calls}"
    return json.loads(posts[0]["data"])["body"]


@pytest.fixture
def state_dir(tmp_path, monkeypatch):
    """Pull state file for two findings, cwd inside the tmp checkout."""
    monkeypatch.chdir(tmp_path)
    return write_pull(tmp_path, findings_two())


# ── Entry shape: byte-exact id, anchor, schema, posted ──


def test_entry_carries_byte_exact_id_anchor_schema_posted(state_dir):
    proc = run_verdict(MR, "1", "--class", "Edge", "--reason", "policy call")
    assert proc.returncode == 0, proc.stderr
    data = read_classified(state_dir)
    assert data["schema"] == 2
    assert len(data["entries"]) == 1
    entry = data["entries"][0]
    assert entry["discussion_id"] == DISC_A  # byte-exact script copy, never retyped
    assert entry["anchor"] == hashlib.sha256(BODY_A.encode("utf-8")).hexdigest()[:16]
    assert entry["no"] == 1
    assert entry["classification"] == "Edge"
    assert entry["reason"] == "policy call"
    assert entry["posted"] is False


def test_anchor_tracks_pull_file_body_not_flag_text(state_dir):
    proc = run_verdict(MR, "2", "--class", "FP", "--reason", "not a defect")
    assert proc.returncode == 0, proc.stderr
    entry = read_classified(state_dir)["entries"][0]
    assert entry["anchor"] == hashlib.sha256(BODY_B.encode("utf-8")).hexdigest()[:16]


# ── Success echo: no + author + first line, zero id shapes ──


def test_success_echo_has_no_author_first_line_and_no_id(state_dir):
    proc = run_verdict(MR, "2", "--class", "FP", "--reason", "not a defect")
    assert proc.returncode == 0, proc.stderr
    assert "no=2" in proc.stdout
    assert AUTHOR_B in proc.stdout
    assert BODY_B_FIRST in proc.stdout  # first line only
    assert "follow-up refactor" not in proc.stdout
    assert DISC_B not in proc.stdout
    assert DISC_B[:8] not in proc.stdout  # no truncated-id shapes either


# ── Per-item resolved semantics (Amendment R2 修订 A) ──


def test_edge_defaults_resolved_true_and_flag_overrides(state_dir):
    proc = run_verdict(MR, "1", "--class", "Edge", "--reason", "checked, closable")
    assert proc.returncode == 0, proc.stderr
    assert read_classified(state_dir)["entries"][0]["resolved"] is True

    proc = run_verdict(MR, "1", "--class", "Edge", "--reason", "keep open", "--force",
                       "--resolved", "false")
    assert proc.returncode == 0, proc.stderr
    assert read_classified(state_dir)["entries"][0]["resolved"] is False


def test_q_defaults_open_and_explicit_true_closes(state_dir):
    proc = run_verdict(MR, "1", "--class", "Q", "--reason", "needs team input")
    assert proc.returncode == 0, proc.stderr
    entry = read_classified(state_dir)["entries"][0]
    assert entry["classification"] == "Q"  # stored as Q; post normalizes
    assert entry["resolved"] is False

    proc = run_verdict(MR, "1", "--class", "Q", "--reason", "verified closable",
                       "--force", "--resolved", "true")
    assert proc.returncode == 0, proc.stderr
    assert read_classified(state_dir)["entries"][0]["resolved"] is True


@pytest.mark.parametrize("cls,extra", [
    ("TP", ["--fix-plan", "add a guard clause"]),
    ("FP", []),
    ("OOS", []),
])
def test_tp_fp_oos_omit_resolved_unless_explicit(state_dir, cls, extra):
    proc = run_verdict(MR, "1", "--class", cls, "--reason", "r", *extra)
    assert proc.returncode == 0, proc.stderr
    entry = read_classified(state_dir)["entries"][0]
    assert "resolved" not in entry  # post's mode map decides (standalone vs triage)

    proc = run_verdict(MR, "1", "--class", cls, "--reason", "r", *extra,
                       "--force", "--resolved", "false")
    assert proc.returncode == 0, proc.stderr
    assert read_classified(state_dir)["entries"][0]["resolved"] is False


def test_tp_stores_fix_plan_and_priority(state_dir):
    proc = run_verdict(MR, "1", "--class", "TP", "--reason", "real defect",
                       "--fix-plan", "add a guard clause", "--priority", "high")
    assert proc.returncode == 0, proc.stderr
    entry = read_classified(state_dir)["entries"][0]
    assert entry["fix_plan"] == "add a guard clause"
    assert entry["priority"] == "high"


def test_tp_without_fix_plan_is_usage_error_and_writes_nothing(state_dir):
    proc = run_verdict(MR, "1", "--class", "TP", "--reason", "real defect")
    assert proc.returncode == 2
    assert "--fix-plan" in proc.stderr
    assert not (state_dir / "classified.json").exists()


# ── State errors (exit 1) ──


def test_missing_pull_file_exit1_with_hint(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    proc = run_verdict(MR, "1", "--class", "FP", "--reason", "r")
    assert proc.returncode == 1
    assert "issues.json" in proc.stderr
    assert "ocr-pull-discussions.py" in proc.stderr


def test_unknown_no_exit1(state_dir):
    proc = run_verdict(MR, "7", "--class", "FP", "--reason", "r")
    assert proc.returncode == 1
    assert "no finding with no=7" in proc.stderr
    assert "1..2" in proc.stderr
    assert not (state_dir / "classified.json").exists()


@pytest.mark.parametrize("raw", ["{not json", "{}", "[]"])
def test_unusable_pull_file_exit1(state_dir, raw):
    (state_dir / "issues.json").write_text(raw, encoding="utf-8")
    proc = run_verdict(MR, "1", "--class", "FP", "--reason", "r")
    assert proc.returncode == 1
    assert "issues.json" in proc.stderr


def test_duplicate_verdict_refused_without_force(state_dir):
    first = run_verdict(MR, "1", "--class", "Edge", "--reason", "policy call")
    assert first.returncode == 0, first.stderr
    again = run_verdict(MR, "1", "--class", "FP", "--reason", "changed my mind")
    assert again.returncode == 1
    assert "--force" in again.stderr
    entry = read_classified(state_dir)["entries"][0]
    assert entry["classification"] == "Edge"  # refusal leaves the original intact
    assert len(read_classified(state_dir)["entries"]) == 1


@pytest.mark.parametrize("content,fragment", [
    ("{corrupt", "not readable JSON"),
    (json.dumps([{"discussion_id": DISC_A}]), "schema"),   # bare array
    (json.dumps({"schema": 1, "entries": []}), "schema"),  # schema 1
])
def test_existing_classified_must_be_schema2(state_dir, content, fragment):
    (state_dir / "classified.json").write_text(content, encoding="utf-8")
    proc = run_verdict(MR, "1", "--class", "FP", "--reason", "r")
    assert proc.returncode == 1
    assert "classified.json" in proc.stderr
    assert fragment in proc.stderr


# ── --force overwrite & incremental append ──


def test_force_overwrites_in_place_without_stale_fields(state_dir):
    run_verdict(MR, "1", "--class", "TP", "--reason", "real defect",
                "--fix-plan", "add a guard clause", "--priority", "high")
    proc = run_verdict(MR, "1", "--class", "FP", "--reason", "false positive", "--force")
    assert proc.returncode == 0, proc.stderr
    data = read_classified(state_dir)
    assert len(data["entries"]) == 1  # replaced, not duplicated
    entry = data["entries"][0]
    assert entry["classification"] == "FP"
    assert entry["reason"] == "false positive"
    assert "fix_plan" not in entry and "priority" not in entry  # old values gone


def test_incremental_append_preserves_previous_entries(state_dir):
    first = run_verdict(MR, "2", "--class", "FP", "--reason", "not a defect")
    assert first.returncode == 0, first.stderr
    after_first = read_classified(state_dir)
    second = run_verdict(MR, "1", "--class", "Edge", "--reason", "policy call")
    assert second.returncode == 0, second.stderr
    after_second = read_classified(state_dir)
    assert len(after_second["entries"]) == 2
    assert after_second["entries"][0] == after_first["entries"][0]  # prior entry untouched
    assert after_second["schema"] == after_first["schema"] == 2
    assert not list(state_dir.glob("*.tmp"))  # atomic rename leaves no debris


def test_same_thread_new_subissue_appends(state_dir):
    # Fallback notes yield several findings sharing one discussion_id —
    # different bodies (different anchors) are distinct findings and append.
    write_pull(state_dir.parent.parent, [
        {"discussion_id": DISC_A, "file": "a.go", "line": 1, "body": "first sub-issue", "author": AUTHOR_A, "no": 1},
        {"discussion_id": DISC_A, "file": "b.go", "line": 2, "body": "second sub-issue", "author": AUTHOR_A, "no": 2},
    ])
    assert run_verdict(MR, "1", "--class", "TP", "--reason", "r",
                       "--fix-plan", "f").returncode == 0
    second = run_verdict(MR, "2", "--class", "FP", "--reason", "r")
    assert second.returncode == 0, second.stderr
    entries = read_classified(state_dir)["entries"]
    assert len(entries) == 2
    assert [e["no"] for e in entries] == [1, 2]


def test_ordinal_reshuffle_never_crossmatches_findings(state_dir):
    """ocr r1 F1: dedup matches (discussion_id, anchor) only — `no` is display
    metadata, never a match key. A different finding taking no=1 after a
    re-pull must append; the original finding under its new ordinal is a
    duplicate by thread+anchor (refused, --force replaces the right entry)."""
    run_verdict(MR, "1", "--class", "TP", "--reason", "real defect",
                "--fix-plan", "guard the retry", "--priority", "high")
    assert [e["no"] for e in read_classified(state_dir)["entries"]] == [1]

    # Round 2 pull: a different finding now carries no=1; the round-1 finding
    # (DISC_A, same body → same anchor) moved to no=3.
    write_pull(state_dir.parent.parent, [
        {"discussion_id": DISC_B, "file": "src/big.py", "line": 7,
         "body": BODY_B, "author": AUTHOR_B, "no": 1},
        {"discussion_id": DISC_A, "file": "src/app.py", "line": 42,
         "body": BODY_A, "author": AUTHOR_A, "no": 3},
    ])

    # New thread at no=1 — must append, not collide with the round-1 verdict.
    rec = run_verdict(MR, "1", "--class", "FP", "--reason", "not a defect")
    assert rec.returncode == 0, rec.stderr
    entries = read_classified(state_dir)["entries"]
    assert len(entries) == 2
    assert entries[1]["discussion_id"] == DISC_B
    assert entries[1]["no"] == 1

    # Original finding at its new ordinal: same thread+anchor → duplicate.
    refused = run_verdict(MR, "3", "--class", "FP", "--reason", "re-verdict")
    assert refused.returncode == 1
    assert "--force" in refused.stderr
    assert len(read_classified(state_dir)["entries"]) == 2

    # --force replaces exactly that finding's entry — not the no=1 twin.
    forced = run_verdict(MR, "3", "--class", "FP", "--reason", "changed verdict", "--force")
    assert forced.returncode == 0, forced.stderr
    by_disc = {e["discussion_id"]: e for e in read_classified(state_dir)["entries"]}
    assert by_disc[DISC_A]["no"] == 3
    assert by_disc[DISC_A]["reason"] == "changed verdict"
    assert by_disc[DISC_B]["reason"] == "not a defect"  # untouched


def test_reshuffled_same_finding_refused_then_force_replaces(state_dir):
    run_verdict(MR, "1", "--class", "Edge", "--reason", "policy call")
    # Same thread + same body re-pulled under a new ordinal — same finding.
    findings = findings_two()
    findings[1]["discussion_id"] = DISC_A
    findings[1]["body"] = BODY_A
    write_pull(state_dir.parent.parent, findings)
    refused = run_verdict(MR, "2", "--class", "FP", "--reason", "r")
    assert refused.returncode == 1
    assert "--force" in refused.stderr
    assert len(read_classified(state_dir)["entries"]) == 1
    forced = run_verdict(MR, "2", "--class", "FP", "--reason", "r", "--force")
    assert forced.returncode == 0, forced.stderr
    entries = read_classified(state_dir)["entries"]
    assert len(entries) == 1  # replaced the reshuffled twin, no duplicate
    assert entries[0]["no"] == 2


# ── Usage errors (exit 2) ──


def test_usage_errors_exit2(state_dir):
    cases = [
        [],  # no args at all
        [MR, "1"],  # missing --class/--reason
        [MR, "1", "--reason", "r"],  # missing --class
        [MR, "1", "--class", "FP"],  # missing --reason
        [MR, "1", "--class", "tp", "--reason", "r"],  # unknown classification
        [MR, "1", "--class", "FP", "--reason", "r", "--priority", "critical"],
        [MR, "1", "--class", "FP", "--reason", "r", "--resolved", "maybe"],
        [MR, "abc", "--class", "FP", "--reason", "r"],  # non-integer ordinal
        [MR, "0", "--class", "FP", "--reason", "r"],  # ordinals start at 1
        ["../escape", "1", "--class", "FP", "--reason", "r"],  # unsafe state-dir name
        [MR, "1", "--class", "FP", "--reason", "   "],  # empty reason
    ]
    for argv in cases:
        proc = run_verdict(*argv)
        assert proc.returncode == 2, f"expected usage exit 2 for {argv}: {proc.stderr}"
        assert proc.stderr, f"expected a usage message for {argv}"


# ── End-to-end through post (offline fake API) ──


def test_q_verdict_end_to_end_through_post(tmp_path, monkeypatch):
    """The #58 recorded acceptance: verdict --class Q output feeds post green."""
    api_log = tmp_path / "api.jsonl"
    monkeypatch.chdir(tmp_path)
    pulled = run_pull("!9")
    assert pulled.returncode == 0, pulled.stderr
    state_dir = tmp_path / ".triage" / "!9"
    state_dir.mkdir(parents=True)
    (state_dir / "issues.json").write_text(pulled.stdout, encoding="utf-8")

    rec = run_verdict("!9", "1", "--class", "Q", "--reason", "needs team input")
    assert rec.returncode == 0, rec.stderr
    assert "no=1" in rec.stdout and AUTHOR_A in rec.stdout

    post = run_post("!9", "--mode", "triage",
                    "--classified", str(state_dir / "classified.json"), api_log=api_log)
    assert post.returncode == 0, post.stderr
    calls = read_api_log(api_log)
    body = reply_body(calls, "a1b2c3d4e5f60718")
    assert "⏸️ 需讨论" in body and "needs team input" in body
    assert not [c for c in calls if c["method"] == "PUT"]  # Q stays open


@pytest.mark.parametrize("cls,resolved_flag,resolves", [
    ("Edge", None, True),        # verdict-time Edge default → post resolves it
    ("Edge", "false", False),    # explicit override keeps it open
    ("Q", "true", True),         # explicit per-item close on a question
])
def test_resolved_decision_propagates_through_post(state_dir, tmp_path, monkeypatch,
                                                   cls, resolved_flag, resolves):
    api_log = tmp_path / "api.jsonl"
    argv = [MR, "1", "--class", cls, "--reason", "r"]
    if resolved_flag:
        argv += ["--resolved", resolved_flag]
    rec = run_verdict(*argv)
    assert rec.returncode == 0, rec.stderr

    post = run_post(MR, "--mode", "triage",
                    "--classified", str(state_dir / "classified.json"), api_log=api_log)
    assert post.returncode == 0, post.stderr
    puts = [c for c in read_api_log(api_log) if c["method"] == "PUT"]
    assert bool(puts) is resolves
    if resolves:
        assert DISC_A in puts[0]["url"]
