"""version-anchor tests: commit / uncommitted / third-party resolution + multi-version + read-load.

The script filename carries a hyphen, so it is loaded via importlib and its
main() invoked in-process — monkeypatched module constants (SOURCE_ROOTS /
THIRD_PARTY_ROOT) then take effect, which a subprocess CLI run could not see.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
_spec = importlib.util.spec_from_file_location("version_anchor", SCRIPTS / "version-anchor.py")
va = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(va)

BODY_V1 = "---\nname: demo\n---\n\n# Demo v1\nold behavior\n"
BODY_V2 = "---\nname: demo\n---\n\n# Demo v2\nnew behavior\n"
BODY_DIRTY = "---\nname: demo\n---\n\n# Demo dirty\nnever committed\n"


def inject(text: str, name: str = "demo") -> str:
    return f'<skill name="{name}" location="/x">\n\n{text}</skill>\n'


def msg_user(text: str, ts: str = "2026-09-11T10:00:00Z") -> dict:
    return {"type": "message", "timestamp": ts,
            "message": {"role": "user", "content": [{"type": "text", "text": text}]}}


def read_pair(body: str, ts: str = "2026-09-11T11:00:00Z") -> list[dict]:
    return [
        {"type": "message", "timestamp": ts,
         "message": {"role": "assistant", "content": [
             {"type": "toolCall", "id": "c1", "name": "read",
              "arguments": {"path": "/anywhere/demo/SKILL.md"}}]}},
        {"type": "toolResult", "toolCallId": "c1", "timestamp": ts,
         "content": [{"type": "text", "text": body}]},
    ]


def write_session(tmp_path: Path, entries: list[dict]) -> Path:
    f = tmp_path / "s.jsonl"
    f.write_text("\n".join(json.dumps(e) for e in entries), encoding="utf-8")
    return f


def git_repo(tmp_path: Path, commits: list[str]) -> Path:
    repo = tmp_path / "skills"
    (repo / "in-progress" / "demo").mkdir(parents=True)

    def run(*a):
        subprocess.run(a, cwd=repo, check=True, capture_output=True)

    run("git", "init", "-q", "-b", "main")
    run("git", "config", "user.email", "t@t")
    run("git", "config", "user.name", "t")
    for i, body in enumerate(commits):
        (repo / "in-progress" / "demo" / "SKILL.md").write_text(body, encoding="utf-8")
        run("git", "add", ".")
        run("git", "commit", "-q", "-m", f"v{i + 1}")
    return repo


@pytest.fixture
def roots(tmp_path, monkeypatch):
    repo = git_repo(tmp_path, [BODY_V1, BODY_V2])
    monkeypatch.setattr(va, "SOURCE_ROOTS", [repo])
    monkeypatch.setattr(va, "THIRD_PARTY_ROOT", tmp_path / "agents")
    return repo


def run_main(session: Path, monkeypatch, capsys) -> list:
    monkeypatch.setattr(sys, "argv", ["version-anchor.py", str(session)])
    va.main()
    return json.loads(capsys.readouterr().out)


def test_commit_resolution(roots, tmp_path, monkeypatch, capsys):
    s = write_session(tmp_path, [msg_user(inject(BODY_V2))])
    r = run_main(s, monkeypatch, capsys)
    assert len(r) == 1
    head = subprocess.run(["git", "-C", str(roots), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    assert r[0]["resolution"] == {"type": "commit", "commit": head, "date": r[0]["resolution"]["date"]}
    assert r[0]["resolution"]["commit"] == head
    assert r[0]["injections"] == 1


def test_uncommitted_matches_current_file(roots, tmp_path, monkeypatch, capsys):
    (roots / "in-progress" / "demo" / "SKILL.md").write_text(BODY_DIRTY, encoding="utf-8")
    s = write_session(tmp_path, [msg_user(inject(BODY_DIRTY))])
    r = run_main(s, monkeypatch, capsys)
    assert r[0]["resolution"] == {"type": "uncommitted", "matches_current_file": True}


def test_uncommitted_variant_gone(roots, tmp_path, monkeypatch, capsys):
    # body matches neither any commit nor the current file — a version that
    # exists nowhere but this session log
    s = write_session(tmp_path, [msg_user(inject(BODY_DIRTY))])
    r = run_main(s, monkeypatch, capsys)
    assert r[0]["resolution"] == {"type": "uncommitted", "matches_current_file": False}


def test_third_party_no_history(tmp_path, monkeypatch, capsys):
    tp = tmp_path / "agents"
    (tp / "demo").mkdir(parents=True)
    (tp / "demo" / "SKILL.md").write_text(BODY_V1, encoding="utf-8")
    monkeypatch.setattr(va, "SOURCE_ROOTS", [tmp_path / "empty-skills"])
    monkeypatch.setattr(va, "THIRD_PARTY_ROOT", tp)
    s = write_session(tmp_path, [msg_user(inject(BODY_V1))])
    r = run_main(s, monkeypatch, capsys)
    assert r[0]["resolution"] == {"type": "third-party", "matches_current_file": True}


def test_multi_version_session(roots, tmp_path, monkeypatch, capsys):
    s = write_session(tmp_path, [
        msg_user(inject(BODY_V1), ts="2026-09-11T10:00:00Z"),
        msg_user(inject(BODY_V2), ts="2026-09-11T12:00:00Z"),
    ])
    r = run_main(s, monkeypatch, capsys)
    assert len(r) == 2
    assert [x["first_seen"] for x in r] == ["2026-09-11T10:00:00Z", "2026-09-11T12:00:00Z"]


def test_read_load_anchor(roots, tmp_path, monkeypatch, capsys):
    s = write_session(tmp_path, read_pair(BODY_V1))
    r = run_main(s, monkeypatch, capsys)
    assert len(r) == 1
    assert r[0]["read_loads"] == 1
    assert r[0]["resolution"]["type"] == "commit"


def test_truncated_read_skipped(roots, tmp_path, monkeypatch, capsys):
    s = write_session(tmp_path, read_pair("Output is truncated...\n" + BODY_V1))
    assert run_main(s, monkeypatch, capsys) == []


def test_no_signal_empty(roots, tmp_path, monkeypatch, capsys):
    s = write_session(tmp_path, [msg_user("hello world")])
    assert run_main(s, monkeypatch, capsys) == []


def test_realistic_injection_form(roots, tmp_path, monkeypatch, capsys):
    # pi's injection strips frontmatter and prepends a References line; the
    # canonical form must converge with the full-file blob form
    realistic = "References are relative to /x.\n\n# Demo v2\nnew behavior\n"
    s = write_session(tmp_path, [
        msg_user(inject(realistic), ts="2026-09-11T10:00:00Z"),
        msg_user(inject(BODY_V2), ts="2026-09-11T11:00:00Z"),
    ])
    r = run_main(s, monkeypatch, capsys)
    assert len(r) == 1  # both forms canonicalize to one version
    assert r[0]["injections"] == 2
    assert r[0]["resolution"]["type"] == "commit"
