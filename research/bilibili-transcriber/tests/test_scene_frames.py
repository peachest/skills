"""Adaptive scene-threshold retry + frame-write discipline guards.

The 2026-10-20 incident: commit fcb6568 set the default scene threshold to
0.3, which cuts only 1 frame on low-transition lecture videos (the 12-frame
run the user saw came from the pre-commit working tree). No test caught the
regression; this file pins the retry logic and the frames-dir write shape.
"""

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest


def load(name):
    script = Path(__file__).parent.parent / "scripts" / name
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_").replace(".py", ""), script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


se = load("slides-extract.py")


# ── adaptive retry logic (extract_frames/ffprobe_duration monkeypatched) ──

def _patch(monkeypatch, cuts_per_threshold, duration):
    calls = []

    def fake_extract(video, out_dir, threshold):
        calls.append(threshold)
        return [{"file": f"frame_{i:03d}.jpg", "time_sec": i}
                for i in range(cuts_per_threshold.get(threshold, 0))]

    monkeypatch.setattr(se, "extract_frames", fake_extract)
    monkeypatch.setattr(se, "ffprobe_duration", lambda video: duration)
    return calls


def test_retry_when_few_cuts_in_long_video(monkeypatch, tmp_path):
    calls = _patch(monkeypatch, {0.3: 1, 0.15: 11}, duration=351)
    frames = se.extract_frames_adaptive(tmp_path / "v.mp4", tmp_path, 0.3)
    assert calls == [0.3, 0.15]
    assert len(frames) == 11


def test_no_retry_in_short_video(monkeypatch, tmp_path):
    calls = _patch(monkeypatch, {0.3: 1}, duration=60)
    se.extract_frames_adaptive(tmp_path / "v.mp4", tmp_path, 0.3)
    assert calls == [0.3]


def test_no_retry_when_enough_cuts(monkeypatch, tmp_path):
    calls = _patch(monkeypatch, {0.3: 5}, duration=351)
    frames = se.extract_frames_adaptive(tmp_path / "v.mp4", tmp_path, 0.3)
    assert calls == [0.3]
    assert len(frames) == 5


def test_retry_still_few_cuts_is_final(monkeypatch, tmp_path):
    # retry result returned as-is — no infinite loop
    calls = _patch(monkeypatch, {0.3: 1, 0.15: 1}, duration=351)
    frames = se.extract_frames_adaptive(tmp_path / "v.mp4", tmp_path, 0.3)
    assert calls == [0.3, 0.15]
    assert len(frames) == 1


# ── real ffmpeg integration: frame-write discipline (leak guard) ──

def _ffmpeg_bin():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        import shutil
        return shutil.which("ffmpeg")


def test_extract_frames_writes_only_frame_prefix(tmp_path):
    """extract_frames only writes frame_*.jpg into frames_dir — the old
    scene_*.jpg every-frame leak (8280 files / 916MB in one workspace) must
    never come back."""
    ff = _ffmpeg_bin()
    if not ff:
        pytest.skip("no ffmpeg binary available")
    video = tmp_path / "v.mp4"
    r = subprocess.run(
        [ff, "-y", "-f", "lavfi", "-i", "color=c=red:s=64x64:d=2", "-c:v", "libx264",
         str(video)], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr

    frames = se.extract_frames(video, tmp_path, 0.3)
    assert frames, "t=0 frame must always be kept"
    produced = [p.name for p in (tmp_path / "frames").iterdir()]
    assert produced, "frames dir must not be empty"
    assert all(name.startswith("frame_") and name.endswith(".jpg")
               for name in produced), f"non-frame file leaked: {produced}"
