#!/bin/bash
# incremental-diff.sh — Phase 0 incremental: git diff hunk → carry forward / re-extract (DD-26)
# Usage: bash incremental-diff.sh <old-claims.json> <old-doc> <new-doc>
# Reads git diff --unified=0, matches source_location lines against hunks.
# Output: stdout JSON { carried_forward: [...], re_extract_queue: [...] }

set -euo pipefail

OLD_CLAIMS="${1:-}"
OLD_DOC="${2:-}"
NEW_DOC="${3:-}"

if [ -z "$OLD_CLAIMS" ] || [ -z "$OLD_DOC" ] || [ -z "$NEW_DOC" ]; then
  echo '{"error":"usage: incremental-diff.sh <old-claims.json> <old-doc> <new-doc>"}' >&2
  exit 1
fi

exec python3 - "$OLD_CLAIMS" "$OLD_DOC" "$NEW_DOC" << 'PYEOF'
import hashlib, json, re, subprocess, sys

old_claims_file, old_doc, new_doc = sys.argv[1], sys.argv[2], sys.argv[3]

with open(old_claims_file) as f:
    old_claims = json.load(f)

# Run git diff --unified=0
result = subprocess.run(
    ["git", "diff", "--unified=0", old_doc, new_doc],
    capture_output=True, text=True,
)
diff_output = result.stdout

# Parse hunks: @@ -old_start,old_count +new_start,new_count @@
hunk_pattern = re.compile(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@')
hunks = []
for m in hunk_pattern.finditer(diff_output):
    old_start = int(m.group(1))
    old_count = int(m.group(2)) if m.group(2) else 1
    hunks.append((old_start, old_start + old_count - 1))

def line_in_hunks(line_num):
    for start, end in hunks:
        if start <= line_num <= end:
            return True
    return False

def compute_hash(text):
    cleaned = " ".join(text.strip().lower().split())
    return f"sha256:{hashlib.sha256(cleaned.encode()).hexdigest()[:12]}"

# Read new doc for hash verification
with open(new_doc) as f:
    new_lines = f.readlines()

carried_forward = []
re_extract = []

for claim in old_claims:
    loc = claim.get("source_location", "")
    # Extract line number from source_location
    line_match = re.search(r':(\d+)', loc)
    if not line_match:
        re_extract.append(claim)
        continue

    line_num = int(line_match.group(1))

    if not line_in_hunks(line_num):
        # Carry forward: verify hash
        old_hash = claim.get("content_hash", "")
        if 1 <= line_num <= len(new_lines):
            src_text = new_lines[line_num - 1].rstrip("\n")
            new_hash = compute_hash(src_text)
            # For single-line docs with char ranges, check if the text is still present
            if old_hash and new_hash:
                # Hash of full line may differ from hash of substring
                # Use text presence check instead
                claim_text = claim.get("claim_text", "")
                if claim_text in src_text:
                    carried_forward.append(claim)
                else:
                    re_extract.append(claim)
            else:
                carried_forward.append(claim)
        else:
            re_extract.append(claim)
    else:
        re_extract.append(claim)

print(json.dumps({
    "carried_forward": len(carried_forward),
    "re_extract": len(re_extract),
    "carried_claims": carried_forward,
    "re_extract_claims": re_extract,
    "hunks": len(hunks),
}, ensure_ascii=False))
PYEOF
