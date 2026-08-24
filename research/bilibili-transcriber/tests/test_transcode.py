"""Seam 2 test: transcode.sh -vn regression guard.

Generates a video+audio fixture mp4 in-test via ffmpeg, runs transcode.sh,
and asserts the output WAV is non-empty, 16 kHz, mono, with correct duration.

Regression guard: without -vn in transcode.sh, the video stream triggers
AAC channel decode errors and produces an empty/short WAV.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
import wave
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
TRANSCODE_SH = SCRIPTS_DIR / "transcode.sh"

FIXTURE_CMD = [
    "ffmpeg", "-y",
    "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
    "-f", "lavfi", "-i", "color=c=red:s=320x240:d=1",
    "-c:a", "aac", "-c:v", "libx264",
    "-shortest",
]


def _generate_fixture_mp4(path: Path):
    """Generate a 1-second video+audio fixture mp4."""
    result = subprocess.run(
        FIXTURE_CMD + [str(path)],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        pytest.fail(f"ffmpeg fixture generation failed: {result.stderr}")


def _run_transcode(input_file: Path, output_wav: Path) -> subprocess.CompletedProcess:
    """Run transcode.sh on input, producing output_wav."""
    return subprocess.run(
        ["bash", str(TRANSCODE_SH), str(input_file), str(output_wav)],
        capture_output=True, text=True, timeout=30,
    )


class TestTranscodeVn:
    """Test that transcode.sh produces correct WAV with -vn."""

    def test_produces_valid_wav_from_video_audio_fixture(self, tmp_path):
        """transcode.sh on a video+audio mp4 produces a valid 16kHz mono WAV."""
        fixture = tmp_path / "fixture.mp4"
        output_wav = tmp_path / "audio.wav"

        _generate_fixture_mp4(fixture)
        assert fixture.exists(), "fixture mp4 was not generated"

        result = _run_transcode(fixture, output_wav)
        assert result.returncode == 0, f"transcode.sh failed: {result.stderr}"

        # Assert WAV exists and is non-empty
        assert output_wav.exists(), "output WAV was not created"
        assert os.path.getsize(output_wav) > 0, "output WAV is empty"

        # Inspect WAV with stdlib wave module
        with wave.open(str(output_wav), "rb") as wf:
            framerate = wf.getframerate()
            nchannels = wf.getnchannels()
            nframes = wf.getnframes()

        assert framerate == 16000, f"expected 16kHz, got {framerate}Hz"
        assert nchannels == 1, f"expected mono, got {nchannels} channels"

        # Duration should be ~1 second (fixture is 1s), within tolerance
        duration = nframes / framerate
        assert 0.8 <= duration <= 1.2, f"expected ~1s duration, got {duration:.2f}s"

    def test_regression_guard_vn_is_present(self, tmp_path):
        """Verify that transcode.sh contains -vn (the regression guard).

        Without -vn, a video+audio input triggers AAC channel decode errors.
        This test asserts the flag is present so the guard is not accidentally
        removed.
        """
        content = TRANSCODE_SH.read_text()
        assert "-vn" in content, (
            "transcode.sh is missing -vn flag — without it, video+audio "
            "inputs trigger AAC decode errors"
        )
