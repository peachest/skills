# Commit Plan Schema

agent 产出、脚本消费的中间格式，作为 agent 到确定性脚本的桥梁。

## 完整 Schema

```typescript
interface CommitPlan {
  /** schema 版本 */
  version: 1;

  /** 每个 commit 按执行顺序排列 */
  commits: CommitSpec[];

  /** 执行前的校验快照 */
  snapshot: Snapshot;
}

interface CommitSpec {
  type: CommitType;
  /** 可选 scope */
  scope?: string;
  /** 简短描述，imperative mood，50-72 字符 */
  summary: string;
  /** 详细 body，可选 */
  body?: string;
  /** 是否 breaking change */
  breaking?: boolean;
  /** 是否添加 --signoff */
  signoff?: boolean;
  /** 按文件列出的 hunk 归属 */
  files: FileHunkSpec[];
}

type CommitType =
  | "feat" | "fix" | "docs" | "style" | "refactor"
  | "perf" | "test" | "build" | "ci" | "chore" | "revert";

interface FileHunkSpec {
  path: string;
  /**
   * 该文件中归属于此 commit 的 hunk 序号列表。
   * hunk 序号由脚本计算（从 0 开始，按文件 diff 顺序排列）。
   *
   * "all" 表示该文件的所有 hunk 都归此 commit。
   * 空数组 [] 表示该文件没有 diff hunk（纯新增未跟踪文件时搭配 untracked: true）。
   */
  hunks: number[] | "all";
  /**
   * 标记为未跟踪新文件（git status --short 中 ?? 状态）。
   * 为 true 时脚本直接 git add 整个文件，不参与 hunk diff 校验。
   * hunks 应设为 "all" 或 []。
   */
  untracked?: boolean;
}

interface Snapshot {
  files: SnapshotFile[];
  created_at: string;
  source: string;
}

interface SnapshotFile {
  path: string;
  /**
   * HEAD commit sha。
   * 未跟踪文件的 head_sha 仍然设置为当前 HEAD（校验的是 HEAD 没变过）。
   */
  head_sha: string;
  /** 该文件的所有 diff hunk。未跟踪文件此数组为空。 */
  hunks: SnapshotHunk[];
}

interface SnapshotHunk {
  index: number;
  /** hunk 完整 diff 内容（@ ... @@ + 所有 +/-/context 行）的 SHA256 */
  fingerprint_sha256: string;
}
```

## 完整示例

```json
{
  "version": 1,
  "commits": [
    {
      "type": "feat",
      "scope": "auth",
      "summary": "add OAuth2 token validation",
      "body": "Move token parsing into a separate validator so it can be reused in middleware.",
      "breaking": false,
      "signoff": true,
      "files": [
        { "path": "internal/auth/validator.go", "hunks": "all" },
        { "path": "internal/auth/handler.go",  "hunks": [0, 2] }
      ]
    },
    {
      "type": "chore",
      "summary": "downgrade debug logs to info in auth handler",
      "files": [
        { "path": "internal/auth/handler.go", "hunks": [1] }
      ]
    }
  ],
  "snapshot": {
    "files": [
      {
        "path": "internal/auth/validator.go",
        "head_sha": "a1b2c3d4e5f6789abcdef0123456789abcdef01",
        "hunks": [
          { "index": 0, "fingerprint_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" }
        ]
      },
      {
        "path": "internal/auth/handler.go",
        "head_sha": "a1b2c3d4e5f6789abcdef0123456789abcdef01",
        "hunks": [
          { "index": 0, "fingerprint_sha256": "abc..." },
          { "index": 1, "fingerprint_sha256": "def..." },
          { "index": 2, "fingerprint_sha256": "ghi..." }
        ]
      }
    ],
    "created_at": "2026-07-20T12:00:00Z",
    "source": "commit-buddy"
  }
}
```

## 包含新文件的示例

```json
{
  "version": 1,
  "commits": [
    {
      "type": "docs",
      "summary": "add contributing guidelines",
      "files": [
        { "path": "CONTRIBUTING.md", "hunks": "all", "untracked": true }
      ]
    }
  ],
  "snapshot": {
    "files": [
      {
        "path": "CONTRIBUTING.md",
        "head_sha": "a1b2c3d4e5f6789abcdef0123456789abcdef01",
        "hunks": []
      }
    ],
    "created_at": "2026-07-20T12:00:00Z",
    "source": "commit-buddy"
  }
}
```

## 校验规则（脚本端）

| # | 规则 | 失败时 |
|---|------|--------|
| 1 | snapshot.files 中每个 path 必须在当前工作区存在 | 中止，列出丢失文件 |
| 2 | 每个 path 的 `head_sha` 必须等于 `git rev-parse HEAD` | 中止，HEAD 已变 |
| 3 | 已分配 hunk（被 commits 引用的）的 SHA256 必须与 snapshot 一致 | 中止，列出指纹不匹配的 hunks |
| 4 | 同一个 hunk 序号不能出现在多个 commit 中 | 中止，列出冲突的 hunk |
| 5 | `untracked: true` 的文件必须是未跟踪状态（`git status --short` 中 `??`） | 中止，列出异常文件 |
| — | ~不再要求 hunk 总数一致~ | 允许未分配的 hunk 存在 |
| — | ~不再要求全覆盖~ | 跳过未分配 hunk，在 PlanResult 中报告 |

## 脚本执行流程（`scripts/execute-plan.sh`）

```
Usage: execute-plan.sh <plan.json>

1. 读取 plan.json
2. 校验规则 1-5
3. git stash push --keep-index --message "commit-buddy-auto-stash"
4. 遍历 commits:
   a. git reset HEAD
   b. 对每个文件:
      - untracked: true → git add 文件
      - hunks: "all" → git add 文件
      - hunks: [...] → 从原始 diff 按 hunk 序号提取 patch 并 git apply --cached
   c. 构造 commit message（type(scope): summary + body + breaking + signoff）
   d. git commit
5. git stash pop
6. 输出 PlanResult JSON（写入 plan.json 同目录的 plan-result.json）
```

## 输出 schema（`PlanResult`）

```typescript
interface PlanResult {
  ok: boolean;
  commits: {
    sha: string;
    message: string;
  }[];
  /** 本次执行未分配（跳过）的 hunks */
  unallocated_hunks?: {
    path: string;
    hunks: number[];
  }[];
  stash_pop_ok?: boolean;
  stash_conflicts?: string[];
  errors?: string[];
}
```

```json
{
  "ok": true,
  "commits": [
    { "sha": "abc123def456", "message": "feat(auth): add OAuth2 token validation\n\nSigned-off-by: User <user@example.com>" }
  ],
  "unallocated_hunks": [
    { "path": "internal/auth/handler.go", "hunks": [1] }
  ],
  "stash_pop_ok": true
}
```