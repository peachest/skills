#!/usr/bin/env node
/*
 * project-wiki CLI — maintain a three-level project knowledge base.
 *
 * Node.js runtime (zero external dependencies). Behaviorally equivalent to
 * the canonical Python implementation (wiki.py): identical SHA1 drift logic,
 * skip rules, module detection, markdown parsing, cache format, and CLI
 * surface so the two runtimes are interchangeable on the same project.
 *
 * Commands:
 *     init    Scan the project, detect modules, generate wiki skeleton.
 *     check   Compare current code state with wiki; report drift (triage).
 *     update  Refresh SHA baseline cache after wiki has been reviewed.
 *     status  Show wiki coverage summary.
 *
 * Usage:
 *     node wiki.js init   [--root .] [--lang auto] [--extensions .go,.py,...] [--json]
 *     node wiki.js check  [--root .] [--fail-on-stale] [--json]
 *     node wiki.js update [--root .] [--json]
 *     node wiki.js status [--root .] [--json]
 */

"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const WIKI_DIR_NAME = "docs/project_wiki";
const CACHE_FILE_NAME = ".review_cache.json";

// Source file extensions by language. "auto" tries all of them.
// Order mirrors wiki.py so generated --lang help text is identical.
const LANG_EXTENSIONS = {
  go: [".go"],
  python: [".py"],
  javascript: [".js", ".jsx", ".mjs", ".cjs"],
  typescript: [".ts", ".tsx"],
  vue: [".vue"],
  rust: [".rs"],
  java: [".java"],
  kotlin: [".kt", ".kts"],
  swift: [".swift"],
  objc: [".h", ".m", ".mm"],
  c: [".c", ".h"],
  cpp: [".cpp", ".cc", ".cxx", ".hpp", ".h"],
  ruby: [".rb"],
  php: [".php"],
  csharp: [".cs"],
  scala: [".scala"],
  elixir: [".ex", ".exs"],
  lua: [".lua"],
  dart: [".dart"],
  generic: [
    ".go", ".py", ".js", ".jsx", ".mjs", ".ts", ".tsx", ".rs",
    ".java", ".kt", ".swift", ".c", ".h", ".cpp", ".cc", ".hpp",
    ".rb", ".php", ".cs", ".scala", ".ex", ".lua", ".dart",
    ".m", ".mm", ".vue", ".svelte",
  ],
};

// Directories to always skip during scanning.
const SKIP_DIRS = new Set([
  ".git", ".svn", ".hg", ".pi", ".agent", ".agents", ".claude",
  "node_modules", "vendor", "venv", ".venv", "env", ".env",
  "__pycache__", ".pytest_cache", ".mypy_cache", ".tox",
  "dist", "build", "target", "out", ".next", ".nuxt",
  ".idea", ".vscode", "coverage", ".coverage",
  "project_wiki", // don't scan the wiki itself (under docs/)
  ".cache", "tmp", "temp", ".tmp",
]);

// Files to always skip (anchored at start via re.match semantics; the leading
// ".*" makes each equivalent to a "ends-with" test, matching wiki.py).
const SKIP_FILE_PATTERNS = [
  /^.*_test\.go$/,
  /^.*_test\.py$/,
  /^.*\.test\.[jt]sx?$/,
  /^.*\.spec\.[jt]sx?$/,
  /^.*\.bench\.[jt]sx?$/,
  /^.*\.mock\.[jt]sx?$/,
  /^.*\.gen\.go$/,
  /^.*\.pb\.go$/,
  /^.*\.pb\.py$/,
  /^.*_pb2\.py$/,
  /^.*_string\.go$/,
  /^zz_generated_.*\.go$/,
  /^.*\.min\.js$/,
  /^.*\.min\.css$/,
];

// ---------------------------------------------------------------------------
// Output helpers (mimic Python print / print(file=sys.stderr))
// ---------------------------------------------------------------------------

// Set to true by main() when --json is passed: human output is suppressed and
// each command emits one machine-readable JSON object on stdout instead.
let JSON_MODE = false;

function stdoutPrint(...args) {
  if (JSON_MODE) return;
  process.stdout.write(args.map((a) => (typeof a === "string" ? a : String(a))).join(" ") + "\n");
}
function stderrPrint(...args) {
  process.stderr.write(args.map((a) => (typeof a === "string" ? a : String(a))).join(" ") + "\n");
}

// Emit the structured result object — the only stdout in --json mode.
function emitJson(result) {
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
}

// Build one stable finding entry (code + path + detail).
function makeSignal(code, filePath, detail) {
  return { code, path: filePath, detail };
}

// Deterministic signal ordering: by code, then path, then detail.
function sortSignals(signals) {
  return signals.slice().sort((a, b) => {
    if (a.code !== b.code) return a.code < b.code ? -1 : 1;
    if (a.path !== b.path) return a.path < b.path ? -1 : 1;
    return a.detail < b.detail ? -1 : a.detail > b.detail ? 1 : 0;
  });
}

// ---------------------------------------------------------------------------
// File scanning
// ---------------------------------------------------------------------------

function shouldSkipFile(filename) {
  for (const pat of SKIP_FILE_PATTERNS) {
    if (pat.test(filename)) return true;
  }
  return false;
}

function computeSha(buf) {
  return crypto.createHash("sha1").update(buf).digest("hex");
}

/**
 * Count lines in a buffer, matching Python's
 * `sum(1 for _ in open(f, errors="replace"))` semantics:
 *   - empty file          -> 0
 *   - ends with newline   -> number of newlines
 *   - does not end with \n-> number of newlines + 1
 * Counts 0x0A bytes, which correctly handles \n and \r\n.
 */
