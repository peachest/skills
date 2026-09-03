#!/usr/bin/env python3
"""
ci-pipeline-profiler — GitLab CI pipeline duration analysis tool.

Subcommands:
  jobs <URL>              Fetch all jobs of a pipeline, output JSON.
  trace <URL> <JOB_ID>    Fetch a job's trace log, save to file, output path.
  sections <LOG_FILE>     Parse GitLab section timestamps, output JSON.
  signals <LOG_FILE>      Extract sub-step timing signals from log, output JSON.

URL format: https://<host>/<group>/<project>/-/pipelines/<id>
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlparse


# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------

def parse_pipeline_url(url: str) -> tuple[str, str, str]:
    """Extract (hostname, url_encoded_project_path, pipeline_id) from a GitLab pipeline URL.

    Example:
      https://gitlab.blue.example/llm/llmops/hami/ppu-device-plugin/-/pipelines/1326695
      → ("gitlab.blue.example", "llm%2Fllmops%2Fhami%2Fppu-device-plugin", "1326695")
    """
    parsed = urlparse(url)
    host = parsed.netloc

    # Path: /llm/llmops/hami/ppu-device-plugin/-/pipelines/1326695
    path = parsed.path
    match = re.match(r'^/(.+?)/-/pipelines/(\d+)', path)
    if not match:
        raise ValueError(f"Cannot parse pipeline URL: {url}")

    project_path = match.group(1)
    pipeline_id = match.group(2)

    # URL-encode project path for API calls: llm/llmops/hami/ppu-device-plugin → llm%2F...
    encoded_project = project_path.replace('/', '%2F')

    return host, encoded_project, pipeline_id


# ---------------------------------------------------------------------------
# glab API helpers
# ---------------------------------------------------------------------------

def glab_api(host: str, endpoint: str) -> str:
    """Run glab api command and return stdout. Uses GITLAB_TOKEN env var."""
    token = os.environ.get("GITLAB_TOKEN") or os.environ.get("GITLAB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("No GitLab token found. Set GITLAB_TOKEN or GITLAB_PERSONAL_ACCESS_TOKEN.")

    cmd = [
        "glab", "api", endpoint,
        "--hostname", host,
    ]
    env = os.environ.copy()
    env["GITLAB_TOKEN"] = token

    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        raise RuntimeError(f"glab api failed: {result.stderr}")

    return result.stdout


def glab_api_raw(host: str, endpoint: str) -> bytes:
    """Run glab api command and return raw bytes (for binary/log endpoints)."""
    token = os.environ.get("GITLAB_TOKEN") or os.environ.get("GITLAB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("No GitLab token found. Set GITLAB_TOKEN or GITLAB_PERSONAL_ACCESS_TOKEN.")

    cmd = [
        "glab", "api", endpoint,
        "--hostname", host,
    ]
    env = os.environ.copy()
    env["GITLAB_TOKEN"] = token

    result = subprocess.run(cmd, capture_output=True, env=env)
    if result.returncode != 0:
        raise RuntimeError(f"glab api failed: {result.stderr.decode(errors='replace')}")

    return result.stdout


# ---------------------------------------------------------------------------
# Subcommand: jobs
# ---------------------------------------------------------------------------

def cmd_jobs(args):
    """Fetch all jobs of a pipeline, output structured JSON."""
    host, project, pipeline_id = parse_pipeline_url(args.url)
    endpoint = f"projects/{project}/pipelines/{pipeline_id}/jobs"
    raw = glab_api(host, endpoint)
    jobs = json.loads(raw)

    # Extract the fields the profiler cares about
    result = []
    for job in jobs:
        result.append({
            "id": job.get("id"),
            "name": job.get("name"),
            "stage": job.get("stage"),
            "status": job.get("status"),
            "allow_failure": job.get("allow_failure", False),
            "duration": job.get("duration"),
            "queued_duration": job.get("queued_duration"),
            "started_at": job.get("started_at"),
            "finished_at": job.get("finished_at"),
            "created_at": job.get("created_at"),
            "runner": _extract_runner(job),
            "web_url": job.get("web_url"),
        })

    # Sort by stage then started_at
    result.sort(key=lambda j: (j.get("stage", ""), j.get("started_at") or ""))
    print(json.dumps(result, indent=2))


def _extract_runner(job):
    runner = job.get("runner") or {}
    return {
        "name": runner.get("name"),
        "description": runner.get("description"),
    } if runner else None


# ---------------------------------------------------------------------------
# Subcommand: trace
# ---------------------------------------------------------------------------

def cmd_trace(args):
    """Fetch a job's trace log and save to a temp file."""
    host, project, _ = parse_pipeline_url(args.url)
    job_id = args.job_id
    endpoint = f"projects/{project}/jobs/{job_id}/trace"
    raw = glab_api_raw(host, endpoint)

    # Decode to text, preserving as much as possible
    text = raw.decode("utf-8", errors="replace")

    # Save to file
    output_file = args.output or f"/tmp/gl_job_{job_id}.log"
    with open(output_file, "w") as f:
        f.write(text)

    print(json.dumps({
        "job_id": job_id,
        "log_file": output_file,
        "size_bytes": len(raw),
        "line_count": text.count("\n") + 1,
    }, indent=2))


