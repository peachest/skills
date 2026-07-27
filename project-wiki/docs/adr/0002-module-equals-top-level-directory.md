# Module = top-level directory, not language-native module system

A "module" in this skill is defined as the first directory component of a
file's relative path (e.g. `src/auth/login.go` → module `src`). We
deliberately do not use language-native module systems (Go packages, Python
packages, Java packages, TS `package.json` workspaces). The trade-off:
language-native modules are semantically accurate but require a different
parser per language, break for polyglot repos, and often don't match how
teams actually organize code. Top-level directory is universal, needs zero
language-specific knowledge, and matches how most repos are physically
laid out. The cost is that some repos with non-standard layouts (e.g.
monorepos where meaningful modules live two levels deep) will get
coarse-grained modules. Users can work around this by running `init` with
`--extensions` to scope the scan, or by manually editing module wiki
metadata headers to adjust `root_dirs`.
