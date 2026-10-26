#!/usr/bin/env python3
"""Collect per-MR ground truth v2 — resolve via session-voted remote URL first.
remote URL -> (host, project path) mapping; probe that project only.
Fallback: scan candidates. Output: ~/tmp/triage-rounds/data/*.json
"""
import json, os, re, subprocess
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT = '/mnt/disk1/hyx/tmp/triage-rounds/data'
os.makedirs(OUT, exist_ok=True)

URL_MAP = {
    '<repo-a>': ('gitlab.example.com', '<group>/<project>'),
    'device-plugin-example': ('gitlab.example.com', '<group>/<project>'),
    '<repo-b>': ('gitlab.example.com', '<group>/<project>'),
    'charts-example': ('gitlab.example.com', '<group>/<project>'),
    'images-example': ('gitlab.example.com', '<group>/<project>'),
    'expense-example': ('gitlab.example.com', '<group>/<project>'),
    'serving-example': ('gitlab.example.com', '<group>/<project>'),
    'hami': ('gitlab.example.com', '<group>/<project>'),
    'scheduler-fork-example': ('gitlab.example.com', '<group>/<project>'),
    'cost-controller-example': ('gitlab.example.com', '<group>/<project>'),
    'sglang': ('gitlab.example.com', '<group>/<project>'),
    '<repo-b>': ('gitlab.example.com', '<group>/<project>'),
}
SCAN = [
    ('gitlab.example.com', p) for p in [
        '<group>/<project>', '<group>/<project>',
        '<group>/<project>', '<group>/<project>',
        '<group>/<project>', '<group>/<project>', '<group>/<project>',
        '<group>/<project>', '<group>/<project>']] + [
    ('gitlab.example.com', p) for p in [
        '<group>/<project>',
        '<group>/<project>', '<group>/<project>']]

def url_to_candidate(url):
    if not url:
        return None
    name = re.sub(r'\.git$', '', url.rstrip('/').split('/')[-1]).lower()
    return URL_MAP.get(name)

def glab(endpoint, host):
    r = subprocess.run(['glab', 'api', '--hostname', host, endpoint],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None

def fetch_all_discussions(esc, iid, host):
    out, page = [], 1
    while True:
        d = glab(f'projects/{esc}/merge_requests/{iid}/discussions?per_page=100&page={page}', host)
        if not d:
            break
        out.extend(d)
        if len(d) < 100 or page > 20:
            break
        page += 1
    return out

# rebuild votes per MR from invocations + session cwd -> remote resolution
inv = json.load(open('/mnt/disk1/hyx/tmp/triage-rounds-pull-invocations.json'))
cwd_cache = {}
def session_cwd(f):
    if f in cwd_cache: return cwd_cache[f]
    cwd = None
    try:
        with open(f, 'rb') as fh:
            for line in fh:
                if b'"cwd"' not in line: continue
                e = json.loads(line)
                cwd = e.get('cwd') or (e.get('message') or {}).get('cwd')
                if cwd: break
    except OSError: pass
    cwd_cache[f] = cwd
    return cwd

import urllib.parse
def remote_of(cwd):
    if not cwd or not os.path.isdir(cwd):
        return None
    try:
        return subprocess.run(['git', '-C', cwd, 'remote', 'get-url', 'origin'],
                              capture_output=True, text=True, timeout=5).stdout.strip() or None
    except Exception:
        return None

votes = defaultdict(Counter)   # mr -> candidate(host,proj) -> votes
for i in inv:
    if not i['mr']:
        continue
    cwd = session_cwd(i['session_file'])
    cand = url_to_candidate(remote_of(cwd))
    if cand:
        votes[i['mr']][cand] += 1

def collect(mr):
    tried, resolved = [], None
    ordered = sorted(votes.get(mr, {}).items(), key=lambda x: -x[1])
    for (host, proj), _ in ordered:
        info = glab(f'projects/{proj.replace("/","%2F")}/merge_requests/{mr}?with_stats=true', host)
        if info and isinstance(info, dict) and info.get('iid') == int(mr):
            resolved = (host, proj, info); break
    if not resolved:  # fallback scan
        for host, proj in SCAN:
            info = glab(f'projects/{proj.replace("/","%2F")}/merge_requests/{mr}?with_stats=true', host)
            if info and isinstance(info, dict) and info.get('iid') == int(mr):
                resolved = (host, proj, info); break
    if not resolved:
        return mr, None, 'unresolved'
    host, proj, info = resolved
    esc = proj.replace('/', '%2F')
    commits = glab(f'projects/{esc}/merge_requests/{mr}/commits?per_page=100', host) or []
    pipelines = glab(f'projects/{esc}/merge_requests/{mr}/pipelines?per_page=100', host) or []
    discs = fetch_all_discussions(esc, mr, host)
    rec = {
        'mr': int(mr), 'host': host, 'project': proj,
        'title': info.get('title'), 'state': info.get('state'),
        'created_at': info.get('created_at'), 'merged_at': info.get('merged_at'),
        'diff_stats': info.get('diff_stats'), 'changes_count': info.get('changes_count'),
        'n_commits': len(commits) if isinstance(commits, list) else None,
        'n_pipelines': len(pipelines) if isinstance(pipelines, list) else None,
        'n_discussions': len(discs), 'discussions': discs,
    }
    json.dump(rec, open(os.path.join(OUT, f"{proj.replace('/','__')}__mr{mr}.json"), 'w'), ensure_ascii=False)
    return mr, proj, 'ok'

mrs = sorted({i['mr'] for i in inv if i['mr']}, key=int)
results = []
with ThreadPoolExecutor(max_workers=4) as ex:
    futs = {ex.submit(collect, m): m for m in mrs}
    for f in as_completed(futs):
        mr, proj, status = f.result()
        results.append({'mr': mr, 'project': proj, 'status': status})
        print(f'!{mr} -> {proj} [{status}]', flush=True)

json.dump(results, open('/mnt/disk1/hyx/tmp/triage-rounds/resolve-log.json', 'w'), ensure_ascii=False, indent=1)
print(f'done: {sum(1 for r in results if r["status"]=="ok")}/{len(mrs)}')
