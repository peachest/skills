# CSS Conventions

Reference for authoring teach lessons and reference documents. Load this when creating or styling HTML.

## Stylesheet

The canonical stylesheet is `skills/teach/assets/base.css`. Each workspace copies it to `./assets/base.css`. Every lesson and reference document links it:

```html
<link rel="stylesheet" href="../assets/base.css">
```

## CSS Variables

Defined in `:root`, overridden in dark mode:

| Variable | Purpose | Light default |
|---|---|---|
| `--serif` | Body font | Georgia, Songti SC, serif |
| `--sans` | Heading font | -apple-system, PingFang SC, sans-serif |
| `--mono` | Code font | SF Mono, Fira Code, monospace |
| `--bg` | Page background | #ffffff |
| `--surface` | Card/container background | #ffffff |
| `--text` | Body text | #1a1a1a |
| `--muted` | Secondary text | #6b6b6b |
| `--accent` | Link/brand color | #0366d6 |
| `--border` | Border color | #e1e4e8 |
| `--green`/`--red`/`--orange`/`--purple`/`--teal` | Semantic colors | GitHub-style palette |

## Dark Mode

Automatic via `prefers-color-scheme: dark`, or per-lesson override by adding `.dark` class to `<html>` or `<body>`. To force light mode, add `.light` class.

## Component Catalog

Use these class names as-is. For semantic variations, use CSS variables (e.g. `style="border-left-color: var(--purple);"`) rather than inventing new classes.

| Category | Classes |
|---|---|
| Callouts | `.callout` + `.callout-note/-tip/-warning/-success/-danger` |
| Quiz | `.quiz-container` > `.quiz` + `.quiz-section/-question/-option/-feedback/-score` |
| Compare | `.compare-grid` > `.compare-card`, `.compare-table` |
| Pipeline | `.pipeline` > `.pipeline-stage` + `.pipeline-arrow` |
| Flow chart | `.flow-diagram` > `.flow-box` + `.flow-arrow` + `.flow-row` + `.flow-step` + `.flow-num` |
| Timeline | `.timeline` > `.timeline-item` + `.timeline-title` + `.timeline-desc` |
| Steps | `.step-list` (auto-numbered), `.stage-num` + `.stage-name` + `.stage-desc` |
| Architecture | `.arch-layer` + `.arch-arrow` |
| Matrix | `.matrix-grid` > `.matrix-cell` + `.matrix-label` |
| Code | `.code-block` + `.keyword`/`.string` syntax highlight, `.code-compare` (diff) |
| Formula | `.formula-box` (KaTeX container) |
| File tree | `.tree` (generic) > `.tree-node`/`.tree-leaf`, `.file-tree` > `.dir`/`.file` |
| Cards | `.tech-card` + `.tech-badge` |
| States | `.selected`, `.show`/`.hidden`, `.good`/`.bad`/`.new` |
| Inline | `.badge`, `.highlight`, `.label`, `.comment`, `.tag`, `.arrow`, `.ref-link` |

## Domain-Specific Styles

For components not in base.css, use inline `<style>` in the lesson. Extract to base.css when the same pattern appears in ≥2 workspaces.

## KaTeX

Opt-in per workspace. Copy `katex.min.css`, `katex.min.js`, `auto-render.min.js`, `render.js` to `./assets/` and add `<script>` tags to lessons that need math.

## Reference Document Styling

Reference documents follow the same conventions as lessons:

- Link `../assets/base.css` (same stylesheet as lessons)
- Use the component library — use `.compare-table`, `.compare-card`, `.badge`, `.callout`, etc. rather than plain `h2/h3/p` stacks
- Match the workspace's theme: if lessons use `.dark`, reference docs should too
- Glossaries: `.compare-table` for term comparison, `.badge` for version/category tags, colored borders for grouping
- Cheatsheets: `.compare-grid` for side-by-side patterns, `.code-block` for snippets, `.callout-warning` for gotchas

Reference documents are the documents users return to most — make them visually rich, not text walls.
