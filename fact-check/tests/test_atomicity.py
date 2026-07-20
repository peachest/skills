"""Integration tests for scripts/check-atomicity.sh (DD-34).

Seam: bash scripts/check-atomicity.sh "<claim_text>" → stdout JSON
  {match, pattern, sub_items, word_count}
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def run_check(text: str) -> tuple[dict, int]:
    args = ["bash", str(SCRIPTS_DIR / "check-atomicity.sh"), text]
    result = subprocess.run(args, capture_output=True, text=True, timeout=10)
    return json.loads(result.stdout), result.returncode


class TestCheckAtomicity:
    # --- and_enum ---
    def test_and_enum_chinese(self):
        data, code = run_check("支持 Linux 和 macOS 以及 Windows")
        assert code == 0
        assert data["match"] is True
        assert data["pattern"] == "and_enum"
        assert len(data["sub_items"]) == 3

    def test_and_enum_english(self):
        data, code = run_check("It supports Linux and macOS and Windows")
        assert code == 0
        assert data["match"] is True
        assert data["pattern"] == "and_enum"

    # --- paren_expand ---
    def test_paren_expand(self):
        data, code = run_check("V3.1（2025年9月发布，128K 上下文，支持混合 thinking）")
        assert code == 0
        assert data["match"] is True
        assert data["pattern"] == "paren_expand"

    # --- paren_append ---
    def test_paren_append(self):
        data, code = run_check("PR #11049 (merged 2025-01-04) adds DeepSeek V3 support")
        assert code == 0
        assert data["match"] is True
        assert data["pattern"] == "paren_append"
        assert len(data["sub_items"]) >= 2

    # --- from_to ---
    def test_from_to_chinese(self):
        data, code = run_check("冷启动从 20 分钟压缩到 7 秒")
        assert code == 0
        assert data["match"] is True
        assert data["pattern"] == "from_to"
        assert len(data["sub_items"]) == 2
        assert "before" in data["sub_items"][0]

    def test_from_to_english(self):
        data, code = run_check("latency reduced from 500ms to 50ms")
        assert code == 0
        assert data["match"] is True
        assert data["pattern"] == "from_to"

    # --- ie_supplement ---
    def test_ie_supplement(self):
        data, code = run_check("MLA，即 Multi-head Latent Attention，压缩 KV cache")
        assert code == 0
        assert data["match"] is True
        assert data["pattern"] == "ie_supplement"

    # --- dash_supplement ---
    def test_dash_supplement(self):
        data, code = run_check("Q4_K_M 量化——约 404GB——在 EPYC 上可达 6.44 tok/s")
        assert code == 0
        assert data["match"] is True
        assert data["pattern"] == "dash_supplement"

    # --- clause_embed ---
    def test_clause_embed_which(self):
        data, code = run_check("PR #11049 which was merged on 2025-01-04 added V3 support")
        assert code == 0
        assert data["match"] is True
        assert data["pattern"] == "clause_embed"

    # --- no match ---
    def test_no_match_atomic(self):
        data, code = run_check("a simple atomic claim")
        assert code == 0
        assert data["match"] is False
        assert data["pattern"] == "none"
        assert data["sub_items"] == []

    # --- word_count ---
    def test_word_count(self):
        data, code = run_check("one two three four five")
        assert code == 0
        assert data["word_count"] == 5

    def test_word_count_zero(self):
        # Empty string: script exits with usage error
        args = ["bash", str(SCRIPTS_DIR / "check-atomicity.sh"), ""]
        result = subprocess.run(args, capture_output=True, text=True, timeout=10)
        assert result.returncode != 0

    # --- priority: paren before and_enum ---
    def test_paren_before_and_enum(self):
        """Paren patterns have higher priority than and_enum."""
        data, code = run_check("模型（2025年发布，支持 Linux，支持 macOS）发布")
        assert code == 0
        # paren_expand should win with comma separators inside parens
        assert data["match"] is True
        assert data["pattern"] == "paren_expand"
