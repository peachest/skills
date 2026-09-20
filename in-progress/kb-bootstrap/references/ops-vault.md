# Ops diagnosis vault — bootstrap reference

For recurring diagnosis work worth re-consulting: cluster bugs, GPU-virtualization failures, k8s internals — anything where a future bug resembles a past one.

## 1. Mission doc → `~/handoff/ops-vault.md`

One paragraph: the domains the vault covers, the labels taxonomy source (start from the domain's recurring failure classes), who reads it (agents running diagnosis).

## 2. Scaffold

```
~/ops/
├── labels.md          # taxonomy: label + one-line definition + when to apply
├── index.md           # grouped list of diagnoses by label/topic
└── <slug>.md          # one file per finished diagnosis (diag-write owns the format)
```

- `labels.md` is the load-bearing file — search quality depends on consistent labels, and labels only stay consistent when defined once, here.
- Do not seed placeholder diagnoses; an empty vault with a real taxonomy beats a fake one.

## 3. Handover

Bootstrap stops at the empty tree. Diagnosis **runs** belong to `diagnosing-bugs-with-docs`; writing a finished diagnosis to the vault belongs to `diag-write` (template, labels, index update); retrieving prior diagnoses belongs to `diag-search`. The vault is live when the first real diagnosis lands via `diag-write`.

Pointer: global `~/.pi/agent/AGENTS.md` read-trigger (run `diag-search` before hypothesizing on an ops-domain bug), unless the vault is scoped to one project — then that project's AGENTS.md.
