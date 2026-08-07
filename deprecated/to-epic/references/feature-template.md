# Feature feature.md Template

```
# <Feature Title>

## Scope

<2-3 sentences describing what this Feature delivers>

## Rationale

<why this Feature comes now, not later — value, risk, prerequisite>

## Acceptance criteria (high level)

- <Feature-level acceptance condition — not user stories>
- <Another condition>
- <e.g. "Users can add/list/remove wishlist entries", not "as a user I want a button">

## Dependencies

- <feature name or "none">

## Source sections in research document

- §x — <section title>
- §y — <section title>
```

**Guidelines:**

- A feature.md is a **scope confirmation gate** — keep it lean. Do NOT include
  current-state analysis, file-level status, user story lists, or implementation
  decisions. Those belong in the PRD step.
- **Acceptance criteria** are high-level boundaries, not user stories. They answer
  "how do we know this Feature is done?" at the Feature level.
- The **Scope** and **Acceptance criteria** together give to-prd enough context to
  write a focused PRD without re-reading the entire research document.