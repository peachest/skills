"""Post classification labels + resolve to OCR review discussions.

Reads a JSON array from stdin with classification results and for each:
  1. Posts a reply note with classification label + reason/fix-plan
  2. Resolves the discussion based on classification type

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
        "reason": "...",           # FP/Edge: why classified this way
        "fix_plan": "...",         # TP only: proposed fix
        "priority": "high|medium|low",  # TP only
        "resolved": true/false     # override default resolve behavior
      },
      ...
    ]

Usage:
    cat classified.json | python3 ocr-post-labels.py 1

Required env:
    CI_SERVER_URL, CI_PROJECT_ID,
    GITLAB__PERSONAL_ACCESS_TOKEN
"""

import json
import os
import re
import sys

from ocr_gitlab import curl, get_project_id

# ── Templates ──

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

# ── Reply body templates ──
# GitLab-flavored Markdown. Uses heading + bullet-style labels so
# fix_plan/reason can contain inline code (`x`) and fenced code blocks (```).

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

# Default resolve behavior by classification
_DEFAULT_RESOLVED = {
    "TP": False,       # stay open for tracking
    "FP": True,        # close — not a real issue
    "Edge": False,     # keep open — real but low priority
    "OOS": True,       # close — not this MR's scope
    "Question": False, # keep open — needs discussion
}

_VALID_CLASSIFICATIONS = set(_CLASSIFICATION_LABELS.keys())

# ── Input parsing ──


def _extract_json(raw):
    """Try to extract a JSON array from raw input.

    Handles: pure JSON, ```json``` fences, embedded JSON in prose.
    """
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
    """Validate a single entry. Returns (ok, error_msg, cleaned_item)."""
    cleaned = dict(item)

    # Normalize field names: _cat/_reason from classification workflow
    if "classification" not in cleaned and "_cat" in cleaned:
        cleaned["classification"] = cleaned["_cat"]
    if "reason" not in cleaned and "_reason" in cleaned:
        cleaned["reason"] = cleaned["_reason"]
    if "priority" not in cleaned and "_priority" in cleaned:
        # Map emoji to text: 🚨→high, ⚠️→medium, 🟢→low
        pri_map = {"🚨": "high", "⚠️": "medium", "🟢": "low"}
        cleaned["priority"] = pri_map.get(cleaned["_priority"], "medium")

    # Required: discussion_id (full 40-char SHA)
    disc_id = str(cleaned.get("discussion_id", "")).strip()
    if not disc_id:
        return (False, f"item {idx}: missing discussion_id", None)
    if len(disc_id) < 20:
        return (False, f"item {idx}: discussion_id too short ({len(disc_id)} chars)", None)
    cleaned["discussion_id"] = disc_id

    # Classification
    cls = cleaned.get("classification", "FP")
    if cls not in _VALID_CLASSIFICATIONS:
        print(f"  [WARN] item {idx}: unknown classification '{cls}', using 'FP'", file=sys.stderr)
        cls = "FP"
    cleaned["classification"] = cls

    # Reason / fix plan
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
        cleaned["adr"] = adr  # 可选，空则不显示 ADR 行
    else:
        reason = str(cleaned.get("reason", "")).strip()
        if not reason:
            return (False, f"item {idx}: missing reason", None)
        cleaned["reason"] = reason

    # Resolved
    resolved = cleaned.get("resolved")
    if resolved is None:
        resolved = _DEFAULT_RESOLVED.get(cls, False)
    if not isinstance(resolved, bool):
        resolved = _DEFAULT_RESOLVED.get(cls, False)
    cleaned["resolved"] = resolved

    return (True, "", cleaned)


def _build_body(cleaned):
    """Build reply body text from cleaned item, using GitLab-flavored Markdown."""
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


# ── Core logic ──


def post_labels(mr_iid, items):
    """Reply + optionally resolve OCR review discussions."""
    project_id = get_project_id()
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

        # 2) Resolve (if applicable)
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


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ocr-post-labels.py <MR_IID>  <  classified.json", file=sys.stderr)
        sys.exit(1)

    mr_iid = sys.argv[1]
    raw = sys.stdin.read()

    items = _extract_json(raw)
    if items is None:
        print("ERROR: no valid JSON array found in input", file=sys.stderr)
        sys.exit(1)
    if not isinstance(items, list):
        print("ERROR: expected JSON array, got " + type(items).__name__, file=sys.stderr)
        sys.exit(1)

    ok = post_labels(mr_iid, items)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
