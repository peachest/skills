---
name: to-epic
description: >
  Break a product research document into milestone-level epics and per-feature specs.
  Produces a two-level directory tree (.scratch/milestone/feature/) where each feature.md
  is a scoped input for to-prd. Use when user says "start a new project" /
  "break this down into phases" / "create epics" / "to epic" / "分解阶段" / "创建里程碑".
  Only produces epics and features. Do NOT write PRDs or issues.
---

# To Epic — Milestone → Feature Pipeline

Parse a product research document from `.scratch/`, identify development milestones (MVP,
Phase 2, …), and decompose each milestone into features. Each milestone gets a directory
tree with a milestone-level epic.md and one feature.md per feature inside it.

Input document must already contain competitive analysis, tech-stack rationale, architecture
overview, and a phased roadmap.

Pipeline position:

```
idea.md → to-epic → feature.md → to-prd → PRD.md → to-issues → issues/
                ↘ epic.md (milestone overview, human-facing)
```

## Process

### 1. Gather context

Read the research document from `.scratch/`. If the user hasn't placed one, ask them to.

If the project has a `CONTEXT.md` and `docs/adr/`, read them to understand domain vocabulary.
Epic and Feature titles should speak the project's language.

**Ensure issue tracker is configured.** Read `docs/agents/issue-tracker.md`. If it
lacks a `## Milestone / Feature — to-epic` section, run the skill at
`setup-to-epic/SKILL.md` first (discoverable as "setup-to-epic"). This appends
the directory conventions so that to-prd and to-issues also understand the
two-level structure.

- [ ] Research document read
- [ ] CONTEXT.md / docs/adr/ read (if present)
- [ ] issue-tracker.md verified (or setup-to-epic run)

### 2. Identify milestones

Parse the phased roadmap. For each phase, identify a **milestone** (thematic container).

Present milestones as a single table — one row per milestone, one sub-table per
Feature within it. Show Scope, Rationale, and Dependencies for each Feature.

Ask the user:

- Does the milestone split look right? Should any be merged, split, added, or removed?
- Are the Features correctly scoped? Are the dependencies right?
- Are there cross-milestone dependencies that affect ordering?

**Do not proceed until the user approves.** Iterate until the user is satisfied.
Combine all questions into one message — do not ask one-at-a-time.

- [ ] User confirmed all milestones and features

### 3. Write files

For each approved milestone, write the structure below. Read the templates from
`references/`.

**Output template:** Read references/output-structure.md for the exact
directory layout and slug rules.

- [ ] epic.md written for each milestone
- [ ] feature.md written for each feature

**Redirect small items to the backlog.** During milestone identification you
may notice tasks too small for a Feature (e.g. "add unit tests for tracker.ts",
"extract shared render helpers"). Collect them. After the user confirms
milestones and Features, run the skill at `to-backlog/SKILL.md` to append
these items to `.scratch/backlog.md`. If `backlog.md` does not exist yet,
suggest a category list to the user.

- [ ] Known small items added to backlog (via to-backlog)

### 4. Generate the index

Write `.scratch/README.md` listing all milestones and their features with links.
Read references/output-structure.md for the README.md format and dependency flow section.

- [ ] README.md written with index and dependency flow

---

## When templates are needed

- **Milestone epic.md**: references/epic-template.md
- **Feature feature.md**: references/feature-template.md
- **Guiding principles**: references/principles.md