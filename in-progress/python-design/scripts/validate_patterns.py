#!/usr/bin/env python3
"""Validate pattern reference .md files against the required format.

Each pattern entry must have these sections in order:
  ### Pattern Name
  `PID` · N occurrences · M projects: ...
  **What**: ...
  **Recognize**: ... (2-4 bullet points)
  **Why**: ... (must mention cost/trade-off)
  **When**: ...
  **When not**: ...
  **Without this pattern** (anti-pattern):
  ```python  (❌ code block)
  **With this pattern**:
  ```python  (✅ code block)

Usage:
  python3 validate_patterns.py references/*.md
  python3 validate_patterns.py references/data.md --verbose
  python3 validate_patterns.py --check-all   # checks all 4 reference files

Exit code: 0 if all valid, 1 if any violations found.
"""

import argparse
import re
import sys
from pathlib import Path

# ── Format rules ──────────────────────────────────────────────────────────

REQUIRED_SECTIONS = [
    # (section_key,  search_pattern,  error_hint)
    ("What",       r"\*\*What\*\*:",            "Missing **What**: one-sentence description"),
    ("Recognize",  r"\*\*Recognize\*\*:",       "Missing **Recognize**: code-level signals"),
    ("Why",        r"\*\*Why\*\*:",             "Missing **Why**: rationale + trade-off"),
    ("When",       r"\*\*When\*\*:",            "Missing **When**: when to use"),
    ("When not",   r"\*\*When not\*\*:",        "Missing **When not**: when NOT to use"),
    ("Without",    r"\*\*Without this pattern\*\*", "Missing **Without this pattern** (anti-pattern)"),
    ("With",       r"\*\*With this pattern\*\*:",    "Missing **With this pattern**"),
]

META_PATTERN = re.compile(
    r"`(P\d+)`\s*·\s*(\d+)\s+occurrences?\s*·\s*(\d+)\s+projects?"
)

CODE_BLOCK = re.compile(r"```python")
BAD_MARKER = "❌"
GOOD_MARKER = "✅"

# ── Parser ────────────────────────────────────────────────────────────────

def split_patterns(content: str) -> list[tuple[str, str]]:
    """Split markdown into (title, body) pairs for each ### pattern."""
    # Match ### headers (but not #### or deeper)
    parts = re.split(r"(?m)^(### .+)$", content)
    patterns = []
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        # Skip dimension headers like "## Dimension Name (N patterns)"
        if title.startswith("### ") and not title.startswith("#### "):
            patterns.append((title, body))
    return patterns


