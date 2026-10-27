# Skill 间依赖的书写规范

一个 skill 引用另一个 skill 时，依赖语义由**动词**承载，`/skill:xxx` 记号本身不承载
语义——同一个记号可以是“接管流程”也可以是“读个文件”。本规范约定动词与记号的搭配。

## 实证：各写法的会话体现率（2026-10-27 全库挖掘）

5593 会话 / 7721 次 skill 注入，与 183 条声明边对账。“体现” = 注入 A 后 assistant
在 reasoning/response 提及 B（排除 B 同会话被独立注入或用户显式请求）：

| 写法 | 体现率（全量） | 体现率（版本锚定保守口径） | 说明 |
|---|---|---|---|
| **read-material**（read + 指名到文件） | **48.3%** (128/265) | **66.2%** (49/74) | 最强；读文件→内容进上下文→自然提及，链路机械单步 |
| **invoke**（delegate/run） | 文本 3.4%，**行为 22.4%** (1113/4967) | 行为 21.0% | 体现形态在 toolCall（读 B 的 SKILL.md / dispatch 带注入），不在文本 |
| **mention**（纯提及） | 9.4% (68/723) | — | 最弱；名字掉落不产生行为 |

范例边：review-spec→pi-subagents（read 指名文件）77/77 全体现；triage-mr→mr-review-triage
42/45；to-peer→multi-agent-collab（invoke）行为 80/85。反例：wayfinder→domain-modeling
文本 1/201——invoke 的证据形态不是复述。

**结论**：需要依赖真正生效时，写 `read /skill:xxx 的 <file>`（指名到文件）；invoke 写法
的体现靠 agent 行为，文本复述不指望；纯 mention 只当背景注释。

## 动词分类（8 类）

| 类 | 动词 | 语义 | 标准写法 |
|---|---|---|---|
| **delegate** | Delegate to / route to / 转交 / hands findings to / run | 对方流程接管控制权，本 skill 暂停 | `Delegate to /skill:xxx with <输入>` |
| **spawn** | spawn a `/skill:xxx` sub-agent / dispatch / one subagent per X | 隔离上下文（`context: fresh`）跑对方流程，回收结果 | `Spawn a /skill:xxx sub-agent (context: fresh)` |
| **read** | read / see / Load X's <file> / follow X's "<section>" | 只取文本、模板、规范作参考材料，不执行 | `Read /skill:xxx 的 references/y.md`（**必须写到文件或小节**） |
| **borrow** | use the X test from `yyy` / xxx-style / 按 `yyy` 的方法域 | 借词汇、判据、风格；裸名反引号 + 点名借什么 | `Use the deletion test from \`codebase-design\`` |
| **sequence** | After `/skill:xxx` / before / first … then | 只约束先后顺序，本轮不执行 | `After /skill:tdd, before /skill:code-review` |
| **route** | failed → / 意见多时走 / if X then `/skill:xxx` | 条件成立才派发 | `<条件> → /skill:xxx` |
| **fork** | Forked from X at <hash> / Identical to X except … | 声明派生关系与差异点 | `Fork of /skill:xxx` + 差异一句 |
| **position** | complements X / X owns A, this owns B / 卡位表 / territory | 划边界，双方独立，不派发 | 一句 "X owns A; this owns B" |

## 搭配规则

1. **delegate/spawn 用行为动词 + `/skill:` 记号**。裸写 `/skill:xxx` 无动词 = 歧义，禁止。
2. **read 必须落到文件或小节名**。`read /skill:xxx`（无文件名）是最常见歧义源；读全文
   用 `See ../xxx/SKILL.md` 相对链接，读局部用 `read /skill:xxx 的 references/y.md`。
3. **borrow 用裸名反引号，不用 `/skill:` 记号**——`/skill:` 记号暗示可调用，borrow 不可。
4. **route 把条件写在前、记号在后**：`stall/timeout → /skill:diagnose-ocr-ci`。
5. **双向关系写两次**：上游写出口指针、下游写入口指针，单向边是盘点时的"缺依赖嫌疑"。
6. **position 类不进完成判据**：卡位说明是给 agent 的分流信号，不是步骤。

## 引用前校验

写引用前 ls 确认目标存在（in-repo 源仓 / `~/.agents/skills` 安装副本 / pi 插件
`~/.pi/agent/npm/node_modules/*/skills`）。目标两处皆无 = dangling 引用（2026-10-27
盘点实测 7 个：platform-browser、unslop、ste100、writing、technical-writing-best-practices、
to-prd、to-issues——引用它们前先建或先改名）。

## 判别速查

拿到一条 `/skill:xxx` 引用，看动词定类型：delegate/spawn 会**转移控制权**（前者同上下文、
后者隔离上下文）；read/borrow 只**取内容**；sequence/route **本轮不执行**；fork/position
**只是声明**。
