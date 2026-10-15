"""Ticket #64 CLI-level tests: verify display de-truncation + pipeline gate.

Spec #57 test seam: real script subprocess, platform API replaced by offline
fixtures (fake curl/gh first on PATH, synthetic ids only). Covers the display
contract (ordinal / content-anchor labels, zero platform-id shapes, [N/M
notes open] annotation, --json full ids) and the Amendment R2 修订 B timing
gate (running → exit 2, --skip-pipeline-check override, terminal → normal
exits, no-CI note path) on both ocr-verify-resolved.py and
ocr-pull-discussions.py.

Pipeline-status tests bring their own per-state route tables (tmp_path)
because the GitLab pipeline status rides in the MR-detail response the gate
queries; fixture bodies stay id-shape-free so the existing truncation-shape
assertions stay honest.
"""

import hashlib
import json

import pytest

from conftest import FIXTURES_DIR, run_pull, run_verify

# ── Synthetic terrain ──

ID_INLINE = "a1b2c3d4e5f60718"
ID_GENERAL = "c3d4e5f607181920"
ID_SUMMARY = "d4e5f607181920a1"
ID_MULTI = "e5f607181920a1b2"
ALL_IDS = [ID_INLINE, ID_GENERAL, ID_SUMMARY, ID_MULTI]

MAPPED_BODY = "Use a named constant for the retry limit instead of a literal"
GENERAL_BODY = "Consider splitting this module before the next feature lands"
SUMMARY_BODY = "🔍 OpenCodeReview run report — 3 findings pulled, triage started"
RENAME_BODY = "Rename helper to match domain vocabulary"
REPLY_BODY = "Still open — waiting on the rename in the follow-up commit"


def _anchor(body):
    """Expected display anchor: same shape the script derives from the body."""
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:8]


def gitlab_discussions():
    """One MR: mapped inline + mapped general + unmapped summary thread +
    a mapped multi-note thread (head resolved, reply open) for the [N/M]
    annotation."""
    return [
        {"id": ID_INLINE, "notes": [
            {"id": 201, "body": MAPPED_BODY, "author": {"username": "ocr-bot"},
             "resolvable": True,
             "position": {"new_path": "src/app.py", "new_line": 42}}]},
        {"id": ID_GENERAL, "notes": [
            {"id": 202, "body": GENERAL_BODY,
             "author": {"username": "human-reviewer"}, "resolvable": True}]},
        {"id": ID_SUMMARY, "notes": [
            {"id": 203, "body": SUMMARY_BODY, "author": {"username": "ocr-bot"},
             "resolvable": True}]},
        {"id": ID_MULTI, "notes": [
            {"id": 204, "body": RENAME_BODY, "author": {"username": "ocr-bot"},
             "resolvable": True, "resolved": True},
            {"id": 205, "body": REPLY_BODY, "author": {"username": "ocr-bot"},
             "resolvable": True, "resolved": False}]},
    ]


def gitlab_discussions_all_resolved():
    return [
        {"id": ID_INLINE, "notes": [
            {"id": 201, "body": MAPPED_BODY, "author": {"username": "ocr-bot"},
             "resolvable": True, "resolved": True}]},
        {"id": ID_GENERAL, "notes": [
            {"id": 202, "body": GENERAL_BODY,
             "author": {"username": "human-reviewer"},
             "resolvable": True, "resolved": True}]},
    ]


def pull_state_file():
    """The bare findings array ocr-pull-discussions.py writes to stdout and
    the agent redirects into .triage/<MR>/issues.json. Summary thread is
    deliberately absent — pull filters it, the gate still counts it."""
    return [
        {"no": 1, "discussion_id": ID_INLINE, "file": "src/app.py", "line": 42,
         "body": MAPPED_BODY, "author": "ocr-bot"},
        {"no": 2, "discussion_id": ID_GENERAL, "file": "(general)", "line": 0,
         "body": GENERAL_BODY, "author": "human-reviewer"},
        {"no": 3, "discussion_id": ID_MULTI, "file": "src/naming.py", "line": 7,
         "body": RENAME_BODY, "author": "ocr-bot"},
    ]


def write_state_dir(tmp_path, content=None):
    state = tmp_path / ".triage" / "9"
    state.mkdir(parents=True, exist_ok=True)
    (state / "issues.json").write_text(
        content if content is not None else json.dumps(pull_state_file()))
    return state / "issues.json"


