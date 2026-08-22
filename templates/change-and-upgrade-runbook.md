<!-- TEMPLATE: copy for a named state/version transition; do not use as a standing plan. -->
# Change Runbook — {System}: {Source state} → {Target state}

> **Status:** Proposed | Approved | In progress | Verified | Rolled back | Closed  
> **Change owner / active writer:** {one identity}  
> **Window:** {date/time/timezone or explicit no-window rationale}  
> **Approval:** {authority and evidence}  
> **Intended outcome:** {observable target state}  
> **Last rehearsed/tested:** {YYYY-MM-DD and environment}

## Scope and invariants

- Components changed:
- Components explicitly unchanged:
- Availability/data/security invariants:
- Out-of-scope adjacent work:

## Source and target identity

| Item | Before | Target | How verified |
|---|---|---|---|
| Version/commit/image | | | |
| Configuration schema | | | |
| Deployed artefacts | | | |

## Compatibility and seam watch

- Upstream changes reviewed:
- Local plugins/hooks/adapters/patches at risk:
- Deprecations/migrations:
- Credentials/provider compatibility:
- Required evaluations and checks:

## Authority and stop conditions

- May inspect:
- May stage:
- May mutate:
- May restart:
- Stop before:
- Escalate to:
- Safe work while waiting:

## Before-state evidence

- Repository cleanliness and ownership of existing changes:
- Config/export snapshot:
- Data/backup snapshot and recovery source:
- Service health baseline:
- User-visible path baseline:
- Rollback target proven available:

## Dry run or canary

- Method:
- Success criteria:
- What the canary does not cover:

## Change sequence

1. **{Action}.**  
   Command/action: `{exact action}`  
   Intermediate health gate: `{read-only check}`  
   Stop/rollback if: {condition}.

## Final verification

| Assertion | Check | Expected evidence |
|---|---|---|
| Target identity active | | |
| Dependencies connected | | |
| User-visible operation works | | |
| Guard/evaluation regressions absent | | |
| Source/deployed state attributable | | |

## Rollback

- Decision deadline / point of no return:
- Rollback trigger:
- Target version/config/data source:
- Sequence:
- Verification:
- If rollback is impossible:

## Observation and closure

- Observation window/signals:
- Known delayed failure modes:
- Result: MET | PARTIALLY MET | NOT MET
- Residual risk / pending evaluations:
- Evidence and log entry:
- Postmortem trigger:

## Related records

{service profile, operational runbook, incident state, policy, decision record}
