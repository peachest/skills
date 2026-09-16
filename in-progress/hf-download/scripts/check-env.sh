#!/usr/bin/env bash
# check-env for hf-download skill (PASS/WARN/FAIL semantics, FAIL exits 1).
# Run on a new node before first real download: bash <SKILL_DIR>/scripts/check-env.sh
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fail=0; warn=0

note() { echo "[$1] $2"; }

# optional runtime.conf (proxy / mirror values, per node, gitignored)
if [ -f "$DIR/runtime.conf" ]; then
    # shellcheck disable=SC1091
    . "$DIR/runtime.conf"
    note PASS "runtime.conf loaded"
else
    note WARN "no runtime.conf (copy scripts/runtime.conf.example if this node needs a proxy/mirror)"
fi

# curl: required by hfd metadata fetch
if command -v curl >/dev/null 2>&1; then
    note PASS "curl $(curl --version | head -1 | awk '{print $2}')"
else
    note FAIL "curl not installed — required by hfd"
    fail=1
fi

# aria2c: multi-thread engine; wget is the documented fallback
if command -v aria2c >/dev/null 2>&1; then
    note PASS "aria2c $(aria2c --version | head -1 | awk '{print $3}')"
else
    note WARN "aria2c not installed — use 'hfd --tool wget', or install aria2 (nix: nix-env -iA nixpkgs.aria2)"
    warn=$((warn+1))
fi

# jq: optional, faster metadata parsing
command -v jq >/dev/null 2>&1 && note PASS "jq present" || { note WARN "jq missing — hfd falls back to grep/awk (slower)"; warn=$((warn+1)); }

# hfd: installed and runnable
hfd_ok() { "$1" --help 2>&1 | head -1 | grep -q '^Usage:'; }
if [ -x "$HOME/.local/bin/hfd" ] && hfd_ok "$HOME/.local/bin/hfd"; then
    note PASS "hfd at ~/.local/bin/hfd"
elif command -v hfd >/dev/null 2>&1 && hfd_ok hfd; then
    note PASS "hfd on PATH"
else
    note WARN "hfd not installed — install with: cp $DIR/hfd ~/.local/bin/hfd && chmod +x ~/.local/bin/hfd"
    warn=$((warn+1))
fi

# HF reachability: direct first, then configured proxy
probe() { curl -sI -o /dev/null -m 10 -w '%{http_code}' "$1" 2>/dev/null; }
code=$(probe "https://huggingface.co")
if [ "$code" = "200" ] || [ "$code" = "302" ]; then
    note PASS "huggingface.co reachable (direct)"
else
    if [ -n "${HF_PROXY:-}" ]; then
        code=$(probe "https://huggingface.co" ) # placeholder to keep style
        code=$(curl -sI -o /dev/null -m 10 -w '%{http_code}' -x "$HF_PROXY" https://huggingface.co 2>/dev/null)
        if [ "$code" = "200" ] || [ "$code" = "302" ]; then
            note PASS "huggingface.co reachable via HF_PROXY"
        else
            note FAIL "huggingface.co unreachable direct and via HF_PROXY=$HF_PROXY (code=$code)"
            fail=1
        fi
    else
        note FAIL "huggingface.co unreachable (code=$code) — set HF_PROXY in scripts/runtime.conf or use HF_ENDPOINT mirror"
        fail=1
    fi
fi

echo "---"
if [ "$fail" -eq 1 ]; then echo "RESULT: FAIL — fix [FAIL] items above, exit 1"; exit 1; fi
echo "RESULT: PASS (${warn} warning(s))"