def mr_detail(pipeline_status):
    """MR-detail body; None status → head_pipeline null (no CI configured)."""
    pipeline = ({"status": pipeline_status}
                if pipeline_status is not None else None)
    return {"iid": 9, "title": "triage fixture MR", "state": "opened",
            "web_url": "https://gitlab.example/group/proj/-/merge_requests/9",
            "head_pipeline": pipeline}


def gitlab_routes(tmp_path, discussions, pipeline_status):
    (tmp_path / "discussions.json").write_text(json.dumps(discussions))
    (tmp_path / "mr_detail.json").write_text(
        json.dumps(mr_detail(pipeline_status)))
    routes = tmp_path / "routes.json"
    # "/discussions" must win over "/merge_requests/9" for the discussions
    # URL — fake_api serves the first matching pattern.
    routes.write_text(json.dumps({
        "/discussions": str(tmp_path / "discussions.json"),
        "/merge_requests/9": str(tmp_path / "mr_detail.json"),
    }))
    return routes


GITHUB_HEAD_SHA = "abc123def4567890abcdef1234567890abcd"


def github_routes(tmp_path, check_runs):
    (tmp_path / "pr.json").write_text(json.dumps({
        "node_id": "PR_node_fixture_1", "title": "triage fixture PR",
        "state": "open",
        "html_url": "https://github.com/owner/repo/pull/9",
        "head": {"sha": GITHUB_HEAD_SHA}}))
    (tmp_path / "check_runs.json").write_text(json.dumps(check_runs))
    routes = tmp_path / "routes.json"
    routes.write_text(json.dumps({
        "/comments": str(FIXTURES_DIR / "github" / "comments.json"),
        "/check-runs": str(tmp_path / "check_runs.json"),
        "/pulls/9": str(tmp_path / "pr.json"),
    }))
    return routes


RUNNING_CHECK_RUNS = {"total_count": 2, "check_runs": [
    {"name": "lint", "status": "completed", "conclusion": "success"},
    {"name": "test", "status": "in_progress", "conclusion": None}]}
DONE_CHECK_RUNS = {"total_count": 2, "check_runs": [
    {"name": "lint", "status": "completed", "conclusion": "success"},
    {"name": "test", "status": "completed", "conclusion": "failure"}]}
NO_CHECK_RUNS = {"total_count": 0, "check_runs": []}


# ── Display de-truncation (verify human output) ──


def test_verify_labels_mapped_threads_with_ordinals(tmp_path):
    write_state_dir(tmp_path)
    routes = gitlab_routes(tmp_path, gitlab_discussions(), "success")
    proc = run_verify("9", routes=routes, cwd=tmp_path)
    assert proc.returncode == 1  # threads open — normal thread-state exit
    for no in (1, 2, 3):
        assert f"no={no}" in proc.stderr
    assert "[1/2 notes open]" in proc.stderr  # S1 annotation preserved
    # Zero platform-id shapes — full or truncated (the [:12] form died here).
    for disc_id in ALL_IDS:
        assert disc_id not in proc.stderr
        assert disc_id[:12] not in proc.stderr
    # Ordinals came from the default .triage/9/issues.json — no --pull-file
    # was passed, so the mapped labels themselves prove the default path.


def test_verify_unmapped_thread_gets_content_anchor(tmp_path):
    write_state_dir(tmp_path)
    routes = gitlab_routes(tmp_path, gitlab_discussions(), "success")
    proc = run_verify("9", routes=routes, cwd=tmp_path)
    assert proc.returncode == 1
    assert f"anchor={_anchor(SUMMARY_BODY)}" in proc.stderr
    assert ID_SUMMARY not in proc.stderr
    assert ID_SUMMARY[:12] not in proc.stderr


def test_verify_without_pull_file_uses_anchors(tmp_path):
    routes = gitlab_routes(tmp_path, gitlab_discussions(), "success")
    proc = run_verify("9", routes=routes, cwd=tmp_path)  # no .triage/ in cwd
    assert proc.returncode == 1
    assert "no=" not in proc.stderr
    assert proc.stderr.count("anchor=") == 4
    for disc_id in ALL_IDS:
        assert disc_id[:12] not in proc.stderr


def test_verify_explicit_pull_file_flag_maps_ordinals(tmp_path):
    custom = tmp_path / "custom-issues.json"
    custom.write_text(json.dumps(pull_state_file()))
    routes = gitlab_routes(tmp_path, gitlab_discussions(), "success")
    proc = run_verify("9", "--pull-file", str(custom),
                      routes=routes, cwd=tmp_path)
    assert proc.returncode == 1
    assert "no=1" in proc.stderr and "no=3" in proc.stderr


