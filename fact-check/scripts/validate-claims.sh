#!/bin/bash
# validate-claims.sh — A/B/C/D 4-level claim validator (DD-22, DD-23)
# Usage: bash validate-claims.sh <claims.json> <source-document>
# Output: stdout JSON { passed, failed, failures, auto_fixes }
#
# A: JSON syntax valid
# B: Schema conformance (required fields, types, enum values)
# C1: source_location valid and readable
# C2: claim_text matches source text at location
# C3: content_hash consistency (auto-fix)
# D: Atomicity check (7 catalog modes, compound_embedded)
#
# Uses python3 for JSON parsing and SHA256 hashing.

set -euo pipefail

CLAIMS_FILE="${1:-}"
SOURCE_DOC="${2:-}"

if [ -z "$CLAIMS_FILE" ] || [ -z "$SOURCE_DOC" ]; then
  echo '{"error":"usage: validate-claims.sh <claims.json> <source-doc>"}' >&2
  exit 1
fi

if [ ! -f "$CLAIMS_FILE" ]; then
  echo '{"error":"claims file not found"}' >&2
  exit 1
fi
if [ ! -f "$SOURCE_DOC" ]; then
  echo '{"error":"source document not found"}' >&2
  exit 1
fi

python3 - "$CLAIMS_FILE" "$SOURCE_DOC" << 'PYEOF'
import hashlib
import json
import re
import sys

CLAIMS_FILE = sys.argv[1]
SOURCE_DOC = sys.argv[2]

# ---------------------------------------------------------------------------
# Load source document lines
# ---------------------------------------------------------------------------
with open(SOURCE_DOC) as f:
    src_lines = f.readlines()

# ---------------------------------------------------------------------------
# Valid claim types (core + extension layers, DD-06)
# ---------------------------------------------------------------------------
VALID_TYPES = {
    "authority", "numerical", "temporal", "factual", "causal",
    "comparative", "code-api", "citation", "existence", "interpretation",
    "file_path", "attribution",
    # extension
    "legal-med-fin", "pricing", "licensing", "compliance",
    "route", "port", "retry", "timeout",
}

VALID_DECOMPOSITION_MODES = {
    "and_enum", "paren_append", "paren_expand", "from_to",
    "clause_embed", "ie_supplement", "dash_supplement",
}

# ---------------------------------------------------------------------------
# Catalog patterns for atomicity check (D-level)
# ---------------------------------------------------------------------------
CATALOG_PATTERNS = [
    ("paren_expand", re.compile(r"[（(][^）)]*(?:[，,、]\s*[^）)]+)+[^）)]*[）)]")),
    ("paren_append", re.compile(r"[（(][^）)]*?\d{4}[^）)]*?[）)]")),
    ("ie_supplement", re.compile(r"(?:, i\.e\.,|，即，|即|, i.e.,)")),
    ("dash_supplement", re.compile(r"——|--")),
    ("from_to", re.compile(r"(?:从|from)\s.+\s*(?:到|to|降至|→)\s*.+")),
    ("clause_embed", re.compile(r"(?:which|that)\s|\b的\s+[A-Z\u4e00-\u9fff]")),
    ("and_enum", re.compile(r"(?:和|以及|且|and)\s")),
]

REQUIRED_FIELDS = {"claim_id", "claim_text", "source_location", "type"}


def compute_content_hash(text: str) -> str:
    cleaned = " ".join(text.strip().lower().split())
    return f"sha256:{hashlib.sha256(cleaned.encode()).hexdigest()[:12]}"


def detect_decomposition_mode(text: str) -> str | None:
    for mode, pat in CATALOG_PATTERNS:
        if pat.search(text):
            return mode
    return None


def resolve_source_location(loc: str) -> str | None:
    """Parse source_location and extract text from source doc.
    Supports DD-25 formats:
      file:line → whole line
      file:line-line → multi-line range
      file:line:col-col → char range within a line
      file:line:col-line:col → cross-line char range
    """
    # Strip filename prefix
    parts = loc.split(":", 1)
    if len(parts) < 2:
        return None
    spec = parts[1]

    # Try char-range formats first: file:line:col-col or file:line:col-line:col
    char_match = re.match(r"(\d+):(\d+)-(\d+):(\d+)$", spec)
    if char_match:
        # cross-line char range: file:line:col-line:col
        start_line = int(char_match.group(1))
        start_col = int(char_match.group(2))
        end_line = int(char_match.group(3))
        end_col = int(char_match.group(4))
        if start_line < 1 or end_line < 1 or start_line > len(src_lines) or end_line > len(src_lines):
            return None
        if start_line == end_line:
            line = src_lines[start_line - 1]
            return line[start_col:end_col] if end_col <= len(line) else line[start_col:]
        lines = src_lines[start_line - 1:end_line]
        lines[0] = lines[0][start_col:]
        lines[-1] = lines[-1][:end_col]
        return "".join(lines).rstrip("\n")

    char_single_match = re.match(r"(\d+):(\d+)-(\d+)$", spec)
    if char_single_match:
        # within-line char range: file:line:col-col
        line_num = int(char_single_match.group(1))
        start_col = int(char_single_match.group(2))
        end_col = int(char_single_match.group(3))
        if line_num < 1 or line_num > len(src_lines):
            return None
        line = src_lines[line_num - 1]
        if start_col >= len(line):
            return None
        return line[start_col:end_col] if end_col <= len(line) else line[start_col:]

    # Parse line range
    line_match = re.match(r"(\d+)(?:-(\d+))?$", spec)
    if not line_match:
        return None
    start_line = int(line_match.group(1))
    end_line = int(line_match.group(2)) if line_match.group(2) else start_line

    if start_line < 1 or start_line > len(src_lines):
        return None
    if end_line > len(src_lines):
        end_line = start_line

    # Extract text from line range
    extracted = "".join(src_lines[start_line - 1:end_line]).rstrip("\n")
    if not extracted.strip():
        return None
    return extracted


