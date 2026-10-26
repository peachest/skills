#!/usr/bin/env python3
"""Analyze triage review-round data: findings per round, TP/FP mix,
priority mix, convergence, diff-size vs review-rounds curve."""
import json, os, re, glob, math
from collections import defaultdict, Counter

DATA = os.path.join(os.environ.get('TRIAGE_ROUNDS_OUT', os.path.expanduser('~/tmp/triage-rounds')), 'data')
OUT = os.environ.get('TRIAGE_ROUNDS_OUT', os.path.expanduser('~/tmp/triage-rounds'))

FINDING_RE = re.compile(r'^\[(?P<cat>[^·\]]+?)\s*·\s*(?P<pri>[^\]]+?)\]')
VERDICT_RE = re.compile(r'###\s*(✅|❌|🟡|🔵|⏸️)|更正分类[:：]\s*(✅|❌|🟡|🔵|⏸️)')
EMOJI_CLS = {'✅': 'TP', '❌': 'FP', '🟡': 'Edge', '🔵': 'OOS', '⏸️': 'Q'}

# mirror ocr-pull-discussions.py's junk filters (canonical finding definition)
JUNK_BODIES = {"changed this line", "changed the description", "nouse",
               "test discussion", "line-ending test", "test discc", "header test",
               "Test discussion", "inline test L57", "inline test ocr-review.yml L30"}
JUNK_PREFIXES = ("changed this line", "**PR Description**", "**[Persistent review]",
                 "## PR Reviewer", "Added 1 commit")
SYSTEM_RE = re.compile(r'^(mentioned in commit|added \d+ commit|assigned to|marked this|resolved all threads|changed \d+ lines?|approved this|unapproved this)')

def is_finding(root):
    body = (root.get('body') or '').strip()
    if root.get('system') or not body:
        return False
    if body in JUNK_BODIES or body.startswith(JUNK_PREFIXES):
        return False
    if body.startswith(('🔍', '✅', '⚠️')) or SYSTEM_RE.match(body):
        return False
    return True

findings = []
mr_meta = []
for fn in sorted(glob.glob(os.path.join(DATA, '*.json'))):
    rec = json.load(open(fn))
    key = f"{rec['project']}!{rec['mr']}"
    ds = rec.get('diff_stats') or {}
    meta = {
        'key': key, 'project': rec['project'], 'mr': rec['mr'],
        'title': rec.get('title'), 'state': rec.get('state'),
        'additions': ds.get('additions'), 'deletions': ds.get('deletions'),
        'files': ds.get('file_count') or rec.get('changes_count'),
        'n_commits': rec.get('n_commits'), 'n_pipelines': rec.get('n_pipelines'),
    }
    mr_meta.append(meta)
    for disc in rec.get('discussions', []):
        notes = disc.get('notes', [])
        if not notes:
            continue
        root = notes[0]
        if not is_finding(root):
            continue
        m = FINDING_RE.match(root.get('body') or '')
        pos = root.get('position') or {}
        # collect verdicts anywhere in the thread
        verdicts = []
        for n in notes[1:] + ([root] if VERDICT_RE.search(root.get('body') or '') else []):
            vm = VERDICT_RE.search(n.get('body') or '')
            if vm:
                emo = vm.group(1) or vm.group(2)
                verdicts.append({'ts': n.get('created_at'), 'cls': EMOJI_CLS[emo]})
        verdicts.sort(key=lambda v: v['ts'] or '')
        findings.append({
            'key': key, 'discussion': disc.get('id'),
            'round_sha': pos.get('head_sha'),
            'created_at': root.get('created_at'),
            'category': (m.group('cat') or '').strip() if m else '',
            'priority': (m.group('pri') or '').strip().lower() if m else '',
            'final_cls': verdicts[-1]['cls'] if verdicts else None,
            'n_verdicts': len(verdicts),
        })

json.dump(findings, open(os.path.join(OUT, 'findings.json'), 'w'), ensure_ascii=False, indent=1)
json.dump(mr_meta, open(os.path.join(OUT, 'mr-meta.json'), 'w'), ensure_ascii=False, indent=1)

# ---- per-MR rounds ----
per_mr = defaultdict(lambda: defaultdict(list))
for f in findings:
    per_mr[f['key']][f['round_sha'] or 'UNANCHORED'].append(f)

mr_stats = []
for meta in mr_meta:
    rounds_map = per_mr.get(meta['key'], {})
    n_unanch = len(rounds_map.get('UNANCHORED', []))
    rl = []
    for sha, fs in rounds_map.items():
        if sha == 'UNANCHORED':
            continue
        fs_sorted = sorted(fs, key=lambda f: f['created_at'] or '')
        rl.append({
            'sha': sha[:8], 'n': len(fs),
            'first': fs_sorted[0]['created_at'],
            'cls': dict(Counter(f['final_cls'] or 'unanswered' for f in fs)),
            'pri': dict(Counter(f['priority'] for f in fs)),
        })
    rl.sort(key=lambda r: r['first'] or '')
    for i, r in enumerate(rl, 1):
        r['round'] = i
    mr_stats.append({**meta, 'rounds': rl,
                     'n_rounds_with_findings': len(rl),
                     'n_findings': sum(r['n'] for r in rl) + n_unanch,
                     'n_unanchored': n_unanch,
                     })
