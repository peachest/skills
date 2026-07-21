#!/usr/bin/env python3
"""
WeChat article adapter.

Strategy: curl + Referer header → save HTML → to_md.py (markitdown).
Does NOT execute JavaScript, which avoids WeChat's anti-bot captcha.

Usage (called by fetch.py, not directly):
    python3 -c "from adapters.weixin import fetch; print(fetch('https://mp.weixin.qq.com/s/xxx'))"
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
TO_MD_PY = SCRIPT_DIR.parent / "to_md.py"


def fetch(url: str, output_dir: str = None) -> dict:
    """
    Fetch a WeChat article via curl, then convert to Markdown with to_md.py.

    Returns dict with title, author, publish_time, body_text (markdown), images.
    """
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="fetch-weixin-")
    else:
        os.makedirs(output_dir, exist_ok=True)

    html_path = os.path.join(output_dir, "article.html")

    # Step 1: curl with Referer header (critical for WeChat)
    print(f"[weixin] Fetching with curl…", file=sys.stderr)
    curl_cmd = [
        "curl", "-sL",
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "-H", "Referer: https://mp.weixin.qq.com/",
        "-o", html_path,
        url,
    ]
    result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)

    if result.returncode != 0:
        return _error(f"curl failed: {result.stderr[:500]}")

    # Check for captcha page
    with open(html_path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    if "wappoc_appmsgcaptcha" in raw or "环境异常" in raw:
        return _error("WeChat captcha page returned. IP may be blocked or rate-limited.")

    # Step 2: Convert to Markdown via to_md.py
    if not TO_MD_PY.exists():
        return _error(f"to_md.py not found at {TO_MD_PY}")

    print(f"[weixin] Converting to Markdown…", file=sys.stderr)
    convert_cmd = [
        sys.executable, str(TO_MD_PY),
        html_path,
        "--images",
        "--output-dir", output_dir,
    ]
    convert_result = subprocess.run(
        convert_cmd, capture_output=True, text=True, timeout=30
    )

    if convert_result.returncode != 0:
        return _error(f"to_md.py failed: {convert_result.stderr[:500]}")

    try:
        data = json.loads(convert_result.stdout)
    except json.JSONDecodeError as e:
        return _error(f"to_md.py output parse error: {e}")

    return {
        "title": data.get("title", ""),
        "author": data.get("author", ""),
        "publish_time": data.get("publish_time", ""),
        "body_text": data.get("body_text", ""),
        "images": data.get("images", []),
        "md_path": data.get("md_path", ""),
    }


def _error(msg: str) -> dict:
    return {
        "error": msg,
        "title": "",
        "author": "",
        "publish_time": "",
        "body_text": "",
        "images": [],
    }
