---
name: hf-download
description: Pull models/datasets from Hugging Face with the right tool — hfd (aria2c multi-thread + resume) first, hf/huggingface-cli, aria2c single-file, curl loop as last resort. Use when asked to 下载模型/拉取模型/下载 HF 模型, download a model or dataset from Hugging Face, fetch a checkpoint (draft model, tokenizer, weights), or set up the download toolchain on a new node.
---

# HF model download

## Tool ladder

Pick the first rung that fits; never hand-write a download loop the ladder already covers.

1. **hfd** — whole repo, multi-file, or filtered pulls. aria2c multi-thread + resume + include/exclude + token auth. The default for models and datasets.
2. **hf download** — whole repo when hfd is absent but a huggingface_hub venv exists: `hf download <repo> --local-dir <dir>` (respects `https_proxy`).
3. **aria2c single file** — one known big file: `https://huggingface.co/<repo>/resolve/main/<path>`, add `header=Authorization: Bearer <token>` for gated repos, `-x 4 -c` for threads + resume.
4. **curl loop** — only for a short list of filenames you already know. Probing an unknown repo layout with curl guesses is the failure mode hfd's metadata API exists to prevent.

## hfd setup

hfd is not preinstalled; this skill ships the script.

```bash
cp <SKILL_DIR>/scripts/hfd ~/.local/bin/hfd && chmod +x ~/.local/bin/hfd
~/.local/bin/hfd --help   # usage banner printed = installed
```

First-use verification — small repo into `~/tmp`, then clean up:

```bash
cd ~/tmp && timeout 120 ~/.local/bin/hfd <small/repo> --local-dir ~/tmp/hfd-test 2>&1 | tail -4
ls ~/tmp/hfd-test/ && rm -rf ~/tmp/hfd-test
```

Requires `curl` and `aria2c` (no aria2c → pass `--tool wget`); `jq` optional but faster metadata parsing. On a new node run `bash <SKILL_DIR>/scripts/check-env.sh` first.

## Usage

```bash
hfd <org/repo> --local-dir <dir>                  # whole model (-x 4 -j 5 defaults)
hfd <org/repo> --local-dir <dir> --hf_username <u> --hf_token <t>   # gated repo
hfd <org/repo> --local-dir <dir> --include '*.safetensors'          # filter in
hfd <org/repo> --local-dir <dir> --exclude '*.md' '*.msgpack'       # filter out
hfd <org/dataset> --dataset --local-dir <dir>     # dataset
HF_ENDPOINT=https://hf-mirror.com hfd ...         # mirror endpoint
```

- Interrupted download resumes by re-running the same command (aria2c control file).
- Always pass `--local-dir`; without it files land in `./<repo_name>` under the CWD.
- A repo's own `config.json`/`README.md` download automatically; no need to name them.

## Network

- Direct-internet nodes: plain `hfd` works, no proxy.
- Proxy-only nodes: `export https_proxy=... http_proxy=...` (per-node value lives in `scripts/runtime.conf`, template in `scripts/runtime.conf.example`) or use the mirror via `HF_ENDPOINT`.
- Downloading onto a remote cluster node: prefer copying an already-downloaded local dir over re-downloading; otherwise scp the script over and run with nohup + log (see the remote-script-exec skill).
