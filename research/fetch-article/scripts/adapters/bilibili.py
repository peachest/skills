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
import shutil
import subprocess
import sys
import time
import tempfile
from pathlib import Path
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def _find_aria2c() -> str:
    """Locate aria2c binary: PATH first, then ~/scripts/aria2c."""
    path = shutil.which("aria2c")
    if path:
        return path
    fallback = Path.home() / "scripts" / "aria2c"
    if fallback.is_file() and os.access(fallback, os.X_OK):
        return str(fallback)
    raise RuntimeError("aria2c not found in PATH or ~/scripts/aria2c")


def _download_with_aria2c(url: str, output_path: str, output_dir: str):
    """Download a URL via aria2c subprocess.

    Uses --continue for cross-call resumption via .aria2 control file.
    Raises RuntimeError on non-zero exit.
    """
    aria2c = _find_aria2c()
    args = [
        aria2c,
        "-d", output_dir,
        "-o", os.path.basename(output_path),
        "--continue=true",
        "--max-tries=3",
        "--retry-wait=2",
        "--header=Referer: https://www.bilibili.com/",
        "--header=User-Agent: " + HEADERS["User-Agent"],
    ]
    proxy = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
    if proxy:
        args.append(f"--all-proxy={proxy}")
    args.append(url)

    result = subprocess.run(args, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        stderr_excerpt = (result.stderr or result.stdout or "")[-500:]
        raise RuntimeError(
            f"aria2c download failed (exit {result.returncode}): {stderr_excerpt}")

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


def _extract_page(url: str) -> int:
    """Extract ?p=N page parameter from URL (1-based). Returns 1 if absent."""
    from urllib.parse import urlparse, parse_qs
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    p = params.get("p", ["1"])[0]
    try:
        page = int(p)
        return max(1, page)
    except ValueError:
        return 1


def fetch(url: str, output_dir: str = None) -> dict:
    """
    Download Bilibili video audio via WBI-signed API.

    Returns dict with title, author, body_text (transcript if CC available),
    duration_sec, images (empty), and audio_path.
    
    Does NOT transcribe — use bilibili-transcriber for ASR.
    """
    bvid = _extract_bvid(url)
    page_num = _extract_page(url)  # 1-based
    page_index = page_num - 1      # 0-based array index
    session = _make_session()

    if output_dir is None:
        output_dir = os.path.join(
            os.path.expanduser("~/.cache/fetch-bilibili"), bvid)
        os.makedirs(output_dir, exist_ok=True)
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
    pages = info.get("pages", [])
    page_count = len(pages) if pages else 1
    if pages:
        if page_index >= len(pages):
            raise RuntimeError(
                f"Page {page_num} out of range (video has {len(pages)} pages)")
        page_info = pages[page_index]
        cid = str(page_info.get("cid", ""))
        duration = page_info.get("duration", 0)
    else:
        cid = str(info.get("cid", ""))
        duration = info.get("duration", 0)
    owner = info.get("owner", {}).get("name", "")
    pubdate = info.get("pubdate", 0)
    print(f"  Page {page_num}/{page_count}, cid={cid}, duration={duration}s",
          file=sys.stderr)

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

        # CC subtitles available — skip audio download entirely
        meta = {
            "bvid": bvid,
            "title": title,
            "uploader": owner,
            "publish_date": str(pubdate),
            "duration_sec": duration,
            "has_cc_subtitles": True,
            "audio_path": None,
            "content_length": None,
            "stream_type": "cc_subtitle_only",
            "page": page_num,
            "page_count": page_count,
        }
        meta_path = os.path.join(output_dir, "metadata.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        print(f"  Metadata → {meta_path} (CC subtitles, audio download skipped)",
              file=sys.stderr)

        return {
            "title": title,
            "author": owner,
            "publish_time": str(pubdate),
            "body_text": body_text,
            "images": [],
            "duration_sec": duration,
            "audio_path": None,
            "has_cc_subtitles": True,
            "content_length": None,
            "stream_type": "cc_subtitle_only",
            "page": page_num,
            "page_count": page_count,
        }

    # ── Step 4: Get audio URL and download ──
    print(f"  [4/4] Getting audio URL…", file=sys.stderr)
    play = wbi_get("https://api.bilibili.com/x/player/wbi/playurl",
                   {"bvid": bvid, "cid": cid,
                    "fnval": 16, "fnver": 0, "qn": 0, "platform": "pc"})

    audio_path = os.path.join(output_dir, "audio.mp4")
    stream_type = None

    # DASH audio first (lowest bandwidth); durl fallback only when no DASH audio
    dash = play.get("dash") or {}
    dash_audio = dash.get("audio", [])
    if dash_audio:
        best = min(dash_audio, key=lambda a: a.get("bandwidth", 0))
        audio_url = best.get("baseUrl", best.get("base_url", ""))
        bandwidth = best.get("bandwidth", 0)
        print(f"  Audio URL obtained (DASH, bandwidth={bandwidth})", file=sys.stderr)
        _download_with_aria2c(audio_url, audio_path, output_dir)
        stream_type = "dash_audio"
    else:
        durl = play.get("durl", [])
        if not durl:
            raise RuntimeError("No audio URL found")
        if len(durl) == 1:
            audio_url = durl[0]["url"]
            print(f"  Audio URL obtained (durl, {durl[0].get('size', 0) / 1_048_576:.1f} MB)",
                  file=sys.stderr)
            _download_with_aria2c(audio_url, audio_path, output_dir)
        else:
            # Multi-segment durl: download each, then ffmpeg concat
            print(f"  Audio URL obtained (durl, {len(durl)} segments)", file=sys.stderr)
            segment_paths = []
            for i, seg in enumerate(durl):
                seg_path = os.path.join(output_dir, f"segment_{i}.m4s")
                _download_with_aria2c(seg["url"], seg_path, output_dir)
                segment_paths.append(seg_path)
            # Generate list.txt for ffmpeg concat
            list_path = os.path.join(output_dir, "list.txt")
            with open(list_path, "w") as f:
                for sp in segment_paths:
                    f.write(f"file '{os.path.basename(sp)}'\n")
            # ffmpeg concat
            result = subprocess.run(
                ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                 "-i", list_path, "-c", "copy", audio_path],
                capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                raise RuntimeError(f"ffmpeg concat failed: {result.stderr[-500:]}")
            # Clean up segments
            for sp in segment_paths:
                os.remove(sp)
            os.remove(list_path)
        stream_type = "durl_video"

    content_length = os.path.getsize(audio_path)
    if content_length == 0:
        raise RuntimeError("Downloaded file is empty")
    print(f"  Downloaded {content_length / 1_048_576:.1f} MB", file=sys.stderr)

    # Write metadata
    meta = {
        "bvid": bvid,
        "title": title,
        "uploader": owner,
        "publish_date": str(pubdate),
        "duration_sec": duration,
        "has_cc_subtitles": has_subs,
        "audio_path": audio_path,
        "content_length": content_length,
        "stream_type": stream_type,
        "page": page_num,
        "page_count": page_count,
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
        "content_length": content_length,
        "stream_type": stream_type,
        "page": page_num,
        "page_count": page_count,
    }