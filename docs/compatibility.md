# Compatibility ledger

> **Skip this while evaluating.** It records what the guide was checked against, not steps you
> perform. In the table below, *runtime smoke* means the author exercised that behaviour on a
> real host — it does not mean every clean installation has been tested.

This ledger records what the guide was checked against. Readers do not need to reproduce or complete it to deploy the stack; it exists to track the guide's review boundary and verify compatibility claims over time. It is evidence scope, not a promise that every combination works.

## Evidence levels

- **Reference recorded:** an upstream revision was pinned so later readers can reproduce the review boundary.
- **Source reviewed:** the named documentation or source seam was read at that revision.
- **Runtime smoke:** the named component path was exercised on a real host.
- **Golden path:** a clean-host deployment completed the minimum private-stack acceptance scenarios.

Do not upgrade a row's evidence level because configuration parsed or a process started.

## Current ledger

| Guide state | Hermes reference | OMP reference | Evidence | Checked |
|---|---|---|---|---|
| Current private candidate | [`bfff32ae8c6a`](https://github.com/NousResearch/hermes-agent/commit/bfff32ae8c6a9c585431997a6cc3d791b6ec9af5) | [`448632b8190e`](https://github.com/can1357/oh-my-pi/commit/448632b8190eac71b8e187880bea234a513773df) | Reference recorded; selected official documentation and source seams reviewed at the pinned revisions, including OMP advisor behavior. Hetzner model availability and publication documentation, links, diagrams, dependency audit, and full-history secret scan checked. No clean-host golden path claimed. | 2026-08-14 |
| Author's field deployment (ahead of the review anchor) | [`27fddcbe5`](https://github.com/ghosty-11/hermes-agent/commit/27fddcbe5df9c5e8408c44ca17510205ab458efe) (public downstream fork; official `45af7a71f` merged 2026-08-15) | OMP release `17.3.4` (native binary) | Runtime smoke: the architecture in this guide is operated live at these revisions — multiplexed gateway with an explicit profile allowlist, per-profile cron scheduling, behavioral eval runner, staged-database backups, and a restore drill all exercised on a real host, across a 655-commit framework advance applied the same day. The advance was gated on a full upstream suite run whose failures were proven identical against official `main` in a control worktree (no regression attributable to the downstream merge), and the deployment's own structural guard returned to its exact pre-update result. Not a clean-host golden path, and not a re-review of the pinned anchor's documentation. | 2026-08-15 |

The source heads above are comparison anchors. Provider catalogs, hosted documentation, free tiers, and installed CLIs may change without either repository revision changing.

## Release update procedure

For each guide release:

1. Record exact Hermes and OMP source revisions before editing behavior claims.
2. Re-read the installed CLI `--help` for every changed command family.
3. Re-check every changed official source and provider page.
4. Run the repository documentation workflow locally.
5. Record which runtime scenarios were actually exercised; leave the rest at the lower evidence level.
6. Tag the guide release only after the ledger describes the evidence that exists.

When the deferred clean-host reference deployment is completed, add a new row rather than rewriting the source-review row into stronger evidence.
