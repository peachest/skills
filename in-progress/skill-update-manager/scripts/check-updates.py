#!/usr/bin/env python3
"""Read-only update checker for globally installed skills (both chains).

Chain 1 (remote/third-party): skills installed via `npx skills add -g <github>`.
  Lives in ~/.agents/skills/ + symlinks from ~/.pi/agent/skills/, tracked in
  ~/.agents/.skill-lock.json. We download each source repo's tarball and do a
  file-level diff against the locally installed folder. This avoids the
  lock-hash-scheme trap (see SKILL.md).

Chain 2 (local source repo): skills installed via `npx skills add -g <local-path>`
  from ~/skills. Never in the lock file. We hash-compare each installed real
  directory against its source folder in the skills repo.

Usage:
  check-updates.py remote   # third-party skills from lock
  check-updates.py local    # local skills from the source repo
  check-updates.py all      # both (default)

Exit code: 0 even when updates exist (this is a report, not a gate).
"""
import hashlib
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from collections import defaultdict
from pathlib import Path

HOME = Path.home()
LOCK = HOME / ".agents" / ".skill-lock.json"
AGENTS_SKILLS = HOME / ".agents" / "skills"
PI_SKILLS = HOME / ".pi/agent/skills"
SRC_REPO = HOME / "skills"  # local skill source repo

EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", "__pypackages__"}
EXCLUDE_FILES = {"metadata.json"}  # excluded by the CLI at install time
# Present in both source and install sides, gitignored, not skill content:
EXCLUDE_FILES_LOCAL = EXCLUDE_FILES | {"runtime.conf"}


def scan_tree(root: Path, extra_exclude_files=frozenset()):
    """{relpath: bytes} for all files under root, with exclusions."""
    out = {}
    for root_, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f in EXCLUDE_FILES or f in extra_exclude_files:
                continue
            p = Path(root_) / f
            out[str(p.relative_to(root))] = p.read_bytes()
    return out


def diff_summary(a: dict, b: dict, limit=6):
    """Compact change list: '+' new upstream, '-' removed, '~' modified."""
    changes = []
    for k in sorted(set(a) | set(b)):
        if k not in a:
            changes.append(f"+{k}")
        elif k not in b:
            changes.append(f"-{k}")
        elif a[k] != b[k]:
            changes.append(f"~{k}")
    head = " ".join(changes[:limit])
    more = f" …(+{len(changes) - limit})" if len(changes) > limit else ""
    return head + more, len(changes)


def installed_dir(name):
    """Resolve the active install location for a skill name, or None."""
    p = PI_SKILLS / name
    if p.is_dir() and not p.is_symlink():
        return p, ".pi(direct)"
    if p.is_symlink():
        return Path(os.path.realpath(p)), "agents"
    return None, None


# ---------------------------------------------------------------- chain 1

