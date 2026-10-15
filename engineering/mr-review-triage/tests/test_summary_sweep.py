"""CLI-level tests for ocr-post-labels.py — ticket #62 (summary-thread sweep).

Post absorbs the OCR summary threads (spec #57 Q6 AMEND): after the
classified findings are posted it sweeps the remaining resolvable
🔍 start / ✅ end+LGTM / ⚠️ error threads itself — the last routine
manual-API path dies. Three template classes: start = confirmation (no
stats, resolved only when an ✅ end thread completed the run), end/LGTM =
statistics (counts from the classified entries + TP fix files) then
resolve, error = fixed escalation, reply ONLY and the run exits non-zero
(gate stays red by design — human-in-loop). Every sweep reply carries the
#61 anchor marker so a re-run posts nothing.

GitHub side pins the dual-ID-space fix (#62): the sweep's REST reply uses
the comment databaseId and its GraphQL resolve uses the thread node id,
both taken from ONE reviewThreads listing — no node id ever rides a REST
path and verify --json ids are never consumed. Also covers the
_resolve_github_thread silent-success fix (thread-not-found reports
failure instead of returning True).

Runs the real script as a subprocess against the offline fake-curl/gh
stub; ids and hosts are synthetic.
"""

import hashlib
import json

import pytest

from conftest import read_api_log, run_post

MR = "!77"
START_DISC = "a1b2c3d4e5f60718"
END_DISC = "b2c3d4e5f6071819"
ERR_DISC = "c3d4e5f607181920"
FALLBACK_DISC = "d4e5f607181920aa"
FINDING_DISC = "e5f607181920aabb"

START_BODY = "🔍 OpenCodeReview 开始审查 MR!77 的 diff"
END_BODY = "✅ OpenCodeReview: found 3 issues (0 critical)"
ERROR_BODY = "⚠️ OpenCodeReview error: runner failed after 3 attempts"
FALLBACK_BODY = ("🔍 OpenCodeReview — issues that could not be posted inline:\n\n---\n\n"
                 "### `src/x.py` (L1-L1)\n\ntext")
FINDING_BODY = "Use a named constant for the retry limit instead of a literal"

GH_START_NODE, GH_END_NODE, GH_ERR_NODE = "PRRT_startnode1", "PRRT_endnode12", "PRRT_errornode"
GH_START_CMT, GH_END_CMT, GH_ERR_CMT = 8001, 8002, 8003
GH_PR_NODE = "PR_node_sweep_1"
GH_START_BODY = "🔍 OpenCodeReview started reviewing PR #1"
GH_END_BODY = "✅ OpenCodeReview: found 3 issues (0 critical)"
GH_ERR_BODY = "⚠️ OpenCodeReview error: runner failed"
GH_DISC = "9876543210001"
GH_BODY = "Consider splitting this module before the next feature lands"


def anchor_of(body):
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


def classified(*entries):
    return json.dumps({"schema": 2, "entries": list(entries)})


def finding(no, disc_id, body, file="src/app.py"):
    return {"no": no, "discussion_id": disc_id, "file": file,
            "line": 1, "author": "ocr-bot", "body": body}


def write_pull(tmp_path, findings, mr=MR):
    state_dir = tmp_path / ".triage" / mr
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "issues.json").write_text(json.dumps(findings), encoding="utf-8")
    return state_dir


def write_classified(tmp_path, entries, mr=MR):
    path = tmp_path / ".triage" / mr / "classified.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema": 2, "entries": entries}), encoding="utf-8")
    return path


def stats_fixture():
    """7 findings → TP 2 / FP 1 / Edge 1 / OOS 1 / Q 2; TP files app.py+util.py."""
    specs = [("TP", "src/app.py"), ("TP", "src/util.py"), ("FP", "src/other.py"),
             ("Edge", "src/edge.py"), ("OOS", "src/oos.py"), ("Q", "src/q1.py"),
             ("Q", "src/q2.py")]
    findings, entries = [], []
    for i, (cls, file) in enumerate(specs, 1):
        disc = f"{i:016x}"
        body = f"finding {i} body"
        findings.append(finding(i, disc, body, file=file))
        entries.append({"discussion_id": disc, "no": i, "anchor": anchor_of(body),
                        "classification": cls, "reason": "r", "resolved": False})
    return findings, entries


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_pull(tmp_path, [finding(1, FINDING_DISC, FINDING_BODY)])
    return tmp_path


