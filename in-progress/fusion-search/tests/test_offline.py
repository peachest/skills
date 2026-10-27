"""Offline tests: fuse(), anysearch output parse, config — no network. Run: uv run --project <skill dir> pytest tests/"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / 'scripts'))
import fusion_search as fs


def test_norm_url():
    assert fs.norm_url('https://www.arxiv.org/abs/1.2/') == 'arxiv.org/abs/1.2'
    assert fs.norm_url('http://X.org') == 'x.org'
    assert fs.norm_url('') == ''


def test_clean_q():
    assert fs.clean_q('  a  b\\ c  ') == 'a b c'


def test_fuse_dedupe_and_consensus():
    a = {'docs': [{'title': 'x', 'url': 'https://a.com/p', 'text': 'a'},
                  {'title': 'y', 'url': 'https://b.com/p', 'text': 'b'}]}
    d = {'docs': [{'title': 'x2', 'url': 'https://a.com/p', 'text': 'a2',
                   'ds_score': 2.0},
                  {'title': 'z', 'url': 'https://c.com/p', 'text': 'c',
                   'ds_score': 1.0}]}
    merged, cands = fs.fuse(a, d)
    keys = [m['_key'] for m in merged]
    assert len(merged) == 3 and len(set(keys)) == 3
    assert len(cands) == 4  # pre-dedup, per-lane candidates
    both = [m for m in merged if m.get('both')]
    assert len(both) == 1 and both[0]['_key'] == 'a.com/p'
    assert both[0]['ds_score'] == 2.0  # DS copy kept on merge
    assert all('rrf' in m for m in merged)


def test_fuse_rrf_ordering():
    # rank-0 in both lanes must outrank rank-9 in one lane only
    a = {'docs': [{'title': str(i), 'url': f'https://a{i}.com/', 'text': 't'} for i in range(10)]}
    d = {'docs': [{'title': 'a0-dup', 'url': 'https://a0.com/', 'text': 't', 'ds_score': 1.0}]}
    merged, _ = fs.fuse(a, d)
    top = max(merged, key=lambda m: m['rrf'])
    assert top['_key'] == 'a0.com'


def test_anysearch_parse_fixture():
    out = ("## Search Results (2 results, 99ms)\n"
           "### 1. First Doc\n"
           "- **URL**: https://one.com/x\n"
           "- by Someone — this is the snippet text.\n"
           "- **URL**: https://one.com/x\n"
           "### 2. Second Doc\n"
           "- **URL**: https://two.com/y\n"
           "- body line about the topic.\n")
    import subprocess, types
    fake = types.SimpleNamespace(stdout=out, returncode=0)
    orig = fs.subprocess.run
    fs.subprocess.run = lambda *a, **k: fake
    try:
        res = fs.anysearch_lane('cli', 'q')
    finally:
        fs.subprocess.run = orig
    assert res['ok'] and len(res['docs']) == 2
    assert res['docs'][0]['url'] == 'https://one.com/x'
    assert 'snippet' in res['docs'][0]['text'] and 'topic' in res['docs'][1]['text']


def test_judge_score_parse():
    import types
    resp = {'choices': [{'message': {'content': '{"scores": {"A0": 3, "D1": 2.0}}'}}],
            'usage': {'total_tokens': 10}}
    orig_urlopen = fs.urllib.request.urlopen
    orig_req = fs.urllib.request.Request
    fs.urllib.request.urlopen = lambda *a, **k: types.SimpleNamespace(read=lambda: None, __enter__=lambda s: s, __exit__=lambda s, *a: None)
    # json.load needs a file-like; emulate
    import io
    fs.urllib.request.urlopen = lambda *a, **k: io.BytesIO(__import__('json').dumps(resp).encode())
    try:
        scores, usage = fs.judge_scores(
            {'JUDGE_URL': 'http://x', 'JUDGE_MODEL': 'm', 'JUDGE_REQUEST_EXTRA': '{}'},
            'q', [{'cid': 'A0', 'title': 't', 'text': 'x'}, {'cid': 'D1', 'title': 'u', 'text': 'y'}])
    finally:
        fs.urllib.request.urlopen = orig_urlopen
    assert scores == {'A0': 3.0, 'D1': 2.0} and usage['total_tokens'] == 10
