"""Tests for content_hash computation and VID generation.

content_hash: SHA256(trim(lowercase(原文 at source_location).replace(/\s+/g, ' ')))[:12]
VID:           SHA256(claim_text.trim().to_lowercase())[:12]

Reference: DD-08 (VID generation), DD-24 (content_hash).
"""

import hashlib


def compute_content_hash(text: str) -> str:
    """SHA256(trim(lowercase(text)), normalize whitespace)[:12]"""
    cleaned = " ".join(text.strip().lower().split())
    return hashlib.sha256(cleaned.encode()).hexdigest()[:12]


def generate_vid(claim_text: str) -> str:
    """SHA256(claim_text.trim().to_lowercase())[:12]"""
    cleaned = claim_text.strip().lower()
    return hashlib.sha256(cleaned.encode()).hexdigest()[:12]


class TestContentHash:
    def test_same_text_same_hash(self):
        a = compute_content_hash("DeepSeek V3.1 was released in September 2025")
        b = compute_content_hash("DeepSeek V3.1 was released in September 2025")
        assert a == b

    def test_case_insensitive(self):
        a = compute_content_hash("KVCache spans HBM DRAM and NVMe")
        b = compute_content_hash("kvcache spans hbm dram and nvme")
        assert a == b

    def test_whitespace_normalization(self):
        a = compute_content_hash("  KVCache   spans   HBM  ")
        b = compute_content_hash("KVCache spans HBM")
        assert a == b

    def test_different_text_different_hash(self):
        a = compute_content_hash("6,440 tok/s on H100")
        b = compute_content_hash("6440 tok/s on H100")
        # comma difference = different content, different hash
        assert a != b

    def test_hash_length(self):
        h = compute_content_hash("any text")
        assert len(h) == 12

    def test_hash_hex_format(self):
        h = compute_content_hash("test")
        assert all(c in "0123456789abcdef" for c in h)


class TestVid:
    def test_same_text_same_vid(self):
        assert generate_vid("arXiv:2605.18071 exists") == generate_vid("arXiv:2605.18071 exists")

    def test_case_insensitive(self):
        assert generate_vid("VLLM IS BETTER") == generate_vid("vllm is better")

    def test_slight_diff_different_vid(self):
        assert generate_vid("PR #3729") != generate_vid("PR#3729")

    def test_vid_length(self):
        assert len(generate_vid("any claim")) == 12
