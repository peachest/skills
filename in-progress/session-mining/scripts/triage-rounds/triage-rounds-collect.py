#!/usr/bin/env python3
"""Collect per-MR ground truth v2 — resolve via session-voted remote URL first.
remote URL -> (host, project path) mapping; probe that project only.
Fallback: scan candidates. Output: ~/tmp/triage-rounds/data/*.json
"""
import json, os, re, subprocess, sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT = os.environ.get('TRIAGE_ROUNDS_OUT', os.path.expanduser('~/tmp/triage-rounds/data'))
os.makedirs(OUT, exist_ok=True)
# Repo->(host, project) mapping is node-specific and NOT tracked (public repo).
# Create url-map.py beside this script: URL_MAP = {repo: (host, project), ...}
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from url_map import URL_MAP
except ImportError:
    sys.exit("FAIL: url-map.py missing beside triage-rounds-collect.py — "
             "copy it from the node-local original (~/tmp/triage-rounds-collect.py "
             "on the mining node) and keep it untracked (contains intranet hosts).")

