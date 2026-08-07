"""Tests for JSON schema validation (4-Level Validator: A+B+C+D).

Validates claims.json against the schema defined in references/schema.md.
DD-22: A=JSON syntax, B=Schema conformance, C=source_location validity,
       D=atomicity check.

Reference: pi-hifi's selftest.ts per-component validation approach.
"""

from __future__ import annotations

import json
import jsonschema
import pytest

# JSON Schema for a single claim (matches references/schema.md)
CLAIM_SCHEMA = {
    "type": "object",
    "required": ["claim_id", "claim_text", "source_location", "type"],
    "properties": {
        "claim_id": {"type": "string", "pattern": "^C\\d{3}$"},
        "claim_text": {"type": "string", "minLength": 1},
        "normalized_claim": {"type": "string"},
        "source_location": {
            "type": "string",
            "pattern": r"^[^:]+:\d+(?:[\-:]\d+)*$",
        },
        "content_hash": {"type": "string", "pattern": "^sha256:[0-9a-f]{12}$"},
        "type": {
            "type": "string",
            "enum": [
                "authority", "numerical", "temporal", "factual", "causal",
                "comparative", "code_api", "citation", "existence",
                "interpretation", "file_path", "attribution",
                "legal_med_fin", "pricing", "licensing", "compliance",
                "route", "port", "retry", "timeout",
            ],
        },
        "expected_verifier": {
            "type": "string",
            "enum": ["rule_engine", "web_search", "refused", "inferred"],
        },
        "atomicity_parent": {"type": "string", "pattern": "^C\\d{3}$"},
        "decomposition_mode": {
            "type": "string",
            "enum": [
                "and_enum", "paren_append", "paren_expand", "from_to",
                "clause_embed", "ie_supplement", "dash_supplement",
            ],
        },
        "compound_flag": {"type": "string", "enum": ["compound_embedded"]},
    },
    "additionalProperties": False,
}


def validate_claims(claims: list[dict]) -> list[dict]:
    """Validate a list of claims. Returns list of {claim_id, errors}."""
    failures = []
    for claim in claims:
        errors = []
        # A: JSON syntax — already passed (it's a Python dict)
        # B: Schema
        try:
            jsonschema.validate(claim, CLAIM_SCHEMA)
        except jsonschema.ValidationError as e:
            errors.append({"code": "SCHEMA_ERROR", "detail": e.message})
        if errors:
            failures.append({"claim_id": claim.get("claim_id", "?"), "errors": errors})
    return failures


class TestSchemaValidation:

    def test_valid_claim_passes(self):
        claim = {
            "claim_id": "C001",
            "claim_text": "DeepSeek V3.1 was released in September 2025",
            "source_location": "report.md:42",
            "type": "temporal",
            "expected_verifier": "web_search",
        }
        assert validate_claims([claim]) == []

    def test_missing_required_field(self):
        claim = {
            "claim_id": "C002",
            "claim_text": "some claim",
            # missing source_location
            "type": "factual",
        }
        failures = validate_claims([claim])
        assert len(failures) == 1
        assert failures[0]["errors"][0]["code"] == "SCHEMA_ERROR"

    def test_invalid_type_enum(self):
        claim = {
            "claim_id": "C003",
            "claim_text": "some claim",
            "source_location": "doc.md:1",
            "type": "invalid_type",
        }
        failures = validate_claims([claim])
        assert len(failures) == 1

    def test_invalid_claim_id_format(self):
        claim = {
            "claim_id": "XYZ",
            "claim_text": "some claim",
            "source_location": "doc.md:1",
            "type": "factual",
        }
        failures = validate_claims([claim])
        assert len(failures) == 1

    def test_source_location_formats(self):
        # valid: doc.md:42
        claim1 = {"claim_id": "C010", "claim_text": "t", "source_location": "doc.md:42", "type": "factual"}
        assert validate_claims([claim1]) == []

        # valid: doc.md:42-45
        claim2 = {"claim_id": "C011", "claim_text": "t", "source_location": "doc.md:42-45", "type": "factual"}
        assert validate_claims([claim2]) == []

        # valid: doc.md:42:10-85
        claim3 = {"claim_id": "C012", "claim_text": "t", "source_location": "doc.md:42:10-85", "type": "factual"}
        assert validate_claims([claim3]) == []

        # invalid: no line number
        claim4 = {"claim_id": "C013", "claim_text": "t", "source_location": "doc.md", "type": "factual"}
        assert len(validate_claims([claim4])) == 1

    def test_decomposition_mode_enum(self):
        claim = {
            "claim_id": "C020",
            "claim_text": "supports vLLM and SGLang and llama.cpp",
            "source_location": "doc.md:5",
            "type": "existence",
            "decomposition_mode": "and_enum",
        }
        assert validate_claims([claim]) == []

    def test_compound_flag_valid(self):
        claim = {
            "claim_id": "C030",
            "claim_text": "KVCache spans HBM DRAM NVMe CXL and RDMA",
            "source_location": "doc.md:20",
            "type": "factual",
            "compound_flag": "compound_embedded",
        }
        assert validate_claims([claim]) == []

    def test_hashes_valid(self):
        claim = {
            "claim_id": "C040",
            "claim_text": "test",
            "source_location": "doc.md:1",
            "type": "factual",
            "content_hash": "sha256:a1b2c3d4e5f6",
        }
        assert validate_claims([claim]) == []

    def test_invalid_hash_format(self):
        claim = {
            "claim_id": "C041",
            "claim_text": "test",
            "source_location": "doc.md:1",
            "type": "factual",
            "content_hash": "not-a-valid-hash",
        }
        assert len(validate_claims([claim])) == 1
