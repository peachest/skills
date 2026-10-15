"""Post classification labels + resolve OCR review discussions.

Reads a schema 2 classified state file (--classified <path>, or stdin as a
bare transport — validation is identical for both) and for each entry:
  1. Posts a reply note with classification label + reason/fix-plan
  2. Resolves the discussion based on classification type (if platform supports)

Platform is auto-detected from git remote:
  - github.com    → GitHub PR review comment replies + GraphQL resolve
  - anything else → GitLab discussion replies + PUT resolve

Classifications (default mode — standalone /fix use):
    ✅ TP  — label "真阳性" + fix plan, NOT resolved (stay open for tracking)
    ❌ FP  — label "假阳性" + reason, resolved
    🟡 Edge — label "边缘" + reason, NOT resolved by default
    🔵 OOS  — label "非本 MR 范围" + reason, resolved
    ⏸️ Q    — label "需讨论" + question, NOT resolved

Classification vocabulary is pinned: state files store the Question verdict
as `Q`; both `Q` and `Question` are accepted and normalized to `Question`
(the canonical key in the label/resolved maps) before any lookup. Unknown or
missing classification values hard-fail the whole run before any platform
call — no silent FP downgrade.

In triage mode (--mode triage), a TP has already been fixed and build-verified
by the time it reaches post-labels, so it is resolved like FP/OOS. The
"stay open for tracking" default serves standalone /fix runs where the fix
may not have landed yet; in /skill:triage-mr the fix is part of the same run.
Edge and Question stay open in both modes (genuinely unresolved).

Input format (schema 2 — versionless or schema-1 files are rejected loudly
with the filename, the missing-field list, and a rebuild hint):
    {
      "schema": 2,
      "entries": [
        {
          "discussion_id": "...",
          "classification": "TP|FP|Edge|OOS|Q",
          "reason": "...",
          "fix_plan": "...",              # TP only
          "priority": "high|medium|low",  # TP only, string enum
          "resolved": true/false          # override default resolve behavior
        },
        ...
      ]
    }

Usage:
    python3 ocr-post-labels.py <MR_OR_PR_ID> --classified .triage/<MR>/classified.json
    cat classified.json | python3 ocr-post-labels.py <MR_OR_PR_ID>
    python3 ocr-post-labels.py <MR_OR_PR_ID> --mode triage --classified .triage/<MR>/classified.json
"""

import json
import os
import re
import sys

from ocr_platform import detect_platform, run_auth_probe

# ── Templates (platform-agnostic) ──

_SCHEMA_VERSION = 2

# State files store the Question verdict as `Q`; the maps below are keyed by
# the canonical `Question`, so normalize aliases BEFORE any lookup.
_CLASSIFICATION_ALIASES = {"Q": "Question"}

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

# Per-classification default resolved state.
# `triage` mode (used by /skill:triage-mr): TP is fixed+verified in-run, so it
# resolves. `default` mode (standalone /fix): TP stays open for tracking.
_DEFAULT_RESOLVED = {
    "TP": False,
    "FP": True,
    "Edge": False,
    "OOS": True,
    "Question": False,
}

