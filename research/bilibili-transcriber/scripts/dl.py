#!/usr/bin/env python3
"""
Bilibili video audio downloader — WBI-signed, outputs into video/{BV}-{title}/raw/audio.mp4

Usage:
  python scripts/dl.py BV1ahVr6gERA
"""

import hashlib, json, os, re, sys, time
from datetime import datetime
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

# ── Path setup ─────────────────────────────────────────────────────────────
# This script lives in .agent/skills/bilibili-transcriber/scripts/dl.py
# Project root is 4 levels up from the scripts/ dir, but we detect at runtime.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)        # …/bilibili-transcriber/
AGENT_DIR = os.path.dirname(SKILL_DIR)          # …/.agent/
PROJECT_ROOT = os.path.dirname(AGENT_DIR)       # …/ai-age-defensive-programming/
VIDEO_DIR = os.path.join(PROJECT_ROOT, "video")  # workspace: raw audio + ASR comparisons
TRANSCRIPT_DIR = os.path.join(PROJECT_ROOT, "references/transcripts")  # final output
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)


# ── WBI helpers ────────────────────────────────────────────────────────────
def get_mixin_key(raw_key: bytes) -> str:
    return "".join(chr(raw_key[i]) for i in MIXIN_KEY_ENC_TAB)


def wbi_sign(params: dict, img_key: str, sub_key: str) -> dict:
    mixin_key = get_mixin_key((img_key + sub_key).encode())
    params["wts"] = int(time.time())
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    query = urlencode(sorted_params)
    w_rid = hashlib.md5((query + mixin_key).encode()).hexdigest()
    params["w_rid"] = w_rid
    return params


# ── main ───────────────────────────────────────────────────────────────────
def _make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    retry = Retry(total=3, backoff_factor=1, allowed_methods=["GET"],
                  connect=3, read=2)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session


