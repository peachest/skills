# ADR-0002: Navigation metaphor as agent skeleton, teaching vocabulary for learners

Date: 2026-08-20

## Status

Accepted

## Context

The skills repo has a shared navigation metaphor system (see
`~/skills/CONTEXT.md` — Navigation Metaphor): terrain, bearing, map,
frontier, fog of war, seam, landmark, waymark, gap, route. It spans
orient, wayfinder, review-spec, project-wiki, hail.

teach's Probe-Plan-Teach loop is structurally homologous to
orient → wayfind → traverse. But teach's audience includes human learners
who need plain language ("理解地图", "学习计划", "上课"), not military
navigation jargon ("bearing", "frontier", "fog of war").

## Decision

Adopt the navigation metaphor as the **agent's internal cognitive skeleton**
for reasoning about the teaching loop, but keep **teaching vocabulary** for
all learner-facing artifacts.

Mapping:
- Agent: orient → bearing  |  Learner: Probe → 理解地图 (UNDERSTANDING-MAP.md)
- Agent: wayfind → map     |  Learner: Plan → 学习计划 (PLAN.md)
- Agent: traverse → route  |  Learner: Teach → 上课 (lessons)

Cross-skill collaboration (teach calling orient/wayfinder) uses the shared
metaphor vocabulary without ambiguity.

## Consequences

- SKILL.md describes the loop in teaching terms; agent reasoning can invoke
  metaphor terms when coordinating with orient/wayfinder.
- CONTEXT.md glossary records both vocabularies and their mapping.
- A learner reading UNDERSTANDING-MAP.md sees "理解地图", not "bearing".
- When teach delegates large-topic planning to wayfinder, the map artifact
  uses wayfinder's native vocabulary (it lives on the tracker, not the
  workspace).
