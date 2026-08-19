# Exploration Principles

Rules every exploration subagent must follow. Read before starting, obey throughout.

## Version pinning

1. Find the **latest release tag** (`git describe --tags`, `git tag --sort=-v:refname | head -5`). Checkout that tag. Record it as `ref` in every occurrence.
2. If the project has no release tags, find the **default branch** (`git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'`). Record the **commit hash** (`git rev-parse --short HEAD`) as `ref`.
3. If the latest tag is a pre-release (rc, alpha, beta, dev), use the latest **stable** tag instead. If no stable tag exists, fall back to default branch + commit hash.
4. Never explore on an arbitrary random commit. The ref must be reproducible — another agent should be able to checkout the exact same state.

## Dual mission

Each project spawns **two subagents** with different missions:

- **Subagent A — Pattern matcher**: Load `references/patterns-db.json`. For each existing pattern, check whether this project uses it. Record matches as new `occurrences` on existing patterns. Focus on: does this project use the pattern? Where? Any variation worth noting?
- **Subagent B — Pattern discoverer**: Explore the project's architecture freely. Find design patterns NOT yet in the database. Record them as new patterns with `is_new: true`. Focus on: what design decisions does this project make that we haven't seen before?

Both subagents are dispatched with `context: fresh` (prevents role confusion from inherited parent context) and `outputSchema` (forces structured JSON output as `{"findings": [...]}`). The schema is defined in `references/subagent-output.schema.json`. Subagents do NOT write to patterns-db.json — the parent session collects all results, validates against the schema, then merges into patterns-db.json in a single pass.

## Code references

Every pattern occurrence must include:

- `project`: project name (matching `projects` array in db)
- `ref`: the pinned version (tag or `commit:<short-hash>`)
- `file`: path relative to repo root
- `lines`: line range (e.g. `"75-100"`, or `""` if pattern spans the whole file)
- `snippet`: real source code excerpt from the file, showing the pattern. Trim imports and irrelevant branches, but keep original syntax and naming. No hard line limit — include enough context to understand the pattern, but stay concise.

Do not include full file contents. Do not guess architectures — read the code to verify. If a pattern match is uncertain, note it but do not fabricate a code reference.

For **new patterns**, include a `rationale` field answering "why this design choice" — separate from `description` which answers "what this pattern is".

## Read-only

Source repos are read-only. Never modify, commit, or push to explored repos. Checkout tags for reading only.

## Quality bar

- A pattern is worth recording if it is a **recurring design decision**, not a one-off hack. Ask: would another project reasonably adopt this?
- Surface the **design rationale** — why this choice, what problem it solves. A pattern without a "why" is just a code snippet.
- Prefer patterns that are **transferable** — designs that work outside the specific project's domain.
- Noise filter: ignore project-specific business logic, test fixtures, CI config, documentation formatting. Focus on structural design.

## Data contract

Each subagent is dispatched with `outputSchema` and `context: fresh`. Output is a JSON object `{"findings": [...]}`. The schema enforces field types and required keys, but cannot enforce conditional constraints (outputSchema limitation). Subagents must self-validate before completing.

### Self-validation before completion

Before calling `structured_output`, verify every finding satisfies these rules:
1. `matched_pattern_id` is a string like `"P001"` or `null`
2. `is_new` is boolean
3. If `is_new` is `false`: `occurrence` must be present, `new_pattern` must be `null` or absent
4. If `is_new` is `true`: `new_pattern` must be present (with name, dimension, description, rationale, occurrence), `occurrence` must be `null` or absent
5. Every `occurrence` has all 5 fields: project, ref, file, lines, snippet
6. `dimension` is one of: data-modeling, validation, error-strategy, pipeline-composition, interface-design, module-organization, plugin-architecture, config-management, serialization, sync-async, state-context

If any finding violates these rules, fix it before submitting. Do NOT submit partial or invalid output.

