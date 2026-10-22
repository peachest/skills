# provenance: session 01a15409 (2026-10-19), baseline in recheck/INDEX.md
# verifies: wt usage drift vs 2026-10-19 portrait; exit 0=holding (this script reports, diff manually)
import json, glob, collections, datetime

# worktrunk calls by (month, command), dedup by call id (session file unique anyway)
monthly_cmd = collections.defaultdict(collections.Counter)
sessions_per_month = collections.defaultdict(set)

for path in glob.glob('/mnt/disk1/hyx/.pi/agent/sessions/*/*.jsonl'):
    sid = path.split('/')[-1][:10]
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            if '"worktrunk"' not in line:
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue
            msg = entry.get('message') or {}
            if msg.get('role') != 'assistant':
                continue
            content = msg.get('content')
            if not isinstance(content, list):
                continue
            ts = entry.get('timestamp', '')
            month = ts[:7]  # YYYY-MM
            for b in content:
                if isinstance(b, dict) and b.get('type') == 'toolCall' and b.get('name') == 'worktrunk':
                    args = b.get('arguments') or {}
                    cmd = args.get('command', '?')
                    rest = args.get('args') or []
                    key = f"{cmd} {rest[0]}" if rest and rest[0].startswith('-') else (f"{cmd} {rest[0]}" if rest else cmd)
                    monthly_cmd[month][key.split()[0]] += 1
                    sessions_per_month[month].add(sid)

print(f"{'month':8s} {'calls':>5s} {'sess':>4s}  breakdown")
for month in sorted(monthly_cmd):
    calls = monthly_cmd[month]
    total = sum(calls.values())
    detail = ' '.join(f"{c}:{n}" for c, n in calls.most_common())
    print(f"{month:8s} {total:5d} {len(sessions_per_month[month]):4d}  {detail}")
