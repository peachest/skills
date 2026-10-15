"""Verify that every resolvable review thread on an MR/PR is resolved.

This is the **closure gate** for /skill:triage-mr. Post-labels returning "ok"
is NOT sufficient — OCR bot posts summary discussions that the pull script
intentionally filters out, yet they are `resolvable=True` threads on the
platform. A triage run is done only when this script exits 0.

Human output never shows platform ids — full or truncated (spec #57 display
discipline; the old `discussion_id[:12]` form caused the P-005 truncation
family). Each thread is labeled with its pull-file ordinal (`no=<N>`, mapped
from the pull state file via --pull-file, default
.triage/<MR>/issues.json) or, when the thread is not in the pull file (OCR
summary threads, no pull run), a short content anchor
(`anchor=<sha256(first note body)[:8]>`). The per-thread
`[N/M notes open]` annotation is load-bearing and kept.

Timing gate (spec #57 Amendment R2 修订 B): head-CI status (GitLab
head_pipeline / GitHub check runs) is queried first; while it is in flight
the script exits 2 — pass --skip-pipeline-check to override. No CI on the
head ref: stderr note and the normal thread check proceeds.

Exit codes:
    0  — every resolvable thread is resolved (MR is closed-for-review)
    1  — one or more resolvable threads remain open (list printed to stderr),
         or a backend error (fail closed)
    2  — CI pipeline/check runs still in flight (--skip-pipeline-check
         overrides), or usage error

Platform is auto-detected from git remote:
  - github.com    → GitHub PR review threads (GraphQL)
  - anything else → GitLab MR discussions

Usage:
    python3 ocr-verify-resolved.py <MR_OR_PR_ID>
    python3 ocr-verify-resolved.py <MR_OR_PR_ID> [--pull-file <path>] \
        [--skip-pipeline-check]
    python3 ocr-verify-resolved.py <MR_OR_PR_ID> --json   # machine-readable

The --json output is an array of unresolved threads:
    [{"discussion_id", "author", "resolvable", "resolved", "body_preview",
      "is_ocr_summary"}]

--json keeps the full platform ids — script chains rely on them; the
ordinal/anchor display discipline applies to human output only.
"""

import hashlib
import json
import os
import sys

from ocr_platform import (detect_platform, run_auth_probe, run_pipeline_gate,
                          triage_state_dir)

# Documented --json contract; internal fields (_body) are projected away so
# script chains see exactly the shape they always saw.
_JSON_FIELDS = ("discussion_id", "author", "resolvable", "resolved",
                "body_preview", "is_ocr_summary")

# A discussion counts as an "OCR summary" (bot status notice, not an inline
# finding) when its first note body starts with the OCR run-report emoji.
# These are the threads that slip past ocr-pull-discussions.py's filter yet
# remain resolvable — the common cause of a false "done".
_OCR_SUMMARY_PREFIXES = ("🔍", "✅ OpenCodeReview", "⚠️ OpenCodeReview")


def _is_ocr_summary(body):
    body = (body or "").strip()
    return any(body.startswith(p) for p in _OCR_SUMMARY_PREFIXES)


def _preview(body, limit=160):
    body = (body or "").strip().replace("\n", " ")
    return body[:limit] + ("…" if len(body) > limit else "")


def _open_note_count(resolvable_notes):
    """Suffix for the human output: open resolvable notes when the thread
    has more than one — flags the resolved-head-but-open-reply trap."""
    open_n = sum(1 for n in resolvable_notes if not n.get("resolved", False))
    if not open_n or len(resolvable_notes) < 2:
        return ""
    return f" [{open_n}/{len(resolvable_notes)} notes open]"


# ── GitLab backend ──


