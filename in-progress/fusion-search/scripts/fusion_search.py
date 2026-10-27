#!/usr/bin/env python3
"""fusion-search: two-lane recall (anysearch + DeepSeek Search) -> dedupe -> RRF -> judge rerank -> top-k.

Single entry point. Exit codes: 0 both lanes ok, 2 one lane failed, 3 nothing usable.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

SKILL_DIR = Path(__file__).resolve().parent.parent
K_RRF = 60
TRUNC = 180
JUDGE_SCORES_RE = re.compile(r'\{.*\}', re.S)

EXIT_OK, EXIT_PARTIAL, EXIT_DEAD = 0, 2, 3


def load_config():
    """runtime.conf (KEY=VALUE) -> dict, overridable by environment."""
    cfg = {}
    conf = SKILL_DIR / 'runtime.conf'
    if conf.exists():
        for line in conf.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, _, v = line.partition('=')
                cfg[k.strip()] = v.strip()
    cfg['DEEPSEEK_SEARCH_URL'] = os.environ.get('DEEPSEEK_SEARCH_URL', cfg.get(
        'DEEPSEEK_SEARCH_URL', 'https://api.deepseek.com/v1/tools/search'))
    cfg['ANYSEARCH_CLI'] = os.environ.get('ANYSEARCH_CLI', cfg.get('ANYSEARCH_CLI')
        or str(Path.home() / '.agents/skills/anysearch/scripts/anysearch_cli.py'))
    cfg['JUDGE_URL'] = os.environ.get('JUDGE_URL', cfg.get('JUDGE_URL', ''))
    cfg['JUDGE_MODEL'] = os.environ.get('JUDGE_MODEL', cfg.get('JUDGE_MODEL', ''))
    cfg['JUDGE_REQUEST_EXTRA'] = os.environ.get('JUDGE_REQUEST_EXTRA', cfg.get(
        'JUDGE_REQUEST_EXTRA', '{}'))
    return cfg


def clean_q(q):
    return ' '.join(q.replace('\\', ' ').split()).strip()


def norm_url(u):
    if not u:
        return ''
    p = urlparse(u)
    return (p.netloc.replace('www.', '') + p.path.rstrip('/')).lower()


def anysearch_lane(cli, query, retry=2, python='/usr/bin/python3'):
    t0 = time.time()
    for attempt in range(retry + 1):
        try:
            r = subprocess.run([python, cli,
                                'search', query, '--max_results', '10'],
                               capture_output=True, text=True, timeout=90)
            docs, block = [], None
            for line in r.stdout.splitlines():
                if line.startswith('### '):
                    if block:
                        docs.append(block)
                    block = {'title': re.sub(r'^\d+\.\s*', '', line[4:].strip()), 'url': '', 'text': ''}
                elif block is not None:
                    if '**URL**:' in line and not block['url']:
                        block['url'] = line.split('**URL**: ')[1].split()[0].strip()
                    elif line.startswith('- ') and not line.startswith('- **'):
                        block['text'] += line[2:].strip() + ' '
            if block:
                docs.append(block)
            docs = [d for d in docs if d['url']]
            if docs:
                return {'docs': docs, 'latency': round(time.time() - t0, 1), 'ok': True, 'err': ''}
            if attempt == retry:
                break
        except Exception as e:
            if attempt == retry:
                return {'docs': [], 'latency': round(time.time() - t0, 1), 'ok': False,
                        'err': f'anysearch: {str(e)[:120]}'}
        time.sleep(3 * (attempt + 1))
    return {'docs': [], 'latency': round(time.time() - t0, 1), 'ok': False,
            'err': 'anysearch: empty after retries (check skill installed: %s)' % cli}


def deepseek_lane(cfg, query, retry=2):
    t0 = time.time()
    key = os.environ.get('DEEPSEEK_API_KEY', '')
    if not key:
        return {'docs': [], 'latency': round(time.time() - t0, 1), 'ok': False,
                'err': 'deepseek: DEEPSEEK_API_KEY not set'}
    for attempt in range(retry + 1):
        try:
            req = urllib.request.Request(
                cfg['DEEPSEEK_SEARCH_URL'],
                data=json.dumps({'query': query[:128], 'count': 10, 'need_content': False}).encode(),
                headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
            body = json.load(urllib.request.urlopen(req, timeout=30))
            docs = [{'title': it.get('title', ''), 'url': it.get('url', ''),
                     'text': (it.get('summary') or it.get('snippet') or '')[:TRUNC],
                     'ds_score': it.get('rerank_score')} for it in body.get('results', [])]
            if docs:
                return {'docs': docs, 'latency': round(time.time() - t0, 1), 'ok': True, 'err': ''}
            if attempt == retry:  # genuine empty (e.g. site: deep path) — no more retries
                return {'docs': [], 'latency': round(time.time() - t0, 1), 'ok': False,
                        'err': 'deepseek: engine returned 0 results'}
        except Exception as e:
            if attempt == retry:
                return {'docs': [], 'latency': round(time.time() - t0, 1), 'ok': False,
                        'err': f'deepseek: {str(e)[:120]}'}
        time.sleep(2 * (attempt + 1))
    return {'docs': [], 'latency': round(time.time() - t0, 1), 'ok': False,
            'err': 'deepseek: empty after retries'}


def judge_scores(cfg, query, cands, retry=2):
    """cands: [{cid, title, text}] -> ({cid: 0-3}, usage)."""
    if not (cfg['JUDGE_URL'] and cfg['JUDGE_MODEL']):
        return {}, {'error': 'judge not configured (JUDGE_URL/JUDGE_MODEL)'}
    listing = '\n'.join(f"{c['cid']} {c['title'][:90]} :: {c['text'][:TRUNC]}" for c in cands)
    prompt = (f"Query: {query}\n\nRate each search result's relevance to the query: "
              f"3=directly answers it, 2=helpful, 1=tangential, 0=irrelevant.\n\n{listing}\n\n"
              'Reply ONLY JSON: {"scores": {"<cid>": <0-3>, ...}}')
    payload = {'model': cfg['JUDGE_MODEL'],
               'messages': [{'role': 'user', 'content': prompt}],
               'temperature': 0, 'max_tokens': 4000}
    try:
        payload.update(json.loads(cfg['JUDGE_REQUEST_EXTRA']))
    except Exception:
        pass
    for attempt in range(retry + 1):
        try:
            req = urllib.request.Request(cfg['JUDGE_URL'],
                data=json.dumps(payload).encode(),
                headers={'Content-Type': 'application/json'})
            body = json.load(urllib.request.urlopen(req, timeout=90))
            content = (body['choices'][0]['message'].get('content') or '').strip()
            data = json.loads(JUDGE_SCORES_RE.search(content).group(0) if JUDGE_SCORES_RE.search(content) else content)
            return {str(k): float(v) for k, v in data.get('scores', {}).items()}, body.get('usage', {})
        except Exception:
            if attempt == retry:
                return {}, {'error': f'judge failed after retries: query too long or endpoint down'}
            time.sleep(2)
    return {}, {}


def fuse(a, d):
    """Merge lanes, tag consensus, compute RRF. Returns (merged, cands)."""
    for src, res in (('A', a), ('D', d)):
        for doc in res['docs']:
            doc['source'] = src
            doc['_key'] = norm_url(doc['url'])
            doc['text'] = (doc.get('text') or '')[:TRUNC]
    merged, seen = [], set()
    for res in (d, a):  # DS first: keeps ds_score on deduped docs
        for doc in res['docs']:
            k = doc['_key']
            if k and k not in seen:
                seen.add(k)
                merged.append(doc)
            elif k in seen and doc['source'] == 'A':
                for m in merged:
                    if m['_key'] == k:
                        m['both'] = True
    rrf = {}
    for res in (a, d):
        for rank, doc in enumerate(res['docs']):
            rrf[doc['_key']] = rrf.get(doc['_key'], 0) + 1.0 / (K_RRF + rank + 1)
    cands = []
    for src, res in (('A', a), ('D', d)):
        for i, doc in enumerate(res['docs']):
            doc['cid'] = f'{src}{i}'
            cands.append(doc)
    for m in merged:
        m['rrf'] = round(rrf.get(m['_key'], 0), 5)
        m['cid'] = next(c['cid'] for c in cands if c['_key'] == m['_key'])
    return merged, cands


def mean(vals):
    vals = [v for v in vals if v is not None]
    return round(sum(vals) / len(vals), 2) if vals else None


def run_query(cfg, query, top_k=5):
    a = anysearch_lane(cfg['ANYSEARCH_CLI'], clean_q(query),
                       python=cfg.get('ANYSEARCH_PYTHON', '/usr/bin/python3'))
    d = deepseek_lane(cfg, clean_q(query))
    merged, cands = fuse(a, d)
    scores, usage = judge_scores(cfg, clean_q(query), cands)
    score_by_key = {}
    for doc in cands:
        doc['llm'] = scores.get(doc['cid'])
        score_by_key[doc['_key']] = doc['llm']
    top = sorted(merged, key=lambda x: (score_by_key.get(x['_key']) is None,
                                        -(score_by_key.get(x['_key']) or 0), -x['rrf']))[:top_k]

    def lane_rel(res):
        vals = [score_by_key.get(doc['_key']) for doc in res['docs'][:5]]
        return mean([v for v in vals if v is not None])

    ok_lanes = sum(1 for r in (a, d) if r['ok'])
    return {
        'query': clean_q(query),
        'degraded': ok_lanes < 2,
        'lanes': {'anysearch': {k: a[k] for k in ('ok', 'latency', 'err')} | {'n': len(a['docs'])},
                  'deepseek': {k: d[k] for k in ('ok', 'latency', 'err')} | {'n': len(d['docs'])}},
        'judge': {'model': cfg['JUDGE_MODEL'], 'usage': usage},
        'n_merged': len(merged),
        'top': [{'title': t['title'][:70], 'url': t['url'][:100], 'src': t['source'],
                 'both': t.get('both', False), 'rrf': t['rrf'],
                 'llm': score_by_key.get(t['_key']), 'ds_score': t.get('ds_score')} for t in top],
        'rel': {'fused': mean([t['llm'] for t in top]), 'anysearch': lane_rel(a), 'deepseek': lane_rel(d)},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('query', nargs='?', help='search query')
    ap.add_argument('--batch', help='file with one query per line')
    ap.add_argument('--out', help='JSON output path (single query)')
    ap.add_argument('--out-dir', help='JSON output directory (batch)')
    ap.add_argument('--top-k', type=int, default=5)
    args = ap.parse_args()
    if not args.query and not args.batch:
        ap.error('query or --batch required')

    cfg = load_config()
    missing = [k for k in ('JUDGE_URL', 'JUDGE_MODEL') if not cfg[k]]
    if missing:
        print(f'FAIL: judge not configured ({", ".join(missing)}) — see runtime.conf.example', file=sys.stderr)
        sys.exit(EXIT_DEAD)

    queries = ([l.strip() for l in Path(args.batch).read_text().splitlines() if l.strip()]
               if args.batch else [args.query])
    results = []
    for q in queries:
        rec = run_query(cfg, q, args.top_k)
        results.append(rec)
        t = rec['top'][0] if rec['top'] else None
        print(f"[{rec['query'][:50]}] fused={rec['rel']['fused']} "
              f"any={rec['rel']['anysearch']} ds={rec['rel']['deepseek']}"
              f"{' DEGRADED: ' + (rec['lanes']['anysearch']['err'] or rec['lanes']['deepseek']['err']) if rec['degraded'] else ''}")
        for i, item in enumerate(rec['top'], 1):
            tag = 'both' if item['both'] else item['src']
            print(f"  {i}. [{tag} llm={item['llm']}] {item['title'][:70]}")
            print(f"     {item['url']}")

    exit_code = EXIT_OK
    if args.batch:
        out_dir = Path(args.out_dir or '.')
        out_dir.mkdir(parents=True, exist_ok=True)
        for rec in results:
            slug = re.sub(r'[^\w\u4e00-\u9fff]+', '-', rec['query'])[:50].strip('-') or 'query'
            (out_dir / f'{slug}.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1))
            if rec['degraded']:
                exit_code = EXIT_PARTIAL
            if not rec['top']:
                exit_code = EXIT_DEAD
    else:
        rec = results[0]
        out = Path(args.out) if args.out else None
        if out:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(rec, ensure_ascii=False, indent=1))
            print(f'JSON: {out}')
        exit_code = EXIT_DEAD if not rec['top'] else (EXIT_PARTIAL if rec['degraded'] else EXIT_OK)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
