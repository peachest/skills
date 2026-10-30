import json, glob, os, re
# broadened key set: plain-language + context-supplement signals
KEYS = ["大白话","不要压缩","别压缩","不要用隐喻","不要隐喻","展开说","展开解释","解释清楚","讲清楚","说清楚","看不懂","听不懂","没说清楚","没说清","补充上下文","补充背景","背景信息","隐含信息","隐含的前提","前提说","重新解释","重新说明","人话","太抽象","太术语","什么意思，说","一遍听懂"]
hits=[]
for fp in glob.glob(os.path.expanduser("~/.pi/agent/sessions/*/*.jsonl")):
    try: f=open(fp, errors="replace")
    except: continue
    for line in f:
        if not any(k in line for k in KEYS): continue
        try: e=json.loads(line)
        except: continue
        m=e.get("message",e)
        if m.get("role")!="user": continue
        c=m.get("content")
        if isinstance(c,str): t=c
        elif isinstance(c,list): t=" ".join(x.get("text","") for x in c if isinstance(x,dict) and x.get("type")=="text")
        else: continue
        if t.startswith("<") or t.startswith("["): continue
        matched=[k for k in KEYS if k in t]
        if matched:
            hits.append({"file":os.path.basename(fp),"keys":matched,"text":t.strip()[:400]})
json.dump(hits,open("user-instructions-broad.json","w"),ensure_ascii=False,indent=1)
print(len(hits),"broad hits")
from collections import Counter
cnt=Counter(h["keys"][0] for h in hits)
for k,v in cnt.most_common(20): print(f"  {k}: {v}")
