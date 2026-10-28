# ADR-0003: 误报白名单不内置，靠脚本内 shellcheck disable 注解

日期: 2026-10-28
状态: accepted

## 背景

SC2206（ARRAY=($(...))）等码是场景相关的：peer 的脚本中 8 条 SC2206 均为故意保留 word splitting 的场景，shellcheck 判为误报需逐条评估。peer 已采用的处置法是脚本内 `# shellcheck disable=SCxxxxx` 注解（且验证过指令行语法严格：不能跟中文注解、需独立注释行说明）。

## 决策

- 白名单不内置在 skill、不引入 `.shellcheckrc` 配置文件。
- skill 报告把命中码归类为「疑似误报，建议逐条定谳」（真修 / 白名单 / disable 注解三选一），定谳动作落在脚本注解上。

## 理由

注解跟着代码走、评审可见、shellcheck 原生支持、多一层配置文件（.shellcheckrc）只增加间接性。
