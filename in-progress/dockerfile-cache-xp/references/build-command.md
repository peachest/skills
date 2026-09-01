# nerdctl local build command

Reference for the build command that runs the optimized `Dockerfile.local`.

## Prerequisites

1. **buildkitd running** — `sudo systemctl status buildkit` shows active, and
   `/run/buildkit/buildkitd.sock` exists.
2. **Harbor auth** — `/root/.docker/config.json` contains an `auths` entry for
   `internal.example.com`. `nerdctl login internal.example.com` has a known bug
   (`expected acArg to be internal.example.com:443, got internal.example.com`),
   even with `:443` appended. Write the config directly:

   ```bash
   echo '{"auths":{"internal.example.com":{"auth":"'$(echo -n 'USER:PASS' | base64 -w0)'"}}}' \
     | sudo tee /root/.docker/config.json
   ```

3. **Proxy address** — from AGENTS.md or memory; the skill does not hardcode it.
   The corporate proxy fully supports HTTPS CONNECT. Pass it via `--build-arg`,
   not as `ENV` in the Dockerfile.

## The command template

```bash
sudo nerdctl build \
  --build-arg http_proxy=<PROXY> \
  --build-arg https_proxy=<PROXY> \
  --build-arg HTTP_PROXY=<PROXY> \
  --build-arg HTTPS_PROXY=<PROXY> \
  --build-arg NO_PROXY=<NO_PROXY> \
  --build-arg no_proxy=<NO_PROXY> \
  -t internal.example.com/<project>/<image>:<tag> \
  -f <path>/Dockerfile.local \
  . > /tmp/build.log 2>&1 &
```

### Why four proxy args (upper + lower)

`curl` reads lowercase by default, `git` reads uppercase in some paths. Pass
**both** sets; one set alone leaves some RUN steps bypassing the proxy.

### NO_PROXY

Include the harbor registry and internal hosts so pushes/pulls and internal
fetches bypass the proxy:

```
NO_PROXY=internal.example.com,localhost,127.0.0.1,<internal-cidr>
```

### nerdctl limitations

- No `--proxy-http`/`--proxy-https` flags — proxy goes through `--build-arg`.
- buildkitd is a separate systemd service; it does NOT inherit the shell's
  `*_proxy` env vars. `--build-arg` is the only reliable path.

## Push

```bash
sudo nerdctl push internal.example.com/<project>/<image>:<tag>
```

Multi-arch (single manifest list, no per-arch tag noise):

```bash
sudo nerdctl build --platform amd64,arm64 -t <image>:<tag> -f <Dockerfile>.local .
sudo nerdctl push --all-platforms <image>:<tag>   # --all-platforms is mandatory
```

Without `--all-platforms`, nerdctl pushes only the current platform's image.

## Background build + log tailing

Builds are long (15-30 min first run). Run in the background and tail the log:

```bash
sudo nerdctl build ... > /tmp/build.log 2>&1 &
tail -f /tmp/build.log
```
