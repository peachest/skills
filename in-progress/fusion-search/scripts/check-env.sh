#!/usr/bin/env bash
# fusion-search environment self-check. Every FAIL line is the install instruction.
set -u
FAIL=0

command -v uv >/dev/null || { echo "FAIL: uv not installed — curl -LsSf https://astral.sh/uv/install.sh | sh"; FAIL=1; }
[ -n "${DEEPSEEK_API_KEY:-}" ] || echo "WARN: DEEPSEEK_API_KEY not in this shell's env (pi credential system injects it when the command text contains \$DEEPSEEK_API_KEY)"

CLI="$HOME/.agents/skills/anysearch/scripts/anysearch_cli.py"
[ -n "${ANYSEARCH_CLI:-}" ] && CLI="$ANYSEARCH_CLI"
[ -f "$CLI" ] || { echo "FAIL: anysearch CLI missing at $CLI — npx skills add -g <anysearch-source> -a pi -y (or set ANYSEARCH_CLI)"; FAIL=1; }

CONF="$(dirname "$0")/../runtime.conf"
[ -f "$CONF" ] || { echo "FAIL: runtime.conf missing — cp runtime.conf.example runtime.conf and fill JUDGE_URL/JUDGE_MODEL"; FAIL=1; }
else_check() { :; }

JUDGE_URL=$(grep -E '^JUDGE_URL=' "$CONF" 2>/dev/null | cut -d= -f2-)
JUDGE_MODEL=$(grep -E '^JUDGE_MODEL=' "$CONF" 2>/dev/null | cut -d= -f2-)
if [ -n "$JUDGE_URL" ] && [ -n "$JUDGE_MODEL" ]; then
  code=$(curl -s -o /dev/null -w '%{http_code}' -m 10 "$JUDGE_URL" -H 'Content-Type: application/json' \
    -d "{\"model\":\"$JUDGE_MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}],\"max_tokens\":1}" || echo 000)
  [ "$code" = "200" ] || { echo "FAIL: judge endpoint $JUDGE_URL unreachable (http $code) — verify VPN/gateway"; FAIL=1; }
fi

if [ -n "${DEEPSEEK_API_KEY:-}" ]; then
  code=$(curl -s -o /dev/null -w '%{http_code}' -m 10 https://api.deepseek.com/v1/tools/search \
    -H "Authorization: Bearer $DEEPSEEK_API_KEY" -H 'Content-Type: application/json' -d '{"query":"ping","count":1}')
  case "$code" in
    200|400) : ;;
    401) echo "FAIL: DEEPSEEK_API_KEY rejected (401) — re-enter credential"; FAIL=1 ;;
    *) echo "FAIL: api.deepseek.com unreachable (http $code) — check proxy"; FAIL=1 ;;
  esac
fi

[ "$FAIL" = 0 ] && echo "check-env: GREEN" || echo "check-env: RED"
exit $FAIL
