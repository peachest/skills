#!/usr/bin/env python3
"""Stratified sample of a frequency-sorted query corpus (extract-queries.py output).

Buckets queries by regex themes, samples proportionally per bucket (min 1),
prefers frequently-asked queries, dedupes near-duplicates by 30-char prefix.
"""
import argparse, json, random, re

ap = argparse.ArgumentParser()
ap.add_argument("--in", dest="inp", required=True, help="extract-queries.py output")
ap.add_argument("--out", required=True, help="sample.json path")
ap.add_argument("--target", type=int, default=30)
ap.add_argument("--seed", type=int, default=42)
ap.add_argument("--buckets", help="JSON file: [[name, regex], ...]; omit for default tech-research buckets")
args = ap.parse_args()

DEFAULT_BUCKETS = [
    ["llm-inference", r"(?i)inference|mlperf|aiperf|genai-perf|servegen|vllm|sglang|ttft|goodput|speculative|prefix cache|router|routellm|semantic-router|token"],
    ["agent-arch", r"(?i)agent|kafka|temporal|langgraph|event|webhook|autogen|n8n|claude.code|codex|copilot|cursor|pi-"],
    ["data-pipeline", r"(?i)datatrove|curator|pii|dataset|crawl|huggingface"],
    ["cost-finance", r"(?i)opencost|cost|etf|index|market|stock|s&p|nasdaq|rebalanc|tco"],
    ["infra-tools", r"(?i)kubernetes|k8s|xvfb|novnc|playwright|container|github|gitlab|argo|helm"],
]
buckets = [(n, re.compile(p)) for n, p in
           (json.load(open(args.buckets)) if args.buckets else DEFAULT_BUCKETS)]

rows = []
for line in open(args.inp, encoding="utf-8"):
    m = re.match(r"\s*(\d+)\s\s(.+)", line.rstrip("\n"))
    if m:
        rows.append((int(m.group(1)), m.group(2)))

def bucket(q):
    for name, pat in buckets:
        if pat.search(q):
            return name
    return "other"

by_b: dict = {}
for n, q in rows:
    by_b.setdefault(bucket(q), []).append((n, q))

total = sum(len(v) for v in by_b.values())
sample = []
for name, items in sorted(by_b.items(), key=lambda kv: -len(kv[0])):
    k = max(1, round(args.target * len(items) / total))
    seen, picked = set(), []
    for n, q in sorted(items, key=lambda x: -x[0]):
        key = re.sub(r"[^a-z0-9 ]", "", q.lower())[:30]
        if key in seen:
            continue
        seen.add(key)
        picked.append(q)
        if len(picked) >= k:
            break
    sample.extend({"bucket": name, "query": q} for q in picked)

print(f"total historical: {total}, buckets: " + ", ".join(f"{k}={len(v)}" for k, v in sorted(by_b.items())))
print(f"sampled: {len(sample)}")
json.dump(sample, open(args.out, "w"), ensure_ascii=False, indent=1)
