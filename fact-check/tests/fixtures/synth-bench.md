# Synth Bench — P0/P2 + Web Search 覆盖

Qwen3-235B-A22B 在 H100 × 8 上使用 vLLM 分布式加载，冷启动时间从
320.8s 降至 47.3s（arXiv:2605.10670 报告的实验结果）。该优化对应的
代码改动在 PR #3729，于 2025 年 12 月合入主分支。

实测吞吐为 6,440 tok/s，批处理延迟约 0.5s。推理由 vLLM 的
Automatic Prefix Caching 特性驱动——该特性在 v0.14.0 中引入。每
GPU 显存占用约 54.92 GiB。

> 以上数据来自 vLLM 社区 benchmark 文档。
