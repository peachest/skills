#!/usr/bin/env bash
# html-render-check orchestrator: structure layer (offline parse) then render
# layer (real Chromium via Playwright). Exits non-zero when hard findings exist.
#
# Usage:
#   bash check.sh [--shot-dir DIR] [--strict] <file.html> [<file.html>...]
# Options:
#   --shot-dir DIR  screenshot output dir (default: each artifact's own directory)
#   --strict        also run html5lib + VNU spec validation (structure layer)
#
# Env (or runtime.conf): PLAYWRIGHT_DIR (default ~/tools/playwright-runner).

set -u

SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
CONF="$SKILL_DIR/runtime.conf"
[ -f "$CONF" ] && . "$CONF"
export PLAYWRIGHT_DIR="${PLAYWRIGHT_DIR:-$HOME/tools/playwright-runner}"

SHOT_DIR=""
STRICT=""
declare -a PASSED_ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --shot-dir) SHOT_DIR="$2"; PASSED_ARGS+=("$1" "$2"); shift 2 ;;
    --strict) STRICT="1"; shift ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) PASSED_ARGS+=("$1"); shift ;;
  esac
done
set -- "${PASSED_ARGS[@]}"
[ $# -ge 1 ] || { echo "usage: check.sh [--shot-dir DIR] [--strict] <file.html>..." >&2; exit 2; }

command -v node >/dev/null 2>&1 || { echo "FAIL node missing — run scripts/check-env.sh first" >&2; exit 1; }
[ -d "$PLAYWRIGHT_DIR/node_modules/playwright" ] || { echo "FAIL playwright module not found in $PLAYWRIGHT_DIR — run scripts/check-env.sh" >&2; exit 1; }

# ---- Stage 0: structure validation (offline, parse-level) --------------------
declare -a STRUCT_OK=()
for f in "$@"; do
  [ -f "$f" ] || { echo "FAIL $f — file not found"; continue; }
  echo "== $f (structure)"
  if [ -n "$STRICT" ]; then
    python3 "$SKILL_DIR/scripts/validate_html.py" --strict "$f"
  else
    python3 "$SKILL_DIR/scripts/validate_html.py" "$f"
  fi
  rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "  structure: FAIL — skipping render pass"
  else
    STRUCT_OK+=("$f")
  fi
done

# ---- Stage 1: render layer (real Chromium) ------------------------------------
if [ "${#STRUCT_OK[@]}" -eq 0 ]; then
  echo "---"
  echo "RESULT: FAIL (no artifact passed structure validation)"
  exit 1
fi

node "$SKILL_DIR/scripts/render-check.mjs" "${STRUCT_OK[@]}" $([ -n "$SHOT_DIR" ] && echo --shot-dir "$SHOT_DIR")
exit $?
