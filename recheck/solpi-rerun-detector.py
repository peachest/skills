import json, glob, os, re, hashlib, time
from collections import defaultdict

root = os.path.expanduser('~/.pi/agent/sessions')
now = time.time()
WINDOW = 30*86400
THRESH = 10*1024

def sha(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()

reruns = []          # dict per incident
archived_total = 0
sessions_scanned = 0

for f in glob.glob(root + '/*/*.jsonl'):
    if os.path.getmtime(f) < now - WINDOW: continue
    m = re.search(r'([0-9a-f]{8})-[0-9a-f]{4}', os.path.basename(f))
    if not m: continue
    sid = m.group(1)
    # ledger obs ids for this session
    led = os.path.join(os.path.dirname(f), 'sol-pi', sid and (m.group(0)[:-1] + '-'+m.group(1)[:0] or ''), )
    proj = os.path.basename(os.path.dirname(f))
    led = os.path.join(root, proj, 'sol-pi', m.group(0)+m.group(1)[8:] if False else '', )
    # simpler: find ledger dir by glob
    led_dir = os.path.join(root, proj, 'sol-pi')
    if not os.path.isdir(led_dir): continue
    match = [d for d in os.listdir(led_dir) if d.startswith(sid)]
    if not match: continue
    led_file = os.path.join(led_dir, match[0], 'observation-pack', 'ledger.jsonl')
    if not os.path.exists(led_file): continue
    ledger_ids = set()
    for line in open(led_file):
        try:
            e = json.loads(line)
            if e.get('id'): ledger_ids.add(e['id'])
        except: pass
    if not ledger_ids: continue
    sessions_scanned += 1

    # pass 1: collect toolResults (archived?) and assistant toolCalls in order
    events = []   # (ts, kind, data)
    for line in open(f):
        try: e = json.loads(line)
        except: continue
        msg = e.get('message') or {}
        ts = e.get('timestamp')
        c = msg.get('content')
        if msg.get('role') == 'toolResult' and isinstance(c, list) and c and all(p.get('type')=='text' for p in c if isinstance(p,dict)):
            text = '\n'.join(p.get('text','') for p in c if isinstance(p,dict))
            b = len(text.encode('utf8'))
            archived = False
            if not msg.get('isError') and b > THRESH:
                ch = sha(text)
                oid = 'obs_' + sha(f"{msg.get('toolName')}\0{msg.get('toolCallId')}\0{ch}")[:24]
                archived = oid in ledger_ids
                if archived: archived_total += 1
            events.append((ts, 'result', {'callId': msg.get('toolCallId'), 'tool': msg.get('toolName'),
                                          'archived': archived, 'bytes': b, 'isError': bool(msg.get('isError'))}))
        elif msg.get('role') == 'assistant' and isinstance(c, list):
            for p in c:
                if isinstance(p, dict) and p.get('type') == 'toolCall':
                    events.append((ts, 'call', {'callId': p.get('id'), 'tool': p.get('name'),
                                                'args': json.dumps(p.get('arguments'), sort_keys=True)}))
                elif isinstance(p, dict) and p.get('type') == 'text' and 'obs_recall' in (p.get('text') or ''):
                    pass
        elif msg.get('role') == 'assistant':
            pass

    # detect obs_recall calls
    recall_calls = [ev for ev in events if ev[1]=='call' and ev[2]['tool']=='obs_recall']

    # pass 2: for each archived result, find later identical (tool,args) call
    for i,(ts,kind,d) in enumerate(events):
        if kind!='result' or not d['archived']: continue
        # build callId->args map
    args_by_id = {ev[2]['callId']: ev[2]['args'] for ev in events if ev[1]=='call'}
    for i,(ts,kind,d) in enumerate(events):
        if kind!='result' or not d['archived']: continue
        orig_args = args_by_id.get(d['callId'])
        if not orig_args: continue
        for j in range(i+1, len(events)):
            ts2, k2, d2 = events[j]
            if k2=='call':
                if d2['tool']=='obs_recall':
                    break  # model recalled first
                if d2['tool']==d['tool'] and d2['args']==orig_args:
                    reruns.append({'sid': sid, 'tool': d['tool'], 'bytes': d['bytes'],
                                   'gap_events': j-i, 'ts': ts2})
                    break

print(f'sessions scanned (with ledger): {sessions_scanned}')
print(f'archived results matched via hash: {archived_total}')
print(f're-run-instead-of-recall incidents: {len(reruns)}')
by_tool = defaultdict(int)
for r in reruns: by_tool[r['tool']] += 1
print('by tool:', dict(by_tool))
gaps = sorted(r['gap_events'] for r in reruns)
if gaps: print('gap events min/med/max:', gaps[0], gaps[len(gaps)//2], gaps[-1])
for r in reruns[:10]: print(r)
