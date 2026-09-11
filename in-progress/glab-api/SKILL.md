---
name: glab-api
description: Decision table + verified quirks for driving GitLab via the glab CLI and REST API (gitlab.blue.example/gitlab.red.example). Use whenever creating or updating MRs, querying jobs/pipelines/traces/artifacts, managing branches or API commits, or when a glab/api call fails unexpectedly (silent failures, 400/415, state_event rejected) — instead of hand-writing request code.
---

# glab-api cookbook

Decision table + worked-around quirks for driving GitLab via the `glab` CLI and its REST API. Reach for this whenever you need to query or mutate GitLab (gitlab.blue.example / gitlab.red.example or any instance in `~/.config/glab-cli/config.yml`) — instead of re-deriving commands or hand-writing request code each run.

## Decision ladder

Climb only as high as needed:

1. **`glab` subcommand** — MR create/close/ready/list, issue, repo. Try first.
2. **`glab api`** — single GET/POST/PUT/DELETE. Add `-H "Content-Type: application/json"` whenever a body is sent.
3. **Raw `curl`** — when `glab api` persistently 500/400s on the same call (see quirks table: discussion resolve is the known case). Token: `$(glab config get token --host <host>)`; always `-o` to a file (rtk intercepts stdout curl).
4. **Python + urllib** — only for: retry loops, multi-step orchestration, JSON transformation, concurrency. Use the helper at the bottom.

## Instance selection

Two hosts are configured (`~/.config/glab-cli/config.yml`). Outside a repo clone, always pass the host explicitly:

```bash
glab api --hostname gitlab.blue.example  ...   # platform group lives here
glab api --hostname gitlab.red.example  ...   # legacy-group/* projects live here
glab mr create --repo https://gitlab.red.example/<group>/<proj> ...   # cross-repo, full URL
```

Project paths in API URLs must be URL-encoded: `tos%2Fai-infra%2Finferencex%2Fsglang`. If path resolution 404s, fall back to the numeric project ID (visible in runner pod names `runner-*-project-<ID>-*` or via `glab api "projects/<path>"`).

## Common recipes (glab, no python)

```bash
# Query jobs of a project (jq optional)
glab api --hostname gitlab.red.example "projects/<pid>/jobs?per_page=30" > jobs.json

# Pipeline jobs
glab api --hostname <host> "projects/<pid>/pipelines/<pipe_id>/jobs"

# MR: close / ready / list (these subcommands work where raw API PUTs fail — see quirks)
glab mr close 53 -R https://gitlab.blue.example/team/platform/common-ci
glab mr ready 65 -R <repo-url>

# Update MR description / title (works via API PUT with -f form fields)
glab api --hostname <host> -X PUT "projects/<pid>/merge_requests/<iid>" -f "title=New title"

# Job trace (redirect to file — glab api has NO -o flag)
glab api --hostname <host> "projects/<pid>/jobs/<jid>/trace" > trace.log

# Delete a branch
glab api --hostname <host> -X DELETE "projects/<pid>/repository/branches/<url-encoded-name>"

# Create branch + multi-file atomic commit WITHOUT cloning (API commits endpoint)
python3 -c '...build commit JSON to file...'   # transform content, then:
glab api --hostname <host> -X POST -H "Content-Type: application/json" \
  "projects/<pid>/repository/commits" --input commit.json
# commit.json = {"branch": "...", "commit_message": "...",
#                "actions": [{"action": "create|update|delete|move", "file_path": "...", "content": "..."}]}
# Branch must exist first: POST "projects/<pid>/repository/branches?branch=<b>&ref=<base>"
```

Strip ANSI codes from traces before grepping markers: `re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', t)`.

## Quirks (all verified 2026-09-04, glab against self-hosted GitLab forks)

Each quirk below silently wasted time; the workaround is the point of this file.

