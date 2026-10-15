"""CLI-level tests for ocr-post-labels.py — ticket #61 (post execution semantics).

Covers the five hardened semantics: ① join validation — every entry's
discussion_id must byte-match an id in the pull state file, hard-fail with
the closest real id before any platform call; ② anchor recompute — the
entry anchor is verified against sha256(body) recomputed from the SAME
pull file; ③ content dedup — a thread already carrying the entry's anchor
marker gets no second reply; ④ reply failure blocks resolve unless
--force; ⑤ per-item resolved execution (Edge resolves, Q stays open) with
the posted:true write-back. Runs the real script as a subprocess against
the offline fake-curl stub; ids and hosts are synthetic.
"""

import hashlib
import json

import pytest

from conftest import POST_SCRIPT, read_api_log, run_post

MR = "!77"
DISC_A = "c3d4e5f607181920"
BODY_A = "Consider splitting this module before the next feature lands"
DISC_B = "d4e5f607181920aa11bb"
BODY_B = "Use a named constant for the retry limit instead of a literal"
GH_DISC = "9876543210001"
GH_BODY = "Consider splitting this module before the next feature lands"


def anchor_of(body):
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


def finding(no, disc_id, body):
    return {"no": no, "discussion_id": disc_id, "file": "src/app.py",
            "line": 1, "author": "ocr-bot", "body": body}


def write_pull(tmp_path, findings, mr=MR):
    state_dir = tmp_path / ".triage" / mr
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "issues.json").write_text(json.dumps(findings), encoding="utf-8")
    return state_dir


def write_classified(tmp_path, entries):
    path = tmp_path / ".triage" / MR / "classified.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema": 2, "entries": entries}), encoding="utf-8")
    return path


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    """cwd in a tmp checkout with the default two-finding pull state file."""
    monkeypatch.chdir(tmp_path)
    write_pull(tmp_path, [finding(1, DISC_A, BODY_A), finding(2, DISC_B, BODY_B)])
    return tmp_path


@pytest.fixture
def api_log(tmp_path):
    return tmp_path / "api.jsonl"


def serve(tmp_path, routes, name="routes.json"):
    """Write a test-local route table; fixture file values are emitted beside
    it (fake_api resolves them relative to the routes file). A value dict may
    carry "content" (object to serialize into "file")."""
    table = {}
    for pattern, value in routes.items():
        if isinstance(value, dict) and "content" in value:
            (tmp_path / value["file"]).write_text(
                json.dumps(value["content"], ensure_ascii=False), encoding="utf-8")
            value = {k: v for k, v in value.items() if k != "content"}
        table[pattern] = value
    path = tmp_path / name
    path.write_text(json.dumps(table), encoding="utf-8")
    return str(path)


def marked_thread_routes(tmp_path, anchor, disc_id=DISC_A):
    """A thread whose wall already carries the verdict marker for `anchor`.
    The sweep's listing GET needs its own (empty) route — "discussions?per_page"
    wins before "/discussions" because fake_api is first-pattern-wins."""
    thread = {"id": disc_id, "notes": [
        {"id": 201, "resolvable": True, "resolved": False,
         "body": f"### 🟡 边缘\n\n**原因**: earlier verdict\n\n<!-- triage-anchor: {anchor} -->"}]}
    return serve(tmp_path, {"discussions?per_page": {"file": "listing.json", "content": []},
                            "/discussions": {"file": "thread.json", "content": thread}})


def replyfail_routes():
    """Static fixture: reply POST gets 422 while the dedup/resolve GETs and the
    resolve PUT succeed (method-scoped route)."""
    return "post_replyfail_routes.json"


def assert_no_platform_calls(proc, api_log):
    assert "Detected platform" not in proc.stderr
    assert "Done:" not in proc.stderr
    assert read_api_log(api_log) == []


def reply_bodies(calls, disc_id):
    return [json.loads(c["data"])["body"] for c in calls
            if c["method"] == "POST" and disc_id in c["url"]]


# ── ① join validation: discussion_id must byte-match the pull file ──


def test_truncated_id_hard_fails_naming_closest_real_id(workdir, api_log):
    entries = [{"discussion_id": DISC_A[:8], "no": 1, "anchor": anchor_of(BODY_A),
                "classification": "FP", "reason": "r", "resolved": True}]
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--classified", str(path), api_log=api_log)
    assert proc.returncode == 1
    assert "no=1" in proc.stderr
    assert DISC_A in proc.stderr  # closest real id, byte-exact
    assert "byte" in proc.stderr
    assert_no_platform_calls(proc, api_log)


