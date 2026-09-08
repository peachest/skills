#!/usr/bin/env bash
# html-render-check environment self-check.
# PASS/WARN/FAIL per item; any FAIL -> exit 1. Self-locating, fast, idempotent.

SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
CONF="$SKILL_DIR/runtime.conf"

[ -f "$CONF" ] && . "$CONF"
PLAYWRIGHT_DIR="${PLAYWRIGHT_DIR:-$HOME/tools/playwright-runner}"

fail_count=0

# 1. node
if command -v node >/dev/null 2>&1; then
  echo "PASS node — $(node --version)"
else
  echo "FAIL node — not on PATH; install Node.js (>= 18)"
  fail_count=$((fail_count+1))
fi

# 2. playwright module (in PLAYWRIGHT_DIR, not the skill repo — repo is public)
if [ -f "$PLAYWRIGHT_DIR/node_modules/playwright/package.json" ]; then
  ver=$(node -e "console.log(require('$PLAYWRIGHT_DIR/node_modules/playwright/package.json').version)" 2>/dev/null)
  echo "PASS playwright module — $PLAYWRIGHT_DIR (${ver:-unknown})"
else
  echo "FAIL playwright module — not found in $PLAYWRIGHT_DIR. Setup:"
  echo "     mkdir -p $PLAYWRIGHT_DIR && cd $PLAYWRIGHT_DIR && npm init -y && npm install playwright"
  echo "     (on the internal cluster, export http_proxy/https_proxy first)"
  fail_count=$((fail_count+1))
fi

# 3. chromium binary (shared Playwright browser cache)
PW_CACHE="${PW_BROWSERS_PATH:-$HOME/.cache/ms-playwright}"
if ls "$PW_CACHE"/chromium* >/dev/null 2>&1; then
  echo "PASS chromium — $(ls "$PW_CACHE" | grep '^chromium' | head -3 | tr '\n' ' ')"
else
  echo "FAIL chromium — not installed in $PW_CACHE. Install:"
  echo "     cd $PLAYWRIGHT_DIR && npx playwright install chromium --only-shell"
  echo "     (downloads ~100-170MB via the network; use the corporate proxy if direct access is blocked)"
  fail_count=$((fail_count+1))
fi

# 4. chromium system libraries (probe the actual binary, not a package guess)
CHROME_BIN=$(ls "$PW_CACHE"/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2>/dev/null | head -1)
if [ -n "$CHROME_BIN" ] && [ -x "$CHROME_BIN" ]; then
  missing=$(ldd "$CHROME_BIN" 2>/dev/null | grep "not found" | awk '{print $1}' | sort -u | tr '\n' ' ')
  if [ -z "$missing" ]; then
    echo "PASS chromium system libs — all shared libraries resolve"
  else
    echo "FAIL chromium system libs — missing: $missing"
    echo "     fix (Debian/Ubuntu): sudo apt install libgbm1 libxkbcommon0 (add others as ldd reports)"
    fail_count=$((fail_count+1))
  fi
else
  echo "WARN chromium system libs — chromium binary not found, cannot probe ldd; re-run after installing chromium"
fi

# 5. sandbox feasibility (informational — render-check defaults to --no-sandbox)
if [ "$(id -u)" = "0" ] || [ ! -w /proc/sys/kernel/unprivileged_userns_clone ] || \
   [ "$(cat /proc/sys/kernel/unprivileged_userns_clone 2>/dev/null)" = "1" ]; then
  echo "PASS sandbox — userns available or running as root; PW_SANDBOX=1 optional"
else
  echo "WARN sandbox — unprivileged userns disabled; render-check launches with --no-sandbox (default on cluster nodes)"
fi

# 6. python3 stdlib (structure layer)
if command -v python3 >/dev/null 2>&1 && python3 -c "import http.server" 2>/dev/null; then
  echo "PASS python3 (structure layer) — stdlib available"
else
  echo "FAIL python3 — not on PATH or stdlib broken; the structure layer needs it"
  fail_count=$((fail_count+1))
fi

# 7. strict-mode optional deps (WARN only)
python3 -c "import html5lib" 2>/dev/null && \
  echo "PASS html5lib (--strict spec parsing available)" || \
  echo "WARN html5lib — not installed; --strict spec parsing disabled (pip install html5lib)"
if [ -f ~/.vnu/vnu.jar ]; then
  echo "PASS vnu.jar (--strict W3C validation available)"
else
  echo "WARN vnu.jar — not at ~/.vnu/vnu.jar; --strict W3C validation disabled"
fi

if [ "$fail_count" -gt 0 ]; then
  echo "---"
  echo "RESULT: FAIL ($fail_count failed checks)"
  exit 1
fi
echo "---"
echo "RESULT: PASS"
