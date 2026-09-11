#!/usr/bin/env python3
"""pipeline-queue.py — producer/consumer transcription queue.

Two independent worker pools connected by a directory queue, fully decoupled:

    manifest ──► [fetch workers ×N] ──► queues/ready ──► [asr workers ×M] ──► transcripts/

- fetch (bilibili API + aria2c download) and ASR (whisper) never wait for each
  other; fetch runs ahead so ASR always has the next audio ready.
- Jobs are claimed by atomic os.rename (mutual exclusion without locks).
- Crash-safe and resumable: on startup, in-flight jobs are requeued; completed
  transcripts are skipped, so the queue is idempotent.
- status.jsonl: one JSON line per terminal state (ok / fetch_failed /
  transcribe_failed), same schema as run-queue.sh.
- ASR workers default to 1 to keep the shared whisper service single-stream;
  raise with --asr-workers only if the service can take it.

Usage:
  pipeline-queue.py <workspace-dir> <manifest.json> [--fetch-workers N] [--asr-workers N]
                    [--fetch-cmd CMD] [--transcribe-cmd CMD]

--fetch-cmd / --transcribe-cmd default to the skill's fetch.py / transcribe.sh
and exist for testing (stub commands) and advanced use.

Environment: same requirements as run-queue.sh — PATH must include a python
with requests+numpy (batch venv), and runtime.conf must point at the whisper
endpoint. Commands run with stdin=/dev/null (see the stdin-swallow lesson).
"""

import argparse
import glob
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

Q_PENDING, Q_READY, Q_FAILED, Q_DONE = "pending", "ready", "failed", "done"
STOP = threading.Event()
LOG_LOCK = threading.Lock()


def log(worker: str, msg: str):
    with LOG_LOCK:
        print(f"[{worker}] {msg}", flush=True)


def write_status(base: Path, bvid: str, status: str):
    line = json.dumps({"bvid": bvid, "status": status}, ensure_ascii=False)
    with LOG_LOCK:
        with open(base / "status.jsonl", "a", encoding="utf-8") as f:
            f.write(line + "\n")


def transcript_exists(base: Path, bvid: str) -> bool:
    return bool(glob.glob(str(base / "references" / "transcripts" / "bilibili" / f"*-{bvid}" / "transcript.md")))


def claim(qdir: Path, name: str, tmp_prefix: str) -> Path | None:
    """Atomically claim job `name` in qdir by renaming it to tmp_prefix+name.
    Returns the claimed path, or None if another worker won the race."""
    src, dst = qdir / name, qdir / f"{tmp_prefix}{name}"
    try:
        os.rename(src, dst)
        return dst
    except FileNotFoundError:
        return None


def unclaim(claimed: Path, qdir: Path):
    """Return a claimed job (name = prefix+bvid) to its queue."""
    prefix = claimed.name[: claimed.name.index("BV")]
    try:
        os.rename(claimed, qdir / claimed.name[len(prefix):])
    except FileNotFoundError:
        pass


class Queue:
    def __init__(self, base: Path):
        self.base = base
        self.q = base / "queues"
        for d in (Q_PENDING, Q_READY, Q_FAILED, Q_DONE):
            (self.q / d).mkdir(parents=True, exist_ok=True)
        (base / "workspaces").mkdir(exist_ok=True)

    def requeue_inflight(self):
        """Return jobs left in claiming state by a crashed run to their queues.
        claim() renames in place with a prefix, so sweep prefixed names."""
        n = 0
        for p in (self.q / Q_PENDING).glob("fetching-*"):
            os.rename(p, self.q / Q_PENDING / p.name[len("fetching-"):]); n += 1
        for p in (self.q / Q_READY).glob("asr-*"):
            os.rename(p, self.q / Q_READY / p.name[len("asr-"):]); n += 1
        if n:
            log("queue", f"requeued {n} in-flight job(s) from previous run")
        # failed jobs are NOT requeued automatically — inspect queues/failed/
        for p in (self.q / Q_FAILED).glob("*.err"):
            log("queue", f"prior failure on record: {p.name}")


