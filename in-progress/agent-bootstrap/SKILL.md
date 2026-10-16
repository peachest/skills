---
name: agent-bootstrap
description: 为当前 session 或指定 agent 创建持久身份（manifest + charter + peers + state + sessions.log，遵循 ~/.agents/agents/SPEC.md）。Use when the user asks to 给 agent 建身份 / agent bootstrap / 自举 / 创建 agent manifest / 把当前 session 变成具名 agent, or wants to register a peer agent identity without binding a session.
---

# Agent Bootstrap

把「一个 pi session」升级为「一个具名、持久、可换届的 agent 身份」。规范唯一真相源：`~/.agents/agents/SPEC.md`——本 skill 只写操作流程，字段语义以 SPEC 为准。

## 模式判定

- **无参数 = 自举**：当前 session 成为一个具名 agent，结束时当前 session 登记为第一任当值。
- **带参数 = 建身份目录**：为指定 agent 建身份，只写文件，不绑定 session（等首次上岗/懒启动）。

## 流程

### 1. 定位 workspace

从 cwd 逐级向上找 `.agents/agents/`，到 `~` 为止：

- **命中**：向用户确认——「找到 workspace `<路径>`，这个 agent 属于它，还是在当前位置新建 workspace？」
- **未命中**：向用户确认在哪个位置新建（cwd 或某个父目录），创建 `agents/agents/` 目录。物理上限：`.git` 或 `~`。

### 2. 收集身份信息（与用户对话，一次问全）

按 AGENT.json 字段逐项收集，给出你的建议值让用户确认或改：

1. **name**：workspace 内唯一。skill-manager 类按 `<skill-name>-manager` 命名。
2. **description**：一句话职责。
3. **charter 要点**：使命、职责（可验证条目）、红线、协作规则。
4. **resources**：当前上下文里已读写过哪些文件/目录（paths.read/write）、已用过哪些 skill（skills）、涉及哪些非文件资源（external：集群/网关/服务）。这是换届记忆提醒，不是权限边界——如实列举即可。
5. **peers**：常协作的 agent 名单及其用途（每个 peer 都要在 peers.md 里写清用途，无 manifest 的 peer 靠这张表说明自己）。

### 3. 写身份目录

在 `<workspace>/.agents/agents/<name>/` 下写五个文件，严格按 SPEC.md §3 的模板：

1. `AGENT.json`——L0 身份卡；
2. `charter.md`——使命/职责/红线/协作规则；
3. `peers.md`——peer 名单/用途/拓扑；
4. `STATE.md`——按当前上下文如实填写「战役快照/活跃后台任务/Backlog/交接附言」；全新 agent 则写初始态；
5. `sessions.log`——自举模式追加第一行：`{"sessionId": "<当前 session UUID>", "startedAt": "<now ISO>", "endedAt": null, "note": "自举上岗"}`；建目录模式不写。

### 4. 更新 workspace AGENTS.md 的 agent 索引

在 workspace 根 `AGENTS.md` 加（或更新）一节，让后续 session 能发现这些身份：

```markdown
## Agents（本 workspace 具名身份）

身份规范：~/.agents/agents/SPEC.md
| 名字 | 职责 | 何时找我 |
|------|------|----------|
| leader | 管理 peer 完成投机采样训练 | 任务派发/状态查询 |
```

向用户展示最终索引内容再写入。

### 5. 收尾输出

打印身份卡给用户确认：目录路径、五个文件清单、当值 session id（自举模式）、下一步提示（如「换届用 /agent-renew（待扩展落地）；给 peer 建身份可再次运行本 skill 带参数模式」）。

## 红线

- 不在检索歧义时静默选边——workspace 归属必须用户确认。
- name 冲突（目录已存在）时停下问用户，不覆盖。
- SPEC.md 是模板与语义的唯一来源；发现模板不够用时，先改 SPEC 再继续，不在本 skill 里私开分叉。
