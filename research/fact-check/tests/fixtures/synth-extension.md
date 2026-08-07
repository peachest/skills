# Synth Extension — 扩展层类型自动检测

本章覆盖扩展层的 5 种类型，验证文档域自动检测逻辑（DD-06 扩展层）。

## pricing

API 定价为 $0.50/1M tokens，批量价低至 $0.003/1K tokens。

## compliance

该平台已通过 FedRAMP Moderate 合规审计，数据处理满足 GDPR 要求。

## route

核心 API 路由 `/v1/chat/completions` 的 p99 延迟为 2.3 秒。

## port

开发服务默认监听端口 8080，生产环境切换至 443 端口的 TLS。

## retry

客户端对 5xx 错误执行指数退避重试，最大重试次数默认为 3。

> 本文档用于验证扩展层类型的关键词自动检测。
