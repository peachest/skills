#!/usr/bin/env python3
"""
Guardrail Optimizer — Command Pattern Analysis & Recommendation Script

Takes the JSON output from scan_commands.ts and produces consolidated,
filtered, safety-checked recommendations for permissionGate.allowedPatterns.

Usage:
  python3 analyze_commands.py /tmp/guardrail_cmd_scan.json
  python3 analyze_commands.py /tmp/guardrail_cmd_scan.json --cap 15

Output: JSON with recommended_entries[], skipped_entries[], summary{}
"""

import json
import re
import argparse
from collections import defaultdict


# ─── Matcher safety classification ─────────────────────────────────────────────

# Matchers that are inherently dangerous regardless of arguments.
# These should NEVER be recommended for allowlisting — the user should
# always be prompted.
INHERENTLY_DANGEROUS_MATCHERS = {
    "rm-rf",
    "shred",
    "dd",
    "mkfs",
    "wipefs",
    "blkdiscard",
    "fdisk",
    "parted",
    "chmod-R",
    "chown-R",
    "container-escape",
}

# Matchers that are dangerous only due to privilege escalation.
# The actual subcommand may be safe (e.g., sudo nerdctl ps is read-only).
# These are candidates for allowlisting with proper patterns.
PRIVILEGE_MATCHERS = {
    "sudo",
    "doas",
    "pkexec",
}


# ─── Command family extraction ─────────────────────────────────────────────────

def extract_command_family(segment: str, matcher: str) -> str:
    """Extract the command family key for grouping.

    Uses the matched_segment (the sub-command that triggered the dangerous
    match), NOT the full compound command string.

    For sudo/doas/pkexec: "sudo <subcommand>" (first 2 words after sudo)
    For others: first 2 words of the segment
    """
    words = segment.split()
    if not words:
        return segment

    if matcher in PRIVILEGE_MATCHERS:
        # sudo nerdctl ps -a → "sudo nerdctl"
        # sudo -E nerdctl ps → "sudo -E nerdctl" (keep flags)
        # Take sudo + next non-flag word + any flags before it
        prefix = [words[0]]
        for w in words[1:]:
            prefix.append(w)
            if not w.startswith("-"):
                break
        return " ".join(prefix)

    # Default: first 2 words
    return " ".join(words[:2])


# Flags that consume a value (so the next token is not a subcommand).
FLAGS_WITH_VALUE = {
    "-n", "--namespace", "-a", "--address", "-H", "--host",
    "--context", "--kubeconfig", "-u", "--user",
}


def extract_subcommands(segment: str, matcher: str) -> list[str]:
    """Extract distinct subcommand tokens for a command.

    Uses the matched_segment, not the full compound command.
    For sudo nerdctl ps/images/logs → ["ps", "images", "logs"]
    """
    words = segment.split()
    if matcher in PRIVILEGE_MATCHERS and len(words) > 2:
        # Skip sudo and the subcommand, collect the action word
        # sudo nerdctl ps → "ps"
        # sudo nerdctl -n test ps → "ps"
        # sudo kubectl get pods → "get"
        idx = 1  # skip "sudo"
        # Skip flags (and their values for value-taking flags)
        while idx < len(words) and words[idx].startswith("-"):
            if words[idx] in FLAGS_WITH_VALUE and idx + 1 < len(words):
                idx += 2  # skip flag + value
            elif "=" in words[idx]:
                idx += 1  # --namespace=test, skip just the flag
            else:
                idx += 1  # bare flag
        idx += 1  # skip the subcommand (nerdctl, kubectl, etc.)
        # Skip more flags (and their values)
        while idx < len(words) and words[idx].startswith("-"):
            if words[idx] in FLAGS_WITH_VALUE and idx + 1 < len(words):
                idx += 2
            elif "=" in words[idx]:
                idx += 1
            else:
                idx += 1
        if idx < len(words):
            return [words[idx]]
    return []


# ─── Pattern generation ────────────────────────────────────────────────────────