# ---------------------------------------------------------------------------
# Subcommand: sections
# ---------------------------------------------------------------------------

# GitLab section timestamp format in trace logs:
#   section_start:UNIX_TIMESTAMP:section_name\r\x1b[0K...
#   section_end:UNIX_TIMESTAMP:section_name\r\x1b[0K...
# Section names are lowercase with underscores (e.g. step_script, prepare_executor).
SECTION_RE = re.compile(r'section_(start|end):(\d+):([a-z_]+)')

def cmd_sections(args):
    """Parse GitLab section timestamps from a log file, output JSON."""
    with open(args.log_file, "r", errors="replace") as f:
        log = f.read()

    events = []
    for match in SECTION_RE.finditer(log):
        event_type, timestamp, section_name = match.groups()
        events.append({
            "type": event_type,
            "timestamp": int(timestamp),
            "section": section_name.strip(),
        })

    # Compute durations per section
    sections = {}
    for ev in events:
        key = ev["section"]
        if key not in sections:
            sections[key] = {"start": None, "end": None}
        if ev["type"] == "start":
            sections[key]["start"] = ev["timestamp"]
        else:
            sections[key]["end"] = ev["timestamp"]

    result = []
    for name, times in sections.items():
        start = times["start"]
        end = times["end"]
        duration = (end - start) if (start and end) else None
        result.append({
            "section": name,
            "start": start,
            "end": end,
            "duration_seconds": duration,
        })

    # Sort by start time (None starts go last)
    result.sort(key=lambda s: s["start"] or float("inf"))
    print(json.dumps(result, indent=2))


# ---------------------------------------------------------------------------
# Subcommand: signals
# ---------------------------------------------------------------------------

