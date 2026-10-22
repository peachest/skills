#!/usr/bin/env python3
"""NeMo Relay enrichment for a pi session — optional deep-analysis path.

Given a pi session id (or a session .jsonl path), find its ATIF trajectory
file(s) in the relay data dir and emit an enrichment JSON: final token metrics,
per-step latency/model/usage, per-tool-call duration/attempt_index/status.

pi session JSONL remains the primary source; this script only adds what the
JSONL lacks (token accounting, wall-clock latency, attempt_index). No matching
trajectory -> status "no-relay-data", exit 0 (silent degradation, never blocks).

Usage:
  relay-enrich.py <pi-session-id | session-file.jsonl> [--relay-dir DIR]
                  [--no-steps] [--max-steps-file-mb N]
Environment: NEMO_RELAY_DIR overrides the default data dir (~/data/nemo-relay).
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

DEFAULT_RELAY_DIR = os.path.join(os.path.expanduser("~"), "data", "nemo-relay")
HEAD_SCAN_BYTES = 65536        # nemo_relay sits near the file head in all observed files
BIG_SCAN_CHUNK = 4_000_000     # chunk size for the final_metrics byte-scan on huge files
UUID_RE = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
NEMO_RELAY_RE = re.compile(rb'"nemo_relay"\s*:\s*\{[^{}]*\}')
TS_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d{1,9}))?(Z|[+-]\d{2}:?\d{2})?$"
)


def resolve_session_id(arg):
    """Accept a pi session uuid or a session .jsonl path; return the uuid."""
    m = re.search(UUID_RE, arg)
    return m.group(0) if m else None


def index_trajectories(relay_dir):
    """Scan trajectory heads for extra.nemo_relay {session_id, session_instance_id}.

    Returns list of (path, session_id, instance_id) for every trajectory file.
    """
    out = []
    try:
        names = sorted(
            n for n in os.listdir(relay_dir)
            if n.startswith("trajectory-") and n.endswith(".json")
        )
    except OSError:
        return out
    for name in names:
        path = os.path.join(relay_dir, name)
        try:
            with open(path, "rb") as fh:
                head = fh.read(HEAD_SCAN_BYTES)
        except OSError:
            continue
        m = NEMO_RELAY_RE.search(head)
        if not m:
            continue
        sid = re.search(rb'"session_id"\s*:\s*"(' + UUID_RE.encode() + rb')"', m.group(0))
        inst = re.search(
            rb'"session_instance_id"\s*:\s*"(' + UUID_RE.encode() + rb')"', m.group(0)
        )
        if sid and inst:
            out.append((path, sid.group(1).decode(), inst.group(1).decode()))
    return out


def parse_ts(s):
    """Parse a timestamp that may carry nanosecond precision (pi emits 9 digits)."""
    if not isinstance(s, str):
        return None
    m = TS_RE.match(s)
    if not m:
        return None
    base, frac, tz = m.groups()
    frac = (frac or "")[:6].ljust(6, "0")
    if not tz:
        tz = "+00:00"
    elif tz == "Z":
        tz = "+00:00"
    elif ":" not in tz:
        tz = tz[:3] + ":" + tz[3:]
    try:
        return datetime.fromisoformat(f"{base}.{frac}{tz}")
    except ValueError:
        return None


def percentile(sorted_vals, p):
    if not sorted_vals:
        return None
    idx = min(len(sorted_vals) - 1, int(round(p / 100.0 * (len(sorted_vals) - 1))))
    return round(sorted_vals[idx], 3)


def latency_summary(values):
    vals = sorted(v for v in values if v is not None)
    if not vals:
        return None
    n = len(vals)
    mean = sum(vals) / n
    return {
        "count": n,
        "mean_s": round(mean, 3),
        "p50_s": percentile(vals, 50),
        "p90_s": percentile(vals, 90),
        "p99_s": percentile(vals, 99),
        "max_s": round(vals[-1], 3),
    }


def summarize_steps(steps):
    """Summary + per-step records from the parsed steps[] array."""
    records = []
    prev_ts = None
    agent_gaps = []
    models = []
    model_switches = 0
    effort_switches = 0
    llm_calls = 0
    tool_error_count = 0
    for s in steps:
        ts = parse_ts(s.get("timestamp"))
        gap = None
        if ts is not None and prev_ts is not None:
            gap = round((ts - prev_ts).total_seconds(), 3)
        prev_ts = ts if ts is not None else prev_ts

        rec = {"step_id": s.get("step_id"), "source": s.get("source"),
               "wall_from_prev_s": gap}
        if s.get("source") == "agent":
            if gap is not None:
                agent_gaps.append(gap)
            model = s.get("model_name")
            effort = s.get("reasoning_effort")
            if model:
                if models and models[-1] != model:
                    model_switches += 1
                if model not in models:
                    models.append(model)
            if effort is not None and records:
                for r in reversed(records):
                    if r.get("source") == "agent" and "reasoning_effort" in r:
                        if r["reasoning_effort"] != effort:
                            effort_switches += 1
                        break
            llm_calls += s.get("llm_call_count") or 0
            rec.update({
                "model_name": model,
                "reasoning_effort": effort,
                "llm_call_count": s.get("llm_call_count"),
            })
            metrics = s.get("metrics") or {}
            for k in ("prompt_tokens", "cached_tokens", "completion_tokens"):
                if k in metrics:
                    rec[k] = metrics[k]
            extra = metrics.get("extra") or {}
            if "reasoning_tokens" in extra:
                rec["reasoning_tokens"] = extra["reasoning_tokens"]
            if "total_tokens" in extra:
                rec["total_tokens"] = extra["total_tokens"]
            tool_calls = []
            results = (s.get("observation") or {}).get("results") or []
            invocations = (s.get("extra") or {}).get("tool_invocations") or []
            for i, r in enumerate(results):
                rex = r.get("extra") or {}
                md = rex.get("metadata") or {}
                ti = invocations[i] if i < len(invocations) else {}
                dur = None
                try:
                    dur = round(ti["end_timestamp"] - ti["start_timestamp"], 3)
                except (KeyError, TypeError):
                    pass
                status = md.get("status")
                if status:
                    if status != "ok":
                        tool_error_count += 1
                tool_calls.append({
                    "tool": rex.get("event_name"),
                    "duration_s": dur,
                    "attempt_index": md.get("attempt_index"),
                    "status": status,
                })
            if tool_calls:
                rec["tool_calls"] = tool_calls
        records.append(rec)

    summary = {
        "llm_calls_total": llm_calls,
        "models_sequence": models,
        "model_switches": model_switches,
        "effort_switches": effort_switches,
        "tool_status": {"errors": tool_error_count},
        "agent_turn_latency": latency_summary(agent_gaps),
    }
    return summary, records


def scan_final_metrics(path):
    """final_metrics for files too big to json.load — byte-scan, then decode the
    small object that directly follows the key."""
    dec = json.JSONDecoder()
    try:
        with open(path, "rb") as fh:
            prev = b""
            while True:
                chunk = fh.read(BIG_SCAN_CHUNK)
                if not chunk:
                    return None
                buf = prev + chunk
                i = buf.find(b'"final_metrics"')
                if i >= 0:
                    j = buf.find(b"{", i)
                    if j >= 0:
                        try:
                            obj, _ = dec.raw_decode(
                                buf[j:j + 4096].decode("utf-8", "replace"))
                            return obj
                        except json.JSONDecodeError:
                            return None
                    return None
                prev = chunk[-64:]
    except OSError:
        return None


def enrich_trajectory(path, instance_id, include_steps, max_steps_bytes):
    size = os.path.getsize(path)
    entry = {
        "file": os.path.basename(path),
        "session_instance_id": instance_id,
        "file_size_bytes": size,
    }
    if size <= max_steps_bytes:
        try:
            with open(path) as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            entry["error"] = f"unparseable trajectory: {e}"
            return entry
        entry["final_metrics"] = data.get("final_metrics")
        summary, records = summarize_steps(data.get("steps") or [])
        entry["step_summary"] = summary
        if include_steps:
            entry["steps"] = records
    else:
        fm = scan_final_metrics(path)
        entry["final_metrics"] = fm
        entry["step_summary"] = None
        entry["notes"] = [
            f"per-step data skipped: file {size // 1_000_000}MB exceeds "
            f"--max-steps-file-mb threshold"
        ]
    fm = entry.get("final_metrics") or {}
    pt = fm.get("total_prompt_tokens")
    ct = fm.get("total_cached_tokens")
    if pt:
        entry["cache_hit_rate"] = round(ct / pt, 4) if ct is not None else None
    return entry


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("session", help="pi session uuid or session .jsonl path")
    ap.add_argument("--relay-dir", default=os.environ.get("NEMO_RELAY_DIR",
                                                          DEFAULT_RELAY_DIR))
    ap.add_argument("--no-steps", action="store_true",
                    help="omit the per-step records (summary only)")
    ap.add_argument("--max-steps-file-mb", type=int, default=256,
                    help="full-parse threshold; larger files keep only "
                         "final_metrics (default 256)")
    args = ap.parse_args(argv)

    session_id = resolve_session_id(args.session)
    if not session_id:
        print(json.dumps({"status": "error",
                          "error": "no uuid found in argument"}, indent=2))
        return 2

    result = {
        "pi_session_id": session_id,
        "relay_dir": args.relay_dir,
        "primary_source_note": (
            "pi session JSONL is the primary source; this enrichment is "
            "supplementary (relay coverage starts 2026-09-14 and requires a "
            "live gateway)")
    }

    trajectories = index_trajectories(args.relay_dir)
    matches = [t for t in trajectories
               if session_id in (t[1], t[2])]

    if not matches:
        result["status"] = "no-relay-data"
        result["notes"] = [
            f"no ATIF trajectory matches session {session_id} in {args.relay_dir} "
            f"({len(trajectories)} files scanned); the session predates relay "
            f"coverage or the gateway was down — stay on the pi JSONL path"
        ]
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    result["status"] = "ok"
    entries = []
    for path, _sid, inst in matches:
        entries.append(enrich_trajectory(path, inst, not args.no_steps,
                                         args.max_steps_file_mb * 1_000_000))
    result["trajectories"] = entries

    totals = {}
    for e in entries:
        fm = e.get("final_metrics") or {}
        for k, v in fm.items():
            if isinstance(v, (int, float)):
                totals[k] = totals.get(k, 0) + v
    if totals:
        pt = totals.get("total_prompt_tokens")
        ct = totals.get("total_cached_tokens")
        if pt:
            totals["cache_hit_rate"] = round(ct / pt, 4) if ct else 0.0
    result["totals"] = totals or None
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
