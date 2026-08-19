#!/usr/bin/env python3
"""
pi-session-cleanup: Quick cleanup tool for pi agent sessions.

Cleans up:
  1. Trivial/test top-level sessions (short, like "hi", "hello", "test")
  2. Old subagent sessions that are unlikely to be resumed in foreground
  3. Old single-message top-level sessions
  4. Empty/abandoned session directories

Usage:
  python3 pi-session-cleanup.py                    # Dry-run, show what would be cleaned
  python3 pi-session-cleanup.py --execute          # Actually delete
  python3 pi-session-cleanup.py --age 14           # Custom age threshold (days) for subagents
  python3 pi-session-cleanup.py --no-subagent      # Only clean trivial top-level sessions
  python3 pi-session-cleanup.py --keep-recent 3    # Keep sessions active within 3 days
  python3 pi-session-cleanup.py --stats            # Only show statistics
"""

import json
import os
import sys
import argparse
import shutil
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path


# Default pi sessions directory
def find_sessions_dir():
    """Find the pi sessions directory."""
    home = os.path.expanduser("~")
    candidates = [
        os.path.join(home, ".pi", "agent", "sessions"),
        os.path.join(home, ".pi", "sessions"),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return candidates[0]


def parse_session_file(fpath):
    """Parse a session JSONL file and extract metadata."""
    try:
        with open(fpath, 'r') as f:
            lines = f.readlines()
        if not lines:
            return None

        first = json.loads(lines[0])
        session_id = first.get('id', '')
        start_ts = first.get('timestamp', '')
        cwd = first.get('cwd', '')
        parent_session = first.get('parentSession', None)

        total_lines = len(lines)
        last_ts = ''
        first_user_msg = ''
        msg_count = 0

        for line in lines:
            try:
                d = json.loads(line)
                ts = d.get('timestamp', '')
                if ts:
                    last_ts = ts
                t = d.get('type', '')
                if t == 'message':
                    msg = d.get('message', {})
                    role = msg.get('role', '')
                    if role == 'user':
                        msg_count += 1
                        if not first_user_msg:
                            content = msg.get('content', '')
                            if isinstance(content, list):
                                texts = [c.get('text', '') for c in content
                                         if isinstance(c, dict) and c.get('type') == 'text']
                                first_user_msg = ' '.join(texts)[:150]
                            elif isinstance(content, str):
                                first_user_msg = content[:150]
            except:
                pass

        file_size = os.path.getsize(fpath)

        try:
            start_dt = datetime.fromisoformat(start_ts.replace('Z', '+00:00'))
        except:
            start_dt = None
        try:
            last_dt = datetime.fromisoformat(last_ts.replace('Z', '+00:00')) if last_ts else start_dt
        except:
            last_dt = start_dt

        return {
            'session_id': session_id,
            'fpath': fpath,
            'start_ts': start_ts,
            'last_ts': last_ts,
            'cwd': cwd,
            'total_lines': total_lines,
            'msg_count': msg_count,
            'first_user_msg': first_user_msg.strip() if first_user_msg else '',
            'file_size': file_size,
            'is_subagent': parent_session is not None,
            'parent_session': parent_session,
            'start_dt': start_dt,
            'last_dt': last_dt,
        }
    except Exception as e:
        return None


def scan_all_sessions(sessions_dir):
    """Scan all session files."""
    results = []
    if not os.path.isdir(sessions_dir):
        return results

    for project_dir in os.listdir(sessions_dir):
        pdir = os.path.join(sessions_dir, project_dir)
        if not os.path.isdir(pdir):
            continue
        for fname in os.listdir(pdir):
            if not fname.endswith('.jsonl'):
                continue
            fpath = os.path.join(pdir, fname)
            info = parse_session_file(fpath)
            if info:
                info['project_dir'] = project_dir
                info['fname'] = fname
                results.append(info)

    return results


def age_days(info, now=None):
    """Calculate age in days since last activity."""
    if now is None:
        now = datetime.now(timezone.utc)
    if info['last_dt']:
        return (now - info['last_dt']).days
    return 999


def is_trivial_session(info):
    """Check if a session is trivial (test/hi/hello/test/doctor)."""
    if info['total_lines'] <= 10:
        msg = info['first_user_msg'].lower().strip()
        trivial_keywords = ['hi', 'hello', 'test', 'say hi', 'doctor', 'version',
                           'help', 'hey', 'ping', '你好', '测试']
        for kw in trivial_keywords:
            if msg == kw or msg.startswith(kw + '\n') or msg.startswith(kw + ' '):
                return True
        # Very short with <=5 lines and small size
        if info['total_lines'] <= 5 and info['file_size'] < 5000:
            return True
    return False


def classify_cleanup(info, args):
    """Determine if a session should be cleaned up and why.
    Returns (should_clean, reason).
    """
    now = datetime.now(timezone.utc)
    age = age_days(info, now)

    # Never clean sessions active within keep_recent days
    if age < args.keep_recent:
        return False, None

    # 1. Trivial top-level sessions
    if not args.no_trivial and not info['is_subagent']:
        if is_trivial_session(info):
            return True, 'trivial_top_level'

    # 2. Old subagent sessions
    if not args.no_subagent and info['is_subagent']:
        if age >= args.subagent_age:
            return True, f'old_subagent_{age}d'

    # 3. Old single-message top-level sessions
    if not args.no_old_single and not info['is_subagent']:
        if info['msg_count'] <= 1 and age >= args.old_single_age:
            # But don't clean if it's a large session (might be important)
            if info['file_size'] < 500000:  # 500KB
                return True, f'old_single_msg_{age}d'

    # 4. Very short sessions regardless of type
    if not args.no_tiny and info['total_lines'] <= 3:
        return True, 'tiny_session'

    return False, None


def format_size(size):
    """Format file size human-readably."""
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size/1024:.1f}KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size/1024/1024:.1f}MB"
    else:
        return f"{size/1024/1024/1024:.2f}GB"


