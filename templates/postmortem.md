<!-- TEMPLATE: copy after a resolved real incident or explicitly named exercise. -->
# Postmortem — {Incident}

> **Incident date:** {YYYY-MM-DD}  
> **Postmortem owner:** {one owner}  
> **Status:** Draft | Reviewed | Actions open | Closed  
> **Incident state record:** {reference}  
> **Review date:** {YYYY-MM-DD}

## Summary

{What happened, contributing mechanism, duration, and impact in two or three sentences.}

## Impact

Use measured values. Write `unknown` with the missing evidence rather than inventing zero.

| Measure | Value | Evidence |
|---|---:|---|
| Start/end of impact | | |
| Users/systems affected | | |
| Data loss or exposure | | |
| Missed deliveries/jobs | | |
| Recovery time | | |

## Detection

- First signal:
- Who/what detected it:
- What should have detected it but did not:
- Detection delay and evidence:

## Evidence-linked timeline

| Time | Event | Evidence |
|---|---|---|
| | | |

## Contributing factors and root cause

- **Direct cause:** {supported mechanism}
- **Contributing conditions:** {conditions that widened impact or delayed recovery}
- **Root-cause confidence:** VERIFIED | LIKELY | UNVERIFIED
- **Not claimed:** {deeper cause not supported by evidence}

Avoid “human error” as a terminal cause. Identify which interface, control, or recovery path made the action consequential.

## Response

- What restored service:
- What went well:
- What hindered response:
- Runbook deviations:
- Evidence preserved:

## Corrective actions

| Action | Owner | Priority | Verification / close condition | Status |
|---|---|---|---|---|
| | | | | Open |

Actions should prevent recurrence, shorten detection/recovery, or make the next response safer. “Be careful” is not an action.

## Residual risk and rejected work

- Accepted residual risk:
- Recommendation rejected/deferred and why:
- Revisit trigger:

## Definition of done

- [ ] Impact and timeline evidence reviewed
- [ ] Root-cause claim matches its confidence
- [ ] Every action has an owner and executable close condition
- [ ] Relevant runbooks, service profiles, and checks updated or consciously left unchanged
- [ ] Outcome reported MET | PARTIALLY MET | NOT MET

## Related records

{incident state, operational runbook, service profile, decision record}
