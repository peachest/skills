# Synth Package — 包管理器 + 镜像 Verifier 全覆盖

此章节验证 6 种包管理器、Docker 镜像和 HuggingFace 模型名。

## PyPI

依赖 torch 和 requests 两个核心包，安装命令为 `pip install torch`。

## Cargo

Rust 生态内使用 `cargo install ripgrep` 安装的代码搜索工具。

## Go module

服务端通过 `go get github.com/spf13/cobra` 集成命令行框架。

## NuGet

.NET 组件通过 `dotnet add package Microsoft.ML` 引入机器学习能力。

## Docker

生产容器基于 `docker pull nginx:1.25` 构建的镜像。

## GitLab MR

该特性由 gitlab.com/mlcommons/openfold/-/merge_requests/42 引入。

## HuggingFace 模型（P1）

推理任务使用 unsloth/DeepSeek-V3-GGUF 量化版本。

> 所有包名、镜像名、模型名均为真实存在。
