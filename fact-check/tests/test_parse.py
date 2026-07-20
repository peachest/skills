"""Tests for [CLAIM] block parser — used by rule-engine.sh to ingest LLM output.

The parser reads the LLM's markdown output and extracts structured claim
objects from [CLAIM]...[/CLAIM] blocks.  This is the first step of Phase 3a
and MUST be deterministic.

Reference: fact-checker/test_parse_claims.py (machug/fact-checker)
"""

import re

CLAIM_BLOCK_RE = re.compile(
    r"\[CLAIM\]\s*\n(.*?)\[/CLAIM\]", re.DOTALL
)


def parse_claims_output(text: str) -> list[dict[str, str | None]]:
    """Parse LLM output text containing [CLAIM] blocks into dicts."""
    claims: list[dict[str, str | None]] = []
    for match in CLAIM_BLOCK_RE.finditer(text):
        block = match.group(1)
        claim: dict[str, str | None] = {}
        for line in block.strip().split("\n"):
            if ":" not in line:
                continue
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip() or None
            if key and val:
                claim[key] = val
        if "id" in claim and "text" in claim:
            claims.append(claim)
    return claims


class TestParseClaimsOutput:
    """Mirrors fact-checker's test_parse_claims.py test structure."""

    def test_basic_extraction(self, sample_claims_output):
        claims = parse_claims_output(sample_claims_output)
        assert len(claims) == 2
        assert claims[0]["id"] == "1"
        assert claims[0]["text"] == "Azure Sentinel costs $2.46/GB"
        assert claims[0]["category"] == "pricing"
        assert claims[0]["section"] == "Pricing"

    def test_empty_input(self):
        assert parse_claims_output("") == []

    def test_no_claim_blocks(self):
        assert parse_claims_output("Some text with no claims at all.") == []

    def test_missing_id_skipped(self):
        text = "[CLAIM]\ntext: A claim without an ID\ncategory: pricing\n[/CLAIM]"
        assert parse_claims_output(text) == []

    def test_missing_text_skipped(self):
        text = "[CLAIM]\nid: 1\ncategory: pricing\n[/CLAIM]"
        assert parse_claims_output(text) == []

    def test_minimal_valid_claim(self):
        text = "[CLAIM]\nid: 99\ntext: Something factual\n[/CLAIM]"
        claims = parse_claims_output(text)
        assert len(claims) == 1
        assert claims[0]["id"] == "99"
        assert claims[0]["text"] == "Something factual"
        assert "category" not in claims[0]

    def test_extra_whitespace_and_blank_lines(self):
        text = (
            "[CLAIM]\n"
            "  id:   42  \n"
            "  text:   Padded claim   \n"
            "  category:  pricing  \n"
            "\n"
            "[/CLAIM]"
        )
        claims = parse_claims_output(text)
        assert len(claims) == 1
        assert claims[0]["id"] == "42"
        assert claims[0]["text"] == "Padded claim"

    def test_multiple_claims_interleaved_with_prose(self):
        text = (
            "Here are the claims:\n\n"
            "[CLAIM]\nid: 1\ntext: First\n[/CLAIM]\n"
            "Some commentary between claims.\n"
            "[CLAIM]\nid: 2\ntext: Second\n[/CLAIM]\n"
            "Final remarks.\n"
        )
        claims = parse_claims_output(text)
        assert len(claims) == 2
        assert claims[0]["text"] == "First"
        assert claims[1]["text"] == "Second"

    def test_claim_with_colon_in_text(self):
        text = "[CLAIM]\nid: 1\ntext: Price: $99/user/month for E5\n[/CLAIM]"
        claims = parse_claims_output(text)
        assert claims[0]["text"] == "Price: $99/user/month for E5"


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


import pytest


@pytest.fixture
def sample_claims_output():
    return (
        "Here are the extracted claims:\n\n"
        "[CLAIM]\n"
        "id: 1\n"
        "text: Azure Sentinel costs $2.46/GB\n"
        "category: pricing\n"
        "section: Pricing\n"
        "[/CLAIM]\n\n"
        "[CLAIM]\n"
        "id: 2\n"
        "text: Entra ID supports FIDO2 keys\n"
        "category: capability\n"
        "section: Auth\n"
        "[/CLAIM]\n"
    )
