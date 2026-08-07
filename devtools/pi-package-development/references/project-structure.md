# Project structure

Pi 的约定：
- `extensions/` 约定目录 → 加载 `.ts` / `.js` 文件
- `skills/` 约定目录 → 递归查找 `SKILL.md`
- `prompts/` 约定目录 → 加载 `.md` 文件
- `themes/` 约定目录 → 加载 `.json` 文件

以上是 pi auto-discovery 的约定路径。**除此之外的文件/目录位置都不是强制的**——只要 `package.json` 的 `pi` 字段指向正确，任意路径都可以。

以下目录树中的 `${ENTRY_PATH}` 表示开发者可自定义的路径，非 pi 强制。

## noEmit + jiti (recommended)

No build step. Pi loads `.ts` / `.js` via jiti.

### Extension only

```
my-package/
├── ${ENTRY_PATH}.{ts,js}     # default export factory function
├── src/                      # core logic
├── test/
├── package.json              # pi: { "extensions": ["./${ENTRY_PATH}.{ts,js}"] }
├── README.md
└── .gitignore
```

TypeScript 项目额外加 `tsconfig.json`（noEmit: true），纯 JS 项目不需要。

### Extension + Skill

```
my-package/
├── ${ENTRY_PATH}.{ts,js}     # default export, pi.registerTool()
├── skills/                   # pi 约定目录或 pi.skills 声明
│   └── my-skill/
│       └── SKILL.md
├── prompts/                  # optional
│   └── *.md
├── package.json              # pi: { "extensions": ["./${ENTRY_PATH}.{ts,js}"], "skills": ["./skills"] }
├── README.md
└── .gitignore
```

`${ENTRY_PATH}` 可以是 `index`、`src/index`、`src/extension/index` 等。参见下方本地 package 参考区的实际例子。

> Real-world examples: `pi-subagents`, `pi-intercom`, `pi-session-search` all use this layout.

## esbuild bundle

Only needed for TypeScript projects or when bundling multiple files into one.

### Extension only

```
my-package/
├── src/index.{ts,js}         # entry point
├── dist/                     # esbuild output
├── test/
├── package.json              # files: ["dist", "README.md"], pi: { "extensions": ["./dist/index.js"] }
└── tsconfig.json             # optional, only for TS projects
```

### Extension + Skill

```
my-package/
├── src/
│   └── ${ENTRY_PATH}.{ts,js} # entry point
├── dist/                     # esbuild output → dist/${OUT}.js
├── skills/
│   └── my-skill/
│       └── SKILL.md
├── prompts/                  # optional
│   └── *.md
├── package.json
│   # files: ["dist", "README.md"]
│   # pi: { "extensions": ["./dist/${OUT}.js"], "skills": ["./skills"] }
└── tsconfig.json             # optional, only for TS projects
```

```json
{
  "scripts": {
    "build": "esbuild src/index.ts --bundle --platform=node --format=esm --outfile=dist/index.js --sourcemap --packages=external --external:@earendil-works/pi-coding-agent",
    "dev": "esbuild src/index.ts --bundle --platform=node --format=esm --outfile=dist/index.js --sourcemap --watch --packages=external --external:@earendil-works/pi-coding-agent"
  }
}
```

`${ENTRY_PATH}` 和 `${OUT}` 由开发者自定。常见为 `src/index.ts` → `dist/index.js`，也可以 `src/extension/index.ts` → `dist/extension/index.js`。