```json
[
  {
    "matched_pattern_id": "P001",
    "is_new": false,
    "occurrence": {
      "project": "attrs",
      "ref": "23.2.0",
      "file": "src/attr/_make.py",
      "lines": "420-460",
      "snippet": "..."
    },
    "variation_notes": "attrs uses __init_subclass__ instead of metaclass, but same principle of building at definition time"
  },
  {
    "matched_pattern_id": null,
    "is_new": true,
    "new_pattern": {
      "name": "Converter functions as field post-processors",
      "dimension": "data-modeling",
      "description": "...",
      "rationale": "...",
      "occurrence": {
        "project": "attrs",
        "ref": "23.2.0",
        "file": "src/attr/_make.py",
        "lines": "300-320",
        "snippet": "..."
      }
    }
  }
]
```

- `matched_pattern_id` non-null → matching an existing pattern. Include `variation_notes` if the project's usage differs interestingly from the original.
- `matched_pattern_id` null, `is_new` true → discovering a new pattern. Include full `new_pattern` with name, dimension, description, and at least one occurrence.
- Dimension must be one of the 10 dimensions defined in `patterns-db.json`. If a new dimension is needed, note it in `variation_notes` and flag for human review.

## Pattern reference format

When writing patterns to `data.md`, `flow.md`, `structure.md`, or `extension.md`, each pattern entry MUST follow this exact structure:

```markdown
### Pattern Name
`P021` · 33 occurrences · 20 projects: attrs, click, httpx, ...

**What**: One sentence describing the structural pattern.

**Recognize**: How to identify this pattern in code. List 2-4 concrete signals:
- Signal 1 (e.g. `class X(Protocol):` appears)
- Signal 2 (e.g. methods have type annotations but no body, just `...`)
- Signal 3

**Why**: Rationale for the design. Include trade-off: what benefit you gain, what cost you pay.

**When**: 1-2 sentences on when to use this pattern.

**When not**: 1-2 sentences on when NOT to use, or link to alternative pattern.

**Without this pattern** (anti-pattern):
```python
# ❌ Bad: what happens without the pattern
```

**With this pattern**:
```python
# project — file:lines
# ✅ Good: the pattern applied
```
```

### Field rules

1. **Header**: `### Pattern Name` — title case, concise, describes the design decision.
2. **Metadata line**: `` `P021` · N occurrences · M projects: list `` — exact format with middle-dot separators.
3. **What**: One sentence. No more than 30 words. Describes structure, not rationale.
4. **Recognize**: 2-4 bullet points. Each must be a concrete code-level signal: specific decorator, class structure, naming convention, import pattern, or type annotation shape. NOT abstract descriptions.
5. **Why**: Rationale + trade-off. Must mention at least one cost/negative. Format: "Benefit: ... Cost: ..."
6. **When**: Practical scenario, not theoretical. Mention a concrete use case.
7. **When not**: When the pattern is wrong. Reference alternatives by pattern ID when possible (e.g. "prefer P003 instead").
8. **Without this pattern**: Valid Python that compiles but represents the naive/anti-pattern approach. Must be syntactically correct.
9. **With this pattern**: Real source code from a project. Must include `# project — file:lines` comment. Pick the clearest occurrence from the DB.

### What NOT to do

- ❌ Skip any of the 7 required sections (What, Recognize, Why, When, When not, Without, With)
- ❌ Write abstract Recognize signals ("good code structure") — must be concrete code patterns
- ❌ Omit trade-off in Why — every pattern has a cost
- ❌ Use fake/fabricated code in the ✅ With section — must be real source
- ❌ Write more than 4 Recognize bullets — pick the strongest signals
- ❌ Include dimension headers inside pattern entries — the file-level header handles that

### Validation

Run `python3 scripts/validate_patterns.py references/*.md` to check format compliance before committing.

## Dimension awareness

The 11 existing dimensions:

1. `data-modeling` — how domain data is represented with types
2. `validation` — how inputs are validated and errors collected
3. `error-strategy` — fail-fast vs collect-all, error object design
4. `pipeline-composition` — how stages chain with type boundaries
5. `interface-design` — Protocol vs ABC, surface size, adapter patterns
6. `module-organization` — public vs internal, file granularity, import discipline
7. `plugin-architecture` — extension without modification, hook systems
8. `config-management` — layering, validation, merge semantics
9. `serialization` — object ↔ bytes/JSON conversion
10. `sync-async` — dual interface strategies
11. `state-context` — how context propagates implicitly through call chains

If a pattern spans multiple dimensions, pick the **primary** one and note the secondary in the description.
