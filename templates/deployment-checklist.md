# Deployment checklist

Copy this checklist into the private deployment repository. Attach commands and observed results to every checked item.

## Baseline

- [ ] Host, OS identities, private network, and supervisor selected.
- [ ] Model/provider privacy and spending policy recorded.
- [ ] Encrypted off-host backup destination configured.
- [ ] Out-of-band host access tested.
- [ ] Hermes installed through one owned update path.
- [ ] OMP installed through one owned update path if selected.
- [ ] Exact installed versions/revisions recorded privately.

## Hermes

- [ ] `hermes doctor` has no blocking result.
- [ ] Config check/migration state is clean.
- [ ] Primary provider succeeds.
- [ ] Provider-diverse fallback succeeds under controlled primary failure.
- [ ] Private authorized message completes end to end.
- [ ] Unauthorized sender is rejected.
- [ ] Gateway supervisor restart returns the real chat path.
- [ ] Baseline backup exists and representative restore succeeds.

## Optional: OMP

- [ ] Interactive disposable-repository task changes the requested behavior only.
- [ ] Targeted verification exits successfully.
- [ ] Session resume works.
- [ ] One-shot mode returns and exits.
- [ ] RPC prompt/response/abort works.
- [ ] Config/credential output is secret-safe.
- [ ] Auth broker/gateway health and authorization tested if enabled.

## Profiles

- [ ] Every online profile has a documented job and consumer.
- [ ] Profile matrix captured from resolved state on every surface.
- [ ] Positive scenario passes per profile.
- [ ] Forbidden scenario is structurally unavailable per profile.
- [ ] Models, fallbacks, memory, skills, and plugins resolve as intended.
- [ ] Gateway process or multiplex allowlist is explicit.
- [ ] Optional public profile, if present, has a separate failure/security boundary.

## Optional: research

- [ ] Search and extraction bind to loopback/private network only.
- [ ] Static and JavaScript pages tested.
- [ ] Private/link-local/file/metadata URLs rejected.
- [ ] Research profile has no privileged tools.
- [ ] Structured output fails closed on malformed/oversized data.

## Optional: knowledge base

- [ ] Knowledge base has one routine writer and an untrusted inbox boundary.
- [ ] Raw web text is not promoted automatically.
- [ ] Links/source dates and backup restore tested.

## Optional: coding broker

- [ ] Caller authentication and profile authorization tested.
- [ ] Repository keys map to server-owned paths/policy.
- [ ] Arbitrary path/env/executable fields cannot be supplied.
- [ ] Hermes cannot read OMP refresh tokens.
- [ ] Shared checkout writes serialize or use isolated worktrees.
- [ ] Read-only, write, reject, cancel, timeout, and dirty-failure scenarios pass.
- [ ] Broker—not model prose—collects Git and verification evidence.
- [ ] Descendant process cleanup observed.

## Optional: mailbox

- [ ] Direct mail is visible only to its intended recipient.
- [ ] Shared mail has one atomic claimant and explicit release.
- [ ] Session-start output contains metadata only.
- [ ] Body reads are explicit, bounded, and wrapped as untrusted content.
- [ ] Read, acknowledgement, and release are separate operations.
- [ ] Restart and restore preserve replay state.

## Cron and operations

- [ ] Deterministic jobs use no-agent mode/scripts.
- [ ] Model jobs are pinned or use a deliberate cron default.
- [ ] Preflight and model-drift guard policy verified.
- [ ] Dangerous commands fail closed headlessly.
- [ ] Deliveries use explicit destinations.
- [ ] Healthy checks are silent.
- [ ] Shared state uses locks/serialization.
- [ ] External dead-man and backup-age checks can fail.
- [ ] Restore drill and incident playbooks exercised.

## Extensions

- [ ] Every skill/plugin has a named need and consumer.
- [ ] Official inventory checked before adding community code.
- [ ] Source, dependencies, install path, network, secrets, and license reviewed.
- [ ] Immutable revision pinned where supported.
- [ ] Positive, negative, failure, restart, and upstream-seam checks pass.
- [ ] Rollback revision/config recorded.
- [ ] Security audit and prompt-size impact reviewed.

## Optional public release

Use this section only when you choose to release any work publicly. It is an optional security policy, not a private deployment requirement.

- [ ] License chosen deliberately.
- [ ] Working tree scanned for secrets and identifying/private data.
- [ ] Full Git history scanned independently.
- [ ] Commit messages reviewed.
- [ ] Author names/emails reviewed.
- [ ] Hidden/generated/archive/image content reviewed.
- [ ] External links and attribution/license obligations checked.
- [ ] Fresh clone passes documentation and schema checks.
- [ ] If history ever contained sensitive data, a new clean-history repository was considered.

## Verdict

```text
Goal:
Changed:
Failed:
Left undone:
Verdict: MET | PARTIALLY MET | NOT MET
Fresh verification evidence:
Next operator action:
```
