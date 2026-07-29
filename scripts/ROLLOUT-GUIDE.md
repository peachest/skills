# HTML Lesson Rollout Guide

Generic pipeline for batch-generating HTML lessons from note vaults using AFK subagents.
Reusable across skills (teach, and any future skill that generates HTML from notes).

## Pipeline Overview

```
scan-and-split-notes.sh  →  spawn subagents (AFK)  →  verify-workspaces.sh  →  analyze-css-classes.sh
       (step 1)               (step 2, skill-specific)       (step 3)                (step 4)
```

| Step | Script | Location | Skill-specific? |
|---|---|---|---|
| 1 | `scripts/scan-and-split-notes.sh` | shared | No — generic note scanner |
| 2 | subagent spawn + prompt template | skill's `afk-prompt-template.md` | **Yes** — prompt is the skill's domain logic |
| 3 | `scripts/verify-workspaces.sh` | shared | No — generic HTML workspace verifier |
| 4 | `scripts/analyze-css-classes.sh` | shared | No — generic CSS pattern analyzer |

## Boundary

**Shared scripts** (`skills/scripts/`): operate on files only, no domain knowledge.
They don't know what a "lesson" is — they just scan, copy, count, and grep.

**Skill-specific** (`skills/teach/`):
- `afk-prompt-template.md` — the prompt that tells subagents HOW to generate lessons
- `configs/teach-lab-workspaces.conf` — workspace split config (which notes → which workspace)
- `component-analysis-spec.md` — teach-specific analysis interpretation (what patterns mean)
- `CSS-CONVENTIONS.md` — teach's CSS component catalog

**To reuse for another skill**: write your own prompt template + workspace config.
The shared scripts don't change.

## Step 1: Scan and Split Notes

```bash
# Create workspace config (see configs/teach-lab-workspaces.conf for format)
# Then run:
bash scripts/scan-and-split-notes.sh ~/teach-lab configs/teach-lab-workspaces.conf
```

This creates `~/teach-lab/<workspace>/source-notes/` for each workspace,
classifies notes by filename keywords, and copies them in.

## Step 2: Spawn AFK Subagents

This step is skill-specific. For teach, see `afk-prompt-template.md`.

Key parameters:
- **Batch size**: 4 parallel subagents (balances throughput vs context window)
- **CWD**: set to workspace directory (e.g. `~/teach-lab/go-core`)
- **Model**: any model that can generate HTML (teach used GLM-5.2-FP8)
- **async**: true (fire-and-forget, wait for batch completion)

To use a **different model**, just change the `model` parameter in the subagent call:
```json
{
  "agent": "worker",
  "model": "anthropic/claude-sonnet-4",
  "cwd": "~/teach-lab/go-core",
  "task": "<prompt from afk-prompt-template.md>",
  "async": true
}
```

The prompt template is model-agnostic. Different models will produce different
CSS patterns and visual styles — this is desirable for diversity.

## Step 3: Verify Workspaces

```bash
bash scripts/verify-workspaces.sh ~/teach-lab
# Or check specific workspaces:
bash scripts/verify-workspaces.sh ~/teach-lab go-core go-eng
```

Reports lesson count, reference count, CSS class count, and token estimates per workspace.

## Step 4: Analyze CSS Patterns

```bash
# Without baseline (all classes):
bash scripts/analyze-css-classes.sh ~/teach-lab

# With baseline (filter out known classes):
bash scripts/analyze-css-classes.sh ~/teach-lab --baseline skills/teach/assets/base.css
```

Outputs:
- `_css-analysis.txt` — workspace|class pairs (raw)
- `_css-frequency.txt` — class frequency (sorted by workspace count)
- `_css-baseline-diff.txt` — candidates not in baseline (>=2 workspaces)
- stdout: CSS variable frequency + dark/light theme distribution

## Lesson Generation Results (teach #12)

| Metric | Value |
|---|---|
| Workspaces | 21 |
| Lessons generated | 95 |
| Unique CSS classes | 1124 |
| Analysis rounds | 3 (v1→v2→v3) |
| Components extracted to base.css | 27 |
| Models used | GLM-5.2-FP8 |

To generate more lessons with different models, repeat step 2 with a different
`model` parameter, then re-run steps 3-4 to discover new patterns.
