"""Post classification labels + resolve OCR review discussions.

Reads a JSON array from stdin with classification results and for each:
  1. Posts a reply note with classification label + reason/fix-plan
  2. Resolves the discussion based on classification type (if platform supports)

Platform is auto-detected from git remote:
  - github.com    → GitHub PR review comment replies + GraphQL resolve
  - anything else → GitLab discussion replies + PUT resolve

Classifications:
    ✅ TP  — label "真阳性" + fix plan, NOT resolved (stay open for tracking)
    ❌ FP  — label "假阳性" + reason, resolved
    🟡 Edge — label "边缘" + reason, NOT resolved by default
    🔵 OOS  — label "非本 MR 范围" + reason, resolved
    ⏸️ Q    — label "需讨论" + question, NOT resolved

Input format:
    [
      {
        "discussion_id": "...",
        "classification": "TP|FP|Edge|OOS|Question",
        "reason": "...",
        "fix_plan": "...",         # TP only
        "priority": "high|medium|low",  # TP only
        "resolved": true/false     # override default resolve behavior
      },
      ...
    ]

Usage:
    cat classified.json | python3 ocr-post-labels.py <MR_OR_PR_ID>
"""

import json
import os
import re
import sys

from ocr_platform import detect_platform

# ── Templates (platform-agnostic) ──

_CLASSIFICATION_LABELS = {
    "TP": "✅ 真阳性",
    "FP": "❌ 假阳性",
    "Edge": "🟡 边缘",
    "OOS": "🔵 非本 MR 范围",
    "Question": "⏸️ 需讨论",
}

_PRIORITY_LABELS = {
    "high": "🚨 高",
    "medium": "⚠️ 中",
    "low": "🟢 低",
}

_BODY_TP = """### {label} {priority}

**修复方案**: {fix_plan}
"""

_BODY_SIMPLE = """### {label}

**原因**: {reason}
"""

_BODY_FP = """### ❌ 假阳性

**原因**: {reason}
{adr_row}"""

_BODY_QUESTION = """### ⏸️ 需讨论

{reason}
"""

_DEFAULT_RESOLVED = {
    "TP": False,
    "FP": True,
    "Edge": False,
    "OOS": True,
    "Question": False,
}

_VALID_CLASSIFICATIONS = set(_CLASSIFICATION_LABELS.keys())


# ── Input parsing (platform-agnostic) ──


def _extract_json(raw):
    text = re.sub(r"```(?:json)?\s*", "", raw)
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return None


def _validate_item(item, idx):
    cleaned = dict(item)

    if "classification" not in cleaned and "_cat" in cleaned:
        cleaned["classification"] = cleaned["_cat"]
    if "reason" not in cleaned and "_reason" in cleaned:
        cleaned["reason"] = cleaned["_reason"]
    if "priority" not in cleaned and "_priority" in cleaned:
        pri_map = {"🚨": "high", "⚠️": "medium", "🟢": "low"}
        cleaned["priority"] = pri_map.get(cleaned["_priority"], "medium")

    disc_id = str(cleaned.get("discussion_id", "")).strip()
    if not disc_id:
        return (False, f"item {idx}: missing discussion_id", None)
    if len(disc_id) < 5:
        return (False, f"item {idx}: discussion_id too short ({len(disc_id)} chars)", None)
    cleaned["discussion_id"] = disc_id

    cls = cleaned.get("classification", "FP")
    if cls not in _VALID_CLASSIFICATIONS:
        print(f"  [WARN] item {idx}: unknown classification '{cls}', using 'FP'", file=sys.stderr)
        cls = "FP"
    cleaned["classification"] = cls

    if cls == "TP":
        fix_plan = str(cleaned.get("fix_plan", "")).strip()
        if not fix_plan:
            return (False, f"item {idx}: TP requires fix_plan", None)
        cleaned["fix_plan"] = fix_plan
        priority = cleaned.get("priority", "medium")
        if priority not in _PRIORITY_LABELS:
            priority = "medium"
        cleaned["priority"] = priority
    elif cls == "FP":
        reason = str(cleaned.get("reason", "")).strip()
        if not reason:
            return (False, f"item {idx}: missing reason", None)
        cleaned["reason"] = reason
        adr = str(cleaned.get("adr", "")).strip()
        cleaned["adr"] = adr
    else:
        reason = str(cleaned.get("reason", "")).strip()
        if not reason:
            return (False, f"item {idx}: missing reason", None)
        cleaned["reason"] = reason

    resolved = cleaned.get("resolved")
    if resolved is None:
        resolved = _DEFAULT_RESOLVED.get(cls, False)
    if not isinstance(resolved, bool):
        resolved = _DEFAULT_RESOLVED.get(cls, False)
    cleaned["resolved"] = resolved

    return (True, "", cleaned)


