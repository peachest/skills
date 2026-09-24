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
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR.parent))

import paths  # noqa: E402

TO_MD_PY = SCRIPT_DIR.parent / "to_md.py"


def fetch(url: str, output_dir: str = None) -> dict:
    """
    Fetch a WeChat article via curl, then convert to Markdown with to_md.py.

    Returns dict with title, author, publish_time, body_text (markdown), images.
    """
    if output_dir is None:
        output_dir = paths.default_output_dir("fetch-weixin-")
    else:
        os.makedirs(output_dir, exist_ok=True)

    html_path = os.path.join(output_dir, "article.html")

    # Step 1: curl with Referer header (critical for WeChat).
    # UA matters: a desktop Chrome UA gets a JS-shell page (~17KB, empty body,
    # no rich_media_content). The MicroMessenger UA gets the full server-rendered
    # article directly — no JS execution needed, no captcha trigger.
    print(f"[weixin] Fetching with curl…", file=sys.stderr)
    curl_cmd = [
        "curl", "-sL",
        "-H", "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49",
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

    # Shell-page guard: a real article page carries the content container and
    # the msg_title JS var. Without them the body will convert to empty UI scraps
    # ("视频 小程序 赞 在看 …") — fail loudly instead of returning garbage.
    if "rich_media_content" not in raw and "var msg_title" not in raw:
        return _error(
            "WeChat returned a JS shell page (no rich_media_content / msg_title). "
            "Retry later, or use a headless-browser fetcher for this URL."
        )

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
