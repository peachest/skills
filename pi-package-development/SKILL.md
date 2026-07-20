---
name: pi-package-development
description: "Full workflow for developing pi packages — extensions, skills, themes, prompts. Covers scaffold, config, entry points, test, install, debug, publish. Use when user says \"create a pi package\" / \"make an extension\" / \"write a skill\" / \"build a theme\" / \"pi install\" / \"pi -e\" / \"why doesn't my extension load\" / \"publish my package\" / \"monorepo\" / \"settings.json\" / \"packages 配置\" / \"project-local\" / \"failed to load\" / \"extension not loading\" / \"package not found\" / \"package doesn't show up\" / \"pi list\" / \"/reload\" / \"jiti cache\" / \"update my package\" / \"uninstall\" / \"remove package\" / \"register a command\" / \"registerCommand\" / \"bump version\" / \"npm pack\" / \"npm publish\", or wants to fix a package's dev workflow, add tests to a pi package, or debug why an extension won't load."
---

# Pi Package Development

## Quick start (noEmit + jiti — simplest path)

```bash
mkdir my-package && cd my-package
npm init -y
npm install -D typescript @types/node @earendil-works/pi-coding-agent
```

```typescript
// index.ts
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
export default function (pi: ExtensionAPI) {
  pi.on("session_start", (_event, ctx) => ctx.ui.notify("Loaded!", "info"));
  pi.registerCommand("hello", {
    description: "Say hello",
    handler: async (_args, ctx) => ctx.ui.notify("Hello!", "info"),
  });
}
```

```json
// package.json — add:
{ "keywords": ["pi-package"], "pi": { "extensions": ["./index.ts"] } }
```

```bash
pi -e ./index.ts   # test
pi install "$(pwd)"  # permanent
```

## Workflow

For each step, ask the user a question to present options and let them choose. Ask one question at a time. Wait for the answer before proceeding. If the user doesn't answer, infer from the conversation context and propose a default.

### 1. Scaffold

The project structure determines how code gets loaded. **noEmit** publishes `.ts` directly (no build step), **esbuild** bundles to `dist/` (clean publish), **tsc** produces `.d.ts` (library consumers).

Ask the user which structure fits.

- **noEmit + jiti** — pi loads `.ts` via jiti. Best for pure extensions with no build toolchain.
- **esbuild bundle** — bundle to `dist/`, `--external` flags exclude pi deps. Best for single output file.
- **tsc build** — TypeScript compiler with `declaration: true`. Best when consumers need `.d.ts`.

When user chooses: read [references/project-structure.md](references/project-structure.md) for the matching directory layout and tsconfig template.

Do not proceed until the user has chosen a scaffold.

### 2. Entry point

The entry point controls how pi finds your extension. A **re-export bridge** keeps `index.ts` clean; **single-file** bundles CLI + extension in one; **directory entry** splits into multiple independent extensions.

Ask the user which entry style.

- **re-export bridge** — `index.ts` only does `export { default } from "./src/main.ts"`. Clean separation.
- **single-file all-in-one** — same file handles CLI (`#!/usr/bin/env node` + `process.argv[1]`) and pi extension.
- **directory entry** — `"pi": { "extensions": ["./extensions"] }`. Each `.ts` file registers independently.

When user chooses: read [references/config.md](references/config.md#入口点模式) for the matching code pattern.

### 3. Dependencies

Ask: "Any runtime dependencies beyond `@earendil-works/pi-coding-agent`?" If yes, they go in `dependencies`.

Read [references/config.md](references/config.md) to scaffold `package.json` and `tsconfig`.

### 4. Testing

Tests verify behavior. **vitest** is batteries-included (recommended), **node:test** needs zero deps.

Ask the user which one.

Read [references/testing-install.md](references/testing-install.md#测试) for the config template.

### 5. Linting

Ask: "eslint, biome, or none?" If chosen, install and add scripts.

### 6. Write extension

Write the extension file after the user has chosen scaffold, entry point, and deps.

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "@sinclair/typebox";

export default function (pi: ExtensionAPI) {
  pi.on("session_start", async (_event, ctx) => { /* init */ });
  pi.registerTool({
    name: "my_tool",
    description: "...",
    parameters: Type.Object({ action: Type.String() }),
    async execute(toolCallId, params, signal, onUpdate, ctx) { /* ... */ },
  });
  pi.registerCommand("mycommand", {
    description: "...",
    handler: async (_args, ctx) => { /* ... */ },
  });
}
```

For entry point variants, read [references/config.md](references/config.md#入口点模式). For event reference, read [references/testing-install.md](references/testing-install.md#常用事件).

### 7. Install locally

Ask the user which install method:

- `pi install ./my-package` — saves to settings (most common)
- `pi -e ./index.ts` — one-shot quick test
- Symlink into `~/.pi/agent/extensions/` — auto-discovery
- `.pi/settings.json` → `{ "packages": [".."] }` — project-local. ⚠️ `".."` 从 `.pi/` 目录向上到项目根，而非 `"."`

After install, run verification:

1. **Agent 自动检查** — 依次执行:
   - `pi list` — 确认 package 出现在列表中
   - 检查 settings.json 中 packages 数组包含本 package 路径
   - 确认目标目录存在（npm/git install 时）
2. **告知用户重新加载** — `Run /reload in pi to pick up the new package (jiti cache).`
3. **手动确认** — 进入 pi 后:
   - `/list-commands` — 确认注册的命令出现
   - `/list-tools` — 确认注册的工具出现
   - 如需更精确的检查，可以临时注册一个 `pi.registerCommand("hello", ...)` 后运行 `/hello`

If any item fails, fix before proceeding.

### 8. Debug

Read [references/testing-install.md](references/testing-install.md#调试) for the error table.

Common causes:
- Changes not reflected → run `/reload` in pi (jiti cache)
- Tool not appearing → check settings.json for `"extensions": []`
- `Cannot find module` → add `allowImportingTsExtensions` to tsconfig

Refer to the error table in the reference file if the symptom isn't listed above.

### 9. Publish

Do not proceed until Steps 1-8 are complete and verified.

Read [references/publishing.md](references/publishing.md). Run through the full checklist. Then:

```bash
npm pack
pi install /path/to/pkg-0.1.0.tgz   # test from tarball
npm publish
```

Checklist:
- [ ] All publishing checklist items pass
- [ ] `pi install` from tarball succeeds
- [ ] `/list-commands` inside pi finds the extension
- [ ] `npm publish` succeeds

## Reference structure

```
pi-package-development/
├── SKILL.md                          ← this file
└── references/
    ├── project-structure.md          ← scaffold types + tsconfig
    ├── config.md                     ← package.json + entry points
    ├── testing-install.md            ← test, install, debug, events
    └── publishing.md                 ← publish, monorepo, pattern ref, CI
```