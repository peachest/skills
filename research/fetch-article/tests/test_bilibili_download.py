"""Seam 1 tests: fetch-article bilibili adapter download engine.

Mocks requests.Session (API calls) and subprocess.run (aria2c download).
No live network calls.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
FIXTURES_DIR = Path(__file__).parent / "fixtures"

# Add scripts dir to path for adapter import
import sys
sys.path.insert(0, str(SCRIPTS_DIR))

from adapters import bilibili


def _load_fixture(name: str) -> dict:
    with open(FIXTURES_DIR / name) as f:
        return json.load(f)


class _FakeResponse:
    """Fake requests.Response for mocking session.get."""

    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json

    def raise_for_status(self):
        pass


def _make_mock_session(playurl_fixture="playurl.json"):
    """Create a mock requests.Session that returns fixture data for API calls."""
    session = MagicMock()
    nav = _load_fixture("nav.json")
    view = _load_fixture("view.json")
    playurl = _load_fixture(playurl_fixture)
    player_v2 = _load_fixture("player_v2.json")

    def get_side_effect(url, *args, **kwargs):
        if "nav" in url:
            return _FakeResponse(nav)
        if "view" in url:
            return _FakeResponse(view)
        if "playurl" in url:
            return _FakeResponse(playurl)
        if "player" in url:
            return _FakeResponse(player_v2)
        return _FakeResponse({})

    session.get.side_effect = get_side_effect
    return session


def _make_mock_subprocess_success(payload_size: int):
    """Return a MagicMock replacing the subprocess module.

    .run writes a fake payload to the output path and returns exit 0.
    .CompletedProcess is preserved for constructing return values.
    """
    mock = MagicMock()

    def fake_run(args, **kwargs):
        # Detect aria2c calls (have -d and -o) vs ffmpeg calls (have -f concat)
        if "-f" in args and "concat" in args:
            # ffmpeg concat: read list.txt, concatenate segment files
            list_idx = args.index("-i") + 1
            list_path = args[list_idx]
            out_idx = args.index("-c")  # -c copy <output> comes after -c
            # output is the last arg
            out_path = args[-1]
            with open(list_path) as f:
                lines = f.read().strip().split("\n")
            seg_dir = os.path.dirname(list_path)
            combined = b""
            for line in lines:
                # parse file 'segment_X.m4s'
                seg_name = line.split("'")[1]
                seg_path = os.path.join(seg_dir, seg_name)
                with open(seg_path, "rb") as sf:
                    combined += sf.read()
            with open(out_path, "wb") as f:
                f.write(combined)
            return subprocess.CompletedProcess(
                args=args, returncode=0, stdout="", stderr="")
        # aria2c call
        dir_idx = args.index("-d") + 1
        out_dir = args[dir_idx]
        name_idx = args.index("-o") + 1
        out_name = args[name_idx]
        out_path = os.path.join(out_dir, out_name)
        with open(out_path, "wb") as f:
            f.write(b"\x00" * payload_size)
        return subprocess.CompletedProcess(
            args=args, returncode=0, stdout="", stderr="")

    mock.run = MagicMock(side_effect=fake_run)
    mock.CompletedProcess = subprocess.CompletedProcess
    return mock


class TestAria2cDownload:
    """Test aria2c download engine, completeness, and workspace."""

    def test_successful_download_writes_content_length(self, tmp_path):
        """aria2c writes N bytes + exits 0 → content_length == N."""
        output_dir = str(tmp_path)
        fake_size = 27862695

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session", return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            result = bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/",
                output_dir=output_dir)

        assert result["content_length"] == fake_size
        audio_path = os.path.join(output_dir, "audio.mp4")
        assert os.path.getsize(audio_path) == fake_size

    def test_aria2c_failure_raises_error(self, tmp_path):
        """aria2c exits non-zero → adapter raises RuntimeError."""
        output_dir = str(tmp_path)

        mock_subprocess = MagicMock()
        mock_subprocess.run = MagicMock(return_value=subprocess.CompletedProcess(
            args=[], returncode=1, stdout="", stderr="Download failed"))
        mock_subprocess.CompletedProcess = subprocess.CompletedProcess

        with patch.object(bilibili, "_make_session", return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            with pytest.raises(RuntimeError, match="aria2c download failed"):
                bilibili.fetch(
                    "https://www.bilibili.com/video/BV1TestBVID01/",
                    output_dir=output_dir)

    def test_empty_download_raises_error(self, tmp_path):
        """aria2c exits 0 but writes 0 bytes → adapter raises RuntimeError."""
        output_dir = str(tmp_path)

        mock_subprocess = _make_mock_subprocess_success(0)
        with patch.object(bilibili, "_make_session", return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            with pytest.raises(RuntimeError, match="Downloaded file is empty"):
                bilibili.fetch(
                    "https://www.bilibili.com/video/BV1TestBVID01/",
                    output_dir=output_dir)

    def test_deterministic_workspace_same_bvid(self, tmp_path, monkeypatch):
        """Two fetch() calls for same BVID (no output_dir) → same workspace."""
        # Redirect ~/.cache to tmp_path
        monkeypatch.setenv("HOME", str(tmp_path))
        fake_size = 1000

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session", return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            bvid = "BV1TestBVID01"
            result1 = bilibili.fetch(
                f"https://www.bilibili.com/video/{bvid}/")
            audio_path1 = result1["audio_path"]

            result2 = bilibili.fetch(
                f"https://www.bilibili.com/video/{bvid}/")
            audio_path2 = result2["audio_path"]

        assert audio_path1 == audio_path2
        # Verify aria2c was called with --continue=true both times
        assert mock_subprocess.run.call_count == 2
        for call in mock_subprocess.run.call_args_list:
            args = call[0][0]
            assert "--continue=true" in args

    def test_different_bvid_different_workspace(self, tmp_path, monkeypatch):
        """Different BVID → different workspace directory."""
        monkeypatch.setenv("HOME", str(tmp_path))
        fake_size = 1000

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session", return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            result1 = bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/")
            result2 = bilibili.fetch(
                "https://www.bilibili.com/video/BV1OtherBVID2/")

        assert result1["audio_path"] != result2["audio_path"]
        # Different parent directories
        assert Path(result1["audio_path"]).parent != Path(result2["audio_path"]).parent

    def test_metadata_json_has_content_length(self, tmp_path):
        """metadata.json contains content_length field."""
        output_dir = str(tmp_path)
        fake_size = 5000

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session", return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/",
                output_dir=output_dir)

        meta_path = os.path.join(output_dir, "metadata.json")
        with open(meta_path) as f:
            meta = json.load(f)
        assert meta["content_length"] == fake_size
        # Existing fields preserved
        assert "bvid" in meta
        assert "title" in meta
        assert "audio_path" in meta

    def test_proxy_passed_when_set(self, tmp_path, monkeypatch):
        """https_proxy env var → --all-proxy in aria2c args."""
        output_dir = str(tmp_path)
        monkeypatch.setenv("https_proxy", "http://172.16.80.252:3128")
        fake_size = 100

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session", return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/",
                output_dir=output_dir)

        args = mock_subprocess.run.call_args[0][0]
        assert "--all-proxy=http://172.16.80.252:3128" in args

    def test_proxy_omitted_when_unset(self, tmp_path, monkeypatch):
        """No https_proxy → no --all-proxy in aria2c args."""
        output_dir = str(tmp_path)
        monkeypatch.delenv("https_proxy", raising=False)
        monkeypatch.delenv("HTTPS_PROXY", raising=False)
        fake_size = 100

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session", return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/",
                output_dir=output_dir)

        args = mock_subprocess.run.call_args[0][0]
        assert not any(a.startswith("--all-proxy") for a in args)

    def test_aria2c_args_include_referer_and_ua(self, tmp_path):
        """aria2c args must include Referer and User-Agent headers."""
        output_dir = str(tmp_path)
        fake_size = 100

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session", return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/",
                output_dir=output_dir)

        args = mock_subprocess.run.call_args[0][0]
        assert any("Referer: https://www.bilibili.com/" in a for a in args)
        assert any("User-Agent:" in a for a in args)


class TestStreamSelection:
    """Test DASH-first stream selection, durl fallback, and stream_type metadata."""

    def test_dash_audio_selected_first(self, tmp_path):
        """Fixture with both durl and dash.audio → picks DASH (lowest bandwidth)."""
        output_dir = str(tmp_path)
        fake_size = 5000

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session",
                          return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            result = bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/",
                output_dir=output_dir)

        assert result["stream_type"] == "dash_audio"
        # Verify aria2c got the lowest-bandwidth DASH URL (bandwidth=65553)
        aria2c_calls = [c for c in mock_subprocess.run.call_args_list
                        if "-d" in c[0][0]]
        assert len(aria2c_calls) == 1
        url = aria2c_calls[0][0][0][-1]
        assert "test-dash-low" in url

    def test_playurl_params_include_fnval_and_pc(self, tmp_path):
        """Playurl request params must include fnval=16, platform=pc."""
        output_dir = str(tmp_path)
        fake_size = 100

        mock_session = _make_mock_session()
        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session", return_value=mock_session), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/",
                output_dir=output_dir)

        # Find the playurl call in mock session.get calls
        playurl_call = None
        for call in mock_session.get.call_args_list:
            url = call[0][0] if call[0] else call[1].get("url", "")
            if "playurl" in str(url):
                playurl_call = call
                break
        assert playurl_call is not None, "playurl API call not found"
        params = playurl_call[1].get("params", {})
        assert params.get("fnval") == 16
        assert params.get("platform") == "pc"
        assert params.get("qn") == 0

    def test_durl_fallback_when_no_dash(self, tmp_path):
        """Fixture with only durl (no dash) → downloads durl, stream_type=durl_video."""
        output_dir = str(tmp_path)
        fake_size = 3000

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session",
                          return_value=_make_mock_session("playurl_durl_only.json")), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            result = bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/",
                output_dir=output_dir)

        assert result["stream_type"] == "durl_video"
        # Only one aria2c call (single durl segment)
        aria2c_calls = [c for c in mock_subprocess.run.call_args_list
                        if "-d" in c[0][0]]
        assert len(aria2c_calls) == 1

    def test_multi_segment_durl_concat(self, tmp_path):
        """Fixture with 2 durl segments → downloaded, concatenated via ffmpeg."""
        output_dir = str(tmp_path)
        fake_size = 2000

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session",
                          return_value=_make_mock_session("playurl_multi.json")), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            result = bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/",
                output_dir=output_dir)

        assert result["stream_type"] == "durl_video"
        # 2 aria2c calls (2 segments) + 1 ffmpeg concat call
        aria2c_calls = [c for c in mock_subprocess.run.call_args_list
                        if "-d" in c[0][0]]
        ffmpeg_calls = [c for c in mock_subprocess.run.call_args_list
                        if "-f" in c[0][0] and "concat" in c[0][0]]
        assert len(aria2c_calls) == 2
        assert len(ffmpeg_calls) == 1
        # Final audio.mp4 should exist and be non-empty (2 segments × fake_size)
        assert os.path.getsize(result["audio_path"]) == fake_size * 2
        # Segments and list.txt should be cleaned up
        assert not os.path.exists(os.path.join(output_dir, "segment_0.m4s"))
        assert not os.path.exists(os.path.join(output_dir, "list.txt"))

    def test_stream_type_in_metadata_json(self, tmp_path):
        """metadata.json contains stream_type field."""
        output_dir = str(tmp_path)
        fake_size = 1000

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session",
                          return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/",
                output_dir=output_dir)

        meta_path = os.path.join(output_dir, "metadata.json")
        with open(meta_path) as f:
            meta = json.load(f)
        assert meta["stream_type"] == "dash_audio"


class TestMultiPageSelection:
    """Test ?p=N page selection and per-page cid/duration."""

    def test_default_selects_page_1(self, tmp_path):
        """No ?p= → defaults to page 1, duration_sec = page-1 duration (not sum)."""
        output_dir = str(tmp_path)
        fake_size = 1000

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session",
                          return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            result = bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/",
                output_dir=output_dir)

        assert result["duration_sec"] == 991  # page-1 duration, not 2130 (sum)
        assert result["page"] == 1
        assert result["page_count"] == 2

    def test_p2_selects_page_2(self, tmp_path):
        """?p=2 → selects page 2's cid and duration."""
        output_dir = str(tmp_path)
        fake_size = 1000

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session",
                          return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            result = bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/?p=2",
                output_dir=output_dir)

        assert result["duration_sec"] == 1139  # page-2 duration
        assert result["page"] == 2
        assert result["page_count"] == 2

    def test_page_fields_in_metadata(self, tmp_path):
        """metadata.json contains page and page_count fields."""
        output_dir = str(tmp_path)
        fake_size = 500

        mock_subprocess = _make_mock_subprocess_success(fake_size)
        with patch.object(bilibili, "_make_session",
                          return_value=_make_mock_session()), \
             patch.object(bilibili, "subprocess", mock_subprocess):

            bilibili.fetch(
                "https://www.bilibili.com/video/BV1TestBVID01/?p=2",
                output_dir=output_dir)

        meta_path = os.path.join(output_dir, "metadata.json")
        with open(meta_path) as f:
            meta = json.load(f)
        assert meta["page"] == 2
        assert meta["page_count"] == 2
        assert meta["duration_sec"] == 1139
