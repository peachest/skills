# CSS Conventions

Reference for authoring teach lessons and reference documents. Load this when creating or styling HTML.

## Stylesheet

The canonical stylesheet is `skills/teach/assets/base.css`. Each workspace copies it to `./assets/base.css`. Every lesson and reference document links it:

```html
<link rel="stylesheet" href="../assets/base.css">
```

## CSS Variables

Defined in `:root`, overridden in dark mode. Full token system is specified in `DESIGN.md`.

### Font families

| Variable | Purpose |
|---|---|
| `--font-voice` | Body/voice font (serif) — Georgia, Songti SC, … |
| `--font-ui` | Heading/UI font (sans) — -apple-system, PingFang SC, … |
| `--font-mono` | Code font — SF Mono, Fira Code, … |
| `--serif`/`--sans`/`--mono` | Aliases of the above (backward compat) |

### Font-size scale (tokenized — no bare `font-size`)

Nine levels consolidate the former 19 ad-hoc rem/px/pt values. **Always reference a token; never write a literal `font-size`.**

| Token | Size | Use |
|---|---|---|
| `--fs-display` | 2.75rem | Lesson big title (use `clamp(2rem,5vw,2.75rem)` for fluid) |
| `--fs-h1` | 1.75rem | Chapter title |
| `--fs-h2` | 1.4rem | Section |
| `--fs-h3` | 1.2rem | Subsection |
| `--fs-h4` | 1.05rem | Paragraph lead / subtitle |
| `--fs-body` | 1rem | Body text (default) |
| `--fs-body-lg` | 1.125rem | Lead / emphasis paragraph |
| `--fs-small` | 0.875rem | Secondary text |
| `--fs-caption` | 0.75rem | Metadata / tags / labels (tracked) |
| `--fs-code` | 0.9rem | Code blocks |

**Exception:** inline `code` and `.comment` use `0.88em` (relative) so they scale with the parent heading — em is correct there, do not replace with a fixed token.

### Line-height scale

`--lh-display`(1.2) / `--lh-h1`(1.3) / `--lh-h2`(1.35) / `--lh-h3`(1.4) / `--lh-h4`(1.45) / `--lh-body`(1.75) / `--lh-small`(1.5) / `--lh-code`(1.5).

### Colors

| Variable | Purpose | Light default |
|---|---|---|
| `--bg` | Page background | #ffffff |
| `--surface` | Card/container background | #ffffff |
| `--text` | Body text | #1a1a1a |
| `--muted` | Secondary text | #6b6b6b |
| `--light` | Tertiary text | #999 |
| `--accent` | Link color | #0366d6 |
| `--accent-bg` | Link/selection tint | #0969da14 |
| `--brand` | Brand fill (Claude lineage) | #d97757 |
| `--brand-emphasized` | Brand hover/press | #c6613f |
| `--border` | Border color | #e1e4e8 |
| `--code-bg` | Code background | #f6f8fa |
| `--green`/`--red`/`--orange`/`--purple`/`--teal` | Semantic colors | GitHub-style palette |
| `--*-bg` | Semantic tints (e.g. `--green-bg`) | GitHub-style palette |

## Typography

Body uses `--font-voice` with `font-feature-settings: "pnum" on, "lnum" on, "liga" on` (proportional + lining numerals + ligatures) for tidy mixed CJK/Latin/digit rendering. Headings use `--font-ui`.

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