def validate_pattern(title: str, body: str, verbose: bool = False) -> list[str]:
    """Validate a single pattern entry. Returns list of error messages."""
    errors = []

    # 1. Title format: ### Words  (allow Python identifiers like @decorator, __dunder__, _private)
    title_text = title.replace("### ", "")
    if not re.match(r"^([A-Z@_]|opt\(|suppress\()", title):
        # Allow titles starting with Python identifiers but require capitalization for word titles
        if not re.match(r"^[a-z]", title) or re.match(r"^(__|_internal|@|opt\(|suppress\()", title_text):
            pass  # Python identifier start is fine
        else:
            errors.append(f"Title should start with capital letter: '{title}'")

    # 2. Metadata line: `P021` · N occurrences · M projects: ...
    if not META_PATTERN.search(body):
        errors.append("Missing or malformed metadata line (expected: `P021` · 33 occurrences · 20 projects: ...)")

    # 3. Required sections in order
    last_pos = 0
    for section_name, pattern, hint in REQUIRED_SECTIONS:
        m = re.search(pattern, body)
        if not m:
            errors.append(hint)
        elif m.start() < last_pos:
            errors.append(f"Section **{section_name}** is out of order (should come after previous section)")
        else:
            last_pos = m.start()

    # 4. Recognize: must have bullet points (allow prose intro before bullets)
    recognize_section = re.search(r"\*\*Recognize\*\*:?\s*(.*?)(?=\n\*\*|\Z)", body, re.DOTALL)
    if recognize_section:
        recognize_text = recognize_section.group(1)
        bullets = [line.strip() for line in recognize_text.split("\n") if line.strip().startswith(("-", "*"))]
        if len(bullets) < 2:
            errors.append(f"**Recognize** should have 2-4 bullet points, found {len(bullets)}")
        elif len(bullets) > 4:
            errors.append(f"**Recognize** should have max 4 bullet points, found {len(bullets)}")
    else:
        # Check if Recognize exists but without bullets
        if "**Recognize**" in body:
            errors.append("**Recognize** must use bullet points (- ...), not prose")

    # 5. Why: must mention cost or trade-off
    why_match = re.search(r"\*\*Why\*\*:\s*(.+?)(?=\n\*\*|\Z)", body, re.DOTALL)
    if why_match:
        why_text = why_match.group(1).lower()
        cost_words = ["cost", "trade-off", "downside", "drawback", "price", "penalty",
                      "overhead", "expense", "sacrifice", "cost:", "but", "however",
                      "the cost", "at the cost"]
        if not any(w in why_text for w in cost_words):
            errors.append("**Why** must mention a cost/trade-off (e.g. 'Cost: ...', 'Trade-off: ...', 'but ...')")

    # 6. Code blocks: must have at least 2 python blocks (❌ and ✅)
    code_blocks = CODE_BLOCK.findall(body)
    if len(code_blocks) < 2:
        errors.append(f"Expected 2 python code blocks (❌ and ✅), found {len(code_blocks)}")

    # 7. ❌ and ✅ markers
    if BAD_MARKER not in body:
        errors.append("Missing ❌ marker in the 'Without this pattern' code block")
    if GOOD_MARKER not in body:
        errors.append("Missing ✅ marker in the 'With this pattern' code block")

    # 8. ✅ With: must have project — file:lines comment
    with_section = body.split("**With this pattern**")[-1] if "**With this pattern**" in body else ""
    if with_section:
        # Look for # project — file:lines pattern
        ref_pattern = re.compile(r"#\s*\w[\w-]*\s+—\s+[\w/.]+:\d+")
        if not ref_pattern.search(with_section):
            # Also accept # project — path:lines
            ref_pattern2 = re.compile(r"#\s*\w[\w-]*\s+[-—]\s+[\w/.]+", )
            if not ref_pattern2.search(with_section):
                errors.append("**With this pattern** code must have a '# project — file:lines' source reference comment")

    if verbose and not errors:
        print(f"  ✅ {title}")

    return errors


def validate_file(filepath: Path, verbose: bool = False) -> tuple[int, list[str]]:
    """Validate a single .md file. Returns (pattern_count, errors)."""
    content = filepath.read_text(encoding="utf-8")
    patterns = split_patterns(content)

    if not patterns:
        return 0, [f"{filepath.name}: No pattern entries (### headers) found"]

    all_errors = []
    for title, body in patterns:
        errs = validate_pattern(title, body, verbose)
        for e in errs:
            all_errors.append(f"{filepath.name} → {title}: {e}")

    return len(patterns), all_errors


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Validate pattern reference .md files")
    ap.add_argument("files", nargs="*", help="Pattern .md files to validate")
    ap.add_argument("--check-all", action="store_true",
                    help="Check all 4 standard reference files")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="Print each pattern as it validates")
    args = ap.parse_args()

    if args.check_all:
        ref_dir = Path(__file__).parent.parent / "references"
        args.files = [ref_dir / f for f in ["data.md", "flow.md", "structure.md", "extension.md"]]
    elif not args.files:
        ap.error("Provide files or --check-all")

    total_patterns = 0
    total_errors = 0
    total_warnings = 0

    for filepath_str in args.files:
        filepath = Path(filepath_str)
        if not filepath.exists():
            print(f"❌ {filepath}: file not found")
            total_errors += 1
            continue

        count, errors = validate_file(filepath, args.verbose)
        total_patterns += count

        if errors:
            print(f"\n{'='*60}")
            print(f"❌ {filepath.name}: {count} patterns, {len(errors)} violations")
            print(f"{'='*60}")
            for e in errors:
                print(f"  ⚠️  {e}")
            total_errors += len(errors)
        else:
            print(f"✅ {filepath.name}: {count} patterns, all valid")

    print(f"\n{'='*60}")
    print(f"Summary: {total_patterns} patterns, {total_errors} violations")
    print(f"{'='*60}")

    sys.exit(1 if total_errors else 0)


if __name__ == "__main__":
    main()
