# Runbook — Detect and reconcile extension and file drift

Use this runbook when an extension, plugin, hook, profile, generated file, service unit, or other deployed artifact may differ from its canonical source or from what a running consumer loaded. Record real paths, identities, and service names only in a private deployment copy.

## Scope and authority

- **In scope:** canonical source, generated output, installed files or links, effective loader configuration, loaded runtime identity, and one representative behavior.
- **Out of scope:** credentials, mutable databases, user content, and migrations that need domain-specific consistency or backup procedures.
- **Active writer:** one identity owns reconciliation across source and deployment.
- **Approval gates:** publication, restart, availability change, destructive replacement, permission broadening, and credential access remain separate operator decisions.

## Source, deployed, loaded, and exercised state

| Layer | Record | Evidence |
|---|---|---|
| Canonical source | Repository, revision, source path, owner | Clean attributable revision |
| Generated artifact | Generator/version and reproducible input, if applicable | Regeneration command and normalized comparison |
| Deployed artifact | Destination, type, owner/mode, link target or content identity | Filesystem observation |
| Loader policy | Search path, manifest, enablement, precedence | Effective configuration |
| Loaded runtime | Process/session/version and loaded extension identity | Loader inventory, startup event, or status API |
| Exercised behavior | One consumer-visible operation | Observed result independent of deployment command |

A matching source and destination hash does not prove a running process loaded that file. A different hash is not drift when the destination contains documented generated or environment-specific fields.

## Detection contract

Choose the narrowest stable invariant:

- resolve symlinks and compare canonical targets when links are the deployment contract;
- compare content hashes only for byte-identical immutable copies;
- normalize documented volatile fields before comparing generated artifacts;
- compare manifests, enablement, precedence, owner, and mode when those control loading;
- observe the loaded identity or behavior when the runtime can cache files;
- report a bounded diff without secrets or complete private configuration.

A healthy drift check is silent. Prove it fails on a reviewed wrong target, modified copy, missing manifest entry, or stale loaded process before scheduling it.

## Safe prechecks

1. Identify the canonical owner and current source revision.
2. Confirm repository and deployment ownership; stop if another writer is active.
3. Capture source, generated, deployed, loader, and loaded identities independently.
4. Determine whether the destination should be a link, immutable copy, generated file, or local configuration.
5. Prove a rollback artifact exists and note whether a reload or restart is required.

Do not replace an unknown file merely because its name matches the expected destination.

## Reconciliation

1. **Classify the mismatch.** Source, generation, deployment, loader, runtime cache, documentation, ownership conflict, or false positive.
2. **Choose the authoritative direction.** Runtime-to-source recovery is valid only after human review; source-to-runtime is not automatically correct.
3. **Add or update a failing contract.** Observe the intended broken fixture fail.
4. **Correct the canonical owner.** Remove competing ownership rather than adding another synchronization path.
5. **Use the normal installer or deployment path.** Preserve mode, ownership, and atomic-replacement guarantees; never patch the deployed copy by hand.
6. **Reload only when required and authorized.** A source change or symlink update may affect a new session without a service restart; prove the actual loader behavior.
7. **Update the private inventory and compatibility record.** Public documentation contains portable procedure, not production topology.

## Independent verification

- compare the canonical and deployed identities using the artifact's declared invariant;
- confirm loader configuration resolves the intended path and no higher-precedence competitor exists;
- start a fresh session or inspect a new process when startup loading is involved;
- exercise one consumer-visible behavior through the real surface;
- confirm the healthy detector is silent;
- rerun the reviewed broken fixture and confirm it still fails;
- record any untested restart, delayed load, or scheduled natural-fire path as a residual gap.

A successful installer exit without loaded identity and consumer-visible behavior is PARTIALLY MET.

## Rollback and escalation

Rollback restores the prior artifact and loader policy, performs only the authorized reload, and repeats the independent consumer check. Stop and escalate when provenance is unknown, a credential-bearing file would enter evidence, a detector compares undocumented volatile state, or reconciliation requires an unapproved restart or destructive replacement.

Related: [Operations](operations.md) · [Verification](verification.md) · [Change-drift template](../templates/change-drift-runbook.md)
