# Testing

## vitest (recommended)

```bash
npm install -D vitest
```

`vitest.config.ts`:
```typescript
import { defineConfig } from "vitest/config";
export default defineConfig({
  test: { include: ["src/**/*.test.ts"] },
});
```

`package.json`:
```json
{ "scripts": { "test": "vitest run", "test:watch": "vitest" } }
```

## node:test (zero deps)

```json
{ "scripts": { "test": "node --experimental-strip-types --test index.test.ts" } }
```

## Pi type resolution in tests

`@earendil-works/pi-coding-agent` is a `peerDependency`. Test runners may not find it.

Fix:
1. `npm install -D @earendil-works/pi-coding-agent`
2. Or use `file:` protocol to link local Pi install

# Local install

Choose the method based on your phase:

| # | Method | Command | Best for | Debug loop |
|---|--------|---------|----------|------------|
| 1 | `pi install ./path` | `pi install ./my-package` | **Active development (default)** — dir referenced as-is from settings.json | Edit source → `/reload` → test, no rebuild |
| 2 | `pi -e ./index.ts` | `pi -e ./index.ts` | Quick one-shot test, no permanent install | Session-only, restart to reload |
| 3 | Tarball install | `pi install /path/to/pkg-0.1.0.tgz` | Verify published tarball before `npm publish` | Must re-pack on every change |
| 4 | Symlink | `ln -s /abs/path ~/.pi/agent/extensions/my-package` | Auto-discovers `*/index.ts` | Same as #1 but manual symlink |
| 5 | Project-local config | `.pi/settings.json` → `{ "packages": [".."] }` | Work on multiple pi packages in one workspace | Same as #1 but per-project ⚠️ `".."` 从 `.pi/` 目录向上到项目根，而非 `"."` |

**推荐调试流程：** `pi install ./path` → 修改源码 → `/reload` → 测试。jiti 热加载实时生效。

Verify: Start Pi, check `/list-commands` and `/list-tools`.

# Debug

## Common errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| Extension not loading | Wrong `pi.extensions` path in package.json | Correct the path |
| Type import error | Missing `@earendil-works/pi-coding-agent` | `npm install -D` it |
| `export default` error | No default export | Export `function(pi: ExtensionAPI)` |
| Code changes not reflected | jiti cache | Run `/reload` (no restart needed) |
| Tool not appearing | Package filter in settings | Check settings.json for `"extensions": []` |
| `Cannot find module` | Missing `allowImportingTsExtensions` | Add to tsconfig |
| `pi install` succeeds but package not found | Deps not installed / `.npmignore` excluded sources | `npm install`; check `.npmignore` |

## Logs

```bash
/debug  # Writes to ~/.pi/agent/pi-debug.log
```

# Events

| Event | When | Use |
|-------|------|-----|
| `session_start` | Session start / resume | Init state, notify |
| `turn_start` / `turn_end` | Before / after each LLM turn | Metering, timing |
| `message_update` | Token streaming | Real-time counters |
| `tool_call` | Before tool execution | Intercept / modify params |
| `tool_result` | After tool execution | Modify results |
| `before_agent_start` | After user input | Inject system prompt |
| `context` | Before each LLM call | Filter / modify messages |
| `agent_end` | Prompt complete | Post-processing |
| `session_shutdown` | Session end / reload | Cleanup, persist |

## ctx.ui

| Method | Purpose | Available in |
|--------|---------|-------------|
| `notify(msg, level)` | Toast notification | TUI + RPC |
| `confirm(title, msg)` | Confirmation dialog | TUI + RPC |
| `setStatus(id, text)` | Bottom status bar | TUI |
| `setWidget(id, lines)` | Editor widget | TUI |