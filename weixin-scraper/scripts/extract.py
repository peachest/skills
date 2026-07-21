#!/usr/bin/env python3
"""Extract WeChat public account article content from saved HTML.

Usage:
    python3 extract.py <html_file> [--json] [--images]

Outputs title, account name, publish date, and body text.
Use --json for machine-readable JSON output.
Use --images to include a list of image URLs.
"""

import re
import sys
import json
import html as html_mod
from pathlib import Path


def extract(filepath: str, include_images: bool = False) -> dict:
    raw = Path(filepath).read_text(encoding="utf-8", errors="replace")

    # --- Metadata ---
    title = _meta(raw, "og:title")
    author = _meta(raw, "og:article:author")
    description = _meta(raw, "og:description")
    url = _meta(raw, "og:url")

    # Fallback: try page-level selectors if og: tags are missing
    if not title:
        title = _text_in_selector(raw, r'<h1[^>]*class="[^"]*rich_media_title[^"]*"[^>]*>([^<]+)')
    if not author:
        author = _text_in_selector(raw, r'id="js_name"[^>]*>([^<]+)')

    # Publish date
    pub_time = _text_in_selector(raw, r'id="publish_time"[^>]*>([^<]+)')
    if not pub_time:
        pub_time = _text_in_selector(raw, r'id="meta_content"[^>]*>([^<]+)')

    # --- Body ---
    body_match = re.search(
        r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script',
        raw, re.DOTALL
    )
    body_text = ""
    images = []

    if body_match:
        content = body_match.group(1)
        if include_images:
            images = re.findall(r'<img[^>]+data-src="([^"]+)"', content)
            if not images:
                images = re.findall(r'<img[^>]+src="([^"]+)"', content)
        # Strip tags
        text = re.sub(r'<[^>]+>', '', content)
        text = html_mod.unescape(text)
        # Collapse whitespace
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        body_text = text.strip()

    result = {
        "title": title or "",
        "author": author or "",
        "description": description or "",
        "url": url or "",
        "publish_time": pub_time or "",
        "body": body_text,
    }
    if include_images:
        result["images"] = images

    return result


def _meta(html: str, prop: str) -> str:
    m = re.search(rf'<meta\s+property="{prop}"\s+content="([^"]+)"', html)
    return m.group(1) if m else ""


def _text_in_selector(html: str, pattern: str) -> str:
    m = re.search(pattern, html)
    return m.group(1).strip() if m else ""


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract.py <html_file> [--json] [--images]")
        sys.exit(1)

    filepath = sys.argv[1]
    as_json = "--json" in sys.argv
    include_images = "--images" in sys.argv

    result = extract(filepath, include_images=include_images)

    if as_json:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    else:
        print(f"标题: {result['title']}")
        if result['author']:
            print(f"公众号: {result['author']}")
        if result['publish_time']:
            print(f"发布时间: {result['publish_time']}")
        if result['description']:
            print(f"摘要: {result['description']}")
        if result['url']:
            print(f"链接: {result['url']}")
        print("---")
        print(result['body'])
        if include_images and result.get('images'):
            print("\n--- 图片 ---")
            for img in result['images']:
                print(img)


if __name__ == "__main__":
    main()
