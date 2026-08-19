#!/usr/bin/env python3
"""Merge validated findings into patterns-db.json.

Usage:
    python3 scripts/merge_findings.py <findings.json> [options]

Options:
    --db <path>           DB path (default: references/patterns-db.json)
    --schema <path>       Schema path (default: references/patterns-db.schema.json)
    --dry-run             Preview without writing
    --project-source 'name=github.com/org/repo'  Override project source (repeatable)
    --backup              Backup DB before merge (writes <db>.bak)
    --repo-root <path>    Auto-detect project source from git remote (e.g. ~/third-party)
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from datetime import date


def detect_project_source(repo_root: str, project: str) -> str:
    """Try to detect GitHub source from git remote URL."""
    for repo_dir in [
        os.path.join(repo_root, project),
        os.path.join(repo_root, project.lower()),
        os.path.join(repo_root, project.replace("_", "-")),
    ]:
        if os.path.isdir(os.path.join(repo_dir, ".git")):
            try:
                result = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    capture_output=True, text=True, cwd=repo_dir, timeout=5,
                )
                url = result.stdout.strip()
                # Extract org/repo from various URL formats
                # git@github.com:org/repo.git → github.com/org/repo
                # https://github.com/org/repo.git → github.com/org/repo
                match = __import__("re").search(r"(?:github\.com[:/])([^/]+/[^/\s]+?)(?:\.git)?$", url)
                if match:
                    return f"github.com/{match.group(1)}"
            except Exception:
                pass
    return f"github.com/{project}/{project}"


def main():
    ap = argparse.ArgumentParser(description="Merge findings into patterns-db.json")
    ap.add_argument("findings", help="Path to validated findings JSON file")
    ap.add_argument("--db", default="references/patterns-db.json")
    ap.add_argument("--schema", default="references/patterns-db.schema.json")
    ap.add_argument("--dry-run", action="store_true", help="Preview without writing")
    ap.add_argument("--project-source", action="append", default=[],
                    help="'project=github.com/org/repo' (repeatable)")
    ap.add_argument("--backup", action="store_true", help="Backup DB before merge")
    ap.add_argument("--repo-root", default=None, help="Auto-detect project source from git remote")
    args = ap.parse_args()

    try:
        import jsonschema
    except ImportError:
        print("ERROR: jsonschema not installed", file=sys.stderr)
        return 1

    # Load
    with open(args.db) as f:
        db = json.load(f)
    with open(args.findings) as f:
        findings = json.load(f)
    with open(args.schema) as f:
        schema = json.load(f)

    # Validate findings — separate valid from invalid, save invalid for retry
    finding_schema = schema["$defs"]["subagent_finding"]
    valid = []
    invalid = []
    for i, f in enumerate(findings):
        try:
            jsonschema.validate(f, finding_schema)
            valid.append(f)
        except jsonschema.ValidationError as e:
            invalid.append((i, f, e.message))
            print(f"WARNING: Invalid finding #{i}: {e.message}", file=sys.stderr)

    # Auto-fix common issue: is_new=true with occurrence key present (should be absent)
    auto_fixed = 0
    for i, f, msg in invalid[:]:
        if f.get("is_new") and f.get("new_pattern") and "occurrence" in f:
            del f["occurrence"]
            try:
                jsonschema.validate(f, finding_schema)
                valid.append(f)
                invalid.remove((i, f, msg))
                auto_fixed += 1
            except jsonschema.ValidationError:
                pass
    if auto_fixed:
        print(f"Auto-fixed {auto_fixed} findings (cleared occurrence for is_new=true)", file=sys.stderr)

    # Save invalid findings for retry
    if invalid:
        retry_path = args.findings.replace(".json", "-invalid.json")
        with open(retry_path, "w") as f:
            json.dump([f for _, f, _ in invalid], f, indent=2, ensure_ascii=False)
        print(f"{len(invalid)} invalid findings saved to {retry_path} for retry", file=sys.stderr)

    matched = [f for f in valid if not f.get("is_new")]
    new = [f for f in valid if f.get("is_new")]

    # Build source override map
    source_overrides = {}
    for s in args.project_source:
        if "=" in s:
            name, src = s.split("=", 1)
            source_overrides[name.strip()] = src.strip()

    # Add new projects
    existing_proj_names = {p["name"] for p in db["projects"]}
    new_projects = []
    for f in valid:
        occ = f.get("occurrence") or f.get("new_pattern", {}).get("occurrence", {})
        proj = occ.get("project")
        if proj and proj not in existing_proj_names:
            existing_proj_names.add(proj)
            if proj in source_overrides:
                source = source_overrides[proj]
            elif args.repo_root:
                source = detect_project_source(args.repo_root, proj)
            else:
                source = f"github.com/{proj}/{proj}"
            new_projects.append(
                {"name": proj, "source": source, "ref": occ.get("ref", ""), "explored": True}
            )
            print(f"  New project: {proj} (ref={occ.get('ref', '?')}, source={source})")

    db["projects"].extend(new_projects)

    # Merge matched: add occurrences to existing patterns
    patterns_by_id = {p["id"]: p for p in db["patterns"]}
    occ_added = 0
    occ_skipped = 0
    for f in matched:
        pid = f["matched_pattern_id"]
        if pid not in patterns_by_id:
            print(f"WARNING: Pattern {pid} not found in DB, skipping", file=sys.stderr)
            continue
        occ = f["occurrence"]
        existing = patterns_by_id[pid]["occurrences"]
        is_dup = any(
            o["project"] == occ["project"]
            and o["file"] == occ["file"]
            and o["lines"] == occ["lines"]
            for o in existing
        )
        if is_dup:
            occ_skipped += 1
        else:
            patterns_by_id[pid]["occurrences"].append(occ)
            occ_added += 1

    # Merge new: assign IDs and add — check for duplicate names first
    max_id = max(int(p["id"][1:]) for p in db["patterns"])
    existing_names = {p["name"] for p in db["patterns"]}
    existing_by_name = {p["name"]: p for p in db["patterns"]}
    new_added = 0
    new_merged_into_existing = 0
    for f in new:
        np = f["new_pattern"]
        if np["name"] in existing_names:
            # Same name already exists — merge occurrence into existing pattern
            target = existing_by_name[np["name"]]
            occ = np["occurrence"]
            is_dup = any(
                o["project"] == occ["project"]
                and o["file"] == occ["file"]
                and o["lines"] == occ["lines"]
                for o in target["occurrences"]
            )
            if not is_dup:
                target["occurrences"].append(occ)
            new_merged_into_existing += 1
            continue
        max_id += 1
        new_pattern = {
            "id": f"P{max_id:03d}",
            "name": np["name"],
            "dimension": np["dimension"],
            "description": np["description"],
            "rationale": np.get("rationale", ""),
            "is_new": True,
            "occurrences": [np["occurrence"]],
        }
        db["patterns"].append(new_pattern)
        existing_names.add(np["name"])
        existing_by_name[np["name"]] = new_pattern
        new_added += 1

    if new_merged_into_existing:
        print(f"  New patterns merged into existing (same name): {new_merged_into_existing}", file=sys.stderr)

    db["last_updated"] = str(date.today())

    # Validate merged DB
    try:
        jsonschema.validate(db, schema)
    except jsonschema.ValidationError as e:
        print(f"ERROR: Merged DB fails validation: {e.message}", file=sys.stderr)
        return 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Merge Summary")
    print(f"{'='*60}")
    print(f"  Findings loaded:    {len(findings)} ({len(valid)} valid, {len(findings)-len(valid)} invalid)")
    print(f"  Matched:            {len(matched)} ({occ_added} new occurrences, {occ_skipped} duplicates skipped)")
    print(f"  New patterns:       {new_added}")
    print(f"  New projects:       {len(new_projects)}")
    print(f"  Total patterns:     {len(db['patterns'])}")
    print(f"  Total projects:     {len(db['projects'])}")
    print(f"  Total occurrences:  {sum(len(p['occurrences']) for p in db['patterns'])}")

    # Top patterns
    print(f"\nTop 10 patterns by occurrence count:")
    sorted_p = sorted(db["patterns"], key=lambda p: len(p["occurrences"]), reverse=True)
    for p in sorted_p[:10]:
        print(f"  {p['id']} ({len(p['occurrences'])} occ): {p['name']}")

    # Dimensions
    dim_counts = Counter(p["dimension"] for p in db["patterns"])
    print(f"\nPatterns by dimension:")
    for dim, count in dim_counts.most_common():
        print(f"  {dim}: {count}")

    if args.dry_run:
        print(f"\n[DRY RUN] No changes written.")
        return 0

    # Backup
    if args.backup:
        bak_path = args.db + ".bak"
        shutil.copy2(args.db, bak_path)
        print(f"\nBackup written to {bak_path}")

    # Write
    with open(args.db, "w") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Written to {args.db} ({os.path.getsize(args.db)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
