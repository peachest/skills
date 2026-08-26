---
name: dynamic-workflow
description: >-
  Design multi-agent workflows the Unix way: agents as CLI commands, shell
  primitives as the orchestrator, files as the message bus. Use when the user
  asks to design, architect, or orchestrate a multi-agent workflow — parallel
  or serial sub-agents, chained agent outputs, deep-research or review
  pipelines — or when a workflow design proposes a DSL, engine, or custom
  runner. Answer with a shell script.
---

# Dynamic Workflow (Unix-native)

A sub-agent CLI call *is* `agent()`. Unix `&` and `wait` *are* parallel and
serial orchestration. File redirection `>` *is* the node-to-node message bus.
**Put the agent back into the CLI, hand the rest to Unix** — the most minimal
Dynamic Workflow implementation is the shell you already have.

## The three primitives

| Dynamic Workflow concept | Unix equivalent |
| --- | --- |
| `agent()` — hand a subtask to an agent | a CLI command: natural-language task in, stdout out |
| parallel / serial orchestration | `&` + `wait` / `&&` / `|` |
| node-to-node communication | files (`>` redirect), stdout, stdin |

## Design steps

Work through these in order. Each step ends with a completion criterion —
meet it before moving on.

### 1. Decompose into agent nodes

Split the task into sub-agents. Each node is **one CLI invocation**: an agent
name, a natural-language task, and a declared output.

```bash
<subagent-cli> researcher --task "study AI agent patents"
```

**Completion:** every sub-task is expressible as one `<subagent-cli> --task "..."` line; no node depends on another node's in-memory state.

### 2. Wire nodes with files

The output file of one node is the input context of the next. Files are the
only API — every language, every tool, every agent can read them.

```bash
<subagent-cli> researcher --task "..." > /tmp/raw.md
<subagent-cli> writer --task "synthesize /tmp/raw.md into a report" > /tmp/report.md
```

**Completion:** every inter-node dependency is a file path or stdout; there is no message schema, no structured protocol, no shared store.

### 3. Orchestrate with shell primitives

- **Parallel** → launch with `&`, join with `wait`
- **Serial** → chain with `&&` or `|`
- **Skip done work** → guard with `[ -f output ] ||`

```bash
# parallel
<subagent-cli> researcher_a --task "..." > /tmp/a.md &
<subagent-cli> researcher_b --task "..." > /tmp/b.md &
wait

# serial
<subagent-cli> step1 --task "..." > /tmp/s1.md && \
<subagent-cli> step2 --task "use /tmp/s1.md" > /tmp/s2.md

# resume without redoing finished stages
[ -f /tmp/s1.md ] || <subagent-cli> step1 --task "..." > /tmp/s1.md
```

**Completion:** every `&` has a matching `wait`; ordering is explicit (`&&` on the line that must finish first); re-running the script skips stages whose output file already exists.

### 4. Give each node a real file

Redirect every node's stdout to the file its consumers read. Name files after
the node's contract, not after the pipeline stage.

```bash
<subagent-cli> market_researcher --task "..." > /tmp/market.md
<subagent-cli> patent_analyst   --task "..." > /tmp/patents.md
```

**Completion:** every node writes exactly one file that at least one downstream node (or the final deliverable) reads; no node reads a sibling's in-memory output.

### 5. Verify the workflow runs

Execute the assembled script end to end before calling it done.

**Completion:** the script runs green with all expected files produced; interrupting and re-running it resumes with the same result.

## Templates

### Parallel research → serial synthesis

```bash
# Stage 1 — three agents in parallel
<subagent-cli> patent_analyst \
  --task "analyze recent AI-agent patents" > /tmp/patents.txt &
<subagent-cli> market_researcher \
  --task "research AI-agent market size and competition" > /tmp/market.txt &
<subagent-cli> literature_reviewer \
  --task "survey 2025-2026 AI-agent papers" > /tmp/papers.txt &
wait

# Stage 2 — one agent consumes all three files
<subagent-cli> report_writer \
  --task "write a comprehensive report from /tmp/patents.txt, /tmp/market.txt, /tmp/papers.txt" \
  > /tmp/final_report.md
```

### PR review

```bash
<subagent-cli> code_reviewer --task "review this PR" > /tmp/review.md
<subagent-cli> fix_agent --task "apply findings from /tmp/review.md" > /tmp/fix_summary.md
```

### Scheduled (cron)

```bash
0 8 * * * /path/to/workflow.sh
```

## When this skill applies

Reach for it when the task **composes multiple agents** — research, review,
analysis, generation — into one runnable flow. Its core is: **the CLI is a
first-class agent interface; Unix primitives already express the workflow.**
Use DSL-free naming: a workflow *is* a shell script; an agent *is* a CLI
command; a pipeline *is* a composition of commands.