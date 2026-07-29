#!/usr/bin/env python3
"""
Pi Insight — Usage Analysis Script

Scans pi session JSONL files and produces a usage frequency report.
Also analyzes system prompt dump structure and installed skills.

Output: JSON with tool_counts, skill_counts, prompt_breakdown, installed_skills.

Usage:
  python3 analyze.py usage --sessions ~/.pi/agent/sessions --limit 100
  python3 analyze.py prompt --dump <path-to-system-prompt-dump.txt>
  python3 analyze.py all --sessions ~/.pi/agent/sessions --limit 100 --dump <path> --skills-dir ~/.pi/agent/skills
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime


# ─── Session Scanning ──────────────────────────────────────────────────────────

def find_session_files(sessions_dir, limit=None):
    """Find all .jsonl session files, sorted by modification time (most recent first)."""
    files = []
    for root, _, filenames in os.walk(sessions_dir):
        for f in filenames:
            if f.endswith('.jsonl'):
                fp = os.path.join(root, f)
                try:
                    mtime = os.path.getmtime(fp)
                    files.append((fp, mtime))
                except OSError:
                    pass
    files.sort(key=lambda x: x[1], reverse=True)
    if limit:
        files = files[:limit]
    return [f[0] for f in files]


def extract_text(content):
    """Extract text from message content."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get('type') == 'text':
                parts.append(block.get('text', ''))
        return ' '.join(parts)
    return ''


# Patterns for skill detection
SKILL_CMD_RE = re.compile(r'/skill:([a-zA-Z0-9_-]+)')
SKILL_TAG_RE = re.compile(r'<skill\s+name="([^"]+)"')


def parse_session(filepath):
    """Parse a session JSONL file and extract tool/skill usage."""
    tool_counts = Counter()
    tools_in_session = set()
    skill_cmd_counts = Counter()      # /skill:name commands
    skill_tag_counts = Counter()      # <skill name="..."> injections
    skills_in_session = set()
    user_msgs = 0
    assistant_msgs = 0
    tool_errors = 0
    session_cwd = None
    session_id = None
    first_ts = None
    last_ts = None
    model = None

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                etype = entry.get('type', '')

                # Session info
                if etype in ('session', 'session_info'):
                    if entry.get('cwd'):
                        session_cwd = entry['cwd']
                    if entry.get('id'):
                        session_id = entry['id']
                    continue

                # Model tracking
                if etype == 'model_change':
                    model = entry.get('id') or entry.get('modelId')
                    continue

                if etype != 'message':
                    continue

                msg = entry.get('message', {})
                if not msg:
                    continue

                role = msg.get('role', '')
                ts = msg.get('timestamp')
                if ts:
                    if first_ts is None:
                        first_ts = ts
                    last_ts = ts

                content = msg.get('content', [])

                if role == 'user':
                    user_msgs += 1
                    text = extract_text(content)
                    if text:
                        # /skill:name commands
                        for m in SKILL_CMD_RE.finditer(text):
                            name = m.group(1)
                            skill_cmd_counts[name] += 1
                            skills_in_session.add(name)
                        # <skill name="..."> injections (agent-invoked skills)
                        for m in SKILL_TAG_RE.finditer(text):
                            name = m.group(1)
                            skill_tag_counts[name] += 1
                            skills_in_session.add(name)

                elif role == 'assistant':
                    assistant_msgs += 1
                    if isinstance(content, list):
                        seen_ids = set()
                        for block in content:
                            if not isinstance(block, dict):
                                continue
                            if block.get('type') == 'toolCall':
                                tid = block.get('id', '')
                                if tid in seen_ids:
                                    continue
                                seen_ids.add(tid)
                                name = block.get('name', 'unknown')
                                tool_counts[name] += 1
                                tools_in_session.add(name)

                elif role == 'toolResult':
                    if msg.get('isError'):
                        tool_errors += 1

        return {
            'filepath': os.path.basename(filepath),
            'session_id': session_id,
            'cwd': session_cwd,
            'model': model,
            'user_messages': user_msgs,
            'assistant_messages': assistant_msgs,
            'tool_counts': dict(tool_counts),
            'tools_used': sorted(tools_in_session),
            'skill_cmd_counts': dict(skill_cmd_counts),
            'skill_tag_counts': dict(skill_tag_counts),
            'skills_used': sorted(skills_in_session),
            'tool_errors': tool_errors,
            'first_timestamp': first_ts,
            'last_timestamp': last_ts,
        }
    except Exception as e:
        print(f"Warning: failed to parse {filepath}: {e}", file=sys.stderr)
        return None


