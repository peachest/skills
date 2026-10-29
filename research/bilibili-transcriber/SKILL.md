---
name: bilibili-transcriber
description: |
  Transcribe Bilibili video audio to text. Use when the user has a Bilibili
  video URL and wants its spoken content as a readable transcript.
---

# Bilibili Video Transcription

## Pipeline

```text
fetch-article (download audio) → this skill (transcribe → slides → merge)
```

The fetch stage also writes `context.md` into the workspace — 简介、置顶评论、
热门评论 Top 5、最新评论 Top 5（作者/观众视角，与转写正文互补；详见
fetch-article SKILL.md 的 Bilibili 节）。

### One-shot entry (RECOMMENDED)

The whole chain in one command — creates the venv if missing (`uv sync`),
runs every python stage through `uv run --project <SKILL_DIR>` (never bare
python3), and prints all artifact paths at the end:

```bash
bash <SKILL_DIR>/scripts/run.sh "https://www.bilibili.com/video/BV1xx/" [outdir]
# flags: --visual / --no-slides / --no-merge
```

**Extraction depth (ask the user when intent is unclear)**: default text
mode stops at CC-subtitles-or-audio (whichever first) — no video stream.
`--visual` downloads the video even when CC subtitles exist and runs the
slides stage (slide-deck OCR + [mm:ss 幻灯片] timeline); use it whenever
the user wants to see slides/frames, not just read the transcript.

Exit codes (also written to `<outdir>/.done`): 0 = all stages ok,
2 = transcript ok but slides/merge failed, 3 = fetch/transcribe failed.

Per-stage control and the cleaning/bilingual/re-clean tooling are below —
drop to them only when you need to run or re-run a single stage.

### Stage 1: Download Audio

```bash
python3 <SKILL_DIR>/../fetch-article/scripts/fetch.py \
  "https://www.bilibili.com/video/BV1xx/" --json
```

Done when: JSON output contains `raw_path` (the `article.json` file
inside the workspace dir — use its parent directory as the workspace)
with `audio.mp4` and `metadata.json` alongside.

### Stage 2: Transcribe

```bash
bash <SKILL_DIR>/scripts/transcribe.sh <workspace-dir>/
```

Prefer `run.sh` (locks every python stage to `uv run --project <SKILL_DIR>`);
when invoking `transcribe.sh` directly, run it via
`cd <SKILL_DIR> && uv run bash scripts/transcribe.sh` so the venv deps
(numpy for chunking) are present.

