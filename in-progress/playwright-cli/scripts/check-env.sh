#!/usr/bin/env bash
# check-env for playwright-cli skill: verifies the runtime assumptions this skill depends on.
# FAIL (exit 1) = skill cannot work; WARN = degraded; PASS = ok.
set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

fail=0; warn=0
report() { # level name detail
  printf '%-4s %-28s %s\n' "$1" "$2" "$3"
  [ "$1" = FAIL ] && fail=1
  [ "$1" = WARN ] && warn=1
}

# 1. playwright-cli binary + version (install: see runtime.conf.example)
PW_BIN="${PLAYWRIGHT_CLI_BIN:-$HOME/tools/playwright-cli/node_modules/.bin/playwright-cli}"
if [ -x "$PW_BIN" ]; then
  ver=$("$PW_BIN" --version 2>/dev/null)
  report PASS "playwright-cli" "$ver at $PW_BIN"
  case "$ver" in
    0.*) report WARN "version-drift" "0.x release — re-verify commands after any upgrade" ;;
  esac
else
  report FAIL "playwright-cli" "missing: $PW_BIN (install per runtime.conf.example)"
fi

# 2. playwright library for raw-script fallback + screencast
RUNNER="${PLAYWRIGHT_CLI_RUNNER:-$HOME/tools/playwright-runner}"
if node -e "require('$RUNNER/node_modules/playwright')" 2>/dev/null; then
  rver=$(node -e "console.log(require('$RUNNER/node_modules/playwright/package.json').version)" 2>/dev/null)
  report PASS "playwright-runner" "v$rver"
else
  report FAIL "playwright-runner" "cannot require playwright from $RUNNER"
fi

# 3. chromium browser binary
if ls "$HOME/.cache/ms-playwright"/chromium_headless_shell-* >/dev/null 2>&1 || ls "$HOME/.cache/ms-playwright"/chromium-* >/dev/null 2>&1; then
  report PASS "chromium" "present in ~/.cache/ms-playwright"
else
  report FAIL "chromium" "none in ~/.cache/ms-playwright (run: npx playwright install chromium)"
fi

# 4. proxy situation — warn if internal hosts would be tunneled
if [ -n "${http_proxy:-}" ]; then
  # cannot enumerate no_proxy targets here (generic skill); just surface the risk
  report WARN "proxy-env" "http_proxy is set ($http_proxy) — internal targets must be in no_proxy or commands must sanitize env"
else
  report PASS "proxy-env" "no proxy set"
fi

echo "---"
[ $fail -eq 1 ] && { echo "RESULT: FAIL"; exit 1; }
[ $warn -eq 1 ] && { echo "RESULT: PASS (with warnings)"; exit 0; }
echo "RESULT: PASS"
