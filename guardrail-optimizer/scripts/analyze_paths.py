#!/usr/bin/env python3
"""
Guardrail Optimizer — Path Analysis & Recommendation Script

Takes the JSON output from scan_paths.ts and produces consolidated,
filtered, safety-checked allowlist recommendations.

Usage:
  python3 analyze_paths.py /tmp/guardrail_scan.json
  python3 analyze_paths.py /tmp/guardrail_scan.json --cap 15
  python3 analyze_paths.py /tmp/guardrail_scan.json --check-sensitive

Output: JSON with recommended_entries[], skipped_paths[], summary{}
"""

import json
import os
import re
import sys
import argparse
from collections import defaultdict
from pathlib import Path


# ─── Noise filtering ───────────────────────────────────────────────────────────

# Paths that are never meaningful allowlist targets
NOISE_PREFIXES = [
    "/dev/null",
    "/proc",
    "/sys",
    "/dev",
    "/root",
    "/var",
    "/opt",
    "/build",
    "/pub",
    "/run",
]

# Pi slash commands that look like paths (start with /)
SLASH_CMD_PATTERN = re.compile(
    r"^/(help|skill|reload|debug|preset|session|goal|clear|compact|model|agent|resume|steer|stop|interrupt|schedule|memory|knowledge|todo|ask|heading|config|install|package|extension|guardrails)"
)

# Glob characters in path
GLOB_PATTERN = re.compile(r"[*?\[\]]")


def is_noise(path: str) -> bool:
    """Check if a path is noise (not a real filesystem access target)."""
    if path in ("/dev/null", "/"):
        return True
    # HTML/XML tags misidentified as paths (e.g., /<style>/, /<div ...>/)
    if path.startswith("/<"):
        return True
    # Markdown headers / sed patterns misidentified as paths (e.g., /## Header/, /pattern/replacement/)
    if path.startswith("/#") or path.startswith("/s/") or path.startswith("/g/"):
        return True
    for prefix in NOISE_PREFIXES:
        if path == prefix or path.startswith(prefix + "/"):
            return True
    if SLASH_CMD_PATTERN.match(path):
        return True
    if GLOB_PATTERN.search(path):
        return True
    # /tmp paths are usually ephemeral (already allowed globally in most setups)
    if path == "/tmp" or path.startswith("/tmp/"):
        return True
    return False


# ─── Broadness checking ────────────────────────────────────────────────────────

def is_too_broad(path: str, home: str) -> bool:
    """Check if a path is too broad for an allowlist entry.

    isGrantTooBroad checks / and ~ only. We also reject:
    - The user's workspace root (parent of multiple projects)
    - Any path that is a direct parent of /projects or equivalent
    - System directories (/usr, /etc, etc.)
    """
    normalized = path.rstrip("/")
    if normalized == "/" or normalized == home:
        return True
    # Reject system directories
    if normalized in ("/usr", "/usr/local", "/etc", "/lib", "/lib64", "/bin", "/sbin"):
        return True
    # Reject workspace-level directories: shallow paths ending in /projects,
    # /research, /work, /src — these are parents of multiple distinct projects.
    # Only check shallow paths (depth ≤ 4) to avoid false positives on deep
    # paths that happen to end in one of these words (e.g., .../skills/research).
    parts = normalized.split("/")
    if len(parts) <= 5 and parts[-1] in ("projects", "research", "work", "src", "workspace", "repos"):
        return True
    # Reject shallow /mnt/ paths (workspace roots like /mnt/disk1/hyx, /mnt/disk1)
    if normalized.startswith("/mnt/") and len(parts) <= 4:
        return True
    return False


# ─── Version-specific path handling ────────────────────────────────────────────

VERSION_PATTERN = re.compile(
    r"/(v?\d+\.\d+\.\d+|"           # v24.15.0 or 24.15.0
    r"go\d+\.\d+(\.\d+)?|"          # go1.26.5 or go1.26
    r"\d+\.\d+\.\d+[-\w]*|"         # 0.2.4, 0.2.4-beta
    r"v\d+)"                        # v1, v2
    r"(?:/|$)"
)


def strip_version_segment(path: str) -> str:
    """If a path contains a version segment, return the parent directory.

    e.g., /home/user/.nvm/versions/node/v24.15.0/lib/... → /home/user/.nvm/versions/node
          /home/user/sdk/go1.26.5/bin      → /home/user/sdk
          /home/user/.vscode-server/extensions/ext-0.2.4 → /home/user/.vscode-server/extensions
    """
    match = VERSION_PATTERN.search(path)
    if match:
        version_start = match.start()
        return path[:version_start].rstrip("/")
    return path


def is_version_specific(path: str) -> bool:
    """Check if a path contains a version number."""
    return bool(VERSION_PATTERN.search(path))


# ─── Consolidation ─────────────────────────────────────────────────────────────