def test_verify_missing_explicit_pull_file_notes(tmp_path):
    missing = tmp_path / "nope" / "issues.json"
    routes = gitlab_routes(tmp_path, gitlab_discussions(), "success")
    proc = run_verify("9", "--pull-file", str(missing),
                      routes=routes, cwd=tmp_path)
    assert proc.returncode == 1
    assert "--pull-file not found" in proc.stderr
    assert str(missing) in proc.stderr
    assert "anchor=" in proc.stderr  # degrades to anchors, never ids


def test_verify_corrupt_pull_file_warns_and_degrades(tmp_path):
    write_state_dir(tmp_path, content="{not json")
    routes = gitlab_routes(tmp_path, gitlab_discussions(), "success")
    proc = run_verify("9", routes=routes, cwd=tmp_path)
    assert proc.returncode == 1
    assert "WARN" in proc.stderr
    assert "issues.json" in proc.stderr  # names the file
    assert "anchor=" in proc.stderr


def test_verify_json_keeps_full_ids(tmp_path):
    write_state_dir(tmp_path)
    routes = gitlab_routes(tmp_path, gitlab_discussions(), "success")
    proc = run_verify("9", "--json", routes=routes, cwd=tmp_path)
    assert proc.returncode == 1  # script chains rely on thread-state exits
    threads = json.loads(proc.stdout)
    assert [t["discussion_id"] for t in threads] == ALL_IDS
    assert "_body" not in proc.stdout  # internal field never leaks
    multi = next(t for t in threads if t["discussion_id"] == ID_MULTI)
    assert "[1/2 notes open]" in multi["body_preview"]
    summary = next(t for t in threads if t["discussion_id"] == ID_SUMMARY)
    assert summary["is_ocr_summary"] is True


def test_verify_all_resolved_exits_zero(tmp_path):
    routes = gitlab_routes(tmp_path, gitlab_discussions_all_resolved(),
                           "success")
    proc = run_verify("9", routes=routes, cwd=tmp_path)
    assert proc.returncode == 0
    assert "0 open" in proc.stderr


# ── Pipeline timing gate (verify, GitLab) ──


def test_verify_pipeline_running_exits_2(tmp_path):
    write_state_dir(tmp_path)
    routes = gitlab_routes(tmp_path, gitlab_discussions(), "running")
    proc = run_verify("9", routes=routes, cwd=tmp_path)
    assert proc.returncode == 2
    assert "not finished" in proc.stderr
    assert "--skip-pipeline-check" in proc.stderr
    assert "running" in proc.stderr
    assert proc.stdout == ""  # no thread data leaks past the gate


def test_verify_pipeline_running_skip_flag_proceeds(tmp_path):
    write_state_dir(tmp_path)
    routes = gitlab_routes(tmp_path, gitlab_discussions(), "running")
    proc = run_verify("9", "--skip-pipeline-check", routes=routes, cwd=tmp_path)
    assert proc.returncode == 1  # thread-state exit, not the gate's 2
    assert "no=1" in proc.stderr


@pytest.mark.parametrize("status", ["success", "failed", "skipped"])
def test_verify_pipeline_terminal_statuses_proceed_normally(status, tmp_path):
    write_state_dir(tmp_path)
    routes = gitlab_routes(tmp_path, gitlab_discussions(), status)
    proc = run_verify("9", routes=routes, cwd=tmp_path)
    assert proc.returncode == 1
    assert "not finished" not in proc.stderr
    assert "no=1" in proc.stderr


def test_verify_no_pipeline_proceeds_with_note(tmp_path):
    write_state_dir(tmp_path)
    routes = gitlab_routes(tmp_path, gitlab_discussions(), None)
    proc = run_verify("9", routes=routes, cwd=tmp_path)
    assert proc.returncode == 1  # note, not an error
    assert "no CI" in proc.stderr
    assert "no=1" in proc.stderr


# ── Pipeline timing gate (verify, GitHub check runs) ──


def test_verify_github_check_runs_running_exits_2(tmp_path):
    routes = github_routes(tmp_path, RUNNING_CHECK_RUNS)
    proc = run_verify("9", platform="github", routes=routes)
    assert proc.returncode == 2
    assert "not finished" in proc.stderr
    assert "--skip-pipeline-check" in proc.stderr


