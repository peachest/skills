---
name: ci-pipeline-profiler
description: "Profile GitLab CI pipeline durations: fetch job timings, drill into slow-job logs, read CI config, and produce a structured report with optimization suggestions. Use when the user says \"profile this pipeline\" / \"分析流水线耗时\" / \"why is my CI slow\" / \"CI pipeline too slow\" / pastes a GitLab pipeline URL and wants duration analysis."
disable-model-invocation: true
---

# CI Pipeline Profiler

**Leading word:** _profile_ — the act of measuring where time goes in a pipeline, then explaining why.

Given a GitLab pipeline URL, profile every job's duration, drill into the slow ones, read the project's CI config, and produce a markdown report with actionable optimization suggestions.

## Prerequisites

- Run from the project's local clone (the agent reads `.gitlab-ci.yml`, `Makefile`, `Dockerfile`, etc. from the working directory).
- `glab` CLI installed and authenticated (`GITLAB_TOKEN` or `GITLAB_PERSONAL_ACCESS_TOKEN` env var set).
- `python3` available (the helper script is stdlib-only).

## Flow

### Step 1: Collect job data

Run the helper script to fetch all jobs of the pipeline:

```bash
python3 <SKILL_DIR>/scripts/profile_pipeline.py jobs "<PIPELINE_URL>"
```

Output is a JSON array. Each job has `id`, `name`, `stage`, `status`, `duration`, `queued_duration`, `started_at`, `finished_at`, `allow_failure`.

**Completion criterion**: every job in the pipeline is accounted for — the JSON array length matches the pipeline's job count.

### Step 2: Identify the critical path and slow jobs

From the job data, compute:

1. **Wall-clock**: max `finished_at` − min `created_at` across all jobs.
2. **Critical path**: for each stage, the longest job; the chain of these across serial stages.
3. **Slow jobs** (drill-down trigger — either condition):
   - The job's `step_script` section exceeds **60 seconds**, or
   - The job's duration exceeds **30%** of wall-clock.

If no job meets either threshold, skip to Step 6 and produce a lightweight report (overview + job table + critical path only).

**Completion criterion**: critical path identified; list of slow jobs to drill into is decided.

### Step 3: Drill into slow jobs

For each slow job, chain three subcommands:

```bash
# 3a: Fetch the trace log
python3 <SKILL_DIR>/scripts/profile_pipeline.py trace "<PIPELINE_URL>" <JOB_ID> --output /tmp/gl_job_<JOB_ID>.log

# 3b: Parse GitLab section timestamps → per-section durations
python3 <SKILL_DIR>/scripts/profile_pipeline.py sections /tmp/gl_job_<JOB_ID>.log

# 3c: Extract sub-step signals (commands, downloads, buildx steps, tool timings, sleeps, cache ops)
python3 <SKILL_DIR>/scripts/profile_pipeline.py signals /tmp/gl_job_<JOB_ID>.log
```

Read all three outputs. The `sections` JSON tells you _where_ time goes at the GitLab level (prepare, get_sources, step_script, archive_cache…). The `signals` JSON tells you _what_ happened inside `step_script` — the raw material for bottleneck analysis.

**Completion criterion**: for every slow job, you have section durations + signal extraction loaded in context.

### Step 4: Read CI config files

Read the project's CI configuration from the working directory to understand _why_ the slow jobs are slow. Prioritize, in order:

1. `.gitlab-ci.yml` — the pipeline definition: stages, scripts, cache config, before_script.
2. `Makefile` / `makefile` — build targets invoked by CI (e.g., `make lint`, `make build-image-multiplatform`).
3. `Dockerfile` — multi-stage build structure, layer ordering, base images.
4. Any scripts referenced by the CI config (e.g., `startdocker.sh`, `hack/*.sh`).

Cross-reference: if `signals` shows `make lint` as a command and `tool_timings` shows "Execution took 48s", the `Makefile` tells you what `make lint` actually does (e.g., downloads golangci-lint, runs it, etc.).

**Completion criterion**: you can explain each slow job's `step_script` duration in terms of the config files that define it.

### Step 5: Analyze and synthesize

Combine the data from Steps 1–4 into bottleneck identification and optimization suggestions. This is the LLM-driven insight layer — the script gives you raw data, you provide the interpretation.

For each slow job:

1. **Section breakdown**: which GitLab section dominates (usually `step_script`).
2. **Sub-step breakdown**: from `signals`, estimate time for each sub-step (e.g., `go mod tidy` ~70s, `make lint-cache-clear` ~75s, `golangci-lint run` ~33s). These are estimates — derive from tool timings, download counts, and command sequence, not from precise per-command profiling.
3. **Bottleneck identification**: rank issues by impact:
   - 🔴 — critical path bottleneck (large, on the serial chain).
   - 🟡 — improvement space, not on critical path.
   - 🟢 — minor, recorded but not urgent.
4. **Optimization suggestions**: for each bottleneck, propose a specific fix with estimated savings (prefixed `~` to mark as rough estimate). Be concrete: name the file and line when possible (e.g., "移除 `.gitlab-ci.yml` 第 198 行的 `sleep 10`").

**Completion criterion**: every 🔴 and 🟡 bottleneck has a corresponding suggestion with an estimated saving.

### Step 6: Produce the report

Follow the report template at `<SKILL_DIR>/references/report-template.md`. The report is in Chinese. Key rules:

- **Adaptive depth**: if no slow jobs were found (Step 2), produce only the overview + job table + critical path. No deep analysis, no suggestion table.
- **Job table** sorted by start time, not duration. Mark the longest with 🔴最长, second with 🟡次长.
- **Critical path**: one or two lines — the chain of longest jobs per stage and the total.
- **Sub-step timings** are estimates — mark the table header as "估计耗时".
- **Suggestions** sorted by priority: 🔴 → 🟡 → 🟢.

Present the report to the user as markdown. Do not modify any project files — this skill produces analysis, not fixes.

**Completion criterion**: the report covers all jobs, identifies the critical path, and for each slow job provides section breakdown, sub-step estimates, bottleneck ranking, and actionable suggestions.