`<workspace-dir>` is the parent dir of the `raw_path` file from Stage 1.
The script loads
`<SKILL_DIR>/runtime.conf` for endpoint/model automatically; if absent,
set `WHISPER_ENDPOINT` and `WHISPER_MODEL` env vars
(see [Service Discovery](#service-discovery)).

Current backend: faster-whisper large-v3-turbo on the user's WSL laptop,
reached through an SSH tunnel (`WHISPER_TUNNEL_*` in runtime.conf) —
transcribe.sh reuses an existing tunnel or opens one automatically
(`ssh -f -N -L` + `ExitOnForwardFailure`) and probes before transcribing.
The original cluster-hosted whisper-asr NodePort backend is **deprecated**; its
discovery recipe stays in `runtime.conf.example` for rollback.

The script transcodes MP4 → 16kHz WAV, then either transcribes directly
(WAV ≤ 25MB) or uses **silence-aware chunking**: detects natural pause
boundaries via ffmpeg `silencedetect`, partitions at those points
(DP by default), transcribes chunks in parallel, and concatenates
directly — no overlap, no dedup. Output uses `verbose_json` to capture
per-segment `avg_logprob` and `compression_ratio`.

Done when: `references/transcripts/bilibili/{date}-{title}-{BV}/transcript.md`
exists with raw ASR text, and the console reports chunk boundaries and
any low-confidence segments (`avg_logprob < -1.0`).

### Stage 3: Clean the Transcript (LLM)

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
repeated-sentence guard (rejects in-ratio outputs that loop a paragraph),
resumable (`transcript.raw.md` marker), failures → `clean-failures.json`.
Language auto-detected per transcript (CJK ratio; `CLEAN_LANG=zh|en` to
force): zh → homophone-proofreading prompt, en → English proofreading
prompt (no translation).

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

**English-reference re-clean** (zh-dub video whose original English
transcript is retrievable — e.g. via yt-dlp auto-subs on the source video;
use when plain cleanup still leaves mangled proper nouns):

```bash
# fetch the English reference first (proxy may be needed for YouTube)
yt-dlp --skip-download --write-auto-subs --sub-langs en -o ref "<EN_VIDEO_URL>"
# then re-clean: raw (transcript.raw.md) + EN ref per aligned chunk -> <stem>-reclean.md
cd <SKILL_DIR> && uv run python scripts/reclean-en.py \
  <transcript-dir>/transcript.raw.md ref.txt \
  [--glossary glossary.txt] [--out <transcript-dir>/transcript.md]
```

Same `CLEAN_LLM_*` config as clean-transcripts.py. The EN reference is the
ground truth for names/terms (ASD-STE100, Mike Hostetler — ASR writes these
as "ASTST100", "迈克·哈斯特勒"). The zh raw only fixes segmentation order and
tone; numbers/examples must survive verbatim. A >40%-shorter-than-EN output
triggers a summarization warning. Optional glossary file: one
term/translation per line, injected into the prompt.

Done when: transcript has paragraph breaks, punctuation, and corrected
homophones — every raw ASR segment accounted for.

## Service Discovery

If `<SKILL_DIR>/runtime.conf` exists, `transcribe.sh` sources it — no
env vars needed. To create it, see `runtime.conf.example`.

Two backend shapes:

1. **Direct endpoint** (LAN / k8s NodePort): set `WHISPER_ENDPOINT` to the
   service URL and `WHISPER_MODEL` to the model ID (query `/v1/models` to
   discover — vLLM uses `/v1`, not `/openai/v1`; the model ID may differ
   from the name, e.g. `atom` instead of `whisper-large-v3`).
2. **NAT'd host behind SSH** (e.g. faster-whisper inside WSL, not reachable
   directly): set `WHISPER_ENDPOINT` to the *local* tunnel side
   (`http://127.0.0.1:<local-port>/v1`) plus `WHISPER_TUNNEL_HOST` /
   `WHISPER_TUNNEL_LOCAL_PORT` / `WHISPER_TUNNEL_REMOTE`. transcribe.sh
   probes the endpoint first and reuses a live tunnel; otherwise opens
   `ssh -f -N -L <local-port>:<remote> <host>` (ExitOnForwardFailure=yes,
   ServerAliveInterval=30) and re-probes. A tunnel that comes up but gets
   no HTTP 200 means the remote service is down — probe it via ssh instead
   of retrying the tunnel.

The runtime record also carries `OCR_LLM_*` (slides, Step 4) and
`CLEAN_LLM_*` (cleanup, Step 3) endpoints.

## Slide Extraction (optional)

For talk-style videos, extract the deck alongside the transcript:

```bash
cd <SKILL_DIR> && uv run python scripts/slides-extract.py <workspace-dir>
```

Downloads the video (yt-dlp, agent node side — WSL has no ffmpeg), cuts frames
at scene changes (`select='gt(scene,0.3)'`, `SLIDE_SCENE_THRESHOLD`
overridable — lower it for animation-style transitions; the frame at t=0
always kept), dedups adjacent frames by dHash hamming distance (code
default 8), then OCRs each kept slide via the vision endpoint in
runtime.conf (`OCR_LLM_*`) with a verbatim-transcription prompt (structure
preserved, numbers never dropped; non-slide shots return `[非幻灯片]`).
Resumable: OCR results cached in `<workspace>/slides/slides.json`.

Done when: `<workspace>/slides/slides.json` (timestamped entries with text)
and `slides.md` exist, and no kept frame has empty OCR text.

Merging with the transcript (automatic as run.sh's stage 4; standalone
re-run after editing slides/OCR results):

```bash
cd <SKILL_DIR> && uv run python scripts/merge-slides.py <workspace-dir> \
  --transcript-dir <references/transcripts/.../BV...>
```

Writes `transcript.final.md` into the transcript directory: cleaned
transcript on top, raw segments on a timeline with each slide's OCR text
inserted as `## [mm:ss 幻灯片]` blocks. Speech and slides are complementary —
keep both; do not drop transcript text where a slide covers the same content.

## Chunking Configuration

Internal chunking knobs (`STRATEGY`, `CHUNK_SEC`, `SILENCE_DB`, `TOLERANCE`,
`PARALLEL`, …) keep sane code defaults for 60-120 minute Mandarin tech talks
— no historical session ever needed to override them, so they are no longer
documented as user-facing config (override via env vars only if a run
surprises you; the four partition algorithms — dp/greedy/weighted/threshold —
are implemented in `chunk_transcribe.py`, comparison in
[`references/chunking.md`](references/chunking.md)).

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

# 3. Queue — producer/consumer pipeline (fetch workers and ASR workers are
#    decoupled: downloads of upcoming videos overlap ASR of the current one),
#    crash-safe via atomic rename claims + startup requeue, resumable:
mkdir -p ~/research/<topic> && cd ~/research/<topic>
uv run --project <SKILL_DIR> python <SKILL_DIR>/scripts/pipeline-queue.py "$PWD" manifest.json \
  --fetch-workers 2 --asr-workers 1
```

The queue runs on the skill's uv env (`uv sync` once in `<SKILL_DIR>`; every
script below runs as `cd <SKILL_DIR> && uv run python scripts/<x>.py` so
children inherit the full dep set). Two non-obvious rules baked into the
scripts: loop children never inherit stdin (a downloader once ate bytes from
the redirected input and truncated every following BV id), and WAV
intermediates are deleted after each success while the source audio and
metrics are kept.
