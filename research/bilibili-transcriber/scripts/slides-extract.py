#!/usr/bin/env python3
"""slides-extract.py — extract slide deck images + verbatim OCR text from a video.

Pipeline: video download (yt-dlp, skipped if video.mp4 exists) → ffmpeg scene-cut
frame extraction → adjacent-frame dedup (dHash hamming distance) → per-frame
vision-LLM OCR → <workspace>/slides/{slides.json,slides.md}.

Config (env or runtime.conf in the script's skill dir):
  OCR_LLM_BASEURL / OCR_LLM_MODEL / OCR_LLM_KEY  — OpenAI-compatible vision endpoint
  SLIDE_SCENE_THRESHOLD  — ffmpeg scene-change sensitivity 0-1 (default 0.3)
  SLIDE_HASH_THRESHOLD   — adjacent dedup, dHash hamming distance (default 8)

Usage: uv run python scripts/slides-extract.py <workspace-dir>
Resumable: OCR results cached in slides.json keyed by frame filename.
"""

from __future__ import annotations

import asyncio
import base64
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image

SKILL_DIR = Path(__file__).resolve().parent.parent

PROMPT = (
    "你是专业的 PPT 转录员。逐字转录这张幻灯片上的所有文字内容：\n"
    "1. 保持原有结构（标题/正文/要点层级），用 Markdown 列表表达\n"
    "2. 逐字转录，不要遗漏任何数字、单位、代码、公式、脚注\n"
    "3. 保持原语言，不翻译\n"
    "4. 如果这张图不是幻灯片（人物、空镜头、过渡画面），只输出：[非幻灯片]"
    "5. 注意：低分辨率或文字模糊但版式为演示文稿（PPT）的图仍是幻灯片，"
    "请尽力转录可辨认的文字，不要因为看不清而判为非幻灯片"
)

NON_SLIDE = "[非幻灯片]"


from _conf import load_conf


def _ocr_conf() -> dict:
    return load_conf(
        "OCR_LLM_BASEURL", "OCR_LLM_MODEL",
        keys=("OCR_LLM_BASEURL", "OCR_LLM_MODEL", "OCR_LLM_KEY",
              "SLIDE_SCENE_THRESHOLD", "SLIDE_HASH_THRESHOLD"),
    )


def parse_showinfo_pts(stderr_text: str) -> list[float]:
    """Extract pts_time values from ffmpeg showinfo stderr, in output order."""
    pts = []
    for m in re.finditer(r"showinfo.*pts_time:([0-9.]+)", stderr_text):
        pts.append(float(m.group(1)))
    return pts


def dhash(img: Image.Image, size: int = 8) -> int:
    """Difference hash: 64-bit from a (size+1)x size grayscale gradient."""
    g = img.convert("L").resize((size + 1, size), Image.LANCZOS)
    px = list(g.getdata())
    bits = 0
    for row in range(size):
        for col in range(size):
            left = px[row * (size + 1) + col]
            right = px[row * (size + 1) + col + 1]
            bits = (bits << 1) | (1 if left > right else 0)
    return bits


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def dedup_adjacent(frames: list[dict], threshold: int) -> list[dict]:
    """frames: [{file, time_sec}, ...] time-sorted. Drop frames too close to
    the previous KEPT frame (repeated slide stays represented once)."""
    kept: list[dict] = []
    for f in frames:
        h = dhash(Image.open(f["file"]))
        if kept and hamming(dhash(Image.open(kept[-1]["file"])), h) <= threshold:
            continue
        f["dhash"] = h
        kept.append(f)
    return kept


def timecode(sec: float) -> str:
    s = int(sec)
    return f"{s // 60:02d}:{s % 60:02d}"


def download_video(workspace: Path) -> Path:
    video = workspace / "video.mp4"
    if video.exists() and video.stat().st_size > 0:
        return video
    meta = json.loads((workspace / "metadata.json").read_text(encoding="utf-8"))
    bvid = meta.get("bvid")
    if not bvid:
        sys.exit("FAIL no video.mp4 and metadata.json has no bvid to download")
    try:
        return download_video_wbi(bvid, video)
    except Exception as e:  # noqa: BLE001 — fall back to yt-dlp
        print(f"  WBI video download failed ({e}); falling back to yt-dlp")
    url = f"https://www.bilibili.com/video/{bvid}/"
    print(f"  downloading video via yt-dlp: {url}")
    r = subprocess.run(
        ["yt-dlp", "-f", "bv*+ba/b", "--merge-output-format", "mp4",
         "-o", str(video), url],
        capture_output=True, text=True, timeout=1800)
    if r.returncode != 0 or not video.exists():
        sys.exit(f"FAIL video download: wbi={e!r}; yt-dlp: {r.stderr[-500:]}")
    return video