def print_stats(sessions):
    """Print session statistics."""
    now = datetime.now(timezone.utc)
    total_size = sum(s['file_size'] for s in sessions)

    print(f"\n{'='*70}")
    print(f"  Pi Session Statistics")
    print(f"{'='*70}")
    print(f"  Total sessions: {len(sessions)}")
    print(f"  Total size:     {format_size(total_size)}")

    sub = [s for s in sessions if s['is_subagent']]
    top = [s for s in sessions if not s['is_subagent']]
    print(f"  Top-level:      {len(top)}")
    print(f"  Subagent:       {len(sub)}")

    # Line count distribution
    print(f"\n  --- Line count distribution ---")
    for name, lo, hi in [('1-5', 0, 5), ('6-10', 6, 10), ('11-20', 11, 20),
                         ('21-50', 21, 50), ('51-100', 51, 100),
                         ('101-200', 101, 200), ('200+', 201, 99999)]:
        c = sum(1 for s in sessions if lo <= s['total_lines'] <= hi)
        bar = '█' * (c // max(1, len(sessions) // 80))
        print(f"    {name:>8} lines: {c:>5}  {bar}")

    # Age distribution
    print(f"\n  --- Age distribution (days since last activity) ---")
    for name, lo, hi in [('<1d', 0, 1), ('1-3d', 1, 3), ('3-7d', 3, 7),
                         ('7-30d', 7, 30), ('30-60d', 30, 60), ('60d+', 60, 99999)]:
        c = sum(1 for s in sessions if lo <= age_days(s, now) < hi)
        bar = '█' * (c // max(1, len(sessions) // 80))
        print(f"    {name:>8}: {c:>5}  {bar}")

    # Top 10 projects
    print(f"\n  --- Top 15 projects by session count ---")
    proj_counter = Counter(s['project_dir'] for s in sessions)
    for proj, count in proj_counter.most_common(15):
        sub_count = sum(1 for s in sessions if s['project_dir'] == proj and s['is_subagent'])
        size = sum(s['file_size'] for s in sessions if s['project_dir'] == proj)
        print(f"    {count:>4} ({sub_count:>3} sub) {format_size(size):>8}  | {proj}")

    # Subagent specifics
    print(f"\n  --- Subagent sessions ---")
    print(f"    Total: {len(sub)}")
    old_sub = [s for s in sub if age_days(s, now) >= 7]
    print(f"    Older than 7 days: {len(old_sub)}")
    old_sub_3 = [s for s in sub if age_days(s, now) >= 3]
    print(f"    Older than 3 days: {len(old_sub_3)}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description='Quick cleanup tool for pi agent sessions.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Dry-run: show what would be cleaned
  %(prog)s --execute                    # Actually delete files
  %(prog)s --age 14                     # Clean subagents older than 14 days
  %(prog)s --keep-recent 3             # Keep sessions active within 3 days
  %(prog)s --no-subagent               # Only clean trivial top-level sessions
  %(prog)s --stats                      # Only show statistics
        """)
    parser.add_argument('--execute', action='store_true',
                        help='Actually delete files (default: dry-run)')
    parser.add_argument('--age', type=int, default=7, dest='subagent_age',
                        help='Min age (days) for subagent cleanup (default: 7)')
    parser.add_argument('--old-single-age', type=int, default=14,
                        help='Min age (days) for old single-message top-level cleanup (default: 14)')
    parser.add_argument('--keep-recent', type=int, default=1,
                        help='Never clean sessions active within N days (default: 1)')
    parser.add_argument('--no-subagent', action='store_true',
                        help='Skip subagent cleanup')
    parser.add_argument('--no-trivial', action='store_true',
                        help='Skip trivial top-level session cleanup')
    parser.add_argument('--no-old-single', action='store_true',
                        help='Skip old single-message top-level cleanup')
    parser.add_argument('--no-tiny', action='store_true',
                        help='Skip tiny session (<=3 lines) cleanup')
    parser.add_argument('--stats', action='store_true',
                        help='Only show statistics, no cleanup analysis')
    parser.add_argument('--sessions-dir', type=str, default=None,
                        help='Custom sessions directory (default: auto-detect)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show details of each session to be cleaned')

    args = parser.parse_args()

    sessions_dir = args.sessions_dir or find_sessions_dir()
    if not os.path.isdir(sessions_dir):
        print(f"Error: Sessions directory not found: {sessions_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning: {sessions_dir}")
    sessions = scan_all_sessions(sessions_dir)

    if not sessions:
        print("No sessions found.")
        sys.exit(0)

    # Always show stats
    print_stats(sessions)

    if args.stats:
        sys.exit(0)

    # Classify sessions
    now = datetime.now(timezone.utc)
    cleanup_list = []
    keep_list = []

    for info in sessions:
        should_clean, reason = classify_cleanup(info, args)
        if should_clean:
            info['cleanup_reason'] = reason
            cleanup_list.append(info)
        else:
            keep_list.append(info)

    # Group by reason
    reason_groups = {}
    for info in cleanup_list:
        reason = info['cleanup_reason']
        # Normalize age in reason for grouping
        if reason.startswith('old_subagent_'):
            reason = 'old_subagent'
        elif reason.startswith('old_single_msg_'):
            reason = 'old_single_msg'
        reason_groups.setdefault(reason, []).append(info)

    total_clean_size = sum(s['file_size'] for s in cleanup_list)
    total_keep_size = sum(s['file_size'] for s in keep_list)

    print(f"{'='*70}")
    print(f"  Cleanup Plan {'(DRY RUN)' if not args.execute else '(EXECUTING)'}")
    print(f"{'='*70}")
    print(f"  Sessions to clean: {len(cleanup_list)} ({format_size(total_clean_size)})")
    print(f"  Sessions to keep:  {len(keep_list)} ({format_size(total_keep_size)})")
    print()

    for reason, items in sorted(reason_groups.items(), key=lambda x: -len(x[1])):
        size = sum(s['file_size'] for s in items)
        print(f"  [{reason}] {len(items)} sessions ({format_size(size)})")
        if args.verbose or len(items) <= 20:
            for s in sorted(items, key=lambda x: x['start_ts'], reverse=True)[:50]:
                sub_tag = "[SUB]" if s['is_subagent'] else "     "
                age = age_days(s, now)
                msg = s['first_user_msg'][:60] if s['first_user_msg'] else '(no user msg)'
                print(f"    {sub_tag} {s['start_ts'][:10]} age={age:>3}d lines={s['total_lines']:>4} "
                      f"size={format_size(s['file_size']):>8} | {msg}")
            if len(items) > 50:
                print(f"    ... and {len(items) - 50} more")
        print()

    # Check for empty project directories that can be removed
    all_project_dirs = set(os.path.join(sessions_dir, s['project_dir']) for s in sessions)
    cleanup_fpaths = set(s['fpath'] for s in cleanup_list)
    empty_dirs = []
    for pdir in all_project_dirs:
        if not os.path.isdir(pdir):
            continue
        remaining = [f for f in os.listdir(pdir) if f.endswith('.jsonl')]
        if not remaining:
            empty_dirs.append(pdir)

    if empty_dirs:
        print(f"  Empty project directories to remove: {len(empty_dirs)}")
        if args.verbose:
            for d in empty_dirs:
                print(f"    {d}")
        print()

    if not args.execute:
        print(f"\n  >>> Dry run complete. Run with --execute to actually delete. <<<")
        print(f"  >>> Would reclaim ~{format_size(total_clean_size)} <<<")
    else:
        print(f"\n  Executing cleanup...")
        deleted_count = 0
        deleted_size = 0
        for info in cleanup_list:
            try:
                os.remove(info['fpath'])
                deleted_count += 1
                deleted_size += info['file_size']
            except Exception as e:
                print(f"    ERROR: {info['fpath']}: {e}", file=sys.stderr)

        # Remove empty directories
        for d in empty_dirs:
            try:
                os.rmdir(d)
            except:
                pass

        print(f"  Deleted {deleted_count} session files ({format_size(deleted_size)})")
        if empty_dirs:
            print(f"  Removed {len(empty_dirs)} empty directories")
        print(f"  Done!")

    print()


if __name__ == '__main__':
    main()
