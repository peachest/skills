#!/usr/bin/env bash
# Verify the active ocr provider config actually sends extra_body (thinking-disable)
# to the LLM gateway — by replaying the REAL config against a local fake OpenAI
# server and inspecting the captured request body.
#
# Why: when `provider <name>` is active, ocr ignores every `llm.*` setting
# (including llm.extra_body). Reading the config file cannot prove what goes on
# the wire; only a captured request can. Adapted from
# ~/projects/ocr-image/diagnostics (fake-llm-server.py + config test matrix).
#
# Usage:
#   bash <SKILL_DIR>/scripts/check-config.sh
#   OCR_CHECK_PORT=18999 bash <SKILL_DIR>/scripts/check-config.sh   # port override
#
# Exit codes: 0 = PASS, 1 = setup/config problem, 2 = thinking fields missing
# from the wire (fix extra_body), 3 = no request captured.
set -uo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="$HOME/.opencodereview/config.json"
PORT="${OCR_CHECK_PORT:-18765}"
WORK="$(mktemp -d)"
SERVER_PID=""

cleanup() {
  [ -n "$SERVER_PID" ] && kill "$SERVER_PID" 2>/dev/null
  rm -rf "$WORK"
}
trap cleanup EXIT

FIX_HINT="Fix (SKILL.md chapter 2):
  ocr config set custom_providers.<name>.extra_body '{\"thinking\": {\"type\": \"disabled\"}, \"chat_template_kwargs\": {\"enable_thinking\": false}}'
Note: llm.extra_body is ignored when a provider is active."

command -v ocr >/dev/null 2>&1 || { echo "FAIL: ocr not installed"; exit 1; }
[ -f "$CONFIG" ] || { echo "FAIL: $CONFIG not found — configure the provider first (SKILL.md chapter 2)"; exit 1; }

# --- 1. Parse config, build a patched copy pointing at the fake server ---------
# python exit codes: 0 ok (patched written) / 10 no active provider /
# 11 provider entry missing / 12 static extra_body missing (informational, continue)
PATCHED="$WORK/config.json"
python3 - "$CONFIG" "$PATCHED" "http://127.0.0.1:$PORT/v1" <<'PY'
import json, sys
src, dst, fake_url = sys.argv[1], sys.argv[2], sys.argv[3]
cfg = json.load(open(src))
provider = cfg.get("provider") or ""
if not provider:
    print("FAIL: no active provider — ocr would fall back to llm.*/env paths")
    sys.exit(10)
cps = cfg.setdefault("custom_providers", {})
entry = cps.get(provider)
if not isinstance(entry, dict):
    print(f"FAIL: provider '{provider}' is active but custom_providers.{provider} is missing")
    sys.exit(11)
eb = entry.get("extra_body") or {}
think = (eb.get("thinking") or {}).get("type")
ctk = (eb.get("chat_template_kwargs") or {}).get("enable_thinking")
if think != "disabled" or ctk is not False:
    print(f"WARN: static check — extra_body at custom_providers.{provider}.extra_body has "
          f"thinking.type={think!r}, enable_thinking={ctk!r} (expected 'disabled' / False)")
    code = 12
else:
    print(f"static check: extra_body present at custom_providers.{provider}.extra_body")
    code = 0
if cfg.get("llm", {}).get("extra_body"):
    print("note: llm.extra_body is also set — it is IGNORED while a provider is active")
entry["url"] = fake_url  # api_key stays, only ever travels to the local fake server
json.dump(cfg, open(dst, "w"), ensure_ascii=False, indent=2)
sys.exit(code)
PY
rc=$?
[ "$rc" -eq 10 ] || [ "$rc" -eq 11 ] && exit 1
echo "dynamic check: replaying config against fake server on :$PORT ..."

# --- 2. Start fake server and wait for it to listen ---------------------------
python3 "$SKILL_DIR/scripts/fake-llm-server.py" "$PORT" "$WORK/requests.jsonl" \
  >"$WORK/server.log" 2>&1 &
SERVER_PID=$!
listening=""
for _ in $(seq 1 25); do
  if python3 -c "import socket,sys; s=socket.socket(); s.settimeout(0.2); sys.exit(0 if s.connect_ex(('127.0.0.1', $PORT))==0 else 1)"; then
    listening=1; break
  fi
  sleep 0.2
done
if [ -z "$listening" ]; then
  echo "FAIL: fake server did not start (port $PORT busy? try OCR_CHECK_PORT=...)"
  cat "$WORK/server.log" 2>/dev/null
  exit 1
fi

# --- 3. Replay one llm test through the patched config ------------------------
OCR_CONFIG_PATH="$PATCHED" ocr llm test >/dev/null 2>&1 || true

# --- 4. Inspect the captured request body --------------------------------------
python3 - "$WORK/requests.jsonl" <<'PY'
import json, sys
reqs = []
try:
    for line in open(sys.argv[1]):
        line = line.strip()
        if line:
            reqs.append(json.loads(line))
except FileNotFoundError:
    pass
if not reqs:
    print("FAIL: no request captured — ocr llm test did not reach the fake server")
    sys.exit(3)
body = reqs[0].get("body") if isinstance(reqs[0].get("body"), dict) else {}
think = (body.get("thinking") or {}).get("type")
ctk = (body.get("chat_template_kwargs") or {}).get("enable_thinking")
if think == "disabled" and ctk is False:
    print(f"PASS: request body carries thinking=disabled, enable_thinking=False "
          f"({len(reqs)} request(s) captured)")
    sys.exit(0)
print(f"FAIL: on the wire thinking.type={think!r}, enable_thinking={ctk!r} — "
      "thinking-disable is NOT being sent")
sys.exit(2)
PY
rc=$?
[ "$rc" -eq 2 ] && echo "$FIX_HINT"
exit "$rc"
