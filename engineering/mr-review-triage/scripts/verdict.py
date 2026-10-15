"""Record one triage verdict into the MR's classified.json (sole writer).

The agent-facing interface of the triage pipeline: a finding ordinal (`no`)
from the pull state file plus the verdict semantic fields. The script —
never the agent — copies the full discussion_id byte-exact from
`.triage/<MR>/issues.json` into `.triage/<MR>/classified.json`, computes the
body anchor (sha256(body)[:16]) and appends or replaces exactly one schema 2
entry per invocation (atomic read-modify-write via tmp file + os.replace).

    python3 <SKILL_DIR>/scripts/verdict.py <MR> <no> --class TP|FP|Edge|OOS|Q \
        --reason "..." [--fix-plan "..."] [--priority high|medium|low] \
        [--resolved true|false] [--force]

Per-item `resolved` semantics (spec #57 Amendment R2, 修订 A): the
close-after-verification decision is made at verdict time and stored per
item — post only executes it. Edge defaults to resolved=true (overridable
with --resolved false); Q defaults to open and closes only on an explicit
--resolved true. TP/FP/OOS leave the field unset so post applies its own
mode map (standalone /fix vs triage).

Success echoes `no` + author + first body line so a misremembered ordinal is
caught at write time. Exit codes: 0 ok; 1 state error (missing pull file,
unknown no, existing verdict without --force, unusable state files); 2 usage
error (argparse). Display discipline: the discussion_id never reaches
human-readable output — no full or truncated id shapes.
"""

import argparse
import hashlib
import json
import os
import sys

from ocr_platform import triage_state_dir

SCHEMA_VERSION = 2


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="verdict.py",
        description="Record one triage verdict into .triage/<MR>/classified.json "
                    "(the sole writer of verdict semantic fields).",
        epilog="Exit codes: 0 ok; 1 state error; 2 usage error.",
    )
    parser.add_argument("mr", help="MR/PR id naming the state dir .triage/<MR>/")
    parser.add_argument("no", type=int, help="finding ordinal from the pull state file (1..N)")
    parser.add_argument("--class", dest="classification", required=True,
                        choices=["TP", "FP", "Edge", "OOS", "Q"],
                        help="verdict classification (stored as given; post normalizes Q)")
    parser.add_argument("--reason", required=True, help="verdict reason for the reply body")
    parser.add_argument("--fix-plan", dest="fix_plan",
                        help="fix plan (required for TP — post skips TP entries without one)")
    parser.add_argument("--priority", choices=["high", "medium", "low"], help="TP priority")
    parser.add_argument("--resolved", choices=["true", "false"],
                        help="per-item resolve decision; default: Edge=true, Q=false, others unset")
    parser.add_argument("--force", action="store_true",
                        help="overwrite an existing verdict for this finding")
    return parser


def _load_pull_finding(pull_path, no):
    """Load the pull state file and return the finding carrying this ordinal."""
    if not os.path.exists(pull_path):
        print(f"ERROR: pull state file not found: {pull_path} — run "
              f"ocr-pull-discussions.py first with stdout redirected to that path",
              file=sys.stderr)
        sys.exit(1)
    try:
        with open(pull_path, encoding="utf-8") as fh:
            findings = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: pull state file {pull_path} is not readable JSON: {exc}",
              file=sys.stderr)
        sys.exit(1)
    if not isinstance(findings, list):
        print(f"ERROR: pull state file {pull_path}: expected the bare findings "
              f"array ocr-pull-discussions.py writes to stdout", file=sys.stderr)
        sys.exit(1)
    finding = next((f for f in findings if isinstance(f, dict) and f.get("no") == no), None)
    if finding is None:
        available = sorted({f["no"] for f in findings
                            if isinstance(f, dict) and isinstance(f.get("no"), int)})
        span = f"{available[0]}..{available[-1]}" if available else "none — empty pull file"
        print(f"ERROR: no finding with no={no} in {pull_path} (available: {span})",
              file=sys.stderr)
        sys.exit(1)
    return finding


