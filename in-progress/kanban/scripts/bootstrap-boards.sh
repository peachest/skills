#!/usr/bin/env bash
# Bootstrap the four-board effort kanban topology (idempotent).
# Reads runtime.conf (see runtime.conf.example) for environment-specific values.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[ -f "$DIR/runtime.conf" ] && . "$DIR/runtime.conf"

BOARDS_DIR="${BOARDS_DIR:-$HOME/boards}"
PROXY_URL="${PROXY_URL:?set PROXY_URL in runtime.conf}"
DEPLOY_CLUSTER="${DEPLOY_CLUSTER:?set DEPLOY_CLUSTER in runtime.conf}"

DISC='纪律：结果先 `board comment` 汇报再 `board done`；--outcome ok=阶段目标达成，fail=未达成（自动流入 Blocked）；禁止自行 move/cancel/retry 自己的卡。'
P_WAY="执行 /skill:wayfinder：从卡描述的输入指针（issue/文档）出发，产出 wayfinder map（决策树+Fog 清单），写入仓库 docs/research/ 或 .scratch/ 对应位置，map 路径写进 comment。$DISC"
P_GRILL="执行 /skill:grilling：对卡描述列出的决策点逐轮 grilling 用户（每轮 2-3 问，在本卡 pane 内对话）；拍板结论与未决项写入 comment。决策全部收敛 → done ok；有未决阻塞 → fail。$DISC"
P_SPEC="串行执行三步：① /skill:to-spec 将 comment 中 map/grilling 产物整理为 spec；② /skill:review-spec 审查，Held gap 修复后复审；③ /skill:to-tickets 切票写回 issue-tracker。spec 路径 + 票号写 comment。$DISC"
P_IMPL="执行 /skill:implement-spec-in-pipeline implementer：领取卡描述指针指向的 spec 与 tickets，完成实现与测试；遵守仓库纪律（领票/分支/提交规范）。改动清单+测试结果写 comment。$DISC"
P_E2E="端到端验证：① 用仓内 Dockerfile 或 Dockerfile.local 本地构建（buildkitd 已就绪；sudo nerdctl 管理镜像，禁 docker；代理 $PROXY_URL 四参数）；② 执行 /skill:argocd-ops 部署到 $DEPLOY_CLUSTER 本地集群验证；③ pod 状态/探针/关键功能冒烟结果写 comment。构建或部署验证失败 → done fail。$DISC"
P_CR="代码评审：用 ocr CLI（内部 open-code-review）评审卡 comment 中 MR/diff 指针指向的改动；severity 分组输出，low 丢弃；无 critical/high/medium → done ok；有 → 修复方案建议写 comment + done fail。$DISC"
P_MR="执行 /skill:create-mr：基于卡 comment 指向的分支创建 draft MR（提交作者邮箱按仓库远端规范），MR 链接写 comment；卡停在 awaiting 等人评审，不要自行推进。$DISC"
P_RETRO="执行 /skill:retro：对本 effort 全程（board comment 链 + 相关 session）复盘，改进项沉淀到对应 skill/wiki/AGENTS.md，复盘摘要写 comment。$DISC"

P="--project $BOARDS_DIR"
mkdir -p "$BOARDS_DIR"
board project create "$BOARDS_DIR" >/dev/null 2>&1 || true

mkboard() { # $1 name -> echoes board id
  local id
  id=$(board $P board list --json 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
m=[b['id'] for b in (d if isinstance(d,list) else d.get('boards',[])) if b['name']=='$1' and not b.get('archived_at')]
print(m[0] if m else '')")
  if [ -z "$id" ]; then
    id=$(board $P board create "$1" --json | python3 -c "import json,sys; print(json.load(sys.stdin)['board']['id'])")
  fi
  echo "$id"
}

col() { # board_id name trigger position [extra args...]  — create if missing, prints col id
  local B=$1 NAME=$2 TRIG=$3 POS=$4; shift 4
  board $P board select "$B" >/dev/null
  local id
  id=$(board $P column list --json 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
m=[c['id'] for c in (d if isinstance(d,list) else d.get('columns',[])) if c['name']=='$NAME']
print(m[0] if m else '')")
  if [ -z "$id" ]; then
    id=$(board $P column create --name "$NAME" --trigger "$TRIG" --position "$POS" "$@" --json | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
  fi
  echo "$id"
}

flow_board() { # $1 runtime ; one 11-column board, full pipeline same-board
  local B IMPL E2E CR MR RETRO DONEC BLK
  B=$(mkboard "$1")
  board $P board select "$B" >/dev/null
  board $P column delete Todo --yes >/dev/null 2>&1 || true
  col "$B" Backlog manual 0 >/dev/null
  local WAY GRILL SPEC
  WAY=$(col "$B" Wayfinder auto 1 --fresh-session)
  GRILL=$(col "$B" Grilling auto 2 --fresh-session)
  SPEC=$(col "$B" Spec auto 3 --fresh-session)
  IMPL=$(col "$B" Implement auto 4 --fresh-session)
  E2E=$(col "$B" "E2E Tests" auto 5 --fresh-session)
  CR=$(col "$B" "Code Review" auto 6 --fresh-session)
  MR=$(col "$B" "MR & Human Review" auto 7 --fresh-session)
  RETRO=$(col "$B" Retro auto 8 --reuse-session)
  DONEC=$(col "$B" Done manual 9)
  BLK=$(col "$B" Blocked manual 10)
  board $P column edit "$WAY" --prompt "$P_WAY" --on-success Grilling --on-fail Blocked --json >/dev/null
  board $P column edit "$GRILL" --prompt "$P_GRILL" --on-success Spec --on-fail Blocked --json >/dev/null
  board $P column edit "$SPEC" --prompt "$P_SPEC" --on-success Implement --on-fail Blocked --json >/dev/null
  board $P column edit "$IMPL" --prompt "$P_IMPL" --on-success "E2E Tests" --on-fail Blocked --json >/dev/null
  board $P column edit "$E2E" --prompt "$P_E2E" --on-success "Code Review" --on-fail Blocked --json >/dev/null
  board $P column edit "$CR" --prompt "$P_CR" --on-success "MR & Human Review" --on-fail Blocked --json >/dev/null
  board $P column edit "$MR" --prompt "$P_MR" --on-fail Blocked --json >/dev/null
  board $P column edit "$RETRO" --prompt "$P_RETRO" --on-success Done --on-fail Blocked --json >/dev/null
  echo "$1=#$B"
}

for RT in agent dev; do flow_board "$RT"; done
echo "topology ready at project $BOARDS_DIR"
