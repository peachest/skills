# Publishing

## Checklist

- [ ] `keywords` includes `pi-package`
- [ ] `package.json` has `pi` declaration
- [ ] `peerDependencies` references `@earendil-works/pi-coding-agent`
- [ ] `files` limits publish to necessary files only
- [ ] Tests pass: `npm test`
- [ ] Type check passes: `npx tsc --noEmit`
- [ ] After `pi install` from tarball, `/list-commands` shows registered extensions
- [ ] `.gitignore` and `.npmignore` have no conflicting rules (e.g. `dist/` excluded in one but not the other)

## .npmignore

```
.*
src/
tsconfig.json
test/
```

> Note: for noEmit projects, `files` in package.json must include `.ts` sources, and `.npmignore` should NOT exclude `src/`.

## Full flow

```bash
npm pack                                    # create tarball
pi install /path/to/pkg-0.1.0.tgz           # test install from tarball
# Verify: start Pi, check /list-commands
npm publish                                 # publish to npm registry
```

# CI

Minimal CI pipeline (GitHub Actions):

```yaml
# .github/workflows/ci.yml
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22 }
      - run: npm ci
      - run: npx tsc --noEmit           # type check
      - run: npm test                     # tests
      - run: npm run build                # build (skip for noEmit projects)
```

If using esbuild, `build` needs `esbuild` installed:

```yaml
      - run: npm run build
```

Optional publish pipeline:

```yaml
# .github/workflows/publish.yml
on:
  release:
    types: [published]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, registry-url: https://registry.npmjs.org }
      - run: npm ci
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

# Monorepo

```
packages/
├── pkg-a/     (package.json → pi: { extensions: [...] })
├── pkg-b/     (package.json → pi: { skills: [...] })

package.json (root)
{
  "private": true,
  "workspaces": ["packages/*"]
}
```

## Shared internal libraries

- Shared config library: `@scope/pi-config`
- Shared i18n library: soft-optional peer dep + dynamic import
- `bundledDependencies`: pack internal core library

# Build pattern reference

| Pattern | Notes |
|---------|-------|
| noEmit + jiti | Simplest, publish `.ts` directly |
| esbuild bundle | Bundle + `--external` for pi deps |
| tsc build | Needed for `.d.ts` |
| directory extensions | `./extensions` as entry |
| CLI + extension in one | Detect via `process.argv[1]` |
| re-export bridge | `index.ts` → `src/` modular |
| exports map | Expose sub-paths |
| bundledDependencies | Pack internal lib |
| i18n architecture | Dynamic import, soft peer dep |