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


def test_metrics_md_parser(tmp_path):
    import importlib.util
    script = Path(__file__).parent.parent / "scripts" / "collect-metrics.py"
    spec = importlib.util.spec_from_file_location("cm", script)
    cm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cm)
    md = tmp_path / "metrics.md"
    md.write_text(
        "| 音频时长 | 1633.7s |\n| WAV 大小 | 49.8MB |\n"
        "| 转码耗时 | 2.154s |\n| 推理耗时 | 27.865s |\n"
        "| RTF | .0170 |\n| 字符数 | 18255 |\n| 转录模式 | silence-aware |",
        encoding="utf-8",
    )
    m = cm.parse_metrics_md(md)
    assert m["duration_s"] == 1633.7
    assert m["rtf"] == 0.017  # ".0170" must NOT parse as 170
    assert m["chars"] == 18255
    assert m["mode"] == "silence-aware"