def _strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text (color codes, clear-line, etc.)."""
    return re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', text)


def cmd_signals(args):
    """Extract sub-step timing signals from a log file, output JSON.

    The agent uses these signals as raw material for LLM-driven analysis:
    - commands: every $ line — what the CI script actually ran
    - downloads: go: downloading count — dependency fetch overhead
    - buildx_steps: Docker buildx step durations — build layer timing
    - tool_timings: self-reported timings from tools (golangci-lint, etc.)
    - sleep_occurrences: hardcoded sleeps — potential waste
    - cache_operations: cache restore/save/hit/miss lines
    """
    with open(args.log_file, "r", errors="replace") as f:
        lines = f.readlines()

    signals = {
        "commands": [],
        "downloads": {"count": 0, "sample": []},
        "buildx_steps": [],
        "tool_timings": [],
        "sleep_occurrences": [],
        "cache_operations": [],
    }

    # Patterns
    cmd_re = re.compile(r'\x1b\[32;1m\$ (.+)')
    download_re = re.compile(r'go: downloading (.+)')
    # Buildx DONE line: "#1 DONE 9.7s" (no description on same line)
    buildx_done_re = re.compile(r'^#(\d+)\s+DONE\s+([\d.]+)s')
    # Buildx description line: "#10 [linux/amd64 stage-1 1/4] FROM ..."
    buildx_desc_re = re.compile(r'^#(\d+)\s+\[.+')
    # Tool self-reported timings: "Execution took 33.06s", "took 1m22.11s", etc.
    # Capture the time unit (s/ms/m) to convert later.
    tool_timing_re = re.compile(r'(Execution took|took\s+|elapsed\s+|completed in\s+)([\d.]+)(s|ms|m)')
    sleep_re = re.compile(r'sleep\s+(\d+)')

    buildx_descriptions = {}  # step_num → description
    buildx_durations = {}     # step_num → duration (last DONE wins, it's the total)

    for i, line in enumerate(lines):
        stripped = line.strip()
        clean = _strip_ansi(stripped)

        # Command lines ($ ...) — keep ANSI stripped for readability
        cmd_match = cmd_re.search(line)
        if cmd_match:
            cmd_text = _strip_ansi(cmd_match.group(1)).strip()
            # Remove trailing [0;m artifacts
            cmd_text = re.sub(r'\[0;m$', '', cmd_text).strip()
            signals["commands"].append({
                "line": i + 1,
                "command": cmd_text[:200],
            })

        # go: downloading
        dl_match = download_re.search(clean)
        if dl_match:
            signals["downloads"]["count"] += 1
            if len(signals["downloads"]["sample"]) < 5:
                signals["downloads"]["sample"].append(dl_match.group(1))

        # Buildx step descriptions (collected separately, merged later)
        if clean.startswith('#') and buildx_desc_re.match(clean):
            step_match = re.match(r'^#(\d+)\s+(.+)', clean)
            if step_match:
                num = step_match.group(1)
                desc = step_match.group(2)
                if 'DONE' not in desc and num not in buildx_descriptions:
                    buildx_descriptions[num] = desc

        # Buildx step durations (collected separately, merged later)
        bx_match = buildx_done_re.match(clean)
        if bx_match:
            num, dur = bx_match.groups()
            buildx_durations[num] = float(dur)

        # Tool-specific timing output
        tt_match = tool_timing_re.search(clean)
        if tt_match:
            label, value_str, unit = tt_match.groups()
            value = float(value_str)
            # Normalize to seconds
            if unit == 'ms':
                value = value / 1000.0
            elif unit == 'm':
                value = value * 60.0
            signals["tool_timings"].append({
                "line": i + 1,
                "label": label.strip(),
                "duration_seconds": value,
                "context": clean[:200],
            })

        # Sleep occurrences (potential waste)
        sleep_match = sleep_re.search(clean)
        if sleep_match:
            # Only flag sleep as a standalone command, not inside a string
            if re.match(r'^\$ sleep\s+\d+', clean) or 'alias' not in clean:
                signals["sleep_occurrences"].append({
                    "line": i + 1,
                    "seconds": int(sleep_match.group(1)),
                    "context": clean[:200],
                })

        # Cache operations
        if 'cache' in clean.lower() and any(kw in clean.lower() for kw in ['restore', 'save', 'upload', 'download', 'hit', 'miss']):
            signals["cache_operations"].append({
                "line": i + 1,
                "context": clean[:200],
            })

    # Merge buildx descriptions and durations
    all_steps = set(buildx_descriptions.keys()) | set(buildx_durations.keys())
    for num in sorted(all_steps, key=int):
        signals["buildx_steps"].append({
            "step": int(num),
            "description": buildx_descriptions.get(num, ""),
            "duration_seconds": buildx_durations.get(num),
        })

    print(json.dumps(signals, indent=2))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="GitLab CI pipeline profiler")
    sub = parser.add_subparsers(dest="command", required=True)

    p_jobs = sub.add_parser("jobs", help="Fetch all jobs of a pipeline")
    p_jobs.add_argument("url", help="Pipeline URL")

    p_trace = sub.add_parser("trace", help="Fetch a job's trace log")
    p_trace.add_argument("url", help="Pipeline URL")
    p_trace.add_argument("job_id", help="Job ID")
    p_trace.add_argument("--output", help="Output file path (default: /tmp/gl_job_<id>.log)")

    p_sections = sub.add_parser("sections", help="Parse section timestamps from log")
    p_sections.add_argument("log_file", help="Path to job trace log file")

    p_signals = sub.add_parser("signals", help="Extract sub-step timing signals from log")
    p_signals.add_argument("log_file", help="Path to job trace log file")

    args = parser.parse_args()

    try:
        if args.command == "jobs":
            cmd_jobs(args)
        elif args.command == "trace":
            cmd_trace(args)
        elif args.command == "sections":
            cmd_sections(args)
        elif args.command == "signals":
            cmd_signals(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
