# Changelog

Notable changes to the Hermes Stackbook. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); entries describe documentation
releases, not software versions. Compatibility evidence for upstream components lives in the
[compatibility ledger](docs/compatibility.md), not here.

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
