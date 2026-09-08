---
name: remote-script-exec
description: Run non-trivial commands on remote nodes by writing the script locally, scp-ing it over, and executing it there — the scp-first pattern. Use when about to send a multi-line command, nested quotes, heredoc, or variable substitution through ssh; when uploading probe/deploy scripts to an unfamiliar node and running them; when deploying a long-running background job (nohup) to a remote host and fetching results back; or when an inline ssh command fails with quoting/escaping errors (引号地狱 / ssh 转义).
---

# remote-script-exec

When a command for a remote node is anything more than a trivial one-liner, do not inline it into the ssh command string. **Write the script locally, scp it over, execute it there.** The local file is the source of truth; the remote copy is disposable.

## The pattern

```bash
# 1. write locally (node-prefixed name, see conventions below)
#    ~/tmp/<node>_<task>.py

# 2. upload and run
scp -o StrictHostKeyChecking=no ~/tmp/<node>_<task>.py <user>@<node>:/tmp/
ssh <user>@<node> 'python3 /tmp/<node>_<task>.py 2>&1'
```

Iterate by editing the local file, re-scp, re-run. Never patch the remote copy in place — the next iteration would clobber the fix.

Inline ssh is fine only for a single command with no nested quotes and no multi-statement chaining (`ssh <node> 'ls /tmp'`). Everything else — loops, pipes with quotes, python one-liners, heredocs, anything you would write across lines — goes through the pattern. On unfamiliar nodes the first connect may need `-o StrictHostKeyChecking=no`; on later connects drop it once the host key is known.

This also satisfies the standing rule that repeatedly-executed logic lives in a script, not in a command string: iteration cost collapses to a re-scp.

## Why: quoting hell

Each layer of nesting eats one quoting level, and three layers deep nothing parses:

1. The outer bash single quotes wrap the ssh argument — nothing inside them expands locally.
2. The remote shell re-parses that same string with its own quoting rules.
3. Embedded content (python f-strings, sed expressions, heredoc bodies) brings its own quotes on top.

Layer 3 collides with layer 1: the script wants single quotes that the outer wrapper already spent. Variable expansion is ambiguous too — `$VAR` in an ssh string is a silent bet on which shell expands it.

Real case (sanitized): mid-diagnosis on an unfamiliar node, a probe script needed a one-line patch. The cheap-looking move was inline `sed` inside `ssh '...'` — bash single quotes + sed expression + python f-string subscript, three layers, parse failure. The neighboring iterations that edited the local file and re-scp'd it never failed. Diagnosing the quoting failure cost more than the scp ever would.

## Directory conventions

| Location | Rule |
|---|---|
| Local staging | `~/tmp/<node>_<task>.py` / `.sh` — node prefix so scripts from different nodes never collide |
| Remote, one-off probes | `/tmp/<name>` — disposable, reboot clears it |
| Remote, persistent work | A dedicated dir such as `/root/<project>/` — deployments, venvs, long-running data collectors all live here |
| Results | scp back into the local working dir of the task (e.g. `<workdir>/data/`), then analyze locally |

## Credentials: two hard rules

1. **Passwords and tokens never appear inline in a command.** Command strings persist in session logs and can leak into shared or public repositories. `sshpass -p '<password>' ssh ...` is the anti-pattern — the password lands in the transcript.
2. **Prefer `~/.ssh/config` Host aliases with key auth.** When sshpass is unavoidable, export the password into the environment from outside any repository and use `sshpass -e ssh ...`.

## Deploy & long-running pattern

For anything that must survive the ssh session or has dependencies (a collector, a service, a test harness):

1. **Package locally** — tarball the source (src + pyproject) plus a deploy script; keep both in `~/tmp/`.
2. **Ship and unpack** — one scp carries the tarball and the deploy script to the persistent remote dir.
3. **Remote environment** — the deploy script creates a venv and pip-installs; route pip through the site proxy when the node has no direct internet.
4. **Background run** — launch with `nohup ... &`, give it a duration or a stop condition, verify the output file grows before disconnecting.
5. **Fetch back** — scp artifacts to the local working dir, decode and analyze locally where the tooling already exists.

## Cleanup

`/tmp` one-offs are left to reboot. Persistent dirs are not: at task end, either remove them from the node or report the residue (path, size, purpose) to the user. An unfamiliar node should not accumulate unowned directories.
