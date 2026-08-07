"""Integration tests for scripts/validate-claims.sh.

Seam: bash scripts/validate-claims.sh <claims.json> <source-document> → stdout JSON
  { passed, failed, failures: [{claim_id, errors: [{code, detail}]}], auto_fixes }

Four validation levels (DD-22):
  A — JSON syntax
  B — Schema conformance (required fields, types, enum values)
  C1 — source_location valid and readable
  C2 — claim_text matches source text at location
  C3 — content_hash consistency (auto-fix)
  D — Atomicity check (7 catalog modes, compound_embedded)
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def compute_content_hash(text: str) -> str:
    """SHA256(trim(lowercase(text)), normalize whitespace)[:12] with sha256: prefix."""
    cleaned = " ".join(text.strip().lower().split())
    h = hashlib.sha256(cleaned.encode()).hexdigest()[:12]
    return f"sha256:{h}"


def run_validate(claims_json: Path, source_doc: Path) -> tuple[dict, int]:
    """Run validate-claims.sh and return (parsed stdout JSON, exit code)."""
    args = ["bash", str(SCRIPTS_DIR / "validate-claims.sh"),
            str(claims_json), str(source_doc)]
    result = subprocess.run(args, capture_output=True, text=True, timeout=10)
    return json.loads(result.stdout), result.returncode


def _write_claims(claims: list[dict], path: Path) -> None:
    path.write_text(json.dumps(claims, ensure_ascii=False))


def _write_source(lines: list[str], path: Path) -> None:
    path.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# Level A — JSON syntax
# ---------------------------------------------------------------------------


class TestLevelAJsonSyntax:
    def test_valid_json_passes(self):
        source = Path(tempfile.mktemp(suffix=".md"))
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        text = "DeepSeek V3.1 was released in September 2025."
        h = compute_content_hash(text)
        claims = [{
            "claim_id": "C001",
            "claim_text": text,
            "normalized_claim": text,
            "source_location": f"{source.name}:1",
            "content_hash": h,
            "type": "temporal",
            "expected_verifier": "web_search",
        }]
        _write_claims(claims, claims_file)
        _write_source([text], source)
        data, code = run_validate(claims_file, source)
        assert code == 0
        assert data["failed"] == 0

    def test_invalid_json_fails(self):
        source = Path(tempfile.mktemp(suffix=".md"))
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        claims_file.write_text("{not valid json")
        _write_source(["hello"], source)
        data, code = run_validate(claims_file, source)
        # A-level failure → script returns non-zero
        assert code != 0 or data["failed"] > 0


# ---------------------------------------------------------------------------
# Level B — Schema conformance
# ---------------------------------------------------------------------------


class TestLevelBSchema:
    def test_missing_required_field_fails(self):
        source = Path(tempfile.mktemp(suffix=".md"))
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        _write_claims([{"claim_id": "C001"}], claims_file)  # missing claim_text etc
        _write_source(["some text"], source)
        data, code = run_validate(claims_file, source)
        assert data["failed"] > 0

    def test_invalid_type_enum_fails(self):
        source = Path(tempfile.mktemp(suffix=".md"))
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        _write_claims([{
            "claim_id": "C001",
            "claim_text": "test",
            "source_location": f"{source.name}:1",
            "type": "not_a_real_type",
        }], claims_file)
        _write_source(["test"], source)
        data, code = run_validate(claims_file, source)
        assert data["failed"] > 0

    def test_valid_schema_passes(self):
        source = Path(tempfile.mktemp(suffix=".md"))
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        text = "DeepSeek V3.1 was released in September 2025."
        h = compute_content_hash(text)
        _write_claims([{
            "claim_id": "C001",
            "claim_text": text,
            "normalized_claim": text,
            "source_location": f"{source.name}:1",
            "content_hash": h,
            "type": "temporal",
            "expected_verifier": "web_search",
        }], claims_file)
        _write_source([text], source)
        data, code = run_validate(claims_file, source)
        assert data["failed"] == 0


# ---------------------------------------------------------------------------
# Level C — source_location validity + text match + content_hash
# ---------------------------------------------------------------------------


class TestLevelC:
    def test_source_location_valid(self):
        source = Path(tempfile.mktemp(suffix=".md"))
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        text = "DeepSeek V3.1 was released in September 2025."
        h = compute_content_hash(text)
        _write_claims([{
            "claim_id": "C001",
            "claim_text": text,
            "source_location": f"{source.name}:1",
            "content_hash": h,
            "type": "temporal",
        }], claims_file)
        _write_source([text], source)
        data, code = run_validate(claims_file, source)
        assert data["failed"] == 0

    def test_source_location_out_of_range_fails(self):
        source = Path(tempfile.mktemp(suffix=".md"))
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        _write_claims([{
            "claim_id": "C001",
            "claim_text": "test",
            "source_location": f"{source.name}:999",
            "type": "temporal",
        }], claims_file)
        _write_source(["line1"], source)
        data, code = run_validate(claims_file, source)
        assert data["failed"] > 0

    def test_text_mismatch_fails(self):
        source = Path(tempfile.mktemp(suffix=".md"))
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        _write_claims([{
            "claim_id": "C001",
            "claim_text": "completely different text",
            "source_location": f"{source.name}:1",
            "type": "temporal",
        }], claims_file)
        _write_source(["actual source text"], source)
        data, code = run_validate(claims_file, source)
        assert data["failed"] > 0

    def test_content_hash_auto_fix(self):
        source = Path(tempfile.mktemp(suffix=".md"))
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        text = "DeepSeek V3.1 was released in September 2025."
        _write_claims([{
            "claim_id": "C001",
            "claim_text": text,
            "source_location": f"{source.name}:1",
            "content_hash": "sha256:000000000000",  # wrong hash
            "type": "temporal",
        }], claims_file)
        _write_source([text], source)
        data, code = run_validate(claims_file, source)
        assert data["failed"] == 0  # auto-fixed, not failed
        assert len(data.get("auto_fixes", [])) > 0


# ---------------------------------------------------------------------------
# Level D — Atomicity (catalog decomposition modes)
# ---------------------------------------------------------------------------


class TestLevelDAtomicity:
    def test_compound_without_decomposition_passes(self):
        """D-level downgraded: compound claims without decomposition_mode no longer fail."""
        source = Path(tempfile.mktemp(suffix=".md"))
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        text = "It supports Linux and macOS and Windows."
        _write_claims([{
            "claim_id": "C001",
            "claim_text": text,
            "source_location": f"{source.name}:1",
            "content_hash": compute_content_hash(text),
            "type": "factual",
        }], claims_file)
        _write_source([text], source)
        data, code = run_validate(claims_file, source)
        assert data["failed"] == 0  # D-level no longer enforces decomposition

    def test_decomposed_claim_passes(self):
        """A claim that is a child (has atomicity_parent) should pass D level."""
        source = Path(tempfile.mktemp(suffix=".md"))
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        text = "It supports Linux."
        _write_claims([{
            "claim_id": "C002",
            "claim_text": text,
            "source_location": f"{source.name}:1",
            "content_hash": compute_content_hash(text),
            "type": "factual",
            "atomicity_parent": "C001",
            "decomposition_mode": "and_enum",
        }], claims_file)
        _write_source([text], source)
        data, code = run_validate(claims_file, source)
        assert data["failed"] == 0

    def test_compound_embedded_warning(self):
        """>25 words, no catalog match → marked compound_embedded, not failed."""
        source = Path(tempfile.mktemp(suffix=".md"))
        claims_file = Path(tempfile.mktemp(suffix=".json"))
        # 30 words, no and/that/which/即/from-to/parens/dash — truly no catalog match
        text = "The system design incorporates multiple optimization strategies for handling requests efficiently given constraints around memory bandwidth latency sensitivity power consumption thermal throttling requirements throughput targets latency percentiles tail distribution characteristics hardware heterogeneity software compatibility concerns operational overhead monitoring instrumentation deployment complexity configuration management safety considerations"
        _write_claims([{
            "claim_id": "C001",
            "claim_text": text,
            "source_location": f"{source.name}:1",
            "content_hash": compute_content_hash(text),
            "type": "factual",
            "compound_flag": None,
        }], claims_file)
        _write_source([text], source)
        data, code = run_validate(claims_file, source)
        # compound_embedded is a warning not a failure — should still pass
        assert data["failed"] == 0
