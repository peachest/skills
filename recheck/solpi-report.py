import json, os, glob, re, statistics
from collections import defaultdict

ROOT = os.path.expanduser("~/.pi/agent/sessions")
HANDLE_TOKENS = 1000  # 2048+1536 bytes ~ rough token estimate for the handle
af_sessions = defaultdict(int)
rows = []

for proj in sorted(os.listdir(ROOT)):
    pdir = os.path.join(ROOT, proj)
    if not os.path.isdir(pdir): continue
    solpi_ids = set(os.listdir(os.path.join(pdir, "sol-pi"))) if os.path.isdir(os.path.join(pdir, "sol-pi")) else set()
    for f in glob.glob(os.path.join(pdir, "*.jsonl")):
        m = re.search(r'_(\d{8}-\d{4})?Z?_?([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', os.path.basename(f))
        if not m: continue
        sid = m.group(2)
        date = os.path.basename(f)[:10]
        has_solpi = sid in solpi_ids
        tokens = {"input":0,"output":0,"cacheRead":0,"cacheWrite":0}
        n_req = 0; af_used = 0
        try:
            for line in open(f):
                if "then_run" in line:
                    # actual usage = args of toolCall, not schema; schema lines contain "required"
                    if '"then_run":{"command"' in line or '"then_run":{"command":' in line.replace(" ",""):
                        af_used += line.count('"then_run":{"command"')
                try: e = json.loads(line)
                except: continue
                msg = e.get("message") or {}
                u = msg.get("usage")
                if msg.get("role") == "assistant" and u:
                    n_req += 1
                    for k in tokens: tokens[k] += u.get(k,0) or 0
        except Exception: continue
        obs_tokens = 0; obs_count = 0
        if has_solpi:
            led = os.path.join(pdir,"sol-pi",sid,"observation-pack","ledger.jsonl")
            if os.path.exists(led):
                for line in open(led):
                    try:
                        e = json.loads(line)
                        if e.get("originalTokens"): obs_tokens += e["originalTokens"]; obs_count += 1
                    except: pass
        if af_used: af_sessions[(proj,sid)] = af_used
        rows.append(dict(proj=proj, date=date, sid=sid, has_solpi=has_solpi, n_req=n_req,
                         total=tokens["input"]+tokens["output"]+tokens["cacheRead"]+tokens["cacheWrite"],
                         **tokens, obs_tokens=obs_tokens, obs_count=obs_count, af_used=af_used))

# sol-pi sessions = any with archive or af usage
sp = [r for r in rows if r["has_solpi"] or r["af_used"]]
base = [r for r in rows if not (r["has_solpi"] or r["af_used"]) and r["n_req"]>5]

def med(rs,k): 
    v=[r[k] for r in rs if r[k]>0]; return statistics.median(v) if v else 0

print(f"sessions total={len(rows)}  solpi-active={len(sp)}  baseline(large)={len(base)}")
print(f"solpi sessions date range: {min([r['date'] for r in sp]) if sp else '-'} .. {max([r['date'] for r in sp]) if sp else '-'}")
print()
print("== per sol-pi session ==")
for r in sorted(sp, key=lambda x:x["date"]):
    print(f"{r['date']} {r['proj'][:40]:42s} req={r['n_req']:4d} in={r['input']:>10,} out={r['output']:>8,} cacheR={r['cacheRead']:>12,} obs_arch={r['obs_tokens']:>7,}/{r['obs_count']} af={r['af_used']}")
print()
print("== mechanism savings estimates ==")
tot_obs = sum(r["obs_tokens"] for r in sp)
n_obs = sum(r["obs_count"] for r in sp)
# rough replay saving: for each session, obs_tokens saved per request after archive
replay_saved = 0
for r in sp:
    if r["obs_count"] and r["n_req"] > 1:
        replay_saved += (r["obs_tokens"]/max(r["obs_count"],1)) * max(r["n_req"]-1,0) - HANDLE_TOKENS*max(r["n_req"]-1,0)
print(f"Observation Pack: {n_obs} observations archived, {tot_obs:,} tokens pulled out of replay")
print(f"  rough replay saving ≈ {int(max(replay_saved,0)):,} tokens (archived tokens re-sent per later request, minus ~{HANDLE_TOKENS}/req handle cost)")
print(f"Action Fusion: {sum(r['af_used'] for r in sp)} fused edit/write+command turns saved (1 model call each)")
print()
print("== baseline comparison (sessions >5 req, no solpi) ==")
if base:
    print(f"median per-session: in={int(med(base,'input')):,} out={int(med(base,'output')):,} cacheR={int(med(base,'cacheRead')):,} req={int(med(base,'n_req'))}")
    spl = [r for r in sp if r["n_req"]>5]
    if spl:
        print(f"solpi per-session median: in={int(med(spl,'input')):,} out={int(med(spl,'output')):,} cacheR={int(med(spl,'cacheRead')):,} req={int(med(spl,'n_req'))}")
