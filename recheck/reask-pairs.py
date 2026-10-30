import json, glob, os
KEYS = ["重新问问题","重新问我问题","重新问它","重新问 Q","不对 Q5 需要重新问","看不懂你的问题"]
pairs=[]
for fp in glob.glob(os.path.expanduser("~/.pi/agent/sessions/*/*.jsonl")):
    try: lines=open(fp,errors="replace").readlines()
    except: continue
    entries=[]
    for l in lines:
        try: entries.append(json.loads(l))
        except: entries.append(None)
    def role_text(e):
        if not e: return None,None
        m=e.get("message",e); r=m.get("role"); c=m.get("content")
        if isinstance(c,str): t=c
        elif isinstance(c,list):
            parts=[]
            for b in c:
                if isinstance(b,dict):
                    if b.get("type")=="text": parts.append(b.get("text",""))
                    elif b.get("type")=="toolCall" and b.get("name") in ("ask_user","contact_supervisor"):
                        a=b.get("arguments",{})
                        parts.append("<<ASK_USER "+json.dumps(a.get("questions",a),ensure_ascii=False)[:1500]+">>")
            t="\n".join(parts)
        else: t=""
        return r,t
    for i,e in enumerate(entries):
        r,t=role_text(e)
        if r!="user" or not t: continue
        if any(k in t for k in KEYS):
            # preceding assistant message(s) with question
            prev=[]
            for j in range(i-1,max(0,i-8),-1):
                r2,t2=role_text(entries[j])
                if r2=="assistant" and t2.strip():
                    prev.append(t2[:1500]); 
                    if len(prev)>=1: break
            # following assistant re-ask
            post=[]
            for j in range(i+1,min(len(entries),i+15)):
                r2,t2=role_text(entries[j])
                if r2=="assistant" and ("<<ASK_USER" in t2 or "?" in t2):
                    post.append(t2[:1800]); break
            pairs.append({"file":os.path.basename(fp),"trigger":t.strip()[:150],"before":"\n<<<\n".join(reversed(prev)),"after":"\n".join(post)})
json.dump(pairs,open("reask-pairs.json","w"),ensure_ascii=False,indent=1)
print(len(pairs),"pairs")
