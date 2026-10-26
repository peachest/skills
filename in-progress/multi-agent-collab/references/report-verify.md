# Report file verification scaffold — 声明式完成判据的机械化补丁

## 根因（两次复现实证：10-22 researcher×3、10-26 brainstorm 3/4 + phaseA 4/5）

子代理报告里的 "REPORT_WRITTEN / 已写入 X" 是**声明式判据**：它证明子代理自以为
写了，不证明文件系统里有。产物漂移进 runtime 管理的 `subagent-artifacts/`
（形如 `<runid>_<agent>_output.md`），子代理仍如实声称成功——写文件动作和声明
之间无机器验证。

上游语义（pi-subagents guide，tool-reference/output-mode-details）：**task 文本
里的路径只是指令，不改变运行时的 output 路由**。这是漂移的根因，也指明治本方法。

## 治本：派发时用 `output:` API 绑定（runtime 持久化，子代理无法漂移）

workflow 脚本——每个 child 显式绑定 output，回收 `outputReference` 而非 child 自述：

```js
const lanes = [
  { key: "brake-a", task: "…分析任务书（不再需要写'务必写到 X 路径'）" },
  { key: "brake-b", task: "…" },
];
const results = await runs.all(lanes.map((l) => ({
  key: l.key,
  agent: "worker",
  task: l.task,
  // API 绑定：runtime 把最终产物持久化到该绝对路径，返回引用
  output: `/mnt/disk1/hyx/tmp/<topic>/${l.key}.md`,
})));
// 回收持久引用（机械事实），不要用 child 报告里的"已写入"句子
return results.map((r, i) => ({
  key: lanes[i].key,
  ok: r.ok,
  outputReference: r.outputReference,
  artifactPaths: r.artifactPaths,
}));
```

直接 `{agent, task}` 单派发同理：`subagent({ agent, task, output: "<abs path>" })`。

## 兜底：父 session 收尾机械验证（child 自写文件的场景仍需要）

child 带写工具、自己动笔写文件时，`output:` 绑定不覆盖它手写的路径——收尾跑：

```bash
# manifest: {"brake-a": "/mnt/disk1/hyx/tmp/topic/brake-a.md", ...}
python3 <skill>/scripts/verify-reports.py ~/tmp/<topic>/manifest.json
```

- exit 0 = 全部存在且非空；exit 1 = 有缺失，同时列出 `subagent-artifacts/`
  窗口期内的新产物候选（预览前 96 字符），人工核对后 cp 回声明路径（回捞）。
- `--window 48` 调回捞搜索窗（默认 24h）。

## 判据规则

- 只要产物要跨 session/跨人使用：一律 `output:` 绑定 + 收尾 verify-reports，二选一不可省。
- 子代理自述的 REPORT_WRITTEN 不计入验收；`test -f` / verify-reports 的 exit code 才算。
