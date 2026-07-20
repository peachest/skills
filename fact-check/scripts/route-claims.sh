#!/bin/bash
# route-claims.sh — Phase 2 deterministic regex routing (DD-06, run-output.md)
# Usage: bash route-claims.sh <claims.json> <regex-rules.json>
# Output: stdout JSON { claims: [...], stats: {...} }
#
# Dual-field matching: claim_text + normalized_claim against 30 rules
# Priority: authority (25) → judgment (3) → interpretation (2) → fallback
# First-match-wins. Unmatched → LLM expected_verifier fallback.

set -euo pipefail

CLAIMS_FILE="${1:-}"
RULES_FILE="${2:-}"

if [ -z "$CLAIMS_FILE" ] || [ -z "$RULES_FILE" ]; then
  echo '{"error":"usage: route-claims.sh <claims.json> <regex-rules.json>"}' >&2
  exit 1
fi

python3 - "$CLAIMS_FILE" "$RULES_FILE" << 'PYEOF'
import json
import re
import sys

CLAIMS_FILE = sys.argv[1]
RULES_FILE = sys.argv[2]

with open(RULES_FILE) as f:
    rules = json.load(f)
with open(CLAIMS_FILE) as f:
    claims = json.load(f)

authority_rules = rules.get("authority_rules", [])
judgment_rules = rules.get("judgment_rules", [])
interpretation_rules = rules.get("interpretation_rules", [])

# Stats
stats = {
    "authority_hit": 0,
    "judgment_refused": 0,
    "judgment_community": 0,
    "judgment_hedging": 0,
    "interpretation": 0,
    "unmatched": 0,
}


def match_authority(text: str) -> dict | None:
    """Try all 25 authority rules against text. First match wins."""
    for rule in authority_rules:
        pat = rule.get("pattern", "")
        try:
            m = re.search(pat, text)
        except re.error:
            continue
        if m:
            # Determine verifier key from rule
            verifier = rule.get("verifier", "rule_engine")
            return {
                "route": "rule_engine",
                "matched_verifier": verifier,
                "matched_rule": rule.get("name", "unknown"),
            }
    return None


def match_judgment(text: str) -> dict | None:
    """Try judgment rules against text."""
    for rule in judgment_rules:
        for pat in rule.get("patterns", []):
            try:
                if re.search(pat, text):
                    continue
            except re.error:
                continue
        else:
            # Re-scan to find which pattern matched and get verdict
            for pat in rule.get("patterns", []):
                try:
                    if re.search(pat, text):
                        verdict = rule.get("verdict", "REFUSED")
                        name = rule.get("name", "")
                        route = "web_search" if verdict == "web_search" else "refused"
                        return {
                            "route": route,
                            "matched_verifier": route,
                            "matched_rule": name,
                            "verdict": verdict if route == "refused" else None,
                        }
                except re.error:
                    continue
    return None


def _judgment_matches(rule: dict, text: str) -> bool:
    """Check if any pattern in a judgment rule matches text."""
    for pat in rule.get("patterns", []):
        try:
            if re.search(pat, text):
                return True
        except re.error:
            continue
    return False


def match_judgment(text: str) -> dict | None:
    """Try judgment rules in order. First match wins."""
    for rule in judgment_rules:
        if _judgment_matches(rule, text):
            verdict = rule.get("verdict", "REFUSED")
            name = rule.get("name", "")
            if verdict == "REFUSED":
                return {
                    "route": "refused",
                    "matched_verifier": "refused",
                    "matched_rule": name,
                    "verdict": "REFUSED",
                }
            elif name == "opinion_attribution":
                return {
                    "route": "web_search",
                    "matched_verifier": "web_search",
                    "matched_rule": name,
                    "verdict": None,
                }
            elif name == "hedging_factual":
                return {
                    "route": "web_search",
                    "matched_verifier": "web_search",
                    "matched_rule": name,
                    "verdict": None,
                }
            elif name == "opinion_vague":
                return {
                    "route": "refused",
                    "matched_verifier": "refused",
                    "matched_rule": name,
                    "verdict": "REFUSED",
                }
    return None


