---
name: vscode-extension
description: >
  Full-lifecycle VS Code extension development skill. Covers project scaffolding,
  extension development (commands, views, webviews, language features, AI
  extensibility), building, bundling, testing, packaging, and publishing to the
  VS Code Marketplace. Use this skill whenever the user asks to create a VS Code
  extension, work on an existing one, scaffold a new extension project, build or
  package an extension, publish or update an extension on the marketplace, add
  commands/tree views/webviews/settings to VS Code, implement language features
  (syntax highlighting, snippets, LSP), add AI chat participants or language
  model tools, debug extension issues, or set up CI/CD for an extension — even
  if they only mention &quot;vscode extension&quot;, &quot;vs code plugin&quot;, &quot;extension
  development&quot;, or &quot;marketplace publish&quot;.
compatibility:
  - Node.js 18+
  - npm or yarn
  - yo (yeoman) + generator-code
  - vsce (VS Code Extension Manager)
  - "@vscode/test-cli"
---

# VS Code Extension Development

A full-lifecycle skill for VS Code extension development. Bundled documentation
(`docs/`) contains raw HTML scraped from the official docs — use it instead of
your training data when exact schemas, API signatures, or current behavior
matter.

<!-- INDEX is the entry point for the user; skill users read from docs/INDEX.md -->
Read `docs/INDEX.md` for the complete file catalog (76 files across 9 categories).

---

## How to Use This Skill

The table below maps user intents to the doc file to read. **Don't inline large
code blocks here** — the doc files have complete, up-to-date examples.

| If the user wants to... | Read `docs/...` |
|---|---|
| Create a new extension project | `getting-started/your-first-extension.md` |
| Understand extension structure | `getting-started/extension-anatomy.md` |
| Register a command | `guides/command.md` |
| Add a tree view / sidebar | `guides/tree-view.md` |
| Build a WebView (HTML/CSS/JS) | `guides/webview.md` |
| Add settings/config | `capabilities/common-capabilities.md` |
| Implement custom editor | `guides/custom-editors.md` |
| Add a notebook type | `guides/notebook.md` |
| Integrate with source control (SCM) | `guides/scm-provider.md` |
| Add a debugger | `guides/debugger-extension.md` |
| Add task provider | `guides/task-provider.md` |
| Add a Chat Participant (`@foo`) | `ai/chat.md` |
| Register LM tools | `ai/tools.md` |
| Use language model in extension | `ai/language-model.md` |
| Implement MCP support | `ai/mcp.md` |
| Build with Prompt TSX | `ai/prompt-tsx.md` |
| Syntax highlighting | `language/syntax-highlight-guide.md` |
| Code snippets | `language/snippet-guide.md` |
| LSP integration | `language/language-server-extension-guide.md` |
| Bundle the extension | `publishing/bundling-extension.md` |
| Test the extension | `testing-extension.md` (also `guides/testing.md`) |
| Publish to Marketplace | `publishing/publishing-extension.md` |
| Set up CI/CD | `publishing/continuous-integration.md` |
| Learn UX best practices | `ux-guidelines/overview.md` |

For **reference lookups** (activation events, contribution points, API docs):

| Topic | Read `docs/...` |
|---|---|
| Activation events | `references/activation-events.md` |
| All contribution points | `references/contribution-points.md` |
| package.json manifest schema | `references/extension-manifest.md` |
| Complete VS Code API | `references/vscode-api.md` |
| When clauses | `references/when-clause-contexts.md` |
| Document selectors | `references/document-selector.md` |
| Theme colors list | `references/theme-color.md` |
| Icons in labels | `references/icons-in-labels.md` |
| Remote extensions | `advanced/remote-extensions.md` |
| Extension host internals | `advanced/extension-host.md` |
| Proposed (experimental) API | `advanced/using-proposed-api.md` |

---

## Phase 1: Scaffold

Use `yo code` to scaffold a new extension:

```bash
npx yo code
```

**Template selection:** TypeScript (recommended), JavaScript (prototypes), Color
Theme, Language Support (grammar + snippets), Code Snippets, Keymap, Extension
Pack, or GitHub Action (publishing).

The generator will also ask about init git, webpack (yes for production), and
package manager.

After scaffolding, read `docs/getting-started/extension-anatomy.md` to
understand each generated file's role.

---

## Phase 2: Develop

### Core pattern