json.dump(mr_stats, open(os.path.join(OUT, 'mr-stats.json'), 'w'), ensure_ascii=False, indent=1)

# ---- aggregate curves ----
print('=== per-MR overview (sorted by findings) ===')
print(f"{'MR':<45} {'files':>5} {'+/-':>7} {'cmt':>4} {'ci':>3} {'rounds':>6} {'finds':>5}")
for m in sorted(mr_stats, key=lambda m: -m['n_findings']):
    chg = (m['additions'] or 0) + (m['deletions'] or 0)
    print(f"{m['key']:<45} {str(m['files']):>5} {chg:>7} {str(m['n_commits']):>4} {str(m['n_pipelines']):>3} {m['n_rounds_with_findings']:>6} {m['n_findings']:>5}")

# normalized round-index decay
maxr = max(len(m['rounds']) for m in mr_stats)
print('\n=== findings per round index (all MRs, anchored rounds only) ===')
print(f"{'round':>5} {'mrs_active':>10} {'findings':>8} {'TP':>4} {'FP':>4} {'Edge':>5} {'OOS':>4} {'Q':>3} {'unans':>6} {'hi':>3} {'med':>4} {'low':>4}")
for r in range(1, maxr + 1):
    active = [m for m in mr_stats if len(m['rounds']) >= r]
    fs = [f for m in active for f in m['rounds'][r-1] and m['rounds'][r-1]['cls'].items() for _ in range(f[1])]
    cls = Counter()
    for m in active:
        cls.update(m['rounds'][r-1]['cls'])
    pri = Counter()
    for m in active:
        pri.update({k: v for k, v in m['rounds'][r-1]['pri'].items() if k in ('high', 'medium', 'low', 'critical')})
    tot = sum(cls.values())
    print(f"{r:>5} {len(active):>10} {tot:>8} {cls.get('TP',0):>4} {cls.get('FP',0):>4} {cls.get('Edge',0):>5} "
          f"{cls.get('OOS',0):>4} {cls.get('Q',0):>3} {cls.get('unanswered',0):>6} "
          f"{pri.get('high',0)+pri.get('critical',0):>3} {pri.get('medium',0):>4} {pri.get('low',0):>4}")

# diff-size vs rounds buckets
print('\n=== diff size (added+deleted lines) vs review rounds with findings ===')
def bucket(chg):
    if chg is None: return 'unknown'
    for b in ((0,50),(50,150),(150,400),(400,1000),(1000,3000),(3000,10**9)):
        if b[0] <= chg < b[1]:
            return f'{b[0]}-{b[1] if b[1]<10**9 else "+"}'
    return 'unknown'
buckets = defaultdict(list)
for m in mr_stats:
    chg = (m['additions'] or 0) + (m['deletions'] or 0)
    buckets[bucket(chg)].append(m)
print(f"{'lines':>12} {'#MR':>4} {'median_rounds':>13} {'mean_rounds':>11} {'median_finds':>12} {'median_commits':>14}")
for b in ['0-50','50-150','150-400','400-1000','1000-3000','3000+','unknown']:
    ms = buckets.get(b, [])
    if not ms: continue
    rs = sorted(m['n_rounds_with_findings'] for m in ms)
    fds = sorted(m['n_findings'] for m in ms)
    cs = sorted((m['n_commits'] or 0) for m in ms)
    med = lambda a: a[len(a)//2] if a else None
    mean_r = sum(rs)/len(rs)
    print(f"{b:>12} {len(ms):>4} {med(rs):>13} {mean_r:>11.1f} {med(fds):>12} {med(cs):>14}")

# correlation
import statistics
xs, ys = [], []
for m in mr_stats:
    chg = (m['additions'] or 0) + (m['deletions'] or 0)
    if chg and m['n_rounds_with_findings']:
        xs.append(chg); ys.append(m['n_rounds_with_findings'])
if len(xs) > 2:
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    r = cov / math.sqrt(sum((x-mx)**2 for x in xs) * sum((y-my)**2 for y in ys))
    print(f'\nPearson r (diff lines vs rounds with findings): n={len(xs)} r={r:.3f}')
    xs2, ys2 = [m['files'] for m in mr_stats if m['files']], [m['n_rounds_with_findings'] for m in mr_stats if m['files']]
    mx, my = statistics.mean(xs2), statistics.mean(ys2)
    cov = sum((x-mx)*(y-my) for x,y in zip(xs2,ys2))
    r2 = cov / math.sqrt(sum((x-mx)**2 for x in xs2) * sum((y-my)**2 for y in ys2))
    print(f'Pearson r (files vs rounds with findings): n={len(xs2)} r={r2:.3f}')
print('\ntotal findings:', len(findings), '| anchored:', sum(1 for f in findings if f['round_sha']))
