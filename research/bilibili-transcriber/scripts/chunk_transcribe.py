#!/usr/bin/env python3
"""
chunk_transcribe.py — Silence-aware chunked transcription for whisper ASR.

Splits a WAV file at natural silence boundaries (via ffmpeg silencedetect),
transcribes each chunk in parallel, and concatenates the results directly.
No overlap, no deduplication — silence boundaries guarantee sentence
integrity.

Chunking strategies (selectable via --strategy):
  dp        — Dynamic programming: globally optimal partition that minimizes
              total cost = α × |chunk_dur - target| + β × (1 / silence_dur)
              (default)
  greedy    — Greedy nearest-silence: picks the closest silence to each
              target boundary independently (fast, local optimum)
  weighted  — Weighted scoring: score = α/dist + β × silence_dur
  threshold — Filter silences by min duration, then greedy nearest

Usage:
  python3 <SKILL_DIR>/scripts/chunk_transcribe.py \
    --wav <wav-path> \
    --endpoint <url> \
    --model <model-id> \
    [--lang zh] \
    [--chunk-sec 600] \
    [--silence-db -30] \
    [--silence-min-dur 0.5] \
    [--strategy dp] \
    [--min-silence-score 1.5] \
    [--max-filesize-mb 25] \
    [--parallel N] \
    [--output <path>]

Environment variables (fallbacks if CLI flags not given):
  WHISPER_ENDPOINT  — API base URL (e.g. http://host:30567/v1)
  WHISPER_MODEL     — model ID (e.g. atom)
  WHISPER_LANG      — language hint (default: zh)
"""

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import time
import wave

import numpy as np


# ── Audio helpers (pure Python — no external binary required) ──

SAMPLE_RATE = 16000


def _open_wav(path: str) -> wave.Wave_read:
    """Open a WAV file with stdlib wave, enforcing the expected format."""
    try:
        w = wave.open(path, "rb")
    except (wave.Error, OSError) as e:
        print(f"ERROR: Not a readable WAV file: {path} ({e})", file=sys.stderr)
        sys.exit(1)
    if w.getframerate() != SAMPLE_RATE or w.getnchannels() != 1:
        print(
            f"ERROR: Expected {SAMPLE_RATE}Hz mono WAV, got "
            f"{w.getframerate()}Hz/{w.getnchannels()}ch", file=sys.stderr)
        sys.exit(1)
    return w


def get_duration(path: str) -> float:
    """Get audio duration in seconds from the WAV header (no probe binary)."""
    with _open_wav(path) as w:
        return w.getnframes() / w.getframerate()


def get_filesize_mb(path: str) -> float:
    return os.path.getsize(path) / (1024 * 1024)