Every extension exports `activate(context)` and optionally `deactivate()`.

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    // Register disposable resources here
    // context.subscriptions.push(...)
}
```

### Activation events

Control **when** the extension loads via `activationEvents` in `package.json`.
Common patterns: `onCommand:xxx`, `onView:xxx`, `onLanguage:xxx`,
`onStartupFinished`, `*` (use sparingly).

→ Full list: `docs/references/activation-events.md`

### Contribution points

The `contributes` field in `package.json` declares your extension's UI surface.
Key entries: `commands`, `menus`, `keybindings`, `viewsContainers`/`views`,
`configuration`, `languages`, `grammars`, `snippets`, `themes`, `customEditors`,
`notebooks`, `taskDefinitions`, `debuggers`, `authentication`, `walkthroughs`.

→ Complete schema: `docs/references/contribution-points.md`

### Common UI patterns

| Pattern | Minimal snippet | Doc |
|---|---|---|
| Command | `vscode.commands.registerCommand('id', fn)` | `guides/command.md` |
| Tree view | `vscode.window.registerTreeDataProvider('id', provider)` | `guides/tree-view.md` |
| WebView | `vscode.window.createWebviewPanel('type', 'title', col, opts)` | `guides/webview.md` |
| Status bar | `vscode.window.createStatusBarItem(align, priority)` | `ux-guidelines/status-bar.md` |
| Settings | `vscode.workspace.getConfiguration('ext').get('key')` | `capabilities/common-capabilities.md` |

When building a WebView:
- Use `acquireVsCodeApi()` in the frontend to send/receive messages
- Use `var(--vscode-*)` CSS variables for native theming
- Set `localResourceRoots` for loading bundled assets
- Add a CSP `<meta>` tag to prevent XSS

### Settings example (minimal)

In `package.json`:
```json
{"contributes":{"configuration":{"title":"My Ext","properties":{"myExt.timeout":{"type":"number","default":5000}}}}}
```

In code: `vscode.workspace.getConfiguration('myExt').get('timeout')`

### Language features

→ `docs/language/` covers syntax highlighting (TextMate grammars), semantic
highlighting, snippets, language config (brackets, comments, auto-closing), LSP
integration, and embedded languages.

### AI extensibility

VS Code 1.94+ supports AI-powered extensions. Key capabilities:
- **Chat Participant** (`@foo`) — `docs/ai/chat.md`
- **LM tools** — `docs/ai/tools.md`
- **Language model API** — `docs/ai/language-model.md`
- **MCP support** — `docs/ai/mcp.md`
- **Prompt TSX** — `docs/ai/prompt-tsx.md`
- **Custom LM chat provider** — `docs/ai/language-model-chat-provider.md`

---

## Phase 3: Build

```bash
npm run compile       # TypeScript → JS
npm run watch         # Watch mode (for development)
npm run build         # Webpack bundle (if configured)
```

Use webpack for production extensions — it reduces size, enables tree-shaking,
and is required for web extensions (`docs/guides/web-extensions.md`).

→ Full bundling guide: `docs/publishing/bundling-extension.md`

---

## Phase 4: Test

```bash
npx @vscode/test-cli run
```

Tests use `suite`/`test` (mocha-style). The scaffolded project includes a basic
test setup. For integration testing (commands, providers, WebViews):

→ `docs/publishing/testing-extension.md` and `docs/guides/testing.md`

---

## Phase 5: Package

```bash
npm version patch              # bump version
npm install -g @vscode/vsce    # install packager
vsce package                   # → .vsix file
code --install-extension *.vsix # local install
```

Ensure `README.md`, `CHANGELOG.md`, and `LICENSE` exist before packaging.

---

## Phase 6: Publish

### Prerequisites
1. Microsoft account
2. Publisher name (create once)
3. Personal Access Token (Azure DevOps → Marketplace scope)

```bash
vsce create-publisher <name>   # one-time
vsce publish                   # publish to marketplace
vsce publish patch             # bump + publish
vsce publish --dry-run         # validate only
vsce unpublish <pub>.ext       # remove
```

→ Full guide: `docs/publishing/publishing-extension.md`
→ CI/CD setup: `docs/publishing/continuous-integration.md`

---

## Debugging

Press `F5` in the extension project to launch an Extension Host window (the
scaffolded `.vscode/launch.json` handles this).

| Symptom | Likely cause |
|---|---|
| "Command not found" | Not registered in `activate()` OR missing from `contributes.commands` |
| Extension won't activate | Wrong `activationEvents` declaration |
| WebView blank | CSP blocking scripts — add `<meta http-equiv="Content-Security-Policy">` |
| vsce publish 401 | PAT expired or wrong scope |
| Extension not found | Publisher name mismatch |
