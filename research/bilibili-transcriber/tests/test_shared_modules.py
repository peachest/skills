"""Tests for shared _conf and _llm modules (architecture deepening: conf/llm client)."""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import _conf
import _llm


# ── _conf.parse_conf_file ──

class TestParseConfFile:
    def test_parses_values_comments_quotes(self, tmp_path):
        rc = tmp_path / "runtime.conf"
        rc.write_text(
            '# comment\n'
            'KEY_A=value-a\n'
            'KEY_B = "quoted val" \n'
            "KEY_C='sq'\n"
            'no-equals-line\n'
            '\n', encoding="utf-8")
        conf = _conf.parse_conf_file(rc)
        assert conf == {"KEY_A": "value-a", "KEY_B": "quoted val", "KEY_C": "sq"}

    def test_missing_file_empty(self, tmp_path):
        assert _conf.parse_conf_file(tmp_path / "nope") == {}


# ── _conf.load_conf ──

class TestLoadConf:
    RC = "BASEURL=https://x.example\nMODEL=m1\nKEY=k1\nOTHER=o\n"

    @pytest.fixture(autouse=True)
    def _setup(self, tmp_path, monkeypatch):
        rc = tmp_path / "runtime.conf"
        rc.write_text(self.RC, encoding="utf-8")
        monkeypatch.setattr(_conf, "CONF_PATH", rc)
        for k in ("BASEURL", "MODEL", "KEY", "OTHER"):
            monkeypatch.delenv(k, raising=False)

    def test_file_fills_required(self):
        conf = _conf.load_conf("BASEURL", "MODEL", keys=("BASEURL", "MODEL", "KEY"))
        assert conf == {"BASEURL": "https://x.example", "MODEL": "m1", "KEY": "k1"}

    def test_env_wins_over_file(self, monkeypatch):
        monkeypatch.setenv("MODEL", "env-model")
        conf = _conf.load_conf("BASEURL", "MODEL")
        assert conf["MODEL"] == "env-model"
        assert conf["BASEURL"] == "https://x.example"

    def test_missing_required_exits(self):
        with pytest.raises(SystemExit, match="MISSING_KEY"):
            _conf.load_conf("BASEURL", "MISSING_KEY")

    def test_no_keys_arg_returns_required_only(self):
        conf = _conf.load_conf("BASEURL")
        assert conf == {"BASEURL": "https://x.example"}


# ── _llm ──

