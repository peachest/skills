#!/usr/bin/env python3
"""
Zhihu zhuanlan article adapter.

Strategy: node + playwright Chromium with injected login cookies, NO proxy
env (the corporate proxy fails to reach zhihu). Zhihu blocks non-browser
TLS fingerprints (curl → 403) and cookie-less browsers ({"code":40362}),
so a real browser + login cookie is the only working path.

Requirements:
- node on PATH
- a playwright install dir with node_modules/playwright (default
  ~/tools/playwright-runner, override ZHIHU_PLAYWRIGHT_RUNNER)
- cookie file ~/tmp/zhihu-cookies.txt ("name=value; name=value" string,
  needs z_c0 / d_c0 / __zse_ck), override ZHIHU_COOKIE_FILE
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
TO_MD_PY = SCRIPT_DIR.parent / "to_md.py"
FETCH_MJS = SCRIPT_DIR / "zhihu_fetch.mjs"

_PROXY_KEYS = {"http_proxy", "https_proxy", "all_proxy", "ftp_proxy", "no_proxy"}


def fetch(url: str, output_dir: str | None = None) -> dict:
    """Fetch a zhuanlan.zhihu.com article; returns dict with title/author/publish_time/body_text/images."""
    m = re.search(r"zhuanlan\.zhihu\.com/p/(\d+)", url)
    if not m:
        return _error(f"only zhuanlan.zhihu.com/p/<id> URLs supported, got: {url}")
    article_id = m.group(1)

    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="fetch-zhihu-")
    else:
        os.makedirs(output_dir, exist_ok=True)

    cookie_file = Path(os.environ.get("ZHIHU_COOKIE_FILE", Path.home() / "tmp/zhihu-cookies.txt"))
    if not cookie_file.exists():
        return _error(
            f"zhihu cookie file not found: {cookie_file}. "
            "Ask the user for their logged-in cookie string (z_c0, d_c0, __zse_ck) and save it there."
        )

    runner_dir = Path(os.environ.get("ZHIHU_PLAYWRIGHT_RUNNER", Path.home() / "tools/playwright-runner"))
    if not (runner_dir / "node_modules/playwright").exists():
        return _error(
            f"playwright not found under {runner_dir}. Install per the skill's runtime notes: "
            "mkdir the dir, `npm install playwright`, `npx playwright install chromium`."
        )

    # Critical: strip proxy env — corporate proxy cannot tunnel to zhihu.
    env = {k: v for k, v in os.environ.items() if k.lower() not in _PROXY_KEYS}
    env["ZHIHU_COOKIE_FILE"] = str(cookie_file)
    env["ZHIHU_RUNNER_DIR"] = str(runner_dir)
    env["ZHIHU_ARTICLE_ID"] = article_id

    print("[zhihu] Fetching with playwright + cookies…", file=sys.stderr)
    result = subprocess.run(
        ["node", str(FETCH_MJS)],
        capture_output=True, text=True, timeout=90, env=env,
    )
    try:
        data = json.loads(result.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return _error(f"zhihu_fetch.mjs produced no JSON: {(result.stderr or result.stdout)[:500]}")
    if data.get("error"):
        return _error(data["error"])

    html_path = os.path.join(output_dir, "article.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(data["html"])

    print("[zhihu] Converting to Markdown…", file=sys.stderr)
    convert = subprocess.run(
        [sys.executable, str(TO_MD_PY), html_path, "--images", "--output-dir", output_dir],
        capture_output=True, text=True, timeout=30,
    )
    if convert.returncode != 0:
        return _error(f"to_md.py failed: {convert.stderr[:500]}")
    try:
        md = json.loads(convert.stdout)
    except json.JSONDecodeError as e:
        return _error(f"to_md.py output parse error: {e}")

    return {
        "title": data["title"],
        "author": data["author"],
        "publish_time": data["publish_time"],
        "body_text": md.get("body_text", ""),
        "images": md.get("images", []),
        "md_path": md.get("md_path", ""),
        "http_status": data.get("http_status", 0),
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
