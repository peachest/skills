#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# transcode.sh — Extract the audio transcode step from transcribe.sh.
#
# Converts an input audio/video file to 16kHz mono WAV, ignoring any video
# stream (-vn). This is testable in isolation and does NOT require a system
# ffmpeg: the binary is located via the `imageio_ffmpeg` Python package (a
# pip-shipped static build) when available, falling back to PATH. Audio
# duration is read from the WAV header with the stdlib `wave` module, so no
# external probe binary is needed.
#
# Usage: bash <SKILL_DIR>/scripts/transcode.sh <input-file> <output-wav>
#
# Outputs:
#   <output-wav>  — 16kHz mono s16 PCM WAV
#   stdout        — three lines: transcode_seconds, wav_size_bytes, duration_seconds
# ──────────────────────────────────────────────────────────────────────────────
set -eo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <input-file> <output-wav>"
  exit 1
fi

INPUT_FILE="$1"
WAV_PATH="$2"

if [ ! -f "$INPUT_FILE" ]; then
  echo "✗ Input file not found: $INPUT_FILE"
  exit 1
fi

# ── Locate an ffmpeg binary ──
# Prefer the static ffmpeg shipped with the imageio-ffmpeg pip package;
# otherwise fall back to any ffmpeg on PATH. A probe binary is NOT required —
# duration comes from the WAV header via pure Python (wave module).
FFMPEG_BIN=""
if python3 -c "import imageio_ffmpeg" >/dev/null 2>&1; then
  FFMPEG_BIN="$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())" 2>/dev/null || true)"
fi
if [ -z "$FFMPEG_BIN" ]; then
  FFMPEG_BIN="$(command -v ffmpeg 2>/dev/null || true)"
fi
if [ -z "$FFMPEG_BIN" ]; then
  echo "✗ No ffmpeg available. Install the pip package: pip install imageio-ffmpeg" >&2
  exit 1
fi

T0=$(date +%s%N)
"$FFMPEG_BIN" -y -i "$INPUT_FILE" -vn -ac 1 -ar 16000 -sample_fmt s16 "$WAV_PATH" -loglevel error
T1=$(date +%s%N)
TRANSCODE_S=$(echo "scale=3; ($T1 - $T0) / 1000000000" | bc)
WAV_SIZE=$(stat -c%s "$WAV_PATH" 2>/dev/null)

# Get duration from the WAV header (pure Python — no probe binary needed)
DURATION="$(python3 - "$WAV_PATH" <<'PY'
import sys, wave
try:
    with wave.open(sys.argv[1], 'rb') as w:
        print(f"{w.getnframes() / w.getframerate():.1f}")
except Exception:
    print("0.0")
PY
)"

# Output machine-readable result for callers
echo "$TRANSCODE_S"
echo "$WAV_SIZE"
echo "$DURATION"