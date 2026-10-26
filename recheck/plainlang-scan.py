import json, os, re, glob, collections

root = os.path.expanduser('~/.pi/agent/sessions')
patterns = {
    'dabaihua': r'大白话',
    'tongsu-zhibai': r'通俗|直白[点地]|说人话',
    'jieshi-shenme-yisi': r'解释[一下下]|什么意思|啥意思|没听懂|不理解',
    'jiandan-suo': r'简单[来说点解释]|简化|通俗易懂',
    'zhankai-shuyu': r'展开[说一]|术语|概念.{0,6}解释',
}
pushback = r'太.{0,4}(术语|专业|抽象|难懂)|看不懂|听不懂|说简单'
wc = collections.Counter(); samples = collections.defaultdict(list); pushback_hits=[]
files = glob.glob(root+'/*/*.jsonl')
n_user=0
for f in files:
    try:
        for line in open(f, encoding='utf-8', errors='ignore'):
            if '"user"' not in line[:400]: continue
            try: rec=json.loads(line)
            except: continue
            msg=rec.get('message') or rec
            if (msg.get('role') or rec.get('type')) != 'user': continue
            c = msg.get('content')
            if isinstance(c, list):
                c = ' '.join(x.get('text','') for x in c if isinstance(x,dict) and x.get('type')=='text')
            if not isinstance(c,str) or len(c)>4000 or c.startswith('<'): continue
            n_user+=1
            for k,p in patterns.items():
                if re.search(p, c):
                    wc[k]+=1
                    if len(samples[k])<4: samples[k].append((os.path.basename(f)[:14], c[:110].replace('\n',' ')))
            if re.search(pushback, c): pushback_hits.append((os.path.basename(f)[:14], c[:110].replace('\n',' ')))
    except: pass
print(f"session files: {len(files)}, user text msgs scanned: {n_user}")
for k in patterns:
    print(f"\n[{k}] {wc[k]}")
    for s in samples[k][:3]: print('  ', s)
print(f"\n[pushback] {len(pushback_hits)}")
for s in pushback_hits[:6]: print('  ', s)

# denoised: exclude peer dispatch / caller identity echoes and skill-injection bodies
wc2 = collections.Counter(); pb2=[]
for f in files:
    try:
        for line in open(f, encoding='utf-8', errors='ignore'):
            if '"user"' not in line[:400]: continue
            try: rec=json.loads(line)
            except: continue
            msg=rec.get('message') or rec
            if (msg.get('role') or rec.get('type')) != 'user': continue
            c = msg.get('content')
            if isinstance(c, list):
                c = ' '.join(x.get('text','') for x in c if isinstance(x,dict) and x.get('type')=='text')
            if not isinstance(c,str) or len(c)>4000 or c.startswith('<'): continue
            if 'caller identity' in c or c.startswith('/skill:') or '[tasks]' in c: continue
            for k,p in patterns.items():
                if re.search(p, c): wc2[k]+=1
            if re.search(pushback, c): pb2.append(c[:100].replace('\n',' '))
    except: pass
print("== denoised (excl peer dispatches/skill injections) ==")
print(dict(wc2), 'pushback:', len(pb2))