def generate_candidate_pattern(
    family: str,
    subcommands: set[str],
    matcher: str,
) -> tuple[str, bool, str | None]:
    """Generate a candidate allowedPattern for a command family.

    Returns (pattern, is_regex, warning).
    """
    words = family.split()

    # For privilege escalation commands (sudo/doas/pkexec)
    if matcher in PRIVILEGE_MATCHERS and len(words) >= 2:
        priv = words[0]  # sudo
        subcmd = words[1] if not words[1].startswith("-") else words[-1]

        if subcommands:
            # We know the subcommands — generate a constrained regex
            # Escape special regex chars in the subcommand names
            escaped_subs = sorted(subcommands)
            if len(escaped_subs) <= 10:
                sub_alt = "|".join(re.escape(s) for s in escaped_subs)
                pattern = rf"^{re.escape(priv)}\s+{re.escape(subcmd)}\b.*\b({sub_alt})(\s|$)"
                return pattern, True, None

        # Fallback: broad prefix match with warning
        pattern = f"{priv} {subcmd} "
        return pattern, False, (
            f"Broad substring pattern — matches ALL '{priv} {subcmd}' commands "
            f"including potentially dangerous ones. Agent should refine to a "
            f"constrained regex listing only safe subcommands."
        )

    # Default: substring pattern from family
    pattern = family + " "
    return pattern, False, (
        f"Substring pattern — review carefully before allowing. "
        f"Matches any command starting with '{family}'."
    )


# ─── Broadness checking ────────────────────────────────────────────────────────

def is_too_broad(family: str, matcher: str) -> bool:
    """Check if a command family is too broad for an allowlist entry."""
    words = family.split()

    if matcher in PRIVILEGE_MATCHERS:
        # "sudo" alone is too broad — would allow ALL sudo commands
        if len(words) < 2:
            return True
        # "sudo <cmd>" is the minimum acceptable granularity
        # But "sudo bash", "sudo sh", "sudo su" are still too broad
        subcmd = words[1] if not words[1].startswith("-") else ""
        if subcmd in ("bash", "sh", "su", "zsh", "fish", "python", "python3",
                       "node", "perl", "ruby", "php", "exec", "eval"):
            return True
        return False

    # For non-privilege matchers, require at least 2 words
    if len(words) < 2:
        return True
    return False


# ─── Existing pattern coverage check ───────────────────────────────────────────

def check_existing_coverage(
    family: str,
    subcommands: set[str],
    existing_patterns: list[dict],
) -> tuple[bool, list[str]]:
    """Check if a command family is already covered by existing allowedPatterns.

    Returns (fully_covered, partially_covered_subcommands).
    full coverage: every subcommand we found is matched by an existing pattern.
    partial coverage: some subcommands are matched — reported so the agent
    can avoid adding duplicate entries.
    """
    if not subcommands:
        # No subcommands to test — use a generic sample
        sample = family + " --help"
        for entry in existing_patterns:
            if not isinstance(entry, dict):
                continue
            pattern = entry.get("pattern", "")
            is_regex = entry.get("regex", False)
            try:
                if is_regex:
                    if re.search(pattern, sample):
                        return True, []
                else:
                    if pattern in sample:
                        return True, []
            except re.error:
                continue
        return False, []

    # Test each subcommand against existing patterns
    covered_subs: list[str] = []
    for sub in sorted(subcommands):
        sample = f"{family} {sub}"
        for entry in existing_patterns:
            if not isinstance(entry, dict):
                continue
            pattern = entry.get("pattern", "")
            is_regex = entry.get("regex", False)
            try:
                if is_regex:
                    if re.search(pattern, sample):
                        covered_subs.append(sub)
                        break
                else:
                    if pattern in sample:
                        covered_subs.append(sub)
                        break
            except re.error:
                continue

    fully_covered = len(covered_subs) == len(subcommands)
    partially_covered = covered_subs if covered_subs and not fully_covered else []
    return fully_covered, partially_covered


# ─── Consolidation ─────────────────────────────────────────────────────────────