def match_interpretation(text: str) -> dict | None:
    """Try interpretation rules against text."""
    for rule in interpretation_rules:
        for pat in rule.get("patterns", []):
            try:
                if re.search(pat, text):
                    return {
                        "route": "inferred",
                        "matched_verifier": "inferred",
                        "matched_rule": rule.get("name", ""),
                        "verdict": "INFERRED",
                    }
            except re.error:
                continue
    return None


def _has_repo_context(text):
    """Check if text contains GitHub/GitLab repo context (owner/repo)."""
    import re as _re
    return bool(_re.search(r'(?:github|gitlab|gitee)\.com/[\w.-]+/[\w.-]+', text)) or \
           bool(_re.search(r'\b[\w.-]+/[\w.-]+\b', text))


# Route each claim
for claim in claims:
    claim_text = claim.get("claim_text", "")
    normalized = claim.get("normalized_claim", "")
    # Test both fields, normalized first (it's cleaner)
    search_texts = [normalized, claim_text]

    routed = None
    for text in search_texts:
        if not text:
            continue
        # Try authority first (highest priority)
        routed = match_authority(text)
        if routed:
            break
        # Then judgment
        routed = match_judgment(text)
        if routed:
            break
        # Then interpretation
        routed = match_interpretation(text)
        if routed:
            break

    if routed:
        # DD-29 guard: bare PR/Issue without repo context → re-route to web_search
        no_context_rules = {"github_pr_symbol", "github_issue", "code_platform_symbol_pr"}
        if routed.get("matched_rule") in no_context_rules:
            if not _has_repo_context(text):
                routed = {
                    "route": "web_search",
                    "matched_verifier": "web_search",
                    "matched_rule": routed["matched_rule"] + "_nocxt",
                }

        claim["route"] = routed["route"]
        claim["matched_verifier"] = routed["matched_verifier"]
        claim["matched_rule"] = routed["matched_rule"]
        if routed.get("verdict"):
            claim["verdict"] = routed["verdict"]

        # Update stats
        if routed["route"] == "rule_engine":
            stats["authority_hit"] += 1
        elif routed["route"] == "refused":
            stats["judgment_refused"] += 1
        elif routed["route"] == "inferred":
            stats["interpretation"] += 1
        elif routed["route"] == "web_search":
            rule_name = routed.get("matched_rule", "")
            if rule_name == "opinion_attribution":
                stats["judgment_community"] += 1
            elif rule_name == "hedging_factual":
                stats["judgment_hedging"] += 1
            else:
                stats["judgment_hedging"] += 1
    else:
        # LLM fallback: use expected_verifier from Phase 1
        expected = claim.get("expected_verifier", "web_search")
        if expected == "rule_engine":
            claim["route"] = "rule_engine"
            claim["matched_verifier"] = "rule_engine"
            claim["matched_rule"] = "llm_fallback"
            stats["authority_hit"] += 1
        elif expected == "refused":
            claim["route"] = "refused"
            claim["matched_verifier"] = "refused"
            claim["matched_rule"] = "llm_fallback"
            claim["verdict"] = "REFUSED"
            stats["judgment_refused"] += 1
        elif expected == "inferred":
            claim["route"] = "inferred"
            claim["matched_verifier"] = "inferred"
            claim["matched_rule"] = "llm_fallback"
            claim["verdict"] = "INFERRED"
            stats["interpretation"] += 1
        else:
            claim["route"] = "web_search"
            claim["matched_verifier"] = "web_search"
            claim["matched_rule"] = "llm_fallback"
            stats["unmatched"] += 1

result = {"claims": claims, "stats": stats}
print(json.dumps(result, ensure_ascii=False))
PYEOF
