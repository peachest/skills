"""Shared helpers for okb scripts — minimal frontmatter parsing/writing."""
import hashlib
import re
from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def slugify(title: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s[:60].strip("-") or "untitled"


def read_frontmatter(path: str) -> dict:
    """Parse our constrained YAML frontmatter into a dict. Values are strings;
    list-like scalars ('[a, b]') are returned raw."""
    fm = {}
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return fm
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 3)
    if end < 0:
        return fm
    for line in text[3:end].splitlines():
        m = re.match(r"^([a-zA-Z_][\w-]*):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def body_links(path: str) -> list:
    """Markdown hyperlinks between notes: ./x.md or ../<topic>/x.md."""
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return []
    # body only (strip frontmatter)
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            text = text[end + 4:]
    out = []
    for m in re.finditer(r"\]\((\.{1,2}/[^)#]+?\.md)\)", text):
        out.append(m.group(1))
    return out