def consolidate_commands(
    dangerous_commands: list[dict],
) -> dict[str, dict]:
    """Group dangerous commands by command family.

    Returns {family: {frequency, sessions, sample_commands, matcher, description, subcommands}}
    """
    groups: dict[str, dict] = defaultdict(lambda: {
        "frequency": 0,
        "sessions": {},  # id → context
        "sample_commands": [],
        "matcher": "",
        "description": "",
        "matched_segment": "",
        "subcommands": set(),
    })

    for entry in dangerous_commands:
        command = entry["command"]
        segment = entry.get("matched_segment", command)
        matcher = entry["matched_matcher"]
        description = entry["matched_description"]

        family = extract_command_family(segment, matcher)

        g = groups[family]
        g["frequency"] += entry["frequency"]
        g["matcher"] = matcher
        g["description"] = description
        g["matched_segment"] = segment
        for s in entry.get("sessions", []):
            g["sessions"][s["id"]] = s
        if len(g["sample_commands"]) < 10:
            g["sample_commands"].append(command)
        g["subcommands"].update(extract_subcommands(segment, matcher))

    return groups


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Analyze command scan output for guardrail optimization"
    )
    parser.add_argument("input", help="Path to scan_commands.ts JSON output file")
    parser.add_argument("--cap", type=int, default=15,
                        help="Max recommendations to show (default 15)")
    args = parser.parse_args()

    with open(args.input) as f:
        scan_data = json.load(f)

    existing_patterns = scan_data.get("existing_allowed_patterns", [])
    dangerous_commands = scan_data.get("dangerous_commands", [])

    # Phase 1: Consolidate
    groups = consolidate_commands(dangerous_commands)

    # Phase 2: Filter and classify
    recommended = []
    skipped = []

    for family, data in groups.items():
        matcher = data["matcher"]

        # Check if inherently dangerous
        if matcher in INHERENTLY_DANGEROUS_MATCHERS:
            skipped.append({
                "command_family": family,
                "reason": "inherently_dangerous",
                "matcher": matcher,
                "frequency": data["frequency"],
                "session_count": len(data["sessions"]),
                "sample_commands": data["sample_commands"][:3],
            })
            continue

        # Check if too broad
        if is_too_broad(family, matcher):
            skipped.append({
                "command_family": family,
                "reason": "too_broad",
                "matcher": matcher,
                "frequency": data["frequency"],
                "session_count": len(data["sessions"]),
                "sample_commands": data["sample_commands"][:3],
            })
            continue

        # Check if already covered by existing patterns
        fully_covered, partially_covered = check_existing_coverage(
            family, data["subcommands"], existing_patterns,
        )
        if fully_covered:
            skipped.append({
                "command_family": family,
                "reason": "already_allowed",
                "matcher": matcher,
                "frequency": data["frequency"],
                "session_count": len(data["sessions"]),
                "sample_commands": data["sample_commands"][:3],
            })
            continue

        # Generate candidate pattern
        pattern, is_regex, warning = generate_candidate_pattern(
            family,
            data["subcommands"],
            matcher,
        )

        recommended.append({
            "command_family": family,
            "candidate_pattern": pattern,
            "regex": is_regex,
            "description": data["description"],
            "matcher": matcher,
            "frequency": data["frequency"],
            "session_count": len(data["sessions"]),
            "sample_commands": data["sample_commands"][:5],
            "distinct_subcommands": sorted(data["subcommands"]) if data["subcommands"] else [],
            "partially_covered_subcommands": partially_covered,
            "security_warning": warning,
        })

    # Sort by frequency descending
    recommended.sort(key=lambda x: x["frequency"], reverse=True)
    skipped.sort(key=lambda x: x["frequency"], reverse=True)

    # Apply cap
    capped = recommended[:args.cap]
    remaining = recommended[args.cap:]

    result = {
        "recommended_entries": capped,
        "remaining_entries": remaining,
        "skipped_entries": skipped,
        "summary": {
            "total_dangerous_commands": sum(d["frequency"] for d in dangerous_commands),
            "unique_commands": len(dangerous_commands),
            "command_families": len(groups),
            "recommended_count": len(capped),
            "remaining_count": len(remaining),
            "skipped_count": len(skipped),
            "skipped_inherently_dangerous": sum(
                1 for s in skipped if s["reason"] == "inherently_dangerous"
            ),
            "skipped_too_broad": sum(
                1 for s in skipped if s["reason"] == "too_broad"
            ),
            "skipped_already_allowed": sum(
                1 for s in skipped if s["reason"] == "already_allowed"
            ),
        },
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
