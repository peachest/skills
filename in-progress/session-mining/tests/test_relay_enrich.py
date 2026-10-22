"""relay-enrich tests: join/glob, re-entry multi-instance, no-relay-data degradation,
big-file final_metrics byte-scan, nanosecond timestamp parsing.

The script filename carries a hyphen, so it is loaded via importlib and its
main() invoked in-process with --relay-dir pointed at a tmp fixture dir.
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
_spec = importlib.util.spec_from_file_location("relay_enrich", SCRIPTS / "relay-enrich.py")
re_ = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(re_)

PI_SID = "01a13a10-54bb-7660-8f4e-e3bc1d858d4c"
INST_1 = "01a13a11-0000-0000-0000-000000000001"
INST_2 = "01a13a12-0000-0000-0000-000000000002"
OTHER_SID = "01a09de1-0220-74f5-bcfc-eb859d753352"


def agent_step(step_id, ts, model="glm53-internal", effort="high", llm=1,
               metrics=None, tool_calls=None, invocations=None):
    s = {
        "source": "agent", "step_id": step_id, "timestamp": ts,
        "model_name": model, "reasoning_effort": effort,
        "llm_call_count": llm,
        "metrics": metrics or {"prompt_tokens": 1000, "cached_tokens": 700,
                               "completion_tokens": 50,
                               "extra": {"reasoning_tokens": 10,
                                         "total_tokens": 1050}},
    }
    if tool_calls is not None:
        results = []
        for i, (name, status, attempt) in enumerate(tool_calls):
            results.append({"extra": {"event_name": name,
                                      "metadata": {"status": status,
                                                   "attempt_index": attempt}}})
        s["observation"] = {"results": results}
        s["extra"] = {"tool_invocations": invocations}
    return s


def write_trajectory(tmp_path, instance_id, session_id, steps, final_metrics=None,
                     indent=2):
    fm = final_metrics or {"total_prompt_tokens": 2000,
                           "total_cached_tokens": 1400,
                           "total_completion_tokens": 100,
                           "total_steps": len(steps)}
    doc = {
        "session_id": instance_id,
        "extra": {"nemo_relay": {"session_id": session_id,
                                 "session_instance_id": instance_id}},
        "final_metrics": fm,
        "steps": steps,
    }
    p = tmp_path / f"trajectory-{instance_id}.json"
    p.write_text(json.dumps(doc, indent=indent))
    return p


def run(tmp_path, arg, *extra):
    return re_.main([str(arg), "--relay-dir", str(tmp_path), *extra])


def test_join_by_pi_session_id(tmp_path, capsys):
    write_trajectory(tmp_path, INST_1, PI_SID,
                     [agent_step(1, "2026-10-15T10:00:00.123456789+00:00")])
    assert run(tmp_path, PI_SID) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "ok"
    assert out["trajectories"][0]["session_instance_id"] == INST_1
    assert out["trajectories"][0]["cache_hit_rate"] == 0.7
    step = out["trajectories"][0]["steps"][0]
    assert step["model_name"] == "glm53-internal"
    assert step["cached_tokens"] == 700
    assert out["totals"]["total_prompt_tokens"] == 2000


def test_join_by_session_file_path(tmp_path, capsys):
    write_trajectory(tmp_path, INST_1, PI_SID, [])
    fake_jsonl = tmp_path / f"2026-10-15T10-00-00-000Z_{PI_SID}.jsonl"
    fake_jsonl.write_text("")
    assert run(tmp_path, fake_jsonl) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "ok"


def test_reentry_multiple_instances_with_totals(tmp_path, capsys):
    write_trajectory(tmp_path, INST_1, PI_SID,
                     [agent_step(1, "2026-10-15T10:00:00+00:00")],
                     final_metrics={"total_prompt_tokens": 100,
                                    "total_cached_tokens": 50,
                                    "total_completion_tokens": 10,
                                    "total_steps": 1})
    write_trajectory(tmp_path, INST_2, PI_SID,
                     [agent_step(1, "2026-10-15T11:00:00+00:00")],
                     final_metrics={"total_prompt_tokens": 300,
                                    "total_cached_tokens": 250,
                                    "total_completion_tokens": 20,
                                    "total_steps": 1})
    assert run(tmp_path, PI_SID) == 0
    out = json.loads(capsys.readouterr().out)
    assert len(out["trajectories"]) == 2
    assert out["totals"]["total_prompt_tokens"] == 400
    assert out["totals"]["cache_hit_rate"] == round(300 / 400, 4)


def test_no_relay_data_degrades_silently(tmp_path, capsys):
    write_trajectory(tmp_path, "01a13a99-0000-0000-0000-000000000009",
                     OTHER_SID, [])
    assert run(tmp_path, PI_SID) == 0  # never a non-zero exit
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "no-relay-data"
    assert "no ATIF trajectory" in out["notes"][0]


def test_empty_relay_dir_degrades(tmp_path, capsys):
    assert run(tmp_path, PI_SID) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "no-relay-data"


def test_no_uuid_argument_errors(tmp_path, capsys):
    assert run(tmp_path, "not-a-uuid") == 2
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "error"


def test_turn_latency_and_switches(tmp_path, capsys):
    steps = [
        {"source": "user", "step_id": 0,
         "timestamp": "2026-10-15T10:00:00.000000000+00:00"},
        agent_step(1, "2026-10-15T10:00:10.000000000+00:00",
                   model="glm53-flash-internal", effort="high"),
        agent_step(2, "2026-10-15T10:00:40.000000000+00:00",
                   model="glm53-internal", effort="low"),
        agent_step(3, "2026-10-15T10:00:44.500000000+00:00",
                   model="glm53-internal", effort="low"),
    ]
    write_trajectory(tmp_path, INST_1, PI_SID, steps)
    assert run(tmp_path, PI_SID, "--no-steps") == 0
    out = json.loads(capsys.readouterr().out)
    summ = out["trajectories"][0]["step_summary"]
    assert summ["models_sequence"] == ["glm53-flash-internal", "glm53-internal"]
    assert summ["model_switches"] == 1
    assert summ["effort_switches"] == 1
    lat = summ["agent_turn_latency"]
    assert lat["count"] == 3
    assert lat["p50_s"] == 10.0
    assert lat["max_s"] == 30.0


def test_tool_call_duration_attempt_status(tmp_path, capsys):
    steps = [agent_step(
        1, "2026-10-15T10:00:10+00:00",
        tool_calls=[("bash", "error", 0), ("bash", "ok", 1)],
        invocations=[{"start_timestamp": 100.0, "end_timestamp": 100.5},
                     {"start_timestamp": 101.0, "end_timestamp": 101.25}])]
    write_trajectory(tmp_path, INST_1, PI_SID, steps)
    assert run(tmp_path, PI_SID) == 0
    out = json.loads(capsys.readouterr().out)
    tcs = out["trajectories"][0]["steps"][0]["tool_calls"]
    assert tcs[0] == {"tool": "bash", "duration_s": 0.5,
                      "attempt_index": 0, "status": "error"}
    assert tcs[1]["attempt_index"] == 1
    assert out["trajectories"][0]["step_summary"]["tool_status"]["errors"] == 1


def test_big_file_keeps_final_metrics_only(tmp_path, capsys, monkeypatch):
    write_trajectory(
        tmp_path, INST_1, PI_SID,
        [agent_step(1, "2026-10-15T10:00:00+00:00")],
        final_metrics={"total_prompt_tokens": 500,
                       "total_cached_tokens": 400,
                       "total_completion_tokens": 5,
                       "total_steps": 1})
    assert run(tmp_path, PI_SID, "--max-steps-file-mb", "0") == 0
    out = json.loads(capsys.readouterr().out)
    tr = out["trajectories"][0]
    assert tr["final_metrics"]["total_prompt_tokens"] == 500
    assert tr["cache_hit_rate"] == 0.8
    assert "steps" not in tr
    assert "per-step data skipped" in tr["notes"][0]


def test_nanosecond_timestamp_parsing():
    assert re_.parse_ts("2026-10-15T10:00:00.123456789+00:00") is not None
    assert re_.parse_ts("2026-10-15T10:00:00Z") is not None
    assert re_.parse_ts("2026-10-15T12:00:00.5+02:00") is not None
    assert re_.parse_ts("garbage") is None
    assert re_.parse_ts(None) is None
