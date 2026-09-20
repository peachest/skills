#!/usr/bin/env python3
"""okb-index-regen — regenerate index.md from the tree; optionally check links.

Scans bronze/silver/gold, reports layer distribution + per-topic note lists,
and carries `ingests_since_status` counters forward from the existing index.md
(regen never resets them — Status's trigger depends on them).

--check-links verifies every silver body Markdown hyperlink (./x.md or
../<topic>/x.md) and every sources[].resource path; exits 1 on broken links.
"""
import argparse
import re
import sys
from pathlib import Path

from _okbutil import body_links, read_frontmatter

LAYERS = ("bronze", "silver", "gold")


def collect(root: Path):
    """{layer: {topic: [note paths]}}"""
    tree = {l: {} for l in LAYERS}
    for layer in LAYERS:
        ldir = root / layer
        if not ldir.is_dir():
            continue
        for topic_dir in sorted(p for p in ldir.iterdir() if p.is_dir()):
            tree[layer][topic_dir.name] = sorted(topic_dir.glob("*.md"))
    return tree


def carried_counters(root: Path):
    counters = {}
    idx = root / "index.md"
    if idx.exists():
        for m in re.finditer(r"ingests_since_status:\s*(\d+)", idx.read_text(encoding="utf-8")):
            # associate with the nearest preceding topic heading
            before = idx.read_text(encoding="utf-8")[: m.start()]
            topics = re.findall(r"^##\s+(.+)$", before, re.M)
            if topics:
                counters[topics[-1].strip()] = int(m.group(1))
    return counters


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--check-links", action="store_true")
    a = p.parse_args()
    root = Path(a.root)
    tree = collect(root)

    lines = ["# OKB index", ""]
    total = {l: sum(len(v) for v in tree[l].values()) for l in LAYERS}
    lines += [
        "## Layer distribution",
        "",
        f"- bronze: {total['bronze']} notes (only fidelity layer)",
        f"- silver: {total['silver']} notes (only rewrite layer)",
        f"- gold: {total['gold']} verification overlays",
        "",
    ]
    counters = carried_counters(root)
    topics = sorted(set(tree["bronze"]) | set(tree["silver"]) | set(tree["gold"]))
    for t in topics:
        lines.append(f"## {t}")
        lines.append("")
        for l in LAYERS:
            for note in tree[l].get(t, []):
                fm = read_frontmatter(note)
                label = fm.get("title") or note.stem
                extra = f" [{fm.get('status', '?')}]" if l != "bronze" else ""
                lines.append(f"- {l}/{note.name} — {label}{extra}")
        n = counters.get(t, 0)
        lines += ["", f"ingests_since_status: {n}", ""]
    (root / "index.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"index.md regenerated: {root/'index.md'}")

    if not a.check_links:
        return
    broken = []
    for topic, notes in tree["silver"].items():
        for note in notes:
            for link in body_links(note):
                if not (note.parent / link).resolve().exists():
                    broken.append(f"{note.name} -> {link}")
            fm = read_frontmatter(note)
            for res in re.findall(r"resource:\s*(\S+)", open(note, encoding="utf-8").read()):
                if not (note.parent / res).resolve().exists():
                    broken.append(f"{note.name} source-edge -> {res}")
    if broken:
        print("broken links:")
        for b in broken:
            print(f"  {b}")
        sys.exit(1)
    print("links: all reachable")


if __name__ == "__main__":
    main()
