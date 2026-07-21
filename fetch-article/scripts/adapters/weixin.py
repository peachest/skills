#!/usr/bin/env python3
"""
WeChat article adapter.

Strategy: curl + Referer header → save HTML → weixin-scraper extract.py.
Does NOT execute JavaScript, which avoids WeChat's anti-bot captcha.

Usage (called by fetch.py, not directly):
    python3 -c "from adapters.weixin import fetch; print(fetch('https://mp.weixin.qq.com/s/xxx'))"
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent.parent
PROJECT_ROOT = SKILL_DIR.parent.parent.parent

# weixin-scraper's extract.py
EXTRACT_PY = PROJECT_ROOT / ".agent" / "skills" / "weixin-scraper" / "scripts" / "extract.py"


def fetch(url: str, output_dir: str = None) -> dict:
    """
    Fetch a WeChat article via curl, then extract with extract.py.
    
    Returns dict with title, author, publish_time, body_text, images.
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
        return {
            "error": f"curl failed: {result.stderr[:500]}",
            "title": "",
            "author": "",
            "publish_time": "",
            "body_text": "",
            "images": [],
        }

    # Check for captcha page
    with open(html_path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    if "wappoc_appmsgcaptcha" in raw or "环境异常" in raw:
        # Curl hit captcha — rare but possible (IP-blocked)
        return {
            "error": "WeChat captcha page returned. IP may be blocked or rate-limited.",
            "title": "",
            "author": "",
            "publish_time": "",
            "body_text": "",
            "images": [],
        }

    # Step 2: Run extract.py
    if not EXTRACT_PY.exists():
        return {
            "error": f"extract.py not found at {EXTRACT_PY}",
            "title": "",
            "author": "",
            "publish_time": "",
            "body_text": "",
            "images": [],
        }

    print(f"[weixin] Extracting with {EXTRACT_PY}…", file=sys.stderr)
    extract_cmd = [
        sys.executable, str(EXTRACT_PY),
        html_path,
        "--json", "--images",
    ]
    extract_result = subprocess.run(
        extract_cmd, capture_output=True, text=True, timeout=15
    )

    if extract_result.returncode != 0:
        return {
            "error": f"extract.py failed: {extract_result.stderr[:500]}",
            "title": "",
            "author": "",
            "publish_time": "",
            "body_text": "",
            "images": [],
        }

    try:
        data = json.loads(extract_result.stdout)
    except json.JSONDecodeError as e:
        return {
            "error": f"extract.py output parse error: {e}",
            "title": "",
            "author": "",
            "publish_time": "",
            "body_text": "",
            "images": [],
        }

    # Ensure keys exist
    return {
        "title": data.get("title", ""),
        "author": data.get("author", ""),
        "publish_time": data.get("publish_time", ""),
        "body_text": data.get("body", ""),
        "images": data.get("images", []),
    }