def download_video_wbi(bvid: str, video: Path) -> Path:
    """Download a video stream via fetch-article's WBI-signed API path
    (bare yt-dlp gets 412 from bilibili)."""
    sys.path.insert(0, str(SKILL_DIR.parent / "fetch-article" / "scripts"))
    import adapters.bilibili as bl  # noqa: PLC0415

    session = bl._make_session()
    # 复用 bili CLI 登录态拿 >480p 流（未登录 DASH 上限 480p，OCR 文字可读性差）
    cred = Path.home() / ".bilibili-cli" / "credential.json"
    if cred.is_file():
        try:
            c = json.loads(cred.read_text(encoding="utf-8"))
            pairs = {"SESSDATA": c.get("sessdata"), "bili_jct": c.get("bili_jct"),
                     "DedeUserID": c.get("dedeuserid"), "buvid3": c.get("buvid3")}
            session.cookies.update({k: v for k, v in pairs.items() if v})
        except Exception as e:  # noqa: BLE001 — 无凭证/坏文件仍可裸抓 480p
            print(f"  no bili CLI credential ({e}); downloading unauthenticated")
    nav = session.get("https://api.bilibili.com/x/web-interface/nav", timeout=15).json()
    wbi = nav["data"]["wbi_img"]
    img_key = re.search(r"/wbi/([^/]+)", wbi["img_url"]).group(1)
    sub_key = re.search(r"/wbi/([^/]+)", wbi["sub_url"]).group(1)

    def wbi_get(base_url: str, params: dict) -> dict:
        signed = bl._wbi_sign(params.copy(), img_key, sub_key)
        j = session.get(base_url, params=signed, timeout=15).json()
        if j.get("code") != 0:
            raise RuntimeError(f"API {j.get('code')}: {j.get('message')}")
        return j["data"]

    info = wbi_get("https://api.bilibili.com/x/web-interface/wbi/view", {"bvid": bvid})
    cid = str(info.get("cid") or info["pages"][0]["cid"])
    play = wbi_get("https://api.bilibili.com/x/player/wbi/playurl",
                   {"bvid": bvid, "cid": cid, "fnval": 16, "fnver": 0,
                    "qn": 0, "platform": "pc"})
    vids = (play.get("dash") or {}).get("video") or []
    if not vids:
        raise RuntimeError("no DASH video stream in playurl response")
    # slides OCR doesn't need 4K: prefer the highest id <= 80 (1080p)
    capped = [v for v in vids if v.get("id", 0) <= 80]
    best = max(capped or vids, key=lambda v: v.get("id", 0))
    url = best.get("baseUrl") or best.get("base_url")
    print(f"  WBI video stream: qn={best.get('id')}, "
          f"~{best.get('bandwidth', 0) * 351 // 8 // 1048576}MB")
    bl._download_with_aria2c(url, str(video), str(video.parent))
    return video


def ffprobe_duration(video: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(video)], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def extract_frames(video: Path, out_dir: Path, threshold: float,
                   grab_delay: float = 1.0) -> list[dict]:
    """Two-pass scene extraction: pass 1 lists cut times (select+showinfo,
    null output); pass 2 grabs a settled frame at each cut + grab_delay
    (cut-frame lands mid-animation for morph-style slide transitions).
    Frame at t=0 always kept. Returns [{file, time_sec}] time-sorted."""
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old in frames_dir.glob("frame_*.jpg"):
        old.unlink()  # stale frames from a previous (different-threshold) run

    r = subprocess.run(
        ["ffmpeg", "-loglevel", "info", "-i", str(video),
         "-vf", f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"],
        capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        sys.exit(f"FAIL ffmpeg scene detection: {r.stderr[-500:]}")
    pts = parse_showinfo_pts(r.stderr)

    def grab(sec: float, dest: Path) -> bool:
        g = subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{sec:.3f}",
             "-i", str(video), "-frames:v", "1", "-q:v", "2", str(dest)],
            capture_output=True, text=True, timeout=120)
        return g.returncode == 0 and dest.exists()

    frames = []
    first = frames_dir / "frame_000.jpg"
    if grab(0.0, first):
        frames.append({"file": str(first), "time_sec": 0.0})
    for i, t in enumerate(pts, 1):
        f = frames_dir / f"frame_{i:03d}.jpg"
        if grab(t + grab_delay, f):
            frames.append({"file": str(f), "time_sec": t})
    return frames


