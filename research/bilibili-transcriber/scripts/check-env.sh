#!/usr/bin/env bash
# check-env.sh — verify every runtime assumption the transcription pipeline
# depends on, driven by runtime.conf (the runtime record).
#
# Usage: bash check-env.sh [runtime.conf]   (default: <skill_dir>/runtime.conf)
#
# Run it on a new node, after an ASR service move, or before a long batch.
# PASS/WARN lines are informational; any FAIL exits 1.

set -u
SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
CONF="${1:-$SKILL_DIR/runtime.conf}"
fails=0

say() { printf '%s\n' "$*"; }
fail() { say "FAIL  $*"; fails=$((fails+1)); }

# 1. runtime.conf present + sourced
if [ ! -f "$CONF" ]; then
  fail "runtime.conf not found: $CONF (copy runtime.conf.example and fill in)"
else
  # shellcheck disable=SC1090
  . "$CONF"
  say "PASS  runtime.conf: $CONF"
  [ -n "${WHISPER_ENDPOINT:-}" ] || fail "WHISPER_ENDPOINT empty in runtime.conf"
  [ -n "${WHISPER_MODEL:-}" ] || fail "WHISPER_MODEL empty in runtime.conf"
fi

# 2. tools on PATH
for tool in aria2c ffmpeg python3; do
  command -v "$tool" > /dev/null 2>&1 && say "PASS  $tool: $(command -v $tool)" \
    || fail "$tool not on PATH"
done

# 3. python deps (requests for fetch.py, numpy for chunk_transcribe.py)
if command -v python3 > /dev/null 2>&1; then
  if python3 -c "import requests, numpy" 2>/dev/null; then
    say "PASS  python3 deps: requests+numpy"
  else
    fail "python3 lacks requests/numpy — prepend a venv that has them to PATH"
  fi
fi

# 4. ASR endpoint alive + model present (bypass proxy: internal IP)
EP="${WHISPER_ENDPOINT:-}"
MODEL="${WHISPER_MODEL:-}"
if [ -n "$EP" ]; then
  # WHISPER_ENDPOINT may or may not already end in /v1 — build the models URL once
  case "$EP" in
    */v1) models_url="${EP%/}/models" ;;
    *)    models_url="${EP%/}/v1/models" ;;
  esac
  resp=$(curl -s --noproxy '*' --max-time 10 "$models_url" 2>/dev/null || true)
  if [ -z "$resp" ]; then
    fail "ASR endpoint unreachable: $EP (service moved/restarted? probe again, check NodePort)"
  elif printf '%s' "$resp" | grep -q "\"id\":\"$MODEL\""; then
    say "PASS  ASR endpoint: $EP (model $MODEL)"
  else
    fail "ASR endpoint alive but model '$MODEL' not listed in $models_url"
  fi
fi

# 5. bilibili reachability (direct first, then via proxy env)
if curl -s -o /dev/null --noproxy '*' --max-time 8 https://www.bilibili.com; then
  say "PASS  bilibili.com direct"
elif curl -s -o /dev/null --max-time 8 https://www.bilibili.com; then
  say "PASS  bilibili.com via proxy"
else
  fail "bilibili.com unreachable (neither direct nor via proxy)"
fi

# 6. bili CLI + credential (needed by enumerate-uploader.py only; the
#    fetch+transcribe pipeline itself works without login)
if command -v bili > /dev/null 2>&1; then
  if bili favorites 2>/dev/null | grep -q '^ok: true'; then
    say "PASS  bili CLI: logged in"
  else
    say "WARN  bili CLI present but credential check failed (needed for enumeration only)"
  fi
else
  say "WARN  bili CLI not installed (needed for enumeration only: uv tool install bilibili-cli)"
fi

if [ "$fails" -gt 0 ]; then
  say "---"
  say "ENVIRONMENT BROKEN: $fails check(s) failed"
  exit 1
fi
say "---"
say "ENVIRONMENT OK"
exit 0
