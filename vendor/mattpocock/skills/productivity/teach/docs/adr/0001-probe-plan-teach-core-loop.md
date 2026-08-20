# ADR-0001: Probe-Plan-Teach as the core teaching loop

Date: 2026-08-20

## Status

Accepted

## Context

The vendor teach skill (mattpocock) has no assessment step — it infers the
learner's level from MISSION.md and learning-records, which in session one
are empty. This is a standing feature request upstream (#725) and the
commonest substantive complaint: "It never did grilling to establish my
starting point so it made lots of assumptions of what I already knew."

The skill also has no explicit teaching plan — it picks the next lesson
inside the ZPD but has no dependency graph, no frontier, no "when to stop."
Upstream docs admit: "good at making the next lesson, but not as good at
knowing when to stop."

Inspiration: Eero Alvar's "How I Use AI to Learn Things" video describes a
Probe → Plan → Teach loop that directly addresses both gaps.

## Decision

Evolve the teach skill's core loop from "infer → lesson" to
**Probe → Plan → Teach**, deeply integrated (not as a second mode).

- **Probe**: intake (decompose large subject into learnable subdomains,
  including execution paths / implementation / algorithms / boundaries for
  code projects) + calibration (graded quizzes + binary search to map
  understanding boundaries). Produces `UNDERSTANDING-MAP.md`.
- **Plan**: dependency graph with frontier + fog. Small topics → `PLAN.md`
  (Mermaid in workspace). Large topics → wayfinder map (issue tracker).
- **Teach**: traverse the graph one node at a time with quiz feedback. AFK
  batch generation is an execution strategy of Teach, not a separate mode.

## Consequences

- New artifacts: `UNDERSTANDING-MAP.md`, `PLAN.md`, `session-log/`.
- AFK batch pipeline (teach-lab) must produce the same artifact schemas;
  skill defines contract, teach-lab defines orchestration.
- Vendor SKILL.md will need revision to describe the three-phase loop.
- fact-check skill integrates at two points: after Plan (B) and after
  lesson generation (A).
- drawio-skill's validate.py + autolayout.py replaces "spawn a subagent to
  look at the diagram" for visualization self-check.