_TRIAGE_RESOLVED = {
    "TP": True,
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


def _parse_state_entries(raw, filename):
    """Parse a schema 2 state payload; hard-fail on versionless/schema-1 input.

    Both transports (--classified <path> and stdin) go through this same
    validation. The error carries the filename, the missing/invalid field
    list, and a one-line rebuild hint, then exits non-zero before any
    platform call.
    """
    data = _extract_json(raw)
    if data is None:
        print(f"ERROR: {filename}: no valid JSON found in state input", file=sys.stderr)
        sys.exit(1)

    if isinstance(data, dict):
        problems = []
        if "schema" not in data:
            problems.append("schema")
        elif data["schema"] != _SCHEMA_VERSION:
            problems.append(f"schema={data['schema']!r} (expected {_SCHEMA_VERSION})")
        if not isinstance(data.get("entries"), list):
            problems.append("entries")
        got = ""
    else:
        problems = ["schema", "entries"]
        got = f" (got bare {type(data).__name__})"

    if problems:
        print(
            f"ERROR: {filename}: schema {_SCHEMA_VERSION} state file required — "
            f"missing/invalid field(s): {', '.join(problems)}{got}. "
            f"Rebuild: re-emit as {{\"schema\": {_SCHEMA_VERSION}, \"entries\": [...]}} — older formats are no longer accepted",
            file=sys.stderr,
        )
        sys.exit(1)
    return data["entries"]


def _preflight(entries, filename):
    """Pin the classification vocabulary before any platform call.

    Normalizes `Q` → `Question` (canonical key of the label/resolved maps —
    a legal Q must not KeyError in _build_body), and hard-fails the whole run
    on unknown or missing classification values (no silent FP downgrade) and
    on TP priorities outside the high|medium|low string enum.
    """
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            print(f"ERROR: {filename}: entry {i}: not a JSON object", file=sys.stderr)
            sys.exit(1)
        raw_cls = entry.get("classification")
        cls = _CLASSIFICATION_ALIASES.get(raw_cls, raw_cls)
        if cls not in _VALID_CLASSIFICATIONS:
            kind = "missing classification" if raw_cls is None else f"unknown classification {raw_cls!r}"
            print(
                f"ERROR: {filename}: entry {i}: {kind} (valid: TP|FP|Edge|OOS|Q/Question) — no platform calls made",
                file=sys.stderr,
            )
            sys.exit(1)
        entry["classification"] = cls
        if cls == "TP":
            # ocr r1 F3: omitted priority defaults to medium in _validate_item;
            # a *supplied* priority must be a valid enum string — explicit null
            # and non-string values (incl. collections, which raise TypeError
            # at an `in` check) hard-fail here, before any platform call.
            if "priority" in entry:
                priority = entry["priority"]
                if not isinstance(priority, str) or priority not in _PRIORITY_LABELS:
                    print(
                        f"ERROR: {filename}: entry {i}: priority must be one of high|medium|low, got {priority!r}",
                        file=sys.stderr,
                    )
                    sys.exit(1)
    return entries


def _validate_item(item, idx, resolved_map=None):
    resolved_map = resolved_map or _DEFAULT_RESOLVED
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
        resolved = resolved_map.get(cls, False)
    if not isinstance(resolved, bool):
        resolved = resolved_map.get(cls, False)
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


def _sweep_notes_gitlab(base, disc_id, curl):
    """Resolve every remaining resolvable-unresolved note in a thread.

    GitLab threads carry per-note resolvable/resolved flags, and the
    discussion-level PUT only resolves the thread head — reply notes
    (including the verdict label just posted) stay open and trip the closure
    gate. Called after a successful thread resolve so the script leaves
    nothing for a manual fallback.

    Returns True iff every resolvable note is resolved after this pass —
    also serves as the fallback resolve path for instances where the
    discussion-level PUT fails structurally (e.g. <git-host> returns 500 on it).
    """
    status, disc, _ = curl(f"{base}/discussions/{disc_id}")
    if status != 200 or not isinstance(disc, dict):
        print(f"[WARN] note sweep {disc_id[:12]}: fetch HTTP {status} — notes untouched", file=sys.stderr)
        return False
    swept = remaining = 0
    for note in disc.get("notes", []):
        if note.get("resolvable") and not note.get("resolved"):
            note_id = note.get("id")
            st, _, _ = curl(
                f"{base}/discussions/{disc_id}/notes/{note_id}",
                method="PUT",
                data={"resolved": True},
            )
            if 200 <= st < 300:
                swept += 1
            else:
                remaining += 1
                print(f"[WARN] note sweep {disc_id[:12]}/{note_id}: HTTP {st}", file=sys.stderr)
    if swept:
        print(f"[OK] swept {swept} open reply note(s) in {disc_id[:12]}", file=sys.stderr)
    return remaining == 0


def _post_gitlab(mr_iid, items, resolved_map=None):
    from ocr_gitlab import curl, get_project_id

    resolved_map = resolved_map or _DEFAULT_RESOLVED
    project_id = get_project_id()
    if not project_id:
        print("ERROR: could not determine GitLab project ID", file=sys.stderr)
        return False

    base = f"/projects/{project_id}/merge_requests/{mr_iid}"
    ok = fail = skip = 0

    for idx, item in enumerate(items):
        valid, err, cleaned = _validate_item(item, idx, resolved_map)
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
        reply_ok = 200 <= status < 300
        if not reply_ok:
            print(f"[WARN] reply {disc_id[:12]}: HTTP {status} — trying resolve anyway", file=sys.stderr)

        # 2) Resolve
        if do_resolve:
            status, _, _ = curl(
                f"{base}/discussions/{disc_id}",
                method="PUT",
                data={"resolved": True},
            )
            if 200 <= status < 300:
                _sweep_notes_gitlab(base, disc_id, curl)
                ok += 1
                label = _CLASSIFICATION_LABELS.get(cls, cls)
                print(f"[OK] {label} resolved {disc_id[:12]}" + ("" if reply_ok else " (reply failed)"), file=sys.stderr)
            elif _sweep_notes_gitlab(base, disc_id, curl):
                # discussion-level PUT failed structurally (e.g. <git-host> 500s)
                # — note-level PUT is the working resolve path there
                ok += 1
                label = _CLASSIFICATION_LABELS.get(cls, cls)
                print(f"[OK] {label} resolved {disc_id[:12]} via note-level fallback" + ("" if reply_ok else " (reply failed)"), file=sys.stderr)
            else:
                print(f"[FAIL] resolve {disc_id[:12]}: HTTP {status}" + ("" if reply_ok else " (reply also failed)"), file=sys.stderr)
                fail += 1
        elif reply_ok:
            ok += 1
            label = _CLASSIFICATION_LABELS.get(cls, cls)
            print(f"[OK] {label} labeled {disc_id[:12]} (open)", file=sys.stderr)
        else:
            fail += 1
            print(f"[FAIL] {disc_id[:12]}: both reply and resolve skipped", file=sys.stderr)

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


def _post_github(pr_number, items, resolved_map=None):
    from ocr_github import curl, get_project_id

    resolved_map = resolved_map or _DEFAULT_RESOLVED
    owner_repo = get_project_id()
    if not owner_repo:
        print("ERROR: could not determine GitHub owner/repo", file=sys.stderr)
        return False

    ok = fail = skip = 0

    for idx, item in enumerate(items):
        valid, err, cleaned = _validate_item(item, idx, resolved_map)
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


def _parse_args(argv):
    """Return (mr_or_pr_id, mode, classified_path) from the CLI tail."""
    if not argv or argv[0].startswith("-"):
        return None, None, None
    mr_or_pr_id = argv[0]
    mode = "default"
    classified_path = None
    rest = argv[1:]
    i = 0
    while i < len(rest):
        arg = rest[i]
        if arg == "--mode" and i + 1 < len(rest):
            mode = rest[i + 1]
            i += 2
        elif arg == "--classified" and i + 1 < len(rest):
            classified_path = rest[i + 1]
            i += 2
        elif arg in ("--mode", "--classified"):
            print(f"ERROR: {arg} requires a value", file=sys.stderr)
            sys.exit(1)
        else:
            i += 1
    return mr_or_pr_id, mode, classified_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ocr-post-labels.py <MR_OR_PR_ID> [--mode triage] [--classified <path>]  [< state.json]", file=sys.stderr)
        sys.exit(1)

    mr_or_pr_id, mode, classified_path = _parse_args(sys.argv[1:])
    if mr_or_pr_id is None:
        print("Usage: python3 ocr-post-labels.py <MR_OR_PR_ID> [--mode triage] [--classified <path>]  [< state.json]", file=sys.stderr)
        sys.exit(1)

    if classified_path is not None:
        filename = classified_path
        try:
            with open(classified_path, encoding="utf-8") as fh:
                raw = fh.read()
        except OSError as exc:
            print(f"ERROR: cannot read --classified {classified_path}: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        # stdin is a transport only — the same schema 2 validation applies
        filename = "<stdin>"
        raw = sys.stdin.read()

    entries = _preflight(_parse_state_entries(raw, filename), filename)
    resolved_map = _TRIAGE_RESOLVED if mode == "triage" else _DEFAULT_RESOLVED

    platform = detect_platform()
    print(f"Detected platform: {platform}", file=sys.stderr)

    run_auth_probe(platform)

    if platform == "github":
        success = _post_github(mr_or_pr_id, entries, resolved_map)
    else:
        success = _post_gitlab(mr_or_pr_id, entries, resolved_map)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