def _unresolved_gitlab(mr_iid):
    """Return unresolved resolvable discussions from a GitLab MR.

    GitLab semantics: every note in a discussion carries its own resolvable/
    resolved flags, and the thread counts as closed only when ALL resolvable
    notes are resolved. Reply notes posted during the triage run (verdict
    labels) are resolvable too — checking only notes[0] yields a false
    gate=0 while reply notes hang open. Pagination follows the same scheme
    as ocr-pull-discussions.py.
    """
    from ocr_gitlab import curl, get_project_id

    project_id = get_project_id()
    if not project_id:
        print("ERROR: could not determine GitLab project ID", file=sys.stderr)
        return None

    unresolved = []
    for page in range(1, 6):
        endpoint = (
            f"/projects/{project_id}/merge_requests/{mr_iid}"
            f"/discussions?per_page=100&page={page}"
        )
        status, body, _ = curl(endpoint)
        if status == 0 or not isinstance(body, list) or not body:
            if page == 1 and status != 200:
                print(
                    f"WARN: discussions fetch HTTP {status} — check glab auth",
                    file=sys.stderr,
                )
            break

        for disc in body:
            notes = disc.get("notes", [])
            if not notes:
                continue
            first = notes[0]
            resolvable_notes = [n for n in notes if n.get("resolvable", False)]
            if not resolvable_notes:
                continue
            if not any(n.get("resolved", False) is False for n in resolvable_notes):
                continue
            note_body = first.get("body", "")
            unresolved.append({
                "discussion_id": disc.get("id", ""),
                "author": first.get("author", {}).get("username", ""),
                "resolvable": True,
                "resolved": False,
                "body_preview": _preview(note_body) + _open_note_count(resolvable_notes),
                "is_ocr_summary": _is_ocr_summary(note_body),
                "_body": note_body,  # display-only; projected out of --json
            })

        if len(body) < 100:
            break

    return unresolved


# ── GitHub backend ──


def _unresolved_github(pr_number):
    """Return unresolved review threads from a GitHub PR via GraphQL."""
    from ocr_github import curl, graphql, get_project_id

    owner_repo = get_project_id()
    if not owner_repo:
        print("ERROR: could not determine GitHub owner/repo", file=sys.stderr)
        return None
    owner, repo = owner_repo.split("/", 1)

    status, pr_body, _ = curl(f"/repos/{owner}/{repo}/pulls/{pr_number}")
    if status == 0 or not isinstance(pr_body, dict):
        print(f"ERROR: could not fetch PR #{pr_number} (HTTP {status})", file=sys.stderr)
        return None
    pr_node_id = pr_body.get("node_id")
    if not pr_node_id:
        print("ERROR: PR has no node_id; cannot query review threads", file=sys.stderr)
        return None

    query = """
    query($pr: ID!) {
      node(id: $pr) {
        ... on PullRequest {
          reviewThreads(first: 100) {
            nodes {
              id
              isResolved
              comments(first: 1) { nodes { body databaseId author { login } } }
            }
          }
        }
      }
    }
    """
    status, result, _ = graphql(query, {"pr": pr_node_id})
    if status == 0 or not result or "data" not in result:
        print("ERROR: GraphQL reviewThreads query failed", file=sys.stderr)
        return None

    threads = (
        result.get("data", {})
        .get("node", {})
        .get("reviewThreads", {})
        .get("nodes", [])
    )

    unresolved = []
    for thread in threads:
        if thread.get("isResolved"):
            continue
        comments = thread.get("comments", {}).get("nodes", [])
        first = comments[0] if comments else {}
        note_body = first.get("body", "")
        unresolved.append({
            "discussion_id": thread.get("id", ""),
            "author": (first.get("author") or {}).get("login", ""),
            "resolvable": True,
            "resolved": False,
            "body_preview": _preview(note_body),
            "is_ocr_summary": _is_ocr_summary(note_body),
            "_body": note_body,  # display-only; projected out of --json
        })

    return unresolved


# ── Main ──


