#!/usr/bin/env python3
"""
project-wiki CLI — maintain a three-level project knowledge base.

L1: project_wiki/overview.md  — module index table (name + one-line responsibility)
L2: project_wiki/<module>.md  — file-level registration table per module
L3: (optional) semantic bridges — left as plugin points, not managed here

Commands:
    init    Scan the project, detect modules, generate wiki skeleton.
    check   Compare current code state with wiki; report drift (triage).
    update  Refresh SHA baseline cache after wiki has been reviewed.
    status  Show wiki coverage summary.

Usage:
    python3 wiki.py init   [--root .] [--lang auto] [--extensions .go,.py,...] [--json]
    python3 wiki.py check  [--root .] [--fail-on-stale] [--json]
    python3 wiki.py update [--root .] [--json]
    python3 wiki.py status [--root .] [--json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WIKI_DIR_NAME = "docs/project_wiki"
CACHE_FILE_NAME = ".review_cache.json"

# Stable finding/signal codes — public contract for CI, hooks, and agents.
# Keep codes stable; adding new ones is additive, renaming is a breaking change.
SIGNAL_CODES = {
    "WIKI-NEW-FILE",                 # file in code, not in SHA baseline
    "WIKI-DELETED-FILE",             # in baseline, gone from code
    "WIKI-MODIFIED-FILE",            # SHA changed since last review
    "WIKI-L3-DRIFT",                 # L3 domain-language link drift
    "WIKI-MODULE-WIKI-MISSING",      # module has source files but no <module>.md
    "WIKI-OVERVIEW-MODULE-MISMATCH",  # overview index vs actual module set
    "WIKI-UNREGISTERED-FILE",        # source file missing from registration table
    "WIKI-ORPHAN-ENTRY",             # registration row for a file not in code
}

# Source file extensions by language. "auto" tries all of them.
LANG_EXTENSIONS: dict[str, list[str]] = {
    "go": [".go"],
    "python": [".py"],
    "javascript": [".js", ".jsx", ".mjs", ".cjs"],
    "typescript": [".ts", ".tsx"],
    "vue": [".vue"],
    "rust": [".rs"],
    "java": [".java"],
    "kotlin": [".kt", ".kts"],
    "swift": [".swift"],
    "objc": [".h", ".m", ".mm"],
    "c": [".c", ".h"],
    "cpp": [".cpp", ".cc", ".cxx", ".hpp", ".h"],
    "ruby": [".rb"],
    "php": [".php"],
    "csharp": [".cs"],
    "scala": [".scala"],
    "elixir": [".ex", ".exs"],
    "lua": [".lua"],
    "dart": [".dart"],
    "generic": [".go", ".py", ".js", ".jsx", ".mjs", ".ts", ".tsx", ".rs",
                ".java", ".kt", ".swift", ".c", ".h", ".cpp", ".cc", ".hpp",
                ".rb", ".php", ".cs", ".scala", ".ex", ".lua", ".dart",
                ".m", ".mm", ".vue", ".svelte"],
}

# Directories to always skip during scanning.
SKIP_DIRS = {
    ".git", ".svn", ".hg", ".pi", ".agent", ".agents", ".claude",
    "node_modules", "vendor", "venv", ".venv", "env", ".env",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".tox",
    "dist", "build", "target", "out", ".next", ".nuxt",
    ".idea", ".vscode", "coverage", ".coverage",
    "project_wiki",  # don't scan the wiki itself (under docs/)
    ".cache", "tmp", "temp", ".tmp",
}

# Files to always skip.
SKIP_FILE_PATTERNS = [
    r".*_test\.go$",
    r".*_test\.py$",
    r".*\.test\.[jt]sx?$",
    r".*\.spec\.[jt]sx?$",
    r".*\.bench\.[jt]sx?$",
    r".*\.mock\.[jt]sx?$",
    r".*\.gen\.go$",
    r".*\.pb\.go$",
    r".*\.pb\.py$",
    r".*_pb2\.py$",
    r".*_string\.go$",
    r"zz_generated_.*\.go$",
    r".*\.min\.js$",
    r".*\.min\.css$",
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SourceFile:
    """A source file discovered in the project."""
    path: str          # relative to project root, e.g. "src/auth/login.go"
    module: str        # detected module name, e.g. "auth"
    sha: str           # SHA1 of file content
    size: int          # file size in bytes
    lines: int         # line count


@dataclass
class WikiEntry:
    """A file entry registered in a module wiki."""
    path: str
    description: str = ""


@dataclass
class ModuleWiki:
    """Parsed content of a module wiki file."""
    module_id: str
    root_dirs: list[str] = field(default_factory=list)
    desc: str = ""
    entries: dict[str, WikiEntry] = field(default_factory=dict)  # path -> entry


@dataclass
class DriftReport:
    """Result of comparing current code with wiki baseline."""
    new_files: list[str] = field(default_factory=list)        # in code, not in wiki
    deleted_files: list[str] = field(default_factory=list)    # in wiki, not in code
    modified_files: list[str] = field(default_factory=list)   # SHA changed since last review
    total_tracked: int = 0
    total_in_wiki: int = 0

    @property
    def has_stale(self) -> bool:
        return bool(self.new_files or self.deleted_files or self.modified_files)

    @property
    def stale_count(self) -> int:
        return len(self.new_files) + len(self.deleted_files) + len(self.modified_files)


# ---------------------------------------------------------------------------
# Output helpers (human output is suppressed in --json mode)
# ---------------------------------------------------------------------------

_JSON_MODE = False


def say(*values: object, **kwargs: object) -> None:
    """Human-output printer. Suppressed when --json is active."""
    if not _JSON_MODE:
        print(*values, **kwargs)  # type: ignore[arg-type]


def emit_json(result: dict) -> None:
    """Emit the structured result object — the only stdout in --json mode."""
    print(json.dumps(result, indent=2, sort_keys=True))


def make_signal(code: str, path: str, detail: str) -> dict:
    """Build one stable finding entry (code + path + detail)."""
    return {"code": code, "path": path, "detail": detail}


def sort_signals(signals: list[dict]) -> list[dict]:
    """Deterministic signal ordering: by code, then path, then detail."""
    return sorted(signals, key=lambda s: (s["code"], s["path"], s["detail"]))


# ---------------------------------------------------------------------------
# File scanning
# ---------------------------------------------------------------------------

def should_skip_file(filename: str) -> bool:
    """Check if a file matches any skip pattern."""
    for pattern in SKIP_FILE_PATTERNS:
        if re.match(pattern, filename):
            return True
    return False


def compute_sha(filepath: Path) -> str:
    """Compute SHA1 hash of file content."""
    h = hashlib.sha1()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    except (OSError, PermissionError):
        return ""
    return h.hexdigest()


def count_lines(filepath: Path) -> int:
    """Count lines in a file."""
    try:
        with open(filepath, "r", errors="replace") as f:
            return sum(1 for _ in f)
    except (OSError, PermissionError):
        return 0


def scan_project(root: Path, extensions: list[str]) -> list[SourceFile]:
    """
    Walk the project tree and collect all source files.

    Returns a list of SourceFile sorted by path.
    """
    files: list[SourceFile] = []
    ext_set = set(ext.lower() for ext in extensions)

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skip directories in-place (os.walk respects this)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in ext_set:
                continue
            if should_skip_file(fname):
                continue

            full_path = Path(dirpath) / fname
            rel_path = str(full_path.relative_to(root))

            # Determine module: first directory component under root
            parts = Path(rel_path).parts
            if len(parts) <= 1:
                module = "root"
            else:
                module = parts[0]

            sha = compute_sha(full_path)
            size = full_path.stat().st_size if full_path.exists() else 0
            lines = count_lines(full_path)

            files.append(SourceFile(
                path=rel_path,
                module=module,
                sha=sha,
                size=size,
                lines=lines,
            ))

    files.sort(key=lambda f: f.path)
    return files


# ---------------------------------------------------------------------------
# Module detection
# ---------------------------------------------------------------------------

def detect_language(root: Path) -> str:
    """Auto-detect the primary language of the project."""
    # Count files by language
    lang_counts: dict[str, int] = {}

    for lang, exts in LANG_EXTENSIONS.items():
        if lang == "generic":
            continue
        ext_set = set(exts)
        count = 0
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fname in filenames:
                ext = os.path.splitext(fname)[1].lower()
                if ext in ext_set:
                    count += 1
        if count > 0:
            lang_counts[lang] = count

    if not lang_counts:
        return "generic"

    # Return the language with the most files
    primary = max(lang_counts, key=lang_counts.get)

    # JS/TS/Vue coexist — if any of them is primary, include all three.
    # This handles the common monorepo / frontend case where .vue + .ts + .js
    # live side by side and we don't want to miss any.
    web_langs = {"javascript", "typescript", "vue"}
    if primary in web_langs and lang_counts.keys() & web_langs:
        return "web"  # sentinel; get_extensions_for_lang handles it

    return primary


def get_extensions_for_lang(lang: str) -> list[str]:
    """Get file extensions for a language."""
    if lang in ("auto", "web"):
        # 'web' is the sentinel from detect_language for JS+TS+Vue projects.
        # 'auto' falls through to generic (all known extensions).
        if lang == "web":
            return [".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".vue", ".svelte"]
        return LANG_EXTENSIONS["generic"]
    return LANG_EXTENSIONS.get(lang, LANG_EXTENSIONS["generic"])


def detect_modules(files: list[SourceFile]) -> dict[str, list[SourceFile]]:
    """
    Group files into modules based on top-level directory.

    Returns a dict: module_name -> list of SourceFile.
    Files at root level go into "root" module.
    """
    modules: dict[str, list[SourceFile]] = {}
    for f in files:
        modules.setdefault(f.module, []).append(f)
    return modules


# ---------------------------------------------------------------------------
# Wiki file parsing and generation
# ---------------------------------------------------------------------------

def parse_module_wiki(wiki_path: Path) -> ModuleWiki | None:
    """
    Parse a module wiki markdown file.

    Extracts:
    - module_id from <!-- module_id: xxx --> comment
    - root_dirs from <!-- root_dirs: ... --> comment
    - desc from <!-- desc: xxx --> comment
    - file entries from the registration table
    """
    if not wiki_path.exists():
        return None

    content = wiki_path.read_text(errors="replace")
    mw = ModuleWiki(module_id=wiki_path.stem)

    # Extract metadata comments
    id_match = re.search(r"<!--\s*module_id:\s*(.+?)\s*-->", content)
    if id_match:
        mw.module_id = id_match.group(1).strip()

    dirs_match = re.search(r"<!--\s*root_dirs:\s*(.+?)\s*-->", content, re.DOTALL)
    if dirs_match:
        raw = dirs_match.group(1).strip()
        # Handle both inline "a, b" and multi-line with "- " prefixes
        dirs = [d.strip().lstrip("- ").strip() for d in raw.replace("\n", ",").split(",")]
        mw.root_dirs = [d for d in dirs if d]

    desc_match = re.search(r"<!--\s*desc:\s*(.+?)\s*-->", content, re.DOTALL)
    if desc_match:
        mw.desc = desc_match.group(1).strip().replace("\n", " ")

    # Parse file registration table rows
    # Format: | `path` | description |
    # Or:    | path   | description |
    table_pattern = re.compile(
        r"^\|\s*`?([^`|]+?)`?\s*\|\s*([^|]*?)\s*\|",
        re.MULTILINE
    )
    for match in table_pattern.finditer(content):
        path = match.group(1).strip()
        desc = match.group(2).strip()

        # Skip header rows and separator rows
        if path in ("文件", "File", "file", "Path", "path", "---", "—", ""):
            continue
        if path.startswith("---") or path.startswith(":--"):
            continue
        # Skip module-level metadata that might be in table format
        if path.startswith("<!--"):
            continue

        mw.entries[path] = WikiEntry(path=path, description=desc)

    return mw


def parse_overview(wiki_path: Path) -> dict[str, dict]:
    """
    Parse overview.md to get the module index table.

    Returns: { module_name: {"desc": ..., "link": ...} }
    """
    if not wiki_path.exists():
        return {}

    content = wiki_path.read_text(errors="replace")
    modules: dict[str, dict] = {}

    # Parse table rows: | module | desc | link |
    # The module column might be `code`, the desc is text, link is [text](url) or `file.md`
    table_pattern = re.compile(
        r"^\|\s*`?([^`|]+?)`?\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|",
        re.MULTILINE
    )
    for match in table_pattern.finditer(content):
        name = match.group(1).strip()
        desc = match.group(2).strip()
        link = match.group(3).strip()

        if name in ("模块", "Module", "module", "---", "—", ""):
            continue
        if name.startswith("---") or name.startswith(":--"):
            continue

        modules[name] = {"desc": desc, "link": link}

    return modules


# ---------------------------------------------------------------------------
# Wiki generation
# ---------------------------------------------------------------------------

def detect_l3_artifacts(root: Path) -> dict:
    """Detect L3 domain-modeling artifacts at the project root.

    Returns a dict with keys:
        context_md: Path | None  — CONTEXT.md location (root or docs/)
        adrs: list[Path]         — ADR files in docs/adr/
        glossary: Path | None    — hand-curated glossary in project_wiki/
    """
    result = {"context_md": None, "adrs": [], "glossary": None}

    # CONTEXT.md — check root first, then docs/
    for candidate in [root / "CONTEXT.md", root / "docs" / "CONTEXT.md"]:
        if candidate.exists():
            result["context_md"] = candidate
            break

    # ADRs — docs/adr/*.md
    adr_dir = root / "docs" / "adr"
    if adr_dir.is_dir():
        result["adrs"] = sorted(adr_dir.glob("*.md"))

    # Hand-curated glossary in project_wiki/
    wiki_glossary = root / WIKI_DIR_NAME / "glossary.md"
    if wiki_glossary.exists():
        result["glossary"] = wiki_glossary

    return result


def generate_overview_content(
    modules: dict[str, list[SourceFile]],
    root: Path | None = None,
) -> str:
    """Generate overview.md content from detected modules.

    If root is provided, detect L3 artifacts (CONTEXT.md, ADRs) and
    add a Domain Language section linking to them.
    """
    lines = [
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
    ]

    for module_name in sorted(modules.keys()):
        files = modules[module_name]
        file_count = len(files)
        wiki_link = f"[{module_name}.md]({module_name}.md)"
        desc = f"_{file_count} source files_ — <one-line responsibility>"
        lines.append(f"| `{module_name}` | {desc} | {wiki_link} |")

    # L3: Domain Language section — links to domain-modeling outputs
    if root is not None:
        l3 = detect_l3_artifacts(root)
        l3_lines: list[str] = []

        if l3["context_md"]:
            rel = os.path.relpath(l3["context_md"], root / WIKI_DIR_NAME)
            l3_lines.append(f"- Vocabulary: [CONTEXT.md]({rel})")

        if l3["adrs"]:
            adr_dir = l3["adrs"][0].parent
            rel = os.path.relpath(adr_dir, root / WIKI_DIR_NAME)
            l3_lines.append(f"- Decisions: [docs/adr/]({rel}) ({len(l3['adrs'])} ADRs)")

        if l3["glossary"]:
            l3_lines.append(f"- Hand-curated glossary: [glossary.md](glossary.md)")

        if l3_lines:
            lines.extend([
                "",
                "## Domain Language",
                "",
                "> L3: concept map — what terms mean and why decisions were made.",
                "> Read this before the module index if you're new to the domain.",
                "",
            ])
            lines.extend(l3_lines)

    lines.extend([
        "",
        "## Statistics",
        "",
        f"- Total modules: {len(modules)}",
        f"- Total source files: {sum(len(fs) for fs in modules.values())}",
        f"- Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "---",
        "",
        "> **Maintenance**: Run `python3 scripts/wiki.py check` to detect drift.",
        "> Run `python3 scripts/wiki.py update` after reviewing and updating wiki entries.",
        "",
    ])

    return "\n".join(lines)


def generate_module_content(module_name: str, files: list[SourceFile]) -> str:
    """Generate a module wiki file content."""
    # Determine root_dirs from file paths
    root_dirs_set: set[str] = set()
    for f in files:
        parts = Path(f.path).parts
        if len(parts) > 1:
            root_dirs_set.add(parts[0])
    root_dirs = sorted(root_dirs_set) if root_dirs_set else [module_name]

    lines = [
        f"<!-- module_id: {module_name} -->",
        f"<!-- root_dirs:",
    ]
    for d in root_dirs:
        lines.append(f"  - {d}/")
    lines.extend([
        "-->",
        f"<!-- desc: <one-line responsibility for {module_name}> -->",
        "",
        f"# Module: {module_name}",
        "",
        f"> L2 knowledge base — file-level registration for the `{module_name}` module.",
        "",
        "## File Registration",
        "",
        "| File | Description |",
        "| ---- | ----------- |",
    ])

    for f in files:
        # Truncate long paths for readability
        display_path = f"`{f.path}`"
        desc = f"<describe {Path(f.path).name}>"
        lines.append(f"| {display_path} | {desc} |")

    lines.extend([
        "",
        "## Statistics",
        "",
        f"- Source files: {len(files)}",
        f"- Total lines: {sum(f.lines for f in files)}",
        "",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Cache (SHA baseline) management
# ---------------------------------------------------------------------------

def load_cache(wiki_dir: Path) -> dict:
    """Load the SHA baseline cache."""
    cache_path = wiki_dir / CACHE_FILE_NAME
    if not cache_path.exists():
        return {"files": {}, "last_updated": None}
    try:
        return json.loads(cache_path.read_text())
    except (json.JSONDecodeError, OSError):
        return {"files": {}, "last_updated": None}


def save_cache(wiki_dir: Path, cache: dict) -> None:
    """Save the SHA baseline cache."""
    cache_path = wiki_dir / CACHE_FILE_NAME
    cache["last_updated"] = datetime.now(timezone.utc).isoformat()
    cache_path.write_text(json.dumps(cache, indent=2, sort_keys=True) + "\n")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_init(args: argparse.Namespace) -> int:
    """Initialize or regenerate the project wiki."""
    root = Path(args.root).resolve()
    wiki_dir = root / WIKI_DIR_NAME

    if not root.exists():
        print(f"Error: project root does not exist: {root}", file=sys.stderr)
        return 1

    # Determine extensions
    lang = args.lang
    if lang == "auto":
        lang = detect_language(root)
        say(f"Detected language: {lang}")

    extensions = get_extensions_for_lang(lang)
    if args.extensions:
        extensions = [e.strip() for e in args.extensions.split(",")]

    say(f"Scanning for extensions: {', '.join(extensions)}")

    # Scan project
    files = scan_project(root, extensions)
    if not files:
        print("Error: no source files found. Check --lang or --extensions.", file=sys.stderr)
        return 1

    modules = detect_modules(files)
    say(f"Found {len(files)} source files in {len(modules)} module(s):")
    for name, mod_files in sorted(modules.items()):
        say(f"  {name}: {len(mod_files)} files")

    # Create wiki directory
    wiki_dir.mkdir(parents=True, exist_ok=True)

    # Generate overview.md
    generated: list[str] = []
    overview_path = wiki_dir / "overview.md"
    overview_content = generate_overview_content(modules, root)
    overview_path.write_text(overview_content)
    generated.append(str(overview_path.relative_to(root)))
    say(f"\nGenerated: {overview_path.relative_to(root)}")

    # Generate module wikis
    for module_name, mod_files in sorted(modules.items()):
        module_path = wiki_dir / f"{module_name}.md"
        content = generate_module_content(module_name, mod_files)
        module_path.write_text(content)
        generated.append(str(module_path.relative_to(root)))
        say(f"Generated: {module_path.relative_to(root)}")

    # Initialize SHA cache
    cache: dict = {"files": {}, "last_updated": None}
    for f in files:
        cache["files"][f.path] = {
            "sha": f.sha,
            "module": f.module,
            "reviewed": False,
        }
    save_cache(wiki_dir, cache)
    say(f"Initialized: {wiki_dir / CACHE_FILE_NAME}")

    # Create .gitignore entry for cache if not exists
    gitignore_updated = False
    gitignore = root / ".gitignore"
    cache_entry = f"{WIKI_DIR_NAME}/{CACHE_FILE_NAME}"
    if gitignore.exists():
        content = gitignore.read_text()
        if cache_entry not in content:
            with open(gitignore, "a") as gf:
                gf.write(f"\n# project-wiki SHA baseline cache\n{cache_entry}\n")
            gitignore_updated = True
            say(f"Added '{cache_entry}' to .gitignore")
    else:
        gitignore.write_text(f"# project-wiki SHA baseline cache\n{cache_entry}\n")
        gitignore_updated = True
        say(f"Created .gitignore with '{cache_entry}'")

    if _JSON_MODE:
        emit_json({
            "command": "init",
            "ok": True,
            "summary": {
                "language": lang,
                "extensions": sorted(extensions),
                "files": len(files),
                "modules": len(modules),
                "module_names": sorted(modules.keys()),
                "generated": generated,
                "gitignore_updated": gitignore_updated,
            },
            "signals": [],
        })
        return 0

    say(f"\n✅ Wiki initialized at {wiki_dir.relative_to(root)}/")
    say("\nNext steps:")
    say("  1. Edit each <module>.md to fill in file descriptions")
    say("  2. Edit overview.md to fill in module responsibilities")
    say("  3. Run 'python3 scripts/wiki.py update' to mark wiki as reviewed")
    say("  4. Run 'python3 scripts/wiki.py check' to verify no drift")

    return 0


def cmd_check(args: argparse.Namespace) -> int:
    """Check for drift between code and wiki."""
    root = Path(args.root).resolve()
    wiki_dir = root / WIKI_DIR_NAME

    if not wiki_dir.exists():
        print(f"Error: no docs/project_wiki/ found at {root}", file=sys.stderr)
        print("Run 'python3 scripts/wiki.py init' first.", file=sys.stderr)
        return 2

    cache = load_cache(wiki_dir)
    cached_files: dict = cache.get("files", {})

    # Determine extensions from cache or re-detect
    # Try to infer from cached file extensions
    if cached_files:
        exts = set()
        for path in cached_files:
            ext = os.path.splitext(path)[1].lower()
            if ext:
                exts.add(ext)
        extensions = list(exts)
    else:
        lang = detect_language(root)
        extensions = get_extensions_for_lang(lang)

    # Scan current state
    files = scan_project(root, extensions)
    current_paths = {f.path for f in files}
    current_by_path = {f.path: f for f in files}
    cached_paths = set(cached_files.keys())

    # Parse module wikis, keyed by file stem (module name)
    module_wiki_map: dict[str, ModuleWiki] = {}
    for wiki_file in sorted(wiki_dir.glob("*.md")):
        if wiki_file.name == "overview.md":
            continue
        mw = parse_module_wiki(wiki_file)
        if mw:
            module_wiki_map[wiki_file.stem] = mw
    wiki_entries: set[str] = set()
    for mw in module_wiki_map.values():
        wiki_entries.update(mw.entries.keys())

    # Build drift report
    report = DriftReport()
    report.total_tracked = len(cached_files)
    report.total_in_wiki = len(wiki_entries)

    for path in sorted(current_paths):
        if path not in cached_paths:
            # New file — in code but not in the baseline cache
            report.new_files.append(path)
        else:
            cached_sha = cached_files[path].get("sha", "")
            current_sha = current_by_path[path].sha
            if cached_sha and current_sha and cached_sha != current_sha:
                # File was reviewed but has since changed
                reviewed = cached_files[path].get("reviewed", False)
                if reviewed:
                    report.modified_files.append(path)

    for path in sorted(cached_paths):
        if path not in current_paths:
            report.deleted_files.append(path)

    # L3: domain-language connectivity drift
    l3 = detect_l3_artifacts(root)
    overview_content = ""
    overview_path = wiki_dir / "overview.md"
    if overview_path.exists():
        overview_content = overview_path.read_text(errors="replace")

    l3_details: list[str] = []
    if l3["context_md"]:
        if "CONTEXT.md" not in overview_content:
            l3_details.append(
                f"CONTEXT.md exists at {l3['context_md'].relative_to(root)} "
                f"but overview.md doesn't link to it"
            )
    elif "CONTEXT.md" in overview_content:
        l3_details.append("overview.md links to CONTEXT.md but the file no longer exists")

    if l3["adrs"]:
        if "docs/adr/" not in overview_content:
            l3_details.append(
                f"{len(l3['adrs'])} ADRs exist in docs/adr/ "
                f"but overview.md doesn't link to them"
            )
    elif "docs/adr/" in overview_content:
        l3_details.append("overview.md links to docs/adr/ but no ADR files exist")

    # ------------------------------------------------------------------
    # Wiki self-integrity: overview <-> module wikis <-> registration
    # ------------------------------------------------------------------
    modules_from_code = detect_modules(files)
    module_names = set(modules_from_code.keys())
    integrity: list[dict] = []

    # 1. Module in code but its module wiki file is missing
    for m in sorted(module_names - set(module_wiki_map.keys())):
        integrity.append(make_signal(
            "WIKI-MODULE-WIKI-MISSING", m,
            f"module '{m}' has {len(modules_from_code[m])} source files "
            f"but {m}.md is missing",
        ))

    # 2. Overview module index vs actual module set
    overview_modules: set[str] = set()
    if overview_path.exists():
        overview_modules = set(parse_overview(overview_path).keys())
    for m in sorted(module_names - overview_modules):
        integrity.append(make_signal(
            "WIKI-OVERVIEW-MODULE-MISMATCH", m,
            f"module '{m}' exists in code but is missing from the overview.md module index",
        ))
    for m in sorted(overview_modules - module_names):
        integrity.append(make_signal(
            "WIKI-OVERVIEW-MODULE-MISMATCH", m,
            f"module '{m}' is listed in overview.md but has no source files",
        ))

    # 3. Registration table coverage per module
    for m in sorted(module_wiki_map.keys()):
        mw = module_wiki_map[m]
        code_paths = {f.path for f in modules_from_code.get(m, [])}
        registered = set(mw.entries.keys())
        for p in sorted(code_paths - registered):
            integrity.append(make_signal(
                "WIKI-UNREGISTERED-FILE", p,
                f"source file exists in module '{m}' but is not registered in {m}.md",
            ))
        for p in sorted(registered - code_paths):
            integrity.append(make_signal(
                "WIKI-ORPHAN-ENTRY", p,
                f"registered in {m}.md but not present in code (module '{m}')",
            ))

    # ------------------------------------------------------------------
    # Assemble signals + summary
    # ------------------------------------------------------------------
    signals: list[dict] = []
    for p in report.new_files:
        signals.append(make_signal("WIKI-NEW-FILE", p, "in code, not yet in wiki"))
    for p in report.deleted_files:
        signals.append(make_signal("WIKI-DELETED-FILE", p, "in baseline, gone from code"))
    for p in report.modified_files:
        signals.append(make_signal("WIKI-MODIFIED-FILE", p, "SHA changed since last review"))
    for d in l3_details:
        signals.append(make_signal("WIKI-L3-DRIFT", "", d))
    signals.extend(integrity)
    signals = sort_signals(signals)

    l3_stale = bool(l3_details)
    integrity_stale = bool(integrity)
    any_stale = report.has_stale or l3_stale or integrity_stale

    summary = {
        "tracked": report.total_tracked,
        "in_wiki": report.total_in_wiki,
        "current": len(files),
        "new": len(report.new_files),
        "deleted": len(report.deleted_files),
        "modified": len(report.modified_files),
        "l3_drift": len(l3_details),
        "integrity": len(integrity),
    }

    if _JSON_MODE:
        emit_json({
            "command": "check",
            "ok": not any_stale,
            "summary": summary,
            "signals": signals,
        })
        if args.fail_on_stale and any_stale:
            return 1
        return 0

    # ----- human output -----
    say("=" * 70)
    say("PROJECT WIKI DRIFT REPORT")
    say("=" * 70)
    say(f"  Tracked files (baseline): {report.total_tracked}")
    say(f"  Registered in wiki:       {report.total_in_wiki}")
    say(f"  Current source files:     {len(files)}")
    say()

    if report.new_files:
        say(f"🟡 NEW FILES ({len(report.new_files)}) — in code, not yet in wiki:")
        for p in report.new_files:
            say(f"    + {p}")
        say()

    if report.deleted_files:
        say(f"🔴 DELETED FILES ({len(report.deleted_files)}) — in wiki/baseline, gone from code:")
        for p in report.deleted_files:
            say(f"    - {p}")
        say()

    if report.modified_files:
        say(f"🟠 MODIFIED FILES ({len(report.modified_files)}) — SHA changed since last review:")
        for p in report.modified_files:
            say(f"    ~ {p}")
        say()

    if l3_details:
        say(f"🔵 L3 DOMAIN-LANGUAGE DRIFT ({len(l3_details)}):")
        for d in l3_details:
            say(f"    {d}")
        say()

    if integrity:
        say(f"🟣 WIKI INTEGRITY ({len(integrity)}):")
        for s in integrity:
            say(f"    ! [{s['code']}] {s['detail']}")
        say()

    if not any_stale:
        say("✅ Wiki is up to date — no drift detected.")
        return 0

    say("-" * 70)
    total_stale = report.stale_count + len(l3_details) + len(integrity)
    say(f"TOTAL STALE: {total_stale} "
        f"({len(report.new_files)} new, "
        f"{len(report.deleted_files)} deleted, "
        f"{len(report.modified_files)} modified, "
        f"{len(l3_details)} L3 drift, "
        f"{len(integrity)} integrity)")
    say()
    say("Actions:")
    if report.new_files:
        say("  • Add new files to the appropriate <module>.md file registration table")
    if report.deleted_files:
        say("  • Remove deleted file entries from <module>.md tables")
    if report.modified_files:
        say("  • Review modified files and update descriptions if responsibilities changed")
    if l3_stale:
        say("  • Run 'python3 scripts/wiki.py update' to re-link L3 domain-language artifacts")
    if any(s["code"] == "WIKI-MODULE-WIKI-MISSING" for s in integrity):
        say("  • Run 'python3 scripts/wiki.py update' to generate missing module wiki skeletons")
    if any(s["code"] in ("WIKI-UNREGISTERED-FILE", "WIKI-ORPHAN-ENTRY") for s in integrity):
        say("  • Sync <module>.md registration tables with the actual file set")
    if any_stale:
        say("  • Run 'python3 scripts/wiki.py update' after making changes")
    say("-" * 70)

    if args.fail_on_stale and any_stale:
        return 1
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """Update the SHA baseline cache after wiki has been reviewed."""
    root = Path(args.root).resolve()
    wiki_dir = root / WIKI_DIR_NAME

    if not wiki_dir.exists():
        print(f"Error: no docs/project_wiki/ found at {root}", file=sys.stderr)
        return 2

    # Determine extensions
    cache = load_cache(wiki_dir)
    cached_files: dict = cache.get("files", {})
    if cached_files:
        exts = set()
        for path in cached_files:
            ext = os.path.splitext(path)[1].lower()
            if ext:
                exts.add(ext)
        extensions = list(exts)
    else:
        lang = detect_language(root)
        extensions = get_extensions_for_lang(lang)

    # Re-scan
    files = scan_project(root, extensions)

    # Create module wiki skeletons for modules that lack one
    # (repair path for WIKI-MODULE-WIKI-MISSING)
    modules = detect_modules(files)
    module_wikis_created: list[str] = []
    for module_name, mod_files in sorted(modules.items()):
        module_path = wiki_dir / f"{module_name}.md"
        if not module_path.exists():
            module_path.write_text(generate_module_content(module_name, mod_files))
            module_wikis_created.append(f"{module_name}.md")
            say(f"Created: {module_path.relative_to(root)} (skeleton — fill in descriptions)")

    # Build new cache
    new_cache: dict = {"files": {}, "last_updated": None}
    for f in files:
        new_cache["files"][f.path] = {
            "sha": f.sha,
            "module": f.module,
            "reviewed": True,
        }

    # Report what changed
    old_paths = set(cached_files.keys())
    new_paths = set(new_cache["files"].keys())

    added = new_paths - old_paths
    removed = old_paths - new_paths
    sha_changed = []
    for p in new_paths & old_paths:
        old_sha = cached_files[p].get("sha", "")
        new_sha = new_cache["files"][p]["sha"]
        if old_sha != new_sha:
            sha_changed.append(p)

    save_cache(wiki_dir, new_cache)

    say(f"✅ SHA baseline updated at {wiki_dir / CACHE_FILE_NAME}")
    say(f"   Total files tracked: {len(new_cache['files'])}")
    if added:
        say(f"   Added: {len(added)}")
    if removed:
        say(f"   Removed: {len(removed)}")
    if sha_changed:
        say(f"   SHA updated: {len(sha_changed)}")

    # Also update overview.md statistics
    overview_updated = False
    overview_path = wiki_dir / "overview.md"
    if overview_path.exists():
        content = generate_overview_content(modules, root)
        # Preserve existing module descriptions if possible
        old_overview = parse_overview(overview_path)
        for module_name, info in old_overview.items():
            if "<one-line responsibility>" in info["desc"]:
                continue
            # Strip the "_N source files_ — " prefix to get just the description
            desc = info["desc"]
            prefix_match = re.match(r"^_\d+ source files_ — (.+)$", desc)
            if prefix_match:
                desc = prefix_match.group(1)
            # Target this module's row specifically using its name as anchor
            file_count = len(modules.get(module_name, []))
            old_row = f"| `{module_name}` | _{file_count} source files_ — <one-line responsibility> |"
            new_row = f"| `{module_name}` | _{file_count} source files_ — {desc} |"
            content = content.replace(old_row, new_row)
        overview_path.write_text(content)
        overview_updated = True
        say(f"   Updated: {overview_path.relative_to(root)}")

    if _JSON_MODE:
        emit_json({
            "command": "update",
            "ok": True,
            "summary": {
                "tracked": len(new_cache["files"]),
                "added": len(added),
                "removed": len(removed),
                "sha_updated": len(sha_changed),
                "module_wikis_created": module_wikis_created,
                "overview_updated": overview_updated,
            },
            "signals": [],
        })

    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Show wiki status summary."""
    root = Path(args.root).resolve()
    wiki_dir = root / WIKI_DIR_NAME

    if not wiki_dir.exists():
        print(f"❌ No docs/project_wiki/ found at {root}")
        print("   Run 'python3 scripts/wiki.py init' to create one.")
        return 2

    cache = load_cache(wiki_dir)
    cached_files: dict = cache.get("files", {})
    last_updated = cache.get("last_updated", "never")

    # Count wiki files
    wiki_files = list(wiki_dir.glob("*.md"))
    module_wikis = [f for f in wiki_files if f.name != "overview.md"]

    # Parse all module wikis
    total_entries = 0
    filled_entries = 0
    for wf in module_wikis:
        mw = parse_module_wiki(wf)
        if mw:
            total_entries += len(mw.entries)
            filled_entries += sum(1 for e in mw.entries.values()
                                  if not e.description.startswith("<"))

    # Check for unreviewed files
    unreviewed = sum(1 for v in cached_files.values() if not v.get("reviewed", False))

    # L3: domain-modeling connectivity
    l3 = detect_l3_artifacts(root)
    l3_count = sum(1 for v in l3.values() if v)  # count non-empty L3 sources
    needs_attention = bool(unreviewed or filled_entries < total_entries)

    if _JSON_MODE:
        emit_json({
            "command": "status",
            "ok": True,
            "summary": {
                "module_wikis": len(module_wikis),
                "tracked": len(cached_files),
                "entries": total_entries,
                "described_entries": filled_entries,
                "unreviewed": unreviewed,
                "last_updated": last_updated,
                "l3_linked": l3_count > 0,
                "needs_attention": needs_attention,
            },
            "signals": [],
        })
        return 0

    say("=" * 50)
    say("PROJECT WIKI STATUS")
    say("=" * 50)
    say(f"  Wiki directory:     {wiki_dir.relative_to(root)}/")
    say(f"  Module wikis:       {len(module_wikis)}")
    say(f"  Tracked files:      {len(cached_files)}")
    say(f"  Wiki entries:       {total_entries}")
    pct = 100 * filled_entries // total_entries if total_entries else 0
    say(f"  Described entries:  {filled_entries}/{total_entries} ({pct}%)")
    say(f"  Unreviewed files:   {unreviewed}")
    say(f"  Last updated:       {last_updated}")
    say(f"  L3 domain language: {'✅ linked' if l3_count else '❌ not found'}")
    if l3["context_md"]:
        say(f"    CONTEXT.md:         {l3['context_md'].relative_to(root)}")
    if l3["adrs"]:
        say(f"    ADRs:               {len(l3['adrs'])} in {l3['adrs'][0].parent.relative_to(root)}")
    if l3["glossary"]:
        say(f"    Hand-curated:       {l3['glossary'].relative_to(root)}")
    say()

    if needs_attention:
        say("⚠️  Wiki needs attention:")
        if filled_entries < total_entries:
            say(f"   • {total_entries - filled_entries} entries still have placeholder descriptions")
        if unreviewed:
            say(f"   • {unreviewed} files not yet marked as reviewed")
        say("   Run 'python3 scripts/wiki.py check' for details.")
    else:
        say("✅ Wiki looks complete and up to date.")

    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="wiki.py",
        description="Maintain a three-level project knowledge base (docs/project_wiki/).",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    p_init = subparsers.add_parser("init", help="Initialize or regenerate the project wiki.")
    p_init.add_argument("--root", default=".", help="Project root directory (default: .)")
    p_init.add_argument("--lang", default="auto",
                        help=f"Language to scan (default: auto). Options: {', '.join(LANG_EXTENSIONS.keys())}, web (JS+TS+Vue)")
    p_init.add_argument("--extensions", default=None,
                        help="Comma-separated file extensions to scan (overrides --lang). E.g. .go,.py")

    # check
    p_check = subparsers.add_parser("check", help="Check for drift between code and wiki.")
    p_check.add_argument("--root", default=".", help="Project root directory (default: .)")
    p_check.add_argument("--fail-on-stale", action="store_true",
                         help="Exit with code 1 if any drift is detected (for CI/hooks).")

    # update
    p_update = subparsers.add_parser("update", help="Update SHA baseline cache after reviewing wiki.")
    p_update.add_argument("--root", default=".", help="Project root directory (default: .)")

    # status
    p_status = subparsers.add_parser("status", help="Show wiki coverage summary.")
    p_status.add_argument("--root", default=".", help="Project root directory (default: .)")

    # --json applies to every subcommand: emit one machine-readable JSON
    # object on stdout instead of human output.
    for p in (p_init, p_check, p_update, p_status):
        p.add_argument("--json", action="store_true",
                       help="Emit a machine-readable JSON object on stdout instead of human output.")

    args = parser.parse_args()

    global _JSON_MODE
    if getattr(args, "json", False):
        _JSON_MODE = True

    if args.command == "init":
        return cmd_init(args)
    elif args.command == "check":
        return cmd_check(args)
    elif args.command == "update":
        return cmd_update(args)
    elif args.command == "status":
        return cmd_status(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
