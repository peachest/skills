#!/usr/bin/env bash
# check-env.sh — verify every runtime assumption the MR/PR review triage
# scripts depend on: glab/gh CLIs with working auth, python3 + the stdlib
# modules the scripts import, the skill's own backend modules, and jq.
#
# No runtime.conf: GitLab/GitHub hosts are derived at runtime from
# `git remote get-url origin` plus glab/gh config (multi-instance aware),
# and tokens come from glab/gh config or optional env overrides
# (GITLAB__PERSONAL_ACCESS_TOKEN / GITHUB_TOKEN) — nothing node-specific.
#
# Usage: bash check-env.sh   (from anywhere; CWD does not matter)
# PASS/WARN lines are informational; any FAIL exits 1.

set -u
SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
fails=0

say() { printf '%s\n' "$*"; }
fail() { say "FAIL  $*"; fails=$((fails+1)); }
warn() { say "WARN  $*"; }

# 1. tools on PATH (git: host/owner derivation; jq: reference-doc pipelines)
for tool in python3 git glab gh jq; do
  if command -v "$tool" > /dev/null 2>&1; then
    say "PASS  $tool: $(command -v $tool)"
  else
    case "$tool" in
      glab) fail "glab not on PATH — install the GitLab CLI (https://gitlab.com/gitlab-org/cli)" ;;
      gh)   fail "gh not on PATH — install the GitHub CLI (https://cli.github.com)" ;;
      jq)   fail "jq not on PATH — install jq (https://jqlang.github.io/jq)" ;;
      *)    fail "$tool not on PATH" ;;
    esac
  fi
done

# 2. glab auth — multi-instance aware: the scripts derive the host from the
#    git remote and read that host's token from glab config, so at least ONE
#    host must be logged in. `glab auth status` exits non-zero if ANY
#    configured host fails (e.g. a rotting token on an unused host) — that is
#    a WARN, not a FAIL, as long as some host still works.
if command -v glab > /dev/null 2>&1; then
  glab_out=$(glab auth status 2>&1); glab_rc=$?
  hosts=$(printf '%s\n' "$glab_out" | grep -o 'Logged in to [^ ]*' | cut -d' ' -f4 | paste -sd, -)
  if [ -z "$hosts" ]; then
    fail "glab installed but no host authenticated — run: glab auth login --hostname <your-gitlab-host>"
  elif [ "$glab_rc" -eq 0 ]; then
    say "PASS  glab auth: $hosts"
  else
    warn "glab auth works for [$hosts] but 'glab auth status' exit $glab_rc — another configured host is failing; check: glab auth status"
  fi
fi

# 3. gh auth
if command -v gh > /dev/null 2>&1; then
  gh_out=$(gh auth status 2>&1); gh_rc=$?
  if [ "$gh_rc" -eq 0 ]; then
    acct=$(printf '%s\n' "$gh_out" | grep -oE 'account [A-Za-z0-9_-]+' | head -1 | cut -d' ' -f2)
    say "PASS  gh auth: ${acct:-logged in}"
  else
    fail "gh installed but not authenticated — run: gh auth login"
  fi
fi

# 4. python imports — the stdlib modules the scripts use
if command -v python3 > /dev/null 2>&1; then
  missing=""
  for mod in json os re subprocess sys time random urllib.parse; do
    python3 -c "import $mod" 2>/dev/null || missing="$missing $mod"
  done
  if [ -n "$missing" ]; then
    fail "python3 missing stdlib modules:$missing — broken python3 install?"
  else
    say "PASS  python3 stdlib deps: json os re subprocess sys time random urllib.parse"
  fi
  # the backend modules every entry script imports (also validates scripts/ is intact)
  if (cd "$SKILL_DIR/scripts" && python3 -c "import ocr_platform, ocr_gitlab, ocr_github" 2>/dev/null); then
    say "PASS  backend modules import: ocr_platform, ocr_gitlab, ocr_github"
  else
    fail "backend modules fail to import — check: cd $SKILL_DIR/scripts && python3 -c 'import ocr_gitlab'"
  fi
fi

if [ "$fails" -gt 0 ]; then
  say "---"
  say "ENVIRONMENT BROKEN: $fails check(s) failed"
  exit 1
fi
say "---"
say "ENVIRONMENT OK"
exit 0
