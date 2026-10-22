# provenance: session 01a15409 (2026-10-19), baseline in recheck/INDEX.md
# verifies: wt usage drift vs 2026-10-19 portrait; exit 0=holding (this script reports, diff manually)
import json, glob, collections, datetime

def week_of(ts):
    d = datetime.date.fromisoformat(ts[:10])
    return (d - datetime.timedelta(days=d.weekday())).isoformat()  # Monday

weekly = collections.defaultdict(collections.Counter)
switch_form = collections.defaultdict(collections.Counter)  # week -> switch arg form
error_weekly = collections.Counter()

for path in glob.glob('/mnt/disk1/hyx/.pi/agent/sessions/*/*.jsonl'):
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            if '"worktrunk"' not in line:
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue
            msg = entry.get('message') or {}
            ts = entry.get('timestamp', '')
            if msg.get('role') == 'assistant':
                content = msg.get('content')
                if not isinstance(content, list):
                    continue
                for b in content:
                    if isinstance(b, dict) and b.get('type') == 'toolCall' and b.get('name') == 'worktrunk':
                        args = b.get('arguments') or {}
                        cmd = args.get('command', '?')
                        rest = args.get('args') or []
                        w = week_of(ts)
                        weekly[w][cmd] += 1
                        if cmd == 'switch':
                            if rest and rest[0] in ('-c', '--create'):
                                switch_form[w]['-c/--create 新建'] += 1
                            elif rest and rest[0] in ('-b', '-C'):
                                switch_form[w][rest[0]] += 1
                            else:
                                switch_form[w]['裸/分支名'] += 1
            elif msg.get('role') == 'toolResult' and msg.get('toolName') == 'worktrunk' and msg.get('isError'):
                error_weekly[week_of(ts)] += 1

print(f"{'week':12s} {'calls':>5s} {'err':>4s}  breakdown")
for w in sorted(weekly):
    calls = weekly[w]
    total = sum(calls.values())
    detail = ' '.join(f"{c}:{n}" for c, n in calls.most_common())
    print(f"{w:12s} {total:5d} {error_weekly.get(w,0):4d}  {detail}")

print("\n== switch 形态按周 ==")
print(f"{'week':12s} " + ' '.join(f"{k:>12s}" for k in ['-c/--create 新建', '裸/分支名', '-b', '-C']))
for w in sorted(switch_form):
    c = switch_form[w]
    print(f"{w:12s} " + ' '.join(f"{c.get(k,0):12d}" for k in ['-c/--create 新建', '裸/分支名', '-b', '-C']))
