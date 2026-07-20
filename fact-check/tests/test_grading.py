"""Integration tests for scripts/grade-evidence.sh and generate-report.sh."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def run_grade(stdin_data: str) -> tuple[dict | list, int]:
    args = ["bash", str(SCRIPTS_DIR / "grade-evidence.sh")]
    result = subprocess.run(args, input=stdin_data, capture_output=True, text=True, timeout=10)
    return json.loads(result.stdout), result.returncode


def run_generate(claims_file: Path, run_file: Path, run_dir: Path) -> tuple[dict, int]:
    args = ["bash", str(SCRIPTS_DIR / "generate-report.sh"),
            str(claims_file), str(run_file), str(run_dir)]
    result = subprocess.run(args, capture_output=True, text=True, timeout=10)
    return json.loads(result.stdout), result.returncode


# ---------------------------------------------------------------------------
# grade-evidence.sh tests
# ---------------------------------------------------------------------------

class TestGradeEvidence:
    def test_github_tier1(self):
        data, code = run_grade(json.dumps({
            "claim_id": "C001", "evidence_url": "https://github.com/ggerganov/llama.cpp/pull/11049",
            "evidence_text": "PR #11049"
        }))
        assert code == 0
        assert data["evidence_tier"] == "T1"

    def test_blog_tier2(self):
        data, code = run_grade(json.dumps({
            "claim_id": "C001", "evidence_url": "https://blog.example.com/post",
            "evidence_text": "blog post"
        }))
        assert code == 0
        assert data["evidence_tier"] == "T2"

    def test_reddit_tier3(self):
        data, code = run_grade(json.dumps({
            "claim_id": "C001", "evidence_url": "https://reddit.com/r/ml/comments/abc",
            "evidence_text": "reddit post"
        }))
        assert code == 0
        assert data["evidence_tier"] == "T3"

    def test_no_url_tier4(self):
        data, code = run_grade(json.dumps({
            "claim_id": "C001", "evidence_url": "", "evidence_text": "no url"
        }))
        assert code == 0
        assert data["evidence_tier"] == "T4"

    def test_staleness_fresh(self):
        data, code = run_grade(json.dumps({
            "claim_id": "C001", "evidence_url": "https://github.com/x/y",
            "evidence_date": "2026-07-01"
        }))
        assert code == 0
        assert data["staleness_warning"] is False

    def test_staleness_old(self):
        data, code = run_grade(json.dumps({
            "claim_id": "C001", "evidence_url": "https://github.com/x/y",
            "evidence_date": "2020-01-01"
        }))
        assert code == 0
        assert data["staleness_warning"] is True

    def test_cross_validation_high_confidence(self):
        data, code = run_grade(json.dumps([
            {"claim_id": "C001", "verdict": "SUPPORTED", "evidence_url": "https://github.com/a/b", "evidence_text": ""},
            {"claim_id": "C001", "verdict": "SUPPORTED", "evidence_url": "https://docs.example.com/c", "evidence_text": ""},
        ]))
        assert code == 0
        for d in data:
            assert d["confidence"] == "high"

    def test_cross_validation_low_confidence(self):
        data, code = run_grade(json.dumps([
            {"claim_id": "C001", "verdict": "SUPPORTED", "evidence_url": "https://github.com/a/b", "evidence_text": ""},
            {"claim_id": "C001", "verdict": "CONTRADICTED", "evidence_url": "https://docs.example.com/c", "evidence_text": ""},
        ]))
        assert code == 0
        for d in data:
            assert d["confidence"] == "low"


# ---------------------------------------------------------------------------
# generate-report.sh tests
# ---------------------------------------------------------------------------

class TestGenerateReport:
    def test_generates_all_files(self):
        tmp = Path(tempfile.mkdtemp())
        # Simulate fact-check/ directory structure
        fact_check = tmp / "fact-check"
        docs_dir = fact_check / "documents" / "doc.md"
        docs_dir.mkdir(parents=True)
        claims_file = docs_dir / "claims.json"
        run_file = fact_check / "run.json"
        run_dir = fact_check / "run-20260101-000000-main"
        run_dir.mkdir()

        claims = [
            {"claim_id": "C001", "claim_text": "arXiv:2605.18071 exists", "source_location": "doc.md:1",
             "verdict": "SUPPORTED", "evidence_tier": "T1", "evidence_url": "https://arxiv.org/abs/2605.18071",
             "evidence": "HTTP 200", "confidence": "high", "severity": "low"},
            {"claim_id": "C002", "claim_text": "This method is better", "source_location": "doc.md:2",
             "verdict": "REFUSED", "evidence_tier": "T4", "evidence_url": "",
             "evidence": "value judgment", "confidence": "medium", "severity": "low"},
            {"claim_id": "C003", "claim_text": "RFC 99999 does not exist", "source_location": "doc.md:3",
             "verdict": "CONTRADICTED", "evidence_tier": "T1", "evidence_url": "https://rfc-editor.org/rfc/rfc99999.txt",
             "evidence": "HTTP 404", "confidence": "high", "severity": "high"},
        ]
        claims_file.write_text(json.dumps(claims))
        run_file.write_text(json.dumps({
            "session_tag": "main", "mode": "full", "repo": "test/repo",
            "document_key": "doc.md", "documents": ["doc.md"],
            "started_at": "2026-01-01T00:00:00Z",
        }))

        data, code = run_generate(claims_file, run_file, run_dir)
        assert code == 0

        # Check files exist
        assert (run_dir / "report.md").exists()
        assert (run_dir / "handoff.md").exists()
        assert "report" in data
        assert data["total_claims"] == 3

        # Check report content
        report = (run_dir / "report.md").read_text()
        assert "C001" in report
        assert "SUPPORTED" in report
        assert "C003" in report
        assert "CONTRADICTED" in report

        # handoff.md only has CONTRADICTED/NUANCED
        handoff = (run_dir / "handoff.md").read_text()
        assert "C003" in handoff
        assert "<!-- handoff-claim C003 -->" in handoff
        assert "C001" not in handoff  # SUPPORTED shouldn't be in handoff

        # ledger.jsonl appended
        ledger = docs_dir / "ledger.jsonl"
        assert ledger.exists()
        lines = ledger.read_text().strip().split("\n")
        assert len(lines) == 3

        # total-stats.json created (in fact-check/ dir)
        stats_file = fact_check / "total-stats.json"
        assert stats_file.exists()

        # run.json updated
        updated_run = json.loads(run_file.read_text())
        assert "completed_at" in updated_run
        assert updated_run["total_claims"] == 3

    def test_empty_claims(self):
        tmp = Path(tempfile.mkdtemp())
        fact_check = tmp / "fact-check"
        docs_dir = fact_check / "documents" / "empty.md"
        docs_dir.mkdir(parents=True)
        claims_file = docs_dir / "claims.json"
        run_file = fact_check / "run.json"
        run_dir = fact_check / "run-empty"
        run_dir.mkdir()

        claims_file.write_text("[]")
        run_file.write_text(json.dumps({
            "session_tag": "main", "mode": "full", "repo": "test/repo",
            "document_key": "empty.md", "documents": ["empty.md"],
            "started_at": "2026-01-01T00:00:00Z",
        }))

        data, code = run_generate(claims_file, run_file, run_dir)
        assert code == 0
        assert data["total_claims"] == 0
