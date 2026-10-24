# Changelog

> Skip this while evaluating — it is the guide's change history, not setup steps.

Notable changes to the Hermes Stackbook. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); entries describe documentation
releases, not software versions. Compatibility evidence for upstream components lives in the
[compatibility ledger](docs/compatibility.md), not here.

## Unreleased

### Changed

- Gateway topology guidance now reflects the upstream multiplexing default: the gateway settles
  multiplexing at a boot preflight, an explicit `gateway.multiplex_profiles: true` bypasses the
  preflight, `gateway.multiplex_profiles: false` and `gateway.multiplex_profile_allowlist` are
  retired, and a separate per-profile gateway needs the temporary `gateway.standalone: true`
  override. The README, planning, verification, operations, sources, and deployment-checklist pages
  align with the rewritten architecture and profiles pages, and the compatibility ledger pins the
  upstream revision the guidance describes.

## 1.0.0 — 2026-08-23

Initial release.

- Complete private-stack guide: architecture, planning, installation, profiles and models,
  supporting services, security, operations, build sequence, and verification.
- Evaluation and reference material: a disposable-VM trial, core concepts, a glossary,
  compatibility evidence, source records, and knowledge-base guidance.
- Optional extension guidance: skills and plugins, scheduled jobs, a central secret store,
  drift runbooks, and six independently versioned first-party packages.
- Public-safe template library for planning, deployment, operations, recovery, and review.