def upscale(image_path: str, factor: int = 2) -> str:
    """Lanczos 放大后存旁路文件，返回路径（低清帧二次判定用）。"""
    im = Image.open(image_path)
    out = image_path + f".{factor}x.jpg"
    im.resize((im.width * factor, im.height * factor), Image.LANCZOS).save(out, quality=92)
    return out


def ocr_frame(conf: dict, image_path: str, attempts: int = 3) -> str:
    from _llm import chat_once
    b64 = base64.b64encode(Path(image_path).read_bytes()).decode()
    return asyncio.run(chat_once(
        baseurl=conf["OCR_LLM_BASEURL"],
        model=conf["OCR_LLM_MODEL"],
        key=conf.get("OCR_LLM_KEY", ""),
        messages=[{"role": "user", "content": [
            {"type": "text", "text": PROMPT},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
        ]}],
        temperature=0,
        timeout=120,
        retries=attempts,
    ))


def extract_frames_grid(video: Path, out_dir: Path, grid_sec: float) -> list[dict]:
    """Uniform grid sampling: one frame every grid_sec seconds.

    For progressive-animation decks (PPT built up in steps) scene-cut frames
    land mid-animation and stay incomplete — a uniform grid almost always
    catches a finished state (peer 01a1878b experiment on BV1WPx769EPZ:
    grid beats scene detection on such decks, and only grid catches
    flash pages shorter than the grid interval). Dedup + [非幻灯片]
    filtering downstream keeps the extra frames cheap.
    """
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old in frames_dir.glob("frame_*.jpg"):
        old.unlink()
    duration = ffprobe_duration(video)
    frames = []
    t = 0.0
    i = 0
    while t < duration:
        f = frames_dir / f"frame_{i:03d}.jpg"
        g = subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.3f}",
             "-i", str(video), "-frames:v", "1", "-q:v", "2", str(f)],
            capture_output=True, text=True, timeout=120)
        if g.returncode == 0 and f.exists():
            frames.append({"file": str(f), "time_sec": t})
        t += grid_sec
        i += 1
    return frames


def scene_score_stats(video: Path) -> list[float]:
    """Probe pass: scene score of every frame boundary, sorted desc.

    Cheap (single ffmpeg null-run) — run before choosing a threshold:
    if even the top scores sit far below the default 0.3, the deck is
    progressive-animation and the grid sampler is the right tool.
    """
    r = subprocess.run(
        ["ffmpeg", "-loglevel", "info", "-i", str(video),
         "-vf", "select='gte(scene,0)',metadata=print", "-f", "null", "-"],
        capture_output=True, text=True, timeout=1800)
    scores = [float(m) for m in re.findall(r"lavfi\.scene_score=([0-9.]+)", r.stderr)]
    return sorted(scores, reverse=True)


def extract_frames_adaptive(video: Path, out_dir: Path, threshold: float,
                            min_frames: int = 3, min_duration: float = 120,
                            retry_threshold: float = 0.15) -> list[dict]:
    """讲解类视频转场分值低，高阈值下几乎无切点；切点过少且视频够长时
    降阈值重试一次。过检由后级 dHash 去重 + OCR [非幻灯片] 判定兜底。"""
    frames = extract_frames(video, out_dir, threshold)
    if len(frames) < min_frames and ffprobe_duration(video) > min_duration:
        print(f"  only {len(frames) - 1} cuts in a long video — "
              f"retrying threshold={retry_threshold}")
        frames = extract_frames(video, out_dir, retry_threshold)
    return frames


