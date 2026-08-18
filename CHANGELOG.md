# Changelog

> Skip this while evaluating — it is the guide's change history, not setup steps.

Notable changes to the Hermes Stackbook. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); entries describe documentation
releases, not software versions. Compatibility evidence for upstream components lives in the
[compatibility ledger](docs/compatibility.md), not here.

## 1.7.0 — 2026-08-18

Adds the loop view of the stack. The guide already described the planes — what exists — and
every mechanism needed to run them, but never said what repeats, so the improvement loop read
as a governance procedure rather than as the outermost loop of the system.

- New **Loops in the system** section in [Architecture](docs/architecture.md): four loops that
  wrap each other, a table mapping each to the chapter that covers it, and the two properties
  that matter more than the ordering — the check is the load-bearing part of verification, and
  the improvement loop reaches inside the others, which is why it stays operator-gated.
- [Verification](docs/verification.md) now names where guards and evals sit in that view, and
  adds two failure modes that both read as success: a check nobody has seen fail, and a
  reviewer running inside the context that produced the work.
- The harness-engineering entry in the [suggested skills roadmap](docs/skills-and-plugins.md)
  gains layer-first diagnosis and a release gate requiring a proposed change to name its loop.
- Guidance only: no upstream behavior claim changed, so the
  [compatibility ledger](docs/compatibility.md) is untouched.

## 1.6.1 — 2026-08-16

Ledger-only release: the field deployment advanced, so its evidence row advanced with it rather
than the older row being rewritten.

- New compatibility row for a 204-commit framework advance and OMP `17.3.5`, recording what was
  actually exercised after the restart: per-profile plugin inventory unchanged, cron scheduling
  across every multiplexed profile, both chat identities reconnected, and a profile-scoped
  platform adapter observed doing something only it does.
- The suite evidence is a slice-and-compare, not a single run: 34k collected tests do not fit
  this host in one process, so slices ran one at a time and every failing area was re-run
  against the exact merged upstream commit in a control worktree. 31,875 passed, 279 failed,
  and the failure sets match the control area for area — which is the claim that matters, since
  a raw failure count says nothing about who caused it.
- The row still records what was **not** measured: no full delegation ran through the rebuilt
  broker client, and one `tests/tools` chunk hangs when its files share a process — on the
  control as well — leaving ~1,500 tests unrun. An evidence row that hides its gaps is worth
  less than one that names them.

## 1.6.0 — 2026-08-16

Corrects the secret-store design on a point that field use found the hard way: separate encrypted
files are necessary but not sufficient. Splitting the files controls who can *read*; it does
nothing about who can *write*.

- **Encryption controls reading; ownership controls writing.** A store configuration lists the
  **public** recipient of every file, because that is how encryption is targeted. So a principal
  that can write another principal's file can encrypt values of its own choosing to that file's
  legitimate recipient, and the victim decrypts them cleanly — credential substitution needing no
  private key at all. A shared group-writable store directory leaves one principal able to feed
  another an API key pointing wherever it likes.
- The design now gives each identity a directory only that identity can write, with a parent that
  is not group-writable. Reading another's ciphertext stays harmless and may remain permitted
  where something legitimately needs it, such as committing the repository; writing is the
  privilege to withhold.
- Requirements and the verification checklist now cover write refusals as well as read refusals,
  and warn against trusting a check that passes for a reason you have not confirmed — a command
  failing for the wrong reason reads exactly like a boundary that holds.
- **New migration step:** know which seams are additive and which replace. A source that merges
  without overriding leaves the old path authoritative, so a store outage is harmless and rollback
  is disabling the source. A configuration field rewritten to call the store is a hard cutover:
  the old path no longer runs, an unreachable store breaks that consumer, and rollback means
  editing configuration. Record which is which before relying on "we can always roll back", and
  note that a consumer failing closed is correct behaviour rather than evidence the store is fine.

## 1.5.0 — 2026-08-16

Adds the credential-storage guidance the guide never had, and removes two ecosystem entries
that a source review found do not do what their one-line descriptions implied. Both changes
come from evaluating a central credential store for the reference deployment and rejecting
every off-the-shelf candidate.

- **New:** [Central secret store](docs/secret-store.md) — when to consolidate credentials, and
  what a store is actually worth. It buys one rotation point, one revocation point, no plaintext
  at rest and one thing to back up. It is **not** a boundary: whatever unlocks the store is
  readable by the identity the harness runs as, so an agent running as that identity can read it
  too. The page says so plainly, because claiming otherwise is the common failure.
