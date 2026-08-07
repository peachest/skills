# package.json

```json
{
  "name": "my-package",
  "version": "0.1.0",
  "keywords": ["pi-package"],
  "type": "module",
  "pi": { "extensions": ["./index.ts"] },
  "peerDependencies": { "@earendil-works/pi-coding-agent": "*" },
  "peerDependenciesMeta": { "@earendil-works/pi-coding-agent": { "optional": true } },
  "devDependencies": {
    "@earendil-works/pi-coding-agent": "^0.78.0",
    "@types/node": "^25.9.1",
    "typescript": "^5.5.0"
  }
}
```

Key points:
- `peerDependencies: "*"` — Pi bundles this package, don't install a second copy
- `peerDependenciesMeta.optional: true` — user has Pi, dependency is satisfied
- `keywords: ["pi-package"]` — discoverable on pi.dev/gallery
- `files` — noEmit needs `.ts` sources; esbuild/tsc only need `dist/`

### Registering multiple resource types

```json
{
  "pi": {
    "extensions": ["./index.ts"],
    "skills": ["./skills"],
    "prompts": ["./prompts"],
    "themes": ["./themes"]
  }
}
```

### Extension path patterns

- Single file: `"./index.ts"`
- Directory: `"./extensions"` (sub-dirs need `index.ts` or `*.ts` files)
- Glob: `"./extensions/*.ts"`

### Pinning to a local Pi install

```json
{
  "devDependencies": {
    "@earendil-works/pi-coding-agent": "file:../../../.nvm/versions/node/v24.15.0/lib/node_modules/@earendil-works/pi-coding-agent"
  }
}
```

# Entry point patterns

## Re-export bridge (recommended)

```typescript
// index.ts
export { default } from "./src/main.ts";
```

Pi loads `index.ts` via jiti; internal imports are also resolved through jiti. Core logic stays modular in `src/`.

## Single-file all-in-one (CLI + extension + barrel)

```typescript
#!/usr/bin/env node

export { parseDiff } from "./src/diff-parser.ts";

const isCLI = process.argv[1]?.endsWith("index.ts");
if (isCLI) { /* parse argv, run */ }

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
export default function (pi: ExtensionAPI) { /* ... */ }
```

```json
{
  "bin": { "my-cli": "index.ts" },
  "pi": { "extensions": ["./index.ts"] }
}
```

## Directory entry

```json
{ "pi": { "extensions": ["./extensions"] } }
```

```
extensions/
├── index.ts          # main extension
└── helpers/
    └── utils.ts
```

## exports map

```json
{
  "exports": {
    ".": "./index.ts",
    "./events": "./src/events.ts"
  }
}
```