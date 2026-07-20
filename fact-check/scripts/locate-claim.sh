#!/bin/bash
# locate-claim.sh — Deterministic claim text locator (DD-33, R22)
# Usage: bash locate-claim.sh "<claim_text>" <doc_path>
# Output: stdout JSON { ok: true, location, hash } | { error, closest_match }
#
# Edit-style exact substring match (not line-by-line grep).
# Multi-line text scanning, O(n) single pass, <1ms for ~80KB docs.

set -euo pipefail

CLAIM_TEXT="${1:-}"
DOC_PATH="${2:-}"

if [ -z "$CLAIM_TEXT" ] || [ -z "$DOC_PATH" ] || [ ! -f "$DOC_PATH" ]; then
  echo '{"error":"usage: locate-claim.sh \"<claim_text>\" <doc_path>"}' >&2
  exit 1
fi

exec python3 - "$CLAIM_TEXT" "$DOC_PATH" << 'PYEOF'
import hashlib, json, re, sys

claim_text, doc_path = sys.argv[1], sys.argv[2]

with open(doc_path) as f:
    doc_content = f.read()

def compute_hash(text):
    cleaned = " ".join(text.strip().lower().split())
    return f"sha256:{hashlib.sha256(cleaned.encode()).hexdigest()[:12]}"

def char_to_location(char_idx):
    """Convert 0-based char index to DD-25 source_location."""
    prefix = doc_content[:char_idx]
    line_num = prefix.count("\n") + 1
    last_nl = prefix.rfind("\n")
    col = char_idx - (last_nl + 1) if last_nl >= 0 else char_idx
    end_idx = char_idx + len(claim_text)
    end_prefix = doc_content[:end_idx]
    end_line_num = end_prefix.count("\n") + 1
    end_last_nl = end_prefix.rfind("\n")
    end_col = end_idx - (end_last_nl + 1) if end_last_nl >= 0 else end_idx

    if line_num == end_line_num:
        return f"{doc_path}:{line_num}:{col}-{end_col}"
    else:
        return f"{doc_path}:{line_num}:{col}-{end_line_num}:{end_col}"

# Exact substring match
idx = doc_content.find(claim_text)

if idx != -1:
    # Check for ambiguous matches (same text at multiple positions)
    second = doc_content.find(claim_text, idx + 1)
    if second != -1 and len(claim_text) <= 20:
        # Short claim with duplicate — ambiguous
        candidates = []
        pos = 0
        while True:
            pos = doc_content.find(claim_text, pos)
            if pos == -1:
                break
            prefix = doc_content[max(0, pos - 40):pos].replace("\n", " ")
            candidates.append({"location": char_to_location(pos), "prefix": f"...{prefix}"})
            pos += 1
        print(json.dumps({"error": "AMBIGUOUS", "candidates": candidates}, ensure_ascii=False))
        sys.exit(1)

    location = char_to_location(idx)
    h = compute_hash(claim_text)
    print(json.dumps({"ok": True, "location": location, "hash": h}, ensure_ascii=False))
else:
    # Try normalized match (collapse whitespace)
    normalized_claim = " ".join(re.split(r"\s+", claim_text.strip()))
    normalized_doc = " ".join(re.split(r"\s+", doc_content))

    norm_idx = normalized_doc.find(normalized_claim)
    if norm_idx != -1:
        # Map back to original doc — find the nearest whitespace boundary
        # Simple approach: use the normalized position to estimate
        accumulated = 0
        real_idx = 0
        for i, ch in enumerate(doc_content):
            if not ch.isspace() or (i > 0 and not doc_content[i-1].isspace()):
                if accumulated == norm_idx:
                    real_idx = i
                    break
                accumulated += 1

        # Extract the actual text at this position
        # Use character-based slice
        end_real = real_idx + len(claim_text)
        location = char_to_location(real_idx)
        h = compute_hash(doc_content[real_idx:end_real])
        print(json.dumps({"ok": True, "location": location, "hash": h}, ensure_ascii=False))
    else:
        # Find closest match by prefix overlap
        prefix_len = min(80, len(claim_text))
        prefix = claim_text[:prefix_len]
        closest_idx = doc_content.find(prefix)
        if closest_idx == -1:
            # Try first 40 chars
            prefix = claim_text[:40]
            closest_idx = doc_content.find(prefix)

        closest_match = ""
        if closest_idx != -1:
            snippet_start = max(0, closest_idx)
            snippet_end = min(len(doc_content), closest_idx + len(claim_text) + 40)
            closest_match = doc_content[snippet_start:snippet_end].replace("\n", " ")[:120]

        print(json.dumps({
            "error": "TEXT_NOT_FOUND",
            "closest_match": closest_match,
        }, ensure_ascii=False))
        sys.exit(1)
PYEOF
