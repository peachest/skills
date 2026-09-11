#!/usr/bin/env bash
# Environment self-check for skill-update-manager.
# Usage: bash scripts/check-env.sh
set -u
SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
FAIL=0

# python3 executable + stdlib only (json/hashlib/tarfile ship with it)
if command -v python3 >/dev/null 2>&1 && python3 -c "import json, hashlib, tarfile" 2>/dev/null; then
  echo "PASS python3 (with json/hashlib/tarfile)"
else
  echo "FAIL python3 — install python3 (stdlib json/hashlib/tarfile required)"
  FAIL=1
fi

# gh CLI, executable, authed (needed for tarball fetch on chain-1 remote check)
if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    echo "PASS gh CLI (authenticated)"
  else
    echo "FAIL gh CLI present but not authenticated — run: gh auth login"
    FAIL=1
  fi
else
  echo "FAIL gh CLI not found — install github cli and run: gh auth login"
  FAIL=1
fi

# Chain 1 target: global skill lock file
LOCK="$HOME/.agents/.skill-lock.json"
if [ -f "$LOCK" ]; then
  echo "PASS lock file $LOCK"
else
  echo "WARN lock file missing — no third-party skills installed yet; 'remote' mode will SKIP"
fi

# Chain 2 target: local skill source repo
SRC="$HOME/skills"
if [ -d "$SRC" ]; then
  echo "PASS source repo $SRC"
else
  echo "WARN source repo $SRC missing — 'local' mode will SKIP"
fi

# Active agent skill directory
if [ -d "$HOME/.pi/agent/skills" ]; then
  echo "PASS agent skills dir ~/.pi/agent/skills"
else
  echo "WARN ~/.pi/agent/skills missing — is this a pi agent node?"
fi

exit $FAIL