def _window_silence_mask(path: str, silence_db: float, min_dur: float,
                         win_sec: float = 0.05, hop_sec: float = 0.02) -> tuple:
    """
    Compute a per-window boolean mask: True where the window's RMS amplitude
    (in dBFS) is below silence_db. Windows are win_sec long, hop_sec apart.

    Returns (mask, hop_sec) — window i covers [i*hop_sec, i*hop_sec+win_sec)
    seconds, so timestamps are derived from hop_sec.
    """
    threshold = 10 ** (silence_db / 20.0)  # linear amplitude (full-scale = 1.0)
    with _open_wav(path) as w:
        data = w.readframes(w.getnframes())
    samples = np.frombuffer(data, dtype="<i2").astype(np.float32) / 32768.0

    win = max(1, int(win_sec * SAMPLE_RATE))
    hop = max(1, int(hop_sec * SAMPLE_RATE))
    n_wins = max(0, (len(samples) - win) // hop + 1)
    mask = np.zeros(n_wins, dtype=bool)
    for i in range(n_wins):
        seg = samples[i * hop:i * hop + win]
        rms = float(np.sqrt(np.mean(seg * seg)))
        mask[i] = rms < threshold
    return mask, hop_sec


def detect_silence(path: str, silence_db: float = -30,
                   min_dur: float = 0.5) -> list:
    """
    Silence-aware pause detection (pure Python path)
    (drop-in for the former "ffmpeg silencedetect" pipeline). Returns a list of (midpoint, duration) tuples — each
    silence segment is a candidate cut point.
    """
    mask, hop_sec = _window_silence_mask(path, silence_db, min_dur)
    if not mask.any():
        return []

    # Contiguous runs of True windows => silence segments
    segs = []
    in_silence = False
    start = 0
    for i, m in enumerate(mask):
        if m and not in_silence:
            in_silence = True
            start = i
        elif not m and in_silence:
            in_silence = False
            if (i - start) * hop_sec >= min_dur:
                segs.append((start, i))
    if in_silence and (len(mask) - start) * hop_sec >= min_dur:
        segs.append((start, len(mask)))

    return [((s + e) / 2 * hop_sec, (e - s) * hop_sec) for s, e in segs]


# ── Chunking strategies ──

def _chunk_cost(chunk_dur: float, target: int, silence_dur: float) -> float:
    """
    Cost of a single chunk. Lower is better.
    - Penalize deviation from target duration
    - Reward longer silence at the cut point (cleaner boundary)
    """
    alpha = 1.0  # weight for duration deviation
    beta = 2.0   # weight for silence quality
    # Normalize duration deviation by target so alpha is scale-free
    dur_penalty = alpha * (abs(chunk_dur - target) / target)
    # silence_dur is in seconds; longer silence = lower cost
    silence_bonus = beta * (1.0 / (1.0 + silence_dur))
    return dur_penalty + silence_bonus


def chunk_dp(duration: float, silences: list, target: int = 600,
             tolerance: int = 60, **kw) -> list:
    """
    Dynamic programming: find the globally optimal partition.
    Minimizes sum of _chunk_cost over all chunks.

    Candidate cut points are silence midpoints within tolerance of any
    multiple of target. DP guarantees the best total cost across all
    possible combinations.
    """
    # Build candidate cut points: silence midpoints within tolerance
    candidates = [0.0]
    for mid, dur in silences:
        # Only keep silences that could be useful (within tolerance of some target multiple)
        if any(abs(mid - k * target) <= tolerance for k in range(1, int(duration / target) + 2)):
            candidates.append(mid)
    if duration not in candidates:
        candidates.append(duration)
    candidates = sorted(set(candidates))

    # DP: dp[i] = (min_cost_to_reach_candidates[i], prev_index)
    # dp[0] = (0, -1) — starting point
    n = len(candidates)
    dp = [(float('inf'), -1)] * n
    dp[0] = (0.0, -1)

    for i in range(1, n):
        ci = candidates[i]
        # Try all previous candidates j where chunk dur is reasonable
        for j in range(i - 1, -1, -1):
            cj = candidates[j]
            chunk_dur = ci - cj
            if chunk_dur < target - tolerance:
                continue  # too short, skip
            if chunk_dur > target + tolerance:
                break  # candidates sorted, further j only makes it longer
            # Find silence duration at this cut point
            sil_dur = 0.0
            for mid, dur in silences:
                if abs(mid - ci) < 0.5:
                    sil_dur = max(sil_dur, dur)
            cost = dp[j][0] + _chunk_cost(chunk_dur, target, sil_dur)
            if cost < dp[i][0]:
                dp[i] = (cost, j)

    # Backtrack to find the partition
    if dp[n - 1][1] == -1:
        # Fallback: no valid partition found, use simple greedy
        return chunk_greedy(duration, [(m, d) for m, d in silences],
                            target, tolerance, **kw)

    cuts = []
    idx = n - 1
    while idx > 0:
        idx = dp[idx][1]
        if idx > 0:
            cuts.append(candidates[idx])
    cuts.reverse()

    chunks = []
    prev = 0.0
    for cut in cuts:
        chunks.append((prev, cut))
        prev = cut
    chunks.append((prev, duration))
    return chunks


def chunk_greedy(duration: float, silences: list, target: int = 600,
                 tolerance: int = 60, **kw) -> list:
    """
    Greedy: for each target boundary, pick the nearest silence midpoint.
    Simple and fast, but local optimum.
    """
    midpoints = [m for m, _ in silences]
    chunks = []
    pos = 0.0
    while pos < duration:
        target_end = pos + target
        if target_end >= duration:
            chunks.append((pos, duration))
            break
        candidates = [m for m in midpoints if abs(m - target_end) <= tolerance]
        end = min(candidates, key=lambda m: abs(m - target_end)) if candidates else target_end
        if end <= pos:
            end = target_end
        chunks.append((pos, end))
        pos = end
    return chunks


def chunk_weighted(duration: float, silences: list, target: int = 600,
                   tolerance: int = 60, alpha: float = 1.0,
                   beta: float = 2.0, **kw) -> list:
    """
    Weighted scoring: score = alpha / dist + beta * silence_dur.
    Picks the highest-scoring silence near each target boundary.
    """
    chunks = []
    pos = 0.0
    while pos < duration:
        target_end = pos + target
        if target_end >= duration:
            chunks.append((pos, duration))
            break
        best_score = -1.0
        best_end = target_end
        for mid, dur in silences:
            dist = abs(mid - target_end)
            if dist > tolerance:
                continue
            score = alpha / (1.0 + dist) + beta * dur
            if score > best_score:
                best_score = score
                best_end = mid
        if best_end <= pos:
            best_end = target_end
        chunks.append((pos, best_end))
        pos = best_end
    return chunks


def chunk_threshold(duration: float, silences: list, target: int = 600,
                    tolerance: int = 60,
                    min_silence_score: float = 1.5, **kw) -> list:
    """
    Threshold filter: discard silences shorter than min_silence_score seconds,
    then greedy nearest-silence on the remaining candidates.
    """
    filtered = [(m, d) for m, d in silences if d >= min_silence_score]
    if not filtered:
        # No long silences found, fall back to all silences
        filtered = silences
    return chunk_greedy(duration, filtered, target, tolerance)


STRATEGIES = {
    "dp": chunk_dp,
    "greedy": chunk_greedy,
    "weighted": chunk_weighted,
    "threshold": chunk_threshold,
}


# ── Transcription helpers ──

def create_chunk(wav_path: str, chunk_path: str, start: float, duration: float):
    """Extract a chunk from the WAV file by slicing frames (pure Python)."""
    with _open_wav(wav_path) as w:
        rate = w.getframerate()
        n_frames = w.getnframes()
        start_frame = max(0, int(start * rate))
        end_frame = min(n_frames, int((start + duration) * rate))
        w.setpos(start_frame)
        data = w.readframes(end_frame - start_frame)

    with wave.open(chunk_path, "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)  # s16
        out.setframerate(rate)
        out.writeframes(data)


def transcribe_chunk(chunk_path: str, endpoint: str, model: str,
                     lang: str) -> tuple:
    """
    Send a chunk to the whisper ASR service.
    Returns (text, segments) where segments is from verbose_json.
    """
    result = subprocess.run(
        ["curl", "-s", "--noproxy", "*", "--max-time", "300",
         "-X", "POST", f"{endpoint}/audio/transcriptions",
         "-F", f"file=@{chunk_path}",
         "-F", f"model={model}",
         "-F", f"language={lang}",
         "-F", "response_format=verbose_json"],
        capture_output=True, text=True
    )
    try:
        data = json.loads(result.stdout)
        return data.get("text", ""), data.get("segments", [])
    except json.JSONDecodeError:
        print(f"  [error] ASR failed for {os.path.basename(chunk_path)}: "
              f"{result.stdout[:200]}", file=sys.stderr)
        return "", []


def flag_low_confidence(segments: list) -> list:
    """
    Flag segments with low confidence for review.
    avg_logprob < -1.0 → low confidence
    compression_ratio > 2.4 → likely repetition/hallucination
    Returns list of (segment_index, issue) tuples.
    """
    issues = []
    for i, seg in enumerate(segments):
        lp = seg.get("avg_logprob")
        cr = seg.get("compression_ratio")
        if lp is not None and lp < -1.0:
            issues.append((i, f"low_logprob={lp:.3f}"))
        if cr is not None and cr > 2.4:
            issues.append((i, f"high_compression={cr:.3f}"))
    return issues


# ── Main ──

def main():
    parser = argparse.ArgumentParser(
        description="Silence-aware chunked transcription for whisper ASR")
    parser.add_argument("--wav", required=True, help="Path to WAV file")
    parser.add_argument("--endpoint",
                        default=os.environ.get("WHISPER_ENDPOINT", ""),
                        help="ASR API base URL")
    parser.add_argument("--model",
                        default=os.environ.get("WHISPER_MODEL", ""),
                        help="ASR model ID")
    parser.add_argument("--lang",
                        default=os.environ.get("WHISPER_LANG", "zh"),
                        help="Language hint")
    parser.add_argument("--chunk-sec", type=int, default=600,
                        help="Target chunk duration in seconds (default: 600)")
    parser.add_argument("--silence-db", type=float, default=-30,
                        help="Silence detection threshold in dB (default: -30)")
    parser.add_argument("--silence-min-dur", type=float, default=0.5,
                        help="Min silence duration for detection in seconds (default: 0.5)")
    parser.add_argument("--tolerance", type=int, default=60,
                        help="Search window for silence boundary (default: 60s)")
    parser.add_argument("--strategy", choices=list(STRATEGIES.keys()),
                        default="dp",
                        help="Chunking strategy (default: dp)")
    parser.add_argument("--min-silence-score", type=float, default=1.5,
                        help="Min silence duration for threshold strategy (default: 1.5s)")
    parser.add_argument("--max-filesize-mb", type=float, default=25.0,
                        help="Max WAV file size in MB before chunking (default: 25)")
    parser.add_argument("--parallel", type=int, default=4,
                        help="Max parallel transcription requests (default: 4)")
    parser.add_argument("--output", default=None,
                        help="Output file path (default: stdout)")
    parser.add_argument("--chunk-dir", default=None,
                        help="Directory for chunk files (default: temp)")
    args = parser.parse_args()

    if not args.endpoint:
        print("ERROR: --endpoint or WHISPER_ENDPOINT env var required",
              file=sys.stderr)
        sys.exit(1)
    if not args.model:
        print("ERROR: --model or WHISPER_MODEL env var required",
              file=sys.stderr)
        sys.exit(1)

    wav_path = args.wav
    if not os.path.isfile(wav_path):
        print(f"ERROR: WAV file not found: {wav_path}", file=sys.stderr)
        sys.exit(1)

    filesize_mb = get_filesize_mb(wav_path)
    duration = get_duration(wav_path)

    print(f"[info] WAV: {wav_path} ({filesize_mb:.1f}MB, {duration:.1f}s)")

    # ── Decide: chunk or direct ──
    if filesize_mb <= args.max_filesize_mb:
        print(f"[info] File size ≤ {args.max_filesize_mb}MB, transcribing directly")
        text, segments = transcribe_chunk(
            wav_path, args.endpoint, args.model, args.lang)
        print(f"[info] Transcription: {len(text)} chars, {len(segments)} segments")

        issues = flag_low_confidence(segments)
        if issues:
            print(f"[info] {len(issues)} low-confidence segments flagged:")
            for idx, issue in issues:
                seg_text = segments[idx].get("text", "").strip()[:60]
                print(f"  seg[{idx}] {issue}: {seg_text}")

        _write_output(text, args.output)
        return

    # ── Silence-aware chunking ──
    print(f"[info] File size > {args.max_filesize_mb}MB, using silence-aware chunking")
    print(f"[info] Detecting silence boundaries (threshold={args.silence_db}dB, "
          f"min_dur={args.silence_min_dur}s)...")

    silences = detect_silence(
        wav_path, args.silence_db, args.silence_min_dur)
    print(f"[info] Found {len(silences)} silence segments")

    strategy_fn = STRATEGIES[args.strategy]
    print(f"[info] Chunking strategy: {args.strategy}")

    chunks = strategy_fn(
        duration, silences, target=args.chunk_sec,
        tolerance=args.tolerance,
        min_silence_score=args.min_silence_score)

    # Report chunk plan with silence quality
    print(f"[info] {len(chunks)} chunks (target={args.chunk_sec}s, "
          f"tolerance={args.tolerance}s):")
    silence_midpoints = {round(m, 1): d for m, d in silences}
    for i, (start, end) in enumerate(chunks):
        actual = end - start
        # Find silence duration at the cut point
        cut_sil_dur = silence_midpoints.get(round(end, 1), 0.0)
        if end >= duration:
            marker = "end"
        elif cut_sil_dur > 0:
            marker = f"silence({cut_sil_dur:.1f}s)"
        else:
            marker = "fixed"
        print(f"  chunk_{i:03d}: {start:7.1f}s - {end:7.1f}s "
              f"({actual:5.1f}s) [{marker}]")

    chunk_dir = args.chunk_dir or os.path.join(
        os.path.dirname(wav_path), "chunks")
    os.makedirs(chunk_dir, exist_ok=True)

    # Create chunks
    chunk_paths = []
    for i, (start, end) in enumerate(chunks):
        actual = end - start
        chunk_path = os.path.join(chunk_dir, f"chunk_{i:03d}.wav")
        create_chunk(wav_path, chunk_path, start, actual)
        chunk_paths.append((i, start, end, chunk_path))

    # Transcribe — try parallel, fall back to serial
    t_start = time.time()
    results = [None] * len(chunk_paths)

    if args.parallel > 1 and len(chunk_paths) > 1:
        print(f"\n[info] Parallel transcription (max {args.parallel} workers)")
        try:
            with concurrent.futures.ThreadPoolExecutor(
                    max_workers=args.parallel) as executor:
                future_to_idx = {
                    executor.submit(
                        transcribe_chunk, c[3],
                        args.endpoint, args.model, args.lang
                    ): c[0]
                    for c in chunk_paths
                }
                for future in concurrent.futures.as_completed(future_to_idx):
                    cidx = future_to_idx[future]
                    try:
                        text, segments = future.result()
                        results[cidx] = (cidx, chunk_paths[cidx][1],
                                         chunk_paths[cidx][2], text, segments)
                        n_issues = len(flag_low_confidence(segments))
                        print(f"  [asr] chunk_{cidx:03d} OK ({len(text)} chars, "
                              f"{len(segments)} segs, {n_issues} low-conf)")
                    except Exception as e:
                        print(f"  [error] chunk_{cidx:03d} failed: {e}",
                              file=sys.stderr)
                        results[cidx] = (cidx, chunk_paths[cidx][1],
                                         chunk_paths[cidx][2], "", [])
        except Exception as e:
            print(f"[warn] Parallel failed ({e}), falling back to serial",
                  file=sys.stderr)
            args.parallel = 1

    if args.parallel <= 1 or len(chunk_paths) <= 1:
        print("\n[info] Serial transcription")
        for cidx, c_start, c_end, c_path in chunk_paths:
            chunk_name = os.path.basename(c_path)
            size_mb = get_filesize_mb(c_path)
            print(f"  [asr] {chunk_name} ({size_mb:.1f}MB)...", end=" ",
                  flush=True)
            t0 = time.time()
            text, segments = transcribe_chunk(
                c_path, args.endpoint, args.model, args.lang)
            t1 = time.time()
            n_issues = len(flag_low_confidence(segments))
            print(f"OK ({t1-t0:.1f}s, {len(text)} chars, "
                  f"{len(segments)} segs, {n_issues} low-conf)")
            results[cidx] = (cidx, c_start, c_end, text, segments)

    t_total = time.time() - t_start
    print(f"\n[info] Total ASR time: {t_total:.1f}s")

    # ── Direct concatenation (no overlap, no dedup) ──
    print("\n[concat] Direct concatenation at silence boundaries")
    merged_text = ""
    all_issues = []
    for entry in results:
        if entry:
            cidx, c_start, c_end, text, segments = entry
            merged_text += text
            for i, seg in enumerate(segments):
                lp = seg.get("avg_logprob")
                cr = seg.get("compression_ratio")
                if (lp is not None and lp < -1.0) or \
                   (cr is not None and cr > 2.4):
                    abs_start = c_start + seg.get("start", 0)
                    seg_text = seg.get("text", "").strip()[:80]
                    issue_parts = []
                    if lp is not None and lp < -1.0:
                        issue_parts.append(f"logprob={lp:.3f}")
                    if cr is not None and cr > 2.4:
                        issue_parts.append(f"compression={cr:.3f}")
                    all_issues.append(
                        f"  [{abs_start:.1f}s] {', '.join(issue_parts)}: {seg_text}")

    print(f"[done] Merged transcript: {len(merged_text)} chars")

    if all_issues:
        print(f"\n[quality] {len(all_issues)} low-confidence segments:")
        for issue in all_issues:
            print(issue)

    _write_output(merged_text, args.output)

    # Save individual chunk transcripts with segment metadata for debugging
    debug_dir = os.path.join(chunk_dir, "transcripts")
    os.makedirs(debug_dir, exist_ok=True)
    for entry in results:
        if entry:
            cidx, c_start, c_end, text, segments = entry
            with open(os.path.join(debug_dir, f"chunk_{cidx:03d}.json"), "w") as f:
                json.dump({
                    "chunk_index": cidx,
                    "start_sec": c_start,
                    "end_sec": c_end,
                    "text": text,
                    "segments": segments,
                }, f, ensure_ascii=False, indent=2)
    print(f"[done] Per-chunk transcripts: {debug_dir}")


def _write_output(text: str, output_path):
    if output_path:
        with open(output_path, "w") as f:
            f.write(text)
        print(f"[done] Saved to: {output_path}")
    else:
        print("\n--- TRANSCRIPT ---")
        print(text)


if __name__ == "__main__":
    main()
