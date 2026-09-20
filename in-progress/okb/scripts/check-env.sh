#!/usr/bin/env bash
# check-env.sh — verify runtime assumptions of the okb scripts.
# Usage: bash scripts/check-env.sh [runtime.conf]   (default: <skill_dir>/runtime.conf)
set -u
SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
CONF="${1:-$SKILL_DIR/runtime.conf}"
fails=0
say() { printf '%s\n' "$*"; }
ok() { say "PASS: $*"; }
warn() { say "WARN: $*"; }
fail() { say "FAIL: $*"; fails=$((fails + 1)); }

# python3 >= 3.10 (scripts use pathlib/zoneinfo-free stdlib)
if command -v python3 >/dev/null; then
  v=$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')
  ok "python3 $v"
else
  fail "python3 not found"
fi

# optional proxy from runtime.conf
if [ -f "$CONF" ]; then
  # shellcheck disable=SC1090
  . "$CONF"
  [ -n "${ARXIV_PROXY:-}" ] && ok "ARXIV_PROXY set: $ARXIV_PROXY" || ok "ARXIV_PROXY empty (direct access)"
else
  warn "runtime.conf absent — copying example is optional (scripts work without it)"
fi

# arXiv reachability (skippable offline)
if [ "${SKIP_NETWORK:-0}" = "1" ]; then
  warn "SKIP_NETWORK=1 — skipping arXiv probe"
else
  if python3 - << 'PY'
import os, sys, urllib.request
proxy = os.environ.get("ARXIV_PROXY", "").strip()
h = {"User-Agent": "okb-check-env/0.1"}
if proxy:
    h = {}
    urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy})))
try:
    req = urllib.request.Request("https://export.arxiv.org/api/query?id_list=1706.03762", headers=h)
    urllib.request.urlopen(req, timeout=15)
    sys.exit(0)
except Exception as e:
    print(e, file=sys.stderr); sys.exit(1)
PY
  then ok "arXiv export API reachable"
  else fail "arXiv export API unreachable (set ARXIV_PROXY in runtime.conf, or SKIP_NETWORK=1)"
  fi
fi

say ""
if [ "$fails" -eq 0 ]; then say "check-env: ALL PASS"; else say "check-env: $fails FAIL(s)"; exit 1; fi
