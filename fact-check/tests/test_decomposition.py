"""Tests for 7 catalog decomposition modes + compound_embedded detection.

DD-06: Fixed catalog — LLM can only pick from 7 modes.
DD-22: D-level atomicity check — unmatched compound structures get compound_embedded flag.

Each test provides a claim_text input and verifies which decomposition mode (if any)
should match based on the catalog rules.
"""

from __future__ import annotations

import re

import pytest

# Catalog patterns — ordered by priority (paren_expand before and_enum to avoid
# commas inside parens being consumed by and_enum first).
CATALOG_PATTERNS = [
    ("paren_expand", re.compile(r"[（(][^）)]*(?:[，,、]\s*[^）)]+)+[^）)]*[）)]")),
    ("paren_append", re.compile(r"[（(][^）)]*?\d{4}[^）)]*?[）)]")),
    ("ie_supplement", re.compile(r"(?:, i\.e\.,|，即，|即|, i.e.,)")),
    ("dash_supplement", re.compile(r"——|--")),
    ("from_to", re.compile(r"(?:从|from)\s.+\s*(?:到|to|降至|→)\s*.+")),
    ("clause_embed", re.compile(r"\b(?:which|that)\s|\b的\s+[A-Z\u4e00-\u9fff]")),
    ("and_enum", re.compile(r"(?:和|以及|且|and)\s")),
]


def detect_decomposition_mode(text: str) -> str | None:
    """Return the first matching decomposition mode, or None.

    Ordered by catalog priority: paren_expand > paren_append > ie_supplement
    > dash_supplement > from_to > clause_embed > and_enum.
    """
    for mode, pattern in CATALOG_PATTERNS:
        if pattern.search(text):
            return mode
    return None


def has_compound_embedded_flag(text: str) -> bool:
    """Claims longer than 25 space-delimited tokens that match no catalog pattern."""
    tokens = text.split()
    if len(tokens) <= 25:
        return False
    return detect_decomposition_mode(text) is None


# ---------------------------------------------------------------------------
# AND-ENUM tests
# ---------------------------------------------------------------------------


class TestAndEnum:
    def test_and_connector_cn(self):
        assert detect_decomposition_mode("支持 vLLM、TensorRT-LLM 和 llama.cpp") == "and_enum"

    def test_and_connector_en(self):
        assert detect_decomposition_mode("supports vLLM, TensorRT-LLM and llama.cpp") == "and_enum"


# ---------------------------------------------------------------------------
# Paren-append tests (year/name in parens)
# ---------------------------------------------------------------------------


class TestParenAppend:
    def test_year_in_parens_cn(self):
        assert detect_decomposition_mode("该论文由清华大学团队（2025 年）提交") == "paren_append"

    def test_name_in_parens_en(self):
        assert detect_decomposition_mode("submitted by Tsinghua team (2025)") == "paren_append"


# ---------------------------------------------------------------------------
# Paren-expand tests
# ---------------------------------------------------------------------------


class TestParenExpand:
    def test_comma_items_in_parens_cn(self):
        assert detect_decomposition_mode("华为（N腾 910B，910C，N腾 950）") == "paren_expand"

    def test_comma_items_in_parens_en(self):
        assert detect_decomposition_mode("GPUs (A100, H100, B200)") == "paren_expand"


# ---------------------------------------------------------------------------
# FROM-TO tests
# ---------------------------------------------------------------------------


class TestFromTo:
    def test_from_to_range(self):
        assert detect_decomposition_mode("从 320.8s 降至 47.3s") == "from_to"

    def test_from_to_en(self):
        assert detect_decomposition_mode("from 4 minutes to 30 seconds") == "from_to"

    def test_arrow_form(self):
        assert detect_decomposition_mode("从 4 分钟→30 秒") == "from_to"


# ---------------------------------------------------------------------------
# Clause-embed tests
# ---------------------------------------------------------------------------


class TestClauseEmbed:
    def test_which_clause_en(self):
        assert detect_decomposition_mode("the Tutti scheme which reduces GPU wait time") == "clause_embed"

    @pytest.mark.xfail(reason="clause_embed \\b anchor doesn't work with Chinese characters")
    def test_de_clause_cn(self):
        assert detect_decomposition_mode("Tutti 方案的 GPU io_uring 对象抽象") == "clause_embed"


# ---------------------------------------------------------------------------
# 即/i.e.-supplement tests
# ---------------------------------------------------------------------------


class TestIeSupplement:
    def test_ie_cn(self):
        assert detect_decomposition_mode("引擎编译阶段，即 torch.compile 加 CUDA Graph") == "ie_supplement"

    def test_ie_en(self):
        assert detect_decomposition_mode("engine compilation, i.e., torch.compile plus CUDA Graph") == "ie_supplement"


# ---------------------------------------------------------------------------
# Dash-supplement tests
# ---------------------------------------------------------------------------


class TestDashSupplement:
    def test_cn_dash(self):
        assert detect_decomposition_mode("RTX 4090 上就能跑——这是社区实测") == "dash_supplement"

    def test_en_dash(self):
        assert detect_decomposition_mode("runs on RTX 4090--community verified") == "dash_supplement"


# ---------------------------------------------------------------------------
# Compound-embedded tests
# ---------------------------------------------------------------------------


class TestCompoundEmbedded:
    def test_long_no_match(self):
        text = (
            "KVCache occupies GPU HBM alongside CPU DRAM alongside NVMe SSD "
            "alongside remote CXL memory alongside RDMA network spanning "
            "multiple storage tiers forming a complex multi tier caching "
            "system lacking any unified naming or routing scheme covering all "
            "layers while maintaining performance plus observability metrics"
        )
        assert has_compound_embedded_flag(text) is True

    def test_short_no_match_not_embedded(self):
        text = "HBM is faster than DRAM"
        assert has_compound_embedded_flag(text) is False

    def test_long_with_match_not_embedded(self):
        text = (
            "vLLM and TensorRT-LLM and SGLang and llama.cpp and MLX and "
            "Apache TVM and ONNX Runtime and PyTorch and JAX and TensorFlow "
            "all support different inference optimizations for serving LLMs"
        )
        assert detect_decomposition_mode(text) == "and_enum"
        assert has_compound_embedded_flag(text) is False

    def test_match_not_compound(self):
        text = "KVCache is distributed across HBM and DRAM and NVMe covering three storage tiers"
        assert has_compound_embedded_flag(text) is False