function countLines(buf) {
  if (buf.length === 0) return 0;
  let nl = 0;
  for (let i = 0; i < buf.length; i++) {
    if (buf[i] === 0x0a) nl++;
  }
  if (buf[buf.length - 1] === 0x0a) return nl;
  return nl + 1;
}

/**
 * Walk the project tree and collect all source files.
 * Returns a list of SourceFile objects sorted by path.
 * Mirrors os.walk(top, followlinks=False): real directories only.
 */
function scanProject(root, extensions) {
  const files = [];
  const extSet = new Set(extensions.map((e) => e.toLowerCase()));

  function walk(absDir) {
    let entries;
    try {
      entries = fs.readdirSync(absDir, { withFileTypes: true });
    } catch (e) {
      return; // permission error, etc. — skip
    }
    for (const ent of entries) {
      // Skip symlinked directories and files (followlinks=False behavior).
      if (ent.isSymbolicLink()) continue;
      const full = path.join(absDir, ent.name);
      if (ent.isDirectory()) {
        if (SKIP_DIRS.has(ent.name)) continue;
        walk(full);
      } else if (ent.isFile()) {
        const ext = path.extname(ent.name).toLowerCase();
        if (!extSet.has(ext)) continue;
        if (shouldSkipFile(ent.name)) continue;

        let rel = path.relative(root, full);
        // Normalize to forward slashes for cross-platform consistency.
        rel = rel.split(path.sep).join("/");
        if (rel === "") continue;

        const parts = rel.split("/");
        const module = parts.length <= 1 ? "root" : parts[0];

        let buf;
        try {
          buf = fs.readFileSync(full);
        } catch (e) {
          buf = Buffer.alloc(0);
        }
        const sha = buf.length ? computeSha(buf) : "";
        let size = 0;
        try {
          size = fs.statSync(full).size;
        } catch (e) {
          /* leave 0 */
        }
        const lines = countLines(buf);

        files.push({ path: rel, module, sha, size, lines });
      }
    }
  }

  walk(root);
  files.sort((a, b) => (a.path < b.path ? -1 : a.path > b.path ? 1 : 0));
  return files;
}

// ---------------------------------------------------------------------------
// Module / language detection
// ---------------------------------------------------------------------------

/**
 * Auto-detect the primary language of the project.
 * Counts files per language (a file may count toward multiple languages when
 * extensions overlap, e.g. ".h" — matching wiki.py's per-language os.walk).
 */
function detectLanguage(root) {
  // Map each extension to the languages that claim it.
  const extToLangs = {};
  for (const [lang, exts] of Object.entries(LANG_EXTENSIONS)) {
    if (lang === "generic") continue;
    for (const ext of exts) {
      const e = ext.toLowerCase();
      (extToLangs[e] = extToLangs[e] || []).push(lang);
    }
  }

  const langCounts = {};
  function walk(absDir) {
    let entries;
    try {
      entries = fs.readdirSync(absDir, { withFileTypes: true });
    } catch (e) {
      return;
    }
    for (const ent of entries) {
      if (ent.isSymbolicLink()) continue;
      const full = path.join(absDir, ent.name);
      if (ent.isDirectory()) {
        if (SKIP_DIRS.has(ent.name)) continue;
        walk(full);
      } else if (ent.isFile()) {
        const ext = path.extname(ent.name).toLowerCase();
        const langs = extToLangs[ext];
        if (!langs) continue;
        for (const lang of langs) {
          langCounts[lang] = (langCounts[lang] || 0) + 1;
        }
      }
    }
  }
  walk(root);

  const keys = Object.keys(langCounts);
  if (keys.length === 0) return "generic";

  let primary = keys[0];
  for (const k of keys) {
    if (langCounts[k] > langCounts[primary]) primary = k;
  }

  // JS/TS/Vue coexist — if any of them is primary, collapse to "web".
  const webLangs = new Set(["javascript", "typescript", "vue"]);
  if (webLangs.has(primary) && keys.some((k) => webLangs.has(k))) {
    return "web";
  }
  return primary;
}

