# Synth Decomp — 7 种 Catalog 拆解模式

本报告覆盖全部 7 种声明拆解模式，以及一个无法拆解的复合声明。

## AND-枚举

该系统支持三种推理后端：vLLM、TensorRT-LLM 和 llama.cpp。

## 括号-补充

该论文由清华大学计算机系团队（2025 年）提交至 MLSys 2026。

## 括号-展开

国产算力卡覆盖华为（昇腾 910B，910C，N腾 950）三个型号。

## FROM-TO

模型加载时间从 320.8s 降至 47.3s，冷启动从 4 分钟降到 30 秒。

## 从句嵌入

该论文提出的 Tutti 方案，其主要创新在于 GPU io_uring 的对象抽象
方法，在长上下文场景下将 GPU 等待时间降低了 78.3%。

## 即-补充

最大瓶颈是引擎编译阶段，即 torch.compile 加 CUDA Graph 捕获的总耗时
约 70 秒。

## 破折号补充

Llama 3.1 8B 在消费级 RTX 4090 上就能跑——这是 vLLM 社区实测结果。

## compound_embedded（不拆，标记）

KVCache 在 GPU HBM 和 CPU DRAM 和 NVMe SSD 和远程 CXL 内存和 RDMA
网络上跨越了多个存储层级，形成一个复杂的 multi-tier 缓存系统，目前
没有统一的命名和路由方案能同时覆盖所有层级并保持性能和可观测性。

> 本文档用于验证 catalog 拆解和 compound_embedded 标记。
