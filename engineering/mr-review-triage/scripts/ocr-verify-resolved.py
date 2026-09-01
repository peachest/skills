"""Verify that every resolvable review thread on an MR/PR is resolved.

This is the **closure gate** for /skill:triage-mr. Post-labels returning "ok"
is NOT sufficient — OCR bot posts summary discussions that the pull script
intentionally filters out, yet they are `resolvable=True` threads on the
platform. A triage run is done only when this script exits 0.

Exit codes:
    0  — every resolvable thread is resolved (MR is closed-for-review)
    1  — one or more resolvable threads remain open (list printed to stderr)

Platform is auto-detected from git remote:
  - github.com    → GitHub PR review threads (GraphQL)
  - anything else → GitLab MR discussions

Usage:
    python3 ocr-verify-resolved.py <MR_OR_PR_ID>
    python3 ocr-verify-resolved.py <MR_OR_PR_ID> --json   # machine-readable

The --json output is an array of unresolved threads:
    [{"discussion_id", "author", "resolvable", "resolved", "body_preview",
      "is_ocr_summary"}]
"""

import json
import sys

from ocr_platform import detect_platform

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


# ── GitLab backend ──


def _unresolved_gitlab(mr_iid):
    """Return unresolved resolvable discussions from a GitLab MR.

    A discussion is resolvable when notes[0].resolvable is true; it is
    unresolved when resolvable and not notes[0].resolved. Pagination follows
    the same scheme as ocr-pull-discussions.py.
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
            if not first.get("resolvable", False):
                continue
            if first.get("resolved", False):
                continue
            note_body = first.get("body", "")
            unresolved.append({
                "discussion_id": disc.get("id", ""),
                "author": first.get("author", {}).get("username", ""),
                "resolvable": True,
                "resolved": False,
                "body_preview": _preview(note_body),
                "is_ocr_summary": _is_ocr_summary(note_body),
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
        })

    return unresolved


# ── Main ──


def _print_human(unresolved):
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
        print(
            f"  • {u['discussion_id'][:12]} ({u['author']}){tag}: {u['body_preview']}",
            file=sys.stderr,
        )
    print(
        "\nOCR summary threads are bot status notices that the pull script "
        "filters out but remain resolvable — reply + resolve them.",
        file=sys.stderr,
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ocr-verify-resolved.py <MR_OR_PR_ID> [--json]", file=sys.stderr)
        sys.exit(2)

    mr_or_pr_id = sys.argv[1]
    as_json = "--json" in sys.argv[2:]

    platform = detect_platform()
    if not as_json:
        print(f"Detected platform: {platform}", file=sys.stderr)

    if platform == "github":
        unresolved = _unresolved_github(mr_or_pr_id)
    else:
        unresolved = _unresolved_gitlab(mr_or_pr_id)

    if unresolved is None:
        # Backend error — treat as not-verified (fail closed).
        sys.exit(1)

    if as_json:
        json.dump(unresolved, sys.stdout, indent=2, ensure_ascii=False)
        print(file=sys.stdout)
    else:
        _print_human(unresolved)

    sys.exit(0 if not unresolved else 1)


if __name__ == "__main__":
    main()
