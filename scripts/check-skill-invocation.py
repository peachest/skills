#!/usr/bin/env python3
"""Guard: flag skills referenced via `/skill:<name>` that are user-invoke-only.

Rule
----
If a SKILL.md body mentions `/skill:<name>`, the referenced skill should be
model-invokable (i.e. NOT `disable-model-invocation: true`). Otherwise the
model will never fire the handoff on its own — the reference is dead.

This script scans every SKILL.md in the repo, extracts `/skill:<name>`
references from the body (frontmatter excluded), resolves each against the
repo + global skill registries (repo wins on name conflicts), and reports any
reference whose target has `disable-model-invocation: true`.

Self-references (a skill naming itself) are skipped. Router/menu skills that
merely *list* other skills instead of *running* them can be excluded via
`--exclude-referrer` (default: `ask-matt`).

Exit code is 1 if any violation is found, 0 otherwise — safe to wire into CI
or a pre-commit hook.

Usage
-----
    python3 scripts/check-skill-invocation.py
    python3 scripts/check-skill-invocation.py --exclude-referrer ask-matt
    python3 scripts/check-skill-invocation.py --global /path/to/skills
    python3 scripts/check-skill-invocation.py --show-missing   # also list unresolved refs
"""

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GLOBAL = Path(os.environ.get(
    "PI_GLOBAL_SKILLS_DIR",
    str(Path.home() / ".pi" / "agent" / "skills"),
))

REF_PAT = re.compile(r'/skill:([A-Za-z0-9][\w\-]*)')
FM_PAT = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)


# ── frontmatter parsing ───────────────────────────────────────────────

def parse_frontmatter(text: str) -> dict:
    """Extract `name` and `disable-model-invocation` from YAML frontmatter."""
    m = FM_PAT.match(text)
    if not m:
        return {"name": None, "dmi": False}
    fm = m.group(1)
    dmi = False
    mm = re.search(r'disable-model-invocation\s*:\s*(\S+)', fm)
    if mm:
        val = mm.group(1).strip().strip('"').strip("'").lower()
        dmi = val in ("true", "yes", "1")
    name = None
    nm = re.search(r'^name\s*:\s*(.+)$', fm, re.MULTILINE)
    if nm:
        name = nm.group(1).strip().strip('"').strip("'")
    return {"name": name, "dmi": dmi}


# ── skill discovery ───────────────────────────────────────────────────

def discover(root: Path) -> dict:
    """name -> {"path", "dmi"} for every SKILL.md under root."""
    out = {}
    if not root.exists():
        return out
    for sk in root.rglob("SKILL.md"):
        try:
            t = sk.read_text(encoding="utf-8")
        except Exception:
            continue
        fm = parse_frontmatter(t)
        name = fm["name"] or sk.parent.name
        out[name] = {"path": str(sk), "dmi": fm["dmi"]}
    return out


def body_of(text: str) -> str:
    """Return the markdown body with frontmatter stripped."""
    return FM_PAT.sub('', text, count=1)


def skill_name_of(text: str, fallback: str) -> str:
    fm = parse_frontmatter(text)
    return fm["name"] or fallback


# ── main ──────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    show_missing = "--show-missing" in args
    excluded_referrers = set()
    global_dir = DEFAULT_GLOBAL
    positional = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--exclude-referrer":
            excluded_referrers.add(args[i + 1]); i += 2
        elif a == "--global":
            global_dir = Path(args[i + 1]); i += 2
        elif a in ("--show-missing",):
            i += 1
        elif a in ("-h", "--help"):
            print(__doc__); return 0
        else:
            positional.append(a); i += 1
    if not excluded_referrers:
        excluded_referrers = {"ask-matt"}

    repo_skills = discover(REPO_ROOT)
    global_skills = discover(global_dir)
    registry = {**global_skills, **repo_skills}  # repo wins

    print(f"Repo skills:   {len(repo_skills)}  ({REPO_ROOT})")
    print(f"Global skills: {len(global_skills)}  ({global_dir})")
    print(f"Excluded referrers (router skills): {sorted(excluded_referrers)}\n")

    # collect edges: referrer -> referenced
    edges = []  # (referrer_skill, referenced, referrer_path, exists, dmi, ref_path)
    for sk in sorted(REPO_ROOT.rglob("SKILL.md")):
        try:
            t = sk.read_text(encoding="utf-8")
        except Exception:
            continue
        referrer = skill_name_of(t, sk.parent.name)
        if referrer in excluded_referrers:
            continue
        body = body_of(t)
        for ref in sorted(set(REF_PAT.findall(body))):
            if ref == referrer:  # self-reference
                continue
            info = registry.get(ref)
            edges.append({
                "referrer": referrer,
                "referenced": ref,
                "referrer_path": str(sk.relative_to(REPO_ROOT)),
                "exists": info is not None,
                "dmi": info["dmi"] if info else None,
                "ref_path": info["path"] if info else None,
            })

    violations = [e for e in edges if e["exists"] and e["dmi"] is True]
    missing = [e for e in edges if not e["exists"]]

    # group violations by referenced skill
    by_target = defaultdict(list)
    for e in violations:
        by_target[e["referenced"]].append(e)

    print(f"=== VIOLATIONS: {len(violations)} edge(s), {len(by_target)} user-invoke-only skill(s) referenced ===\n")
    for name in sorted(by_target):
        info = registry[name]
        rel = info["path"].replace(str(REPO_ROOT) + "/", "")
        referrers = sorted({e["referrer"] for e in by_target[name]})
        print(f"  /skill:{name}")
        print(f"    target:  {rel}")
        print(f"    dmi=True, referenced by: {referrers}")
        print()

    if show_missing and missing:
        print(f"=== MISSING (referenced skill not found): {len(missing)} ===\n")
        by_missing = defaultdict(list)
        for e in missing:
            by_missing[e["referenced"]].append(e["referrer"])
        for name in sorted(by_missing):
            print(f"  /skill:{name}  <- {sorted(set(by_missing[name]))}")
        print()

    # summary
    ok = len([e for e in edges if e["exists"] and e["dmi"] is False])
    print(f"Summary: {ok} ok, {len(violations)} violations, {len(missing)} missing")
    if violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
