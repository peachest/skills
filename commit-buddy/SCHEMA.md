# Commit Plan Schema

## Agent 输出（简化方案）

Agent 只负责语义判断——分组、commit message、hunk 归属。不需要跑 `git diff`、不需要计算指纹。

```typescript
interface CommitPlanInput {
  version: 1;
  commits: CommitSpec[];
}

interface CommitSpec {
  type: CommitType;
  scope?: string;
  summary: string;
  body?: string;
  breaking?: boolean;
  signoff?: boolean;
  files: FileHunkSpec[];
}

type CommitType =
  | "feat" | "fix" | "docs" | "style" | "refactor"
  | "perf" | "test" | "build" | "ci" | "chore" | "revert";

interface FileHunkSpec {
  path: string;
  /** hunk 序号列表（从 0 开始），或 "all" 表示全部 */
  hunks: number[] | "all";
  /** 未跟踪新文件标记 */
  untracked?: boolean;
}
```

### 示例

```json
{
  "version": 1,
  "commits": [
    {
      "type": "feat",
      "scope": "auth",
      "summary": "add OAuth2 token validation",
      "body": "Move token parsing into a separate validator.",
      "signoff": true,
      "files": [
        { "path": "internal/auth/validator.go", "hunks": "all" },
        { "path": "internal/auth/handler.go", "hunks": [0, 2] }
      ]
    },
    {
      "type": "chore",
      "summary": "downgrade debug logs to info in auth handler",
      "files": [
        { "path": "internal/auth/handler.go", "hunks": [1] }
      ]
    }
  ]
}
```

## 完整 CommitPlan（脚本生成）

`generate-plan.sh` 接收简化方案，自动补全 `snapshot`（提取 hunk、计算 SHA256 指纹、记录 HEAD sha），输出完整 CommitPlan。

```typescript
interface CommitPlan {
  version: 1;
  commits: CommitSpec[];
  snapshot: Snapshot;
}

interface Snapshot {
  files: SnapshotFile[];
  created_at: string;
  source: string;
}

interface SnapshotFile {
  path: string;
  head_sha: string;
  hunks: SnapshotHunk[];
}

interface SnapshotHunk {
  index: number;
  fingerprint_sha256: string;
}
```

## 校验规则（execute-plan.sh 执行前）

| # | 规则 | 失败时 |
|---|------|--------|
| 1 | snapshot.files 中每个 path 必须在当前工作区存在 | 中止，列出丢失文件 |
| 2 | 每个 path 的 `head_sha` 必须等于 `git rev-parse HEAD` | 中止，HEAD 已变 |
| 3 | 已分配 hunk 的 SHA256 必须与 snapshot 一致 | 中止，列出指纹不匹配的 hunks（用户在确认期间改了代码） |
| 4 | 同一个 hunk 序号不能出现在多个 commit 中 | 中止，列出冲突的 hunk |
| 5 | `untracked: true` 的文件必须是未跟踪状态（`??`） | 中止，列出异常文件 |

未分配的 hunk 不阻断执行，在 PlanResult 中报告。

## 脚本

### generate-plan.sh

```
Usage: generate-plan.sh <input.json>

1. 读取简化方案 JSON
2. 对每个文件运行 git diff HEAD，提取 hunk，计算 SHA256 指纹
3. 记录当前 HEAD sha
4. 输出完整 CommitPlan JSON 到 <PROJECT_DIR>/.pi/commit-buddy/plan.json
```

### execute-plan.sh

```
Usage: execute-plan.sh <plan.json>

1. 读取完整 CommitPlan JSON
2. 校验规则 1-5（fingerprint 检测确认期间代码是否被改动）
3. git stash push --keep-index
4. 遍历 commits: reset HEAD → apply hunk patches → git commit
5. git stash pop
6. 输出 PlanResult JSON 到 result.json
```

## PlanResult

```typescript
interface PlanResult {
  ok: boolean;
  commits: { sha: string; message: string }[];
  unallocated_hunks?: { path: string; hunks: number[] }[];
  stash_pop_ok?: boolean;
  stash_conflicts?: string[];
  errors?: string[];
}
```