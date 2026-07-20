# Synth Inference — INFERRED Verdict 覆盖

## causal: 使……可行 → INFERRED

MLA 注意力机制将 KV Cache 压缩到约 1/32 大小，使 CPU 推理在
长上下文场景下变得可行。

## significance: 关键/核心 → INFERRED

Prefix Caching 是长文档问答场景的核心性能优化手段。

## attribution: 社区共识 → 可验证（T3）

根据 GitHub Discussion 的用户反馈，KTransformers 是当前最活跃的
国产异构推理框架。

## 混合：可验证事实 + 推断结论 → SUPPORTED（事实部分）+ INFERRED（结论部分）

MLA 压缩率约为 32x（CUDA kernel 实现可验证数值），因此使 CPU 推理
的性价比显著优于 GPU 方案。

> 本文档用于验证 INFERRED verdict（DD-03）与 INFERRED 事实拆分（DD-06）。
