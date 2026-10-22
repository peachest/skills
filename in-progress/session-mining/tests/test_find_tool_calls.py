"""Fixture session jsonl — generic data only (no internal hosts/paths)."""

import json
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def entry(eType, msg=None, **kw):
    e = {"type": eType, **kw}
    if msg is not None:
        e["message"] = msg
    return json.dumps(e, ensure_ascii=False)


def call_block(cid, name, arguments):
    return {"type": "toolCall", "id": cid, "name": name, "arguments": arguments}


def assistant_msg(blocks, **msg_kw):
    return {"role": "assistant", "content": blocks, **msg_kw}


def tool_result(cid, name, text, is_error=False):
    return {"role": "toolResult", "toolCallId": cid, "toolName": name,
            "content": [{"type": "text", "text": text}], "isError": is_error,
            "timestamp": 1789000000000}


@pytest.fixture
def session_file(tmp_path):
    """A sessions dir containing one session with 3 bash calls + 1 other-tool call."""
    lines = [
        entry("session", id="sess-1", timestamp="2026-09-10T10:00:00Z", cwd="/proj"),
        # call 1: glab api, succeeds
        entry("message", assistant_msg([call_block("c1", "bash", {"command": "glab api projects -ojson"})]),
              timestamp="2026-09-10T10:00:01Z"),
        entry("message", tool_result("c1", "bash", "[{...projects...}]"), timestamp="2026-09-10T10:00:02Z"),
        # call 2: glab api, fails
        entry("message", assistant_msg([call_block("c2", "bash", {"command": "glab api mr 1 -X PUT --input body.json"})]),
              timestamp="2026-09-10T10:01:00Z"),
        entry("message", tool_result("c2", "bash", "Command exited with code 1", is_error=True),
              timestamp="2026-09-10T10:01:01Z"),
        # call 3: unrelated bash command, fails
        entry("message", assistant_msg([call_block("c3", "bash", {"command": "ls missing-dir"})]),
              timestamp="2026-09-10T10:02:00Z"),
        entry("message", tool_result("c3", "bash", "ls: cannot access 'missing-dir': No such file or directory\nCommand exited with code 2", is_error=True),
              timestamp="2026-09-10T10:02:01Z"),
        # call 4: other tool, ignored
        entry("message", assistant_msg([call_block("c4", "read", {"path": "/proj/x.md"})]),
              timestamp="2026-09-10T10:03:00Z"),
        entry("message", tool_result("c4", "read", "file content"), timestamp="2026-09-10T10:03:01Z"),
        # malformed line, must be skipped
        "{not json",
    ]
    d = tmp_path / "slug"
    d.mkdir()
    f = d / "2026-09-10T10-00-00Z_sess-1.jsonl"
    f.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return tmp_path, f


def run_script(monkeypatch, capsys, argv):
    import importlib.util
    spec = importlib.util.spec_from_file_location("find_tool_calls", SCRIPTS / "find-tool-calls.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monkeypatch.setattr("sys.argv", ["find-tool-calls.py"] + argv)
    try:
        mod.main()
    except SystemExit as e:
        assert e.code in (0, None), f"unexpected exit {e.code}"
    return json.loads(capsys.readouterr().out)


class TestSearch:
    def test_basic_counts(self, monkeypatch, capsys, session_file):
        tmp, _ = session_file
        out = run_script(monkeypatch, capsys, ["bash", "--sessions-dir", str(tmp)])
        assert out["matches"] == 1
        s = out["sessions"][0]
        assert s["tool_total_calls"] == 3
        assert s["matched_calls"] == 3
        assert s["matched_errors"] == 2
        assert s["last_match_error"] is True

    def test_args_contains_filters_calls(self, monkeypatch, capsys, session_file):
        tmp, _ = session_file
        out = run_script(monkeypatch, capsys, ["bash", "--args-contains", "glab api", "--sessions-dir", str(tmp)])
        s = out["sessions"][0]
        assert s["tool_total_calls"] == 3  # totals still count all bash calls
        assert s["matched_calls"] == 2
        assert s["matched_errors"] == 1
        assert "code 1" in s["sample_error_texts"][0]

    def test_errors_only(self, monkeypatch, capsys, session_file):
        tmp, _ = session_file
        out = run_script(monkeypatch, capsys, ["bash", "--args-contains", "glab api",
                                               "--errors-only", "--sessions-dir", str(tmp)])
        s = out["sessions"][0]
        assert s["matched_calls"] == 1
        assert s["matched_errors"] == 1

    def test_no_match_reports_empty(self, monkeypatch, capsys, session_file):
        tmp, _ = session_file
        out = run_script(monkeypatch, capsys, ["bash", "--args-contains", "kubectl",
                                               "--sessions-dir", str(tmp)])
        assert out["matches"] == 0


class TestDump:
    def test_pairs_and_entries(self, monkeypatch, capsys, session_file):
        _, f = session_file
        out = run_script(monkeypatch, capsys, ["bash", "--dump", str(f)])
        assert out["matched_calls"] == 3
        by_id = {c["id"]: c for c in out["calls"]}
        assert by_id["c1"]["is_error"] is False
        assert by_id["c2"]["is_error"] is True
        assert by_id["c2"]["call_entry"] < by_id["c2"]["result_entry"]
        assert "glab api mr 1" in by_id["c2"]["args"]
        assert "code 1" in by_id["c2"]["result"]

    def test_arg_clipping(self, monkeypatch, capsys, session_file, tmp_path):
        _, f = session_file
        lines = f.read_text().splitlines()
        big = entry("message",
                    assistant_msg([call_block("c9", "subagent", {"task": "x" * 9000})]),
                    timestamp="2026-09-10T11:00:00Z")
        lines.append(big)
        big_file = tmp_path / "big.jsonl"
        big_file.write_text("\n".join(lines) + "\n")
        out = run_script(monkeypatch, capsys, ["subagent", "--dump", str(big_file)])
        c = out["calls"][0]
        assert c["arg_len"] == 9012  # {"task": "..."} wrapper adds 12 chars
        assert len(c["args"]) < 4200  # clipped
        out_full = run_script(monkeypatch, capsys, ["subagent", "--dump", str(big_file), "--full-args"])
        assert len(out_full["calls"][0]["args"]) >= 9000

    def test_call_without_result_excluded_from_errors_only(self, monkeypatch, capsys, session_file, tmp_path):
        _, f = session_file
        lines = f.read_text().splitlines()
        lines.append(entry("message",
                           assistant_msg([call_block("cX", "bash", {"command": "glab api orphan"})]),
                           timestamp="2026-09-10T12:00:00Z"))
        orphan = tmp_path / "orphan.jsonl"
        orphan.write_text("\n".join(lines) + "\n")
        out_all = run_script(monkeypatch, capsys, ["bash", "--dump", str(orphan), "--args-contains", "glab api orphan"])
        assert out_all["matched_calls"] == 1
        assert out_all["calls"][0]["result_entry"] is None
        assert out_all["calls"][0]["is_error"] is None
        out_err = run_script(monkeypatch, capsys, ["bash", "--dump", str(orphan), "--args-contains", "glab api orphan", "--errors-only"])
        assert out_err["matched_calls"] == 0
