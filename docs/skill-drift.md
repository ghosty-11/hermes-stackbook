# Runbook — Detect and reconcile skill drift

Use this runbook when a skill source changes, a harness upgrade changes discovery, an expected skill is missing, a name resolves to the wrong source, or selection behavior changes. Record deployment-specific paths and identities in a private copy, not in this public guide.

## Scope and authority

- **In scope:** Agent Skills source directories, frontmatter, discovery settings, filters, source precedence, installed copies or links, and harness-rendered selection behavior.
- **Out of scope:** judging whether a skill's advice is useful; use a behavioral evaluation for that.
- **Active writer:** one person or agent owns source and deployment mutation.
- **Approval gates:** remote publication, service restart, credential changes, destructive cleanup, and replacing an artifact with unknown provenance remain separately authorized actions.

## Source, discovered, and exercised state

| Layer | Record | Evidence |
|---|---|---|
| Canonical source | Repository, revision, skill directory, `SKILL.md` identity | Clean attributable revision and file content |
| Discovery policy | Enabled roots, source toggles, include/ignore filters, precedence | Effective harness configuration, not only a config file |
| Discovered skill | Resolved name, description, provider/source, path | Fresh-process inventory or direct skill URL resolution |
| Exercised behavior | Direct load, positive selection, nearby negative selection | Tool/event transcript and resulting work |

List duplicate names and name collisions explicitly. A valid source file is not proof that the intended loader won precedence.

## Detection contract

A deterministic check should:

1. enumerate one-level skill directories under each authoritative root;
2. require `SKILL.md`, matching directory/frontmatter names, and a meaningful description;
3. compare the authoritative root with effective discovery settings and filters;
4. detect duplicate names and report both source paths;
5. compare installed copies or links with their canonical sources;
6. start a fresh harness process and resolve at least one changed skill;
7. omit bodies, credentials, and private paths from public reports.

A healthy drift check is silent. Before scheduling it, prove a missing file, wrong name, conflicting source, or wrong deployment makes it fail.

## Safe prechecks

1. Record the installed harness version and its current skill/discovery help.
2. Confirm repository cleanliness and identify any existing writer.
3. Capture effective roots, toggles, filters, and precedence.
4. Inventory source and deployed skill names without loading untrusted bodies into a privileged context.
5. Preserve the current revision or deployment artifact as the rollback source.

Stop before mutation when ownership is ambiguous, a second source claims authority, or the resolved source cannot be observed.

## Reconciliation

1. **Classify the mismatch.** Choose source, deployment, discovery-policy, runtime, documentation, or false-positive drift.
2. **Select the authoritative direction.** Do not assume the repository is right merely because it is version-controlled.
3. **Add or update a failing contract.** Assert the intended name, source, filter, or forbidden stale path and observe it fail.
4. **Correct the canonical source or discovery policy.** Remove obsolete competing copies and paths only after provenance is established.
5. **Deploy through the normal installer or documented discovery root.** Do not hand-edit a generated or installed copy.
6. **Start a fresh harness process.** Existing sessions may retain their startup inventory.
7. **Update private deployment records.** Keep environment-specific paths out of public artifacts.

## Independent verification

For every changed skill:

- resolve its direct skill URL or command in a fresh harness process;
- confirm the resolved source is the intended canonical revision;
- run one realistic prompt that should select it;
- run one close prompt that should not select it;
- inspect the resulting behavior, not only a model claim that the skill was used;
- rerun the deterministic suite and the planted broken fixture;
- confirm no obsolete source remains eligible.

Record MET, PARTIALLY MET, or NOT MET. A direct load without positive and nearby negative selection is PARTIALLY MET, not complete selection evidence.

## Rollback and escalation

Rollback restores the prior source revision, discovery policy, and deployed artifact, then starts another fresh harness process and repeats direct resolution. Stop and escalate before deleting unknown copies, weakening a detector to accept unexplained drift, or restarting a harness/service without authority.

Related: [Skills and plugins](skills-and-plugins.md) · [Verification](verification.md) · [Change-drift template](../templates/change-drift-runbook.md)
