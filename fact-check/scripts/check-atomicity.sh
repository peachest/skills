#!/bin/bash
# check-atomicity.sh — Catalog pattern matcher for claim decomposition (DD-34, R23)
# Usage: bash check-atomicity.sh "<claim_text>"
# Output: stdout JSON { match, pattern, sub_items, word_count }
#
# 7 fixed catalog patterns, first-match-wins priority.
# Phase 1 immediate feedback — agent uses sub_items to generate child claims.

set -euo pipefail

CLAIM_TEXT="${1:-}"

if [ -z "$CLAIM_TEXT" ]; then
  echo '{"error":"usage: check-atomicity.sh \"<claim_text>\""}' >&2
  exit 1
fi

exec python3 - "$CLAIM_TEXT" << 'PYEOF'
import json, re, sys

text = sys.argv[1]

# 7 catalog patterns in priority order
PATTERNS = [
    ("paren_expand", re.compile(r"[（(][^）)]*(?:[，,、]\s*[^）)]+)+[^）)]*[）)]")),
    ("paren_append", re.compile(r"[（(][^）)]*?\d{4}[^）)]*?[）)]")),
    ("ie_supplement", re.compile(r"(?:, i\.e\.,|，即，|即|, i.e.,)")),
    ("dash_supplement", re.compile(r"——|--")),
    ("from_to", re.compile(r"(?:从|from)\s.+\s*(?:到|to|降至|→)\s*.+")),
    ("clause_embed", re.compile(r"(?:which|that)\s|\b的\s+[A-Z\u4e00-\u9fff]")),
    ("and_enum", re.compile(r"(?:和|以及|且|and)\s")),
]

word_count = len(re.findall(r"\S+", text))

# Try each pattern
for pattern_name, pat in PATTERNS:
    m = pat.search(text)
    if m:
        # Extract sub-items based on pattern type
        sub_items = []
        if pattern_name == "and_enum":
            # Split on connectors
            parts = re.split(r"(?:和|以及|且|and)\s", text)
            sub_items = [p.strip() for p in parts if p.strip()]
        elif pattern_name == "paren_expand":
            # Extract comma-separated items inside parens
            paren_match = re.search(r"[（(]([^）)]+)[）)]", text)
            if paren_match:
                inner = paren_match.group(1)
                sub_items = [s.strip() for s in re.split(r"[，,、]", inner) if s.strip()]
        elif pattern_name == "paren_append":
            paren_match = re.search(r"[（(]([^）)]*?\d{4}[^）)]*?)[）)]", text)
            if paren_match:
                main = re.sub(r"[（(][^）)]*[）)]", "", text).strip()
                sub_items = [main, paren_match.group(1).strip()]
        elif pattern_name == "from_to":
            m2 = re.search(r"(?:从|from)\s(.+)\s*(?:到|to|降至|→)\s*(.+)", text)
            if m2:
                sub_items = [f"{m2.group(1).strip()} (before)", f"{m2.group(2).strip()} (after)"]
        elif pattern_name == "ie_supplement":
            parts = re.split(r"(?:, i\.e\.,|，即，|即|, i.e.,)", text, maxsplit=1)
            sub_items = [p.strip() for p in parts if p.strip()]
        elif pattern_name == "dash_supplement":
            parts = re.split(r"——|--", text)
            sub_items = [p.strip() for p in parts if p.strip()]
        elif pattern_name == "clause_embed":
            # Split at relative clause marker
            m2 = re.search(r"\b(which|that)\s", text)
            if m2:
                idx = m2.start()
                before = text[:idx].strip().rstrip(",").strip()
                after = text[idx:].strip()
                sub_items = [before, after]

        print(json.dumps({
            "match": True,
            "pattern": pattern_name,
            "sub_items": sub_items,
            "word_count": word_count,
        }, ensure_ascii=False))
        sys.exit(0)

# No catalog match
print(json.dumps({
    "match": False,
    "pattern": "none",
    "sub_items": [],
    "word_count": word_count,
}, ensure_ascii=False))
PYEOF
