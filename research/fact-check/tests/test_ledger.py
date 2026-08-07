"""Tests for per-document ledger (JSONL append-only, vid-覆盖).

DD-09: append-only JSONL, latest timestamp wins.
DD-14: status machine (extracted → checked → resolved).

Reference: groundcheck's claim ledger schema.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path


def ledger_append(ledger_path: Path, entry: dict) -> None:
    """Append one claim verdict entry to the ledger JSONL file."""
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with open(ledger_path, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def ledger_query(ledger_path: Path, vid: str | None = None) -> list[dict]:
    """Query the ledger — optionally filtered by vid."""
    if not ledger_path.exists():
        return []
    results = []
    with open(ledger_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if vid is None or entry.get("vid") == vid:
                results.append(entry)
    return results


def ledger_latest(ledger_path: Path, vid: str) -> dict | None:
    """Get the most recent entry for a vid (timestamp wins)."""
    entries = ledger_query(ledger_path, vid)
    if not entries:
        return None
    return max(entries, key=lambda e: e.get("timestamp", ""))


class TestLedgerAppend:
    def test_append_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.ledger.jsonl"
            ledger_append(path, {"vid": "abc123", "verdict": "SUPPORTED", "timestamp": "2026-07-09T00:00:00Z"})
            assert path.exists()

    def test_append_multiple_unique_vids(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.ledger.jsonl"
            ledger_append(path, {"vid": "abc", "verdict": "SUPPORTED", "timestamp": "2026-07-09T00:00:00Z"})
            ledger_append(path, {"vid": "def", "verdict": "CONTRADICTED", "timestamp": "2026-07-09T00:00:01Z"})
            assert len(ledger_query(path)) == 2

    def test_latest_timestamp_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.ledger.jsonl"
            ledger_append(path, {"vid": "abc", "verdict": "CONTRADICTED", "timestamp": "2026-07-09T00:00:00Z"})
            ledger_append(path, {"vid": "abc", "verdict": "SUPPORTED", "timestamp": "2026-07-09T01:00:00Z"})
            latest = ledger_latest(path, "abc")
            assert latest["verdict"] == "SUPPORTED"
            assert latest["timestamp"] == "2026-07-09T01:00:00Z"

    def test_query_by_vid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.ledger.jsonl"
            ledger_append(path, {"vid": "abc", "verdict": "SUPPORTED", "timestamp": "2026-07-09T00:00:00Z"})
            ledger_append(path, {"vid": "def", "verdict": "CONTRADICTED", "timestamp": "2026-07-09T00:00:01Z"})
            assert len(ledger_query(path, "abc")) == 1
            assert ledger_query(path, "abc")[0]["vid"] == "abc"

    def test_empty_ledger_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nonexistent.ledger.jsonl"
            assert ledger_query(path) == []
            assert ledger_latest(path, "abc") is None

    def test_append_preserves_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.ledger.jsonl"
            entry = {"vid": "xyz", "claim_text": "MLA 压缩使 CPU 推理可行", "verdict": "INFERRED", "timestamp": "2026-07-09T00:00:00Z"}
            ledger_append(path, entry)
            results = ledger_query(path)
            assert results[0]["claim_text"] == "MLA 压缩使 CPU 推理可行"