def check_remote():
    print("== Chain 1: third-party skills (lock: %s) ==" % LOCK)
    if not LOCK.exists():
        print("SKIP  no lock file found")
        return
    lock = json.loads(LOCK.read_text())

    by_repo = defaultdict(list)
    for name, e in lock["skills"].items():
        if e.get("sourceType") != "github":
            print(f"SKIP    {name}  (sourceType={e.get('sourceType')})")
            continue
        by_repo[e["source"]].append((name, e))

    results = []
    for repo, items in sorted(by_repo.items()):
        ref = next((e.get("ref") for _, e in items if e.get("ref")), None)
        with tempfile.TemporaryDirectory(prefix="skillchk-") as td:
            tarball = Path(td) / "repo.tgz"
            api = f"repos/{repo}/tarball/{ref}" if ref else f"repos/{repo}/tarball"
            r = subprocess.run(
                ["gh", "api", api], stdout=open(tarball, "wb"),
                stderr=subprocess.PIPE, timeout=180,
            )
            if r.returncode != 0:
                # GitHub API flakiness is common; one blind retry
                r = subprocess.run(
                    ["gh", "api", api], stdout=open(tarball, "wb"),
                    stderr=subprocess.PIPE, timeout=180,
                )
            if r.returncode != 0:
                err = r.stderr.decode()[:100].strip().splitlines()[-1] if r.stderr.strip() else "unknown"
                results.extend(("ERROR", n, repo, err) for n, _ in items)
                continue
            try:
                with tarfile.open(tarball) as tf:
                    tf.extractall(td, filter="data")
            except Exception as exc:
                results.extend(("ERROR", n, repo, f"extract: {exc}") for n, _ in items)
                continue
            dirs = [d for d in Path(td).iterdir() if d.is_dir()]
            if not dirs:
                results.extend(("ERROR", n, repo, "empty tarball") for n, _ in items)
                continue
            src_root = dirs[0]

            for name, e in items:
                local_dir, where = installed_dir(name)
                if local_dir is None:
                    results.append(("MISSING", name, repo, "lock residue — not installed"))
                    continue
                # repo-root skill: skillPath has no dir prefix
                folder = e["skillPath"].rsplit("/", 1)[0] if "/" in e["skillPath"] else ""
                upstream_dir = src_root / folder
                if not upstream_dir.is_dir():
                    results.append(("GONE", name, repo, f"upstream path '{folder or '.'}' gone"))
                    continue
                up = scan_tree(upstream_dir)
                loc = scan_tree(local_dir)
                if up == loc:
                    results.append(("OK", name, repo, where))
                else:
                    summary, _ = diff_summary(loc, up)
                    results.append(("OUTDATED", name, repo, f"[{where}] {summary}"))

    order = {"OUTDATED": 0, "GONE": 1, "MISSING": 2, "ERROR": 3, "OK": 4}
    results.sort(key=lambda x: (order[x[0]], x[1]))
    for status, name, repo, detail in results:
        print(f"{status:9} {name:36} {detail}")
    n = lambda s: sum(1 for r in results if r[0] == s)
    print(f"\nRemote summary: {n('OUTDATED')} outdated, {n('OK')} up to date, "
          f"{n('GONE')} gone-upstream, {n('MISSING')} lock-residue, {n('ERROR')} errors")
    outdated = sorted(r[1] for r in results if r[0] == "OUTDATED")
    if outdated:
        print("Update:  npx skills update " + " ".join(outdated) + " -g")
    residue = sorted(r[1] for r in results if r[0] == "MISSING")
    if residue:
        print("Clean residue:  npx skills remove " + " ".join(residue) + " -g -y")


# ---------------------------------------------------------------- chain 2

def find_local_sources():
    """{skill-name: source-dir} for every skill folder in the source repo."""
    src_map = {}
    for root, dirs, files in os.walk(SRC_REPO):
        if root.count(os.sep) - str(SRC_REPO).count(os.sep) > 3:
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "tests", "docs", "scripts", "vendor")]
        for d in dirs:
            if (Path(root) / d / "SKILL.md").exists():
                src_map.setdefault(d, Path(root) / d)
    return src_map


def check_local():
    print("== Chain 2: local skills from %s ==" % SRC_REPO)
    if not SRC_REPO.is_dir():
        print("SKIP  no source repo")
        return
    src_map = find_local_sources()
    stale, fresh = [], []
    for name, src in sorted(src_map.items()):
        local_dir, where = installed_dir(name)
        if local_dir is None:
            continue  # source exists but never installed — not our business
        if scan_tree(src, EXCLUDE_FILES_LOCAL) == scan_tree(local_dir, EXCLUDE_FILES_LOCAL):
            fresh.append(name)
        else:
            stale.append((name, str(src).replace(str(HOME), "~")))
    print(f"Up to date: {len(fresh)}")
    print(f"\nSource changed but not reinstalled: {len(stale)}")
    for name, src in stale:
        print(f"  {name}  <-  {src}")
    if stale:
        print("\nReinstall (one per line):")
        for name, src in stale:
            print(f"  npx skills add -g {src} -a pi -y")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("remote", "all"):
        check_remote()
        print()
    if mode in ("local", "all"):
        check_local()


if __name__ == "__main__":
    main()
