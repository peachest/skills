#!/usr/bin/env python3
"""
Bilibili video audio downloader adapter.

Downloads audio via WBI-signed API. Does NOT transcribe.
If CC subtitles are available, saves them directly.

Usage (called by fetch.py, not directly):
    python3 -c "from adapters.bilibili import fetch; print(fetch('https://www.bilibili.com/video/BV1xx/'))"
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import time
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

MIXIN_KEY_ENC_TAB = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35,
    27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
    37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4,
    22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52,
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/",
    "Origin": "https://www.bilibili.com",
}


def _get_mixin_key(raw_key: bytes) -> str:
    return "".join(chr(raw_key[i]) for i in MIXIN_KEY_ENC_TAB)


def _wbi_sign(params: dict, img_key: str, sub_key: str) -> dict:
    mixin_key = _get_mixin_key((img_key + sub_key).encode())
    params["wts"] = int(time.time())
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    query = urlencode(sorted_params)
    w_rid = hashlib.md5((query + mixin_key).encode()).hexdigest()
    params["w_rid"] = w_rid
    return params


def _make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    retry = Retry(total=3, backoff_factor=1, allowed_methods=["GET"],
                  connect=3, read=2)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session


def _extract_bvid(url: str) -> str:
    """Extract BV id from a Bilibili URL."""
    m = re.search(r"(BV[a-zA-Z0-9]+)", url)
    if m:
        return m.group(1)
    # b23.tv short URL — need to resolve
    raise ValueError(f"Cannot extract BV id from URL: {url}")


def fetch(url: str, output_dir: str = None) -> dict:
    """
    Download Bilibili video audio via WBI-signed API.

    Returns dict with title, author, body_text (transcript if CC available),
    duration_sec, images (empty), and audio_path.
    
    Does NOT transcribe — use bilibili-transcriber for ASR.
    """
    bvid = _extract_bvid(url)
    session = _make_session()

    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="fetch-bilibili-")
    else:
        os.makedirs(output_dir, exist_ok=True)

    print(f"[bilibili] Fetching BV: {bvid}", file=sys.stderr)

    # ── Step 1: Get WBI keys ──
    print(f"  [1/4] Getting WBI keys…", file=sys.stderr)
    resp = session.get("https://api.bilibili.com/x/web-interface/nav", timeout=15)
    data = resp.json()
    wbi_img = data.get("data", {}).get("wbi_img", {})
    img_key = re.search(r"/wbi/([^/]+)", wbi_img["img_url"]).group(1)
    sub_key = re.search(r"/wbi/([^/]+)", wbi_img["sub_url"]).group(1)

    def wbi_get(base_url, params):
        signed = _wbi_sign(params.copy(), img_key, sub_key)
        r = session.get(base_url, params=signed, timeout=15)
        j = r.json()
        if j.get("code") != 0:
            raise RuntimeError(f"API error {j.get('code')}: {j.get('message', j)}")
        return j["data"]

    # ── Step 2: Get video info ──
    print(f"  [2/4] Getting video info…", file=sys.stderr)
    info = wbi_get("https://api.bilibili.com/x/web-interface/wbi/view", {"bvid": bvid})
    title = info.get("title", "").strip()
    cid = str(info.get("cid", ""))
    if not cid and info.get("pages"):
        cid = str(info["pages"][0]["cid"])
    duration = info.get("duration", 0)
    owner = info.get("owner", {}).get("name", "")
    pubdate = info.get("pubdate", 0)

    # ── Step 3: Check for CC subtitles ──
    print(f"  [3/4] Checking CC subtitles…", file=sys.stderr)
    has_subs = False
    body_text = ""
    try:
        player = wbi_get("https://api.bilibili.com/x/player/wbi/v2",
                         {"bvid": bvid, "cid": cid})
        subs = player.get("subtitle", {}).get("subtitles", [])
    except Exception:
        subs = []

    if subs:
        sub_url = subs[0]["subtitle_url"]
        if sub_url.startswith("//"):
            sub_url = "https:" + sub_url
        sub_data = session.get(sub_url, timeout=15).json()
        body_parts = [item.get("content", "") for item in sub_data.get("body", [])]
        body_text = "\n".join(body_parts)
        has_subs = True
        print(f"  Found CC subtitles: {len(body_text)} chars", file=sys.stderr)

        # Save transcript
        tpath = os.path.join(output_dir, "transcript.md")
        with open(tpath, "w", encoding="utf-8") as f:
            f.write(body_text)
        print(f"  Transcript saved → {tpath}", file=sys.stderr)

    # ── Step 4: Get audio URL and download ──
    print(f"  [4/4] Getting audio URL…", file=sys.stderr)
    play = wbi_get("https://api.bilibili.com/x/player/wbi/playurl",
                   {"bvid": bvid, "cid": cid, "qn": 16, "platform": "web"})
    durl = play.get("durl", [])
    if not durl:
        audio_ = play.get("dash", {}).get("audio", [])
        if audio_:
            durl = [{"url": audio_[0].get("baseUrl", audio_[0].get("base_url", "")),
                     "size": audio_[0].get("size", 0)}]
    if not durl:
        raise RuntimeError("No audio URL found")

    audio_url = durl[0]["url"]
    audio_size = durl[0].get("size", 0)
    print(f"  Audio URL obtained ({audio_size / 1_048_576:.1f} MB)", file=sys.stderr)

    # Download
    audio_path = os.path.join(output_dir, "audio.mp4")
    max_attempts = 3
    downloaded = 0
    for attempt in range(1, max_attempts + 1):
        headers = HEADERS.copy()
        existing = os.path.getsize(audio_path) if os.path.exists(audio_path) else 0
        if existing > 0 and existing < audio_size:
            headers["Range"] = f"bytes={existing}-"
        else:
            existing = 0

        try:
            r = session.get(audio_url, headers=headers, stream=True,
                          timeout=(10, 30))
            r.raise_for_status()
            mode = "ab" if existing > 0 else "wb"
            with open(audio_path, mode) as f:
                for chunk in r.iter_content(chunk_size=65536):
                    if chunk:
                        f.write(chunk)
                        downloaded = existing + f.tell()
            total = os.path.getsize(audio_path)
            if total >= audio_size:
                print(f"  Downloaded {total / 1_048_576:.1f} MB", file=sys.stderr)
                break
        except Exception as e:
            print(f"  Download error (attempt {attempt}): {e}", file=sys.stderr)
            if attempt == max_attempts:
                raise
            time.sleep(2 ** attempt)

    # Write metadata
    meta = {
        "bvid": bvid,
        "title": title,
        "uploader": owner,
        "publish_date": str(pubdate),
        "duration_sec": duration,
        "has_cc_subtitles": has_subs,
        "audio_path": audio_path,
    }
    meta_path = os.path.join(output_dir, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"  Metadata → {meta_path}", file=sys.stderr)

    return {
        "title": title,
        "author": owner,
        "publish_time": str(pubdate),
        "body_text": body_text,
        "images": [],
        "duration_sec": duration,
        "audio_path": audio_path,
        "has_cc_subtitles": has_subs,
    }