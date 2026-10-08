"""Tests for doc-usage.py — doc consumption matrix and echo verification."""

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


def assistant_msg(blocks):
    return {"role": "assistant", "content": blocks}


def tool_result(cid, name, text, is_error=False):
    return {"role": "toolResult", "toolCallId": cid, "toolName": name,
            "content": [{"type": "text", "text": text}], "isError": is_error,
            "timestamp": 1789000000000}


def load_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("doc_usage", SCRIPTS / "doc-usage.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def du():
    return load_module()


class TestClassifyBash:
    def test_read_prefixes(self, du):
        assert du.classify_bash("cat docs/CONTEXT.md") == "read"
        assert du.classify_bash("grep -rn deviation-ledger docs/") == "read"
        assert du.classify_bash("rg 'gpu' status.md") == "read"
        assert du.classify_bash("sed -n '1,20p' CONSTRAINT.md") == "read"

    def test_write_markers(self, du):
        assert du.classify_bash("sed -i 's/a/b/' status.md") == "write"
        assert du.classify_bash("echo x >> status.md") == "write"
        assert du.classify_bash("cat > status.md <<'EOF'\nbody\nEOF") == "write"
        assert du.classify_bash("tee status.md") == "write"

    def test_python_edit_fallback_is_write(self, du):
        # agent falls back to python when the edit tool fails
        assert du.classify_bash(
            'python3 -c "src=open(\'f.md\').read(); '
            "open('f.md','w').write(src.replace('a','b'))\"") == "write"
        assert du.classify_bash(
            "python3 -c \"p=Path('doc.md'); p.write_text(p.read_text().replace('x','y'))\"") == "write"

    def test_python_read(self, du):
        assert du.classify_bash("python3 -c \"import json; print(json.load(open('c.json')))\"") == "read"

    def test_python_no_marker_is_mention(self, du):
        assert du.classify_bash("python3 train.py --epochs 3") == "mention"

    def test_plain_mention(self, du):
        assert du.classify_bash('echo "see CONTEXT.md for rules"') == "mention"


class TestMatrix:
    @pytest.fixture
    def sessions(self, tmp_path):
        lines = [
            entry("session", id="s1", cwd="/proj"),
            # read tool: consumed
            entry("message", assistant_msg([call_block("r1", "read", {"path": "/proj/docs/CONTEXT.md"})])),
            entry("message", tool_result("r1", "read", "# CONTEXT\nterm-alpha rules")),
            # bash grep: consumed
            entry("message", assistant_msg([call_block("b1", "bash", {"command": "grep term-alpha docs/CONTEXT.md"})])),
            entry("message", tool_result("b1", "bash", "term-alpha: always")),
            # bash python edit: write fallback
            entry("message", assistant_msg([call_block("b2", "bash",
                  {"command": "python3 -c \"open('docs/CONTEXT.md','w').write(x.replace('a','b'))\""})])),
            entry("message", tool_result("b2", "bash", "")),
            # write tool: maintenance only
            entry("message", assistant_msg([call_block("w1", "write", {"path": "/proj/docs/domain.md", "content": "x"})])),
            entry("message", tool_result("w1", "write", "ok")),
            # mention only
            entry("message", assistant_msg([call_block("m1", "bash", {"command": "echo 'see CONTEXT.md'"})])),
            entry("message", tool_result("m1", "bash", "")),
            # heredoc write
            entry("message", assistant_msg([call_block("b3", "bash",
                  {"command": "cat > docs/CONTEXT.md <<'EOF'\nnew\nEOF"})])),
            entry("message", tool_result("b3", "bash", "")),
        ]
        d = tmp_path / "proj"
        d.mkdir()
        (d / "main.jsonl").write_text("\n".join(lines) + "\n")
        # nested session (fork) — must be discovered by the recursive scan
        nested = d / "main.jsonl-fork"
        fork = d / "forks"
        fork.mkdir()
        (fork / "f1.jsonl").write_text(
            entry("message", assistant_msg([call_block("f1", "read", {"path": "/proj/docs/domain.md"})])) + "\n" +
            entry("message", tool_result("f1", "read", "domain rules")))
        return d

    def test_recursive_discovery(self, du, sessions):
        assert len(du.iter_sessions(str(sessions))) == 2

    def test_classification_channels(self, du, sessions):
        out = du.scan_matrix(du.iter_sessions(str(sessions)),
                             {"CONTEXT.md": ["CONTEXT.md"], "domain.md": ["domain.md"]}, None, 3)
        by = {t["target"]: t for t in out["targets"]}
        ctx = by["CONTEXT.md"]
        assert ctx["READ"] == 2          # read tool + bash grep
        assert ctx["WRITE"] == 2         # python edit fallback + heredoc
        assert ctx["MENTION"] == 1       # echo mention
        assert ctx["read_with_result"] == 2
        # domain.md: one nested read + one top-level write maintenance
        dom = by["domain.md"]
        assert dom["READ"] == 1
        assert dom["WRITE"] == 1

    def test_escape_rate(self, du, sessions, tmp_path):
        # a session with GPU action signatures but zero target touch
        esc = tmp_path / "proj2"
        esc.mkdir()
        (esc / "runaway.jsonl").write_text(
            entry("message", assistant_msg([call_block("g1", "bash", {"command": "nvidia-smi"})])) + "\n" +
            entry("message", tool_result("g1", "bash", "ok")) + "\n" +
            entry("message", assistant_msg([call_block("g2", "bash", {"command": "nvidia-smi"})])) + "\n" +
            entry("message", tool_result("g2", "bash", "ok")) + "\n" +
            entry("message", assistant_msg([call_block("g3", "bash", {"command": "nvidia-smi"})])) + "\n" +
            entry("message", tool_result("g3", "bash", "ok")) + "\n" +
            entry("message", assistant_msg([call_block("g4", "bash", {"command": "nvidia-smi"})])) + "\n" +
            entry("message", tool_result("g4", "bash", "ok")) + "\n")
        out = du.scan_matrix([str(esc / "runaway.jsonl")],
                             {"CONTEXT.md": ["CONTEXT.md"]},
                             escape=r"nvidia-smi", escape_min=3)
        assert len(out["escapes"]) == 1
        assert out["escapes"][0]["sig_count"] == 4

    def test_no_escape_when_target_touched_even_by_write(self, du, tmp_path):
        f = tmp_path / "ledger-writer.jsonl"
        f.write_text(
            entry("message", assistant_msg([call_block("g1", "bash", {"command": "nvidia-smi"})])) + "\n" +
            entry("message", tool_result("g1", "bash", "ok")) + "\n" +
            entry("message", assistant_msg([call_block("g2", "bash", {"command": "nvidia-smi"})])) + "\n" +
            entry("message", tool_result("g2", "bash", "ok")) + "\n" +
            entry("message", assistant_msg([call_block("g3", "bash", {"command": "nvidia-smi"})])) + "\n" +
            entry("message", tool_result("g3", "bash", "ok")) + "\n" +
            entry("message", assistant_msg([call_block("g4", "bash", {"command": "nvidia-smi"})])) + "\n" +
            entry("message", tool_result("g4", "bash", "ok")) + "\n" +
            entry("message", assistant_msg([call_block("w1", "edit", {"path": "/p/gpu-ledger.md", "oldText": "a", "newText": "b"})])) + "\n" +
            entry("message", tool_result("w1", "edit", "ok")) + "\n")
        out = du.scan_matrix([str(f)], {"ledger": ["gpu-ledger"]}, escape=r"nvidia-smi", escape_min=3)
        assert out["escapes"] == []


class TestEcho:
    @pytest.fixture
    def doc(self, tmp_path):
        d = tmp_path / "docs"
        d.mkdir()
        f = d / "RULES.md"
        f.write_text("# Rules\n\nThe reserve-gpu protocol requires ledger booking before "
                     "allocation. Escalation path goes through triage-labels first. "
                     "Escalation path is mandatory.\n")
        return f

    def make_session(self, path, calls_texts):
        lines = [entry("session", id="s", cwd="/proj")]
        for i, (tool, args, result, texts) in enumerate(calls_texts):
            lines.append(entry("message", assistant_msg(
                [call_block(f"c{i}", tool, args)] + [{"type": "text", "text": t} for t in texts])))
            if result is not None:
                lines.append(entry("message", tool_result(f"c{i}", tool, result)))
        Path(path).write_text("\n".join(lines) + "\n")

    def test_echo_after_read_counts(self, du, doc, tmp_path):
        f = tmp_path / "s1.jsonl"
        self.make_session(f, [
            ("read", {"path": str(doc)}, "file content", []),
            ("bash", {"command": "echo next"}, "next",
             ["The escalation path goes through triage-labels before allocation."]),
        ])
        out = du.scan_echo([str(f)], "RULES.md", str(doc))
        assert out["sessions_with_echo"] == 1
        assert "consumed" in out["verdict"]

    def test_echo_before_read_ignored(self, du, doc, tmp_path):
        # text before the first read-like touch is not consumption evidence
        f = tmp_path / "s2.jsonl"
        self.make_session(f, [
            ("bash", {"command": "echo plan"}, "plan",
             ["The reserve-gpu protocol requires booking."]),
            ("read", {"path": str(doc)}, "file content", []),
        ])
        out = du.scan_echo([str(f)], "RULES.md", str(doc))
        assert out["sessions_with_echo"] == 0

    def test_write_only_session_not_anchored(self, du, doc, tmp_path):
        # a session that only WRITES the doc echoes its own content — not consumption
        f = tmp_path / "s3.jsonl"
        self.make_session(f, [
            ("write", {"path": str(doc), "content": "The reserve-gpu protocol requires ledger booking."},
             None, ["Writing the reserve-gpu protocol section now."]),
        ])
        out = du.scan_echo([str(f)], "RULES.md", str(doc))
        assert out["sessions_with_echo"] == 0
        assert out["sessions_touch_but_no_read"] == 1
        assert out["verdict"] == "no-echo-evidence"

    def test_no_read_at_all(self, du, doc, tmp_path):
        f = tmp_path / "s4.jsonl"
        self.make_session(f, [
            ("bash", {"command": "nvidia-smi"}, "ok", []),
        ])
        out = du.scan_echo([str(f)], "RULES.md", str(doc))
        assert out["sessions_with_echo"] == 0
