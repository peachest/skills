## 2026-09-22 drift log (orca app 1.4.2xx, verified live on kube-nodexpu-manager #34 spawn)

1. `worker-start` rejects creation flags (`--name`, `--setup`, `--repo`, `--base-branch`, `--display-name`, `--comment`) for existing worktrees — pass only `--task --worktree --agent`.
2. `run-create --json`: real run id at `.result.run.id` (`run_*` prefix); top-level `.id` is the mutation-request uuid. Accept only `run_*` ids.
3. `worktree list` fs-watch lag: retry path resolution 10x1s after `wt switch -c`.
4. First verified end-to-end spawn: run `run_b9eb50bb268d` → task `task_d6297548ab9f` → dispatch `ctx_e657a446d46f` → worker terminal `term_f85bd7be`.
5. Fencing recovery on the same spawn (run-create probe rebound the coordinator terminal): `run-use --id <run> --from <coordinator-handle>` restores binding; the worker_done sat in the probe Run's inbox, invisible to run-scoped `check` but visible via global `orchestration inbox`; run-scoped `check --ack` on it returns `stale_delivery` (harmless — content already retrieved). Worker completed ticket #34 in ~4 min (commit 4a71dbc, all gates green).
