#!/usr/bin/env python3
"""Second pass: compute exact diff sizes (+/- lines, files) via the changes
endpoint, since with_stats returns nil diff_stats on large MRs.
Updates mr-stats.json in place (additions/deletions/files)."""
import json, os, re, glob, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT = '/mnt/disk1/hyx/tmp/triage-rounds'
DATA = os.path.join(OUT, 'data')

def glab(endpoint, host):
    r = subprocess.run(['glab', 'api', '--hostname', host, endpoint],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None

def diff_size(rec):
    esc = rec['project'].replace('/', '%2F')
    d = glab(f'projects/{esc}/merge_requests/{rec["mr"]}/changes?access_raw_diffs=true', rec['host'])
    if not d or 'changes' not in d:
        return None
    add = dele = 0
    diffs = d['changes'] or []
    for df in diffs:
        for line in (df.get('diff') or '').splitlines():
            if line.startswith('+++') or line.startswith('---'):
                continue
            if line.startswith('+'):
                add += 1
            elif line.startswith('-'):
                dele += 1
    return {'files': len(diffs), 'additions': add, 'deletions': dele}

files = sorted(glob.glob(os.path.join(DATA, '*.json')))
with ThreadPoolExecutor(max_workers=3) as ex:
    futs = {ex.submit(diff_size, json.load(open(fn))): fn for fn in files}
    for f in as_completed(futs):
        fn = futs[f]
        try:
            size = f.result()
        except Exception as e:
            size = None
        rec = json.load(open(fn))
        name = f"{rec['project']}!{rec['mr']}"
        if size:
            rec['diff_stats'] = {**size, 'file_count': size['files']}
            json.dump(rec, open(fn, 'w'), ensure_ascii=False)
            print(f"{name}: +{size['additions']}/-{size['deletions']} files={size['files']}", flush=True)
        else:
            print(f"{name}: FAILED", flush=True)
