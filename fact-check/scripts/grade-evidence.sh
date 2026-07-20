#!/bin/bash
# grade-evidence.sh — Evidence grading: tier classification + cross-validation + staleness (DD-04)
# Usage: echo '{"claim_id":"C001","evidence_url":"...","evidence_text":"..."}' | bash grade-evidence.sh
# Or:     bash grade-evidence.sh < verify-batch.json  (reads JSON array from stdin)
# Output: stdout JSON with added evidence_tier, confidence, staleness_warning

set -euo pipefail

# Save stdin to a temp file, pass path to python
INPUT_TMP=$(mktemp)
cat > "$INPUT_TMP"

exec python3 - "$INPUT_TMP" << 'PYEOF'
import json, re, sys
from datetime import datetime, timedelta, timezone

# Tier classification by domain pattern
TIER_PATTERNS = {
    "T1": [
        r"github\.com", r"gitlab\.com", r"gitee\.com",
        r"arxiv\.org", r"doi\.org",
        r"docs\.", r"readthedocs\.io", r"\.dev/docs",
        r"huggingface\.co",
        r"pubmed\.ncbi\.nlm\.nih\.gov",
        r"rfc-editor\.org", r"datatracker\.ietf\.org",
        r"patents\.google\.com",
        r"spdx\.org/licenses",
        r"pypi\.org", r"npmjs\.com", r"crates\.io",
        r"pkg\.go\.dev", r"nuget\.org",
        r"hub\.docker\.com",
    ],
    "T2": [
        r"blog\.", r"medium\.com", r"dev\.to",
        r"readme", r"README",
    ],
    "T3": [
        r"reddit\.com", r"news\.ycombinator\.com",
        r"v2ex\.com", r"zhihu\.com",
        r"github\.com/.*/discussions",
        r"twitter\.com", r"x\.com",
    ],
}

def classify_tier(url):
    if not url:
        return "T4"
    for tier, patterns in TIER_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, url, re.IGNORECASE):
                return tier
    return "T4"

def is_stale(evidence_date_str):
    if not evidence_date_str:
        return False
    try:
        # Parse ISO date or simple date
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"):
            try:
                dt = datetime.strptime(evidence_date_str, fmt).replace(tzinfo=timezone.utc)
                break
            except ValueError:
                continue
        else:
            return False
        age = datetime.now(timezone.utc) - dt
        return age > timedelta(days=180)  # 6 months
    except:
        return False

# Read input from temp file arg
input_file = sys.argv[1]
with open(input_file) as f:
    raw = f.read()
if not raw.strip():
    print(json.dumps({"error": "no input"}))
    sys.exit(1)

try:
    data = json.loads(raw)
except json.JSONDecodeError:
    print(json.dumps({"error": "invalid JSON"}))
    sys.exit(1)

# Support both single object and array
if isinstance(data, dict):
    items = [data]
else:
    items = data

for item in items:
    url = item.get("evidence_url", "")
    item["evidence_tier"] = classify_tier(url)
    item["staleness_warning"] = is_stale(item.get("evidence_date", ""))
    item["confidence"] = "medium"  # default, caller can override

# Cross-validation: if multiple items with same claim_id, check consistency
by_cid = {}
for item in items:
    cid = item.get("claim_id", "")
    by_cid.setdefault(cid, []).append(item)

for cid, group in by_cid.items():
    if len(group) >= 2:
        verdicts = {g.get("verdict") for g in group}
        if len(verdicts) == 1:
            for g in group:
                g["confidence"] = "high"
        else:
            for g in group:
                g["confidence"] = "low"

if isinstance(data, dict):
    print(json.dumps(items[0], ensure_ascii=False))
else:
    print(json.dumps(items, ensure_ascii=False))
PYEOF
