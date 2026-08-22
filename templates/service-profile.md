<!-- TEMPLATE: copy for one live service/system; reconcile fields against live state. -->
# Service — {Name}

> **Purpose:** {one sentence}  
> **Owner:** {one accountable person/role}  
> **Status:** Active | Degraded | Retired  
> **Criticality:** {what fails if unavailable}  
> **Last reconciled with live state:** {YYYY-MM-DD and how}  
> **Review by:** {YYYY-MM-DD}

## Consumers and boundaries

- Human/agent consumers:
- Trust boundary:
- Exposed surfaces:
- Data classification:

## Dependencies and dependants

| Direction | Service/system | Contract | Failure effect |
|---|---|---|---|
| Depends on | | | |
| Used by | | | |

## Runtime identity

- Host/container/user:
- Service manager and unit:
- Version/image/commit source:
- Network bindings:
- Resource limits:

## Configuration, data, and credentials

- Configuration source:
- Deployed path:
- Persistent data:
- Secret references/owner — never secret values:
- Source/deployed parity check:

## Health and observability

| Signal | Safe check | Healthy result | Evidence location |
|---|---|---|---|
| Process/unit | | | |
| Functional probe | | | |
| Logs/metrics/traces | | | |
| User-visible path | | | |

## Operations and authority

- Start/stop/restart command:
- Who may execute:
- Permission/restart gate:
- Drain or dependency window:
- Relevant runbooks:

## Backup and recovery

- Data included/excluded:
- Recovery source and encryption/credential dependency:
- Restore ordering:
- Last restore test and evidence:

## Known failure modes

| Symptom | Likely cause | Safe discriminator | Runbook/escalation |
|---|---|---|---|
| | | | |

## Change lifecycle

- Upstream/source owner:
- Update mechanism:
- Local seams/forks:
- Compatibility checks:
- Last change and evidence:

## Open risks

- {risk, state, owner, and next action}

## Related records

{operational runbook, change runbook, policy, incident, postmortem}
