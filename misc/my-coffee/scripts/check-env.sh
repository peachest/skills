#!/usr/bin/env bash
# check-env.sh — verify the my-coffee MCP server runtime assumptions.
#
# The skill's only external dependency is the `my-coffee` MCP server
# (streamableHttp, Luckin order API). No runtime.conf: the server config
# lives in pi's MCP registry — ~/.pi/agent/mcp.json (mcpServers."my-coffee"),
# with ~/.pi/agent/settings.json (mcpServers key) as a fallback location.
#
# Usage: bash check-env.sh   (from anywhere; CWD does not matter)
# FAIL only on missing config; network problems are WARNs (transient or
# proxy-related). Never prints the Authorization token or config contents.

set -u
fails=0

say() { printf '%s\n' "$*"; }
fail() { say "FAIL  $*"; fails=$((fails+1)); }
warn() { say "WARN  $*"; }

MCP_JSON="$HOME/.pi/agent/mcp.json"
SETTINGS_JSON="$HOME/.pi/agent/settings.json"

# 1. my-coffee MCP server entry in pi config (exact JSON parse when python3
#    is available; grep fallback on the "key": shape otherwise)
CONF=""
for f in "$MCP_JSON" "$SETTINGS_JSON"; do
  [ -f "$f" ] || continue
  if command -v python3 > /dev/null 2>&1; then
    python3 -c "import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if 'my-coffee' in (d.get('mcpServers') or {}) else 1)" "$f" 2>/dev/null && CONF="$f"
  else
    grep -q '"my-coffee":' "$f" 2>/dev/null && CONF="$f"
  fi
  [ -n "$CONF" ] && break
done
if [ -z "$CONF" ]; then
  fail "my-coffee MCP server not configured — add a \"my-coffee\" entry under mcpServers in ~/.pi/agent/mcp.json (config block in SKILL.md 前置条件)"
else
  say "PASS  my-coffee MCP entry: $CONF"
fi

# 2. token availability (priority per SKILL.md: env LUCKIN_MCP_TOKEN >
#    user-provided > ~/.my-coffee/LUCKIN_MCP_TOKEN; the mcp.json entry may
#    embed it as an Authorization header)
token_src=""
[ -n "${LUCKIN_MCP_TOKEN:-}" ] && token_src="env LUCKIN_MCP_TOKEN"
if [ -z "$token_src" ] && [ -f "$HOME/.my-coffee/LUCKIN_MCP_TOKEN" ]; then
  token_src="~/.my-coffee/LUCKIN_MCP_TOKEN"
fi
if [ -z "$token_src" ] && [ -n "$CONF" ] && command -v python3 > /dev/null 2>&1; then
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); h=((d.get('mcpServers') or {}).get('my-coffee') or {}).get('headers') or {}; sys.exit(0 if h.get('Authorization') else 1)" "$CONF" 2>/dev/null \
    && token_src="Authorization header in $CONF"
fi
if [ -n "$token_src" ]; then
  say "PASS  LUCKIN token source: $token_src"
else
  warn "no LUCKIN_MCP_TOKEN found (env, ~/.my-coffee/LUCKIN_MCP_TOKEN, or mcp.json headers) — the token must come from the user per SKILL.md"
fi

# 3. endpoint reachability — extract the url (never the headers), probe
#    direct, then via proxy (env, then pi's ~/.pi/agent/proxy.env)
if [ -n "$CONF" ]; then
  URL=""
  if command -v python3 > /dev/null 2>&1; then
    URL=$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(((d.get('mcpServers') or {}).get('my-coffee') or {}).get('url') or '')" "$CONF" 2>/dev/null || true)
  else
    URL=$(grep -A10 '"my-coffee":' "$CONF" 2>/dev/null | grep -oE '"url"[[:space:]]*:[[:space:]]*"[^"]+"' | head -1 | sed 's/.*"\(https\?:[^"]*\)".*/\1/')
  fi
  if [ -z "$URL" ]; then
    warn "my-coffee entry has no url — skipping endpoint probe (non-HTTP transport?)"
  elif ! command -v curl > /dev/null 2>&1; then
    warn "curl not on PATH — cannot probe $URL"
  else
    say "PASS  endpoint configured: $URL"
    code=$(curl -s -o /dev/null -w '%{http_code}' --noproxy '*' --max-time 5 "$URL" 2>/dev/null || true)
    if [ -n "$code" ] && [ "$code" != "000" ]; then
      say "PASS  endpoint reachable direct (HTTP $code)"
    else
      proxy="${https_proxy:-${HTTPS_PROXY:-}}"
      if [ -z "$proxy" ] && [ -f "$HOME/.pi/agent/proxy.env" ]; then
        proxy=$(grep -E '^(https_proxy|HTTPS_PROXY)=' "$HOME/.pi/agent/proxy.env" | head -1 | cut -d= -f2-)
      fi
      if [ -n "$proxy" ]; then
        code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 -x "$proxy" "$URL" 2>/dev/null || true)
        if [ -n "$code" ] && [ "$code" != "000" ]; then
          say "PASS  endpoint reachable via proxy (HTTP $code)"
        else
          p_show=$(printf '%s' "$proxy" | sed 's#//[^/@]*@#//<creds>@#')
          warn "endpoint unreachable (direct and via proxy $p_show) — MCP calls will fail until the network path works"
        fi
      else
        warn "endpoint unreachable direct and no proxy configured — MCP calls will fail until the network path works"
      fi
    fi
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
