---
name: knowledge-impact
description: Answer "改 X 会影响谁" / "谁在用 Y" / "X 的上下游是什么" for cross-repo and platform questions by looking up curated knowledge catalogs first (llmops-wiki catalog views + entity-alias), falling back to CodeGraph live queries, and writing confirmed findings back. Use when the question spans repos (CRD field readers/writers, chart value consumers, platform API routes, entity aliasing, deploy→image→source-repo mapping), when CodeGraph is unavailable or would only answer half, or when the user asks 影响面 / 谁读写 / 调用链 in the kgpu/llmops domains.
---

# Knowledge Impact

Catalog-first impact lookup. Single-repo symbol questions stay with CodeGraph (the `codegraph_callers`/`codegraph_impact` tools); this skill handles the questions CodeGraph cannot see: **cross-repo contracts, non-code assets (fields, values, routes, devices), and platform components**.

## Lookup order (catalog → live → write-back)

### Step 1 — Read the catalog

The curated catalogs live in `~/projects/llmops-wiki/catalog/` and `~/projects/llmops-wiki/silver/entity-alias/`. Match the question to a view:

| 问题形态 | 查哪里 |
|---|---|
| 改 CRD 字段影响谁（如 `spec.mode`、`devmem`） | `catalog/views/crd-field-matrix.md` |
| 改 chart value 影响哪个模板/组件 | `catalog/views/chart-values.md` |
| 平台某页面/接口打到哪个后端 | `catalog/views/llmops-api-routes.md` |
| 这个设备/组件在各系统叫什么（别名互查） | `silver/entity-alias/index.md`（含 4 陷阱） |
| 某部署跑的什么镜像、源码仓在哪 | `silver/entity-alias/index.md` §4 |
| 跨仓语义（单位/切分/计费含义） | `../gold/<topic>/` fallback `../silver/<topic>/`（经 RESOURCES.md 路由） |

Also grep the whole catalog when the question doesn't map cleanly:

```bash
rg -il '<资源名或组件名>' ~/projects/llmops-wiki/catalog/ ~/projects/llmops-wiki/silver/entity-alias/
```

Catalog hit → report with the source anchor (file + line the view records), then **spot-check one anchor** (`sed -n '<line>p'` in the owning repo) before staking a conclusion on it — views are regenerated artifacts, check the freshness stamp in frontmatter `updated:`.

### Step 2 — Fall back to live queries

Catalog miss (or stale) → answer it live, per question type:

- **Single-repo symbol flow** → CodeGraph tools (`codegraph_callers`, `codegraph_impact`, `codegraph_explore`).
- **CRD field readers/writers** → JSON-tag grep across repos (`rg '"<jsonTag>"' <repo> -t go`), mirroring `catalog/scripts/gen-crd-view.py`'s method.
- **Platform entity resolution** → live kubectl/Prom queries (never trust cached instance state; see entity-alias frontmatter note).
- **Chart value consumers** → `rg '\.Values\.<key>' <chart>/templates/`.

Present the live answer, marked as "现查"（非目录）。

### Step 3 — Write back (consumption is sedimentation)

A live answer worth keeping is one line in the catalog, not a session memory:

- New field/alias/route confirmed by evidence → append to the matching view (or `scripts/seed.json` for hand-curated columns), with the `文件:行号` anchor and today's date.
- Correction (catalog said X, live says Y) → fix the view in place and note the drift in the view's frontmatter `updated:`.
- New trap (name said X, actually Y) → `silver/entity-alias/` 陷阱 list, same style as the existing four.

Then re-run `bash ~/projects/llmops-wiki/catalog/scripts/lint-catalog.sh` before committing the catalog change.

## Boundaries

- **Never answer instance state from the catalog** ("who is running now" → live kubectl). Catalogs hold stable mappings only — this is the freshness rule from the research it came from.
- **Semantic questions** (what does devmem mean, how is GPU-equivalent billed) route to okb gold/silver via `RESOURCES.md`, not the catalog — the split is: 语义归 okb，影响面归 catalog.
- Do not create new views unilaterally; a new view type (like the existing three) deserves a user decision first.

## Done when

- [ ] Question answered from catalog with anchor spot-check, or from live query marked as such, or honestly "两处都没有" (then consider whether a new view row is warranted)
- [ ] Any confirmed new fact written back with anchor + date, lint green
- [ ] Semantic/impact questions not conflated (okb vs catalog routing respected)
