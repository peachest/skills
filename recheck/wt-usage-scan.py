# provenance: session 01a15409 (2026-10-19), baseline in recheck/INDEX.md
# verifies: wt usage drift vs 2026-10-19 portrait; exit 0=holding (this script reports, diff manually)
import json, glob, collections, re, sys

cmd_counter = collections.Counter()      # top-level command
full_counter = collections.Counter()     # command + subcommand path
arg_keys = collections.Counter()         # args object keys
flag_counter = collections.Counter()     # flags inside args array
errors_by_cmd = collections.Counter()
total = 0
err_total = 0

def walk(content):
    if isinstance(content, list):
        for c in content:
            yield from walk(c)
    else:
        yield content

sessions = glob.glob('/mnt/disk1/hyx/.pi/agent/sessions/*/*.jsonl')
results_by_id = {}  # per session; reset each file

for path in sessions:
    results_by_id = {}
    try:
        f = open(path, encoding='utf-8', errors='replace')
    except Exception:
        continue
    with f:
        for line in f:
            if '"worktrunk"' not in line:
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue
            msg = entry.get('message') or {}
            role = msg.get('role')
            content = msg.get('content')
            if role == 'assistant':
                for block in walk(content):
                    if isinstance(block, dict) and block.get('type') == 'toolCall' and block.get('name') == 'worktrunk':
                        args = block.get('arguments') or {}
                        total += 1
                        for k in args:
                            arg_keys[k] += 1
                        cmd = args.get('command')
                        rest = args.get('args') or []
                        if cmd:
                            cmd_counter[cmd] += 1
                            if rest:
                                full_counter[f"{cmd} {rest[0]}"] += 1
                            else:
                                full_counter[cmd] += 1
                            results_by_id[block.get('id')] = cmd
                            for tok in rest:
                                if tok.startswith('-'):
                                    flag_counter[tok] += 1
            elif role == 'toolResult' and msg.get('toolName') == 'worktrunk':
                cid = msg.get('toolCallId')
                if msg.get('isError'):
                    err_total += 1
                    cmd = results_by_id.get(cid, '?')
                    errors_by_cmd[cmd] += 1

print(f"total worktrunk toolCall: {total}, errors: {err_total}\n")
print("== top-level command ==")
for c, n in cmd_counter.most_common():
    e = errors_by_cmd.get(c, 0)
    print(f"{n:4d}  (err {e})  {c}")
print("\n== command + first arg ==")
for c, n in full_counter.most_common():
    print(f"{n:4d}  {c}")
print("\n== args keys ==")
for k, n in arg_keys.most_common():
    print(f"{n:4d}  {k}")
print("\n== flags in args ==")
for k, n in flag_counter.most_common(25):
    print(f"{n:4d}  {k}")
