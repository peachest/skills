---
name: academy
description: Orchestrate an academy — several teach courses sharing one mission, one OKB, and one asset library, taught by per-course herdr sessions. Manual entry point.
disable-model-invocation: true
argument-hint: "[academy] [course or action]"
---

The user invoked the academy layer: several teach courses under one umbrella topic, sharing one OKB, one asset library, and one mission. This session is the **academy session** — an orchestrator. It never teaches; course sessions do.

## Academy layout

An academy is a directory with an `ACADEMY.md` marker:

```
<academy-root>/            e.g. ~/teach-lab/llm-inference/
├── ACADEMY.md             academy mission (same spirit as a course MISSION.md)
├── CURRICULUM.md          cross-course map (see Curriculum)
├── okb/                   shared OKB: gold/<course-namespace>/…
├── assets/                shared lesson components (single source)
└── courses/<course>/      standard teach workspaces
```

Resolve the academy root from the argument (a path, `~/teach-lab/<argument>/`, or a human name matched against each `ACADEMY.md` title under the lab root), else by walking up from the cwd looking for `ACADEMY.md`.

Each course under `courses/` is a complete teach workspace; `teach` operates inside it with zero academy awareness. The academy layer owns only: shared `okb/`, shared `assets/`, `CURRICULUM.md`, and session routing.

## Roles

- **Academy session** (this one): surveys progress, routes the user to course sessions, creates and migrates courses, curates the shared layer. It never authors course content: after an incubation closes (N/N receipts) — or any time teaching is underway — it only orchestrates (CURRICULUM, routing, progress). Course-content questions (source-code checks, lesson-design verdicts, errata) take the correction path: verify with a fresh read-only subagent → send the verdict to the owning course session via `herdr agent prompt` → let it apply and report back. The academy relays verdicts, it does not produce technical analysis itself.
- **Course session**: one persistent herdr agent per course, named `teach-<course>` (agent names are lowercase ASCII — course dirnames are too), cwd = the course directory, running the teach loop interactively with the user. Reused across lessons. One active session per course at a time — lesson numbering is a filesystem resource.
- **Skills session** (the ~/skills repo session that authored this academy): owns the vendored teach fork and the academy skill. A course session that hits teach-skill friction reports it via herdr to the skills session and keeps teaching; the skills session lands the fix, runs the skill's tests, re-installs, and announces the change to the reporting session.

## Route a learning session

1. Survey: for each course in `courses/`, read `PLAN.md` (frontier), `UNDERSTANDING-MAP.md` (status summary), and the newest `session-log/*.md` (date). Present a compact overview: course / last session / frontier.
2. The user picks a course (or names one on invocation).
3. Find or create its session (next section), bootstrap it with today's goal, then point the user at the pane/tab.

Completion criterion: the user knows which pane holds the course session, and that session has received its bootstrap prompt. The academy session then steps back — teaching content never relays through it.

## Course session protocol

Find: `herdr agent list` → agent named `teach-<course>`. If present and not blocked, reuse it — the course files are the state; session memory is a bonus.

Create: one **tab** per course in the herdr workspace that already hosts this academy's course sessions — a new academy starts in the current workspace. `herdr tab create --cwd <course-dir>` (root pane hosts the agent, full screen for teaching, one-key switch between courses), then `herdr agent start teach-<course> --kind pi --pane <root-pane-id>`. The academy session stays in its own tab.

Bootstrap prompt (send and return — do **not** use `--wait`: its stdout carries only a `status` field, while the real receipt arrives asynchronously as an injected user message; waiting on stdout is idle wall-clock). Must include:
- `/skill:herdr` at the start — so the session knows its reply path back to this academy session
- the course directory (cwd is already set; have it confirm)
- `/skill:teach` to load, plus today's goal as the user stated it
- the shared layer paths: knowledge via its `RESOURCES.md` → `../../okb/`; components via `../assets/` (symlink to the academy assets)

## Create a course

