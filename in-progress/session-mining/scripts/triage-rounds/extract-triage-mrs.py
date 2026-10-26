#!/usr/bin/env python3
"""Extract ocr-pull-discussions.py invocations from the find-tool-calls dump.
Input: $TRIAGE_ROUNDS_OUT/pull-calls.json (default ~/tmp/triage-rounds).
Output: $TRIAGE_ROUNDS_OUT/pull-invocations.json, per-invocation
{session_file, ts, mr, mode(digest/full), cmd}"""
import json, os, re, sys, glob

OUT_DIR = os.environ.get('TRIAGE_ROUNDS_OUT', os.path.expanduser('~/tmp/triage-rounds'))

IN = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT_DIR, 'pull-calls.json')
sessions = json.load(open(IN))['sessions']
out = []
mr_re = re.compile(r'ocr-pull-discussions\.py\s+(\S+)')
for s in sessions:
    f = s['file']
    try:
        lines = open(f, 'rb').read().splitlines()
    except OSError:
        continue
    for line in lines:
        try:
            e = json.loads(line)
        except Exception:
            continue
        msg = e.get('message') or {}
        # find tool calls
        content = msg.get('content')
        if not isinstance(content, list):
            continue
        for c in content:
            if not isinstance(c, dict) or c.get('type') != 'toolCall':
                continue
            call = c.get('call', c)
            name = call.get('name') or call.get('toolName')
            args = call.get('arguments') or call.get('args') or {}
            cmd = ''
            if isinstance(args, dict):
                cmd = args.get('command') or args.get('cmd') or ''
                if not isinstance(cmd, str):
                    cmd = json.dumps(cmd, ensure_ascii=False)
            elif isinstance(args, str):
                cmd = args
            if 'ocr-pull-discussions.py' not in cmd:
                continue
            ts = e.get('timestamp') or msg.get('timestamp')
            # tokenize: MR id = numeric token right after the script name
            toks = cmd.replace('\n', ' ').split()
            mr = None
            for i, t in enumerate(toks):
                if t.endswith('ocr-pull-discussions.py'):
                    rest = toks[i+1:i+3]
                    for r in rest:
                        if re.fullmatch(r'\d+', r):
                            mr = r
                            break
                    break
            mode = 'digest' if '--digest' in cmd else 'full'
            out.append({
                'session_file': f,
                'ts': ts,
                'mr': mr,
                'mode': mode,
                'cmd': cmd[:300],
            })
json.dump(out, open(os.path.join(OUT_DIR, 'pull-invocations.json'), 'w'), ensure_ascii=False, indent=1)
# summary
from collections import Counter
mrs = Counter(i['mr'] for i in out if i['mr'])
print('total invocations:', len(out))
print('distinct MR ids:', len(mrs))
for mr, n in mrs.most_common(30):
    print(f'  {mr}: {n}')
