"""Seam 2 test: transcode.sh -vn regression guard + no system ffmpeg.

Generates a video+audio fixture mp4 WITHOUT relying on a system ffmpeg
(uses the static binary bundled with the imageio-ffmpeg pip package when
available, else skips), runs transcode.sh, and asserts the output WAV is
non-empty, 16 kHz, mono.

Also verifies transcode.sh itself does not shell out to `ffprobe`/`ffmpeg`
from PATH: it derives the binary via imageio_ffm ( and reads duration from
the WAV header with the stdlib `wave` module.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import wave
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
TRANSCODE_SH = SCRIPTS_DIR / "transcode.sh"


def _ffmpeg_bin() -> str | None:
    """Locate ffmpeg: imageio_ffmpeg static binary first, then PATH."""
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    return shutil.which("ffmpeg")


def _generate_fixture_mp4(path: Path):
    """Generate a 1-second video+audio fixture mp4 via the resolved binary."""
    ff = _ffmpeg_bin()
    if not ff:
        pytest.skip("no ffmpeg binary available (neither imageio_ffmpeg nor PATH)")
    cmd = [ff, "-y",
           "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
           "-f", "lavfi", "-i", "color=c=red:s=320x240:d=1",
           "-c:a", "aac", "-c:v", "libx264",
           "-shortest", str(path)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        pytest.fail(f"fixture generation failed: {result.stderr}")


def _run_transcode(input_file: Path, output_wav: Path, env=None) -> subprocess.CompletedProcess:
    """Run transcode.sh on input, producing output_wav."""
    return subprocess.run(
        ["bash", str(TRANSCODE_SH), str(input_file), str(output_wav)],
        capture_output=True, text=True, timeout=60, env=env,
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

        assert output_wav.exists(), "output WAV was not created"
        assert os.path.getsize(output_wav) > 0, "output WAV is empty"

        with wave.open(str(output_wav), "rb") as wf:
            framerate = wf.getframerate()
            nchannels = wf.getnchannels()
            nframes = wf.getnframes()

        assert framerate == 16000, f"expected 16kHz, got {framerate}Hz"
        assert nchannels == 1, f"expected mono, got {nchannels} channels"

        duration = nframes / framerate
        assert 0.8 <= duration <= 1.2, f"expected ~1s duration, got {duration:.2f}s"

    def test_regression_guard_vn_is_present(self):
        """Verify that transcode.sh contains -vn (the regression guard)."""
        content = TRANSCODE_SH.read_text()
        assert "-vn" in content, (
            "transcode.sh is missing -vn flag — without it, video+audio "
            "inputs trigger AAC decode errors"
        )


class TestNoSystemFfmpeg:
    """transcode.sh must not require a system ffmpeg/ffprobe on PATH."""

    def test_script_does_not_call_ffprobe(self):
        """transcode.sh gets duration from the WAV header, not ffprobe."""
        content = TRANSCODE_SH.read_text()
        assert "ffprobe" not in content, (
            "transcode.sh must not depend on ffprobe — duration is read from "
            "the WAV header via the stdlib wave module"
        )

    def test_works_without_ffmpeg_on_path(self, tmp_path):
        """Runs when PATH has neither ffmpeg nor ffprobe (imageio_ffmpeg only)."""
        ff = _ffmpeg_bin()
        if not ff:
            pytest.skip("no ffmpeg binary available (neither imageio_ffmpeg nor PATH)")

        fixture = tmp_path / "fixture.mp4"
        output_wav = tmp_path / "audio.wav"
        _generate_fixture_mp4(fixture)

        # A PATH with python3 but no ffmpeg/ffprobe — emulate a host without
        # system ffmpeg installed.
        python3 = shutil.which("python3")
        assert python3, "python3 required"
        clean_path = os.path.dirname(python3)
        env = dict(os.environ)
        env["PATH"] = clean_path

        result = _run_transcode(fixture, output_wav, env=env)
        assert result.returncode == 0, (
            f"transcode.sh should work with imageio_ffmpeg only: {result.stderr}"
        )
        with wave.open(str(output_wav), "rb") as wf:
            assert wf.getframerate() == 16000
            assert wf.getnchannels() == 1

        # Duration line on stdout must be numeric (WAV header, no ffprobe)
        lines = result.stdout.strip().splitlines()
        assert len(lines) == 3, f"expected 3 stdout lines, got: {result.stdout!r}"
        assert float(lines[2]) > 0, f"duration should be > 0: {lines[2]}"