# Changelog

> Skip this while evaluating — it is the guide's change history, not setup steps.

Notable changes to the Hermes Stackbook. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); entries describe documentation
releases, not software versions. Compatibility evidence for upstream components lives in the
[compatibility ledger](docs/compatibility.md), not here.

## 1.2.0 — 2026-08-15

Newcomer on-ramp, prompted by first-impression feedback from a technical reader who found the
guide hard to follow and wanted a throwaway machine to experiment on. No security content was
relaxed; the rigorous material gained scope labels so it stops reading as a prerequisite.

- **New:** [Try it safely](docs/safe-sandbox.md) — a disposable-VM evaluation path with one
  recommended default, alternatives and their tradeoffs, five preconditions that must hold
  before installing anything, a bounded 30-minute trial with an explicit stop point,
  destruction steps, and a plain statement of residual risk.
- **New:** [Glossary](docs/glossary.md) — only the terms this guide uses in a specific way,
  grouped by purpose, including an "easy to confuse" section (profile vs OS user vs VM, skill
  vs plugin, model vs provider, backup vs sync, guard vs eval).
- **New:** [Core concepts](docs/core-concepts.md) — what each piece is in day-to-day terms,
  which one a given job needs, and one request followed end to end through the minimum path.
- README: a three-way entry table, an "In one minute" plain-language summary, a minimum-path
  diagram beside the full reference architecture, a Step 0 pointing at the sandbox, and a
  pointer to the sandbox directly beneath the personal-machine warning. The assisted-setup
  section is now explicitly labelled the real-deployment path.
- Scope labels added to Operations, Verification, Skills and plugins, Scheduled jobs,
  Supporting services, Compatibility, both drift runbooks, the template library, and this
  changelog. Verification also gained a four-check "minimum proof for a first trial" panel.

## 1.1.1 — 2026-08-15

- Profiles: warn that omitting `gateway.multiplex_profile_allowlist` is fail-open — the
  default serves every installed named profile, so an experimental profile directory
  becomes a served execution scope; an empty list serves only the default.
- Profiles: document `--no-skills` for deliberately minimal seats.
- Operations: record the delegation lane's own provider/model separately from the parent's,
  and pin delegation concurrency/iteration ceilings — both are version-dependent defaults a
  framework update can raise underneath you, and a shared per-key provider rate limit is
  usually the binding constraint rather than price.

## 1.1.0 — 2026-08-15

Field-evidence corrections and additions from operating the reference deployment:

- Compatibility ledger: recorded the author's live field deployment (Hermes `27fddcbe5`,
  OMP 17.3.4) as a runtime-smoke row ahead of the pinned review anchor, including the
  655-commit framework advance and how it was gated.
- Architecture + profiles: documented that a multiplexed gateway persists every served
  secondary profile's live sessions in the serving profile's state database (the serving
  profile's own rows may be untagged), and that the secondary profile's own state file
  answers with *different* sessions from standalone CLI runs rather than none — a wrong
  answer that reads like a complete one.
- Supporting services: clarified the local-inference rule (single *loaded* model versus a
  small deliberate on-disk inventory) and added three field-tested backup principles
  (backup plane survives the agent plane; stage live databases consistently; expose a
  narrow non-secret status projection).
- Scheduled jobs: named the two deliberate exceptions to silent-when-healthy
  (consumer-facing heartbeat jobs; bounded collector-to-reviewer handoffs).
- Operations: added the optional independent operator control-plane pattern.

## 1.0.0 — 2026-08-14

Initial release.

- Core private-stack guide: architecture, planning, installation, profiles and models,
  supporting services, security, operations, build sequence, and verification.
- Extension references: skills and plugins, suggested scheduled jobs, skill drift and
  extension/file drift runbooks, and the separate
  [hermes-omp-broker](https://github.com/ghosty-11/hermes-omp-broker) and
  [hermes-mailbox](https://github.com/ghosty-11/hermes-mailbox) packages.
- Template library: eleven public-safe templates and worksheets plus the proposed
  knowledge-base structure.
- Compatibility ledger and sources reviewed 2026-08-14.
