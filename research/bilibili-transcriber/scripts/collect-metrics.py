#!/usr/bin/env python3
"""collect-metrics.py — harvest per-video fetch and transcript metrics into
two persistent datasets under ~/data/bilibili-transcription/:

  fetch-metrics.json       download size / time / speed per video
  transcript-metrics.json  transcode / ASR time / RTF / chars per video

Both datasets merge incrementally by bvid: rerunning after a queue finishes
(possibly for a different uploader, via --source) appends new records and
refreshes existing ones — never loses other sources' data.

Usage:
  python3 collect-metrics.py <workspace-dir> --source 3blue1brown
  python3 collect-metrics.py <workspace-dir> --source manshi [--out-dir DIR]

Fetch timing method: audio.mp4 birth→mtime is the downloader's start→end
window — self-contained and immune to queue reruns overwriting older logs.
Records with a missing/implausible window are kept with reliable=false and
excluded from aggregates.

Transcript fields come from each workspace's faster-whisper/metrics.md.
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_OUT = Path.home() / "data" / "bilibili-transcription"
MAX_PLAUSIBLE_DL = 1800  # s


def linux_birth(path: Path):
    try:
        b = subprocess.run(
            ["stat", "-c", "%W", str(path)], capture_output=True, text=True
        ).stdout.strip()
        return int(b) if b.isdigit() and int(b) > 0 else None
    except Exception:
        return None


def parse_metrics_md(path: Path) -> dict:
    out = {}
    txt = path.read_text(encoding="utf-8")
    for key, pat in [
        ("duration_s", r"音频时长 \| ([\d.]+)s"),
        ("wav_mb", r"WAV 大小 \| ([\d.]+)MB"),
        ("transcode_s", r"转码耗时 \| \.?([\d.]+)s"),
        ("asr_s", r"推理耗时 \| \.?([\d.]+)s"),
        ("rtf", r"RTF \| (\d*\.?\d+)"),
        ("chars", r"字符数 \| (\d+)"),
    ]:
        import re

        m = re.search(pat, txt)
        if m:
            out[key] = float(m.group(1))
    m = re.search(r"转录模式 \| ([\w-]+)", txt)
    if m:
        out["mode"] = m.group(1)
    return out


def load_merge(out_path: Path, records: list) -> dict:
    data = {"updated": time.strftime("%Y-%m-%dT%H:%M:%S"), "records": []}
    if out_path.is_file():
        try:
            old = json.loads(out_path.read_text(encoding="utf-8"))
            data["records"] = old.get("records", [])
        except Exception:
            pass
    by_bvid = {r["bvid"]: r for r in data["records"]}
    for r in records:
        by_bvid[r["bvid"]] = r  # upsert: refresh existing, append new
    data["records"] = sorted(by_bvid.values(), key=lambda r: r["bvid"])
    return data


def agg(rows, key, flt=None):
    vals = sorted(r[key] for r in rows if r.get(key) is not None and (flt is None or flt(r)))
    if not vals:
        return None
    n = len(vals)
    return {
        "n": n,
        "median": vals[n // 2],
        "p10": vals[max(0, n // 10)],
        "p90": vals[min(n - 1, n - n // 10)],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="harvest fetch/transcript metrics")
    ap.add_argument("workspace", help="queue workspace dir (contains workspaces/BV*/)")
    ap.add_argument("--source", required=True, help="source label, e.g. 3blue1brown, manshi")
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT), help=f"datasets dir (default {DEFAULT_OUT})")
    args = ap.parse_args()

    ws = Path(args.workspace) / "workspaces"
    if not ws.is_dir():
        print(f"no workspaces dir under {args.workspace}", file=sys.stderr)
        return 2
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    fetch_rows, tr_rows = [], []
    for d in sorted(ws.iterdir()):
        if not d.is_dir() or not d.name.startswith("BV"):
            continue
        bvid = d.name
        audio, meta_p = d / "audio.mp4", d / "metadata.json"
        if meta_p.is_file():
            try:
                meta = json.loads(meta_p.read_text(encoding="utf-8"))
            except Exception:
                meta = {}
        else:
            meta = {}

        if audio.is_file():
            row = {
                "bvid": bvid,
                "source": args.source,
                "title": meta.get("title", ""),
                "duration_s": meta.get("duration_sec"),
                "audio_bytes": meta.get("content_length") or audio.stat().st_size,
                "download_s": None,
                "speed_mb_s": None,
                "reliable": False,
            }
            row["audio_mb"] = round(row["audio_bytes"] / 1048576, 2)
            if row["duration_s"]:
                row["audio_mb_per_min"] = round(
                    row["audio_mb"] / (row["duration_s"] / 60), 3
                )
            st = audio.stat()
            birth = linux_birth(audio)
            if birth:
                dl = st.st_mtime - birth
                if 0 < dl <= MAX_PLAUSIBLE_DL:
                    row.update(
                        reliable=True,
                        download_s=round(dl, 1),
                        speed_mb_s=round(row["audio_mb"] / dl, 2),
                    )
            row["fetched_at"] = int(st.st_mtime)
            fetch_rows.append(row)

        md = d / "faster-whisper" / "metrics.md"
        if md.is_file():
            m = parse_metrics_md(md)
            if m:
                row = {
                    "bvid": bvid,
                    "source": args.source,
                    "title": meta.get("title", ""),
                    "duration_s": meta.get("duration_sec") or m.get("duration_s"),
                    "mode": m.get("mode"),
                    "wav_mb": m.get("wav_mb"),
                    "transcode_s": m.get("transcode_s"),
                    "asr_s": m.get("asr_s"),
                    "rtf": m.get("rtf"),
                    "chars": m.get("chars"),
                }
                if row["asr_s"] and row["duration_s"]:
                    row["asr_sec_per_audio_min"] = round(
                        row["asr_s"] / (row["duration_s"] / 60), 2
                    )
                row["transcribed_at"] = int(md.stat().st_mtime)
                tr_rows.append(row)

    fetch_path = out_dir / "fetch-metrics.json"
    tr_path = out_dir / "transcript-metrics.json"
    fetch_path.write_text(
        json.dumps(load_merge(fetch_path, fetch_rows), ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    tr_path.write_text(
        json.dumps(load_merge(tr_path, tr_rows), ensure_ascii=False, indent=1),
        encoding="utf-8",
    )

    print(f"source={args.source}: {len(fetch_rows)} fetch, {len(tr_rows)} transcript records")
    rel = [r for r in fetch_rows if r["reliable"]]
    s = agg(rel, "speed_mb_s")
    if s:
        print(f"  download speed MB/s: median={s['median']} p10={s['p10']} p90={s['p90']} (n={s['n']})")
    s = agg(fetch_rows, "audio_mb_per_min")
    if s:
        print(f"  audio MB/video-min: median={s['median']}")
    s = agg(tr_rows, "rtf")
    if s:
        print(f"  ASR RTF: median={s['median']} ({1/s['median']:.0f}x realtime) p90={s['p90']}")
    s = agg(tr_rows, "asr_sec_per_audio_min")
    if s:
        print(f"  ASR sec/video-min: median={s['median']}")
    print(f"-> {fetch_path}\n-> {tr_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
