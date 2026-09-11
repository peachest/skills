"""Integration tests for scripts/build-claims.py (R24: single-emission contract).

Seam: cat seeds.jsonl | python3 scripts/build-claims.py --doc <doc> --out <claims.json>
  → stdout compact JSON {written, total_in_file, next_id, located, failed, validation}
Merge seam: cat patches.json | ... --merge → {patched, deleted, failed, validation}

Covers the failure mode observed in session 01a07d01 (2026-09-07):
  - format drift (wrong field names / invalid type) must fail fast, zero writes
  - locate failures must return actionable feedback WITHOUT re-emitting the set
  - retries must be incremental (append / patch), never whole-set rewrites
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
BUILD = SCRIPTS_DIR / "build-claims.py"


def run_build(stdin_payload: str, doc: Path, out: Path, *flags: str) -> tuple[dict, int]:
    result = subprocess.run(
        ["python3", str(BUILD), "--doc", str(doc), "--out", str(out), *flags],
        input=stdin_payload, capture_output=True, text=True, timeout=30,
    )
    return json.loads(result.stdout), result.returncode


def make_doc(lines: list[str]) -> Path:
    doc = Path(tempfile.mktemp(suffix=".md"))
    doc.write_text("\n".join(lines) + "\n")
    return doc


DOC_LINES = [
    "# Report",
    "",
    "DeepSeek V3.1 was released in September 2025.",
    "The `enable_dsa_shared_kv_cache` flag does not support an L3 storage backend yet.",
    "arXiv:2412.19437 proposed the method (merged 2025-01-04).",
]


@pytest.fixture
def doc() -> Path:
    return make_doc(DOC_LINES)


@pytest.fixture
def out(tmp_path: Path) -> Path:
    return tmp_path / "claims.json"


class TestAssemble:
    def test_minimal_seeds_assemble_and_validate(self, doc, out):
        seeds = json.dumps([
            {"claim_text": "DeepSeek V3.1 was released in September 2025",
             "type": "temporal", "expected_verifier": "web_search"},
        ])
        data, code = run_build(seeds, doc, out)
        assert code == 0
        assert data["written"] == 1
        assert data["validation"]["failed"] == 0
        claims = json.loads(out.read_text())
        assert claims[0]["claim_id"] == "C001"
        assert claims[0]["source_location"].endswith(".md:3:0-44")
        assert claims[0]["content_hash"].startswith("sha256:")

    def test_backtick_claim_text_survives_stdin(self, doc, out):
        """Round-1 hazard: markdown backticks in claim_text (safe via stdin, not via bash args)."""
        seeds = json.dumps([{
            "claim_text": "The `enable_dsa_shared_kv_cache` flag does not support an L3 storage backend yet.",
            "type": "factual", "expected_verifier": "local_repo",
        }])
        data, code = run_build(seeds, doc, out)
        assert code == 0
        assert data["located"] == 1

    def test_locate_failure_returns_feedback_not_written(self, doc, out):
        seeds = json.dumps([
            {"claim_text": "DeepSeek V3.1 was released in September 2025", "type": "temporal"},
            {"claim_text": "this text is nowhere in the document", "type": "factual"},
        ])
        data, code = run_build(seeds, doc, out)
        assert code == 1
        assert data["written"] == 1
        assert len(data["failed"]) == 1
        assert data["failed"][0]["error"] == "TEXT_NOT_FOUND"
        # the failed claim must NOT be in the file
        claims = json.loads(out.read_text())
        assert len(claims) == 1

    def test_retry_after_failure_is_incremental(self, doc, out):
        """The core R24 regression: fix round 1 → append round 2, ids continue."""
        seeds1 = json.dumps([
            {"claim_text": "DeepSeek V3.1 was released in September 2025", "type": "temporal"},
            {"claim_text": "nowhere to be found", "type": "factual"},
        ])
        run_build(seeds1, doc, out)
        # agent fixes ONLY the failed claim
        seeds2 = json.dumps([
            {"claim_text": "arXiv:2412.19437 proposed the method", "type": "authority",
             "expected_verifier": "rule_engine"},
        ])
        data, code = run_build(seeds2, doc, out)
        assert code == 0
        assert data["total_in_file"] == 2
        claims = json.loads(out.read_text())
        assert [c["claim_id"] for c in claims] == ["C001", "C002"]

    def test_ambiguous_short_text_reports_candidates(self, out):
        doc = make_doc(["The release was in September 2025.", "Another mention of September 2025 here."])
        seeds = json.dumps([{"claim_text": "September 2025", "type": "temporal"}])
        data, code = run_build(seeds, doc, out)
        # AMBIGUOUS (≤20 chars, multiple positions) — failed, not written
        assert code == 1
        assert data["written"] == 0
        assert data["failed"][0]["error"] == "AMBIGUOUS"
        assert len(data["failed"][0]["candidates"]) >= 2

    def test_compound_claim_gets_atomicity_fields(self, doc, out):
        text = "arXiv:2412.19437 proposed the method (merged 2025-01-04)."
        seeds = json.dumps([{"claim_text": text, "type": "authority"}])
        data, code = run_build(seeds, doc, out)
        assert code == 0
        claims = json.loads(out.read_text())
        assert claims[0]["decomposition_mode"] == "paren_append"

    def test_replace_discards_existing(self, doc, out):
        run_build(json.dumps([
            {"claim_text": "DeepSeek V3.1 was released in September 2025", "type": "temporal"}]), doc, out)
        data, code = run_build(json.dumps([
            {"claim_text": "arXiv:2412.19437 proposed the method", "type": "authority"}]),
            doc, out, "--replace")
        assert code == 0
        assert data["total_in_file"] == 1
        claims = json.loads(out.read_text())
        assert claims[0]["claim_id"] == "C001"
        assert claims[0]["type"] == "authority"


class TestFormatDriftGuard:
    """The exact round-1 disaster: wrong field names + invented type enum."""

    def test_invalid_type_fails_fast_zero_writes(self, doc, out):
        seeds = json.dumps([
            {"id": "C001", "locator": "anchor", "type": "code_anchor",
             "claim_text": "DeepSeek V3.1 was released in September 2025"},
        ])
        result = subprocess.run(
            ["python3", str(BUILD), "--doc", str(doc), "--out", str(out)],
            input=seeds, capture_output=True, text=True, timeout=30,
        )
        assert result.returncode == 2
        err = json.loads(result.stderr)
        assert "invalid type" in err["error"]
        assert not out.exists() or json.loads(out.read_text()) == []

    def test_missing_claim_text_fails_fast(self, doc, out):
        seeds = json.dumps([{"type": "temporal"}])
        result = subprocess.run(
            ["python3", str(BUILD), "--doc", str(doc), "--out", str(out)],
            input=seeds, capture_output=True, text=True, timeout=30,
        )
        assert result.returncode == 2

    def test_jsonl_input_accepted(self, doc, out):
        seeds = json.dumps({"claim_text": "DeepSeek V3.1 was released in September 2025",
                            "type": "temporal"})
        data, code = run_build(seeds, doc, out)
        assert code == 0 and data["written"] == 1


class TestMerge:
    def _seeded(self, doc, out):
        run_build(json.dumps([
            {"claim_text": "DeepSeek V3.1 was released in September 2025", "type": "temporal"},
        ]), doc, out)

    def test_patch_claim_text_relocates(self, doc, out):
        self._seeded(doc, out)
        patches = json.dumps([{
            "claim_id": "C001",
            "patch": {"claim_text": "DeepSeek V3.1 was released in September 2025"},
        }])
        data, code = run_build(patches, doc, out, "--merge")
        assert code == 0
        assert data["patched"] == ["C001"]
        assert data["validation"]["failed"] == 0

    def test_delete_claim(self, doc, out):
        self._seeded(doc, out)
        patches = json.dumps([{"claim_id": "C001", "delete": True}])
        data, code = run_build(patches, doc, out, "--merge")
        assert code == 0
        assert data["deleted"] == ["C001"]
        assert json.loads(out.read_text()) == []

    def test_unknown_claim_id_fails(self, doc, out):
        self._seeded(doc, out)
        patches = json.dumps([{"claim_id": "C999", "patch": {"type": "factual"}}])
        data, code = run_build(patches, doc, out, "--merge")
        assert code == 1
        assert data["failed"][0]["error"] == "CLAIM_NOT_FOUND"

    def test_merge_requires_existing_file(self, doc, out):
        patches = json.dumps([{"claim_id": "C001", "delete": True}])
        result = subprocess.run(
            ["python3", str(BUILD), "--doc", str(doc), "--out", str(out), "--merge"],
            input=patches, capture_output=True, text=True, timeout=30,
        )
        assert result.returncode == 2
