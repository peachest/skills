"""Tests for scripts/find-skill-sessions.py.

Covers the two seams:
  search: <skill-name> [--session <id>] --sessions-dir <dir> → JSON {matches, sessions[]}
  index:  --index <file> → JSON {entries_indexed, truncated, index[]}
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
SCRIPT = SCRIPTS_DIR / "find-skill-sessions.py"


def run(*args: str) -> tuple[dict | list, int, str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, timeout=30,
    )
    try:
        out = json.loads(result.stdout)
    except json.JSONDecodeError:
        out = None
    return out, result.returncode, result.stderr


def session_line(entry: dict) -> str:
    return json.dumps(entry, ensure_ascii=False)


INJECTED_USER_MSG = {
    "type": "message",
    "timestamp": "2026-09-07T17:55:15.371Z",
    "message": {
        "role": "user",
        "content": [{"type": "text", "text": '<skill name="my-skill" location="/x/SKILL.md">\\nbody\\n</skill>\\n\\ncheck this'}],
    },
}

ASSISTANT_MSG = {
    "type": "message",
    "timestamp": "2026-09-07T17:55:23.316Z",
    "message": {
        "role": "assistant",
        "content": [
            {"type": "text", "text": "ok"},
            {"type": "toolCall", "id": "c1", "name": "bash", "arguments": {"command": "ls"}},
        ],
        "usage": {"input": 100, "output": 50, "cacheRead": 500, "cacheWrite": 0},
    },
}


def write_session(path: Path, skill_name: str | None, session_id: str) -> None:
    lines = [
        session_line({"type": "session", "version": 3, "id": session_id,
                      "timestamp": "2026-09-07T17:54:28.086Z", "cwd": "/tmp/proj"}),
    ]
    if skill_name:
        msg = json.loads(session_line(INJECTED_USER_MSG))
        msg["message"]["content"][0]["text"] = (
            f'<skill name="{skill_name}" location="/x/SKILL.md">\\nbody\\n</skill>\\n\\ncheck this'
        )
        lines.append(session_line(msg))
    lines.append(session_line(ASSISTANT_MSG))
    path.write_text("\n".join(lines) + "\n")


@pytest.fixture
def sessions_dir(tmp_path: Path) -> Path:
    slug = tmp_path / "--tmp-proj--"
    slug.mkdir()
    write_session(slug / "2026-09-07T17-54-28-086Z_11111111-1111.jsonl", "my-skill", "11111111-1111")
    write_session(slug / "2026-09-07T18-00-00-000Z_22222222-2222.jsonl", "other-skill", "22222222-2222")
    return slug


class TestSearch:
    def test_marker_match_finds_only_invoking_session(self, sessions_dir):
        out, code, _ = run("my-skill", "--sessions-dir", str(sessions_dir))
        assert code == 0
        assert out["matches"] == 1
        s = out["sessions"][0]
        assert s["marker_count"] >= 1
        assert s["session_id"] == "11111111-1111"
        assert s["selected_via"] == "marker"

    def test_no_match_returns_empty(self, sessions_dir):
        out, code, _ = run("no-such-skill", "--sessions-dir", str(sessions_dir))
        assert code == 0
        assert out["matches"] == 0

    def test_stats_collected(self, sessions_dir):
        out, _, _ = run("my-skill", "--sessions-dir", str(sessions_dir))
        s = out["sessions"][0]
        assert s["entries"] == 3
        assert s["messages"].get("assistant") == 1
        assert s["tool_calls"] == {"bash": 1}
        assert s["usage"]["output"] == 50
        assert s["usage"]["cacheRead"] == 500
        assert "first_timestamp" in s and "last_timestamp" in s

    def test_explicit_session_reports_even_without_marker(self, sessions_dir):
        # s2 invoked other-skill, but user explicitly asked for it
        out, code, _ = run("my-skill", "--session", "22222222",
                           "--sessions-dir", str(sessions_dir))
        assert code == 0
        assert out["matches"] == 1
        assert out["sessions"][0]["session_id"] == "22222222-2222"
        assert out["sessions"][0]["selected_via"] == "explicit-id"
        assert out["sessions"][0]["marker_count"] == 0

    def test_explicit_session_unknown_prefix_errors(self, sessions_dir):
        out, code, err = run("my-skill", "--session", "deadbeef",
                             "--sessions-dir", str(sessions_dir))
        assert code == 1

    def test_missing_sessions_dir_errors(self):
        out, code, err = run("x", "--sessions-dir", "/nonexistent-xyz")
        assert code == 2


class TestIndex:
    def test_index_lines_carry_roles_and_calls(self, sessions_dir):
        f = sessions_dir / "2026-09-07T17-54-28-086Z_11111111-1111.jsonl"
        out, code, _ = run("--index", str(f))
        assert code == 0
        assert out["entries_indexed"] == 3
        assert out["truncated"] is False
        assert "[0]" in out["index"][0] and "session" in out["index"][0]
        assistant_lines = [l for l in out["index"] if "CALL bash" in l]
        assert assistant_lines, "tool call must appear in index"
        assert "in=100" in assistant_lines[0] and "cacheR=500" in assistant_lines[0]

    def test_index_truncation_cap(self, tmp_path):
        f = tmp_path / "big.jsonl"
        f.write_text("\n".join(
            session_line({"type": "session", "id": "x", "timestamp": "2026-09-07T00:00:00Z", "cwd": "/x"})
            if i == 0 else
            session_line({"type": "message", "timestamp": "2026-09-07T00:00:00Z",
                          "message": {"role": "user", "content": [{"type": "text", "text": "hi"}]}})
            for i in range(700)
        ) + "\n")
        out, code, _ = run("--index", str(f))
        assert code == 0
        assert out["truncated"] is True
        assert out["entries_indexed"] == 600

    def test_index_missing_file_errors(self):
        out, code, err = run("--index", "/nonexistent.jsonl")
        assert code == 2
