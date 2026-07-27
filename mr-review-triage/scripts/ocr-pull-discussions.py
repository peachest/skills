"""Pull all OCR review issues from a GitLab MR or GitHub PR.

Outputs deduplicated review issues as JSON to stdout.
Progress messages go to stderr — do NOT redirect stderr into stdout (no 2>&1).

    python3 <SKILL_DIR>/scripts/ocr-pull-discussions.py <MR_OR_PR_ID> > /tmp/issues.json

Platform is auto-detected from git remote:
  - github.com        → GitHub PR review comments
  - anything else     → GitLab MR discussions

Project/repo resolved automatically from env or git remote.
"""

import json
import os
import re
import subprocess
import sys

from ocr_platform import detect_platform

# ── Junk filters (platform-agnostic) ──

_JUNK_BODIES = {
    "changed this line", "changed the description", "nouse",
    "test discussion", "line-ending test", "test discc", "header test",
    "Test discussion", "inline test L57", "inline test ocr-review.yml L30",
}

_JUNK_PREFIXES = {
    "changed this line", "**PR Description**", "**[Persistent review]",
    "## PR Reviewer", "Added 1 commit",
}


def _is_review_content(body):
    """Check if a body looks like an OCR review issue (not summary/junk)."""
    body_stripped = body.strip()
    if body_stripped in _JUNK_BODIES:
        return False
    if any(body_stripped.startswith(p) for p in _JUNK_PREFIXES):
        return False
    # Exclude summary / fallback / LGTM / error notes
    # (fallback notes are handled separately by _is_fallback_*)
    if body_stripped.startswith("🔍 OpenCodeReview — issues"):
        return False  # fallback note — handled separately
    if body_stripped.startswith("🔍"):
        return False  # summary
    if body_stripped.startswith("✅"):
        return False  # LGTM
    if body_stripped.startswith("⚠️"):
        return False  # error
    return True


# ── Fallback note parsing (platform-agnostic format) ──

_FALLBACK_SEP = re.compile(r"\n---\n")
_FALLBACK_HEADER = re.compile(r"### `([^`]+)`")
_FALLBACK_LINE = re.compile(r"L(\d+)")


def _parse_fallback_issues(discussion_id, body):
    """Extract sub-issues from a fallback note body.

    The fallback note format is the same on both platforms:

        🔍 OpenCodeReview — issues that could not be posted inline:

        ---

        ### `path/to/file.go` (L1-L1)

        text

        ---

    Args:
        discussion_id: The discussion/comment ID to assign to each sub-issue.
        body: The fallback note body text.

    Returns:
        list[dict]: {discussion_id, file, line, body}
    """
    issues = []
    blocks = _FALLBACK_SEP.split(body)[1:]
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        header_match = _FALLBACK_HEADER.search(block)
        if not header_match:
            continue
        filepath = header_match.group(1)
        line_match = _FALLBACK_LINE.search(block)
        line = int(line_match.group(1)) if line_match else 0
        header_end = header_match.end()
        desc = block[header_end:].strip()
        if desc.startswith("("):
            paren_end = desc.find(")")
            desc = desc[paren_end + 1:].strip()
        issues.append({
            "discussion_id": discussion_id,
            "file": filepath,
            "line": line,
            "body": desc,
        })
    return issues


def _is_fallback_body(body):
    """Check if a body is an OCR fallback note."""
    return body.strip().startswith("🔍 OpenCodeReview — issues")


# ── GitLab backend ──


