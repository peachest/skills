#!/usr/bin/env python3
"""version-anchor.py — resolve WHICH version of a skill a session actually ran.

The skill-injection message carries the full SKILL.md body that was in
effect at call time. Hash that body and resolve the hash against the source
repo's git history:

  hit    → skill@<commit> (<date>)   — the bytes that ran are a committed version
  miss   → uncommitted               — the session ran a working-tree state that
                                       was never committed (a diagnosis signal in
                                       itself: findings cite a version that no
                                       longer exists anywhere but this log)
  third-party → no git history       — installed via `npx skills`, old bodies
                                       survive ONLY in session logs; snapshot the
                                       body when archiving (eval case rule)

Read-loads (manual `read` of SKILL.md) anchor the same way via the
toolResult content of the read call.

Usage:
  python3 version-anchor.py <session-file.jsonl> [--skill <name>]
  # name defaults to the first skill injection found in the file

Output: JSON array — one entry per DISTINCT version body:
  {skill, sha256, first_seen, last_seen, injections, read_loads,
   resolution: {type, commit?, date?, matches_current_file?}}
Exit 0 always on a parseable file (empty array = no anchorable signal).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SOURCE_ROOTS = [Path.home() / "skills", Path.home() / "internal-skills"]
THIRD_PARTY_ROOT = Path.home() / ".agents" / "skills"
GLOB_PATTERNS = ["in-progress/{n}/SKILL.md", "*/{n}/SKILL.md", "{n}/SKILL.md"]
MAX_COMMITS = 100  # ponytail: linear scan of recent history; raise if a skill has deeper history


def canonical(text: str) -> str:
    """Normalize the three forms of a SKILL.md body to one canonical shape:
    - injection body: pi strips the frontmatter and prepends a
      "References are relative to <dir>." line — drop that line
    - git blob / read-load toolResult: raw file — strip the leading
      YAML frontmatter block
    All three then converge on "file content minus frontmatter".
    """
    t = text.strip()
    if t.startswith("References are relative to"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
    if t.startswith("---"):
        t = re.sub(r"\A---\n.*?\n---\n", "", t, flags=re.DOTALL)
    return t.strip()


def sha(text: str) -> str:
    return hashlib.sha256(canonical(text).encode()).hexdigest()


def iter_entries(path: Path):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(entry, dict):
                yield entry


def entry_ts(entry: dict) -> str | None:
    ts = entry.get("timestamp") or (entry.get("message") or {}).get("timestamp")
    return str(ts) if ts else None


def collect_bodies(path: Path, skill: str) -> dict[str, dict]:
    """One record per distinct body-hash: counts + first/last seen."""
    bodies: dict[str, dict] = {}
    marker_re = re.compile(r'<skill name=\\?"' + re.escape(skill) + r'\\?"[^>]*>')
    pending_reads: dict[str, str] = {}  # toolCallId -> "1" (mark read-loads awaiting result)

    def record(body: str, kind: str, ts: str | None) -> None:
        h = sha(body)
        rec = bodies.setdefault(h, {"injections": 0, "read_loads": 0, "first": ts, "last": ts})
        rec[kind] += 1
        if ts:
            if rec["first"] is None or ts < rec["first"]:
                rec["first"] = ts
            if rec["last"] is None or ts > rec["last"]:
                rec["last"] = ts

    for entry in iter_entries(path):
        msg = entry.get("message") or {}
        ts = entry_ts(entry)
        content = msg.get("content")
        # 1) injection marker in user text
        if msg.get("role") == "user" and isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    text = part.get("text", "")
                    m = marker_re.search(text)
                    if m:
                        body = text[m.end():].split("</skill>")[0]
                        record(body, "injections", ts)
        # 2) read toolCall of SKILL.md → pair with its toolResult
        if isinstance(content, list):
            for part in content:
                if not (isinstance(part, dict) and part.get("type") == "toolCall"):
                    continue
                args = part.get("arguments") or {}
                p = str(args.get("path", ""))
                if part.get("name") == "read" and p.endswith(f"/{skill}/SKILL.md"):
                    pending_reads[part.get("id", "")] = p
        if entry.get("type") == "toolResult":
            tcid = str(entry.get("toolCallId", ""))
            if tcid in pending_reads:
                text = "".join(
                    p.get("text", "") for p in (entry.get("content") or [])
                    if isinstance(p, dict) and p.get("type") == "text"
                )
                if text and "truncated" not in text[:200]:
                    record(text, "read_loads", ts)
                pending_reads.pop(tcid, None)
    return bodies


def first_skill_name(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'<skill name=\\?"([A-Za-z0-9_-]+)\\?"', text)
    if m:
        return m.group(1)
    m = re.search(r'"path":\s*"[^"]*?/([A-Za-z0-9_-]+)/SKILL\.md"', text)
    return m.group(1) if m else None


def locate_sources(skill: str) -> list[Path]:
    """All existing SKILL.md candidates, source roots first (git history), then third-party."""
    found = []
    for root in SOURCE_ROOTS + [THIRD_PARTY_ROOT]:
        for pat in GLOB_PATTERNS:
            cand = root / pat.format(n=skill)
            if cand.is_file():
                found.append(cand)
    return found


def resolve(h: str, sources: list[Path]) -> dict:
    for src in sources:
        repo = _git_repo(src)
        if repo:
            rel = src.resolve().relative_to(repo)
            log = subprocess.run(
                ["git", "-C", str(repo), "log", "--all", "--format=%H %cI", "--", str(rel)],
                capture_output=True, text=True, check=False,
            ).stdout.strip()
            for line in log.splitlines()[:MAX_COMMITS]:
                commit, date = line.split(" ", 1)
                blob = subprocess.run(
                    ["git", "-C", str(repo), "show", f"{commit}:{rel}"],
                    capture_output=True, text=True, check=False,
                ).stdout
                if blob and sha(blob) == h:
                    return {"type": "commit", "commit": commit, "date": date}
        # no git (or no hit): does the current file on disk match?
        if sha(src.read_text(encoding="utf-8", errors="replace")) == h:
            return {
                "type": "third-party" if THIRD_PARTY_ROOT in src.parents else "uncommitted",
                "matches_current_file": True,
            }
    return {
        "type": "third-party" if any(THIRD_PARTY_ROOT in s.parents for s in sources) else "uncommitted",
        "matches_current_file": False,
    }


def _git_repo(path: Path) -> Path | None:
    d = path.resolve().parent
    while d != d.parent:
        if (d / ".git").exists():
            return d
        d = d.parent
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("session_file", type=Path)
    ap.add_argument("--skill")
    args = ap.parse_args()

    if not args.session_file.is_file():
        print(f"error: no such file: {args.session_file}", file=sys.stderr)
        sys.exit(2)

    skill = args.skill or first_skill_name(args.session_file)
    if not skill:
        print("[]")
        return

    sources = locate_sources(skill)
    out = []
    for h, rec in collect_bodies(args.session_file, skill).items():
        out.append({
            "skill": skill,
            "sha256": h,
            "first_seen": rec["first"],
            "last_seen": rec["last"],
            "injections": rec["injections"],
            "read_loads": rec["read_loads"],
            "resolution": resolve(h, sources),
        })
    out.sort(key=lambda r: r["first_seen"] or "")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
