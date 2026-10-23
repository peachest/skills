import json, glob, os, re, time, statistics
from collections import defaultdict

root = os.path.expanduser('~/.pi/agent/sessions')
now = time.time()
calls = []       # (sid, callId, obs_id)
results = {}     # callId -> (isError, size, text)

for f in glob.glob(root + '/*/*.jsonl'):
    if os.path.getmtime(f) < now - 30*86400: continue
    sid = re.search(r'([0-9a-f]{8})-[0-9a-f]{4}-', os.path.basename(f))
    sid = sid.group(1) if sid else '?'
    with open(f) as fh:
        for line in fh:
            if '"obs_recall"' not in line: continue
            try: e = json.loads(line)
            except: continue
            m = e.get('message') or {}
            c = m.get('content')
            if m.get('role') == 'assistant' and isinstance(c, list):
                for part in c:
                    if isinstance(part, dict) and part.get('type')=='toolCall' and part.get('name')=='obs_recall':
                        obs_id = (part.get('arguments') or {}).get('id')
                        calls.append((sid, part.get('id'), obs_id))
            elif m.get('role') == 'toolResult' and m.get('toolName') == 'obs_recall':
                text = m.get('content')
                text = text if isinstance(text, str) else json.dumps(text)
                results[m.get('toolCallId')] = (m.get('isError', False), len(text or ''), (text or '')[:100])

print('real obs_recall calls (30d):', len(calls))
if len(calls) == 0: import sys; sys.exit('ZERO-RESULT: no obs_recall calls parsed - structure or filter drifted')
paired = [results[ci] for _,ci,_ in calls if ci in results]
print('paired results:', len(paired))
err = sum(1 for v in paired if v[0])
print('error results:', err)
ok_sizes = sorted(v[1] for v in paired if not v[0])
if ok_sizes:
    print('size min/med/max: %d/%d/%d' % (ok_sizes[0], ok_sizes[len(ok_sizes)//2], ok_sizes[-1]))
    print('tiny (<200B):', sum(1 for s in ok_sizes if s<200), ' substantial (>1KB):', sum(1 for s in ok_sizes if s>1024))
print('distinct obs ids:', len(set(x[2] for x in calls if x[2])))
per = defaultdict(int)
for x in calls: per[x[0]] += 1
print('sessions with >=1 call:', len(per), ' top:', sorted(per.items(), key=lambda x:-x[1])[:5])
print('--- samples ---')
n=0
for v in paired:
    if v[0] and n<3: print('ERR', repr(v[2])); n+=1
for v in paired:
    if not v[0] and v[1]>800 and n<6: print('BIG', v[1], repr(v[2])); n+=1
