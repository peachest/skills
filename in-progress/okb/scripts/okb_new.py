#!/usr/bin/env python3
"""okb-new — create a silver/gold skeleton note with contract-legal frontmatter.

Silver always starts `status: draft` with empty `verified`; only factcheck
writes stable/verified (P-002 gate). Gold is an overlay skeleton, no body.
"""
import argparse
import sys
from pathlib import Path

from _okbutil import now_iso


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--layer", required=True, choices=["silver", "gold"])
    p.add_argument("--topic", required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--title")
    p.add_argument("--description", help="one-line factual summary, <=40 chars")
    p.add_argument("--type", default="concept", choices=["concept", "reference"])
    p.add_argument("--stale-after", help="ISO 8601; e.g. evergreen ~12mo, fast-moving 1-3mo")
    p.add_argument("--force", action="store_true")
    a = p.parse_args()

    out = Path(a.root) / a.layer / a.topic / f"{a.slug}.md"
    if out.exists() and not a.force:
        sys.exit(f"error: {out} exists (use --force to overwrite)")
    out.parent.mkdir(parents=True, exist_ok=True)

    if a.layer == "silver":
        fm = (
            "---\n"
            f"type: {a.type}\n"
            f"title: {a.title or a.slug}\n"
            f"description: {a.description or ''}\n"
            "tags: []\n"
            "status: draft            # only factcheck (or user confirmation) promotes to stable\n"
            f"generated: {{ by: process:okb-new, at: {now_iso()} }}\n"
            f"updated: {now_iso()}\n"
            "conflicts_with: []\n"
            "verified: []\n"
            f"stale_after: {a.stale_after or ''}\n"
            "sources: []\n"
            "---\n\n"
            f"# {a.title or a.slug}\n\n"
        )
    else:
        fm = (
            "---\n"
            "status: stable\n"
            "verified: []             # append events: { by, at, method }; evidence cites bronze content\n"
            "verdicts: []\n"
            "sources: []              # resource points at the silver note\n"
            "---\n"
        )
    out.write_text(fm, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
