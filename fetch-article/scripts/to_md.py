#!/usr/bin/env python3
"""Convert HTML file to Markdown with metadata extraction.

Usage:
    python3 to_md.py <html_file> [--images] [--output-dir DIR]

Uses markitdown CLI for body conversion, plus bs4 for metadata (title,
author, publish_time). Outputs structured JSON to stdout.

Output keys:
    title, author, publish_time, body_text (markdown), images, md_path
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("bs4 not installed, metadata extraction limited", file=sys.stderr)
    BeautifulSoup = None


def extract_metadata(html: str) -> dict:
    """Extract title, author, publish_time from HTML."""
    meta = {"title": "", "author": "", "publish_time": ""}

    if BeautifulSoup:
        soup = BeautifulSoup(html, "html.parser")

        # Title: og:title first, then h1.rich_media_title
        og = soup.find("meta", property="og:title")
        if og and og.get("content"):
            meta["title"] = og["content"].strip()
        if not meta["title"]:
            h1 = soup.find("h1", class_=re.compile(r"rich_media_title"))
            if h1:
                meta["title"] = h1.get_text(strip=True)

        # Author: og:article:author first, then #js_name
        og = soup.find("meta", property="og:article:author")
        if og and og.get("content"):
            meta["author"] = og["content"].strip()
        if not meta["author"]:
            el = soup.find(id="js_name")
            if el:
                meta["author"] = el.get_text(strip=True)

        # Publish time
        el = soup.find(id="publish_time")
        if not el:
            el = soup.find(id="meta_content")
        if el:
            meta["publish_time"] = el.get_text(strip=True)
    else:
        # Fallback: regex
        if not meta["title"]:
            m = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"', html)
            if m:
                meta["title"] = m.group(1)
        if not meta["author"]:
            m = re.search(r'<meta\s+property="og:article:author"\s+content="([^"]+)"', html)
            if m:
                meta["author"] = m.group(1)
        if not meta["author"]:
            m = re.search(r'id="js_name"[^>]*>([^<]+)', html)
            if m:
                meta["author"] = m.group(1).strip()
        if not meta["publish_time"]:
            m = re.search(r'id="publish_time"[^>]*>([^<]+)', html)
            if not m:
                m = re.search(r'id="meta_content"[^>]*>([^<]+)', html)
            if m:
                meta["publish_time"] = m.group(1).strip()

    return meta


def extract_images(html: str) -> list:
    """Extract image URLs from HTML."""
    images = []
    if BeautifulSoup:
        soup = BeautifulSoup(html, "html.parser")
        for img in soup.find_all("img"):
            src = img.get("data-src") or img.get("src") or ""
            if src:
                images.append(src)
    else:
        images = re.findall(r'<img[^>]+data-src="([^"]+)"', html)
        if not images:
            images = re.findall(r'<img[^>]+src="([^"]+)"', html)
    return images


def main():
    parser = argparse.ArgumentParser(description="HTML to Markdown converter")
    parser.add_argument("html_file", help="Path to input HTML file")
    parser.add_argument("--images", action="store_true",
                        help="Include image URLs in output")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: input file dir)")
    args = parser.parse_args()

    html_path = Path(args.html_file).resolve()
    if not html_path.exists():
        print(f"File not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir or html_path.parent).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_html = html_path.read_text(encoding="utf-8", errors="replace")

    # Step 1: extract metadata
    meta = extract_metadata(raw_html)
    images = extract_images(raw_html) if args.images else []

    # Step 2: convert to markdown via markitdown CLI
    md_path = output_dir / "article.md"
    markitdown_cmd = ["markitdown", str(html_path)]
    result = subprocess.run(
        markitdown_cmd,
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode == 0:
        md_content = result.stdout
    else:
        # Fallback: strip HTML tags
        import html as html_mod
        text = re.sub(r'<[^>]+>', "", raw_html)
        text = html_mod.unescape(text)
        text = re.sub(r'[ \t]+', " ", text)
        text = re.sub(r'\n\s*\n+', "\n\n", text)
        md_content = text.strip()

    md_path.write_text(md_content, encoding="utf-8")

    # Output
    output = {
        "title": meta["title"],
        "author": meta["author"],
        "publish_time": meta["publish_time"],
        "body_text": md_content,
        "md_path": str(md_path),
    }
    if args.images:
        output["images"] = images

    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()