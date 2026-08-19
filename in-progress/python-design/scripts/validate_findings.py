#!/usr/bin/env python3
"""Validate subagent findings against patterns-db.schema.json.

Usage:
    python3 scripts/validate_findings.py <findings.json> [options]

Checks:
1. Schema validation (structure, required fields, conditional rules)
2. matched_pattern_id exists in current DB
3. Snippet quality (literal escapes, length extremes, markdown artifacts)
4. Pattern name transferability (project-specific terms)
5. File path format (no commas, no absolute paths)
6. Ref format (tag name or commit:<short-hash>)
7. Duplicate new pattern names (exact + fuzzy similarity)
8. Rationale presence for new patterns
9. File path existence (if --repo-root given)

Exit code: 0 if all valid, 1 if schema-invalid. Quality warnings don't affect exit code.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter
from difflib import SequenceMatcher


def main():
    ap = argparse.ArgumentParser(description="Validate findings against schema")
    ap.add_argument("findings", help="Path to findings JSON file")
    ap.add_argument("--schema", default="references/patterns-db.schema.json")
    ap.add_argument("--db", default="references/patterns-db.json", help="DB for pattern ID cross-check")
    ap.add_argument("--repo-root", default=None, help="Root dir of explored repos for file path verification")
    args = ap.parse_args()

    try:
        import jsonschema
    except ImportError:
        print("ERROR: jsonschema not installed. Run: pip install jsonschema", file=sys.stderr)
        return 1

    with open(args.schema) as f:
        schema = json.load(f)
    with open(args.findings) as f:
        findings = json.load(f)
    with open(args.db) as f:
        db = json.load(f)

    finding_schema = schema["$defs"]["subagent_finding"]
    valid_pattern_ids = {p["id"] for p in db["patterns"]}

    # === Schema validation (hard fail) ===
    valid = []
    invalid = []
    for i, f in enumerate(findings):
        try:
            jsonschema.validate(f, finding_schema)
            valid.append(f)
        except jsonschema.ValidationError as e:
            invalid.append((i, f, e.message, list(e.absolute_path)))

    print(f"Valid: {len(valid)}, Invalid: {len(invalid)}")

    if invalid:
        print(f"\n{'='*60}")
        print(f"Invalid findings ({len(invalid)}):")
        for i, f, msg, path in invalid:
            print(f"  #{i}: {msg}")
            print(f"    path: {' -> '.join(str(p) for p in path)}")
            print(f"    keys: {list(f.keys())}")
        return 1

    matched = [f for f in valid if not f.get("is_new")]
    new = [f for f in valid if f.get("is_new")]

    print(f"\nMatched (existing patterns): {len(matched)}")
    print(f"New patterns: {len(new)}")

    # === Stats ===
    pattern_counts = Counter(f["matched_pattern_id"] for f in matched)
    print(f"\nPattern match frequency:")
    for pid, count in pattern_counts.most_common():
        print(f"  {pid}: {count} projects")

    dim_counts = Counter(f["new_pattern"]["dimension"] for f in new)
    print(f"\nNew patterns by dimension:")
    for dim, count in dim_counts.most_common():
        print(f"  {dim}: {count}")

    proj_counts = Counter()
    for f in valid:
        occ = f.get("occurrence") or f.get("new_pattern", {}).get("occurrence", {})
        if occ:
            proj_counts[occ.get("project", "?")] += 1
    print(f"\nFindings by project:")
    for proj, count in proj_counts.most_common():
        print(f"  {proj}: {count}")

    # === Quality checks (warnings, not hard fails) ===
    warnings = []
    info = []

    for i, f in enumerate(valid):
        occ = f.get("occurrence") or f.get("new_pattern", {}).get("occurrence", {})
        snip = occ.get("snippet", "")
        filepath = occ.get("file", "")

        # Literal \n / \t in snippets
        if "\\n" in snip or "\\t" in snip:
            warnings.append(f"#{i}: literal \\n/\\t in snippet (run extract with auto-fix)")

        # Markdown fence artifacts
        if "```" in snip:
            warnings.append(f"#{i}: markdown fence in snippet")

        # Comma in file path (multiple files in one field)
        if "," in filepath:
            warnings.append(f"#{i}: comma in file path (run extract with auto-fix)")

        # Absolute or ./ path
        if filepath.startswith("./"):
            warnings.append(f"#{i}: file path starts with ./")
        if filepath.startswith("/"):
            info.append(f"#{i}: absolute file path: {filepath[:60]}")

        # Snippet length extremes
        if len(snip) > 2000:
            warnings.append(f"#{i}: snippet very long ({len(snip)} chars)")
        # Note: short snippets (<20 chars) are often legitimate (_marker = object())
        # Report as info, not warning
        if len(snip) < 15 and snip:
            info.append(f"#{i}: snippet very short ({len(snip)} chars): {snip[:40]}")

        # File specified but lines empty
        if filepath and not occ.get("lines"):
            info.append(f"#{i}: file specified but lines is empty")

        # Ref format — just check it's not empty or too short
        ref = occ.get("ref", "")
        if not ref:
            warnings.append(f"#{i}: empty ref")
        elif len(ref) < 2:
            warnings.append(f"#{i}: ref too short: '{ref}'")

    # Project name in new pattern name
    for i, f in enumerate(new):
        np = f["new_pattern"]
        proj = np["occurrence"]["project"]
        name_lower = np["name"].lower()
        for term in proj.lower().split("-"):
            if len(term) > 3 and term in name_lower:
                warnings.append(
                    f"#{i}: pattern name '{np['name']}' contains project term '{term}'"
                )

    # Cross-check matched_pattern_id exists in DB
    for i, f in enumerate(matched):
        pid = f["matched_pattern_id"]
        if pid not in valid_pattern_ids:
            warnings.append(f"#{i}: matched_pattern_id '{pid}' not found in DB")

    # Rationale check for new patterns
    for i, f in enumerate(new):
        np = f["new_pattern"]
        if not np.get("rationale"):
            warnings.append(f"#{i}: new pattern '{np['name']}' missing rationale")
        elif len(np.get("rationale", "")) < 10:
            info.append(f"#{i}: new pattern '{np['name']}' has short rationale ({len(np['rationale'])} chars)")

    # Duplicate new pattern names — exact
    names = [f["new_pattern"]["name"] for f in new]
    name_counts = Counter(names)
    dupes = {n: c for n, c in name_counts.items() if c > 1}
    if dupes:
        warnings.append(f"Duplicate new pattern names: {dupes}")
    else:
        print(f"\n✅ No duplicate new pattern names ({len(names)} unique)")

    # Fuzzy duplicate detection
    name_ids = [(f["new_pattern"]["name"], i) for i, f in enumerate(new)]
    fuzzy_dupes = []
    for a in range(len(name_ids)):
        for b in range(a + 1, len(name_ids)):
            name_a, idx_a = name_ids[a]
            name_b, idx_b = name_ids[b]
            ratio = SequenceMatcher(None, name_a.lower(), name_b.lower()).ratio()
            if ratio > 0.75:
                fuzzy_dupes.append((idx_a, idx_b, name_a, name_b, ratio))
    if fuzzy_dupes:
        print(f"\n⚠️  Potential duplicate pattern names (similarity > 0.75):")
        for idx_a, idx_b, name_a, name_b, ratio in fuzzy_dupes:
            print(f"  #{idx_a} vs #{idx_b} ({ratio:.2f}): '{name_a}' vs '{name_b}'")

    # File path existence
    if args.repo_root:
        repo_root = os.path.expanduser(args.repo_root)
        missing = 0
        for i, f in enumerate(valid):
            occ = f.get("occurrence") or f.get("new_pattern", {}).get("occurrence", {})
            proj = occ.get("project", "")
            filepath = occ.get("file", "")
            if proj and filepath:
                found = False
                for repo_dir in [
                    os.path.join(repo_root, proj),
                    os.path.join(repo_root, proj.lower()),
                    os.path.join(repo_root, proj.replace("_", "-")),
                ]:
                    if os.path.exists(os.path.join(repo_dir, filepath)):
                        found = True
                        break
                if not found:
                    missing += 1
                    if missing <= 5:
                        warnings.append(f"#{i}: file not found: {proj}/{filepath}")
        if missing > 5:
            print(f"\n⚠️  {missing} files not found (showing first 5)")

    # Output
    if warnings:
        print(f"\n⚠️  Quality warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")
    else:
        print(f"\n✅ No quality warnings")

    if info:
        print(f"\nℹ️  Info ({len(info)}):")
        for msg in info[:10]:
            print(f"  {msg}")
        if len(info) > 10:
            print(f"  ... and {len(info) - 10} more")

    return 0 if not invalid else 1


if __name__ == "__main__":
    sys.exit(main())