@pytest.fixture
def gh_workdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_pull(tmp_path, [finding(1, GH_DISC, GH_BODY)], mr="1")
    return tmp_path


@pytest.fixture
def api_log(tmp_path):
    return tmp_path / "api.jsonl"


def serve(tmp_path, routes):
    """Write a test-local route table; "content" values are serialized into
    fixture files emitted beside it (fake_api resolves them relatively)."""
    table = {}
    for pattern, value in routes.items():
        if isinstance(value, dict) and "content" in value:
            (tmp_path / value["file"]).write_text(
                json.dumps(value["content"], ensure_ascii=False), encoding="utf-8")
            value = {k: v for k, v in value.items() if k != "content"}
        table[pattern] = value
    path = tmp_path / "routes.json"
    path.write_text(json.dumps(table), encoding="utf-8")
    return str(path)


def summary_thread(disc_id, body, note_id=300):
    return {"id": disc_id, "notes": [
        {"id": note_id, "body": body, "author": {"username": "ocr-bot"},
         "resolvable": True, "resolved": False}]}


def marked_summary_thread(disc_id, body, marker, note_id=300):
    """A summary thread whose wall already carries a previous sweep reply."""
    return {"id": disc_id, "notes": [
        {"id": note_id, "body": body, "author": {"username": "ocr-bot"},
         "resolvable": True, "resolved": False},
        {"id": note_id + 1, "body": f"earlier sweep reply\n\n{marker}",
         "author": {"username": "triage-agent"}, "resolvable": False}]}


def sweep_routes(tmp_path, listing, overrides=None):
    """Ordered GitLab sweep route table — fake_api is first-pattern-wins, so
    the listing pattern must precede the generic per-thread patterns."""
    table = dict(overrides or {})
    table["discussions?per_page"] = {"file": "listing.json", "content": listing}
    table["GET /discussions/"] = {"file": "thread.json",
                                  "content": {"id": "t", "notes": []}}
    table["PUT /discussions"] = {}
    table["POST /discussions/"] = {}
    return serve(tmp_path, table)


def reply_bodies(calls, disc_id):
    return [json.loads(c["data"])["body"] for c in calls
            if c["method"] == "POST" and disc_id in c["url"]]


# ── GitLab sweep ──


def test_start_thread_confirmed_without_stats_left_open(workdir, api_log, tmp_path):
    listing = [summary_thread(START_DISC, START_BODY)]
    proc = run_post(MR, stdin_text=classified(), api_log=api_log,
                    routes_file=sweep_routes(tmp_path, listing))
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    body = reply_bodies(calls, START_DISC)[0]
    assert "本轮 triage 已启动，结果将回帖于运行汇总处" in body
    assert "TP" not in body  # confirmation type — no statistics (spec Q6)
    assert not [c for c in calls if c["method"] == "PUT"]  # no ✅ end thread → open


def test_end_thread_stats_match_classified_and_resolves(workdir, api_log, tmp_path):
    findings, entries = stats_fixture()
    write_pull(workdir, findings)
    path = write_classified(workdir, entries)
    listing = [summary_thread(END_DISC, END_BODY)]
    proc = run_post(MR, "--classified", str(path), api_log=api_log,
                    routes_file=sweep_routes(tmp_path, listing))
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    body = reply_bodies(calls, END_DISC)[0]
    assert "TP 2 / FP 1 / Edge 1 / OOS 1 / Q 2" in body
    assert "- src/app.py" in body and "- src/util.py" in body
    assert "src/other.py" not in body  # only TP files are 修复涉及文件
    assert f"<!-- triage-anchor: {anchor_of(END_BODY)} -->" in body
    puts = [c for c in calls if c["method"] == "PUT"]
    assert len(puts) == 1 and END_DISC in puts[0]["url"]  # replied, then resolved


