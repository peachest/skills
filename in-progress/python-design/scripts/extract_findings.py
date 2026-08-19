#!/usr/bin/env python3
"""Extract subagent findings from output files into a single JSON array.

Supports raw JSON (R4+) and markdown-embedded JSON (R1-R3 fallback).
Auto-fixes common data quality issues during extraction.

Usage:
    python3 scripts/extract_findings.py <output-dir> [--out <path>] [--ext .md]
"""
import argparse
import json
import os
import re
import sys
from collections import Counter


def parse_objects_individually(content: str) -> list:
    """Fallback: parse JSON objects one by one using brace-depth tracking.

    Handles truncated JSON (missing closing brace on last object),
    unescaped newlines in strings, and other LLM output quirks.
    """
    depth = 0
    in_str = False
    esc = False
    obj_starts = []
    obj_ends = []

    for i, c in enumerate(content):
        if esc:
            esc = False
            continue
        if c == "\\":
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == "{":
            if depth == 0:
                obj_starts.append(i)
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                obj_ends.append(i)

    # If more starts than ends, the last object is truncated — try to salvage
    salvaged = []
    if len(obj_starts) > len(obj_ends):
        # The truncated content may need both } and ] to close
        # Try progressively adding closing chars — covers array+object nesting
        closing_candidates = [
            "}", "}}", "}}}", "}}}}",
            "]}", "]}}", "]}}}",
            "}]}", "}]}}",
            "}}]}", "}}]}}",
            "}}}]}",
            "]}]}", "]}]}]}",
            "}}]}]}", "}}]}]}}",
        ]
        last_start = obj_starts[-1]
        truncated = content[last_start:]
        for extra in closing_candidates:
            try:
                obj = json.loads(truncated + extra)
                if isinstance(obj, dict):
                    salvaged.append(obj)
                    break
            except json.JSONDecodeError:
                # Also try with newlines escaped
                fixed = truncated.replace("\n", "\\n") + extra
                try:
                    obj = json.loads(fixed)
                    if isinstance(obj, dict):
                        salvaged.append(obj)
                        break
                except json.JSONDecodeError:
                    continue

    findings = []
    for start, end in zip(obj_starts, obj_ends):
        if end < start:
            continue
        obj_str = content[start : end + 1]
        try:
            obj = json.loads(obj_str)
            findings.append(obj)
        except json.JSONDecodeError:
            # Try fixing literal newlines inside string values
            fixed = obj_str.replace("\n", "\\n")
            try:
                obj = json.loads(fixed)
                findings.append(obj)
            except json.JSONDecodeError:
                pass  # skip unparseable object

    findings.extend(salvaged)

    # Unwrap {"findings": [...]} wrappers — can appear in salvaged objects
    unwrapped = []
    for f in findings:
        if isinstance(f, dict) and "findings" in f and isinstance(f["findings"], list):
            unwrapped.extend(f["findings"])
        else:
            unwrapped.append(f)
    return unwrapped


def extract_json_from_content(content: str) -> list:
    """Extract JSON findings from content.

    Handles three formats:
    1. {"findings": [...]} — outputSchema wrapper (preferred, R6+)
    2. [...] — raw JSON array (R4-R5)
    3. ```json [...] ``` — markdown fenced (R1-R3 fallback)
    4. Object-by-object parsing (handles truncated/malformed JSON)
    """
    # 1. Direct parse — could be {"findings": [...]} or [...]
    try:
        obj = json.loads(content)
        if isinstance(obj, dict):
            findings = obj.get("findings", [])
            return findings if isinstance(findings, list) else [findings]
        elif isinstance(obj, list):
            return obj
        return []
    except json.JSONDecodeError:
        pass

    # 2. Fenced blocks
    arrays = []
    for block in re.findall(r"```json\s*\n(.*?)\n```", content, re.DOTALL):
        try:
            obj = json.loads(block)
            if isinstance(obj, dict):
                findings = obj.get("findings", [])
                arrays.extend(findings if isinstance(findings, list) else [findings])
            elif isinstance(obj, list):
                arrays.extend(obj)
        except json.JSONDecodeError:
            # Try object-by-object on the fenced block
            objs = parse_objects_individually(block)
            # Also check if any object is a {"findings": [...]} wrapper
            extracted = []
            for o in objs:
                if isinstance(o, dict) and "findings" in o:
                    extracted.extend(o["findings"])
                else:
                    extracted.append(o)
            arrays.extend(extracted)
    if arrays:
        return arrays

    # 3. Object-by-object parsing (handles truncated JSON)
    objs = parse_objects_individually(content)
    if objs:
        # Check if any object is a {"findings": [...]} wrapper
        extracted = []
        for o in objs:
            if isinstance(o, dict) and "findings" in o:
                extracted.extend(o["findings"])
            else:
                extracted.append(o)
        return extracted

    # 4. Bracket matching
    for match in re.finditer(r"^\s*\[", content, re.MULTILINE):
        start = match.start()
        depth = 0
        for end in range(start, len(content)):
            if content[end] == "[":
                depth += 1
            elif content[end] == "]":
                depth -= 1
                if depth == 0:
                    try:
                        obj = json.loads(content[start : end + 1])
                        if isinstance(obj, list):
                            return obj
                    except json.JSONDecodeError:
                        pass
                    break
    return []