def _load_no_map(pull_file, explicit):
    """Map discussion_id → pull-file ordinal for the human thread labels.

    Missing file → {} (verify stays meaningful without a pull run); an
    explicitly requested missing file gets a note (typo guard); corrupt
    content → WARN and {} — display-only degradation, never blocks the gate.
    """
    if not pull_file or not os.path.exists(pull_file):
        if explicit:
            print(f"note: --pull-file not found: {pull_file} — threads "
                  f"labeled with content anchors", file=sys.stderr)
        return {}
    try:
        with open(pull_file, encoding="utf-8") as fh:
            findings = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"WARN: pull state file {pull_file} unreadable ({exc}) — "
              f"threads labeled with content anchors", file=sys.stderr)
        return {}
    if not isinstance(findings, list):
        print(f"WARN: pull state file {pull_file} is not a findings array — "
              f"threads labeled with content anchors", file=sys.stderr)
        return {}
    return {f["discussion_id"]: f["no"] for f in findings
            if isinstance(f, dict) and isinstance(f.get("discussion_id"), str)
            and isinstance(f.get("no"), int)}


def _thread_label(discussion_id, body, no_map):
    """Human-output thread handle: pull-file ordinal when mapped, else a
    short content anchor — never a platform-id shape (full or truncated)."""
    no = no_map.get(discussion_id)
    if no is not None:
        return f"no={no}"
    return "anchor=" + hashlib.sha256((body or "").encode("utf-8")).hexdigest()[:8]


def _print_human(unresolved, no_map=None):
    no_map = no_map or {}
    if not unresolved:
        print("✅ All resolvable review threads resolved (0 open).", file=sys.stderr)
        return

    ocr_count = sum(1 for u in unresolved if u["is_ocr_summary"])
    print(
        f"❌ {len(unresolved)} resolvable thread(s) still open"
        + (f" ({ocr_count} OCR summary)" if ocr_count else "")
        + " — triage NOT complete.",
        file=sys.stderr,
    )
    for u in unresolved:
        tag = " [OCR summary]" if u["is_ocr_summary"] else ""
        label = _thread_label(u["discussion_id"], u.get("_body", ""), no_map)
        print(
            f"  • {label} ({u['author']}){tag}: {u['body_preview']}",
            file=sys.stderr,
        )
    print(
        "\nOCR summary threads are bot status notices that the pull script "
        "filters out but remain resolvable — reply + resolve them.",
        file=sys.stderr,
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ocr-verify-resolved.py <MR_OR_PR_ID> [--json] "
              "[--pull-file <path>] [--skip-pipeline-check]", file=sys.stderr)
        sys.exit(2)

    mr_or_pr_id = sys.argv[1]
    rest = sys.argv[2:]
    as_json = "--json" in rest
    skip_pipeline = "--skip-pipeline-check" in rest
    explicit_pull_file = "--pull-file" in rest
    pull_file = None
    if explicit_pull_file:
        i = rest.index("--pull-file")
        if i + 1 >= len(rest):
            print("ERROR: --pull-file requires a file path argument", file=sys.stderr)
            sys.exit(2)
        pull_file = rest[i + 1]

    platform = detect_platform()
    if not as_json:
        print(f"Detected platform: {platform}", file=sys.stderr)

    run_auth_probe(platform)
    run_pipeline_gate(platform, mr_or_pr_id, skip=skip_pipeline)

    if platform == "github":
        unresolved = _unresolved_github(mr_or_pr_id)
    else:
        unresolved = _unresolved_gitlab(mr_or_pr_id)

    if unresolved is None:
        # Backend error — treat as not-verified (fail closed).
        sys.exit(1)

    if as_json:
        projected = [{k: u[k] for k in _JSON_FIELDS} for u in unresolved]
        json.dump(projected, sys.stdout, indent=2, ensure_ascii=False)
        print(file=sys.stdout)
    else:
        pull_file = pull_file or os.path.join(
            triage_state_dir(mr_or_pr_id), "issues.json")
        _print_human(unresolved, _load_no_map(pull_file, explicit_pull_file))

    sys.exit(0 if not unresolved else 1)


if __name__ == "__main__":
    main()