def test_fallback_discussion_multi_sub_issues_all_validate_and_post(workdir, api_log, tmp_path):
    """H5: a fallback discussion carries several findings under ONE id with
    distinct bodies (pull's _parse_fallback_issues emits one entry per
    sub-issue, verdict.py records per-body anchors). The by_id index used to
    keep only the LAST sub-issue, so every verdict was checked against that
    body and a legitimate multi-finding fallback was rejected wholesale.
    Each entry must validate against ANY candidate body — and the TP
    修复涉及文件 lookup follows the same anchor→candidate distinction."""
    findings = [finding(1, FALLBACK_DISC, "first sub-issue body", file="src/a.py"),
                finding(2, FALLBACK_DISC, "second sub-issue body", file="src/b.py")]
    write_pull(workdir, findings)
    entries = [
        {"discussion_id": FALLBACK_DISC, "no": 1, "anchor": anchor_of("first sub-issue body"),
         "classification": "TP", "reason": "r1", "fix_plan": "f1", "priority": "high",
         "resolved": True},
        {"discussion_id": FALLBACK_DISC, "no": 2, "anchor": anchor_of("second sub-issue body"),
         "classification": "TP", "reason": "r2", "fix_plan": "f2", "priority": "low",
         "resolved": True},
    ]
    path = write_classified(workdir, entries)
    listing = [summary_thread(END_DISC, END_BODY)]
    proc = run_post(MR, "--classified", str(path), api_log=api_log,
                    routes_file=sweep_routes(tmp_path, listing))
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    assert len(reply_bodies(calls, FALLBACK_DISC)) == 2  # both sub-issue verdicts posted
    body = reply_bodies(calls, END_DISC)[0]
    assert "- src/a.py" in body and "- src/b.py" in body  # each TP's own candidate file


def test_error_thread_escalates_without_resolve_and_fails_run(workdir, api_log, tmp_path):
    listing = [summary_thread(ERR_DISC, ERROR_BODY)]
    proc = run_post(MR, stdin_text=classified(), api_log=api_log,
                    routes_file=sweep_routes(tmp_path, listing))
    assert proc.returncode == 1  # intentional: gate stays red on error rounds
    calls = read_api_log(api_log)
    body = reply_bodies(calls, ERR_DISC)[0]
    assert "本轮 OpenCodeReview 运行异常，未产出裁决" in body
    assert "请人工检查 OCR 运行日志" in body
    assert not [c for c in calls if c["method"] == "PUT"]  # never resolved
    assert "human-in-loop" in proc.stderr


def test_rerun_on_swept_mr_zero_new_replies_end_still_resolves(workdir, api_log, tmp_path):
    marker = f"<!-- triage-anchor: {anchor_of(END_BODY)} -->"
    listing = [marked_summary_thread(END_DISC, END_BODY, marker)]
    proc = run_post(MR, stdin_text=classified(), api_log=api_log,
                    routes_file=sweep_routes(tmp_path, listing))
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    assert not [c for c in calls if c["method"] == "POST"]  # zero new replies
    assert [c for c in calls if c["method"] == "PUT"]       # resolve still executes
    assert "content dedup" in proc.stderr


def test_deduped_error_thread_still_fails_run(workdir, api_log, tmp_path):
    marker = f"<!-- triage-anchor: {anchor_of(ERROR_BODY)} -->"
    listing = [marked_summary_thread(ERR_DISC, ERROR_BODY, marker)]
    proc = run_post(MR, stdin_text=classified(), api_log=api_log,
                    routes_file=sweep_routes(tmp_path, listing))
    assert proc.returncode == 1  # escalation already on the wall, gate stays red
    calls = read_api_log(api_log)
    assert not [c for c in calls if c["method"] == "POST"]
    assert not [c for c in calls if c["method"] == "PUT"]


