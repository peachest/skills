#!/usr/bin/env python3
"""
fetch-article — Universal article fetcher.

Usage:
    python3 fetch.py <URL> [--json] [--text] [--output-dir DIR]

Routes to the right adapter by URL pattern, outputs structured JSON to
stdout or plain text with --text.
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
ADAPTERS_DIR = SCRIPT_DIR / "adapters"
PROJECT_ROOT = SKILL_DIR.parent.parent.parent  # .agent/skills/ → project root

sys.path.insert(0, str(ADAPTERS_DIR))
sys.path.insert(0, str(SCRIPT_DIR))


def classify_url(url: str) -> str:
    """Return adapter name for URL."""
    url_lower = url.lower()
    if "mp.weixin.qq.com" in url_lower:
        return "weixin"
    if "bilibili.com/video" in url_lower or "b23.tv" in url_lower:
        return "bilibili"
    return "generic"


def main():
    parser = argparse.ArgumentParser(description="Universal article fetcher")
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("--json", action="store_true",
                        help="Output structured JSON")
    parser.add_argument("--text", action="store_true",
                        help="Output plain body text only")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: temp)")
    args = parser.parse_args()

    adapter_name = classify_url(args.url)
    output_dir = args.output_dir

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = tempfile.mkdtemp(prefix="fetch-article-")

    # Import adapter by name
    try:
        adapter_module = __import__(adapter_name)
    except ImportError as e:
        print(f"Error loading adapter '{adapter_name}': {e}", file=sys.stderr)
        sys.exit(1)

    if not hasattr(adapter_module, "fetch"):
        print(f"Adapter '{adapter_name}' has no fetch() function",
              file=sys.stderr)
        sys.exit(1)

    result = adapter_module.fetch(args.url, output_dir=output_dir)
    result["source"] = adapter_name

    # Save raw output
    raw_path = os.path.join(output_dir, "article.json")
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    result["raw_path"] = raw_path

    if args.text:
        print(result.get("body_text", "") or "")
    elif args.json:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    else:
        # Default: human-readable
        print(f"标题: {result.get('title', '')}")
        if result.get("author"):
            print(f"作者: {result['author']}")
        if result.get("publish_time"):
            print(f"时间: {result['publish_time']}")
        print("---")
        print(result.get("body_text", "")[:2000])
        if len(result.get("body_text", "")) > 2000:
            print("\n... (truncated, use --json for full output)")


if __name__ == "__main__":
    main()