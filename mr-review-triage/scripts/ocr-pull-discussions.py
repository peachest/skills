"""Pull all OCR review discussions from a GitLab MR.

Outputs deduplicated review issues as JSON to stdout.
Progress messages go to stderr — do NOT redirect stderr into stdout (no 2>&1).

    python3 scripts/ocr-pull-discussions.py <MR_IID> > /tmp/issues.json

Project ID resolved automatically from env or git remote;
optional override: CI_PROJECT_ID=<id>.  Required: CI_SERVER_URL,
GITLAB__PERSONAL_ACCESS_TOKEN
"""

import json
import re
import sys

from ocr_gitlab import curl, get_project_id

# ── Junk filters ──

_JUNK_BODIES = {
    "changed this line", "changed the description", "nouse",
    "test discussion", "line-ending test", "test discc", "header test",
    "Test discussion", "inline test L57", "inline test ocr-review.yml L30",
}

_JUNK_PREFIXES = {
    "changed this line", "**PR Description**", "**[Persistent review]",
    "## PR Reviewer", "Added 1 commit",
}


def _is_resolved(discussion):
    """Check if a discussion has been resolved.

    GitLab stores resolved state on the first note (not on the discussion).
    The first note's 'resolved' field is set when PUT /discussions/{id}
    with 'resolved': true is called.
    """
    notes = discussion.get("notes", [])
    if not notes:
        return False
    return notes[0].get("resolved", False)


def _is_review_content(body):
    """Check if a discussion body looks like an OCR review issue."""
    body_stripped = body.strip()
    # Exclude junk
    if body_stripped in _JUNK_BODIES:
        return False
    if any(body_stripped.startswith(p) for p in _JUNK_PREFIXES):
        return False
    # Exclude summary / fallback / LGTM notes
    if body_stripped.startswith("🔍"):
        return False
    if body_stripped.startswith("✅"):
        return False
    if body_stripped.startswith("⚠️"):
        return False
    return True


def _is_bot_note(discussion):
    """Check if a discussion's first note is from gitblue.bot."""
    notes = discussion.get("notes", [])
    if not notes:
        return False
    return notes[0].get("author", {}).get("username") == "gitblue.bot"


def _is_inline_issue(discussion):
    """Check if a discussion is an inline OCR review issue."""
    if not _is_bot_note(discussion):
        return False
    first_note = discussion["notes"][0]
    if not first_note.get("position"):
        return False
    return _is_review_content(first_note.get("body", ""))


# ── Fallback note parsing ──
#
# Format:
#   
#   ### `path/to/file.go` (L42-L42)
#   
#   description text...
#   
#   ---
#   
#   ### `path/to/file2.go` (L45-L60)
#   
#   text...
#   
#   ---

_FALLBACK_SEP = re.compile(r"\n---\n")
_FALLBACK_HEADER = re.compile(r"### `([^`]+)`")
_FALLBACK_LINE = re.compile(r"L(\d+)")


def _is_fallback_note(discussion):
    """Check if a discussion is an OCR fallback note (no inline position)."""
    if not _is_bot_note(discussion):
        return False
    first_note = discussion["notes"][0]
    if first_note.get("position"):
        return False
    body = first_note.get("body", "")
    return body.startswith("🔍 OpenCodeReview — issues")


def _parse_fallback_issues(discussion):
    """Extract sub-issues from a fallback note.

    Returns:
        list[dict]: {discussion_id, file, line, body}
    """
    body = discussion["notes"][0]["body"]
    disc_id = discussion["id"]
    issues = []

    # Split by --- separator, skip the first block (header)
    blocks = _FALLBACK_SEP.split(body)[1:]
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # Extract file path from ### `...`
        header_match = _FALLBACK_HEADER.search(block)
        if not header_match:
            continue
        filepath = header_match.group(1)
        line_match = _FALLBACK_LINE.search(block)
        line = int(line_match.group(1)) if line_match else 0
        # Body is everything after the header line
        header_end = header_match.end()
        desc = block[header_end:].strip()
        if desc.startswith("("):
            # Skip optional (L42-L42) suffix after file
            paren_end = desc.find(")")
            desc = desc[paren_end + 1:].strip()
        issues.append({
            "discussion_id": disc_id,
            "file": filepath,
            "line": line,
            "body": desc,
        })

    return issues


def pull_discussions(project_id, mr_iid, max_pages=5, skip_resolved=True):
    """Fetch all OCR review issues from an MR.

    Handles both inline discussions (with diff position) and fallback notes
    (issues that couldn't be posted inline).

    Args:
        skip_resolved: If True (default), skip discussions that are resolved.

    Returns:
        list[dict]: {discussion_id, file, line, body}
    """
    all_issues = []

    for page in range(1, max_pages + 1):
        endpoint = f"/projects/{project_id}/merge_requests/{mr_iid}/discussions?per_page=100&page={page}"
        status, body, _ = curl(endpoint)
        if status == 0 or not isinstance(body, list) or not body:
            break

        for disc in body:
            # Skip resolved discussions by default; --all overrides
            if skip_resolved and _is_resolved(disc):
                continue
            if _is_inline_issue(disc):
                first_note = disc["notes"][0]
                pos = first_note["position"]
                all_issues.append({
                    "discussion_id": disc["id"],
                    "file": pos.get("new_path", ""),
                    "line": pos.get("new_line", 0),
                    "body": first_note["body"],
                })
            elif _is_fallback_note(disc):
                all_issues.extend(_parse_fallback_issues(disc))

        # Stop if last page
        if len(body) < 100:
            break

    return all_issues


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


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ocr-triage-pull.py <MR_IID>", file=sys.stderr)
        sys.exit(1)

    mr_iid = sys.argv[1]
    skip_resolved = "--all" not in sys.argv
    project_id = get_project_id()

    # Pull
    issues = pull_discussions(project_id, mr_iid, skip_resolved=skip_resolved)
    print(f"Pulled {len(issues)} raw issues", file=sys.stderr)

    # Deduplicate
    unique = deduplicate(issues)
    print(f"Deduplicated to {len(unique)} unique issues", file=sys.stderr)

    # Output JSON
    json.dump(unique, sys.stdout, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