def main(bvid: str):
    session = _make_session()

    # Step 1: Get WBI keys
    print(f"[1/5] Fetching WBI keys…")
    resp = session.get("https://api.bilibili.com/x/web-interface/nav", timeout=15)
    data = resp.json()
    wbi_img = data.get("data", {}).get("wbi_img", {})
    img_key = re.search(r"/wbi/([^/]+)", wbi_img["img_url"]).group(1)
    sub_key = re.search(r"/wbi/([^/]+)", wbi_img["sub_url"]).group(1)
    print(f"  keys: {img_key[:8]}… / {sub_key[:8]}…")

    def wbi_get(base_url, params):
        signed = wbi_sign(params.copy(), img_key, sub_key)
        r = session.get(base_url, params=signed, timeout=15)
        j = r.json()
        if j.get("code") != 0:
            raise RuntimeError(f"API error {j.get('code')}: {j.get('message', j)}")
        return j["data"]

    # Step 2: Get video info
    print(f"[2/5] Fetching video info…")
    info = wbi_get("https://api.bilibili.com/x/web-interface/wbi/view", {"bvid": bvid})
    title = info.get("title", "").strip()
    cid = str(info.get("cid", ""))
    if not cid and info.get("pages"):
        cid = str(info["pages"][0]["cid"])
    desc = info.get("desc", "")
    duration = info.get("duration", 0)
    owner = info.get("owner", {}).get("name", "")
    pubdate = info.get("pubdate", 0)
    stat = info.get("stat", {})
    print(f"  title: {title[:60]}")
    print(f"  cid: {cid}, duration: {duration}s")

    # Step 3: Check for CC subtitles
    print(f"[3/5] Checking CC subtitles…")
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
        body = sub_data.get("body", [])
        transcript = "\n".join(item.get("content", "") for item in body)
        print(f"  Found {len(subs)} subtitle track(s), {len(transcript)} chars")
        has_subs = True
    else:
        transcript = ""
        has_subs = False
        print(f"  No CC subtitles")

    # Step 4: Get audio URL
    print(f"[4/5] Fetching audio URL…")
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
    print(f"  URL obtained ({audio_size / 1_048_576:.1f} MB)")

    # Prepare date for directory naming
    today = datetime.now().strftime("%Y%m%d")
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)[:60] if title else bvid

    # Build workspace directory: video/{BV}-{title}/ (raw audio + ASR cache)
    work_dir = os.path.join(VIDEO_DIR, f"{bvid}-{safe_title}")
    raw_dir = os.path.join(work_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)
    audio_path = os.path.join(raw_dir, "audio.mp4")

    # Build transcript reference directory: references/transcripts/bilibili/{date}-{title}-{BV}/
    ref_dir = os.path.join(TRANSCRIPT_DIR, "bilibili", f"{today}-{safe_title}-{bvid}")
    os.makedirs(ref_dir, exist_ok=True)

    # Step 5: Download audio with resume
    print(f"[5/5] Downloading audio ({audio_size / 1_048_576:.1f} MB)…")
    max_attempts = 3
    downloaded = 0
    for attempt in range(1, max_attempts + 1):
        headers = HEADERS.copy()
        existing = os.path.getsize(audio_path) if os.path.exists(audio_path) else 0
        if existing > 0 and existing < audio_size:
            headers["Range"] = f"bytes={existing}-"
            print(f"  [attempt {attempt}/{max_attempts}] Resuming from {existing / 1_048_576:.1f} MB…")
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
                print(f"  Saved {total / 1_048_576:.1f} MB")
                break
            else:
                print(f"  Partial: {total / 1_048_576:.1f}/{audio_size / 1_048_576:.1f} MB, retrying…")
        except Exception as e:
            print(f"  Download error: {e}")
            if attempt == max_attempts:
                raise
            time.sleep(2 ** attempt)

    # Helper: write metadata file
    def write_metadata(target_dir):
        mpath = os.path.join(target_dir, "metadata.md")
        with open(mpath, "w", encoding="utf-8") as f:
            f.write("# 视频元数据\n\n")
            f.write("| 字段 | 值 |\n|------|------|\n")
            f.write(f"| 来源 | Bilibili |\n")
            f.write(f"| BV号 | `{bvid}` |\n")
            f.write(f"| 标题 | {title} |\n")
            f.write(f"| UP主 | {owner} |\n")
            f.write(f"| 发布时间 | {pubdate} |\n")
            f.write(f"| 时长 | {duration//60}分{duration%60}秒 |\n")
            f.write(f"| 链接 | <https://www.bilibili.com/video/{bvid}/> |\n")
            f.write(f"| 转录日期 | {today} |\n\n")
            f.write("## 统计\n\n| 指标 | 数值 |\n|------|------|\n")
            f.write(f"| 播放 | {stat.get('view', 'N/A')} |\n")
            f.write(f"| 弹幕 | {stat.get('danmaku', 'N/A')} |\n")
            f.write(f"| 评论 | {stat.get('reply', 'N/A')} |\n")
            f.write(f"| 收藏 | {stat.get('favorite', 'N/A')} |\n")
            f.write(f"| 硬币 | {stat.get('coin', 'N/A')} |\n")
            f.write(f"| 分享 | {stat.get('share', 'N/A')} |\n")
            f.write(f"| 点赞 | {stat.get('like', 'N/A')} |\n\n")
            if info.get("ugc_season"):
                f.write("## 合集信息\n\n")
                f.write(f"| 字段 | 值 |\n|------|------|\n")
                f.write(f"| 合集名 | {info['ugc_season'].get('title', '')} |\n")
            f.write("\n## 视频简介\n\n")
            f.write(f"> {desc}\n\n")
            f.write("## 提取参数\n\n| 参数 | 值 |\n|------|-----|\n")
            f.write(f"| 提取方式 | Bilibili API（WBI签名）→ 音频下载 |\n")
            f.write(f"| 字幕情况 | {'有内嵌CC' if has_subs else '无内嵌CC（仅音频）'} |\n")
            f.write(f"| 原始音频 | {audio_path} ({downloaded / 1_048_576:.1f} MB) |\n")
        return mpath

    # Write metadata to both workspace and reference dir
    mpath_work = write_metadata(work_dir)
    mpath_ref = write_metadata(ref_dir)
    print(f"  Metadata → {mpath_ref}")

    # If subtitles available, save transcript to reference dir (skip ASR)
    if transcript:
        tpath = os.path.join(ref_dir, "transcript.md")
        with open(tpath, "w", encoding="utf-8") as f:
            f.write(transcript)
        # Also save to workspace for convenience
        tpath_work = os.path.join(work_dir, "transcript.md")
        with open(tpath_work, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"  CC Transcript → {tpath} (skip ASR)")

    print(f"\n✓ Done.")
    print(f"  Reference:  {ref_dir}/")
    print(f"  Workspace:  {work_dir}/")
    print(f"  Transcript: {'CC subtitles (skip ASR)' if transcript else 'Run transcribe.sh next'}")
    return ref_dir, work_dir


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/dl.py <BV号>")
        sys.exit(1)
    main(sys.argv[1])