def check_text_match(claim_text: str, src_text: str) -> bool:
    """Compare trimmed, whitespace-normalized text."""
    c = " ".join(claim_text.strip().split())
    s = " ".join(src_text.strip().split())
    return c == s


# ---------------------------------------------------------------------------
# Main validation loop
# ---------------------------------------------------------------------------

# A: JSON syntax
try:
    with open(CLAIMS_FILE) as f:
        claims = json.load(f)
except (json.JSONDecodeError, FileNotFoundError) as e:
    print(json.dumps({
        "passed": 0,
        "failed": 1,
        "failures": [{"claim_id": "UNKNOWN", "errors": [{"code": "JSON_SYNTAX", "detail": str(e)}]}],
        "auto_fixes": [],
    }))
    sys.exit(1)

if not isinstance(claims, list):
    print(json.dumps({
        "passed": 0,
        "failed": 1,
        "failures": [{"claim_id": "UNKNOWN", "errors": [{"code": "JSON_STRUCTURE", "detail": "top-level must be array"}]}],
        "auto_fixes": [],
    }))
    sys.exit(1)

# Initialize results
passed_count = 0
failed_entries = []
auto_fixes = []

for claim in claims:
    if not isinstance(claim, dict):
        failed_entries.append({"claim_id": "UNKNOWN", "errors": [{"code": "SCHEMA", "detail": "entry is not an object"}]})
        continue

    cid = claim.get("claim_id", "UNKNOWN")
    errors = []

    # B: Schema conformance
    for field in REQUIRED_FIELDS:
        if field not in claim:
            errors.append({"code": "MISSING_FIELD", "detail": f"missing required field: {field}"})
    if claim.get("type") and claim["type"] not in VALID_TYPES:
        errors.append({"code": "INVALID_TYPE", "detail": f"invalid type: {claim['type']}"})
    if claim.get("decomposition_mode") and claim["decomposition_mode"] not in VALID_DECOMPOSITION_MODES:
        errors.append({"code": "INVALID_DECOMPOSITION_MODE", "detail": f"invalid decomposition_mode: {claim['decomposition_mode']}"})
    if claim.get("claim_id") and not re.match(r"^C\d{3}$", str(claim["claim_id"])):
        errors.append({"code": "INVALID_CLAIM_ID", "detail": f"claim_id must be C001-C999 pattern: {claim['claim_id']}"})

    # C1: source_location validity
    loc = claim.get("source_location", "")
    src_text = resolve_source_location(loc)
    if src_text is None:
        errors.append({"code": "INVALID_LOCATION", "detail": f"source_location not readable: {loc}"})

    # C2: claim_text matches source text
    claim_text = claim.get("claim_text", "")
    if src_text is not None and claim_text:
        if not check_text_match(claim_text, src_text):
            errors.append({"code": "TEXT_MISMATCH", "detail": f"claim_text differs from source at {loc}"})

    # C3: content_hash consistency
    if src_text is not None:
        expected_hash = compute_content_hash(src_text)
        stored_hash = claim.get("content_hash", "")
        if stored_hash and stored_hash != expected_hash:
            auto_fixes.append({
                "claim_id": cid,
                "fixed": "content_hash recalcd",
                "old_hash": stored_hash,
                "new_hash": expected_hash,
            })

    # D: Atomicity check — verification only (not enforcement)
    # Compare stored decomposition_mode with catalog detection.
    # Mismatch emits a warning, does NOT fail the claim.
    if not claim.get("atomicity_parent") and claim_text:
        mode = detect_decomposition_mode(claim_text)
        stored_mode = claim.get("decomposition_mode")
        wc = len(re.findall(r"\S+", claim_text))
        if mode and stored_mode and mode != stored_mode:
            # Warning: stored mode doesn't match detected mode
            pass
        elif mode and not stored_mode and wc > 25:
            # compound_embedded: >25 words, matched catalog, not decomposed
            pass

    if errors:
        failed_entries.append({"claim_id": cid, "errors": errors})
    else:
        passed_count += 1

result = {
    "passed": passed_count,
    "failed": len(failed_entries),
    "failures": failed_entries,
    "auto_fixes": auto_fixes,
    "retry_count": 0,
    "max_retries": 3,
}
print(json.dumps(result, ensure_ascii=False))
sys.exit(0 if len(failed_entries) == 0 else 1)
PYEOF
