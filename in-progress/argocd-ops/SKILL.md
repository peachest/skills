---
name: argocd-ops
description: Operate an ArgoCD deployment on a Kubernetes cluster from the CLI — check application sync/health status, trigger hard refresh or sync, diff, and diagnose stuck OutOfSync apps. Use when the user mentions ArgoCD, GitOps sync, a chart version published but not appearing on the cluster, or asks to refresh/sync/diff/inspect an ArgoCD application.
version: 0.1.0
---

## Environment binding

Every command reads `<SKILL_DIR>/.env`. On first use, if `.env` is missing, copy `.env.example` to `.env` and fill it for the target cluster (kubectl is needed to discover the Service address and, optionally, credentials).

Load it once per session:

```bash
set -a; source <SKILL_DIR>/.env; set +a
```

Completion criterion: `ARGOCD_SERVER`, `ARGOCD_USERNAME`, `ARGOCD_PASSWORD`, `KUBECTL` are all non-empty.

## Playbook

### 1. Status check — no login needed

kubectl reads the Application CR directly; this is the fastest path and needs no ArgoCD auth:

```bash
$KUBECTL -n $ARGOCD_NS get application <app> -ojson | python3 -c "
import json,sys
a=json.load(sys.stdin); st=a.get('status',{})
print('sync:',st.get('sync',{}).get('status'),'| health:',st.get('health',{}).get('status'))
for r in st.get('resources',[]):
    if r.get('status')!='Synced':
        print(f\"  {r.get('kind')}/{r.get('name')}: {r.get('status')}\")"
```

Also read `status.conditions` — warnings such as RepeatedResourceWarning surface there.

Also read `status.operationState.finishedAt` and `spec.syncPolicy` (automated / prune / selfHeal). `finishedAt` answers "did a sync run at the moment my manual kubectl change mysteriously disappeared" — correlate it with your own change timestamps. `syncPolicy` answers "will my out-of-band change survive": automated + prune means the next sync reclaims it, selfHeal=false only means it waits for a git change.

Completion criterion: sync status, health status, the full list of not-yet-synced resources, the last operation time, and the sync policy are stated.

### 2. Login — only when the CLI is needed (diff, manual sync, app create)

```bash
$ARGOCD_BIN login $ARGOCD_SERVER --username $ARGOCD_USERNAME --password "$ARGOCD_PASSWORD" \
  $( [ "$ARGOCD_INSECURE" = true ] && echo --insecure ) \
  $( [ "$ARGOCD_GRPC_WEB" = true ] && echo --grpc-web )
```

The context persists in `~/.argocd/config` — later sessions skip login. If login fails with `Invalid username or password`, the real password was rotated: ask the cluster operator; do not trust `argocd-initial-admin-secret` blindly (it can be stale).

Completion criterion: `argocd app list` returns the application table.

### 3. Hard refresh — after a same-version chart republish

**The pitfall:** when a chart repo re-publishes a chart under a version tag ArgoCD already tracks (common with dev tags like `0.0.0-dev`), ArgoCD's version cache sees an unchanged version string and reports `Synced` — while the package content actually changed. Nothing deploys until the cache is bypassed.

Trigger a hard refresh (no login needed — it goes through the Application CR):

```bash
$KUBECTL -n $ARGOCD_NS patch application <app> --type merge \
  -p '{"metadata":{"annotations":{"argocd.argoproj.io/refresh":"hard"}}}'
```

Then re-read status (step 1). With auto-sync enabled the app converges by itself; sync typically completes within a minute or two, during which brief OutOfSync/Degraded states are normal — wait one auto-sync cycle before diagnosing further.

Completion criterion: app reaches its post-refresh steady state (Synced again, or a stable list of genuinely conflicting resources).

### 4. Manual sync

For apps with auto-sync, a hard refresh (step 3) is enough — syncing follows automatically. Only when sync policy is manual:

```bash
$ARGOCD_BIN app sync <app>
```

Completion criterion: `sync: Synced` from step 1, and the expected resource (e.g. a CRD) verified present on the cluster with `$KUBECTL get <resource>`.

### 5. Diff

```bash
$ARGOCD_BIN app diff <app>          # exit 0 + empty output = fully converged
```

If the local machine cannot reach the ArgoCD server, run the same command inside the argocd-server pod — it bundles the CLI:

```bash
$KUBECTL -n $ARGOCD_NS exec deploy/argocd-server -- \
  argocd app diff <app> --server localhost:8080 --plaintext
```

