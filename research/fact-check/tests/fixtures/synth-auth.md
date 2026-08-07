# Synth Auth — P0 确权型 Verifier 覆盖

本报告分析 AuthHub 的身份认证方案。AuthHub 采用 Gitee 上开源的
`authhub/identity-core` 仓库（gitee.com/authhub/identity-core）作为核心
库。其中 issue #42 报告了 OAuth 回调重定向的安全漏洞，该问题也在
GitLab（gitlab.com/authhub/identity-core/-/issues/100）被同步追踪。

依赖包方面，AuthHub 通过 `npm install @authhub/jwt-validator` 安装 JWT
校验库。授权协议采用 MIT license（licensed under MIT）。核心算法的
原始论文见 doi:10.1145/3731569.3764843，补充文档发布在
https://docs.authhub.example.com/spec。

> 所有数字来自内部环境验证。