def test_forged_id_hard_fails_without_similar_id(workdir, api_log):
    entries = [{"discussion_id": "deadbeefcafebabe1234", "no": 2,
                "classification": "FP", "reason": "r", "resolved": True}]
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--classified", str(path), api_log=api_log)
    assert proc.returncode == 1
    assert "no=2" in proc.stderr
    assert "no similar id" in proc.stderr
    assert_no_platform_calls(proc, api_log)


def test_missing_pull_file_hard_fails_with_pull_hint(workdir, api_log):
    (workdir / ".triage" / MR / "issues.json").unlink()
    path = write_classified(workdir, [{"discussion_id": DISC_A, "classification": "FP", "reason": "r"}])
    proc = run_post(MR, "--classified", str(path), api_log=api_log)
    assert proc.returncode == 1
    assert "issues.json" in proc.stderr and "ocr-pull-discussions.py" in proc.stderr
    assert_no_platform_calls(proc, api_log)


def test_pull_file_override_param(workdir, tmp_path, api_log):
    alt = tmp_path / "elsewhere" / "issues.json"
    alt.parent.mkdir()
    alt.write_text(json.dumps([finding(1, DISC_A, BODY_A)]), encoding="utf-8")
    entries = [{"discussion_id": DISC_A, "classification": "FP", "reason": "r", "resolved": True}]
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--pull-file", str(alt), "--classified", str(path), api_log=api_log)
    assert proc.returncode == 0, proc.stderr
    assert reply_bodies(read_api_log(api_log), DISC_A)


# ── ② anchor recompute from the same pull file ──


def test_anchor_mismatch_hard_fails(workdir, api_log):
    entries = [{"discussion_id": DISC_A, "no": 1, "anchor": "0123456789abcdef",
                "classification": "FP", "reason": "r", "resolved": True}]
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--classified", str(path), api_log=api_log)
    assert proc.returncode == 1
    assert "anchor mismatch" in proc.stderr and "no=1" in proc.stderr
    assert_no_platform_calls(proc, api_log)


def test_valid_anchor_recomputed_from_same_pull_passes(workdir, api_log):
    """Verdict-shaped entries whose anchors match the pull file digest end to
    end — a reviewer editing the live comment later cannot false-reject here,
    because both verdict and post read the same stale pull snapshot."""
    entries = [
        {"discussion_id": DISC_A, "no": 1, "anchor": anchor_of(BODY_A),
         "classification": "FP", "reason": "design intent", "resolved": True},
        {"discussion_id": DISC_B, "no": 2, "anchor": anchor_of(BODY_B),
         "classification": "Q", "reason": "needs input"},
    ]
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--classified", str(path), api_log=api_log)
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    # the anchor marker rides on the wall — the key content dedup searches for
    assert f"<!-- triage-anchor: {anchor_of(BODY_A)} -->" in reply_bodies(calls, DISC_A)[0]
    puts = [c for c in calls if c["method"] == "PUT"]
    assert len(puts) == 1 and DISC_A in puts[0]["url"]  # FP resolves, Q stays open


# ── ③ content dedup: marker already on the wall → no second reply ──


def test_dedup_skips_reply_but_still_resolves(workdir, tmp_path, api_log):
    entries = [{"discussion_id": DISC_A, "no": 1, "anchor": anchor_of(BODY_A),
                "classification": "Edge", "reason": "earlier verdict",
                "resolved": True, "posted": False}]
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--classified", str(path), api_log=api_log,
                    routes_file=marked_thread_routes(tmp_path, anchor_of(BODY_A)))
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    assert not [c for c in calls if c["method"] == "POST"]  # zero new replies
    assert [c for c in calls if c["method"] == "PUT"]       # resolve still executes
    assert "content dedup" in proc.stderr
    # posted stays untouched for a dedup-skipped entry — delivery happened in a
    # previous run; content, not the flag, is the idempotency source here
    assert json.loads(path.read_text())["entries"][0]["posted"] is False


def test_dedup_leaves_q_open_without_resolve(workdir, tmp_path, api_log):
    entries = [{"discussion_id": DISC_A, "no": 1, "anchor": anchor_of(BODY_A),
                "classification": "Q", "reason": "earlier verdict", "resolved": False}]
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--classified", str(path), api_log=api_log,
                    routes_file=marked_thread_routes(tmp_path, anchor_of(BODY_A)))
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    assert not [c for c in calls if c["method"] == "POST"]
    assert not [c for c in calls if c["method"] == "PUT"]


