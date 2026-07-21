---
name: bilibili-transcriber
description: |
  Transcribe Bilibili video audio to text via a whisper-asr service. Use
  when the user has a Bilibili video and wants its content as text for
  technique extraction. The audio download step is now handled by the
  fetch-article skill — this skill only does the transcription.
---

# Bilibili Video Transcription

Transcribe Bilibili video audio via any OpenAI-compatible whisper-asr service.

## Pipeline

```text
fetch-article (download audio) → this skill (transcribe)
```

### Step 1: Download Audio (via fetch-article)

```bash
python3 .agent/skills/fetch-article/scripts/fetch.py \
  "https://www.bilibili.com/video/BV1xx/" \
  --json
```

This saves audio to a temp directory and outputs JSON with `audio_path`,
`title`, `author`, `duration_sec`, and `has_cc_subtitles`.

If CC subtitles are available, they are saved directly and ASR is skipped.

### Step 2: Transcribe

```bash
WHISPER_ENDPOINT=http://your-asr:8000/openai/v1 \
WHISPER_MODEL=whisper-large-v3 \
WHISPER_LANG=zh \
bash .agent/skills/bilibili-transcriber/scripts/transcribe.sh <workspace-dir>/
```

Where `<workspace-dir>` is the output directory from fetch-article
(use the `raw_path` field from the JSON output).

### Step 3: Clean the Transcript (Manual)

The raw transcript is continuous text without punctuation. You must manually
add paragraph breaks and fix homophone ASR errors. See the detailed cleaning
guide below.

## Prerequisites

- `ffmpeg` in PATH
- Network access to `api.bilibili.com`
- A running whisper-asr service with OpenAI-compatible endpoint
- `curl` for API calls

## Environment Variables for transcribe.sh

| Variable | Required | Default | Description |
| ---------- | ---------- | --------- | ------------- |
| `WHISPER_ENDPOINT` | Yes | — | API base URL, e.g. `http://host:8000/openai/v1` |
| `WHISPER_MODEL` | Yes | — | Model name, e.g. `whisper-large-v3` |
| `WHISPER_LANG` | No | `zh` | Language hint |
| `METHOD` | No | `faster-whisper` | Intermediate subdirectory name |

## Output

```text
<workspace-dir>/                    ← from fetch-article
├── raw/audio.mp4                   ← downloaded audio
├── $METHOD/                        ← intermediate ASR output
│   ├── audio.wav                   ← transcoding cache
│   ├── transcript.md               ← raw ASR (metadata + text)
│   └── metrics.md                  ← performance metrics

references/transcripts/
└── bilibili/
    └── {date}-{title}-{BV}/
        └── transcript.md           ← ← edit this one
```

## Cleaning the Transcript

The raw ASR output is continuous text. You must manually clean it.

### Common Issues

| Issue | Example | Fix |
| ------- | --------- | ----- |
| No paragraph breaks | `...防线建好先建立全景认知...` | Add `\n\n` at topic boundaries |
| Missing punctuation | `模型滥用供应链攻击成本攻击` | Add `、` between list items |
| Wrong characters (ASR hallucination) | `Swift Modeling` → `Threat Modeling` | Correct based on context |
| Wrong characters (homophone) | `转印` → 转义, `托命` → 脱敏 | Correct based on context |
| Garbage transcription | `等下摄影19000...` | **Keep**, annotate with `[音频不清]` |
| Stuck/repeated phrases | Model repeating the same fragment | Deduplicate |

### Workflow

1. Read through the full text while skimming the video at 2x
2. Insert `\n\n` at each topic boundary
3. For wrong terms: hallucination → `[音频不清]`, homophone → correct, proper noun mangled → correct
4. For a 10-minute tech talk, expect ~15-20 minutes of cleaning

## Full Pipeline (one-liner)

```bash
WHISPER_ENDPOINT=http://your-asr:8000/openai/v1 \
WHISPER_MODEL=whisper-large-v3 \
BVID="BV1xx..." && \
OUT=$(python3 .agent/skills/fetch-article/scripts/fetch.py \
  "https://www.bilibili.com/video/$BVID/" \
  --json | python3 -c "import sys,json; print(json.load(sys.stdin)['raw_path'])") && \
bash .agent/skills/bilibili-transcriber/scripts/transcribe.sh "$OUT"
```
