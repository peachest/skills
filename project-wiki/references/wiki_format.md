# Wiki Format Reference

Detailed format specification for L1, L2, and L3 wiki files.

## L1: overview.md

```markdown
<!-- module_id: overview -->
<!-- desc: Project overview — module index and responsibilities -->

# Project Overview

> L1 knowledge base entry point. Each module links to its L2 detail wiki.
> Keep this file under 5KB — it's loaded into every AI context window.

## Module Index

| Module | Responsibility | Detail Wiki |
| ------ | -------------- | ----------- |
| `auth` | Authentication, JWT issuance, session management | [auth.md](auth.md) |
| `mail` | Mail list, rendering, composition, send/receive | [mail.md](mail.md) |
| `model` | Domain models, DB persistence, business managers | [model.md](model.md) |

## Statistics

- Total modules: 3
- Total source files: 142
- Last updated: 2026-07-26 12:00 UTC
```

### Rules

- **Size**: under 5 KB. If it grows, split modules or trim descriptions.
- **One row per module**: name in backticks, one-line responsibility, link to L2.
- **No file listings here** — that's L2's job. L1 is a directory, not a store.

## L2: `<module>.md`

```markdown
<!-- module_id: auth -->
<!-- root_dirs:
  - src/auth/
  - internal/auth/
-->
<!-- desc: Authentication, JWT issuance, session management -->

# Module: auth

> L2 knowledge base — file-level registration for the `auth` module.

## File Registration

| File | Description |
| ---- | ----------- |
| `src/auth/login.go` | **Login handler** — validates credentials, issues JWT |
| `src/auth/logout.go` | **Logout handler** — invalidates session, clears token |
| `src/auth/middleware.go` | **Auth middleware** — JWT verification for protected routes |
| `src/auth/token.go` | **Token utilities** — JWT signing, parsing, refresh logic |

## Statistics

- Source files: 4
- Total lines: 520
```

### Metadata header

Three HTML comments at the top, machine-readable:

| Field | Purpose | Example |
| ----- | ------- | ------- |
| `module_id` | Module identifier (matches filename without `.md`) | `auth` |
| `root_dirs` | Directory roots this module covers (one `- path/` per line) | `src/auth/` |
| `desc` | One-line responsibility | `Authentication, JWT issuance` |

### File registration table

- **Two columns**: File path (in backticks) and Description.
- **Description format**: `**Bold role** — specifics`. One line.
- **Every source file in the module must be registered** — the table is exhaustive.
- Placeholder before filling: `<describe filename>`.

### How descriptions should read

Good:
```
| `src/auth/login.go` | **Login handler** — validates credentials, issues JWT |
```

Bad (too vague):
```
| `src/auth/login.go` | handles login |
```

Bad (too long):
```
| `src/auth/login.go` | This file contains the login handler which validates user credentials against the database and issues a JWT token with a 24-hour expiration. It also handles rate limiting and failed attempt tracking. |
```

## L3: Semantic bridges (optional, hand-curated)

L3 has two sources:

1. **domain-modeling integration** (auto-detected by `init`): If
   `CONTEXT.md` exists at the project root or `docs/adr/` contains ADR
   files, `init` links them from `overview.md` in a Domain Language
   section. These are typically produced by `/skill:domain-modeling`.
   project-wiki links to them but never generates or modifies them.

2. **Hand-curated mapping files** in `docs/project_wiki/`: user-created
   vocabulary bridges between external systems and code. Examples below.

### glossary.md

Maps product/business language to code identifiers:

```markdown
# Glossary

> Product terms → Code identifiers. Bridges the semantic gap.

| Product term | Code identifier | Location |
| ------------ | ---------------- | -------- |
| "小红条" (red bar) | `TipsView` | `src/ui/tips_view.go` |
| "邮件红点" (mail badge) | `setMailboxBadgeValue` | `src/mail/badge.go` |
| "全选" (select all) | `selectAllItems` | `src/mail/list_controller.go` |
```

### api_mapping.md

Maps external API fields to internal types:

```markdown
# API Mapping

> External API → Internal types and handlers.

| API field | Internal type | Parser | Notes |
| --------- | ------------- | ------ | ----- |
| `is_show_warning` | `WarningConfig.ShowIcon` | `Config.parse()` | Bool, default false |
| `mail_count` | `Mailbox.Count` | `Mailbox.fromProto()` | Int32 |
```

### design_token_mapping.md

Maps design system tokens to code:

```markdown
# Design Token Mapping

> Figma/design tokens → Code implementation. Prevents hardcoded values.

| Token | Code | Type | Notes |
| ----- | ---- | ---- | ----- |
| `Mobile/title_1` | `TextStyle.Heading1` | Font | 24px / Bold |
| `Base/gray_100` | `Color.Gray100` | Color | Auto dark-mode variant |
| `button_blue_large` | `Button.Primary.Large` | Component | Standard CTA |
```

## .review_cache.json

Gitignored. Not for human editing. Structure:

```json
{
  "files": {
    "src/auth/login.go": {
      "sha": "a1b2c3d4...",
      "module": "auth",
      "reviewed": true
    }
  },
  "last_updated": "2026-07-26T12:00:00+00:00"
}
```

- `sha`: SHA1 of file content at last review.
- `reviewed`: `true` after `update`, `false` for newly tracked files.
- `last_updated`: ISO timestamp of last `update` run.
