---
name: multi-arch-harbor-push
description: >
  本地用 nerdctl 构建 amd64+arm64 Docker 镜像，fan-out 推送到 Harbor 的
  aip、aip-amd、aip-arm、aip-mm 四个 repo。
disable-model-invocation: true
---

本地用 nerdctl 构建 amd64+arm64 Docker 镜像，fan-out 推送到 Harbor 的四个 repo：`aip`（多架构）、`aip-amd`（amd64）、`aip-arm`（arm64）、`aip-mm`（多架构）。

## 前置检查

```bash
# binfmt 已注册（arm64 交叉构建前提）
ls /proc/sys/fs/binfmt_misc/qemu-aarch64

# nerdctl 可用
sudo nerdctl --version

# Harbor 已登录
sudo nerdctl login internal.example.com
```

任何一项不满足就停，报告缺什么。

## 扇出

一个镜像要推到四个 repo，但只构建两次（amd64 一次、arm64 一次）。架构关系：

| repo | 内容 | 来源 |
|------|------|------|
| `aip-amd` | amd64 单架构 | build amd64 → tag → push |
| `aip-arm` | arm64 单架构 | build arm64 → tag → push |
| `aip` | 多架构 manifest | manifest create from 上面两个 |
| `aip-mm` | 多架构 manifest | 同上，另一 repo 副本 |

tag 策略：版本号 + `latest`，可选 minor tag。

## 执行

### 1 — 确认参数

从项目 `.env` / Makefile / 用户输入收集：

- `IMAGE_NAME` — 镜像名（如 `ocr`、`kube-scheduler`）
- `IMAGE_TAG` — 版本 tag（如 `1.9.2`、`v1.36.3-cvefix`）
- `MINOR_TAG` — 可选，如 `1.9`、`v1.36`
- `DOCKERFILE` — 默认 `Dockerfile`
- `BUILD_ARGS` — 传给 build 的 `--build-arg`，如 `OCR_VERSION=1.9.2`

**完成标准**：所有参数确认，`IMAGE_NAME` 和 `IMAGE_TAG` 非空。

### 2 — 构建 amd64

```bash
sudo nerdctl --namespace k8s.io build --platform linux/amd64 \
  -f <DOCKERFILE> \
  <BUILD_ARGS> \
  -t internal.example.com/aip-amd/<IMAGE_NAME>:<IMAGE_TAG> \
  -t internal.example.com/aip-amd/<IMAGE_NAME>:latest \
  .
```

**完成标准**：`nerdctl build` 退出码 0，amd64 镜像在本地存在。

### 3 — 构建 arm64

```bash
sudo nerdctl --namespace k8s.io build --platform linux/arm64 \
  -f <DOCKERFILE> \
  <BUILD_ARGS> \
  -t internal.example.com/aip-arm/<IMAGE_NAME>:<IMAGE_TAG> \
  -t internal.example.com/aip-arm/<IMAGE_NAME>:latest \
  .
```

**完成标准**：`nerdctl build` 退出码 0，arm64 镜像在本地存在。

### 4 — 推送单架构镜像

```bash
# amd64
sudo nerdctl --namespace k8s.io push internal.example.com/aip-amd/<IMAGE_NAME>:<IMAGE_TAG>
sudo nerdctl --namespace k8s.io push internal.example.com/aip-amd/<IMAGE_NAME>:latest

# arm64
sudo nerdctl --namespace k8s.io push internal.example.com/aip-arm/<IMAGE_NAME>:<IMAGE_TAG>
sudo nerdctl --namespace k8s.io push internal.example.com/aip-arm/<IMAGE_NAME>:latest
```

**完成标准**：四个 push 全部退出码 0。

### 5 — 创建并推送多架构 manifest

对 `aip` 和 `aip-mm` 各做一遍：先删旧 manifest（忽略错误），再 create + push。

```bash
for REPO in aip aip-mm; do
  FULL=internal.example.com/${REPO}/<IMAGE_NAME>:<IMAGE_TAG>
  LATEST=internal.example.com/${REPO}/<IMAGE_NAME>:latest

  sudo nerdctl --namespace k8s.io manifest rm "$FULL" 2>/dev/null || true
  sudo nerdctl --namespace k8s.io manifest rm "$LATEST" 2>/dev/null || true

  sudo nerdctl --namespace k8s.io manifest create "$FULL" \
    internal.example.com/aip-amd/<IMAGE_NAME>:<IMAGE_TAG> \
    internal.example.com/aip-arm/<IMAGE_NAME>:<IMAGE_TAG>
  sudo nerdctl --namespace k8s.io manifest push "$FULL"

  sudo nerdctl --namespace k8s.io manifest create "$LATEST" \
    internal.example.com/aip-amd/<IMAGE_NAME>:<IMAGE_TAG> \
    internal.example.com/aip-arm/<IMAGE_NAME>:<IMAGE_TAG>
  sudo nerdctl --namespace k8s.io manifest push "$LATEST"

  # 可选 minor tag
  if [ -n "<MINOR_TAG>" ]; then
    MINOR=internal.example.com/${REPO}/<IMAGE_NAME>:<MINOR_TAG>
    sudo nerdctl --namespace k8s.io manifest rm "$MINOR" 2>/dev/null || true
    sudo nerdctl --namespace k8s.io manifest create "$MINOR" \
      internal.example.com/aip-amd/<IMAGE_NAME>:<IMAGE_TAG> \
      internal.example.com/aip-arm/<IMAGE_NAME>:<IMAGE_TAG>
    sudo nerdctl --namespace k8s.io manifest push "$MINOR"
  fi
done
```

**完成标准**：`aip` 和 `aip-mm` 各有 `<IMAGE_TAG>` + `latest`（+ 可选 `<MINOR_TAG>`）manifest 推送成功。

### 6 — 验证

```bash
# 抽查一个多架构 manifest
sudo nerdctl --namespace k8s.io manifest inspect \
  internal.example.com/aip-mm/<IMAGE_NAME>:<IMAGE_TAG> | grep -A2 platform
```

应看到 `linux/amd64` 和 `linux/arm64` 两个 platform entry。

**完成标准**：manifest inspect 输出包含两个架构。

## 产出清单

执行完毕后报告：

```
✅ <IMAGE_NAME>:<IMAGE_TAG>
  aip-amd  → amd64  (tag + latest)
  aip-arm  → arm64  (tag + latest)
  aip      → multi  (tag + latest [+ minor])
  aip-mm   → multi  (tag + latest [+ minor])
```

## 常见问题

- **arm64 build 卡住或超慢** — QEMU 模拟比原生慢 5-10 倍，正常现象。如果 >10min 无输出，检查 binfmt 是否注册。
- **manifest create 报 "image not found"** — 单架构镜像必须先 push 成功，manifest create 引用的是远端镜像。
- **manifest rm 报 "not found"** — 首次推送时正常，`|| true` 已处理。
- **push 报 unauthorized** — `sudo nerdctl login internal.example.com` 重新登录。
