"""Tests for enumerate-uploader.py — arg validation and duration parsing only
(network-dependent paths are exercised live, not in tests)."""

import importlib.util
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "enumerate-uploader.py"


def test_requires_bv_or_mid():
    r = subprocess.run(
        [sys.executable, str(SCRIPT)], capture_output=True, text=True
    )
    assert r.returncode == 2
    assert "--bv" in r.stderr and "--mid" in r.stderr


def test_bv_and_mid_mutually_exclusive():
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--bv", "BV1xx", "--mid", "123"],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 2
    assert "not allowed with" in r.stderr


def test_duration_parser():
    spec = importlib.util.spec_from_file_location("eu", SCRIPT)
    eu = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(eu)
    assert eu.dur_sec("10:15") == 615
    assert eu.dur_sec("1:02:03") == 3723
    assert eu.dur_sec("0:00") == 0
    assert eu.dur_sec("") == 0
