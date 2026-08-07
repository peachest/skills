#!/usr/bin/env python3
"""
Generic webpage adapter.

Strategy: Try Scrapling CLI first, fall back to curl + HTML tag stripping.

Requires:
  pip install "scrapling[all]"
  scrapling install

Usage (called by fetch.py, not directly):
    python3 -c "from adapters.generic import fetch; print(fetch('https://example.com'))"
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import html as html_mod
from pathlib import Path


def fetch(url: str, output_dir: str = None) -> dict:
    """
    Fetch a generic webpage.

    Tries Scrapling CLI first. If Scrapling is not installed or fails,
    falls back to curl + HTML tag stripping.
    """
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="fetch-generic-")
    else:
        os.makedirs(output_dir, exist_ok=True)

    # Try Scrapling first
    result = _try_scrapling(url, output_dir)
    if result is not None:
        return result

    # Fallback: curl
    print(f"[generic] Scrapling unavailable, falling back to curl…",
          file=sys.stderr)
    result = _try_curl(url, output_dir)
    if result is not None:
        return result

    return {
        "error": "All fetch methods failed",
        "title": "",
        "author": "",
        "publish_time": "",
        "body_text": "",
        "images": [],
    }


def _try_scrapling(url: str, output_dir: str) -> dict | None:
    """Try scrapling extract get URL. Returns None if unavailable/fails."""
    # Check if scrapling is installed
    check = subprocess.run(
        ["python3", "-c", "import scrapling; print('ok')"],
        capture_output=True, text=True, timeout=5
    )
    if check.returncode != 0:
        print(f"[generic] Scrapling not installed", file=sys.stderr)
        return None

    md_path = os.path.join(output_dir, "content.md")

    try:
        result = subprocess.run(
            ["scrapling", "extract", "get", url, md_path],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0 and os.path.exists(md_path):
            with open(md_path, "r", encoding="utf-8", errors="replace") as f:
                body_text = f.read().strip()
            if body_text:
                print(f"[generic] Scrapling succeeded ({len(body_text)} chars)",
                      file=sys.stderr)
                return {
                    "title": _extract_title_from_md(body_text),
                    "author": "",
                    "publish_time": "",
                    "body_text": body_text,
                    "images": [],
                }
    except Exception as e:
        print(f"[generic] Scrapling error: {e}", file=sys.stderr)

    return None


def _try_curl(url: str, output_dir: str) -> dict | None:
    """Fallback: curl + HTML tag stripping."""
    html_path = os.path.join(output_dir, "page.html")

    try:
        result = subprocess.run(
            ["curl", "-sL",
             "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
             "-o", html_path,
             url],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print(f"[generic] curl failed: {result.stderr[:200]}",
                  file=sys.stderr)
            return None

        with open(html_path, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read()

        # Extract title
        title = ""
        title_m = re.search(r'<title[^>]*>([^<]+)</title>', raw, re.IGNORECASE)
        if title_m:
            title = html_mod.unescape(title_m.group(1).strip())

        # Extract body text
        body_match = re.search(
            r'<body[^>]*>(.*)</body>', raw, re.DOTALL | re.IGNORECASE
        )
        body_html = body_match.group(1) if body_match else raw
        text = re.sub(r'<script[^>]*>.*?</script>', '', body_html,
                      flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text,
                      flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = html_mod.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'\n\s*\n+', '\n\n', text)

        print(f"[generic] curl succeeded ({len(text)} chars)",
              file=sys.stderr)
        return {
            "title": title,
            "author": "",
            "publish_time": "",
            "body_text": text,
            "images": [],
        }

    except Exception as e:
        print(f"[generic] curl error: {e}", file=sys.stderr)

    return None


def _extract_title_from_md(md_text: str) -> str:
    """Extract first # heading from markdown text."""
    lines = md_text.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
        if line.startswith("## "):
            return line[3:].strip()
    return ""