class TestLlmClient:
    def test_chat_url_join(self):
        assert _llm.chat_url("https://x/v1") == "https://x/v1/chat/completions"
        assert _llm.chat_url("https://x/v1/") == "https://x/v1/chat/completions"

    def test_build_headers(self):
        assert _llm.build_headers() == {"Content-Type": "application/json"}
        assert _llm.build_headers("sekrit")["Authorization"] == "Bearer sekrit"

    def test_build_payload_effort_and_extra(self):
        p = _llm.build_payload("m", [], temperature=0.5, extra={"frequency_penalty": 0.3},
                               effort="low")
        assert p["chat_template_kwargs"] == {"reasoning_effort": "low"}
        assert p["frequency_penalty"] == 0.3
        assert "chat_template_kwargs" not in _llm.build_payload("m", [])

    def test_strip_fence(self):
        # faithful to the original clean-transcripts behavior: strip("`") both ends
        assert _llm.strip_fence("```\nbody\n```") == "body\n"
        assert _llm.strip_fence("plain") == "plain"

    @staticmethod
    def _fake_sess(responses):
        """responses: list of (status, content) or Exception per call."""
        calls = []

        class _Resp:
            def __init__(self, pair):
                self.status, self._content = pair

            async def text(self):
                return "server error"

            async def json(self):
                return {"choices": [{"message": {"content": self._content}}]}

            async def __aenter__(self):
                return self

            async def __aexit__(self, *exc):
                return False

        class _Sess:
            def post(self, url, **kwargs):
                calls.append({"url": url, **kwargs})
                r = responses.pop(0)
                if isinstance(r, Exception):
                    raise r
                return _Resp(r)

        return _Sess(), calls

    @staticmethod
    def _no_sleep(monkeypatch):
        async def _sleep(_s):
            pass
        monkeypatch.setattr(_llm.asyncio, "sleep", _sleep)

    def test_chat_success_retries_then_succeeds(self, monkeypatch):
        # 2 failures then success — ladder must keep going
        sleeps = []
        async def _sleep(s):
            sleeps.append(s)
        monkeypatch.setattr(_llm.asyncio, "sleep", _sleep)
        fails = [RuntimeError("boom"), RuntimeError("boom2")]
        sess, calls = self._fake_sess(fails + [(200, "ok")])
        out = asyncio.run(_llm.chat(
            sess, baseurl="https://x/v1", model="m", messages=[{"role": "user", "content": "hi"}]))
        assert out == "ok"
        assert len(calls) == 3
        assert sleeps == [2, 4]  # linear backoff
        assert calls[0]["url"] == "https://x/v1/chat/completions"
        assert calls[0]["headers"]["Content-Type"] == "application/json"

    def test_chat_raises_after_last_attempt(self, monkeypatch):
        self._no_sleep(monkeypatch)
        sess, calls = self._fake_sess([RuntimeError("down")] * 3)
        with pytest.raises(RuntimeError, match="down"):
            asyncio.run(_llm.chat(sess, baseurl="https://x", model="m", messages=[]))
        assert len(calls) == 3

    def test_chat_http_error_includes_body(self, monkeypatch):
        self._no_sleep(monkeypatch)
        sess, _ = self._fake_sess([(500, "")])
        with pytest.raises(RuntimeError, match="HTTP 500"):
            asyncio.run(_llm.chat(sess, baseurl="https://x", model="m", messages=[], retries=1))

    def test_chat_bearer_and_effort_reach_wire(self):
        sess, calls = self._fake_sess([(200, "```\ncleaned\n```")])
        out = asyncio.run(_llm.chat(
            sess, baseurl="https://x", model="m", key="kk",
            messages=[{"role": "user", "content": "hi"}], effort="low"))
        assert out == "cleaned\n"  # fence stripped (original semantics: trailing newline kept)
        assert calls[0]["headers"]["Authorization"] == "Bearer kk"
        assert calls[0]["json"]["chat_template_kwargs"] == {"reasoning_effort": "low"}

    def test_chat_vision_payload_passthrough(self):
        """Vision = caller puts image_url in messages; client must not touch content."""
        msgs = [{"role": "user", "content": [
            {"type": "text", "text": "ocr this"},
            {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,QUJD"}}]}]
        sess, calls = self._fake_sess([(200, "[非幻灯片]")])
        out = asyncio.run(_llm.chat(sess, baseurl="https://x", model="v", messages=msgs))
        assert out == "[非幻灯片]"
        assert calls[0]["json"]["messages"] == msgs


class TestLogChange:
    def test_appends_jsonl(self, tmp_path):
        _llm.log_change(tmp_path, script="clean", item="chunk-1", raw="abcd",
                        out="ab", used_fallback=False)
        _llm.log_change(tmp_path, script="clean", item="chunk-2", raw="xyz",
                        out="wxyz")
        lines = (tmp_path / "llm-changes.jsonl").read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2
        r1 = json.loads(lines[0])
        assert r1["script"] == "clean" and r1["item"] == "chunk-1"
        assert r1["raw_len"] == 4 and r1["out_len"] == 2 and r1["ratio"] == 0.5
        assert "ts" in r1

    def test_failure_non_fatal(self, tmp_path, monkeypatch):
        # unwritable target must not raise
        monkeypatch.setattr(Path, "mkdir", lambda *a, **k: (_ for _ in ()).throw(OSError("ro")))
        _llm.log_change(tmp_path / "sub", script="s", item="i", raw="a", out="b")  # no raise
