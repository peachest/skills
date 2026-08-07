---
name: html-review
description: Validate HTML file structural integrity — DOCTYPE, charset, tag closure, duplicate ids, resource references. Use when user has generated an HTML file and wants to check correctness, or says "验证 HTML" / "检查一下 html" / "validate this html" / "检查页面结构" / "review my html".
---

# HTML Review

## Quick start

```bash
python3 <skill_dir>/scripts/validate_html.py <file>
python3 <skill_dir>/scripts/validate_html.py --strict <file>  # 含 html5lib + VNU
```

## Workflow

1. **Agent 生成了 HTML 文件后**，询问用户是否需要校验
2. 用户同意后，运行基础校验
3. 向用户报告校验结果（问题列表 / 通过）
4. 如有问题，用户可选择：自行修复 / 让 agent 修复后重新校验 / 忽略

## Validation checks

| Check | What it detects |
|---|---|
| DOCTYPE | 缺失或错误（非 `<!DOCTYPE html>`） |
| 基础结构 | 缺失/重复 `<html>` `<head>` `<body>` |
| `<title>` | 缺失 |
| charset | 缺少 `<meta charset="utf-8">` |
| 重复 id | 相同 id 出现多次 |
| 标签闭合 | lxml vs html.parser 交叉验证，元素数不一致报未闭合 |
| 外链资源 | 列出 `script[src]` 和 `link[rel=stylesheet]` 数量与 URL |
| 内联事件处理器 | 计数 `onclick`, `onchange` 等 |

### --strict mode

- **html5lib**：HTML5 规范解析，检出 `&` 未转义等语法违规（需 `pip install html5lib`）
- **VNU**：W3C Nu Checker 离线校验（需 `vnu.jar` 置于 `~/.vnu/vnu.jar`）

## Exit code

- `0` — 所有检查通过
- `1` — 发现问题

## Checklist

- [ ] 询问用户是否需要校验
- [ ] 运行 `python3 <skill_dir>/scripts/validate_html.py <file>`
- [ ] 报告通过/问题
- [ ] 如用户要求修复，修复后重新校验确认