def test_unrelated_thread_still_gets_its_reply(workdir, tmp_path, api_log):
    """The dedup check is anchor-specific: a marker for another verdict on the
    canned thread must not suppress this entry."""
    entries = [{"discussion_id": DISC_A, "no": 1, "anchor": anchor_of(BODY_A),
                "classification": "FP", "reason": "r", "resolved": True}]
    path = write_classified(workdir, entries)
    other = anchor_of("a different verdict body")
    proc = run_post(MR, "--classified", str(path), api_log=api_log,
                    routes_file=marked_thread_routes(tmp_path, other))
    assert proc.returncode == 0, proc.stderr
    assert reply_bodies(read_api_log(api_log), DISC_A)


# ── ④ reply failure blocks resolve (unless --force) ──


def test_reply_failure_blocks_resolve(workdir, api_log):
    entries = [{"discussion_id": DISC_A, "no": 1, "anchor": anchor_of(BODY_A),
                "classification": "Edge", "reason": "r", "resolved": True}]
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--classified", str(path), api_log=api_log,
                    routes_file=replyfail_routes())
    assert proc.returncode == 1
    assert not [c for c in read_api_log(api_log) if c["method"] == "PUT"]  # never closed
    assert "NOT resolving" in proc.stderr
    assert json.loads(path.read_text())["entries"][0].get("posted") is not True


def test_reply_failure_with_force_resolves_but_counts_fail(workdir, api_log):
    entries = [{"discussion_id": DISC_A, "no": 1, "anchor": anchor_of(BODY_A),
                "classification": "Edge", "reason": "r", "resolved": True}]
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--force", "--classified", str(path), api_log=api_log,
                    routes_file=replyfail_routes())
    assert proc.returncode == 1  # the verdict reason is still not on the wall
    assert [c for c in read_api_log(api_log) if c["method"] == "PUT"]  # --force overrides
    assert "resolving anyway" in proc.stderr


def test_reply_failure_fails_even_without_resolve_request(workdir, api_log):
    entries = [{"discussion_id": DISC_A, "no": 1, "anchor": anchor_of(BODY_A),
                "classification": "Q", "reason": "r", "resolved": False}]
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--classified", str(path), api_log=api_log,
                    routes_file=replyfail_routes())
    assert proc.returncode == 1
    assert not [c for c in read_api_log(api_log) if c["method"] == "PUT"]


# ── ⑤ per-item resolved execution + posted write-back ──


def test_edge_resolves_and_q_stays_open_per_item(workdir, api_log):
    """The verdict-time decision rides in the entry; post executes, never judges."""
    entries = [
        {"discussion_id": DISC_A, "no": 1, "anchor": anchor_of(BODY_A),
         "classification": "Edge", "reason": "r", "resolved": True},
        {"discussion_id": DISC_B, "no": 2, "anchor": anchor_of(BODY_B),
         "classification": "Q", "reason": "r", "resolved": False},
    ]
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--mode", "triage", "--classified", str(path), api_log=api_log)
    assert proc.returncode == 0, proc.stderr
    puts = [c for c in read_api_log(api_log) if c["method"] == "PUT"]
    assert len(puts) == 1 and DISC_A in puts[0]["url"]


def test_legacy_entry_without_resolved_keeps_mode_map(workdir, api_log):
    entries = [{"discussion_id": DISC_A, "no": 1, "anchor": anchor_of(BODY_A),
                "classification": "Edge", "reason": "r"}]  # legacy dual-mode: no resolved field
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--classified", str(path), api_log=api_log)  # default mode
    assert proc.returncode == 0, proc.stderr
    assert not [c for c in read_api_log(api_log) if c["method"] == "PUT"]


def test_posted_flag_written_back_on_success(workdir, api_log):
    entries = [
        {"discussion_id": DISC_A, "no": 1, "anchor": anchor_of(BODY_A),
         "classification": "FP", "reason": "r", "resolved": True, "posted": False},
        {"discussion_id": DISC_B, "no": 2, "anchor": anchor_of(BODY_B),
         "classification": "Q", "reason": "r"},
    ]
    path = write_classified(workdir, entries)
    proc = run_post(MR, "--classified", str(path), api_log=api_log)
    assert proc.returncode == 0, proc.stderr
    saved = json.loads(path.read_text())["entries"]
    assert saved[0]["posted"] is True
    assert saved[1]["posted"] is True


