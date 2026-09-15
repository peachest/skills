#!/usr/bin/env python3
"""
YouTube video adapter.

Strategy: yt-dlp. Prefer subtitles (manual or auto) — no download, the
subtitle text IS the deliverable. Only when no subtitles exist, download
best-audio for ASR (set WHISPER_LANG=en for the transcriber).

Proxy: YouTube is often unreachable directly from CN networks. yt-dlp
honors https_proxy/HTTPS_PROXY env vars automatically; the adapter also
forwards them explicitly via --proxy.

Usage (called by fetch.py, not directly).
"""

import glob
import json
import os
import re
import shutil
import subprocess
import sys

PROXY_ENV_VARS = ("https_proxy", "HTTPS_PROXY", "http_proxy", "HTTP_PROXY")


def _find_ytdlp() -> str:
    path = shutil.which("yt-dlp")
    if not path:
        raise RuntimeError(
            "yt-dlp not found on PATH — youtube adapter requires it "
            "(nix profile, pip install yt-dlp, or brew)")
    return path


def _proxy_args() -> list:
    for var in PROXY_ENV_VARS:
        if os.environ.get(var):
            return ["--proxy", os.environ[var]]
    return []


def _extract_video_id(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([A-Za-z0-9_-]{11})", url)
    if not m:
        raise ValueError(f"Cannot extract video id from URL: {url}")
    return m.group(1)


def _vtt_to_text(path: str) -> str:
    """VTT → plain text. Auto-subs repeat each line in a rolling window;
    dropping consecutive duplicates removes the repetition. Inline
    timestamp tags (<00:00.319>) are stripped."""
    lines = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for ln in f:
            ln = re.sub(r"<[^>]+>", "", ln)
            ln = re.sub(r"\s+", " ", ln).strip()
            if (not ln or "-->" in ln or ln.startswith(("WEBVTT", "Kind:",
                    "Language:", "NOTE")) or ln.isdigit()):
                continue
            if not lines or ln != lines[-1]:
                lines.append(ln)
    return " ".join(lines)


def _pick_subtitle(output_dir: str, video_id: str):
    """Prefer manual subs (.{id}.en.vtt) over auto (.{id}.en-orig.vtt)."""
    vtt_files = glob.glob(os.path.join(output_dir, f"{video_id}.*.vtt"))
    for f in sorted(vtt_files):
        if f.endswith(f"{video_id}.en.vtt"):
            return f
    return vtt_files[0] if vtt_files else None


def fetch(url: str, output_dir: str = None) -> dict:
    video_id = _extract_video_id(url)
    os.makedirs(output_dir, exist_ok=True)
    ytdlp = _find_ytdlp()

    print(f"[youtube] Video id: {video_id}", file=sys.stderr)

    # ── Step 1: metadata + subtitles (no media download) ──
    result = subprocess.run(
        [ytdlp, "--skip-download", "--write-info-json",
         "--write-subs", "--write-auto-subs",
         "--sub-langs", "en.*", "--sub-format", "vtt",
         "-o", os.path.join(output_dir, "%(id)s.%(ext)s")]
        + _proxy_args() + [url],
        capture_output=True, text=True, timeout=300)
    info_path = os.path.join(output_dir, f"{video_id}.info.json")
    if result.returncode != 0 or not os.path.exists(info_path):
        raise RuntimeError(
            f"yt-dlp metadata/subs failed (exit {result.returncode}): "
            f"{(result.stderr or '')[-500:]}")

    with open(info_path, encoding="utf-8") as f:
        info = json.load(f)
    title = info.get("title", "").strip()
    author = info.get("channel", "") or info.get("uploader", "")
    upload_date = info.get("upload_date", "")  # YYYYMMDD
    duration = info.get("duration", 0)
    description = info.get("description", "") or ""

    # ── Step 2: subtitle text, or audio fallback ──
    sub_path = _pick_subtitle(output_dir, video_id)
    audio_path = None
    if sub_path:
        body_text = _vtt_to_text(sub_path)
        stream_type = "subtitle_only"
        print(f"  Subtitles: {os.path.basename(sub_path)} "
              f"({len(body_text)} chars) — audio download skipped",
              file=sys.stderr)
    else:
        print("  No subtitles — downloading best-audio for ASR "
              "(set WHISPER_LANG=en in the transcriber)", file=sys.stderr)
        audio_path = os.path.join(output_dir, "audio.mp4")
        result = subprocess.run(
            [ytdlp, "-f", "bestaudio[ext=m4a]/bestaudio",
             "-o", audio_path]
            + _proxy_args() + [url],
            capture_output=True, text=True, timeout=1200)
        if result.returncode != 0 or not os.path.exists(audio_path):
            raise RuntimeError(
                f"yt-dlp audio download failed (exit {result.returncode}): "
                f"{(result.stderr or '')[-500:]}")
        body_text = description
        stream_type = "audio_only"

    content_length = (os.path.getsize(audio_path)
                      if audio_path and os.path.exists(audio_path) else None)

    meta = {
        "video_id": video_id,
        "title": title,
        "uploader": author,
        "upload_date": upload_date,
        "duration_sec": duration,
        "has_subtitles": sub_path is not None,
        "audio_path": audio_path,
        "content_length": content_length,
        "stream_type": stream_type,
    }
    meta_path = os.path.join(output_dir, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"  Metadata → {meta_path}", file=sys.stderr)

    return {
        "title": title,
        "author": author,
        "publish_time": upload_date,
        "body_text": body_text,
        "images": [],
        "duration_sec": duration,
        "audio_path": audio_path,
        "has_subtitles": sub_path is not None,
        "content_length": content_length,
        "stream_type": stream_type,
    }