def _build_body(cleaned):
    cls = cleaned["classification"]

    if cls == "TP":
        pri = _PRIORITY_LABELS.get(cleaned["priority"], "⚠️ 中")
        return _BODY_TP.format(
            label=_CLASSIFICATION_LABELS[cls],
            priority=pri,
            fix_plan=cleaned["fix_plan"],
        ).strip()

    if cls == "FP":
        adr_row = ""
        if cleaned.get("adr"):
            adr_row = f"\n**ADR**: {cleaned['adr']}"
        return _BODY_FP.format(
            reason=cleaned["reason"],
            adr_row=adr_row,
        ).strip()

    if cls == "Question":
        return _BODY_QUESTION.format(reason=cleaned["reason"]).strip()

    return _BODY_SIMPLE.format(
        label=_CLASSIFICATION_LABELS[cls],
        reason=cleaned["reason"],
    ).strip()


# ── GitLab backend ──


def _post_gitlab(mr_iid, items):
    from ocr_gitlab import curl, get_project_id

    project_id = get_project_id()
    if not project_id:
        print("ERROR: could not determine GitLab project ID", file=sys.stderr)
        return False

    base = f"/projects/{project_id}/merge_requests/{mr_iid}"
    ok = fail = skip = 0

    for idx, item in enumerate(items):
        valid, err, cleaned = _validate_item(item, idx)
        if not valid:
            print(f"[SKIP] {err}", file=sys.stderr)
            skip += 1
            continue

        disc_id = cleaned["discussion_id"]
        cls = cleaned["classification"]
        do_resolve = cleaned["resolved"]
        body = _build_body(cleaned)

        # 1) Post reply
        status, resp, _ = curl(
            f"{base}/discussions/{disc_id}/notes",
            method="POST",
            data={"body": body},
        )
        if not (200 <= status < 300):
            print(f"[FAIL] reply {disc_id[:12]}: HTTP {status}", file=sys.stderr)
            fail += 1
            continue

        # 2) Resolve
        if do_resolve:
            status, _, _ = curl(
                f"{base}/discussions/{disc_id}",
                method="PUT",
                data={"resolved": True},
            )
            if 200 <= status < 300:
                ok += 1
                label = _CLASSIFICATION_LABELS.get(cls, cls)
                print(f"[OK] {label} resolved {disc_id[:12]}", file=sys.stderr)
            else:
                print(f"[WARN] reply ok but resolve failed for {disc_id[:12]}: HTTP {status}", file=sys.stderr)
                fail += 1
        else:
            ok += 1
            label = _CLASSIFICATION_LABELS.get(cls, cls)
            print(f"[OK] {label} labeled {disc_id[:12]} (open)", file=sys.stderr)

    total = ok + fail
    print(f"Done: {ok} ok, {fail} failed, {skip} skipped ({total}/{len(items)} processed)", file=sys.stderr)
    return fail == 0


# ── GitHub backend ──