def _run(cmd: list[str], cwd: Path, log_path: Path) -> tuple[int, str]:
    """Run cmd with stdin=/dev/null, tee output to log_path.
    Returns (returncode, last 500 chars of output) for error reporting."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(cmd, cwd=cwd, stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, timeout=3600)
    out = (proc.stdout or "") + (proc.stderr or "")
    log_path.write_text(out, encoding="utf-8", errors="replace")
    return proc.returncode, out[-500:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("manifest")
    ap.add_argument("--fetch-workers", type=int, default=2)
    ap.add_argument("--asr-workers", type=int, default=1)
    ap.add_argument("--fetch-cmd", default=None,
                    help="override fetch command (default: skill fetch.py <url> --json --output-dir <dir>)")
    ap.add_argument("--transcribe-cmd", default=None,
                    help="override transcribe command (default: skill transcribe.sh <dir>)")
    ap.add_argument("--poll", type=float, default=2.0)
    args = ap.parse_args()

    base = Path(args.workspace).resolve()
    skill_dir = Path(__file__).resolve().parent.parent
    fetch_cmd = args.fetch_cmd
    if fetch_cmd is None:
        fetch_cmd = (f"python3 {skill_dir}/../fetch-article/scripts/fetch.py "
                     "https://www.bilibili.com/video/{bv}/ --json --output-dir {dir}")
    tr_cmd = args.transcribe_cmd
    if tr_cmd is None:
        tr_cmd = f"bash {skill_dir}/scripts/transcribe.sh {{dir}}"

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    manifest.sort(key=lambda v: v["duration"])  # shortest first, same as run-queue.sh

    q = Queue(base)
    q.requeue_inflight()

    # seed pending/ with jobs that still need work (idempotent: skip existing
    # pending/ready entries and finished transcripts)
    pending = {p.name for p in (q.q / Q_PENDING).glob("BV*")}
    ready = {p.name for p in (q.q / Q_READY).glob("BV*")}
    failed = {p.stem for p in (q.q / Q_FAILED).glob("BV*")}
    total = len(manifest)
    for v in manifest:
        bv = v["bvid"]
        if bv in pending or bv in ready:
            continue
        if transcript_exists(base, bv):
            continue  # already transcribed (resume across runs)
        (q.q / Q_PENDING / bv).write_text(v["title"], encoding="utf-8")
    todo = len(list((q.q / Q_PENDING).glob("BV*")))
    log("queue", f"{total} in manifest, {todo} to fetch, "
                f"{len(ready)} fetched-awaiting-ASR, {len(failed)} failed-on-record")

    def sigterm(_sig, _frm):
        STOP.set()
    signal.signal(signal.SIGTERM, sigterm)
    signal.signal(signal.SIGINT, sigterm)

    stop_evt = STOP
    stats = {"ok": 0, "fetch_failed": 0, "transcribe_failed": 0}
    stats_lock = threading.Lock()

    def fetcher(wid: int):
        name = f"fetch-{wid}"
        while not stop_evt.is_set():
            bv = None
            # claim one pending job
            for p in sorted((q.q / Q_PENDING).glob("BV*")):
                if claim(q.q / Q_PENDING, p.name, "fetching-") is not None:
                    bv = p.name
                    break
            if bv is None:
                time.sleep(args.poll)
                continue
            ws = base / "workspaces" / bv
            ws.mkdir(parents=True, exist_ok=True)
            cmd = fetch_cmd.format(bv=bv, dir=ws).split()
            log(name, f"{bv} fetching...")
            rc, tail = _run(cmd, base, base / "workspaces" / f"{bv}.fetch2.log")
            if rc == 0:
                os.rename(q.q / Q_PENDING / f"fetching-{bv}", q.q / Q_READY / bv)
                log(name, f"{bv} fetched → ready")
            else:
                err = q.q / Q_FAILED / f"{bv}.err"
                err.write_text(f"fetch rc={rc}\n{tail}", encoding="utf-8")
                try:
                    os.remove(q.q / Q_PENDING / f"fetching-{bv}")
                except FileNotFoundError:
                    pass
                write_status(base, bv, "fetch_failed")
                with stats_lock:
                    stats["fetch_failed"] += 1
                log(name, f"{bv} FETCH-FAILED: {tail[:120]}")

    def transcriber(wid: int):
        name = f"asr-{wid}"
        while not stop_evt.is_set():
            bv = None
            for p in sorted((q.q / Q_READY).glob("BV*")):
                if claim(q.q / Q_READY, p.name, "asr-") is not None:
                    bv = p.name
                    break
            if bv is None:
                # nothing ready — quit only when producers are done and queue drained
                if stop_evt.is_set():
                    break
                time.sleep(args.poll)
                continue
            ws = base / "workspaces" / bv
            cmd = tr_cmd.format(bv=bv, dir=ws).split()
            log(name, f"{bv} transcribing...")
            rc, tail = _run(cmd, base, base / "workspaces" / f"{bv}.tr2.log")
            if rc == 0:
                os.rename(q.q / Q_READY / f"asr-{bv}", q.q / Q_DONE / bv)
                # cleanup intermediate WAVs (same as run-queue.sh)
                for wav in ws.glob("*.wav"):
                    wav.unlink(missing_ok=True)
                for wav in (ws / "faster-whisper" / "chunks").glob("*.wav"):
                    wav.unlink(missing_ok=True)
                write_status(base, bv, "ok")
                with stats_lock:
                    stats["ok"] += 1
                log(name, f"{bv} OK")
            else:
                err = q.q / Q_FAILED / f"{bv}.tr-err"
                err.write_text(f"transcribe rc={rc}\n{tail}", encoding="utf-8")
                try:
                    os.remove(q.q / Q_READY / f"asr-{bv}")
                except FileNotFoundError:
                    pass
                write_status(base, bv, "transcribe_failed")
                with stats_lock:
                    stats["transcribe_failed"] += 1
                log(name, f"{bv} TRANSCRIBE-FAILED: {tail[:120]}")

    threads = []
    for i in range(max(1, args.fetch_workers)):
        threads.append(threading.Thread(target=fetcher, args=(i,), daemon=True))
    for i in range(max(1, args.asr_workers)):
        threads.append(threading.Thread(target=transcriber, args=(i,), daemon=True))
    for t in threads:
        t.start()

    # main thread: wait for completion (all queues drained) or stop
    try:
        while True:
            time.sleep(args.poll)
            if stop_evt.is_set():
                break
            n_pend = len(list((q.q / Q_PENDING).glob("BV*"))) + len(list((q.q / Q_PENDING).glob("fetching-*")))
            n_ready = len(list((q.q / Q_READY).glob("BV*"))) + len(list((q.q / Q_READY).glob("asr-*")))
            if n_pend == 0 and n_ready == 0:
                # producers finished and consumers drained — one grace poll for stragglers
                time.sleep(args.poll * 2)
                n_ready = len(list((q.q / Q_READY).glob("BV*"))) + len(list((q.q / Q_READY).glob("asr-*")))
                if n_ready == 0:
                    break
    finally:
        stop_evt.set()
        for t in threads:
            t.join(timeout=10)

    print(f"QUEUE DONE: ok={stats['ok']} fetch_failed={stats['fetch_failed']} "
          f"transcribe_failed={stats['transcribe_failed']} total={total}", flush=True)
    return 0 if (stats["fetch_failed"] == 0 and stats["transcribe_failed"] == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
