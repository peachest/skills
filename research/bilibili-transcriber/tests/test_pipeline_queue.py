"""pipeline-queue.py — producer/consumer queue state machine tests.

Covers: atomic claim mutual exclusion, crash requeue, transcript-skip
idempotency, and a stub-command end-to-end run (no network, no whisper).
"""

import importlib.util
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "pipeline-queue.py"
spec = importlib.util.spec_from_file_location("pq", SCRIPT)
pq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pq)


def make_queue(tmp_path: Path) -> pq.Queue:
    return pq.Queue(tmp_path)


def test_claim_is_mutually_exclusive(tmp_path):
    qd = tmp_path / "pending"
    qd.mkdir()
    (qd / "BV1abc").write_text("t")
    assert pq.claim(qd, "BV1abc", "fetching-") is not None
    # second claim of the same name fails (winner already renamed it)
    assert pq.claim(qd, "BV1abc", "fetching-") is None
    assert (qd / "fetching-BV1abc").exists()


def test_claim_two_workers_one_job(tmp_path):
    qd = tmp_path / "pending"
    qd.mkdir()
    for bv in ("BV1a", "BV1b"):
        (qd / bv).write_text("t")
    got = []
    lock = threading.Lock()

    def worker(tag):
        c = pq.claim(qd, "BV1a", f"{tag}-")
        if c is not None:
            with lock:
                got.append(tag)

    ts = [threading.Thread(target=worker, args=(f"w{i}",)) for i in range(4)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert len(got) == 1  # exactly one winner


def test_requeue_inflight_after_crash(tmp_path):
    q = make_queue(tmp_path)
    (q.q / pq.Q_PENDING / "BV1x").write_text("t")
    (q.q / pq.Q_PENDING / "fetching-BV1y").write_text("t")  # crashed mid-fetch
    (q.q / pq.Q_READY / "asr-BV1z").write_text("t")          # crashed mid-ASR
    q.requeue_inflight()
    assert (q.q / pq.Q_PENDING / "BV1y").exists()
    assert (q.q / pq.Q_READY / "BV1z").exists()
    assert not list((q.q / pq.Q_PENDING).glob("fetching-*"))
    assert not list((q.q / pq.Q_READY).glob("asr-*"))


def test_seed_skips_existing_transcripts(tmp_path):
    q = make_queue(tmp_path)
    # pretend BV1done already has a transcript
    tdir = tmp_path / "references" / "transcripts" / "bilibili" / "20260101-某标题-BV1done"
    tdir.mkdir(parents=True)
    (tdir / "transcript.md").write_text("x")
    assert pq.transcript_exists(tmp_path, "BV1done")
    assert not pq.transcript_exists(tmp_path, "BV1todo")


def test_end_to_end_with_stubs(tmp_path):
    """Full pipeline with stub fetch/transcribe: 3 videos, verify decoupling
    artifacts (ready/ drains to done/, status.jsonl correct, idempotent rerun)."""
    ws = tmp_path / "ws"
    ws.mkdir()
    manifest = [
        {"bvid": f"BV1stub{i}", "title": f"stub{i}", "duration": 60 + i, "created": 0}
        for i in range(3)
    ]
    (ws / "manifest.json").write_text(json.dumps(manifest))

    # stub fetch: sleep a little, create the transcript-side marker audio + metadata
    fetch_stub = tmp_path / "fetch_stub.sh"
    fetch_stub.write_text(
        "#!/bin/bash\n"
        "# args: fake URL --json --output-dir DIR  (we only care about DIR)\n"
        "DIR=\"${@: -1}\"\n"
        "sleep 0.1\n"
        "mkdir -p \"$DIR\" && echo ok > \"$DIR/audio.mp4\"\n"
        "echo '{\"duration_sec\":1}' > \"$DIR/metadata.json\"\n"
    )
    fetch_stub.chmod(0o755)
    # stub transcribe: create the transcript tree that skip-detection expects
    tr_stub = tmp_path / "tr_stub.sh"
    tr_stub.write_text(
        "#!/bin/bash\n"
        "DIR=\"$1\"\n"
        "sleep 0.1\n"
        "BV=$(basename \"$DIR\")\n"
        "T=\"$DIR/../../references/transcripts/bilibili/20260101-x-$BV\"\n"
        "mkdir -p \"$T\" && echo transcript > \"$T/transcript.md\"\n"
        "mkdir -p \"$DIR/faster-whisper/chunks\" && touch \"$DIR/faster-whisper/metrics.md\" \"$DIR/x.wav\"\n"
    )
    tr_stub.chmod(0o755)

    cmd = [
        sys.executable, str(SCRIPT), str(ws), str(ws / "manifest.json"),
        "--fetch-workers", "2", "--asr-workers", "1", "--poll", "0.05",
        "--fetch-cmd", f"bash {fetch_stub} url --json --output-dir {{dir}}",
        "--transcribe-cmd", f"bash {tr_stub} {{dir}}",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    statuses = [json.loads(l) for l in (ws / "status.jsonl").read_text().splitlines()]
    assert all(s["status"] == "ok" for s in statuses)
    assert len(statuses) == 3
    # all jobs reached done/
    done = list((ws / "queues" / "done").glob("BV*"))
    assert len(done) == 3
    # wav cleanup ran (x.wav at ws root removed)
    assert not (ws / "workspaces" / "BV1stub0" / "x.wav").exists()

    # idempotent rerun: nothing new to do
    r2 = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    assert r2.returncode == 0
    statuses2 = [json.loads(l) for l in (ws / "status.jsonl").read_text().splitlines()]
    assert len(statuses2) == 3  # no new entries


def test_fetch_failure_recorded_not_fatal(tmp_path):
    ws = tmp_path / "ws"
    ws.mkdir()
    manifest = [{"bvid": "BV1bad", "title": "bad", "duration": 10, "created": 0}]
    (ws / "manifest.json").write_text(json.dumps(manifest))
    bad = tmp_path / "bad.sh"
    bad.write_text("#!/bin/bash\nexit 3\n")
    bad.chmod(0o755)
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(ws), str(ws / "manifest.json"),
         "--poll", "0.05", "--fetch-cmd", f"bash {bad}", "--transcribe-cmd", "true"],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 1
    statuses = [json.loads(l) for l in (ws / "status.jsonl").read_text().splitlines()]
    assert statuses == [{"bvid": "BV1bad", "status": "fetch_failed"}]
    assert (ws / "queues" / "failed" / "BV1bad.err").exists()
