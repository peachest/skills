"""Stub-endpoint smoke tests for chunk_transcribe.py (architecture candidate ③).

The transcribe.sh direct-curl path was removed — direct.json must now be
written by chunk_transcribe.py itself. These tests spin a local fake ASR
server (OpenAI /audio/transcriptions shape) and run the real script.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import threading
import wave
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "chunk_transcribe.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("chunk_transcribe_smoke", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VERBOSE_JSON = {
    "text": "你好世界，这是一段测试转录。",
    "segments": [
        {"start": 0.0, "end": 1.5, "text": " 你好世界，",
         "avg_logprob": -0.2, "compression_ratio": 1.1},
        {"start": 1.5, "end": 3.0, "text": " 这是一段测试转录。",
         "avg_logprob": -0.3, "compression_ratio": 1.2},
    ],
}


def _make_wav(path: Path, seconds: float = 1.0, rate: int = 16000):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"\x00\x00" * int(rate * seconds))


class _FakeASR(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        self.rfile.read(length)  # drain multipart body
        body = json.dumps(VERBOSE_JSON).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # silence request logging
        pass


def _serve():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _FakeASR)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server, f"http://127.0.0.1:{server.server_port}"


def test_direct_writes_direct_json_and_output(tmp_path):
    mod = _load_module()
    wav = tmp_path / "audio.wav"
    _make_wav(wav)
    out = tmp_path / "transcript_raw.txt"
    server, endpoint = _serve()
    try:
        rc = subprocess.run(
            [sys.executable, str(SCRIPT), "--wav", str(wav),
             "--endpoint", endpoint, "--model", "test-model", "--lang", "zh",
             "--output", str(out)],
            capture_output=True, text=True, timeout=60)
        assert rc.returncode == 0, rc.stderr[-500:]
    finally:
        server.shutdown()

    assert out.read_text(encoding="utf-8") == VERBOSE_JSON["text"]
    direct = tmp_path / "chunks" / "transcripts" / "direct.json"
    assert direct.is_file(), "direct.json must be written by chunk_transcribe.py itself"
    data = json.loads(direct.read_text(encoding="utf-8"))
    assert data["text"] == VERBOSE_JSON["text"]
    assert len(data["segments"]) == 2  # dual-transcribe harvests these


def test_no_chunk_flag_forces_direct(tmp_path):
    """--no-chunk overrides the size check: small file, flag set, still direct."""
    mod = _load_module()
    wav = tmp_path / "audio.wav"
    _make_wav(wav)
    out = tmp_path / "transcript_raw.txt"
    server, endpoint = _serve()
    try:
        rc = subprocess.run(
            [sys.executable, str(SCRIPT), "--wav", str(wav),
             "--endpoint", endpoint, "--model", "test-model", "--lang", "zh",
             "--no-chunk", "--max-filesize-mb", "0.001",
             "--output", str(out)],
            capture_output=True, text=True, timeout=60)
        assert rc.returncode == 0, rc.stderr[-500:]
    finally:
        server.shutdown()

    assert out.is_file()
    assert (tmp_path / "chunks" / "transcripts" / "direct.json").is_file()
    # no chunk wav files created — went straight to direct
    assert not list(tmp_path.glob("chunks/chunk_*.wav"))