@pytest.mark.parametrize("status", ["waiting", "pending", "requested"])
def test_verify_github_check_run_nonterminal_statuses_in_flight(status, tmp_path):
    """M4: waiting/pending/requested check runs are nonterminal — they used to
    fall through to completed, passing the timing gate while CI is unfinished
    (e.g. a job waiting for environment approval)."""
    routes = github_routes(tmp_path, {"total_count": 1, "check_runs": [
        {"name": "gate", "status": status, "conclusion": None}]})
    proc = run_verify("9", platform="github", routes=routes)
    assert proc.returncode == 2, proc.stderr
    assert status in proc.stderr


def test_verify_github_check_runs_paginated_before_completed(tmp_path):
    """M3: the completion gate aggregates every check-run page — a head with
    >100 checks used to read only the first page and declare completed while
    an active check sat on page 2."""
    completed = [{"name": f"check-{i}", "status": "completed",
                  "conclusion": "success"} for i in range(100)]
    page1 = {"total_count": 101, "check_runs": completed}
    page2 = {"total_count": 101, "check_runs": [
        {"name": "slow", "status": "queued", "conclusion": None}]}
    (tmp_path / "pr.json").write_text(json.dumps({
        "node_id": "PR_node_fixture_1", "title": "triage fixture MR",
        "state": "open",
        "html_url": "https://github.com/owner/repo/pull/9",
        "head": {"sha": GITHUB_HEAD_SHA}}))
    (tmp_path / "page1.json").write_text(json.dumps(page1))
    (tmp_path / "page2.json").write_text(json.dumps(page2))
    routes = tmp_path / "routes.json"
    # page-2 pattern must precede the generic /check-runs (first match wins)
    routes.write_text(json.dumps({
        "/comments": str(FIXTURES_DIR / "github" / "comments.json"),
        "check-runs?per_page=100&page=2": str(tmp_path / "page2.json"),
        "/check-runs": str(tmp_path / "page1.json"),
        "/pulls/9": str(tmp_path / "pr.json"),
    }))
    proc = run_verify("9", platform="github", routes=str(routes))
    assert proc.returncode == 2, proc.stderr
    assert "queued" in proc.stderr


# ── Pipeline timing gate (pull) ──


def test_pull_pipeline_running_exits_2(tmp_path):
    routes = gitlab_routes(tmp_path, gitlab_discussions(), "running")
    proc = run_pull("9", routes=routes)
    assert proc.returncode == 2
    assert "not finished" in proc.stderr
    assert "--skip-pipeline-check" in proc.stderr
    assert proc.stdout == ""  # findings never leave the script pre-gate


def test_pull_pipeline_running_skip_flag_pulls(tmp_path):
    routes = gitlab_routes(tmp_path, gitlab_discussions(), "running")
    proc = run_pull("9", "--skip-pipeline-check", routes=routes)
    assert proc.returncode == 0
    findings = json.loads(proc.stdout)
    # 1=inline, 2=general; the multi-note thread is skipped by pull (head
    # note resolved) and the summary by the review-content filter.
    assert [f["no"] for f in findings] == [1, 2]


def test_pull_pipeline_completed_exits_zero(tmp_path):
    routes = gitlab_routes(tmp_path, gitlab_discussions(), "success")
    proc = run_pull("9", routes=routes)
    assert proc.returncode == 0
    assert json.loads(proc.stdout)


def test_pull_no_pipeline_proceeds_with_note(tmp_path):
    routes = gitlab_routes(tmp_path, gitlab_discussions(), None)
    proc = run_pull("9", routes=routes)
    assert proc.returncode == 0
    assert "no CI" in proc.stderr
    assert json.loads(proc.stdout)


def test_pull_github_check_runs_running_exits_2(tmp_path):
    routes = github_routes(tmp_path, RUNNING_CHECK_RUNS)
    proc = run_pull("9", platform="github", routes=routes)
    assert proc.returncode == 2
    assert "not finished" in proc.stderr
    assert proc.stdout == ""


def test_pull_github_check_runs_completed_pulls(tmp_path):
    routes = github_routes(tmp_path, DONE_CHECK_RUNS)
    proc = run_pull("9", platform="github", routes=routes)
    assert proc.returncode == 0
    assert json.loads(proc.stdout)


def test_pull_github_no_check_runs_notes_and_proceeds(tmp_path):
    routes = github_routes(tmp_path, NO_CHECK_RUNS)
    proc = run_pull("9", platform="github", routes=routes)
    assert proc.returncode == 0
    assert "no CI" in proc.stderr