def test_start_resolves_when_end_thread_completed(workdir, api_log, tmp_path):
    listing = [summary_thread(START_DISC, START_BODY), summary_thread(END_DISC, END_BODY)]
    proc = run_post(MR, stdin_text=classified(), api_log=api_log,
                    routes_file=sweep_routes(tmp_path, listing))
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    puts = [c for c in calls if c["method"] == "PUT"]
    assert len(puts) == 2
    assert any(START_DISC in c["url"] for c in puts)  # the end thread took over
    assert any(END_DISC in c["url"] for c in puts)


def test_resolved_end_thread_still_closes_start(workdir, api_log, tmp_path):
    """H3: run 1 resolved the ✅ end but left 🔍 start open (e.g. the
    classified reply failed). The sweep builders used to discard resolved
    threads — has_end stayed false forever and start could never close. A
    resolved summary thread must ride the listing as closure evidence: never
    re-replied, never re-resolved, but it counts toward has_end."""
    end = summary_thread(END_DISC, END_BODY)
    end["notes"][0]["resolved"] = True
    listing = [summary_thread(START_DISC, START_BODY), end]
    proc = run_post(MR, stdin_text=classified(), api_log=api_log,
                    routes_file=sweep_routes(tmp_path, listing))
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    assert reply_bodies(calls, START_DISC)    # start still gets its confirmation
    assert not reply_bodies(calls, END_DISC)  # completed end never re-replied
    puts = [c for c in calls if c["method"] == "PUT"]
    assert any(START_DISC in c["url"] for c in puts)   # run 2 closes the start
    assert not any(END_DISC in c["url"] for c in puts)


def test_start_stays_open_when_classified_phase_failed(workdir, api_log, tmp_path):
    entries = [{"discussion_id": FINDING_DISC, "no": 1, "anchor": anchor_of(FINDING_BODY),
                "classification": "Edge", "reason": "r", "resolved": True}]
    path = write_classified(workdir, entries)
    listing = [summary_thread(START_DISC, START_BODY), summary_thread(END_DISC, END_BODY)]
    overrides = {f"POST /discussions/{FINDING_DISC}/notes": {"status": 422}}
    proc = run_post(MR, "--classified", str(path), api_log=api_log,
                    routes_file=sweep_routes(tmp_path, listing, overrides))
    assert proc.returncode == 1  # classified reply failed — run not completing
    calls = read_api_log(api_log)
    assert reply_bodies(calls, START_DISC)   # start still gets its confirmation
    assert reply_bodies(calls, END_DISC)
    puts = [c for c in calls if c["method"] == "PUT"]
    assert not any(START_DISC in c["url"] for c in puts)  # start NOT resolved
    assert any(END_DISC in c["url"] for c in puts)        # end resolves regardless


def test_sweep_ignores_fallback_and_regular_finding_threads(workdir, api_log, tmp_path):
    listing = [
        summary_thread(FALLBACK_DISC, FALLBACK_BODY),  # finding carrier → verdicts, not a status reply
        {"id": FINDING_DISC, "notes": [
            {"id": 400, "body": FINDING_BODY, "author": {"username": "human"},
             "resolvable": True, "resolved": False}]},
    ]
    proc = run_post(MR, stdin_text=classified(), api_log=api_log,
                    routes_file=sweep_routes(tmp_path, listing))
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    assert not [c for c in calls if c["method"] == "POST"]
    assert not [c for c in calls if c["method"] == "PUT"]


def test_gitlab_listing_failure_fails_closed(workdir, api_log, tmp_path):
    routes = serve(tmp_path, {"/discussions": {"status": 500}})
    proc = run_post(MR, stdin_text=classified(), api_log=api_log, routes_file=routes)
    assert proc.returncode == 1
    assert "summary sweep" in proc.stderr and "listing failed" in proc.stderr


# ── GitHub sweep: dual-ID-space discipline ──


def gh_summary_thread(node, db_id, body, resolved=False, extra=()):
    comments = [{"databaseId": db_id, "body": body,
                 "author": {"login": "github-actions[bot]"}}]
    comments += [{"databaseId": db, "body": b} for db, b in extra]
    return {"id": node, "isResolved": resolved, "comments": {"nodes": comments}}


def gh_threads_payload(*threads):
    return {"data": {"node": {"reviewThreads": {"nodes": list(threads)}}}}


