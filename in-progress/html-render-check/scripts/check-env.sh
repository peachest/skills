#!/usr/bin/env bash
# html-render-check environment self-check.
# PASS/WARN/FAIL per item; any FAIL -> exit 1. Self-locating, fast, idempotent.

SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
CONF="$SKILL_DIR/runtime.conf"

# Load runtime.conf, falling back to defaults for anything unset.
[ -f "$CONF" ] && . "$CONF"
OBSCURA_BIN="${OBSCURA_BIN:-obscura}"
CHECK_PORT="${CHECK_PORT:-8742}"
PI_MCP_CONFIG="${PI_MCP_CONFIG:-$HOME/.pi/agent/mcp.json}"

fail_count=0

check_bin() {
  # Resolve OBSCURA_BIN: a path (test executable) or a command name (command -v).
  if command -v "$OBSCURA_BIN" >/dev/null 2>&1; then
    local resolved
    resolved=$(command -v "$OBSCURA_BIN")
  elif [ -x "$OBSCURA_BIN" ]; then
    local resolved="$OBSCURA_BIN"
  else
    echo "FAIL obscura binary — not found or not executable ('$OBSCURA_BIN'). Reinstall:"
    echo "     cd ~/tmp && curl -sLO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-x86_64-linux-stealth.tar.gz && \\"
    echo "       tar xzf obscura-x86_64-linux-stealth.tar.gz && cp obscura obscura-worker ~/.local/bin/ && chmod +x ~/.local/bin/obscura*"
    echo "     (The binary has been lost once before on this fleet — it does not survive node re-imaging.)"
    fail_count=$((fail_count+1))
    return 1
  fi
  local ver
  ver=$("$resolved" --version 2>&1) || {
    echo "FAIL obscura binary — found at $resolved but --version failed: $ver"
    fail_count=$((fail_count+1))
    return 1
  }
  echo "PASS obscura binary — $resolved ($ver)"
}

check_worker() {
  local bin_dir resolved
  if command -v "$OBSCURA_BIN" >/dev/null 2>&1; then
    resolved=$(command -v "$OBSCURA_BIN")
  else
    resolved="$OBSCURA_BIN"
  fi
  bin_dir=$(dirname "$resolved")
  if [ -x "$bin_dir/obscura-worker" ]; then
    echo "PASS obscura-worker — $bin_dir/obscura-worker"
  else
    echo "FAIL obscura-worker — missing next to the binary ($bin_dir/obscura-worker). The fetch pipeline spawns it; reinstall both from the release tarball (see obscura FAIL above)."
    fail_count=$((fail_count+1))
  fi
}

check_python() {
  if command -v python3 >/dev/null 2>&1; then
    if python3 -c "import http.server" 2>/dev/null; then
      echo "PASS python3 http.server — stdlib available"
    else
      echo "FAIL python3 http.server — python3 exists but stdlib import failed; fix the python3 installation"
      fail_count=$((fail_count+1))
    fi
  else
    echo "FAIL python3 — not on PATH; the verification server needs it"
    fail_count=$((fail_count+1))
  fi
}

check_port_free() {
  if python3 - <<EOF 2>/dev/null
import socket, sys
s = socket.socket()
try:
    s.bind(("", $CHECK_PORT))
except OSError:
    sys.exit(1)
finally:
    s.close()
EOF
  then
    echo "PASS check port $CHECK_PORT — bindable"
  else
    echo "WARN check port $CHECK_PORT — in use or unbindable; check.sh will still try it, override CHECK_PORT in runtime.conf if this recurs"
  fi
}

check_mcp() {
  if [ -f "$PI_MCP_CONFIG" ] && grep -q '"obscura"' "$PI_MCP_CONFIG" 2>/dev/null; then
    echo "PASS obscura MCP server — configured in $PI_MCP_CONFIG"
  else
    echo "WARN obscura MCP server — not found in $PI_MCP_CONFIG; CLI mode (primary) works without it, MCP mode (console errors, multi-step) unavailable"
  fi
}

check_bin && check_worker
check_python
check_port_free
check_mcp

if [ "$fail_count" -gt 0 ]; then
  echo "---"
  echo "RESULT: FAIL ($fail_count failed checks)"
  exit 1
fi
echo "---"
echo "RESULT: PASS"
