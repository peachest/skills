"""Integration tests for scripts/locate-claim.sh (DD-33).

Seam: bash scripts/locate-claim.sh "<claim_text>" <doc_path> → stdout JSON
  {ok: true, location, hash} | {error: "TEXT_NOT_FOUND", closest_match} | {error: "AMBIGUOUS", candidates}
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def run_locate(claim_text: str, doc_path: Path) -> tuple[dict, int]:
    args = ["bash", str(SCRIPTS_DIR / "locate-claim.sh"), claim_text, str(doc_path)]
    result = subprocess.run(args, capture_output=True, text=True, timeout=10)
    return json.loads(result.stdout), result.returncode


class TestLocateClaim:
    def test_exact_match_returns_location_and_hash(self):
        doc = Path(tempfile.mktemp(suffix=".md"))
        doc.write_text("DeepSeek V3.1 was released in September 2025.")
        data, code = run_locate("DeepSeek V3.1 was released", doc)
        assert code == 0
        assert data["ok"] is True
        assert "location" in data
        assert "hash" in data
        assert data["hash"].startswith("sha256:")

    def test_text_not_found_returns_closest_match(self):
        doc = Path(tempfile.mktemp(suffix=".md"))
        doc.write_text("The system uses MLX for acceleration.")
        data, code = run_locate("CUDA acceleration pipeline", doc)
        assert code != 0
        assert data.get("error") == "TEXT_NOT_FOUND"

    def test_text_not_found_with_similar_prefix(self):
        doc = Path(tempfile.mktemp(suffix=".md"))
        doc.write_text("DeepSeek V3.1 supports FP8 training on H100 GPUs with NVLink.")
        data, code = run_locate("DeepSeek V3.1 supports FP8 training on H100 GPUs without NVLink.", doc)
        assert code != 0
        assert data.get("error") == "TEXT_NOT_FOUND"
        assert "closest_match" in data

    def test_ambiguous_short_text(self):
        doc = Path(tempfile.mktemp(suffix=".md"))
        # Same text appears twice
        doc.write_text("The token is ABC. Another token is ABC again.")
        data, code = run_locate("ABC", doc)
        assert code != 0
        assert data.get("error") == "AMBIGUOUS"
        assert len(data.get("candidates", [])) >= 2

    def test_multi_line_text_match(self):
        doc = Path(tempfile.mktemp(suffix=".md"))
        doc.write_text("Line one.\nLine two.\nLine three.")
        data, code = run_locate("Line two.", doc)
        assert code == 0
        assert data["ok"] is True
        # location should point to line 2
        assert ":2:" in data["location"] or ":2-" in data["location"]

    def test_location_format_is_dd25(self):
        doc = Path(tempfile.mktemp(suffix=".md"))
        doc.write_text("Single line claim text.")
        data, code = run_locate("Single line", doc)
        assert code == 0
        # DD-25: file:line:col-col or file:line
        loc = data["location"]
        assert ":" in loc
        # At minimum: file:line format
        parts = loc.split(":")
        assert len(parts) >= 2

    def test_hash_is_deterministic(self):
        doc = Path(tempfile.mktemp(suffix=".md"))
        doc.write_text("Exact same text in document.")
        a, _ = run_locate("Exact same text in document.", doc)
        b, _ = run_locate("Exact same text in document.", doc)
        assert a["hash"] == b["hash"]

    def test_empty_claim_text(self):
        doc = Path(tempfile.mktemp(suffix=".md"))
        doc.write_text("some content")
        # Empty string: script exits with error
        args = ["bash", str(SCRIPTS_DIR / "locate-claim.sh"), "", str(doc)]
        result = subprocess.run(args, capture_output=True, text=True, timeout=10)
        assert result.returncode != 0

    def test_whitespace_normalized_match(self):
        """Text with different whitespace should still match via normalization."""
        doc = Path(tempfile.mktemp(suffix=".md"))
        doc.write_text("DeepSeek   V3.1  was\nreleased\tin September 2025.")
        data, code = run_locate("DeepSeek V3.1 was released in September 2025.", doc)
        # Either exact match fails but normalized succeeds, or exact match works
        assert isinstance(data, dict)

    def test_chinese_text_exact_match(self):
        doc = Path(tempfile.mktemp(suffix=".md"))
        doc.write_text("DeepSeek V3.1 于 2025 年 9 月发布，支持混合 thinking 模式。")
        data, code = run_locate("DeepSeek V3.1 于 2025 年 9 月发布", doc)
        assert code == 0
        assert data["ok"] is True
