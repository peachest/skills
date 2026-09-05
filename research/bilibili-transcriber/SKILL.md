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

The raw transcript is continuous text without punctuation. Two automated
paths — both need `CLEAN_LLM_BASEURL` / `CLEAN_LLM_MODEL` (+ optional
`CLEAN_LLM_KEY`) in runtime.conf:

**Mono-lingual audio** (Chinese dub only):

```bash
cd <SKILL_DIR> && uv run python scripts/clean-transcripts.py <manifest-or-dirs>
```

Chunks the body (~3000 chars), cleans via an OpenAI-compatible endpoint,
per-chunk ±25% length validation (rejects silent summarizing), escalation
ladder for stubborn chunks (halve → sampling escape temp 0.7/fp 0.6 — flash
models deterministically repetition-loop on some dense chunks at temp 0),
resumable (`transcript.raw.md` marker), failures → `clean-failures.json`.

**Bilingual dual-audio** (English original + condensed Chinese voice-over
mixed in one track — common for translated channels; a zh-hinted single pass
bleeds both languages into one messy text):

```bash
cd <SKILL_DIR> && uv run python scripts/dual-transcribe.py <targets.json>
```

Re-runs ASR with `WHISPER_LANG=en` in a scratch root (zh side reuses the
existing chunk JSONs), aligns both timelines into ~90s windows, then one LLM
merge per 4 windows: cleaned zh + full EN translation + `[对照存疑]` flags
where the dub skips content or the EN original corrects an ASR homophone
(汉玛→Hanuman, 夏天宝座→Summer Palace — the EN side doubles as ground
truth for proper nouns). Output is the interleaved format the user chose:
`## [mm:ss - mm:ss]` window → zh paragraphs → `> **EN 原声（译文）**`
blockquote → optional flag line. Previous text is kept as
`transcript.mixed.md`; resumable via `dual-state.json`.

Bilingual detection: scan transcripts for ASCII ratio > 10% — anything
above is a dual-pass candidate. Manual prompt template and pre-marking
workflow live in [`references/llm-cleanup.md`](references/llm-cleanup.md).

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

## Environment Check

`runtime.conf` is the runtime record: the ASR endpoint, model, and language the
pipeline assumes. Assumptions rot when the service moves, the pod restarts, or
you switch dev nodes. Validate them before a long batch — or whenever a
transcription run surprises you:

```bash
bash <SKILL_DIR>/scripts/check-env.sh
```

PASS/WARN lines are informational; any FAIL exits 1. It probes: runtime.conf
values, aria2c/ffmpeg/python3 (with requests+numpy+aiohttp), the ASR endpoint
via `/v1/models` (model id included), the LLM cleanup endpoint (Step 3),
bilibili.com reachability (direct, then proxy), and the `bili` CLI credential
(enumeration only). Run it inside the uv env for a green pass:
`cd <SKILL_DIR> && uv run bash scripts/check-env.sh`.

## Batch Mode

Transcribing a whole channel: enumerate the uploader's videos into a manifest,
filter it to taste, then run the resumable queue.

```bash
# 1. Enumerate (credential REQUIRED — anonymous space-API calls hit 412)
~/.local/share/uv/tools/bilibili-cli/bin/python <SKILL_DIR>/scripts/enumerate-uploader.py \
  --bv BV1iz4R6EEFk --out ~/research/<topic>/manifest.json
#    (or --mid <mid> directly)

# 2. Filter the manifest (jq / python) — drop vlogs, keep the teaching videos

# 3. Queue — pipeline version (RECOMMENDED): fetch and ASR run as independent
#    worker pools connected by queues/ (pending → ready → done); downloads of
#    upcoming videos overlap ASR of the current one, crash-safe via atomic
#    rename claims + startup requeue, resumable, same status.jsonl schema.
mkdir -p ~/research/<topic> && cd ~/research/<topic>
uv run --project <SKILL_DIR> python <SKILL_DIR>/scripts/pipeline-queue.py "$PWD" manifest.json \
  --fetch-workers 2 --asr-workers 1

#    Serial fallback (simpler, no pipelining):
#    bash <SKILL_DIR>/scripts/run-queue.sh "$PWD" manifest.json
```

The queue runs on the skill's uv env (`uv sync` once in `<SKILL_DIR>`; every
script below runs as `cd <SKILL_DIR> && uv run python scripts/<x>.py` so
children inherit the full dep set). Two non-obvious rules baked into the
scripts: loop children never inherit stdin (a downloader once ate bytes from
the redirected input and truncated every following BV id), and WAV
intermediates are deleted after each success while the source audio and
metrics are kept.