def scan_usage(sessions_dir, limit=100):
    """Scan recent sessions and aggregate usage stats."""
    files = find_session_files(sessions_dir, limit)
    if not files:
        return {'error': f'No session files found in {sessions_dir}'}

    sessions = []
    all_tool_calls = Counter()
    tool_session_count = Counter()
    all_skill_cmd = Counter()
    all_skill_tag = Counter()
    skill_session_count = Counter()
    total_user = 0
    total_assistant = 0
    total_errors = 0

    for fp in files:
        result = parse_session(fp)
        if not result:
            continue
        sessions.append(result)
        for tool, cnt in result['tool_counts'].items():
            all_tool_calls[tool] += cnt
        for tool in result['tools_used']:
            tool_session_count[tool] += 1
        for skill, cnt in result['skill_cmd_counts'].items():
            all_skill_cmd[normalize_skill_name(skill)] += cnt
        for skill, cnt in result['skill_tag_counts'].items():
            all_skill_tag[normalize_skill_name(skill)] += cnt
        for skill in result['skills_used']:
            skill_session_count[normalize_skill_name(skill)] += 1
        total_user += result['user_messages']
        total_assistant += result['assistant_messages']
        total_errors += result['tool_errors']

    timestamps = [s['first_timestamp'] for s in sessions if s['first_timestamp']]
    date_range = {}
    if timestamps:
        raw_start = min(timestamps)
        raw_end = max(timestamps)
        date_range['start'] = _fmt_ts(raw_start)
        date_range['end'] = _fmt_ts(raw_end)
        date_range['start_raw'] = raw_start
        date_range['end_raw'] = raw_end

    return {
        'sessions_analyzed': len(sessions),
        'date_range': date_range,
        'totals': {
            'user_messages': total_user,
            'assistant_messages': total_assistant,
            'tool_errors': total_errors,
        },
        'tool_usage': {
            'total_calls': dict(all_tool_calls.most_common()),
            'session_count': dict(tool_session_count.most_common()),
        },
        'skill_usage': {
            'cmd_invocations': dict(all_skill_cmd.most_common()),
            'tag_injections': dict(all_skill_tag.most_common()),
            'session_count': dict(skill_session_count.most_common()),
        },
    }


