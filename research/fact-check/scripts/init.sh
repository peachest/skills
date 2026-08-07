#!/bin/bash
# init.sh — Phase 0 initialization script
# Usage: bash init.sh <path> [project-root]
# Output: stdout JSON { document_key, mode, repo, session_tag, is_directory }
#
# Reference: DD-30, run-output.md Phase 0

set -euo pipefail

INPUT_PATH="${1:-}"
PROJECT_ROOT="${2:-}"

if [ -z "$INPUT_PATH" ]; then
  echo '{"error":"missing path argument"}' >&2
  exit 1
fi

# ---- Resolve absolute paths ----
REAL_INPUT=$(realpath "$INPUT_PATH" 2>/dev/null || echo "$INPUT_PATH")

# If project-root not given, try to find it from git
if [ -z "$PROJECT_ROOT" ]; then
  PROJECT_ROOT=$(git -C "$(dirname "$REAL_INPUT")" rev-parse --show-toplevel 2>/dev/null || echo "")
fi

# If still not found, use the input path's dir as project root
if [ -z "$PROJECT_ROOT" ]; then
  # For non-git: use the input path's parent as project root
  if [ -d "$INPUT_PATH" ]; then
    PROJECT_ROOT="$REAL_INPUT"
  else
    PROJECT_ROOT="$(dirname "$REAL_INPUT")"
  fi
fi

REAL_ROOT=$(realpath "$PROJECT_ROOT")

# ---- Document key ----
REL_PATH=$(realpath --relative-to="$REAL_ROOT" "$REAL_INPUT" 2>/dev/null || echo "$INPUT_PATH")
DOCUMENT_KEY=$(echo "$REL_PATH" | sed 's|/|--|g')

# ---- Mode detection ----
LEDGER_FILE="$REAL_ROOT/fact-check/documents/$DOCUMENT_KEY/ledger.jsonl"
MODE="full"
if [ -f "$LEDGER_FILE" ]; then
  MODE="incremental"
fi

# ---- Repo detection ----
REPO="NO_REPO"
if git -C "$REAL_ROOT" rev-parse --show-toplevel &>/dev/null; then
  REPO_URL=$(git -C "$REAL_ROOT" remote get-url origin 2>/dev/null || echo "")
  if [ -n "$REPO_URL" ]; then
    # Extract owner/repo from git URL (supports https and ssh), strip .git suffix
    CLEAN_URL=$(echo "$REPO_URL" | tr -d '\n' | sed 's|\.git$||')
    REPO=$(echo "$CLEAN_URL" | sed -n 's|.*[:/]\([^/]*/[^/]*\)$|\1|p')
    if [ -z "$REPO" ]; then
      REPO="UNPARSABLE"
    fi
  fi
fi

# ---- Session tag (branch name) ----
SESSION_TAG=""
if git -C "$REAL_ROOT" rev-parse --show-toplevel &>/dev/null; then
  SESSION_TAG=$(git -C "$REAL_ROOT" branch --show-current 2>/dev/null || echo "main")
fi
if [ -z "$SESSION_TAG" ]; then
  SESSION_TAG="main"
fi

# ---- Is directory? ----
IS_DIRECTORY=false
if [ -d "$REAL_INPUT" ]; then
  IS_DIRECTORY=true
fi

# ---- Output JSON ----
cat <<EOF
{
  "document_key": "$DOCUMENT_KEY",
  "mode": "$MODE",
  "repo": "$REPO",
  "session_tag": "$SESSION_TAG",
  "is_directory": $IS_DIRECTORY
}
EOF