| Symptom | Cause | Fix |
|---|---|---|
| `glab api` "Unknown shorthand flag: 'o'" | no `-o` output flag | shell redirect `> file` |
| `--input file.json` → HTTP 400/415 | glab sends body **without Content-Type** | add `-H "Content-Type: application/json"` |
| `glab mr create` prints nothing, no MR created (twice on tos/* repos) | unknown, silent | fallback: API `POST projects/<pid>/merge_requests` with `--input` + `-H` |
| `glab mr update --draft=false` accepted but MR stays draft | draft flag is just the `Draft:` title prefix | `glab api -X PUT .../merge_requests/<iid> -f "title=<without Draft:>"` |
| API `PUT` with `state_event=closed` → 400 "state_event does not have a valid value" | fork rejects the documented value | `glab mr close <iid> -R <repo-url>` works |
| Python `urllib` DELETE branch returns 200 + branch object but branch survives | fork quirk | use `glab api -X DELETE` and verify with a follow-up GET (404 = gone) |
| API intermittently 404s on valid paths (project/job queries flap for minutes) | fork instability | retry 3-5× with backoff; only then treat as real 404 |
| `glab api -X PUT .../discussions/<id>` with `-F resolved=true` OR `?resolved=true` → persistent 500/400 (verified 2026-09-07, MR !14: five 500s + 400s in a row) | glab's form/query encoding of this fork's discussion-resolve endpoint breaks | **fallback to raw curl**: `curl -s -o /tmp/r.json -X PUT "http://<host>/api/v4/<path>" -H "PRIVATE-TOKEN: $(glab config get token --host <host>)" -d "resolved=true"` — succeeded first try. Mind rtk: curl output must go to a file (`-o`), never stdout. |
| `glab api -X POST .../discussions/<id>/notes` with `-f body=...` → 400 | same encoding issue | `glab mr note <iid> -m "..."` subcommand works fine |
| Raw curl blocked by rtk hook | rtk intercepts inline HTTP output | always `curl -s -o /tmp/x.json` then parse the file with python | 
| Trace shows `<cmd> # collapsed multi-line command` | runner 15.11 truncates command echoes | analyze command *output*, not the echoed command line |

Token for python fallback: parse `~/.config/glab-cli/config.yml` with **yaml** (`cfg['hosts'][<host>]['token']`). Regex extraction silently matched nothing → empty token → misleading 401s.

## When python is the right tool

- **Retry loops** against the 404 flapping (the ladder's step 3 helper below).
- **Multi-step orchestration**: fetch → transform → assert → push (e.g. YAML edits with `assert t.count(old) == 1` guards before replace).
- **Concurrency**: group-wide project scans, `ThreadPoolExecutor(max_workers=12)`.
- **JSON digestion**: extracting fields from large responses without dumping them into context.

Standard retry helper (paste into a script, don't re-derive):

```python
import json, ssl, time, urllib.request, urllib.error, yaml
cfg = yaml.safe_load(open('/mnt/disk1/hyx/.config/glab-cli/config.yml'))
TOK = cfg['hosts']['gitlab.red.example']['token']          # per target host
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

def api(path, tries=5):
    for i in range(tries):
        req = urllib.request.Request(f"https://gitlab.red.example/api/v4/{path}",
                                     headers={"PRIVATE-TOKEN": TOK})
        try:
            return json.load(urllib.request.urlopen(req, timeout=30, context=CTX))
        except urllib.error.HTTPError as e:
            if e.code in (404, 502, 503) and i < tries - 1:
                time.sleep(8 * (i + 1)); continue
            return {"_err": e.code}
        except Exception:
            if i < tries - 1: time.sleep(8); continue
            return {"_err": "net"}
```

For body-carrying calls add `"Content-Type": "application/json"` and `method='POST'` with `json.dumps(payload).encode()`.

## Completion criteria

- The chosen command form is the lowest rung of the ladder that does the job.
- Any body-sending `glab api` call carries the Content-Type header.
- Destructive calls (DELETE, force push, branch ops) are verified with a follow-up read before being reported as done.
- Any quirk hit that is not in the table above gets added to the table (one row) before the session ends.