def _fmt_ts(ts):
    """Format timestamp (epoch ms or ISO string) to human-readable."""
    if ts is None:
        return None
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M')
    if isinstance(ts, str):
        try:
            return datetime.fromisoformat(ts.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
        except Exception:
            return ts
    return str(ts)


# ─── Skill Name Normalization ─────────────────────────────────────────────────

# Known skill name variants that should be merged
SKILL_NORMALIZE_MAP = {
    'grill-with-doc': 'grill-with-docs',
    'learn-from-example': 'learn-from-examples',
}


def normalize_skill_name(name):
    """Normalize skill name to canonical form."""
    return SKILL_NORMALIZE_MAP.get(name, name)


# ─── System Prompt Analysis ────────────────────────────────────────────────────

# Section markers in the system prompt dump
SECTION_MARKERS = [
    ('tools',         r'^Available tools:'),
    ('transition',    r'^In addition to the tools above'),
    ('guidelines',    r'^Guidelines:'),
    ('pi_docs',       r'^Pi documentation'),
    ('project_context', r'^## Development'),
    ('agent_skills',  r'^## Agent skills'),
    ('skills_list',   r'^<available_skills>'),
    ('after_skills',  r'^</available_skills>'),
]


def analyze_prompt_dump(dump_path):
    """Analyze system prompt dump structure."""
    try:
        with open(dump_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return {'error': f'Cannot read {dump_path}: {e}'}

    total_lines = len(lines)
    total_bytes = os.path.getsize(dump_path)

    # Find section boundaries
    sections = []
    current_section = 'preamble'
    current_start = 0
    for i, line in enumerate(lines):
        for name, pattern in SECTION_MARKERS:
            if re.match(pattern, line.strip()):
                if i > current_start:
                    sections.append((current_section, current_start, i))
                current_section = name
                current_start = i
                break
    sections.append((current_section, current_start, total_lines))

    section_stats = []
    for name, start, end in sections:
        line_count = end - start
        byte_count = sum(len(lines[j].encode('utf-8')) for j in range(start, end))
        pct = round(line_count / total_lines * 100, 1) if total_lines > 0 else 0
        section_stats.append({
            'section': name,
            'start_line': start + 1,
            'end_line': end,
            'lines': line_count,
            'bytes': byte_count,
            'percentage': pct,
        })

    # Extract tool declarations
    tools_declared = []
    in_tools = False
    for line in lines:
        if line.strip() == 'Available tools:':
            in_tools = True
            continue
        if in_tools:
            if line.startswith('- '):
                m = re.match(r'^- (\S+):', line)
                if m:
                    tools_declared.append(m.group(1))
            elif not line.startswith(' ') and not line.startswith('-') and line.strip():
                in_tools = False

    # Extract skill declarations from <available_skills> section
    # Also measure per-skill prompt footprint (lines + bytes within <skill> blocks)
    skills_declared = []
    skill_prompt_footprint = {}  # name -> {lines, bytes}
    in_skills = False
    in_skill_block = False
    skill_block_start = 0
    current_skill_name = None
    for i, line in enumerate(lines):
        if '<available_skills>' in line:
            in_skills = True
        if in_skills and '<skill>' in line:
            in_skill_block = True
            skill_block_start = i
            current_skill_name = None
        if in_skills and in_skill_block and '<name>' in line:
            m = re.search(r'<name>([^<]+)</name>', line)
            if m:
                current_skill_name = m.group(1)
                skills_declared.append(current_skill_name)
        if in_skills and in_skill_block and '</skill>' in line:
            block_lines = i - skill_block_start + 1
            block_bytes = sum(len(lines[j].encode('utf-8')) for j in range(skill_block_start, i + 1))
            if current_skill_name:
                skill_prompt_footprint[current_skill_name] = {
                    'prompt_lines': block_lines,
                    'prompt_bytes': block_bytes,
                }
            in_skill_block = False
        if '</available_skills>' in line:
            in_skills = False

    return {
        'total_lines': total_lines,
        'total_bytes': total_bytes,
        'total_kb': round(total_bytes / 1024, 1),
        'sections': section_stats,
        'tools_declared': tools_declared,
        'tools_count': len(tools_declared),
        'skills_declared': skills_declared,
        'skills_count': len(skills_declared),
        'skill_prompt_footprint': skill_prompt_footprint,
    }


# ─── Installed Skills ──────────────────────────────────────────────────────────

def list_installed_skills(skills_dir):
    """List installed skills with line counts.
    Scans top-level dirs for SKILL.md, then recursively scans subdirs of
    top-level dirs that don't have their own SKILL.md (handles nested
    skill packages like domain-driven-design-skills/skills/ddd-contexts/).
    """
    skills = []
    if not os.path.isdir(skills_dir):
        return skills

    def parse_skill_md(skill_md, dir_name):
        """Parse SKILL.md for name, description, line_count."""
        name = dir_name
        description = ''
        line_count = 0
        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
                line_count = content.count('\n') + 1
                if content.startswith('---'):
                    end = content.find('---', 3)
                    if end > 0:
                        for line in content[3:end].split('\n'):
                            if line.startswith('name:'):
                                name = line.split(':', 1)[1].strip()
                            elif line.startswith('description:'):
                                description = line.split(':', 1)[1].strip().strip('"\'')
        except Exception as e:
            print(f"Warning: failed to read {skill_md}: {e}", file=sys.stderr)
        return {
            'dir_name': dir_name,
            'name': name,
            'description': description[:200],
            'line_count': line_count,
        }

    for entry in sorted(os.listdir(skills_dir)):
        skill_path = os.path.join(skills_dir, entry)
        if not os.path.isdir(skill_path):
            continue
        top_skill_md = os.path.join(skill_path, 'SKILL.md')
        if os.path.isfile(top_skill_md):
            # Top-level skill
            skills.append(parse_skill_md(top_skill_md, entry))
        else:
            # Nested skill package — recursively find SKILL.md in subdirs
            for root, _, filenames in os.walk(skill_path):
                if 'SKILL.md' in filenames:
                    nested_md = os.path.join(root, 'SKILL.md')
                    nested_dir = os.path.basename(root)
                    skills.append(parse_skill_md(nested_md, nested_dir))

    skills.sort(key=lambda s: s['name'])
    return skills


# ─── Cross-Reference ───────────────────────────────────────────────────────────

def cross_reference(usage_data, prompt_data, installed_skills):
    """Cross-reference declared vs used tools/skills."""
    result = {}

    # Tools
    if prompt_data and 'tools_declared' in prompt_data:
        declared = set(prompt_data['tools_declared'])
        used = set(usage_data.get('tool_usage', {}).get('session_count', {}).keys())
        result['tools'] = {
            'declared': sorted(declared),
            'used': sorted(declared & used),
            'zero_use': sorted(declared - used),
            'not_declared_but_used': sorted(used - declared),
        }

    # Skills
    if prompt_data and 'skills_declared' in prompt_data:
        declared = set(prompt_data['skills_declared'])
    else:
        declared = set(s['dir_name'] for s in installed_skills)

    used_skills = set(usage_data.get('skill_usage', {}).get('session_count', {}).keys())
    result['skills'] = {
        'declared': sorted(declared),
        'used': sorted(declared & used_skills),
        'zero_use': sorted(declared - used_skills),
        'not_declared_but_used': sorted(used_skills - declared),
    }

    # Skill savings: measure both disk footprint and prompt footprint
    # Build a lookup that matches by name (from frontmatter) AND dir_name
    if installed_skills:
        # Index by both dir_name and frontmatter name for fuzzy matching
        skill_by_dir = {s['dir_name']: s for s in installed_skills}
        skill_by_name = {s['name']: s for s in installed_skills if s['name'] != s['dir_name']}

        def find_skill_info(skill_name):
            """Find skill info by prompt name, trying dir_name then frontmatter name."""
            if skill_name in skill_by_dir:
                return skill_by_dir[skill_name]
            if skill_name in skill_by_name:
                return skill_by_name[skill_name]
            return None

        zero_use_disk_lines = 0
        for s in result['skills']['zero_use']:
            info = find_skill_info(s)
            if info:
                zero_use_disk_lines += info['line_count']
        result['skills']['zero_use_disk_lines'] = zero_use_disk_lines

    # Prompt footprint: actual lines/bytes in the <skill> blocks (from prompt analysis)
    if prompt_data and 'skill_prompt_footprint' in prompt_data:
        footprint = prompt_data['skill_prompt_footprint']
        zero_use_prompt_lines = sum(
            footprint.get(s, {}).get('prompt_lines', 0)
            for s in result['skills']['zero_use']
        )
        zero_use_prompt_bytes = sum(
            footprint.get(s, {}).get('prompt_bytes', 0)
            for s in result['skills']['zero_use']
        )
        result['skills']['zero_use_prompt_lines'] = zero_use_prompt_lines
        result['skills']['zero_use_prompt_bytes'] = zero_use_prompt_bytes
        result['skills']['zero_use_prompt_kb'] = round(zero_use_prompt_bytes / 1024, 1)

        # Also build per-skill detail table for all declared skills
        usage_session_count = usage_data.get('skill_usage', {}).get('session_count', {})
        usage_cmd = usage_data.get('skill_usage', {}).get('cmd_invocations', {})
        usage_tag = usage_data.get('skill_usage', {}).get('tag_injections', {})
        detail = []
        for s in result['skills']['declared']:
            fp = footprint.get(s, {})
            disk_info = find_skill_info(s) if installed_skills else None
            detail.append({
                'name': s,
                'prompt_lines': fp.get('prompt_lines', 0),
                'prompt_bytes': fp.get('prompt_bytes', 0),
                'disk_lines': disk_info['line_count'] if disk_info else 0,
                'session_count': usage_session_count.get(s, 0),
                'cmd_count': usage_cmd.get(s, 0),
                'tag_count': usage_tag.get(s, 0),
                'status': 'used' if s in used_skills else 'zero_use',
            })
        # Sort by session_count desc, then prompt_lines desc
        detail.sort(key=lambda x: (-x['session_count'], -x['prompt_lines']))
        result['skills']['detail'] = detail

    return result


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Pi Insight — Usage Analysis')
    sub = parser.add_subparsers(dest='command')

    # Debugging-only subcommands; production path is 'all'
    p_usage = sub.add_parser('usage', help='[debug] Scan session usage only')
    p_usage.add_argument('--sessions', default=os.path.expanduser('~/.pi/agent/sessions'))
    p_usage.add_argument('--limit', type=int, default=100)

    p_prompt = sub.add_parser('prompt', help='[debug] Analyze system prompt dump only')
    p_prompt.add_argument('--dump', required=True, help='Path to system prompt dump file')

    # all subcommand
    p_all = sub.add_parser('all', help='Full analysis')
    p_all.add_argument('--sessions', default=os.path.expanduser('~/.pi/agent/sessions'))
    p_all.add_argument('--limit', type=int, default=100)
    p_all.add_argument('--dump', default=None, help='Path to system prompt dump file')
    p_all.add_argument('--skills-dir', default=os.path.expanduser('~/.pi/agent/skills'))

    args = parser.parse_args()

    if args.command == 'usage':
        result = scan_usage(args.sessions, args.limit)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.command == 'prompt':
        result = analyze_prompt_dump(args.dump)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.command == 'all':
        usage = scan_usage(args.sessions, args.limit)
        prompt = analyze_prompt_dump(args.dump) if args.dump else None
        skills = list_installed_skills(args.skills_dir)
        xref = cross_reference(usage, prompt, skills)

        result = {
            'usage': usage,
            'prompt': prompt,
            'installed_skills': skills,
            'installed_skill_count': len(skills),
            'total_skill_lines': sum(s['line_count'] for s in skills),
            'cross_reference': xref,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