RESOLVE_OK = {"data": {"resolveReviewThread": {"thread": {"isResolved": True}}}}


def gh_routes(tmp_path, threads=None, *, reply_status=None):
    """Ordered GitHub route table. "/pulls/1" (PR fetch) must come after the
    /comments-ish patterns — reply URLs contain it as a substring."""
    table = {}
    if reply_status is not None:
        table["POST /replies"] = {"status": reply_status}
    table["/replies"] = {"file": "replies.json", "content": []}
    table["/pulls/comments"] = {"file": "parent.json",
                                "content": {"id": GH_END_CMT, "body": "parent body"}}
    table["/comments"] = {"file": "pr_comments.json", "content": []}
    table["/pulls/1"] = {"file": "pr.json",
                         "content": {"number": 1, "node_id": GH_PR_NODE}}
    if threads is not None:
        table["reviewThreads"] = {"file": "threads.json", "content": threads}
    table["resolveReviewThread"] = {"file": "resolve.json", "content": RESOLVE_OK}
    return serve(tmp_path, table)


def test_github_end_thread_rest_reply_then_graphql_resolve(gh_workdir, api_log, tmp_path):
    threads = gh_threads_payload(gh_summary_thread(GH_END_NODE, GH_END_CMT, GH_END_BODY))
    proc = run_post("1", stdin_text=classified(), platform="github", api_log=api_log,
                    routes_file=gh_routes(tmp_path, threads))
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    replies = [c for c in calls if c["method"] == "POST"
               and f"comments/{GH_END_CMT}/replies" in c["url"]]
    assert replies, calls  # REST reply targets the comment databaseId
    body = json.loads(replies[0]["data"])["body"]
    assert "TP 0 / FP 0 / Edge 0 / OOS 0 / Q 0" in body  # empty classified round
    assert "（无）" in body  # no TP fix files
    rest = [c for c in calls if c["method"] != "GRAPHQL"]
    assert not [c for c in rest if GH_END_NODE in c["url"]]  # node id never on a REST path
    muts = [c for c in calls if "resolveReviewThread" in c["url"]]
    assert len(muts) == 1
    assert muts[0]["vars"] == {"threadId": GH_END_NODE}  # GraphQL resolve takes the node id


def test_github_error_thread_reply_only_nonzero_exit(gh_workdir, api_log, tmp_path):
    threads = gh_threads_payload(gh_summary_thread(GH_ERR_NODE, GH_ERR_CMT, GH_ERR_BODY))
    proc = run_post("1", stdin_text=classified(), platform="github", api_log=api_log,
                    routes_file=gh_routes(tmp_path, threads))
    assert proc.returncode == 1
    calls = read_api_log(api_log)
    replies = [c for c in calls if c["method"] == "POST"
               and f"comments/{GH_ERR_CMT}/replies" in c["url"]]
    assert replies
    body = json.loads(replies[0]["data"])["body"]
    assert "本轮 OpenCodeReview 运行异常，未产出裁决" in body
    assert not [c for c in calls if "resolveReviewThread" in c["url"]]


def test_github_start_thread_resolves_after_end(gh_workdir, api_log, tmp_path):
    threads = gh_threads_payload(
        gh_summary_thread(GH_START_NODE, GH_START_CMT, GH_START_BODY),
        gh_summary_thread(GH_END_NODE, GH_END_CMT, GH_END_BODY))
    proc = run_post("1", stdin_text=classified(), platform="github", api_log=api_log,
                    routes_file=gh_routes(tmp_path, threads))
    assert proc.returncode == 0, proc.stderr
    muts = [c for c in read_api_log(api_log) if "resolveReviewThread" in c["url"]]
    assert {c["vars"]["threadId"] for c in muts} == {GH_START_NODE, GH_END_NODE}