def main() -> None:
    args = sys.argv[1:]
    grid_sec = 0.0
    if "--grid" in args:
        i = args.index("--grid")
        grid_sec = float(args[i + 1])
        del args[i:i + 2]
    if len(args) < 1:
        sys.exit(f"Usage: {sys.argv[0]} <workspace-dir> [--grid <sec>]")
    workspace = Path(args[0])
    if not workspace.is_dir():
        sys.exit(f"FAIL workspace not found: {workspace}")
    conf = _ocr_conf()
    threshold = float(conf["SLIDE_SCENE_THRESHOLD"] or 0.3)
    hash_threshold = int(conf["SLIDE_HASH_THRESHOLD"] or 8)

    out_dir = workspace / "slides"
    out_dir.mkdir(exist_ok=True)
    cache_path = out_dir / "slides.json"
    cache: dict[str, dict] = {}
    if cache_path.exists():
        cache = {e["file"]: e for e in json.loads(cache_path.read_text(encoding="utf-8"))}

    video = download_video(workspace)
    print(f"[1/4] video: {video.name} ({video.stat().st_size // 1048576}MB)")

    print(f"[2/4] frame extraction…")
    if grid_sec > 0:
        frames = extract_frames_grid(video, out_dir, grid_sec)
        print(f"  uniform grid every {grid_sec}s: {len(frames)} frames")
    else:
        # score probe before committing to scene detection: top scores far
        # below the default threshold ⇒ progressive-animation deck ⇒ grid
        stats = scene_score_stats(video)
        top = stats[0] if stats else 0.0
        if top < threshold * 0.5:
            grid_sec = 15.0
            print(f"  scene scores max {top:.3f} << default {threshold} — "
                  f"progressive-animation deck, degrading to uniform grid ({grid_sec}s)")
            frames = extract_frames_grid(video, out_dir, grid_sec)
            print(f"  uniform grid every {grid_sec}s: {len(frames)} frames")
        else:
            frames = extract_frames_adaptive(video, out_dir, threshold)
            print(f"  {len(frames) - 1} scene cuts (top score {top:.3f}) + t=0 frame")

    print(f"[3/4] adjacent-frame dedup (dHash hamming ≤ {hash_threshold})…")
    kept = dedup_adjacent(frames, hash_threshold)
    print(f"  {len(frames)} → {len(kept)} unique slides")

    print("[4/4] OCR via vision LLM…")
    t0 = time.time()
    entries = []
    def flush():
        # 原子写：写入中途被杀会让缓存变截断 JSON，下次启动直接报废全部进度
        tmp = cache_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, cache_path)
    for i, f in enumerate(kept, 1):
        cached = cache.get(f["file"])
        if cached and cached.get("text"):
            text, status = cached["text"], "cached"
        else:
            try:
                text = ocr_frame(conf, f["file"])
                status = "ok"
                if text == NON_SLIDE:
                    # 二次判定：2x 放大提升小字可读性，仍判非幻灯片才落地
                    up = upscale(f["file"])
                    try:
                        text2 = ocr_frame(conf, up)
                    finally:
                        Path(up).unlink(missing_ok=True)
                    if text2 and text2 != NON_SLIDE:
                        text, status = text2, "ok (rejudged 2x)"
            except Exception as e:  # noqa: BLE001 — report and continue
                text, status = "", f"error: {e}"
        entries.append({"file": f["file"], "time_sec": f["time_sec"],
                        "timecode": timecode(f["time_sec"]), "text": text, "status": status})
        flush()  # 逐帧落盘：中断后重跑已完成的帧直接命中缓存
        print(f"  [{i}/{len(kept)}] {timecode(f['time_sec'])} {status}: {text[:40]!r}")
    ocr_s = time.time() - t0

    md = ["# 幻灯片（场景切帧 + 识图）", ""]
    for e in entries:
        md.append(f"## [{e['timecode']} 幻灯片]")
        md.append("")
        md.append(e["text"] if e["text"] else f"_({e['status']})_")
        md.append("")
    (out_dir / "slides.md").write_text("\n".join(md), encoding="utf-8")

    empty = [e for e in entries if not e["text"]]
    print(f"done: {len(entries)} slides, OCR {ocr_s:.1f}s → {cache_path}")
    if empty:
        print(f"WARN {len(empty)} entries without text — inspect slides.md / rerun (cached)")
        sys.exit(2)


if __name__ == "__main__":
    main()