- The design requirement that is easy to get backwards: **one encrypted file per consuming
  identity, not one shared ciphertext**. Where two harnesses run as OS users that cannot read
  each other's credentials today, a single blob readable by both is a regression in blast radius
  disguised as consolidation. Verify the isolation rather than assume it.
- Requirements are derived from the delivery contracts a harness already imposes — a complete
  `KEY=VALUE` map from one invocation for a bulk seam, one value per field for a per-field seam,
  both under fixed timeouts, non-interactive after reboot — rather than from any product's
  feature list.
- Includes a worked example, migration order, rotation, and a verification checklist. Migration
  leads with inventorying **every** reader, because service units with an environment-file
  directive, helper scripts parsing credential files directly, and inline passwords in container
  definitions all keep live copies that make "rotate once" false.
- Security: the Secrets section now recommends a store first, and notes that a hand-made
  `.env.bak` inherits the umask rather than the original's mode.
- Operations: the credential-exposure playbook now treats a value that reached an agent context,
  a model provider or a transcript as exposed **off-host**, and states that rotating a store key
  is not a substitute for rotating the credential — removing a recipient reaches neither history,
  backups, nor a value already read.
- Planning, build sequence and backups gain the matching decision points; backups call out that
  the store's key material must be kept separately from the store's ciphertext.
- **Removed:** two entries from the ecosystem candidate list. One was described as a local
  credential broker, but its raw credential-returning routes are registered unconditionally with
  no flag to disable them and its own ADR defers per-agent filtering to a policy layer that does
  not exist. The other is a configuration UI for an agent framework's own container terminal
  backend rather than an access-control system. Listing either invited readers to install
  software this project evaluated and rejected.

## 1.4.0 — 2026-08-16

Releases the last unfilled item on the architecture document's own custom-work list, so it is
no longer planned work.

- **New package:** [hermes-web-research](https://github.com/ghosty-11/hermes-web-research) —
  web access for a privileged profile that holds no web tools. One tool delegates to a
  quarantined profile in a separate OS process, asks for a single JSON object, and forwards
  only known fields, each bounded and neutralised. Output that does not parse forwards
  nothing, and forwarded values cannot impersonate the label that marks them untrusted. It
  ships a threat model, because a boundary published without one is a claim rather than a
  control.
- Architecture: the fail-closed web-research hop moves from "remaining custom work" to a
  released package. Five items remain on that list.
- Skills and plugins: the new package's review note names the thing that actually decides its
  safety — the quarantine seat's own resolved tool surface is the blast radius, and config
  membership is not resolved capability.
- Tests: the released-package coverage assertion now covers six packages.

## 1.3.0 — 2026-08-16

New released package, plus a package-coverage correction. An audit of the reference deployment
against this guide found two already-released packages the guide either never named or framed as
somebody else's work, so a reader could not tell what this project actually ships. No security
posture changed; the gap was provenance and index coverage.

- **New package:** [hermes-trace](https://github.com/ghosty-11/hermes-trace) — per-session
  evidence of what an agent did: which skills were exposed and never activated, tool calls, API
  cost and duration, as bounded append-only events plus a compact card per session. It observes
  only: every handler returns nothing, so it cannot gate a turn. Documented under the same
  review procedure as any third-party plugin, because its output is as sensitive as the
  conversations it records.
- **New:** README [Released packages](README.md#released-packages) — a single index of the five
  first-party packages with what each adds and the boundary that makes it safe to have. It
  replaces the two-package sentence that had to be edited by hand for every release and was not.
- Skills and plugins: a first-party packages section placing all five inside the same plugin
  review procedure as any third-party extension, stating outright that being first-party is
  provenance and not an exemption. `hermes-optmem-tools` is documented for the first time; only
  the upstream memory store it wraps had been listed.
- Security and Sources: the ambient public-chat adapter is now identified as this project's own
  implementation running on the reference deployment's public profile, rather than "one public
  implementation to review". Sources gained an explicit first-party provenance paragraph.
- Extension and file drift: a worked example for the layer readers skip — loader policy against
  loaded runtime. Three profiles listed an extension that resolved to nothing on the host and
  the gateway ignored the unknown name in silence, so the configuration asserted a capability
  for weeks. The invariant is that every name in an enablement list resolves to a discoverable
  extension on the profile that lists it, checked in both directions.
- Tests: a released-package coverage assertion, so a package published without documentation
  fails CI instead of going unmentioned. Watched failing before it was made to pass.

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
