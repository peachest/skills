#!/usr/bin/env python3
"""
Generic webpage adapter.

Strategy: Try Scrapling CLI first, then curl + HTML tag stripping,
then r.jina.ai reader proxy (bypasses Cloudflare-protected sites
where direct curl only gets a JS-challenge shell page).

Requires:
  pip install "scrapling[all]"
  scrapling install
  (r.jina.ai needs no install — it is a network fallback, but may
  rate-limit without a JINA_API_KEY.)

Usage (called by fetch.py, not directly):
    python3 -c "from adapters.generic import fetch; print(fetch('https://example.com'))"
"""

import json
import os
import re
import subprocess
import sys
import html as html_mod
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

import paths  # noqa: E402

# Markers of an anti-bot challenge page (Cloudflare & friends) that curl
# cannot solve. When one appears in the fetched HTML, treat the fetch as
# failed so the next fallback layer (r.jina.ai) gets a chance.
_CF_MARKERS = (
    "Enable JavaScript and cookies to continue",
    "Just a moment...",
    "Attention Required",
    "challenge-platform",
    "cf-browser-verification",
)


def fetch(url: str, output_dir: str = None) -> dict:
    """
    Fetch a generic webpage.

    Tries Scrapling first, then curl, then r.jina.ai reader proxy.
    Returns the first non-None result.
    """
    if output_dir is None:
        output_dir = paths.default_output_dir("fetch-generic-")
    else:
        os.makedirs(output_dir, exist_ok=True)

    # Try Scrapling first
    result = _try_scrapling(url, output_dir)
    if result is not None:
        return result

    # Fallback 1: curl direct
    print(f"[generic] Scrapling unavailable, falling back to curl…",
          file=sys.stderr)
    result = _try_curl(url, output_dir)
    if result is not None:
        return result

    # Fallback 2: r.jina.ai reader proxy (Cloudflare bypass)
    print(f"[generic] curl direct failed/challenge page, trying r.jina.ai…",
          file=sys.stderr)
    result = _try_jina(url, output_dir)
    if result is not None:
        return result

    return {
        "error": "All fetch methods failed (scrapling, curl, r.jina.ai)",
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

        # Anti-bot challenge shell? Then the stripped text would be garbage —
        # fail this layer so r.jina.ai gets a chance.
        for marker in _CF_MARKERS:
            if marker in raw:
                print(f"[generic] curl got challenge page ({marker!r})",
                      file=sys.stderr)
                return None

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


def _try_jina(url: str, output_dir: str) -> dict | None:
    """Last-resort fallback: r.jina.ai reader proxy.

    Effective against Cloudflare-protected sites where direct curl only
    returns a JS-challenge shell. Output format:
      Title: …\nURL Source: …\nMarkdown Content:\n<body markdown>
    """
    md_path = os.path.join(output_dir, "jina.md")

    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "90",
             "-o", md_path,
             f"https://r.jina.ai/{url}"],
            capture_output=True, text=True, timeout=100,
        )
        if result.returncode != 0 or not os.path.exists(md_path):
            print(f"[generic] r.jina.ai curl failed: {result.stderr[:200]}",
                  file=sys.stderr)
            return None

        with open(md_path, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read()

        title, body = _parse_jina(raw)
        if len(body) < 30:
            print(f"[generic] r.jina.ai returned empty/too-short body "
                  f"({len(body)} chars)", file=sys.stderr)
            return None

        print(f"[generic] r.jina.ai succeeded ({len(body)} chars)",
              file=sys.stderr)
        return {
            "title": title,
            "author": "",
            "publish_time": "",
            "body_text": body,
            "images": [],
        }

    except Exception as e:
        print(f"[generic] r.jina.ai error: {e}", file=sys.stderr)

    return None


def _parse_jina(raw: str) -> tuple[str, str]:
    """Parse r.jina.ai reader output into (title, markdown body)."""
    title = ""
    title_m = re.search(r"^Title:\s*(.*)$", raw, re.MULTILINE)
    if title_m:
        title = html_mod.unescape(title_m.group(1).strip())

    if "Markdown Content:" in raw:
        body = raw.split("Markdown Content:", 1)[1].strip()
    else:
        body = raw.strip()
    return title, body