def _pull_gitlab(mr_iid, skip_resolved=True):
    """Fetch OCR review issues from a GitLab MR."""
    from ocr_gitlab import curl, get_project_id

    project_id = get_project_id()
    if not project_id:
        print("ERROR: could not determine GitLab project ID", file=sys.stderr)
        return []

    all_issues = []
    max_pages = 5

    for page in range(1, max_pages + 1):
        endpoint = f"/projects/{project_id}/merge_requests/{mr_iid}/discussions?per_page=100&page={page}"
        status, body, _ = curl(endpoint)
        if status == 0 or not isinstance(body, list) or not body:
            break

        for disc in body:
            notes = disc.get("notes", [])
            if not notes:
                continue
            first_note = notes[0]

            # Skip resolved discussions by default
            if skip_resolved and first_note.get("resolved", False):
                continue

            # Only process bot notes
            author = first_note.get("author", {}).get("username", "")
            if author != "gitblue.bot":
                continue

            pos = first_note.get("position")
            note_body = first_note.get("body", "")

            if pos:
                # Inline issue
                if _is_review_content(note_body):
                    all_issues.append({
                        "discussion_id": disc["id"],
                        "file": pos.get("new_path", ""),
                        "line": pos.get("new_line", 0),
                        "body": note_body,
                    })
            else:
                # Fallback note
                if _is_fallback_body(note_body):
                    all_issues.extend(_parse_fallback_issues(disc["id"], note_body))

        if len(body) < 100:
            break

    return all_issues


# ── GitHub backend ──


def _get_github_bot_login():
    """Get the OCR bot login to filter review comments."""
    return os.environ.get("OCR_BOT_LOGIN", "github-actions[bot]")


def _is_github_bot(comment):
    """Check if a GitHub review comment is from the OCR bot."""
    bot_login = _get_github_bot_login()
    user = comment.get("user", {})
    # Match by login or type=Bot
    return user.get("login") == bot_login or user.get("type") == "Bot"


def _pull_github(pr_number, skip_resolved=True):
    """Fetch OCR review issues from a GitHub PR.

    GitHub review comments are flat (not nested like GitLab discussions).
    Thread root comments have in_reply_to_id == null.

    For resolve detection: GitHub doesn't expose resolved state on the REST
    comment object. Resolved threads require GraphQL. For pull phase, we
    skip resolved detection (fetch all), and rely on the post-labels phase
    to handle resolve state.
    """
    from ocr_github import curl, get_project_id

    owner_repo = get_project_id()
    if not owner_repo:
        print("ERROR: could not determine GitHub owner/repo", file=sys.stderr)
        return []

    all_issues = []
    page = 1
    per_page = 100

    while page <= 10:  # safety cap
        endpoint = f"/repos/{owner_repo}/pulls/{pr_number}/comments?per_page={per_page}&page={page}"
        status, body, headers = curl(endpoint)
        if status == 0 or not isinstance(body, list) or not body:
            break

        for comment in body:
            # Only process bot comments
            if not _is_github_bot(comment):
                continue

            # Only process thread roots (not replies)
            if comment.get("in_reply_to_id") is not None:
                continue

            comment_id = str(comment.get("id", ""))
            filepath = comment.get("path", "")
            line = comment.get("line") or comment.get("original_line") or 0
            note_body = comment.get("body", "")

            if _is_review_content(note_body):
                all_issues.append({
                    "discussion_id": comment_id,
                    "file": filepath,
                    "line": line,
                    "body": note_body,
                })
            elif _is_fallback_body(note_body):
                all_issues.extend(_parse_fallback_issues(comment_id, note_body))

        if len(body) < per_page:
            break
        page += 1

    return all_issues


# ── Shared dedup ──


def deduplicate(issues):
    """Deduplicate by (file, line, body_full). First occurrence wins."""
    seen = set()
    unique = []
    for d in issues:
        key = (d["file"], d["line"], d["body"].strip())
        if key not in seen:
            seen.add(key)
            unique.append(d)
    return unique


# ── Main ──


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ocr-pull-discussions.py <MR_OR_PR_ID> [--all]", file=sys.stderr)
        sys.exit(1)

    mr_or_pr_id = sys.argv[1]
    skip_resolved = "--all" not in sys.argv

    platform = detect_platform()
    print(f"Detected platform: {platform}", file=sys.stderr)

    if platform == "github":
        issues = _pull_github(mr_or_pr_id, skip_resolved=skip_resolved)
    else:
        issues = _pull_gitlab(mr_or_pr_id, skip_resolved=skip_resolved)

    print(f"Pulled {len(issues)} raw issues", file=sys.stderr)

    unique = deduplicate(issues)
    print(f"Deduplicated to {len(unique)} unique issues", file=sys.stderr)

    json.dump(unique, sys.stdout, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