Completion criterion: the actual resource-level differences are shown (or convergence confirmed by empty output).

## Pitfalls

### Same-version republish

Chart re-published under an existing version tag → ArgoCD cache stale → app `Synced` but cluster lacks the new content. Symptom: published chart has resource X, `kubectl get` says X not found, app shows Synced. Fix: hard refresh (playbook step 3).

### Chart chain

Umbrella charts nest subcharts (`<umbrella>/charts/<sub>/charts/<subsub>/`), and each level may pin its own copy. When a change deep in the chain does not appear, verify the chain package by package: download each chart tarball, untar, and check the target file exists in the nested subchart directory. A chart repo's `index.yaml` records `created` timestamps per version — under same-version republish this timestamp is the only freshness signal. Fix stale links at the level that repackaged with an old dependency.

### Field-owner deadlock

A resource shows one resource permanently OutOfSync while `kubectl apply --dry-run=server` on the chart's version succeeds, and the only diff is a field the chart no longer declares (e.g. a leftover `spec.conversion`). Cause: a previous field manager (helm, manual apply) owns that field; ServerSideApply cannot remove fields it does not own. Diagnose by diffing the full live JSON (`-ojson`, strip `status` and metadata noise) against the chart source. Fix by removing the stale field explicitly:

```bash
$KUBECTL patch <resource> --type=json -p '[{"op":"remove","path":"<field-path>"}]'
```

### Duplicate resource definition

`RepeatedResourceWarning` in app conditions: the same resource is defined twice among the app's sources (typical: the same CRD in both the umbrella chart and a subchart). The conflicting definitions can hold the resource OutOfSync indefinitely. This is a chart packaging bug, not an ArgoCD setting — fix the chart, deduplicate the resource.

### Auto-sync vs out-of-band kubectl on shared objects (the testing trap)

When a cluster hosts both an ArgoCD-managed app and kubectl-direct test deployments that share **fixed-name cluster-scoped objects** (webhook configurations, ClusterRoles, CRDs — names not derived from the release name), every git-triggered sync:

1. reverts the shared objects to the chart's declared state (rolling back manual patches), and
2. with `prune: true` + `CreateNamespace: true`, can prune a whole test namespace the app does not know about.

Symptom: manual changes vanish minutes after being applied, or old field values (e.g. a months-old caBundle) reappear. Forensics: compare `status.operationState.finishedAt` with your change timestamps; check `managedFields` for the rewriting owner (argocd-controller Apply).

Fix for the testing window: disable auto-sync first, deploy, test, then re-enable. The `argocd app set <app> --sync-policy none` CLI call **fails on multi-source apps** ("Source position should be specified") — patch the Application CR instead:

```bash
$KUBECTL -n $ARGOCD_NS patch application <app> --type=json \
  -p '[{"op":"replace","path":"/spec/syncPolicy","value":{<same syncOptions, no "automated">}}]'
```

Re-enable by restoring the original `syncPolicy` (read it before patching!). Long-term fix: charts should derive the shared object names from the release (webhookNameOverride etc.) so test and prod deployments never collide.

### Helm hook jobs re-run on every sync

`helm.sh/hook: post-install,post-upgrade` jobs (certgen and friends) re-run whenever ArgoCD syncs the chart. Their side effects (writing caBundle, creating secrets) overwrite whatever another owner wrote since the last sync. Symptom signature: a certificate's notBefore date suddenly steps backwards. When diagnosing webhook TLS issues after a sync, check whether a hook job ran.

### cert-manager cainjector rewrites caBundle behind your back

A webhook configuration annotated `cert-manager.io/inject-ca-from` gets its `clientConfig.caBundle` continuously rewritten by the cainjector — ANY value you or a certgen job write there is reverted within seconds. Symptom: you patch caBundle with the right CA, read it back, and it is the old CA again. Forensics: `managedFields` shows `cert-manager-cainjector Update` owning `clientConfig`. Fix: remove the annotation (`kubectl annotate <webhookconfig> cert-manager.io/inject-ca-from-`) — only then can another owner hold the field. Note the annotation can come from the chart's default `injectCert: CertManager` value and survives kubectl apply of a manifest rendered with a different value (annotations not in last-applied are preserved).

### Stale admin secret

`argocd-initial-admin-secret` holds the install-time password and is not updated when the password is changed afterwards. On `Invalid username or password`, get the real credential from the cluster operator instead of re-reading the secret.
