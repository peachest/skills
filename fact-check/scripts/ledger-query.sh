#!/bin/bash
# ledger-query.sh — Query per-document JSONL ledgers for stats and history
# Usage:
#   bash ledger-query.sh <ledger.jsonl>                    — print stats summary
#   bash ledger-query.sh <ledger.jsonl> --vid <id>         — show history for one vid
#   bash ledger-query.sh <ledger.jsonl> --latest           — show latest verdict per vid

set -euo pipefail

LEDGER="${1:-}"
SUBCOMMAND="${2:-}"

if [ -z "$LEDGER" ] || [ ! -f "$LEDGER" ]; then
  echo "Usage: bash ledger-query.sh <ledger.jsonl> [--vid <id>|--latest]"
  echo ""
  echo "Examples:"
  echo "  bash ledger-query.sh documents/llamacpp.ledger.jsonl"
  echo "  bash ledger-query.sh documents/llamacpp.ledger.jsonl --vid 3a8f2b1c"
  echo "  bash ledger-query.sh documents/llamacpp.ledger.jsonl --latest"
  exit 1
fi

# --- Stats summary ---
stats() {
  local total
  total=$(wc -l < "$LEDGER")

  echo "=== Ledger Stats ==="
  echo "File: $LEDGER"
  echo "Total entries: $total"
  echo ""

  echo "By verdict:"
  grep -o '"verdict":"[^"]*"' "$LEDGER" 2>/dev/null | sort | uniq -c | sort -rn | while read -r count verdict; do
    local clean_count
    clean_count=$(echo "$count" | xargs)
    local clean_verdict
    clean_verdict=$(echo "$verdict" | grep -o '"[^"]*"$' | tr -d '"')
    case "$clean_verdict" in
      CONTRADICTED)       icon="🔴" ;;
      NUANCED)       icon="🟡" ;;
      OUTDATED)      icon="🕐" ;;
      UNVERIFIABLE)  icon="⚪" ;;
      SUPPORTED)     icon="🟢" ;;
      REFUSED)       icon="⛔" ;;
      *)             icon="  " ;;
    esac
    printf "  %s %-14s  %s\n" "$icon" "$clean_verdict" "$clean_count"
  done
  echo ""

  echo "By evidence tier:"
  grep -o '"evidence_tier":"[^"]*"' "$LEDGER" 2>/dev/null | sort | uniq -c | sort -rn | while read -r count tier; do
    printf "  %-5s  %s\n" "$(echo "$count" | xargs)" "$(echo "$tier" | grep -o '"[^"]*"$' | tr -d '"')"
  done
  echo ""

  echo "By severity (latest per vid):"
  # ponytail: use jq for proper JSONL query when needed
  echo "  (requires jq for grouped query)"
}

# --- History for one vid ---
history() {
  local vid="$1"
  echo "=== History for vid=$vid ==="
  grep "\"vid\":\"$vid\"" "$LEDGER" | while read -r line; do
    local verdict timestamp evidence
    verdict=$(echo "$line" | grep -o '"verdict":"[^"]*"' | head -1 | grep -o '"[^"]*"$' | tr -d '"')
    timestamp=$(echo "$line" | grep -o '"timestamp":"[^"]*"' | head -1 | grep -o '"[^"]*"$' | tr -d '"')
    evidence=$(echo "$line" | grep -o '"evidence":"[^"]*"' | head -1 | grep -o '"[^"]*"$' | tr -d '"')
    printf "  %-14s  %s  %s\n" "$verdict" "$timestamp" "$evidence"
  done
}

# --- Latest per vid ---
latest() {
  echo "=== Latest verdict per claim ==="
  # ponytail: use jq for proper grouping when available; grep-based is approximate
  # Groups by vid, takes max timestamp
  local vids
  vids=$(grep -o '"vid":"[^"]*"' "$LEDGER" | sort -u | grep -o '"[^"]*"$' | tr -d '"')
  for vid in $vids; do
    local latest_line
    latest_line=$(grep "\"vid\":\"$vid\"" "$LEDGER" | tail -1)
    local verdict
    verdict=$(echo "$latest_line" | grep -o '"verdict":"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"')
    local claim
    claim=$(echo "$latest_line" | grep -o '"claim_text":"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"')
    printf "  %s  %-14s  %s\n" "$vid" "$verdict" "${claim:0:60}"
  done
}

# --- Dispatch ---
case "$SUBCOMMAND" in
  --vid)
    if [ -z "${3:-}" ]; then
      echo "Error: --vid requires an argument"
      exit 1
    fi
    history "$3"
    ;;
  --latest)
    latest
    ;;
  *)
    stats
    ;;
esac