def _load_classified_entries(classified_path):
    """Return prior entries, or None when the file does not exist yet.

    A file that exists but is corrupt or not schema 2 is a state error — it
    must never be silently replaced (that would discard verdicts).
    """
    if not os.path.exists(classified_path):
        return None
    try:
        with open(classified_path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: classified file {classified_path} is not readable JSON: "
              f"{exc} — fix or remove it before recording verdicts", file=sys.stderr)
        sys.exit(1)
    if (not isinstance(data, dict) or data.get("schema") != SCHEMA_VERSION
            or not isinstance(data.get("entries"), list)):
        print(f"ERROR: {classified_path}: schema {SCHEMA_VERSION} classified file "
              f"required ({{\"schema\": {SCHEMA_VERSION}, \"entries\": [...]}}) — "
              f"rebuild it before recording verdicts", file=sys.stderr)
        sys.exit(1)
    return data["entries"]


def _find_existing(entries, no, disc_id, anchor):
    """Locate a prior verdict for the same ordinal, or for the same finding
    (same thread + same body anchor) under an ordinal reshuffled across pulls.
    Returns (index, kind) or (None, None)."""
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        if entry.get("no") == no:
            return i, "ordinal"
        if entry.get("discussion_id") == disc_id and entry.get("anchor") == anchor:
            return i, "finding"
    return None, None


def main():
    parser = _build_parser()
    args = parser.parse_args()

    if args.no < 1:
        parser.error(f"no must be >= 1, got {args.no}")
    if args.mr in (".", "..") or "/" in args.mr:
        parser.error(f"mr must be a plain state-dir name, got {args.mr!r}")
    if not args.reason.strip():
        parser.error("--reason must not be empty")
    if args.classification == "TP" and not (args.fix_plan or "").strip():
        parser.error("--fix-plan is required for --class TP")

    if args.resolved is not None:
        resolved = args.resolved == "true"
    elif args.classification == "Edge":
        resolved = True  # Amendment R2 修订 A: Edge default-resolve decided at verdict time
    elif args.classification == "Q":
        resolved = False
    else:
        resolved = None  # TP/FP/OOS: post applies its mode map (standalone vs triage)

    state_dir = triage_state_dir(args.mr)
    pull_path = os.path.join(state_dir, "issues.json")
    classified_path = os.path.join(state_dir, "classified.json")

    finding = _load_pull_finding(pull_path, args.no)
    disc_id = finding.get("discussion_id")
    if not isinstance(disc_id, str) or not disc_id:
        print(f"ERROR: pull state file {pull_path}: finding no={args.no} carries "
              f"no discussion_id", file=sys.stderr)
        sys.exit(1)
    body = finding.get("body", "")
    author = str(finding.get("author") or "?")
    anchor = hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]

    entries = _load_classified_entries(classified_path)
    if entries is None:
        entries = []

    match_idx, match_kind = _find_existing(entries, args.no, disc_id, anchor)
    if match_idx is not None and not args.force:
        if match_kind == "finding":
            print(f"ERROR: this finding is already classified (existing entry no="
                  f"{entries[match_idx].get('no')}) — ordinal reshuffled across "
                  f"pulls? pass --force to replace it", file=sys.stderr)
        else:
            print(f"ERROR: no={args.no} already has a verdict in {classified_path} — "
                  f"pass --force to overwrite", file=sys.stderr)
        sys.exit(1)

    entry = {
        # byte-exact copy made here — the agent never touches the id
        "discussion_id": disc_id,
        "no": args.no,
        "anchor": anchor,
        "classification": args.classification,
        "reason": args.reason.strip(),
    }
    if (args.fix_plan or "").strip():
        entry["fix_plan"] = args.fix_plan.strip()
    if args.priority is not None:
        entry["priority"] = args.priority
    if resolved is not None:
        entry["resolved"] = resolved
    entry["posted"] = False

    if match_idx is not None:
        entries[match_idx] = entry  # in-place slot replace; other entries untouched
    else:
        entries.append(entry)

    os.makedirs(state_dir, exist_ok=True)
    tmp_path = classified_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as fh:
        json.dump({"schema": SCHEMA_VERSION, "entries": entries},
                  fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp_path, classified_path)  # atomic read-modify-write

    first_line = body.strip().splitlines()[0] if body.strip() else ""
    line = f"[OK] no={args.no} {args.classification}"
    if resolved is not None:
        line += f" resolved={'true' if resolved else 'false'}"
    line += f" author={author}: {first_line}"
    print(line)


if __name__ == "__main__":
    main()
