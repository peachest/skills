# ADR-0003: drawio-skill for visualization self-check

Date: 2026-08-20

## Status

Accepted

## Context

teach lessons for technical topics (KVCache, k8s-scheduling, Go internals)
need structural diagrams: dependency graphs, architecture diagrams, data
flow, sequence diagrams. The video inspiration showed a "generate → look →
edit → look again" cycle for SVG visualizations.

Three visualization tools were evaluated:
- **Flint Chart** (Microsoft): statistical data visualization (bar/line/
  heatmap/sunburst). Data → chart. MCP-based. Wrong domain.
- **Lieflat Charts**: monochrome data viz, 48 HTML/SVG templates.
  Statistical charts. PolyForm Noncommercial license. Wrong domain.
- **drawio-skill** (Agents365-ai): structural diagrams (architecture/UML/
  ER/flowchart/sequence/network topology). .drawio XML → PNG/SVG/PDF.
  Has validate.py (dangling edges, duplicate IDs, overlap) + autolayout.py
  (Graphviz). MIT license.

## Decision

Use **drawio-skill** for teach's visualization self-check (D7).

- Lessons containing `.drawio` automatically run validate.py + autolayout.py.
- Structural correctness (dangling edges, duplicate IDs) checked
  mechanically, not by LLM "looking at" the diagram.
- Visual clarity (overlap, layout) handled by Graphviz autolayout.
- No separate "spawn a subagent to describe the SVG" step — drawio-skill's
  tooling is more reliable than LLM vision for structural diagrams.

## Consequences

- teach skill references drawio-skill as the diagram tool for complex
  visualizations.
- Simple KaTeX formulas (already in base.css) are not subject to viz-check.
- fact-check (claim-level) and viz-check (structural/visual) are orthogonal
  — both run on lessons with diagrams, checking different things.
- teach-lab's AFK pipeline can batch-run validate.py across generated
  lessons.
