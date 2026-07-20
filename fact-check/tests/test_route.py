"""Integration tests for scripts/route-claims.sh.

Seam: bash scripts/route-claims.sh <claims.json> <regex-rules.json> → stdout JSON
  { claims: [...], stats: { authority_hit, judgment_refused, ... } }
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
REFERENCES_DIR = Path(__file__).parent.parent / "references"


def run_route(claims_json: Path) -> tuple[dict, int]:
    args = [
        "bash", str(SCRIPTS_DIR / "route-claims.sh"),
        str(claims_json),
        str(REFERENCES_DIR / "regex-rules.json"),
    ]
    result = subprocess.run(args, capture_output=True, text=True, timeout=10)
    return json.loads(result.stdout), result.returncode


def _write_claims(claims: list[dict], path: Path):
    path.write_text(json.dumps(claims, ensure_ascii=False))


class TestRouteClaims:
    def test_authority_claim_routed_to_rule_engine(self):
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        _write_claims([{
            "claim_id": "C001",
            "claim_text": "arXiv:2605.18071 proposed the method",
            "normalized_claim": "arXiv:2605.18071 exists",
            "type": "authority",
            "expected_verifier": "rule_engine",
        }], claims_file)
        data, code = run_route(claims_file)
        assert code == 0
        claim = data["claims"][0]
        assert claim["route"] == "rule_engine"

    def test_pure_judgment_routed_to_refused(self):
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        _write_claims([{
            "claim_id": "C001",
            "claim_text": "vLLM is better than SGLang",
            "normalized_claim": "vLLM better than SGLang",
            "type": "interpretation",
            "expected_verifier": "refused",
        }], claims_file)
        data, code = run_route(claims_file)
        assert code == 0
        claim = data["claims"][0]
        assert claim["route"] == "refused"

    def test_community_attribution_routed_to_web_search(self):
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        _write_claims([{
            "claim_id": "C001",
            "claim_text": "社区认为 llama.cpp 最活跃",
            "normalized_claim": "community thinks llama.cpp most active",
            "type": "attribution",
            "expected_verifier": "web_search",
        }], claims_file)
        data, code = run_route(claims_file)
        assert code == 0
        claim = data["claims"][0]
        assert claim["route"] == "web_search"

    def test_causal_interpretation_routed_to_inferred(self):
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        _write_claims([{
            "claim_id": "C001",
            "claim_text": "MLA 32x compression makes CPU inference feasible",
            "normalized_claim": "MLA compression enables CPU inference",
            "type": "interpretation",
            "expected_verifier": "inferred",
        }], claims_file)
        data, code = run_route(claims_file)
        assert code == 0
        claim = data["claims"][0]
        assert claim["route"] == "inferred"

    def test_stats_include_all_categories(self):
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        _write_claims([
            {
                "claim_id": "C001",
                "claim_text": "arXiv:2605.18071 proposed the method",
                "normalized_claim": "arXiv:2605.18071 exists",
                "type": "authority",
                "expected_verifier": "rule_engine",
            },
            {
                "claim_id": "C002",
                "claim_text": "vLLM is better than SGLang",
                "normalized_claim": "vLLM better than SGLang",
                "type": "interpretation",
                "expected_verifier": "refused",
            },
            {
                "claim_id": "C003",
                "claim_text": "社区认为 llama.cpp 最活跃",
                "normalized_claim": "community thinks llama.cpp most active",
                "type": "attribution",
                "expected_verifier": "web_search",
            },
        ], claims_file)
        data, code = run_route(claims_file)
        assert code == 0
        assert "stats" in data
        assert data["stats"]["authority_hit"] >= 1
        assert data["stats"]["judgment_refused"] >= 1
        assert "judgment_community" in data["stats"]

    def test_unmatched_claims_use_fallback(self):
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        _write_claims([{
            "claim_id": "C001",
            "claim_text": "Some random factual claim about nothing specific",
            "normalized_claim": "random factual claim nothing specific",
            "type": "factual",
            "expected_verifier": "web_search",
        }], claims_file)
        data, code = run_route(claims_file)
        assert code == 0
        claim = data["claims"][0]
        assert "route" in claim
        assert claim["route"] == "web_search"

    def test_claims_array_preserved(self):
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        _write_claims([
            {"claim_id": "C001", "claim_text": "arXiv:2605.18071", "normalized_claim": "", "type": "authority", "expected_verifier": "rule_engine"},
            {"claim_id": "C002", "claim_text": "vLLM is better", "normalized_claim": "", "type": "interpretation", "expected_verifier": "refused"},
            {"claim_id": "C003", "claim_text": "some fact", "normalized_claim": "", "type": "factual", "expected_verifier": "web_search"},
        ], claims_file)
        data, code = run_route(claims_file)
        assert code == 0
        assert len(data["claims"]) == 3
        for c in data["claims"]:
            assert "route" in c

    def test_empty_claims(self):
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        _write_claims([], claims_file)
        data, code = run_route(claims_file)
        assert code == 0
        assert data["claims"] == []
        assert data["stats"]["authority_hit"] == 0
