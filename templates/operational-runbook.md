<!-- TEMPLATE: copy to a live operations document; do not edit in place. -->
# Runbook — {Outcome}

> **Status:** Draft | Tested | Degraded | Retired  
> **Owner:** {one accountable person or role}  
> **Trigger:** {observable condition narrow enough for these steps}  
> **Intended outcome:** {observable final state}  
> **Last field-tested:** {YYYY-MM-DD, environment and evidence}  
> **Review by:** {YYYY-MM-DD}

## Scope and authority

- **Authoritative implementation:** {source repository/file and deployed path}
- **In scope:** {systems and failure class}
- **Out of scope:** {nearby cases requiring another runbook}
- **May execute:** {identity or role}
- **Permission gates:** {step and required approver}
- **Active writer:** one; name the writer before the first mutation

## Invariants and dependency windows

- **Must remain true:** {security, data, and independence properties recovery must preserve}
- **Do not operate during:** {active writer, dependency, or protected production window}

## Known limitations

- {what this runbook or its recovery source does not protect, prove, or reverse}

## Prerequisites

- {dependency, access path, recovery source, or credential reference — never secret material}

## Safe prechecks

Read-only checks. Record command, timestamp, and observed output.

1. `{command}`
   Expected: {observation}.  
   Stop if: {unexpected state}.

## Procedure

1. **{Action}.**  
   Command/action: `{exact action}`  
   Evidence: {what this produces}.  
   Stop if: {condition}.

## Verification

Verify independently of the mutation where possible.

| Outcome assertion | Check | Expected evidence |
|---|---|---|
| {user-visible/system state} | `{read-only check}` | {specific result} |

## Rollback

- **Rollback trigger:** {condition and deadline}
- **Recovery source:** {snapshot/commit/export and identity}
- **Steps:** {narrow inverse}
- **Rollback verification:** {final-state check}
- **No rollback:** if true, state why and escalate before the irreversible step

## Stop and escalate

| Condition | Stop before | Escalate to | Safe work while waiting |
|---|---|---|---|
| {ambiguity/failure} | {step} | {operator/owner} | {read-only evidence gathering} |

## Evidence record

- Start/end time:
- Executor and approver:
- Commands/actions actually run:
- Evidence paths/IDs/hashes:
- Deviations from this runbook:
- Result: MET | PARTIALLY MET | NOT MET

## Related records

{service profile, policy, diagnostic note, postmortem, decision}
