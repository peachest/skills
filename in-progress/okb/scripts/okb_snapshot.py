#!/usr/bin/env python3
"""okb-snapshot — fetch a source and write a bronze snapshot (P-001 sediment).

Usage:
  okb_snapshot.py --root OKB --topic T <arxiv-id | https-url>
  okb_snapshot.py --root OKB --topic T --from-file F --title T2 [--author A] [--source-url U]

arXiv input: fetches metadata via the export API; body = abstract, with a
fidelity warning printed when the paper's core claims likely live in the body.
Non-arXiv URL: use the fetch-article skill, then pass the saved markdown via
--from-file (verbatim content is the bronze body; sha256 hashes it).
"""
import argparse
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from _okbutil import now_iso, read_frontmatter, sha256_text, slugify

NS = {"a": "http://www.w3.org/2005/Atom"}


def fetch_arxiv(arxiv_id: str) -> dict:
    api = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"
    with urllib.request.urlopen(api, timeout=30) as r:
        root = ET.fromstring(r.read())
    entry = root.find("a:entry", NS)
    if entry is None:
        sys.exit(f"error: arXiv returned no entry for {arxiv_id}")
    return {
        "source": f"https://arxiv.org/abs/{arxiv_id}",
        "title": "".join(entry.find("a:title", NS).itertext()).strip(),
        "author": "; ".join(a.find("a:name", NS).text for a in entry.findall("a:author", NS)) or "unknown",
        "body": "".join(entry.find("a:summary", NS).itertext()).strip(),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True, help="okb root dir")
    p.add_argument("--topic", required=True)
    p.add_argument("source", nargs="?", help="arXiv id or https URL")
    p.add_argument("--from-file", help="verbatim markdown fetched elsewhere (fetch-article)")
    p.add_argument("--title", help="label (required with --from-file)")
    p.add_argument("--author", default="unknown")
    p.add_argument("--source-url", help="original URL when body came from --from-file")
    a = p.parse_args()

    if a.from_file:
        if not a.title:
            sys.exit("error: --from-file requires --title")
        body = Path(a.from_file).read_text(encoding="utf-8")
        meta = {"source": a.source_url or "local-file", "title": a.title, "author": a.author, "body": body}
        fidelity_note = ""
    else:
        if not a.source:
            sys.exit("error: provide an arXiv id/URL or --from-file")
        src = a.source
        if src.startswith("http") and "arxiv.org/abs/" in src:
            src = src.rsplit("/", 1)[-1]
        if not src.replace("v", "", 1).replace(".", "", 1).replace("_", "", 1).isalnum():
            sys.exit(f"error: {a.source} is not an arXiv id/abs-URL; use fetch-article + --from-file")
        meta = fetch_arxiv(src)
        fidelity_note = (
            "warning: bronze body is the arXiv ABSTRACT only. If distill will claim "
            "results that live in the paper body (algorithms, theorems, tables), fetch "
            "the full text and re-snapshot with --from-file — factcheck evidence must "
            "reach the origin (P-003).\n"
        )

    topic_dir = Path(a.root) / "bronze" / a.topic
    topic_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(meta["title"])
    out = topic_dir / f"{slug}.md"

    # dedup: same content hash already snapshotted in this topic?
    digest = sha256_text(meta["body"])
    for existing in topic_dir.glob("*.md"):
        if read_frontmatter(existing).get("sha256") == digest:
            print(f"skip: identical content already snapshotted: {existing}")
            return

    fm = (
        f"---\nsource: {meta['source']}\ntitle: {meta['title']}\n"
        f"author: {meta['author']}\nfetched_at: {now_iso()}\nsha256: {digest}\n---\n\n"
    )
    out.write_text(fm + meta["body"] + "\n", encoding="utf-8")
    print(fidelity_note, end="")
    print(f"bronze: {out}")


if __name__ == "__main__":
    main()
