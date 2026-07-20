"""Shared fixtures for fact-check test suite."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"
GOLDEN_DIR = Path(__file__).parent / "golden"
REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
REFERENCES_DIR = REPO_ROOT / "references"


def _load_json(path: Path) -> dict | list:
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# regex-rules.json
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def regex_rules() -> dict:
    return _load_json(REFERENCES_DIR / "regex-rules.json")


# ---------------------------------------------------------------------------
# Golden fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def golden_auth() -> list[dict]:
    return _load_json(GOLDEN_DIR / "synth-auth.golden.json")


@pytest.fixture
def golden_bench() -> list[dict]:
    return _load_json(GOLDEN_DIR / "synth-bench.golden.json")


@pytest.fixture
def golden_decomp() -> list[dict]:
    return _load_json(GOLDEN_DIR / "synth-decomp.golden.json")


@pytest.fixture
def golden_judgment() -> list[dict]:
    return _load_json(GOLDEN_DIR / "synth-judgment.golden.json")


@pytest.fixture
def golden_inference() -> list[dict]:
    return _load_json(GOLDEN_DIR / "synth-inference.golden.json")


@pytest.fixture
def golden_patent() -> list[dict]:
    return _load_json(GOLDEN_DIR / "synth-patent.golden.json")


@pytest.fixture
def golden_package() -> list[dict]:
    return _load_json(GOLDEN_DIR / "synth-package.golden.json")


@pytest.fixture
def golden_extension() -> list[dict]:
    return _load_json(GOLDEN_DIR / "synth-extension.golden.json")


# ---------------------------------------------------------------------------
# Sample claims
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_claims() -> list[dict]:
    return [
        {
            "claim_id": "C001",
            "claim_text": "DeepSeek V3.1 was released in September 2025",
            "normalized_claim": "DeepSeek V3.1 release date September 2025",
            "source_location": "report.md:42",
            "content_hash": "sha256:7d1e9f3a2b4c",
            "type": "temporal",
            "expected_verifier": "web_search",
            "atomicity_parent": None,
            "decomposition_mode": None,
            "compound_flag": None,
        },
        {
            "claim_id": "C002",
            "claim_text": "arXiv:2605.18071 proposed the method",
            "normalized_claim": "arXiv:2605.18071 exists",
            "source_location": "report.md:44",
            "content_hash": "sha256:a1b2c3d4e5f6",
            "type": "authority",
            "expected_verifier": "rule_engine",
            "atomicity_parent": None,
            "decomposition_mode": None,
            "compound_flag": None,
        },
        {
            "claim_id": "C003",
            "claim_text": "vLLM is better than SGLang",
            "normalized_claim": "vLLM better than SGLang",
            "source_location": "report.md:46",
            "content_hash": "sha256:112233445566",
            "type": "interpretation",
            "expected_verifier": "refused",
            "atomicity_parent": None,
            "decomposition_mode": None,
            "compound_flag": None,
        },
    ]

