---
name: bilibili-transcriber
description: |
  Transcribe Bilibili video audio to text. Use when the user has a Bilibili
  video URL and wants its spoken content as a readable transcript.
---

# Bilibili Video Transcription

## Pipeline

```text
fetch-article (download audio) → this skill (transcribe) → LLM (clean)
```

### Step 1: Download Audio

```bash
python3 <SKILL_DIR>/../fetch-article/scripts/fetch.py \
  "https://www.bilibili.com/video/BV1xx/" --json
```

Done when: JSON output contains `raw_path` pointing to a workspace dir
with `audio.mp4` and `metadata.json`.

### Step 2: Transcribe

```bash
bash <SKILL_DIR>/scripts/transcribe.sh <workspace-dir>/
```

`<workspace-dir>` is the `raw_path` from Step 1. The script loads
`<SKILL_DIR>/runtime.conf` for endpoint/model automatically; if absent,
set `WHISPER_ENDPOINT` and `WHISPER_MODEL` env vars
(see [Service Discovery](#service-discovery)).

The script transcodes MP4 → 16kHz WAV, then either transcribes directly
(WAV ≤ 25MB) or uses **silence-aware chunking**: detects natural pause
boundaries via ffmpeg `silencedetect`, partitions at those points
(DP by default), transcribes chunks in parallel, and concatenates
directly — no overlap, no dedup. Output uses `verbose_json` to capture
per-segment `avg_logprob` and `compression_ratio`.

Done when: `references/transcripts/bilibili/{date}-{title}-{BV}/transcript.md`
exists with raw ASR text, and the console reports chunk boundaries and
any low-confidence segments (`avg_logprob < -1.0`).

### Step 3: Clean the Transcript (LLM)

The raw transcript is continuous text without punctuation. Feed it to an
LLM for homophone correction, punctuation, and paragraph segmentation.
See [`references/llm-cleanup.md`](references/llm-cleanup.md) for the
prompt template and pre-marking low-confidence segments.

Done when: transcript has paragraph breaks, punctuation, and corrected
homophones — every raw ASR segment accounted for.

## Service Discovery

If `<SKILL_DIR>/runtime.conf` exists, `transcribe.sh` sources it — no
env vars needed. To create it, see `runtime.conf.example` for Kubernetes
discovery steps (`kubectl get svc`, NodePort, `curl /v1/models`).

For non-Kubernetes: set `WHISPER_ENDPOINT` to the service URL and
`WHISPER_MODEL` to the model ID (query `/v1/models` to discover — vLLM
uses `/v1`, not `/openai/v1`; the model ID may differ from the name,
e.g. `atom` instead of `whisper-large-v3`).

## Chunking Configuration

`STRATEGY` selects the partition algorithm — see
[`references/chunking.md`](references/chunking.md) for comparison.
Remaining defaults (`CHUNK_SEC=600`, `SILENCE_DB=-30`, `TOLERANCE=60`,
`MAX_FILESIZE_MB=25`, `PARALLEL=4`) are sensible for 60-120 minute
Mandarin tech talks. Override via env vars or `transcribe.sh` flags.

## Full Pipeline (one-liner)

```bash
BVID="BV1xx..." && \
OUT=$(python3 <SKILL_DIR>/../fetch-article/scripts/fetch.py \
  "https://www.bilibili.com/video/$BVID/" \
  --json | python3 -c "import sys,json; print(json.load(sys.stdin)['raw_path'])") && \
bash <SKILL_DIR>/scripts/transcribe.sh "$OUT"
```
