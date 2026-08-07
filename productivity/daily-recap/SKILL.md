---
name: daily-recap
description: "Recap the day's pi sessions into a structured daily report saved to file — for 日报, weekly and monthly roll-ups. Use when the user asks to summarize or review their day's work — mentions recap, daily report, 日报, 总结今天的工作, 今天做了什么, what did I do today."
---

# Daily Recap

A **recap** turns the day's scattered sessions into a structured daily report — saved to file, grouped by project, ready for weekly and monthly roll-ups.

## Output

Write to `<recapDir>/<year>/<month>/<week>/<date>.md` — e.g., `~/.pi/recap/2026/08/W32/2026-08-05.md`. `<recapDir>` defaults to `~/.pi/recap/` (check `memory_search` for "recap output dir" for a user override). `<month>` is zero-padded, `<week>` is ISO week (`W32`, from `date +%V`), `<date>` is `YYYY-MM-DD`. Create directories with `mkdir -p`.

The file opens with a YAML frontmatter — `date`, `projects` (list), `sessions` (count), `work_sessions`, `subagent_sessions` — so future roll-up tools can scan metadata without parsing the body.

## Session kinds

- **Work session** — title does not start with `subagent-`. The user drove work here.
- **Subagent session** — title starts with `subagent-` (e.g., `subagent-worker-…`, `subagent-reviewer-…`). Spawned by a work session; counted as evidence of parallel work, not scanned independently.

## Steps

### 1. Gather

Sessions span midnight. List recent sessions with `session_list` (past 3 days, all projects), then keep those **created OR modified** on the target date — a session started on Aug 4 that runs past midnight has an Aug 5 mtime but belongs to Aug 4. Check both the creation timestamp (from the JSONL `session` event) and the file mtime (`stat -c %Y`), comparing each to the target date in the user's timezone. The target date defaults to today; accept a date argument for past days.

**Done when** every session file modified on the target date is identified — no session missed, no stale session included.

### 2. Triage

Split by title prefix: work sessions vs subagent sessions. Group work sessions by project (cwd). For each project, tally: work session count, total messages, tools used, subagent session count and roles (worker / reviewer / researcher / other).

Mark a work session **significant** at >5 messages — quick queries and title-generation sessions rarely exceed this. Sessions at 1-2 messages with no tools are **incidental**.

**Done when** every session is classified, every work session is in a project group and marked significant or incidental.

### 3. Scan

Fan out: one researcher subagent per project (scan in-session if only one project). Each subagent reads the **opening** (first user message — the task) and **closing** (last assistant message — the outcome) of each significant session, noting `ask_user_question` decisions and `todo` planned-vs-completed. Incidental sessions need only their title.

Each subagent returns a per-project summary. Collect and merge.

**Done when** every significant session has a one-sentence outcome; every incidental session has a label.

### 4. Synthesize

Write the recap file:

- **Frontmatter**: date, projects list, session counts (total / work / subagent)
- **Day overview**: 2-3 sentences on the day's theme across all projects
- **Per project**:
  - **Done** — what was accomplished (1-3 bullets)
  - **Decisions** — choices made (from `ask_user_question`, grilling, or explicit turns)
  - **Subagents** — count and roles of subagent runs

Save to the output path. Display the recap inline.

**Done when** the file is written to the correct path and the recap is displayed.