def fix_finding(finding: dict, fix_log: list) -> dict:
    """Auto-fix common data quality issues in a finding. Returns fixed finding + logs changes."""
    occ = finding.get("occurrence") or finding.get("new_pattern", {}).get("occurrence", {})
    if not occ:
        return finding

    # Fix 1: literal \n and \t in snippet → real newlines
    snip = occ.get("snippet", "")
    if "\\n" in snip or "\\t" in snip:
        occ["snippet"] = snip.replace("\\n", "\n").replace("\\t", "\t")
        fix_log.append("snippet: literal \\n/\\t → real newlines")

    # Fix 2: comma in file path → keep only first path
    filepath = occ.get("file", "")
    if "," in filepath:
        occ["file"] = filepath.split(",")[0].strip()
        fix_log.append("file path: multi-path → first only")

    # Fix 3: absolute or ./ path → strip prefix
    if filepath.startswith("./"):
        occ["file"] = filepath[2:]
        fix_log.append("file path: stripped ./ prefix")

    # Fix 4: markdown fence artifacts in snippet
    snip = occ.get("snippet", "")
    if "```" in snip:
        occ["snippet"] = snip.replace("```python\n", "").replace("```python", "").replace("```", "").strip()
        fix_log.append("snippet: stripped markdown fences")

    # Fix 5: leading/trailing whitespace in snippet
    snip = occ.get("snippet", "")
    if snip != snip.strip():
        occ["snippet"] = snip.strip()

    return finding


def deduplicate(findings: list) -> list:
    """Remove exact duplicates by serialized JSON keys."""
    seen = set()
    unique = []
    for f in findings:
        key = json.dumps(f, sort_keys=True)
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def main():
    ap = argparse.ArgumentParser(description="Extract findings from subagent output files")
    ap.add_argument("output_dir", help="Directory containing subagent output files")
    ap.add_argument("--out", default=None, help="Output file path (default: stdout)")
    ap.add_argument("--ext", default=".md", help="File extension to scan (default: .md)")
    ap.add_argument("--no-fix", action="store_true", help="Skip auto-fix of common issues")
    args = ap.parse_args()

    if not os.path.isdir(args.output_dir):
        print(f"ERROR: {args.output_dir} is not a directory", file=sys.stderr)
        return 1

    all_findings = []
    stats = {}
    total_fixes = Counter()

    for fname in sorted(os.listdir(args.output_dir)):
        if not fname.endswith(args.ext):
            continue
        key = fname.replace(args.ext, "")
        path = os.path.join(args.output_dir, fname)
        with open(path) as f:
            content = f.read()

        raw = extract_json_from_content(content)

        # Auto-fix
        if not args.no_fix:
            for f in raw:
                fixes = []
                fix_finding(f, fixes)
                for fix in fixes:
                    total_fixes[fix] += 1

        unique = deduplicate(raw)

        matched = sum(1 for f in unique if not f.get("is_new"))
        new = sum(1 for f in unique if f.get("is_new"))
        stats[key] = {"total": len(unique), "matched": matched, "new": new}
        all_findings.extend(unique)

    # Summary
    print(f"Extracted {len(all_findings)} findings from {len(stats)} files:", file=sys.stderr)
    for key in sorted(stats):
        s = stats[key]
        print(f"  {key:20s}: {s['total']:3d} ({s['matched']} matched, {s['new']} new)", file=sys.stderr)

    if total_fixes:
        print(f"\nAuto-fixes applied:", file=sys.stderr)
        for fix, count in total_fixes.most_common():
            print(f"  {fix}: {count}", file=sys.stderr)

    output = json.dumps(all_findings, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w") as f:
            f.write(output)
        print(f"Written {len(all_findings)} findings to {args.out}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
