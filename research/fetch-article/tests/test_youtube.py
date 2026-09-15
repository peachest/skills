"""YouTube adapter tests: VTT parsing, id extraction, routing, and a
mocked end-to-end fetch (subtitle path + audio fallback). No network."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from adapters import youtube


class TestExtractVideoId:
    @pytest.mark.parametrize("url,vid", [
        ("https://www.youtube.com/watch?v=7zZy1QTvokM", "7zZy1QTvokM"),
        ("https://youtu.be/7zZy1QTvokM", "7zZy1QTvokM"),
        ("https://www.youtube.com/shorts/7zZy1QTvokM", "7zZy1QTvokM"),
        ("https://www.youtube.com/watch?v=7zZy1QTvokM&t=30s", "7zZy1QTvokM"),
    ])
    def test_urls(self, url, vid):
        assert youtube._extract_video_id(url) == vid

    def test_invalid_url_raises(self):
        with pytest.raises(ValueError):
            youtube._extract_video_id("https://example.com/no-id")


class TestVttToText:
    def test_dedup_and_tag_strip(self, tmp_path):
        vtt = tmp_path / "test.en-orig.vtt"
        vtt.write_text(
            "WEBVTT\nKind: captions\nLanguage: en\n\n"
            "00:00:00.000 --> 00:00:02.000\n"
            "Hello <00:00:00.319><c> world</c>\n\n"
            "00:00:01.500 --> 00:00:03.000\n"
            "Hello world\n\n"           # rolling-window repeat
            "00:00:02.000 --> 00:00:04.000\n"
            "this is\na test\n\n"
            "1\n00:00:04.000 --> 00:00:05.000\n"  # cue number line
            "done\n", encoding="utf-8")
        assert youtube._vtt_to_text(str(vtt)) == "Hello world this is a test done"


class TestPickSubtitle:
    def test_prefers_manual_over_auto(self, tmp_path):
        (tmp_path / "abc12345678.en-orig.vtt").write_text("a", encoding="utf-8")
        manual = tmp_path / "abc12345678.en.vtt"
        manual.write_text("b", encoding="utf-8")
        assert youtube._pick_subtitle(str(tmp_path), "abc12345678") == str(manual)

    def test_none_when_absent(self, tmp_path):
        assert youtube._pick_subtitle(str(tmp_path), "abc12345678") is None


class TestProxyArgs:
    def test_forwarded_when_set(self, monkeypatch):
        monkeypatch.setenv("https_proxy", "http://p:3128")
        assert youtube._proxy_args() == ["--proxy", "http://p:3128"]

    def test_omitted_when_unset(self, monkeypatch):
        for v in youtube.PROXY_ENV_VARS:
            monkeypatch.delenv(v, raising=False)
        assert youtube._proxy_args() == []


VID = "7zZy1QTvokM"
INFO = {"title": "Test Video", "channel": "Chan", "upload_date": "20260609",
        "duration": 798, "description": "desc text"}


def _mock_ytdlp(info_json: dict, write_vtt: bool, audio_ok: bool = True):
    """Fake subprocess.run implementing enough of yt-dlp's file outputs."""
    def fake_run(args, **kwargs):
        if "--write-info-json" in args:
            outdir = os.path.dirname(args[args.index("-o") + 1])
            with open(os.path.join(outdir, f"{VID}.info.json"), "w") as f:
                json.dump(info_json, f)
            if write_vtt:
                with open(os.path.join(outdir, f"{VID}.en-orig.vtt"), "w") as f:
                    f.write("WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nhello\n")
            class R: returncode = 0; stderr = ""
            return R()
        if "-f" in args:  # audio download
            if audio_ok:
                with open(args[args.index("-o") + 1], "wb") as f:
                    f.write(b"x" * 100)
            class R2: returncode = 0 if audio_ok else 1; stderr = ""
            return R2()
        raise AssertionError(f"unexpected args: {args}")
    return fake_run


class TestFetch:
    def test_subtitle_path_skips_audio(self, tmp_path):
        with patch.object(youtube.subprocess, "run",
                          side_effect=_mock_ytdlp(INFO, write_vtt=True)):
            r = youtube.fetch(f"https://youtu.be/{VID}", output_dir=str(tmp_path))
        assert r["has_subtitles"] is True
        assert r["audio_path"] is None
        assert r["stream_type"] == "subtitle_only"
        assert r["body_text"] == "hello"
        assert r["duration_sec"] == 798
        meta = json.loads((tmp_path / "metadata.json").read_text())
        assert meta["stream_type"] == "subtitle_only"

    def test_no_subtitle_downloads_audio(self, tmp_path):
        with patch.object(youtube.subprocess, "run",
                          side_effect=_mock_ytdlp(INFO, write_vtt=False)):
            r = youtube.fetch(f"https://youtu.be/{VID}", output_dir=str(tmp_path))
        assert r["has_subtitles"] is False
        assert r["stream_type"] == "audio_only"
        assert r["content_length"] == 100
        assert r["body_text"] == "desc text"

    def test_audio_failure_raises(self, tmp_path):
        with patch.object(youtube.subprocess, "run",
                          side_effect=_mock_ytdlp(INFO, write_vtt=False,
                                                  audio_ok=False)):
            with pytest.raises(RuntimeError, match="audio download failed"):
                youtube.fetch(f"https://youtu.be/{VID}", output_dir=str(tmp_path))


class TestRouting:
    def test_classify(self):
        sys.path.insert(0, str(SCRIPTS_DIR))
        import fetch
        assert fetch.classify_url("https://www.youtube.com/watch?v=7zZy1QTvokM") == "youtube"
        assert fetch.classify_url("https://youtu.be/7zZy1QTvokM") == "youtube"
        assert fetch.classify_url("https://www.bilibili.com/video/BV1xx/") == "bilibili"
        assert fetch.classify_url("https://example.com/a") == "generic"