def test_docstring_semantics_rewritten():
    text = POST_SCRIPT.read_text(encoding="utf-8")
    assert "stay open in both modes" not in text
    assert "--pull-file" in text and "--force" in text


# ── GitHub side ──


def test_github_forged_id_zero_platform_calls(workdir, api_log):
    write_pull(workdir, [finding(1, GH_DISC, GH_BODY)], mr="1")
    entries = [{"discussion_id": "deadbeefcafebabe", "no": 1,
                "classification": "FP", "reason": "r"}]
    path = write_classified(workdir, entries)
    proc = run_post("1", "--classified", str(path), platform="github", api_log=api_log)
    assert proc.returncode == 1
    assert_no_platform_calls(proc, api_log)


def test_github_dedup_skips_reply(workdir, tmp_path, api_log):
    write_pull(workdir, [finding(1, GH_DISC, GH_BODY)], mr="1")
    anchor = anchor_of(GH_BODY)
    routes = serve(tmp_path, {
        "GET /replies": {"file": "replies_marked.json", "content": [
            {"id": 555, "body": f"### 🟡 边缘\n\n**原因**: earlier\n\n<!-- triage-anchor: {anchor} -->"}]},
        "/replies": {"file": "replies_other.json", "content": []},
        "/pulls/comments": {"file": "comment.json", "content": {"id": 555, "body": GH_BODY}},
        "/comments": {"file": "comments.json", "content": []},
        # summary sweep: PR fetch + an empty reviewThreads listing (no summaries)
        "/pulls/1": {"file": "pr.json", "content": {"number": 1, "node_id": "PR_node_1"}},
        "reviewThreads": {"file": "threads.json",
                          "content": {"data": {"node": {"reviewThreads": {"nodes": []}}}}},
    })
    entries = [{"discussion_id": GH_DISC, "no": 1, "anchor": anchor,
                "classification": "Edge", "reason": "r", "resolved": True}]
    path = write_classified(workdir, entries)
    proc = run_post("1", "--classified", str(path), platform="github",
                    api_log=api_log, routes_file=routes)
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    assert not [c for c in calls if c["method"] == "POST"]
    assert "content dedup" in proc.stderr


def test_github_reply_failure_blocks_resolve(workdir, tmp_path, api_log):
    write_pull(workdir, [finding(1, GH_DISC, GH_BODY)], mr="1")
    routes = serve(tmp_path, {
        "POST /replies": {"status": 422},
        "POST /comments": {"status": 422},
        "GET /replies": {"file": "replies.json", "content": []},
        "/pulls/comments": {"file": "comment.json", "content": {"id": 555, "body": GH_BODY}},
        "/comments": {"file": "comments.json", "content": []},
    })
    entries = [{"discussion_id": GH_DISC, "no": 1, "anchor": anchor_of(GH_BODY),
                "classification": "Edge", "reason": "r", "resolved": True}]
    path = write_classified(workdir, entries)
    proc = run_post("1", "--classified", str(path), platform="github",
                    api_log=api_log, routes_file=routes)
    assert proc.returncode == 1
    assert "NOT resolving" in proc.stderr
    assert "resolve failed" not in proc.stderr  # resolve never attempted


def test_github_edge_resolved_true_attempts_resolve(workdir, tmp_path, api_log):
    write_pull(workdir, [finding(1, GH_DISC, GH_BODY)], mr="1")
    entries = [{"discussion_id": GH_DISC, "no": 1, "anchor": anchor_of(GH_BODY),
                "classification": "Edge", "reason": "r", "resolved": True}]
    path = write_classified(workdir, entries)
    # PR fetch + an empty reviewThreads listing: the resolve mutation itself
    # stays unrouteable offline → the warn proves the attempt happened
    routes = serve(tmp_path, {
        "/comments": {"file": "comments.json", "content": []},
        "/pulls/1": {"file": "pr.json", "content": {"number": 1, "node_id": "PR_node_1"}},
        "reviewThreads": {"file": "threads.json",
                          "content": {"data": {"node": {"reviewThreads": {"nodes": []}}}}},
    })
    proc = run_post("1", "--mode", "triage", "--classified", str(path),
                    platform="github", api_log=api_log, routes_file=routes)
    assert proc.returncode == 0, proc.stderr
    # graphql resolve is unserveable offline → the warn proves the attempt happened
    assert "resolve failed" in proc.stderr
