# Synth Judgment — REFUSED / Hedging Factual Gateway

## 纯价值判断 → REFUSED

vLLM 的方案比 SGLang 更好，在生产环境中强烈推荐使用 vLLM。

## 模糊推断 → REFUSED

这个问题大概率是 NUMA 拓扑不匹配导致的，或许和 GPU 亲和性设置也有关系。

## hedging_factual 含可验证原子 → web_search（T3）

该模型在 H100 集群上可能达到 6,440 tok/s 的推理吞吐。

## 社区归因 → web_search（T3）

据 vLLM 社区称，Automatic Prefix Caching 特性在生产环境的使用率
已超过 80%。

## hedging_factual 无可验证原子 → REFUSED（guard fail fallback）

该方案在极端情况下可能略微有延迟抖动。

> 本文档用于验证 judgment refine（DD-29）和 hedging_factual guard。