def consolidate_paths(outside_paths: list, home: str) -> list:
    """Group paths by parent directory and consolidate into directory recommendations.

    Returns a list of consolidated entries with merged frequency, tools, sessions.
    """
    # First: strip version segments and normalize
    normalized = []
    for entry in outside_paths:
        path = entry["path"]
        if is_noise(path):
            continue

        # Strip version segment if present
        if is_version_specific(path):
            path = strip_version_segment(path)

        normalized.append({
            "original_path": entry["path"],
            "normalized_path": path,
            "frequency": entry["frequency"],
            "tools": entry["tools"],
            "blocked_count": entry["blocked_count"],
            "sessions": entry["sessions"],
        })

    # Group by parent directory
    # For each normalized path, the candidate directory is:
    # - The path itself if it's a directory (no file extension, no trailing file)
    # - The parent directory otherwise
    groups: dict[str, dict] = defaultdict(lambda: {
        "frequency": 0,
        "tools": set(),
        "blocked_count": 0,
        "sessions": {},  # id → context
        "file_count": 0,
        "original_paths": [],
    })

    for entry in normalized:
        path = entry["normalized_path"]

        # Determine the directory to group under
        # Heuristic: if the path has a file extension or is clearly a file,
        # group under its parent directory. Otherwise, the path IS the directory.
        path_obj = Path(path)
        has_extension = bool(path_obj.suffix)
        looks_like_file = has_extension or path.endswith((".json", ".md", ".py", ".ts", ".js", ".go", ".txt", ".yaml", ".yml", ".toml", ".sh"))

        if looks_like_file:
            group_dir = str(path_obj.parent)
        else:
            group_dir = path

        g = groups[group_dir]
        g["frequency"] += entry["frequency"]
        g["tools"].update(entry["tools"])
        g["blocked_count"] += entry["blocked_count"]
        for s in entry["sessions"]:
            g["sessions"][s["id"]] = s
        g["file_count"] += 1
        g["original_paths"].append(entry["original_path"])

    # Convert to list and sort by frequency
    result = []
    for dir_path, data in groups.items():
        result.append({
            "path": dir_path,
            "kind": "directory",
            "frequency": data["frequency"],
            "tools": sorted(data["tools"]),
            "blocked_count": data["blocked_count"],
            "session_count": len(data["sessions"]),
            "sessions": list(data["sessions"].values()),
            "file_count": data["file_count"],
            "is_version_specific": is_version_specific(dir_path),
        })

    result.sort(key=lambda x: x["frequency"], reverse=True)
    return result


# ─── Sensitive file checking ───────────────────────────────────────────────────

SENSITIVE_FILE_NAMES = {
    "auth.json", "credentials.json", ".env", ".env.local", ".env.production",
    "id_rsa", "id_ed25519", "token", "tokens.json", ".npmrc", ".pypirc",
    "secrets.json", "secret.key", ".git-credentials", ".netrc",
}

SENSITIVE_FILE_PATTERNS = [
    re.compile(r".*token.*", re.IGNORECASE),
    re.compile(r".*secret.*", re.IGNORECASE),
    re.compile(r".*credential.*", re.IGNORECASE),
    re.compile(r".*password.*", re.IGNORECASE),
    re.compile(r".*\.pem$"),
    re.compile(r".*\.key$"),
]


def find_sensitive_files(directory: str) -> list:
    """Check if a directory contains sensitive files. Returns list of found files."""
    found = []
    if not os.path.isdir(directory):
        return found
    try:
        for entry in os.listdir(directory):
            entry_lower = entry.lower()
            if entry_lower in SENSITIVE_FILE_NAMES:
                found.append(entry)
                continue
            for pattern in SENSITIVE_FILE_PATTERNS:
                if pattern.match(entry):
                    found.append(entry)
                    break
    except PermissionError:
        pass
    return found


# ─── Existing allowed paths checking ───────────────────────────────────────────

def is_already_allowed(path: str, existing_paths: list, home: str) -> bool:
    """Check if a path is already covered by an existing allowed path entry."""
    abs_path = os.path.expanduser(path)
    for entry in existing_paths:
        if not isinstance(entry, dict):
            continue
        kind = entry.get("kind", "")
        entry_path = os.path.expanduser(entry.get("path", ""))

        if kind == "file":
            if abs_path == entry_path:
                return True
        elif kind == "directory":
            # Directory grants cover descendants
            if abs_path == entry_path or abs_path.startswith(entry_path.rstrip("/") + "/"):
                return True
    return False


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Analyze guardrail scan output")
    parser.add_argument("input", help="Path to scan_paths.ts JSON output file")
    parser.add_argument("--cap", type=int, default=15, help="Max recommendations to show (default 15)")
    parser.add_argument("--home", default=os.path.expanduser("~"), help="Home directory")
    args = parser.parse_args()

    with open(args.input) as f:
        scan_data = json.load(f)

    home = args.home
    existing_allowed = scan_data.get("existing_allowed_paths", [])
    outside_paths = scan_data.get("outside_paths", [])

    # Phase 1: Consolidate
    consolidated = consolidate_paths(outside_paths, home)

    # Phase 2: Filter and classify
    recommended = []
    skipped = []

    for entry in consolidated:
        path = entry["path"]

        # Check broadness
        if is_too_broad(path, home):
            skipped.append({**entry, "skip_reason": "too_broad"})
            continue

        # Check already allowed
        if is_already_allowed(path, existing_allowed, home):
            skipped.append({**entry, "skip_reason": "already_allowed"})
            continue

        # Check sensitive files
        sensitive_files = find_sensitive_files(os.path.expanduser(path))

        entry["sensitive_files"] = sensitive_files
        entry["security_warning"] = bool(sensitive_files)
        recommended.append(entry)

    # Phase 3: Cap
    capped = recommended[:args.cap]
    remaining = recommended[args.cap:]

    # Build output
    result = {
        "summary": {
            "scope": scan_data.get("scope"),
            "cwd": scan_data.get("cwd"),
            "config_path": scan_data.get("config_path"),
            "sessions_scanned": scan_data.get("sessions_scanned"),
            "date_range": scan_data.get("date_range"),
            "total_outside_paths": len(outside_paths),
            "consolidated_entries": len(consolidated),
            "recommended_count": len(recommended),
            "shown_count": len(capped),
            "remaining_count": len(remaining),
            "skipped_count": len(skipped),
            "existing_allowed_count": len(existing_allowed),
        },
        "recommended_entries": capped,
        "remaining_entries": remaining,
        "skipped_entries": skipped,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