def _resolve_github_thread(pr_number, comment_id):
    """Resolve a GitHub PR review thread via GraphQL.

    GitHub's REST API doesn't support resolving review threads. We need to:
    1. Get the PR's node_id
    2. Query review threads to find the thread containing our comment
    3. Call resolveReviewThread mutation

    Returns True if resolved (or already resolved), False on failure.
    """
    from ocr_github import curl, graphql, get_project_id

    owner_repo = get_project_id()
    if not owner_repo:
        return False
    owner, repo = owner_repo.split("/", 1)

    # 1. Get PR node_id
    status, pr_body, _ = curl(f"/repos/{owner}/{repo}/pulls/{pr_number}")
    if status == 0 or not isinstance(pr_body, dict):
        return False
    pr_node_id = pr_body.get("node_id")
    if not pr_node_id:
        return False

    # 2. Query review threads to find the one containing our comment
    #    comment_id is the databaseId; we match against comments[].databaseId
    try:
        comment_id_int = int(comment_id)
    except (ValueError, TypeError):
        return False

    query = """
    query($pr: ID!) {
      node(id: $pr) {
        ... on PullRequest {
          reviewThreads(first: 100) {
            nodes {
              id
              isResolved
              comments(first: 5) {
                nodes { databaseId }
              }
            }
          }
        }
      }
    }
    """
    status, result, _ = graphql(query, {"pr": pr_node_id})
    if status == 0 or not result or "data" not in result:
        return False

    threads = (
        result.get("data", {})
        .get("node", {})
        .get("reviewThreads", {})
        .get("nodes", [])
    )

    thread_node_id = None
    for thread in threads:
        if thread.get("isResolved"):
            continue
        comment_ids = [c.get("databaseId") for c in thread.get("comments", {}).get("nodes", [])]
        if comment_id_int in comment_ids:
            thread_node_id = thread.get("id")
            break

    if not thread_node_id:
        # Thread not found or already resolved
        return True  # treat as success (already resolved)

    # 3. Resolve the thread
    mutation = """
    mutation($threadId: ID!) {
      resolveReviewThread(input: {threadId: $threadId}) {
        thread { isResolved }
      }
    }
    """
    status, result, _ = graphql(mutation, {"threadId": thread_node_id})
    if status == 0 or not result or "errors" in result:
        return False

    return (
        result.get("data", {})
        .get("resolveReviewThread", {})
        .get("thread", {})
        .get("isResolved", False)
    )


def _post_github(pr_number, items):
    from ocr_github import curl, get_project_id

    owner_repo = get_project_id()
    if not owner_repo:
        print("ERROR: could not determine GitHub owner/repo", file=sys.stderr)
        return False

    ok = fail = skip = 0

    for idx, item in enumerate(items):
        valid, err, cleaned = _validate_item(item, idx)
        if not valid:
            print(f"[SKIP] {err}", file=sys.stderr)
            skip += 1
            continue

        comment_id = cleaned["discussion_id"]
        cls = cleaned["classification"]
        do_resolve = cleaned["resolved"]
        body = _build_body(cleaned)

        # 1) Post reply to the review comment thread
        endpoint = f"/repos/{owner_repo}/pulls/{pr_number}/comments/{comment_id}/replies"
        status, resp, _ = curl(endpoint, method="POST", data={"body": body})
        if not (200 <= status < 300):
            # Fallback: post as a regular PR comment
            status2, _, _ = curl(
                f"/repos/{owner_repo}/issues/{pr_number}/comments",
                method="POST",
                data={"body": body},
            )
            if not (200 <= status2 < 300):
                print(f"[FAIL] reply {comment_id}: HTTP {status}, fallback HTTP {status2}", file=sys.stderr)
                fail += 1
                continue

        # 2) Resolve thread (if requested)
        if do_resolve:
            resolved = _resolve_github_thread(pr_number, comment_id)
            if resolved:
                ok += 1
                label = _CLASSIFICATION_LABELS.get(cls, cls)
                print(f"[OK] {label} resolved {comment_id[:12]}", file=sys.stderr)
            else:
                print(f"[WARN] reply ok but resolve failed for {comment_id[:12]}", file=sys.stderr)
                ok += 1  # reply succeeded, just couldn't resolve
        else:
            ok += 1
            label = _CLASSIFICATION_LABELS.get(cls, cls)
            print(f"[OK] {label} labeled {comment_id[:12]} (open)", file=sys.stderr)

    total = ok + fail
    print(f"Done: {ok} ok, {fail} failed, {skip} skipped ({total}/{len(items)} processed)", file=sys.stderr)
    return fail == 0


# ── Main ──


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ocr-post-labels.py <MR_OR_PR_ID>  <  classified.json", file=sys.stderr)
        sys.exit(1)

    mr_or_pr_id = sys.argv[1]
    raw = sys.stdin.read()

    items = _extract_json(raw)
    if items is None:
        print("ERROR: no valid JSON array found in input", file=sys.stderr)
        sys.exit(1)
    if not isinstance(items, list):
        print("ERROR: expected JSON array, got " + type(items).__name__, file=sys.stderr)
        sys.exit(1)

    platform = detect_platform()
    print(f"Detected platform: {platform}", file=sys.stderr)

    if platform == "github":
        success = _post_github(mr_or_pr_id, items)
    else:
        success = _post_gitlab(mr_or_pr_id, items)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
