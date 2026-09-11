#!/usr/bin/env bash
# check-env.sh — verify every runtime assumption the fetch-article adapters
# depend on: python3 + its imports, aria2c, ffmpeg resolution, markitdown,
# scrapling, bilibili API reachability, proxy env.
#
# No runtime.conf: every endpoint the adapters touch is public and hardcoded
# in the adapter source (api.bilibili.com, mp.weixin.qq.com, arbitrary user
# URLs) — there are no node-specific values to configure.
#
# Usage: bash check-env.sh   (from anywhere; CWD does not matter)
# Run it on a new node or before a long fetch batch.
# PASS/WARN lines are informational; any FAIL exits 1.

set -u
SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
fails=0

say() { printf '%s\n' "$*"; }
fail() { say "FAIL  $*"; fails=$((fails+1)); }
warn() { say "WARN  $*"; }

# 1. tools on PATH (curl: weixin adapter + generic fallback fetching)
for tool in python3 curl; do
  command -v "$tool" > /dev/null 2>&1 && say "PASS  $tool: $(command -v $tool)" \
    || fail "$tool not on PATH"
done

# 2. aria2c — mirrors adapters/bilibili.py _find_aria2c(): PATH, then ~/scripts/aria2c
aria2c_bin=""
if command -v aria2c > /dev/null 2>&1; then
  aria2c_bin=$(command -v aria2c)
elif [ -x "$HOME/scripts/aria2c" ]; then
  aria2c_bin="$HOME/scripts/aria2c"
fi
if [ -n "$aria2c_bin" ]; then
  say "PASS  aria2c: $aria2c_bin"
else
  fail "aria2c not found (PATH or ~/scripts/aria2c) — bilibili audio download will fail (CC-subtitle-only videos still work)"
fi

# 3. ffmpeg — mirrors adapters/bilibili.py _resolve_ffmpeg(): imageio_ffmpeg
#    pip package first, then system PATH; needed only for multi-segment durl concat
if command -v python3 > /dev/null 2>&1 && python3 -c "import imageio_ffmpeg" 2>/dev/null; then
  say "PASS  ffmpeg: imageio_ffmpeg (bundled static binary)"
elif command -v ffmpeg > /dev/null 2>&1; then
  say "PASS  ffmpeg: $(command -v ffmpeg)"
else
  warn "ffmpeg not resolvable (neither imageio_ffmpeg pip package nor PATH) — only multi-segment durl concat needs it (pip install imageio-ffmpeg)"
fi

# 4. python deps (requests: bilibili WBI API, hard import; bs4: to_md.py
#    metadata extraction, degrades to regex)
if command -v python3 > /dev/null 2>&1; then
  if python3 -c "import requests" 2>/dev/null; then
    say "PASS  python3 deps: requests (bilibili WBI API)"
  else
    fail "python3 lacks requests — bilibili adapter will crash (pip install requests)"
  fi
  if python3 -c "import bs4" 2>/dev/null; then
    say "PASS  python3 deps: bs4 (weixin metadata extraction)"
  else
    warn "python3 lacks bs4 — to_md.py falls back to regex metadata (pip install beautifulsoup4)"
  fi
fi

# 5. markitdown CLI — to_md.py body conversion, degrades to tag stripping
if command -v markitdown > /dev/null 2>&1; then
  say "PASS  markitdown: $(command -v markitdown)"
else
  warn "markitdown CLI not on PATH — to_md.py falls back to HTML tag stripping (pip install markitdown)"
fi

# 6. scrapling — generic adapter anti-bot path; generic.py needs BOTH the
#    python module (its probe) and the CLI (its invocation); curl fallback exists
if command -v python3 > /dev/null 2>&1; then
  scrapling_mod=0; scrapling_cli=0
  python3 -c "import scrapling" 2>/dev/null && scrapling_mod=1
  command -v scrapling > /dev/null 2>&1 && scrapling_cli=1
  if [ "$scrapling_mod" -eq 1 ] && [ "$scrapling_cli" -eq 1 ]; then
    say "PASS  scrapling: module + CLI (generic adapter anti-bot path)"
  elif [ "$scrapling_mod" -eq 0 ] && [ "$scrapling_cli" -eq 0 ]; then
    warn "scrapling not installed — generic adapter falls back to curl, anti-bot sites will fail (pip install \"scrapling[all]\" && scrapling install)"
  else
    warn "scrapling half-installed (module=$scrapling_mod cli=$scrapling_cli) — generic adapter needs both, falls back to curl meanwhile"
  fi
fi

# 7. bilibili API reachability (the bilibili adapter's first network call).
#    WARN on failure: network may be proxied or transiently down.
if command -v curl > /dev/null 2>&1; then
  if curl -s -o /dev/null --noproxy '*' --max-time 6 https://api.bilibili.com/x/web-interface/nav; then
    say "PASS  api.bilibili.com direct"
  elif curl -s -o /dev/null --max-time 6 https://api.bilibili.com/x/web-interface/nav; then
    say "PASS  api.bilibili.com via proxy"
  else
    warn "api.bilibili.com unreachable (direct and via proxy) — bilibili adapter will fail; check network/proxy"
  fi
fi

# 8. proxy env report (bilibili.py feeds https_proxy to aria2c --all-proxy;
#    curl honors http_proxy/https_proxy). Credentials redacted.
proxy_vars=""
for v in http_proxy https_proxy HTTP_PROXY HTTPS_PROXY; do
  eval "val=\${$v:-}"
  [ -n "$val" ] && proxy_vars="$proxy_vars $v"
done
if [ -n "$proxy_vars" ]; then
  p=$(printf '%s' "${https_proxy:-${HTTPS_PROXY:-${http_proxy:-${HTTP_PROXY:-}}}}")
  p_show=$(printf '%s' "$p" | sed 's#//[^/@]*@#//<creds>@#')
  say "PASS  proxy env:$proxy_vars — downloads via $p_show"
else
  say "PASS  proxy env: none (direct network)"
fi

if [ "$fails" -gt 0 ]; then
  say "---"
  say "ENVIRONMENT BROKEN: $fails check(s) failed"
  exit 1
fi
say "---"
say "ENVIRONMENT OK"
exit 0
