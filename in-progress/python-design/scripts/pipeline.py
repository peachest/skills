#!/usr/bin/env python3
"""Pipeline: extract → validate → merge in one command.

Usage:
    python3 scripts/pipeline.py <output-dir> [options]

Options:
    --repo-root <path>    Root dir of explored repos (e.g. ~/third-party)
    --dry-run             Validate only, don't merge
    --backup              Backup DB before merge
    --keep-temp           Keep temp findings file (default: /tmp/pipeline-findings.json)

Example:
    python3 scripts/pipeline.py /path/to/subagent-outputs --repo-root ~/third-party --backup
"""
import argparse
import os
import subprocess
import sys
import tempfile


def main():
    ap = argparse.ArgumentParser(description="Extract → validate → merge pipeline")
    ap.add_argument("output_dir", help="Directory containing subagent output files")
    ap.add_argument("--repo-root", default=None, help="Root dir of explored repos for file verification")
    ap.add_argument("--dry-run", action="store_true", help="Validate only, don't merge")
    ap.add_argument("--backup", action="store_true", help="Backup DB before merge")
    ap.add_argument("--keep-temp", action="store_true", help="Keep temp findings file")
    ap.add_argument("--skill-dir", default=None, help="Skill directory (default: auto-detect from script location)")
    args = ap.parse_args()

    # Resolve skill dir
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = args.skill_dir or os.path.dirname(script_dir)
    scripts_dir = os.path.join(skill_dir, "scripts")

    # Temp file for findings
    temp_file = tempfile.mktemp(prefix="pipeline-findings-", suffix=".json")

    # Step 1: Extract
    print("=" * 60)
    print("Step 1: Extract")
    print("=" * 60)
    ret = subprocess.run(
        [sys.executable, os.path.join(scripts_dir, "extract_findings.py"),
         args.output_dir, "--out", temp_file],
        cwd=skill_dir,
    )
    if ret.returncode != 0:
        print(f"❌ Extract failed (exit {ret.returncode})")
        return 1

    # Step 2: Validate
    print("\n" + "=" * 60)
    print("Step 2: Validate")
    print("=" * 60)
    validate_cmd = [
        sys.executable, os.path.join(scripts_dir, "validate_findings.py"),
        temp_file,
        "--db", os.path.join(skill_dir, "references/patterns-db.json"),
        "--schema", os.path.join(skill_dir, "references/patterns-db.schema.json"),
    ]
    if args.repo_root:
        validate_cmd.extend(["--repo-root", os.path.expanduser(args.repo_root)])
    ret = subprocess.run(validate_cmd, cwd=skill_dir)
    if ret.returncode != 0:
        print(f"\n❌ Validation failed (exit {ret.returncode})")
        if not args.keep_temp:
            os.unlink(temp_file)
        return 1

    if args.dry_run:
        print(f"\n[DRY RUN] Skipping merge.")
        if not args.keep_temp:
            os.unlink(temp_file)
        return 0

    # Step 3: Merge
    print("\n" + "=" * 60)
    print("Step 3: Merge")
    print("=" * 60)
    merge_cmd = [
        sys.executable, os.path.join(scripts_dir, "merge_findings.py"),
        temp_file,
        "--db", os.path.join(skill_dir, "references/patterns-db.json"),
        "--schema", os.path.join(skill_dir, "references/patterns-db.schema.json"),
    ]
    if args.backup:
        merge_cmd.append("--backup")
    if args.repo_root:
        merge_cmd.extend(["--repo-root", os.path.expanduser(args.repo_root)])
    ret = subprocess.run(merge_cmd, cwd=skill_dir)
    if ret.returncode != 0:
        print(f"\n❌ Merge failed (exit {ret.returncode})")
        if not args.keep_temp:
            os.unlink(temp_file)
        return 1

    # Cleanup
    if not args.keep_temp:
        os.unlink(temp_file)

    print(f"\n✅ Pipeline complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