function getExtensionsForLang(lang) {
  if (lang === "web") {
    return [".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".vue", ".svelte"];
  }
  if (lang === "auto") {
    return LANG_EXTENSIONS.generic.slice();
  }
  return (LANG_EXTENSIONS[lang] || LANG_EXTENSIONS.generic).slice();
}

/**
 * Group files into modules based on top-level directory.
 * Returns a Map: module_name -> SourceFile[] (preserving global path order).
 */
function detectModules(files) {
  const modules = new Map();
  for (const f of files) {
    if (!modules.has(f.module)) modules.set(f.module, []);
    modules.get(f.module).push(f);
  }
  return modules;
}

// ---------------------------------------------------------------------------
// Wiki file parsing
// ---------------------------------------------------------------------------

function readFileText(filePath) {
  try {
    return fs.readFileSync(filePath, "utf8");
  } catch (e) {
    return "";
  }
}

/**
 * Parse a module wiki markdown file.
 * Extracts module_id / root_dirs / desc from HTML comments and the file
 * registration table rows.
 */
function parseModuleWiki(wikiPath) {
  if (!fs.existsSync(wikiPath)) return null;
  const content = readFileText(wikiPath);
  const mw = {
    module_id: path.basename(wikiPath, ".md"),
    root_dirs: [],
    desc: "",
    entries: {}, // path -> { path, description }
  };

  const idMatch = content.match(/<!--\s*module_id:\s*(.+?)\s*-->/);
  if (idMatch) mw.module_id = idMatch[1].trim();

  const dirsMatch = content.match(/<!--\s*root_dirs:\s*([\s\S]+?)\s*-->/);
  if (dirsMatch) {
    const raw = dirsMatch[1];
    const dirs = raw.replace(/\n/g, ",").split(",").map((d) => {
      let s = d.trim();
      // lstrip("- ") — strip leading '-' and ' ' characters
      s = s.replace(/^[-\s]+/, "");
      return s.trim();
    }).filter((d) => d.length > 0);
    mw.root_dirs = dirs;
  }

  const descMatch = content.match(/<!--\s*desc:\s*([\s\S]+?)\s*-->/);
  if (descMatch) mw.desc = descMatch[1].trim().replace(/\n/g, " ");

  const tableRe = /^\|\s*`?([^`|]+?)`?\s*\|\s*([^|]*?)\s*\|/gm;
  let m;
  while ((m = tableRe.exec(content)) !== null) {
    const p = m[1].trim();
    const desc = m[2].trim();

    if (["文件", "File", "file", "Path", "path", "---", "—", ""].includes(p)) continue;
    if (p.startsWith("---") || p.startsWith(":--")) continue;
    if (p.startsWith("<!--")) continue;

    mw.entries[p] = { path: p, description: desc };
  }
  return mw;
}

/**
 * Parse overview.md module index table.
 * Returns: { module_name: { desc, link } }
 */
function parseOverview(wikiPath) {
  const modules = {};
  if (!fs.existsSync(wikiPath)) return modules;
  const content = readFileText(wikiPath);

  const tableRe = /^\|\s*`?([^`|]+?)`?\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|/gm;
  let m;
  while ((m = tableRe.exec(content)) !== null) {
    const name = m[1].trim();
    const desc = m[2].trim();
    const link = m[3].trim();

    if (["模块", "Module", "module", "---", "—", ""].includes(name)) continue;
    if (name.startsWith("---") || name.startsWith(":--")) continue;

    modules[name] = { desc, link };
  }
  return modules;
}

// ---------------------------------------------------------------------------
// Wiki generation
// ---------------------------------------------------------------------------

/**
 * Detect L3 domain-modeling artifacts at the project root.
 */
function detectL3Artifacts(root) {
  const result = { context_md: null, adrs: [], glossary: null };

  for (const candidate of [path.join(root, "CONTEXT.md"), path.join(root, "docs", "CONTEXT.md")]) {
    if (fs.existsSync(candidate)) {
      result.context_md = candidate;
      break;
    }
  }

  const adrDir = path.join(root, "docs", "adr");
  if (fs.existsSync(adrDir) && fs.statSync(adrDir).isDirectory()) {
    try {
      result.adrs = fs
        .readdirSync(adrDir)
        .filter((f) => f.endsWith(".md"))
        .sort()
        .map((f) => path.join(adrDir, f));
    } catch (e) {
      result.adrs = [];
    }
  }

  const wikiGlossary = path.join(root, WIKI_DIR_NAME, "glossary.md");
  if (fs.existsSync(wikiGlossary)) result.glossary = wikiGlossary;

  return result;
}

function nowTimestamp() {
  // "YYYY-MM-DD HH:MM UTC"
  const d = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return (
    `${d.getUTCFullYear()}-${pad(d.getUTCMonth() + 1)}-${pad(d.getUTCDate())} ` +
    `${pad(d.getUTCHours())}:${pad(d.getUTCMinutes())} UTC`
  );
}

/**
 * Generate overview.md content from detected modules.
 * If root is provided, detect L3 artifacts and add a Domain Language section.
 */
function generateOverviewContent(modules, root) {
  const lines = [
    "<!-- module_id: overview -->",
    "<!-- desc: Project overview — module index and responsibilities -->",
    "",
    "# Project Overview",
    "",
    "> L1 knowledge base entry point. Each module links to its L2 detail wiki.",
    "> Keep this file under 5KB — it's loaded into every AI context window.",
    "",
    "## Module Index",
    "",
    "| Module | Responsibility | Detail Wiki |",
    "| ------ | -------------- | ----------- |",
  ];

  const sortedNames = [...modules.keys()].sort();
  for (const moduleName of sortedNames) {
    const files = modules.get(moduleName);
    const fileCount = files.length;
    const wikiLink = `[${moduleName}.md](${moduleName}.md)`;
    const desc = `_${fileCount} source files_ — <one-line responsibility>`;
    lines.push(`| \`${moduleName}\` | ${desc} | ${wikiLink} |`);
  }

  if (root) {
    const l3 = detectL3Artifacts(root);
    const l3Lines = [];
    const wikiDir = path.join(root, WIKI_DIR_NAME);

    if (l3.context_md) {
      const rel = path.relative(wikiDir, l3.context_md).split(path.sep).join("/");
      l3Lines.push(`- Vocabulary: [CONTEXT.md](${rel})`);
    }
    if (l3.adrs.length) {
      const adrDir = path.dirname(l3.adrs[0]);
      const rel = path.relative(wikiDir, adrDir).split(path.sep).join("/");
      l3Lines.push(`- Decisions: [docs/adr/](${rel}) (${l3.adrs.length} ADRs)`);
    }
    if (l3.glossary) {
      l3Lines.push("- Hand-curated glossary: [glossary.md](glossary.md)");
    }

    if (l3Lines.length) {
      lines.push(
        "",
        "## Domain Language",
        "",
        "> L3: concept map — what terms mean and why decisions were made.",
        "> Read this before the module index if you're new to the domain.",
        ""
      );
      lines.push(...l3Lines);
    }
  }

  const totalFiles = [...modules.values()].reduce((s, fs_) => s + fs_.length, 0);
  lines.push(
    "",
    "## Statistics",
    "",
    `- Total modules: ${modules.size}`,
    `- Total source files: ${totalFiles}`,
    `- Last updated: ${nowTimestamp()}`,
    "",
    "---",
    "",
    "> **Maintenance**: Run `python3 scripts/wiki.py check` to detect drift.",
    "> Run `python3 scripts/wiki.py update` after reviewing and updating wiki entries.",
    ""
  );

  return lines.join("\n");
}

/**
 * Generate a module wiki file content.
 */
function generateModuleContent(moduleName, files) {
  const rootDirsSet = new Set();
  for (const f of files) {
    const parts = f.path.split("/");
    if (parts.length > 1) rootDirsSet.add(parts[0]);
  }
  const rootDirs = rootDirsSet.size ? [...rootDirsSet].sort() : [moduleName];

  const lines = [
    `<!-- module_id: ${moduleName} -->`,
    `<!-- root_dirs:`,
  ];
  for (const d of rootDirs) lines.push(`  - ${d}/`);
  lines.push(
    "-->",
    `<!-- desc: <one-line responsibility for ${moduleName}> -->`,
    "",
    `# Module: ${moduleName}`,
    "",
    `> L2 knowledge base — file-level registration for the \`${moduleName}\` module.`,
    "",
    "## File Registration",
    "",
    "| File | Description |",
    "| ---- | ----------- |"
  );

  for (const f of files) {
    const displayPath = `\`${f.path}\``;
    const base = f.path.split("/").pop();
    const desc = `<describe ${base}>`;
    lines.push(`| ${displayPath} | ${desc} |`);
  }

  const totalLines = files.reduce((s, f) => s + f.lines, 0);
  lines.push(
    "",
    "## Statistics",
    "",
    `- Source files: ${files.length}`,
    `- Total lines: ${totalLines}`,
    ""
  );

  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Cache (SHA baseline) management
// ---------------------------------------------------------------------------

function sortObject(o) {
  if (Array.isArray(o)) return o.map(sortObject);
  if (o && typeof o === "object") {
    const sorted = {};
    for (const k of Object.keys(o).sort()) sorted[k] = sortObject(o[k]);
    return sorted;
  }
  return o;
}

function loadCache(wikiDir) {
  const cachePath = path.join(wikiDir, CACHE_FILE_NAME);
  if (!fs.existsSync(cachePath)) return { files: {}, last_updated: null };
  try {
    const parsed = JSON.parse(fs.readFileSync(cachePath, "utf8"));
    if (!parsed || typeof parsed !== "object") return { files: {}, last_updated: null };
    if (!parsed.files) parsed.files = {};
    return parsed;
  } catch (e) {
    return { files: {}, last_updated: null };
  }
}

function saveCache(wikiDir, cache) {
  const cachePath = path.join(wikiDir, CACHE_FILE_NAME);
  cache.last_updated = new Date().toISOString();
  fs.writeFileSync(cachePath, JSON.stringify(sortObject(cache), null, 2) + "\n", "utf8");
}

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

function cmdInit(args) {
  const root = path.resolve(args.root);
  const wikiDir = path.join(root, WIKI_DIR_NAME);

  if (!fs.existsSync(root)) {
    stderrPrint(`Error: project root does not exist: ${root}`);
    return 1;
  }

  let lang = args.lang;
  if (lang === "auto") {
    lang = detectLanguage(root);
    stdoutPrint(`Detected language: ${lang}`);
  }

  let extensions = getExtensionsForLang(lang);
  if (args.extensions) {
    extensions = args.extensions.split(",").map((e) => e.trim());
  }

  stdoutPrint(`Scanning for extensions: ${extensions.join(", ")}`);

  const files = scanProject(root, extensions);
  if (files.length === 0) {
    stderrPrint("Error: no source files found. Check --lang or --extensions.");
    return 1;
  }

  const modules = detectModules(files);
  stdoutPrint(`Found ${files.length} source files in ${modules.size} module(s):`);
  for (const name of [...modules.keys()].sort()) {
    stdoutPrint(`  ${name}: ${modules.get(name).length} files`);
  }

  fs.mkdirSync(wikiDir, { recursive: true });

  const generated = [];
  const overviewPath = path.join(wikiDir, "overview.md");
  fs.writeFileSync(overviewPath, generateOverviewContent(modules, root), "utf8");
  generated.push(path.relative(root, overviewPath));
  stdoutPrint(`\nGenerated: ${path.relative(root, overviewPath)}`);

  for (const moduleName of [...modules.keys()].sort()) {
    const modulePath = path.join(wikiDir, `${moduleName}.md`);
    fs.writeFileSync(modulePath, generateModuleContent(moduleName, modules.get(moduleName)), "utf8");
    generated.push(path.relative(root, modulePath));
    stdoutPrint(`Generated: ${path.relative(root, modulePath)}`);
  }

  const cache = { files: {}, last_updated: null };
  for (const f of files) {
    cache.files[f.path] = { sha: f.sha, module: f.module, reviewed: false };
  }
  saveCache(wikiDir, cache);
  stdoutPrint(`Initialized: ${path.join(wikiDir, CACHE_FILE_NAME)}`);

  // .gitignore entry for the cache
  let gitignoreUpdated = false;
  const gitignore = path.join(root, ".gitignore");
  const cacheEntry = `${WIKI_DIR_NAME}/${CACHE_FILE_NAME}`;
  if (fs.existsSync(gitignore)) {
    const content = readFileText(gitignore);
    if (!content.includes(cacheEntry)) {
      fs.appendFileSync(gitignore, `\n# project-wiki SHA baseline cache\n${cacheEntry}\n`, "utf8");
      gitignoreUpdated = true;
      stdoutPrint(`Added '${cacheEntry}' to .gitignore`);
    }
  } else {
    fs.writeFileSync(gitignore, `# project-wiki SHA baseline cache\n${cacheEntry}\n`, "utf8");
    gitignoreUpdated = true;
    stdoutPrint(`Created .gitignore with '${cacheEntry}'`);
  }

  if (JSON_MODE) {
    emitJson({
      command: "init",
      ok: true,
      summary: {
        language: lang,
        extensions: [...extensions].sort(),
        files: files.length,
        modules: modules.size,
        module_names: [...modules.keys()].sort(),
        generated,
        gitignore_updated: gitignoreUpdated,
      },
      signals: [],
    });
    return 0;
  }

  stdoutPrint(`\n✅ Wiki initialized at ${path.relative(root, wikiDir)}/`);
  stdoutPrint("\nNext steps:");
  stdoutPrint("  1. Edit each <module>.md to fill in file descriptions");
  stdoutPrint("  2. Edit overview.md to fill in module responsibilities");
  stdoutPrint("  3. Run 'python3 scripts/wiki.py update' to mark wiki as reviewed");
  stdoutPrint("  4. Run 'python3 scripts/wiki.py check' to verify no drift");

  return 0;
}

function cmdCheck(args) {
  const root = path.resolve(args.root);
  const wikiDir = path.join(root, WIKI_DIR_NAME);

  if (!fs.existsSync(wikiDir)) {
    stderrPrint(`Error: no docs/project_wiki/ found at ${root}`);
    stderrPrint("Run 'python3 scripts/wiki.py init' first.");
    return 2;
  }

  const cache = loadCache(wikiDir);
  const cachedFiles = cache.files || {};

  let extensions;
  if (Object.keys(cachedFiles).length) {
    const exts = new Set();
    for (const p of Object.keys(cachedFiles)) {
      const ext = path.extname(p).toLowerCase();
      if (ext) exts.add(ext);
    }
    extensions = [...exts];
  } else {
    extensions = getExtensionsForLang(detectLanguage(root));
  }

  const files = scanProject(root, extensions);
  const currentPaths = new Set(files.map((f) => f.path));
  const currentByPath = {};
  for (const f of files) currentByPath[f.path] = f;
  const cachedPaths = new Set(Object.keys(cachedFiles));

  // Parse module wikis, keyed by file stem (module name)
  const moduleWikiMap = {};
  let wikiMdFiles = [];
  try {
    wikiMdFiles = fs
      .readdirSync(wikiDir)
      .filter((f) => f.endsWith(".md"))
      .sort()
      .map((f) => path.join(wikiDir, f));
  } catch (e) {
    /* ignore */
  }
  for (const wf of wikiMdFiles) {
    if (path.basename(wf) === "overview.md") continue;
    const mw = parseModuleWiki(wf);
    if (mw) moduleWikiMap[path.basename(wf, ".md")] = mw;
  }
  const wikiEntries = new Set();
  for (const mw of Object.values(moduleWikiMap)) {
    for (const k of Object.keys(mw.entries)) wikiEntries.add(k);
  }

  const report = {
    new_files: [],
    deleted_files: [],
    modified_files: [],
    total_tracked: Object.keys(cachedFiles).length,
    total_in_wiki: wikiEntries.size,
  };

  for (const p of [...currentPaths].sort()) {
    if (!cachedPaths.has(p)) {
      report.new_files.push(p);
    } else {
      const cachedSha = (cachedFiles[p] && cachedFiles[p].sha) || "";
      const currentSha = currentByPath[p].sha;
      if (cachedSha && currentSha && cachedSha !== currentSha) {
        const reviewed = cachedFiles[p] && cachedFiles[p].reviewed;
        if (reviewed) report.modified_files.push(p);
      }
    }
  }

  for (const p of [...cachedPaths].sort()) {
    if (!currentPaths.has(p)) report.deleted_files.push(p);
  }

  const hasStale =
    report.new_files.length || report.deleted_files.length || report.modified_files.length;
  const staleCount =
    report.new_files.length + report.deleted_files.length + report.modified_files.length;

  // L3: domain-language connectivity drift
  const l3 = detectL3Artifacts(root);
  let overviewContent = "";
  const overviewPath = path.join(wikiDir, "overview.md");
  if (fs.existsSync(overviewPath)) overviewContent = readFileText(overviewPath);

  const l3Details = [];

  if (l3.context_md) {
    if (!overviewContent.includes("CONTEXT.md")) {
      l3Details.push(
        `CONTEXT.md exists at ${path.relative(root, l3.context_md)} but overview.md doesn't link to it`
      );
    }
  } else if (overviewContent.includes("CONTEXT.md")) {
    l3Details.push("overview.md links to CONTEXT.md but the file no longer exists");
  }

  if (l3.adrs.length) {
    if (!overviewContent.includes("docs/adr/")) {
      l3Details.push(`${l3.adrs.length} ADRs exist in docs/adr/ but overview.md doesn't link to them`);
    }
  } else if (overviewContent.includes("docs/adr/")) {
    l3Details.push("overview.md links to docs/adr/ but no ADR files exist");
  }

  // ------------------------------------------------------------------
  // Wiki self-integrity: overview <-> module wikis <-> registration
  // ------------------------------------------------------------------
  const modulesFromCode = detectModules(files);
  const moduleNames = new Set(modulesFromCode.keys());
  const integrity = [];

  // 1. Module in code but its module wiki file is missing
  for (const m of [...moduleNames]
    .filter((m) => !moduleWikiMap[m])
    .sort()) {
    integrity.push(
      makeSignal(
        "WIKI-MODULE-WIKI-MISSING",
        m,
        `module '${m}' has ${modulesFromCode.get(m).length} source files but ${m}.md is missing`
      )
    );
  }

  // 2. Overview module index vs actual module set
  const overviewModules = new Set(
    fs.existsSync(overviewPath) ? Object.keys(parseOverview(overviewPath)) : []
  );
  for (const m of [...moduleNames].filter((m) => !overviewModules.has(m)).sort()) {
    integrity.push(
      makeSignal(
        "WIKI-OVERVIEW-MODULE-MISMATCH",
        m,
        `module '${m}' exists in code but is missing from the overview.md module index`
      )
    );
  }
  for (const m of [...overviewModules].filter((m) => !moduleNames.has(m)).sort()) {
    integrity.push(
      makeSignal(
        "WIKI-OVERVIEW-MODULE-MISMATCH",
        m,
        `module '${m}' is listed in overview.md but has no source files`
      )
    );
  }

  // 3. Registration table coverage per module
  for (const m of Object.keys(moduleWikiMap).sort()) {
    const mw = moduleWikiMap[m];
    const codePaths = new Set((modulesFromCode.get(m) || []).map((f) => f.path));
    const registered = new Set(Object.keys(mw.entries));
    for (const p of [...codePaths].filter((p) => !registered.has(p)).sort()) {
      integrity.push(
        makeSignal("WIKI-UNREGISTERED-FILE", p, `source file exists in module '${m}' but is not registered in ${m}.md`)
      );
    }
    for (const p of [...registered].filter((p) => !codePaths.has(p)).sort()) {
      integrity.push(
        makeSignal("WIKI-ORPHAN-ENTRY", p, `registered in ${m}.md but not present in code (module '${m}')`)
      );
    }
  }

  // ------------------------------------------------------------------
  // Assemble signals + summary
  // ------------------------------------------------------------------
  const allSignals = [];
  for (const p of report.new_files) {
    allSignals.push(makeSignal("WIKI-NEW-FILE", p, "in code, not yet in wiki"));
  }
  for (const p of report.deleted_files) {
    allSignals.push(makeSignal("WIKI-DELETED-FILE", p, "in baseline, gone from code"));
  }
  for (const p of report.modified_files) {
    allSignals.push(makeSignal("WIKI-MODIFIED-FILE", p, "SHA changed since last review"));
  }
  for (const d of l3Details) {
    allSignals.push(makeSignal("WIKI-L3-DRIFT", "", d));
  }
  for (const s of integrity) allSignals.push(s);
  const signals = sortSignals(allSignals);

  const l3Stale = l3Details.length > 0;
  const integrityStale = integrity.length > 0;
  const anyStale = !!hasStale || l3Stale || integrityStale;

  const summary = {
    tracked: report.total_tracked,
    in_wiki: report.total_in_wiki,
    current: files.length,
    new: report.new_files.length,
    deleted: report.deleted_files.length,
    modified: report.modified_files.length,
    l3_drift: l3Details.length,
    integrity: integrity.length,
  };

  if (JSON_MODE) {
    emitJson({ command: "check", ok: !anyStale, summary, signals });
    if (args.fail_on_stale && anyStale) return 1;
    return 0;
  }

  // ----- human output -----
  stdoutPrint("=".repeat(70));
  stdoutPrint("PROJECT WIKI DRIFT REPORT");
  stdoutPrint("=".repeat(70));
  stdoutPrint(`  Tracked files (baseline): ${report.total_tracked}`);
  stdoutPrint(`  Registered in wiki:       ${report.total_in_wiki}`);
  stdoutPrint(`  Current source files:     ${files.length}`);
  stdoutPrint("");

  if (report.new_files.length) {
    stdoutPrint(`🟡 NEW FILES (${report.new_files.length}) — in code, not yet in wiki:`);
    for (const p of report.new_files) stdoutPrint(`    + ${p}`);
    stdoutPrint("");
  }
  if (report.deleted_files.length) {
    stdoutPrint(`🔴 DELETED FILES (${report.deleted_files.length}) — in wiki/baseline, gone from code:`);
    for (const p of report.deleted_files) stdoutPrint(`    - ${p}`);
    stdoutPrint("");
  }
  if (report.modified_files.length) {
    stdoutPrint(`🟠 MODIFIED FILES (${report.modified_files.length}) — SHA changed since last review:`);
    for (const p of report.modified_files) stdoutPrint(`    ~ ${p}`);
    stdoutPrint("");
  }

  if (l3Details.length) {
    stdoutPrint(`🔵 L3 DOMAIN-LANGUAGE DRIFT (${l3Details.length}):`);
    for (const d of l3Details) stdoutPrint(`    ${d}`);
    stdoutPrint("");
  }

  if (integrity.length) {
    stdoutPrint(`🟣 WIKI INTEGRITY (${integrity.length}):`);
    for (const s of integrity) stdoutPrint(`    ! [${s.code}] ${s.detail}`);
    stdoutPrint("");
  }

  if (!anyStale) {
    stdoutPrint("✅ Wiki is up to date — no drift detected.");
    return 0;
  }

  stdoutPrint("-".repeat(70));
  const totalStale = staleCount + l3Details.length + integrity.length;
  stdoutPrint(
    `TOTAL STALE: ${totalStale} ` +
      `(${report.new_files.length} new, ` +
      `${report.deleted_files.length} deleted, ` +
      `${report.modified_files.length} modified, ` +
      `${l3Details.length} L3 drift, ` +
      `${integrity.length} integrity)`
  );
  stdoutPrint("");
  stdoutPrint("Actions:");
  if (report.new_files.length)
    stdoutPrint("  • Add new files to the appropriate <module>.md file registration table");
  if (report.deleted_files.length)
    stdoutPrint("  • Remove deleted file entries from <module>.md tables");
  if (report.modified_files.length)
    stdoutPrint("  • Review modified files and update descriptions if responsibilities changed");
  if (l3Stale)
    stdoutPrint("  • Run 'python3 scripts/wiki.py update' to re-link L3 domain-language artifacts");
  if (integrity.some((s) => s.code === "WIKI-MODULE-WIKI-MISSING"))
    stdoutPrint("  • Run 'python3 scripts/wiki.py update' to generate missing module wiki skeletons");
  if (integrity.some((s) => s.code === "WIKI-UNREGISTERED-FILE" || s.code === "WIKI-ORPHAN-ENTRY"))
    stdoutPrint("  • Sync <module>.md registration tables with the actual file set");
  if (anyStale) stdoutPrint("  • Run 'python3 scripts/wiki.py update' after making changes");
  stdoutPrint("-".repeat(70));

  if (args.fail_on_stale && anyStale) return 1;
  return 0;
}

function cmdUpdate(args) {
  const root = path.resolve(args.root);
  const wikiDir = path.join(root, WIKI_DIR_NAME);

  if (!fs.existsSync(wikiDir)) {
    stderrPrint(`Error: no docs/project_wiki/ found at ${root}`);
    return 2;
  }

  const cache = loadCache(wikiDir);
  const cachedFiles = cache.files || {};

  let extensions;
  if (Object.keys(cachedFiles).length) {
    const exts = new Set();
    for (const p of Object.keys(cachedFiles)) {
      const ext = path.extname(p).toLowerCase();
      if (ext) exts.add(ext);
    }
    extensions = [...exts];
  } else {
    extensions = getExtensionsForLang(detectLanguage(root));
  }

  const files = scanProject(root, extensions);

  // Create module wiki skeletons for modules that lack one
  // (repair path for WIKI-MODULE-WIKI-MISSING)
  const modules = detectModules(files);
  const moduleWikisCreated = [];
  for (const moduleName of [...modules.keys()].sort()) {
    const modulePath = path.join(wikiDir, `${moduleName}.md`);
    if (!fs.existsSync(modulePath)) {
      fs.writeFileSync(modulePath, generateModuleContent(moduleName, modules.get(moduleName)), "utf8");
      moduleWikisCreated.push(`${moduleName}.md`);
      stdoutPrint(`Created: ${path.relative(root, modulePath)} (skeleton — fill in descriptions)`);
    }
  }

  const newCache = { files: {}, last_updated: null };
  for (const f of files) {
    newCache.files[f.path] = { sha: f.sha, module: f.module, reviewed: true };
  }

  const oldPaths = new Set(Object.keys(cachedFiles));
  const newPaths = new Set(Object.keys(newCache.files));
  const added = [...newPaths].filter((p) => !oldPaths.has(p));
  const removed = [...oldPaths].filter((p) => !newPaths.has(p));
  const shaChanged = [];
  for (const p of [...newPaths].filter((p) => oldPaths.has(p))) {
    const oldSha = (cachedFiles[p] && cachedFiles[p].sha) || "";
    const newSha = newCache.files[p].sha;
    if (oldSha !== newSha) shaChanged.push(p);
  }

  saveCache(wikiDir, newCache);

  stdoutPrint(`✅ SHA baseline updated at ${path.join(wikiDir, CACHE_FILE_NAME)}`);
  stdoutPrint(`   Total files tracked: ${Object.keys(newCache.files).length}`);
  if (added.length) stdoutPrint(`   Added: ${added.length}`);
  if (removed.length) stdoutPrint(`   Removed: ${removed.length}`);
  if (shaChanged.length) stdoutPrint(`   SHA updated: ${shaChanged.length}`);

  // Refresh overview.md statistics, preserving existing module descriptions.
  let overviewUpdated = false;
  const overviewPath = path.join(wikiDir, "overview.md");
  if (fs.existsSync(overviewPath)) {
    let content = generateOverviewContent(modules, root);
    const oldOverview = parseOverview(overviewPath);
    for (const [moduleName, info] of Object.entries(oldOverview)) {
      if (info.desc.includes("<one-line responsibility>")) continue;
      let desc = info.desc;
      const prefixMatch = desc.match(/^_\d+ source files_ — (.+)$/);
      if (prefixMatch) desc = prefixMatch[1];
      const fileCount = (modules.get(moduleName) || []).length;
      const oldRow = `| \`${moduleName}\` | _${fileCount} source files_ — <one-line responsibility> |`;
      const newRow = `| \`${moduleName}\` | _${fileCount} source files_ — ${desc} |`;
      content = content.split(oldRow).join(newRow);
    }
    fs.writeFileSync(overviewPath, content, "utf8");
    overviewUpdated = true;
    stdoutPrint(`   Updated: ${path.relative(root, overviewPath)}`);
  }

  if (JSON_MODE) {
    emitJson({
      command: "update",
      ok: true,
      summary: {
        tracked: Object.keys(newCache.files).length,
        added: added.length,
        removed: removed.length,
        sha_updated: shaChanged.length,
        module_wikis_created: moduleWikisCreated,
        overview_updated: overviewUpdated,
      },
      signals: [],
    });
  }

  return 0;
}

function cmdStatus(args) {
  const root = path.resolve(args.root);
  const wikiDir = path.join(root, WIKI_DIR_NAME);

  if (!fs.existsSync(wikiDir)) {
    stdoutPrint(`❌ No docs/project_wiki/ found at ${root}`);
    stdoutPrint("   Run 'python3 scripts/wiki.py init' to create one.");
    return 2;
  }

  const cache = loadCache(wikiDir);
  const cachedFiles = cache.files || {};
  const lastUpdated = cache.last_updated || "never";

  let wikiFiles = [];
  try {
    wikiFiles = fs
      .readdirSync(wikiDir)
      .filter((f) => f.endsWith(".md"))
      .map((f) => path.join(wikiDir, f));
  } catch (e) {
    /* ignore */
  }
  const moduleWikis = wikiFiles.filter((f) => path.basename(f) !== "overview.md");

  let totalEntries = 0;
  let filledEntries = 0;
  for (const wf of moduleWikis) {
    const mw = parseModuleWiki(wf);
    if (!mw) continue;
    totalEntries += Object.keys(mw.entries).length;
    for (const e of Object.values(mw.entries)) {
      if (!e.description.startsWith("<")) filledEntries++;
    }
  }

  let unreviewed = 0;
  for (const v of Object.values(cachedFiles)) {
    if (!v || !v.reviewed) unreviewed++;
  }

  const l3 = detectL3Artifacts(root);
  const l3Count =
    (l3.context_md ? 1 : 0) + (l3.adrs.length ? 1 : 0) + (l3.glossary ? 1 : 0);
  const needsAttention = unreviewed > 0 || filledEntries < totalEntries;

  if (JSON_MODE) {
    emitJson({
      command: "status",
      ok: true,
      summary: {
        module_wikis: moduleWikis.length,
        tracked: Object.keys(cachedFiles).length,
        entries: totalEntries,
        described_entries: filledEntries,
        unreviewed,
        last_updated: lastUpdated,
        l3_linked: l3Count > 0,
        needs_attention: needsAttention,
      },
      signals: [],
    });
    return 0;
  }

  stdoutPrint("=".repeat(50));
  stdoutPrint("PROJECT WIKI STATUS");
  stdoutPrint("=".repeat(50));
  stdoutPrint(`  Wiki directory:     ${path.relative(root, wikiDir)}/`);
  stdoutPrint(`  Module wikis:       ${moduleWikis.length}`);
  stdoutPrint(`  Tracked files:      ${Object.keys(cachedFiles).length}`);
  const pct = totalEntries ? Math.floor((100 * filledEntries) / totalEntries) : 0;
  stdoutPrint(`  Wiki entries:       ${totalEntries}`);
  stdoutPrint(`  Described entries:  ${filledEntries}/${totalEntries} (${pct}%)`);
  stdoutPrint(`  Unreviewed files:   ${unreviewed}`);
  stdoutPrint(`  Last updated:       ${lastUpdated}`);
  stdoutPrint(`  L3 domain language: ${l3Count ? "✅ linked" : "❌ not found"}`);
  if (l3.context_md) stdoutPrint(`    CONTEXT.md:         ${path.relative(root, l3.context_md)}`);
  if (l3.adrs.length)
    stdoutPrint(`    ADRs:               ${l3.adrs.length} in ${path.relative(root, path.dirname(l3.adrs[0]))}`);
  if (l3.glossary) stdoutPrint(`    Hand-curated:       ${path.relative(root, l3.glossary)}`);
  stdoutPrint("");

  if (needsAttention) {
    stdoutPrint("⚠️  Wiki needs attention:");
    if (filledEntries < totalEntries)
      stdoutPrint(`   • ${totalEntries - filledEntries} entries still have placeholder descriptions`);
    if (unreviewed) stdoutPrint(`   • ${unreviewed} files not yet marked as reviewed`);
    stdoutPrint("   Run 'python3 scripts/wiki.py check' for details.");
  } else {
    stdoutPrint("✅ Wiki looks complete and up to date.");
  }

  return 0;
}

// ---------------------------------------------------------------------------
// Argument parsing & main
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  const args = { command: null, root: ".", lang: "auto", extensions: null, fail_on_stale: false, json: false };
  const rest = argv.slice(0);
  if (rest.length === 0) return args;
  args.command = rest[0];
  for (let i = 1; i < rest.length; i++) {
    const a = rest[i];
    if (a === "--root") {
      args.root = rest[++i];
    } else if (a === "--lang") {
      args.lang = rest[++i];
    } else if (a === "--extensions") {
      args.extensions = rest[++i];
    } else if (a === "--fail-on-stale") {
      args.fail_on_stale = true;
    } else if (a === "--json") {
      args.json = true;
    } else if (a.startsWith("--root=")) {
      args.root = a.slice("--root=".length);
    } else if (a.startsWith("--lang=")) {
      args.lang = a.slice("--lang=".length);
    } else if (a.startsWith("--extensions=")) {
      args.extensions = a.slice("--extensions=".length);
    }
  }
  return args;
}

function printHelp() {
  stdoutPrint("usage: wiki.py [-h] {init,check,update,status} ...");
  stdoutPrint("");
  stdoutPrint("Maintain a three-level project knowledge base (docs/project_wiki/).");
  stdoutPrint("");
  stdoutPrint("positional arguments:");
  stdoutPrint("  {init,check,update,status}");
  stdoutPrint("                        Available commands");
  stdoutPrint("");
  stdoutPrint("options:");
  stdoutPrint("  -h, --help            show this help message and exit");
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.json) JSON_MODE = true;
  switch (args.command) {
    case "init":
      return cmdInit(args);
    case "check":
      return cmdCheck(args);
    case "update":
      return cmdUpdate(args);
    case "status":
      return cmdStatus(args);
    default:
      printHelp();
      return 1;
  }
}

process.exit(main());
