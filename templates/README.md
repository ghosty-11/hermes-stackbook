# Documentation templates

> **First trial: copy nothing.** For a real deployment, start with the
> [deployment checklist](deployment-checklist.md) and [profile matrix](profile-matrix.md); add
> runbooks only once a service has a named owner.

These public-safe templates turn recurring operational work into reviewable records. Copy the narrowest template that matches the reader's job; never fill a template in place.

## Install into your operational knowledge base

If operators or agents rely on an LLM-maintained wiki, copy only the runbooks, templates, and
worksheets they will use into that private knowledge base. Do not bulk-import the library.
Link each installed copy from the local runbook or template index so normal agent search can
find it without depending on this checkout or an external URL.
Use the [proposed wiki structure](../docs/knowledge-base-structure.md) as a placement guide,
not as a requirement to create folders with no documents or reader.

Adapt each installed copy before treating it as operational: replace generic fields with the
real owners, paths, approval gates, rollback sources, verification commands, and related local
records. Preserve this repository's source URL or revision for provenance, but keep private
topology and credentials in the private copy. After field use, repurpose, shorten, or split the
copy to fit the system that actually exists; do not preserve unused sections as ceremony.

| Need | Template | Use when |
|---|---|---|
| Execute a known procedure | [Operational runbook](operational-runbook.md) | The trigger and intended outcome are known. |
| Coordinate a live event | [Incident state](incident-state.md) | An incident or controlled exercise begins. |
| Learn from a resolved event | [Postmortem](postmortem.md) | Evidence exists for a real incident or named exercise. |
| State standing authority | [Operational policy](operational-policy.md) | A durable rule needs owners, approvals, and enforcement. |
| Preserve a consequential choice | [Decision record](decision-record.md) | Alternatives, authority, tradeoffs, and a revisit trigger matter. |
| Map a running service | [Service profile](service-profile.md) | Operators and agents need one current service boundary. |
| Move between named versions/states | [Change and upgrade runbook](change-and-upgrade-runbook.md) | A bounded transition needs prechecks, rollback, and final proof. |
| Reconcile source, deployment, runtime, or documentation drift | [Change-drift runbook](change-drift-runbook.md) | A mismatch needs classification, an authoritative reconciliation direction, and independent proof. |

Stack-specific worksheets remain beside them:

- [Profile matrix](profile-matrix.md)
- [Profile SOUL templates](profile-souls.md)
- [Hermes–OMP broker schemas](https://github.com/ghosty-11/hermes-omp-broker/tree/main/schemas)
- [Deployment checklist](deployment-checklist.md)

## Rules

- Placeholders are not claims or defaults. Remove every placeholder instruction from a completed document.
- Omit a field only when it is meaningless; do not manufacture `N/A` rows for appearance.
- A precheck is read-only. The command that made a condition true is a procedure step, not a precheck.
- Verification observes the intended outcome, not merely a zero exit code from a mutation.
- Name the permission boundary that stops execution and what can continue safely while waiting.
- Keep one active writer for shared state. Other agents may research, record, or verify.
- Link current sources and field-tested examples from the completed document, not from the reusable template.
- Keep credentials, private identifiers, production paths, and private topology out of public examples.