def test_github_resolved_end_thread_still_closes_start(gh_workdir, api_log, tmp_path):
    """H3 GitHub side: an already-resolved ✅ end thread is closure evidence —
    the sweep must not re-reply or re-resolve it, but has_end must count it so
    the open start can close on the next run."""
    threads = gh_threads_payload(
        gh_summary_thread(GH_START_NODE, GH_START_CMT, GH_START_BODY),
        gh_summary_thread(GH_END_NODE, GH_END_CMT, GH_END_BODY, resolved=True))
    proc = run_post("1", stdin_text=classified(), platform="github", api_log=api_log,
                    routes_file=gh_routes(tmp_path, threads))
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    replies = [c for c in calls if c["method"] == "POST"]
    assert len(replies) == 1 and f"comments/{GH_START_CMT}/replies" in replies[0]["url"]
    muts = [c for c in calls if "resolveReviewThread" in c["url"]]
    assert len(muts) == 1 and muts[0]["vars"] == {"threadId": GH_START_NODE}


def test_github_sweep_dedup_skips_reply_still_resolves(gh_workdir, api_log, tmp_path):
    anchor = anchor_of(GH_END_BODY)
    threads = gh_threads_payload(gh_summary_thread(
        GH_END_NODE, GH_END_CMT, GH_END_BODY,
        extra=[(8010, f"earlier sweep reply\n\n<!-- triage-anchor: {anchor} -->")]))
    proc = run_post("1", stdin_text=classified(), platform="github", api_log=api_log,
                    routes_file=gh_routes(tmp_path, threads))
    assert proc.returncode == 0, proc.stderr
    calls = read_api_log(api_log)
    assert not [c for c in calls if c["method"] == "POST"]  # dedup: zero new replies
    muts = [c for c in calls if "resolveReviewThread" in c["url"]]
    assert len(muts) == 1 and muts[0]["vars"] == {"threadId": GH_END_NODE}


def test_github_sweep_listing_failure_fails_closed(gh_workdir, api_log, tmp_path):
    routes = gh_routes(tmp_path, threads=None)  # graphql listing unrouteable
    proc = run_post("1", stdin_text=classified(), platform="github", api_log=api_log,
                    routes_file=routes)
    assert proc.returncode == 1
    assert "reviewThreads listing failed" in proc.stderr


def test_github_resolve_not_found_reports_failure_not_silent_success(
        gh_workdir, api_log, tmp_path):
    """#62: a comment whose thread is absent from the GraphQL listing used to
    `return True` — silent success. It must report failure instead."""
    entries = [{"discussion_id": GH_DISC, "no": 1, "anchor": anchor_of(GH_BODY),
                "classification": "Edge", "reason": "r", "resolved": True}]
    path = write_classified(gh_workdir, entries, mr="1")
    threads = gh_threads_payload(  # the listing knows another thread, not ours
        gh_summary_thread("PRRT_otherthread", 9999, "some other finding body"))
    proc = run_post("1", "--mode", "triage", "--classified", str(path), platform="github",
                    api_log=api_log, routes_file=gh_routes(tmp_path, threads))
    # ocr r2 M7: resolve failure counts as failure — non-zero exit, sweep sees incomplete run
    assert proc.returncode != 0, proc.stderr
    assert f"no open review thread contains comment {GH_DISC}" in proc.stderr
    assert "1 failed" in proc.stderr
    assert not [c for c in read_api_log(api_log) if "resolveReviewThread" in c["url"]]


def test_github_resolve_already_resolved_thread_is_idempotent_success(
        gh_workdir, api_log, tmp_path):
    entries = [{"discussion_id": GH_DISC, "no": 1, "anchor": anchor_of(GH_BODY),
                "classification": "Edge", "reason": "r", "resolved": True}]
    path = write_classified(gh_workdir, entries, mr="1")
    threads = gh_threads_payload(
        gh_summary_thread("PRRT_resolved", int(GH_DISC), GH_BODY, resolved=True))
    proc = run_post("1", "--mode", "triage", "--classified", str(path), platform="github",
                    api_log=api_log, routes_file=gh_routes(tmp_path, threads))
    assert proc.returncode == 0, proc.stderr
    assert "resolve failed" not in proc.stderr  # genuinely resolved — not the not-found path
    assert not [c for c in read_api_log(api_log) if "resolveReviewThread" in c["url"]]
