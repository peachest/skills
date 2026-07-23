#!/usr/bin/env python3
"""Rewrite mattpocock skill references: /<name> -> /skill:<name>.

Idempotent — safe to run repeatedly.  Derives skill names from the directory
structure (any folder containing SKILL.md), so it auto-adapts when upstream
adds new skills.

Usage:
    python3 scripts/rewrite-skill-refs.py               # default target
    python3 scripts/rewrite-skill-refs.py --dry-run      # preview, no writes
    python3 scripts/rewrite-skill-refs.py <dir>          # custom target
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGET = REPO_ROOT / "vendor" / "mattpocock"


# ── skill name discovery ──────────────────────────────────────────────

def get_skill_names(target: Path) -> list[str]:
    """Collect every directory name that contains a SKILL.md."""
    names = {sk.parent.name for sk in target.rglob("SKILL.md")}
    # longest first — harmless with boundary-anchored regex, but cheap insurance
    return sorted(names, key=len, reverse=True)


# ── regex engine ──────────────────────────────────────────────────────

def build_pattern(skill_name: str) -> re.Pattern:
    """Match /<name> as a skill ref, not a URL or file path.

    Lookbehind: the '/' must NOT be preceded by
        :  (URL scheme   — https://)
        \w (word char    — token/URL/path segment)
        .  (relative path — ./foo)
        /  (nested path  — a/b/c)
        -  (hyphenated prefix)

    Lookahead: <name> must NOT be followed by
        \w or -  (would be a longer identifier)
    """
    return re.compile(
        r'(?<![:\w./\-])/' + re.escape(skill_name) + r'(?![\w\-])'
    )


def rewrite_text(text: str, skill_names: list[str]) -> tuple[str, int]:
    count = 0
    for name in skill_names:
        pat = build_pattern(name)

        def repl(_m, _name=name):
            nonlocal count
            count += 1
            return '/skill:' + _name

        text = pat.sub(repl, text)
    return text, count


# ── main ──────────────────────────────────────────────────────────────

def main():
    dry_run = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    target = Path(args[0]).resolve() if args else DEFAULT_TARGET

    if not target.exists():
        print(f"Error: {target} does not exist", file=sys.stderr)
        sys.exit(1)

    skill_names = get_skill_names(target)
    print(f"Discovered {len(skill_names)} skills:")
    print(f"  {', '.join(sorted(skill_names))}\n")

    total_files, total_reps = 0, 0
    for md in sorted(target.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        new_text, n = rewrite_text(text, skill_names)
        if n > 0:
            rel = md.relative_to(target)
            print(f"  {rel}: {n}")
            total_files += 1
            total_reps += n
            if not dry_run:
                md.write_text(new_text, encoding="utf-8")

    tag = "[dry-run] " if dry_run else ""
    print(f"\n{tag}{total_reps} replacements in {total_files} files")


if __name__ == "__main__":
    main()