> When your extension imports `@sinclair/typebox`, append `--external:@sinclair/typebox` to both commands. (It's a pi peer dep, not a user dependency.)

## tsc build

Needed when `.d.ts` is required.

### Extension only

```
my-package/
├── src/
│   └── index.ts              # entry point
├── dist/                     # tsc output
├── test/
├── package.json              # main: "dist/index.js", pi: { "extensions": ["./dist/index.js"] }
└── tsconfig.json             # outDir: "dist", declaration: true
```

### Extension + Skill

```
my-package/
├── src/
│   └── ${ENTRY_PATH}.ts      # entry point
├── dist/                     # tsc output: src/${ENTRY_PATH}.ts → dist/${OUT}.js
├── skills/
│   └── my-skill/
│       └── SKILL.md
├── prompts/                  # optional
│   └── *.md
├── package.json              # main: "dist/${OUT}.js", pi: { "extensions": ["./dist/${OUT}.js"], "skills": ["./skills"] }
└── tsconfig.json             # outDir: "dist", declaration: true
```

# tsconfig.json (TypeScript only)

以下两个模板只适用于 TypeScript 项目。纯 JS 项目无需 tsconfig.json，也无需安装 `typescript` 或 `@types/node`。

## noEmit

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "types": ["node"]
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules", "dist", ".scratch"]
}
```

## build

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

# Pi package 完整目录参考

pi package 可以同时包含四种资源类型。`package.json` 的 `pi` 字段显式声明路径（不加 `pi` 字段时，pi 也会自动发现约定目录，但显式声明更可靠）。

| 组件 | `pi` 字段值示例 | 约定目录 | 说明 |
|------|----------------|----------|------|
| **Extension** | `"./${ENTRY_PATH}.{ts,js}"` | `extensions/` | `.ts` / `.js` 文件，`pi.registerTool()` 注册 tool |
| **Skill** | `"./skills"` | `skills/` | 目录树，每层一个 `SKILL.md` 即一个 skill |
| **Prompt** | `"./prompts"` | `prompts/` | `.md` 文件，通过 `/name` 展开 |
| **Theme** | `"./themes"` | `themes/` | `.json` 文件 |

`${ENTRY_PATH}` 由开发者自定（如 `index`、`src/index`、`src/extension/index`）。pi 只要求指向一个 `.ts` 或 `.js` 文件，不限制路径。

## 完整示例

以下是一个同时包含 extension、skill 和 prompt 的 pi package 目录结构（路径仅为示例）：

```
my-package/
├── src/
│   └── extension/
│       └── index.ts          # default export, pi.registerTool()
├── skills/
│   └── my-skill/
│       └── SKILL.md          # skill 描述，引用 extension 注册的 tool
├── prompts/                  # 可选：prompt templates
│   └── quick-review.md
├── themes/                   # 可选：主题
│   └── my-theme.json
├── package.json              # pi 字段声明所有组件
├── tsconfig.json             # 纯 JS 项目不需要
├── README.md
└── .gitignore
```

**package.json：**

```json
{
  "name": "my-package",
  "keywords": ["pi-package"],
  "pi": {
    "extensions": ["./src/extension/index.ts"],
    "skills": ["./skills"],
    "prompts": ["./prompts"],
    "themes": ["./themes"]
  }
}
```

路径可自由调整。等价地也可以写为 `"./index.{ts,js}"`（顶层）、`"./extensions/my-tool.js"`（extensions/ 目录）等。

如不引用 pi 的类型（纯 JS、无 `import type { ExtensionAPI }`），则无需安装 `@earendil-works/pi-coding-agent` 等类型包，也无需 tsconfig.json。

**技能和扩展的配合方式：**

- Extension 通过 `pi.registerTool()` 向 LLM 注册可调用的 tool
- SKILL.md 指导 agent 在什么场景下使用这些 tool 以及用什么样的工作流
- 两者分开，skill 不包含 executable code，extension 不包含 agent 指令

## 只含某一类的 package 参考

本地已安装 package 的实际目录布局：

### Extension only

```
pi-mcp-adapter/        pi-simplify/           pi-markdown-preview/
├── index.ts           ├── src/               ├── index.ts
├── cli.js             ├── dist/              ├── client/
├── ...                ├── package.json       ├── package.json
├── package.json       └── README.md          └── README.md
```

### Extension + Skill

```
pi-subagents/                pi-session-search/          pi-intercom/
├── src/                     ├── src/                    ├── index.ts
│   └── extension/           │   └── index.ts            ├── skills/
│       └── index.ts         ├── dist/                   │   └── pi-intercom/
├── skills/                  │   └── index.js            │       └── SKILL.md
│   └── pi-subagents/        ├── skills/                 └── package.json
│       └── SKILL.md         │   └── session-history/
├── prompts/                 │       └── SKILL.md
│   └── *.md                 └── package.json
├── package.json
└── README.md
```