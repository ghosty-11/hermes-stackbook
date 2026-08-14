<!-- TEMPLATE: copy for one drift boundary; do not fill in or run this template in place. -->
# Change-Drift Runbook — {System or artifact boundary}

> **Status:** Draft | Tested | Degraded | Retired  
> **Owner / active writer:** {one accountable identity}  
> **Trigger:** {scheduled check, release, deployment, incident, or observed mismatch}  
> **Intended outcome:** {authoritative, deployed, and resolved state agree where policy requires}  
> **Last field-tested:** {YYYY-MM-DD, environment, and evidence reference}  
> **Review by:** {YYYY-MM-DD}

## Scope, authority, and invariants

- **In scope:** {configuration keys, skills, plugins, extensions, policies, templates, generated files, or service units}
- **Out of scope:** {nearby state owned by another runbook}
- **May inspect:** {identity or role}
- **May reconcile:** {identity or role}
- **Approval gates:** {publication, restart, credential, destructive, or other gated steps}
- **Must remain true:** {availability, security, data, provenance, and single-writer invariants}
- **Do not operate during:** {active deployment, protected window, migration, or other conflicting writer}

## Authoritative and observed state

Name every layer separately. A repository file, deployed file, and running process are not interchangeable evidence.

| Layer | Identity or location | Expected revision/value | Observation method | Owner |
|---|---|---|---|---|
| Source artifact | {repository path, package, or immutable reference} | | | |
| Generated artifact | {if applicable} | | | |
| Deployed artifact | {installation or runtime-loaded path} | | | |
| Resolved runtime state | {effective config, loaded inventory, API, or user-visible behavior} | | | |
| Documentation or inventory | {record that must agree with reality} | | | |

## Drift classification

Classify before mutating. Do not assume that source is correct merely because it is version-controlled.

| Class | Meaning | Default response |
|---|---|---|
| Expected difference | Intentional environment-specific or generated variation | Record the reason and keep the check scoped to the invariant. |
| Source drift | Canonical source is stale or wrong | Correct source, review it, then redeploy through the normal path. |
| Deployment drift | Source is correct but the installed artifact differs | Redeploy from the pinned source; do not hand-edit the deployed copy. |
| Runtime drift | Files agree but effective behavior or loaded state differs | Diagnose precedence, cache, reload, process, or dependency state before changing source. |
| Documentation drift | Operational records disagree with authoritative or observed state | Correct the owning record and its validation contract. |
| Ownership conflict | Two sources claim authority for the same state | Stop mutation; choose one owner and retire the competing path. |
| False positive | The check compares a volatile or irrelevant property rather than the intended invariant | Fix the check and preserve the valid difference; never force state to satisfy a bad assertion. |
| Unknown | Evidence cannot attribute the mismatch | Stop at read-only diagnosis and escalate. |

- **Observed class:** {one class above}
- **Evidence:** {exact mismatch, timestamps, revisions, or effective values}
- **Reconciliation direction:** {source → deployment → runtime, runtime → reviewed source, documentation-only, or no mutation}
- **Why this direction is authoritative:** {owner, policy, approval, or decision record}

## Detection contract

- **Check:** `{deterministic command or query}`
- **Compared invariant:** {semantic value, normalized manifest, content hash, resolved inventory, or behavior}
- **Excluded volatile fields:** {timestamps, generated IDs, ordering, caches, or host-specific values}
- **Failure output:** {bounded diff with source and observed identities; no secrets}
- **Delivery:** {named operator surface for actionable drift}
- **Suppression/exception owner and expiry:** {who may accept a temporary difference and until when}

A healthy check is silent. It exits successfully without sending a routine notification. The check must fail on a reviewed broken fixture before it is trusted in automation.

## Safe prechecks

Record command, timestamp, and complete observed result.

1. `{confirm the active writer and repository cleanliness}`  
   Expected: {attributable baseline}.  
   Stop if: {unowned changes or another writer}.
2. `{capture source, deployed, and resolved identities independently}`  
   Expected: {enough evidence to classify drift}.  
   Stop if: {a layer cannot be observed safely}.
3. `{prove the rollback source is available}`  
   Expected: {immutable revision, backup, export, or package}.  
   Stop if: {rollback cannot restore the affected boundary}.

## Reconciliation procedure

1. **{Correct the authoritative layer or select the approved source revision}.**  
   Action: `{exact action}`  
   Evidence: {reviewed diff, revision, or approval}.  
   Stop if: {authority or attribution changes}.
2. **{Regenerate or deploy through the normal installation path}.**  
   Action: `{exact action}`  
   Evidence: {deployed identity derived from the approved source}.  
   Stop if: {the installer would replace unrelated state or broaden access}.
3. **{Reload or restart only when the runtime requires it and authority permits}.**  
   Action: `{exact action or explicit no-reload rationale}`  
   Evidence: {new process/session/load identity}.  
   Stop if: {availability or approval gate is not satisfied}.
4. **{Update the owning documentation or inventory}.**  
   Action: `{exact record update}`  
   Evidence: {record names the verified state without private data in public artifacts}.

## Independent verification

Observe the effective consumer, not only the files changed by the reconciliation.

| Outcome assertion | Independent check | Expected evidence |
|---|---|---|
| Source identity is approved and attributable | | |
| Deployed artifact derives from that source | | |
| Resolved runtime state uses the intended value/artifact | | |
| One representative user-visible behavior works | | |
| The drift check is silent on healthy state | | |
| A reviewed broken fixture still makes the check fail | | |
| No adjacent source or deployment path still competes | | |

## Rollback

- **Rollback trigger and deadline:** {condition and point of no return}
- **Recovery source:** {immutable revision, backup, or export}
- **Sequence:** {restore deployment, reload if required and authorized, verify effective state}
- **Rollback verification:** {independent consumer check}
- **Preserved evidence:** {diff, logs, revisions, and failed observations}

## Stop and escalate

| Condition | Stop before | Escalate to | Safe work while waiting |
|---|---|---|---|
| Authority is ambiguous or two sources claim ownership | Any mutation | {owner/operator} | Capture identities and bounded diffs. |
| Mismatch includes credentials or private data | Printing or committing evidence | {security owner} | Record only redacted metadata and affected boundary. |
| Reconciliation requires an unapproved restart, publication, or destructive action | Gated action | {approver} | Complete source correction and read-only checks that do not imply deployment. |
| Verification disagrees with file-level state | Further source edits | {runtime owner} | Diagnose precedence, caching, loaders, and process identity. |

## Evidence record

- Start/end time:
- Executor and approver:
- Source/deployed/resolved identities before and after:
- Drift classification and reconciliation direction:
- Commands/actions actually run:
- Evidence paths, run IDs, revisions, or hashes:
- Exceptions and expiry:
- Deviations from this runbook:
- Result: MET | PARTIALLY MET | NOT MET
- Residual risk and next review:

## Related records

{change runbook, operational runbook, service profile, policy, compatibility ledger, incident, or decision record}
