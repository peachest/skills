# Output Structure

When this skill writes the directory tree, the result looks like this:

```
.scratch/
├── <research-document>.md            # original input (unchanged)
├── README.md                         # index — links to every epic and feature
├── 001-<milestone-1-slug>/
│   ├── epic.md                       # milestone overview (references/epic-template.md)
│   ├── <feature-1-slug>/
│   │   └── feature.md                # scoped input for to-prd (references/feature-template.md)
│   └── <feature-2-slug>/
│       └── feature.md
└── 002-<milestone-2-slug>/
    ├── epic.md
    └── <feature-3-slug>/
        └── feature.md
```

## README.md format

Write `.scratch/README.md` as:

```
# Epics

## Milestone 1: <title>

| Feature | File |
|---------|------|
| <name> | [`<slug>/feature.md`](<path>) |
| <name> | [`<slug>/feature.md`](<path>) |

## Milestone 2: <title>

| Feature | File |
|---------|------|
| <name> | [`<slug>/feature.md`](<path>) |
```

Then append a dependency section derived from each feature's `Dependencies` field:

```
## Dependency flow

<Milestone 1> → <Milestone 2>  (if milestone-to-milestone deps exist)
<Feature A> → <Feature B>      (feature-level dependencies)
```

If a feature declares no dependencies, state "can start immediately".

## Slug rules

- Milestone slugs are **three-digit prefix + English kebab-case**:
  `001-foundation`, `002-modal-tui`, `003-cli-tui`, `004-polish`.
- Feature slugs use English **kebab-case** derived from the Scope's core
  concept.
- **A Feature slug must never equal its parent milestone slug.** If template
  yields `modal-tui` for both milestone and Feature, pick a longer slug
  for the Feature: `core-modal` or `interactive-modal`.
- **Every Feature needs its own subdirectory** — even single-Feature
  milestones. Always `<feature-slug>/feature.md`, never just `feature.md`
  at the milestone level.