Ask for the course mission first — a course without a mission gets teach's treatment: question the user before scaffolding anything. Then scaffold under `courses/<name>/` (ASCII, dash-case): `MISSION.md`, `RESOURCES.md` (pointers into `../../okb/<namespace>/`), `lessons/`, `session-log/`, `reference/`, `learning-records/`, and `assets` as a symlink → `../../assets`. Register the course in `CURRICULUM.md`. The course's first session runs Probe (teach's flow, unchanged).

## Incubate a topic

When the user arrives with a new subject to learn ("X has been released, I want to learn X and its lineage — research and assign lessons"), this is topic incubation: research, split into courses, batch-spawn sessions. Flow:

1. **Survey**: read `CURRICULUM.md` and existing courses' missions; note which existing courses the new topic extends (adjacency decides dependency notes later).
2. **Research**: search + extract primary sources (paper, tech report, release notes, credible deep-dives) and produce an evolution-mainline conclusion — what bottleneck each generation solved — not a link list. Index the sources into session knowledge; they land in RESOURCES later.
3. **Split by concept direction**: one direction = one course (MoE routing, latent attention, training infra, …), **not one topic per lesson** inside a single course. Mark the cross-course dependency mainline in `CURRICULUM.md` prose notes.
4. **Ask only decisions the user must own**: mission wording and split shape (one coarse course vs several direction courses). If the user declines the questions and instead injects a skill (e.g. multi-agent-collab), read that as the answer — in this lab the user chose multi-course dispatch by injecting the collab protocol — and proceed without re-asking.
5. **Scaffold in batch** (Create-a-course shape per course). Distribute the user's existing notes (`~/ai`, obsidian vaults, TOREAD lists) and any mid-flight articles they hand over into the right courses' RESOURCES — their open questions are Probe-start gold. Materials that arrive mid-incubation are routed the same way, not queued.
6. **Spawn one tab + `teach-<course>` session per course** (Course session protocol), bootstrap prompts sent in parallel (no `--wait` — receipts arrive as injected messages), each following the multi-agent-collab dispatch contract.
7. **Wait for every bootstrap receipt** (N/N), counted from the injected messages — not from any prompt stdout. Each course self-reports: workspace state, user-notes preread, planned Probe starting point. Chase late receipts (`herdr agent list` / prompt status) instead of assuming failure. A missing receipt means the course is not ready — do not declare done.
8. **Close**: memory note (series layout + tabs), summary table (tab / session / direction / Probe start), a recommended learning order (mainline first, others interleaved), then step back — sessions wait for the user, teaching never relays through the academy session.

Completion criterion: N/N receipts in hand, CURRICULUM registered, user knows which tab holds which course.

## Migrate an existing course

The notify-first protocol — a directory is never moved out from under a live session:

1. Locate any session currently managing the course (`herdr agent list`, match by title, cwd, or course name). Send advance notice via `herdr agent prompt`: start with `/skill:herdr`, state the new course path, and ask it to confirm it is idle. Wait for the ack before moving anything.
2. Move: `mv <course> <academy-root>/courses/<name>` (ASCII dash-case name; state the rename in the notice when there is one).
3. Lift a course-local `okb/` into the academy OKB (merge, keep its namespace) and rewrite that course's `RESOURCES.md` pointers to `../../okb/…`.
4. Dedupe assets: verify the academy `assets/` union covers the course's, then replace the course's `assets/` dir with a symlink → `../../assets`. Lessons keep their `../assets/…` links — they resolve through the symlink.
5. Register the course in `CURRICULUM.md`.
6. Notify the managing session of the new path and ask it to `cd` there.
7. Verify: every `RESOURCES.md` link resolves, and a spot-check of lesson HTML `../assets/` links resolves.

Completion criterion: all seven steps done, and the managing session (if any) acks from the new path.

## Curriculum

`CURRICULUM.md` is the cross-course map. Its format is deliberately minimal — course-level nodes with prose notes for cross-course dependencies (e.g. "tp-cp needs sglang-pp's source anchors") — until practice shows which edges matter. Enrich it when real cross-course references appear; do not invent a heavyweight schema ahead of that evidence. The long-term shape is a drillable layered graph: framework mechanisms (pp, spec-decoding, tp) → engine implementations (sglang, vllm) → cuda programming → gpu architecture, with math foundations (statistics, calculus, linear algebra) hanging off wherever they are actually needed.

## Shared layer

- **OKB**: one per academy, namespaced by course or topic (`okb/gold/sglang-pp/`, `okb/gold/spec-decoding/`, …). Curation (ingest → distill → gold) follows the `okb` skill, unchanged; a course triggers it when its `RESOURCES.md` is thin.
- **Assets**: single source at the academy root. Courses hold only the symlink, never real asset files; new reusable components land in the academy `assets/`.
- **Designed later, on demand**: cross-course scheduling (what to learn today), fine-grained cross-course dependency edges, and course→academy progress reporting. When the user asks for any of these, design it against real usage then.
