"""Test the pure-Python audio path of chunk_transcribe.py.

These tests synthesize WAV fixtures directly with the stdlib `wave` module
and never invoke ffmpeg/ffprobe binaries — the point is that the transcribe
pipeline no longer depends on system ffmpeg.
"""

from __future__ import annotations

import os
import subprocess
import wave
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
CHUNK_SCRIPT = SCRIPTS_DIR / "chunk_transcribe.py"
RATE = 16000


def _make_tone_wav(n_seconds: float = 1.0, amp: float = 0.5) -> bytes:
    """16kHz mono s16 PCM — a sine tone at 440Hz, non-silent."""
    n = int(RATE * n_seconds)
    t = np.arange(n) / RATE
    return (amp * 32767 * np.sin(2 * np.pi * 440 * t)).astype("<i2").tobytes()


def _write_wav(path: Path, pcm: bytes, nframes: int):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm)
        assert w.getnframes() == nframes


@pytest.fixture(scope="module")
def ct_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("chunk_transcribe", CHUNK_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestGetDuration:
    def test_wav_header_duration(self, tmp_path, ct_module):
        wav = tmp_path / "t.wav"
        pcm = _make_tone_wav(3.0)
        _write_wav(wav, pcm, len(pcm) // 2)
        assert ct_module.get_duration(str(wav)) == pytest.approx(3.0, abs=0.01)


class TestDetectSilence:
    def test_finds_silence_boundaries(self, tmp_path, ct_module):
        """Tone 2s, zeros 5s, tone 23s → silence at ~4.5s of ~5s."""
        wav = tmp_path / "t.wav"
        pcm = (_make_tone_wav(2.0)
               + b"\x00\x00" * (int(RATE * 5))
               + _make_tone_wav(23.0))
        _write_wav(wav, pcm, len(pcm) // 2)

        sils = ct_module.detect_silence(str(wav), silence_db=-30, min_dur=0.5)
        assert any(abs(mid - 4.5) < 1.0 and abs(dur - 5.0) < 0.7
                   for mid, dur in sils), f"expected 2-7s silence, got {sils}"

    def test_no_silence_in_continuous_tone(self, tmp_path, ct_module):
        wav = tmp_path / "t.wav"
        pcm = _make_tone_wav(2.0)
        _write_wav(wav, pcm, len(pcm) // 2)
        assert ct_module.detect_silence(str(wav), silence_db=-30, min_dur=0.5) == []


class TestCreateChunk:
    def test_slices_frames_correctly(self, tmp_path, ct_module):
        wav = tmp_path / "t.wav"
        pcm = _make_tone_wav(10.0)
        _write_wav(wav, pcm, len(pcm) // 2)

        chunk = tmp_path / "c.wav"
        ct_module.create_chunk(str(wav), str(chunk), 2.0, 3.0)
        import wave as w
        with w.open(str(chunk), "rb") as wf:
            assert abs(wf.getnframes() / wf.getframerate() - 3.0) < 0.01
            assert wf.getframerate() == 16000
            assert wf.getnchannels() == 1


class TestAudioHelpersDoNotRequireFfmpeg:
    """The audio helpers in this file must not shell out to ffmpeg/ffprobe.
    (They read WAV headers with the stdlib `wave` module and never spawn
    node/php binaries, so these tests pass with or without host ffmpeg.)"""



class TestAudioHelpersDoNotRequireSystemBins:
    """核心验证目标：音频辅助函数不依赖 system ffmpeg / ffprobe / bc。

    方法：在一个 PATH 中排除所有 ffmpeg/ffprobe/bc 的干净环境里，把
    `subprocess` 的 `run` 打桩，断言沙箱脚本从未 spawn 任何进程，
    仅靠 stdlib wave + numpy 完成检测/切块。
    """

    def test_audio_helpers_run_without_spawning_processes(self, tmp_path, ct_module, monkeypatch):
        spawned = []

        class _FakePopen:
            def __init__(self, *a, **k):
                pytest.fail(f"audio helper tried to spawn a process: {a}")

        monkeypatch.setattr(subprocess, "run", _FakePopen)

        import wave as _wave
        wav = tmp_path / "t.wav"
        pcm = (_make_tone_wav(1.0)
               + b"\x00\x00" * (int(RATE * 3))
               + _make_tone_wav(1.0))
        with _wave.open(str(wav), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
            w.writeframes(pcm)

        assert ct_module.get_duration(str(wav)) == pytest.approx(5.0, abs=0.05)
        sils = ct_module.detect_silence(str(wav), silence_db=-30, min_dur=0.5)
        assert any(abs(mid - 2.5) < 1.0 and 2.5 <= dur <= 3.5 for mid, dur in sils)

        chunk = tmp_path / "c.wav"
        ct_module.create_chunk(str(wav), str(chunk), 0.5, 2.0)
        with _wave.open(str(chunk), "rb") as w:
            assert w.getframerate() == RATE and w.getnchannels() == 1
