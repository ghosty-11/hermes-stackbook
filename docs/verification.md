# Verification

> **Minimum proof for a first trial.** Before the layered material below, four checks tell you
> whether the thing works at all: the built-in diagnostic reports no blocking problem; you ask
> a private question and get a reply; a sender who is not authorised cannot make it act; and
> you restore one file from backup and it matches. Everything after that matters once the stack
> runs unattended or faces anyone but you.

Configuration is an intention. Verification exercises the real profile, surface, dependency, and failure path.

Keep a private verification record with date, installed revisions, commands, exit codes, and evidence locations. Do not copy secrets or private identifiers into this repository.

## Verification layers

| Layer | Proves | Does not prove |
|---|---|---|
| Static config/schema check | Keys parse and required values exist | Capability is reachable or correctly scoped |
| Resolved tool/profile inventory | What the model can call on one surface | Handler works or other surfaces match |
| Unit/fixture check | One deterministic policy can detect a known failure | Production wiring and credentials work |
| Smoke scenario | Real component path works now | Negative boundaries or long-term reliability |
| Negative scenario | Forbidden action is unavailable/rejected | All bypasses are impossible |
| Restore drill | Selected backup content can be recovered | Full-host recovery unless that was tested |
| External monitor | Another process can detect absence/failure | The monitored function's output is correct |

Use all relevant layers. Do not rename a static config check “end to end.”

## Baseline commands

Run current help first:

```sh
hermes --help
hermes doctor
hermes status
hermes config check
hermes gateway list
hermes cron list
hermes skills list
hermes plugins
hermes security audit
hermes prompt-size

# Run these only if OMP is installed:
omp --help
omp --version
omp config list
```

An omitted optional component has no passing check to claim. Record OMP as not enabled rather than treating its skipped commands or bridge scenarios as verified.

When auth broker/gateway is enabled, add their `status` and credential-check commands. The strict OMP auth-gateway check can consume quota; record whether the non-strict or strict path was used.

## Profile matrix

For every profile and each enabled surface—CLI, gateway platform, cron, delegated worker—capture:

- resolved model/provider;
- fallback chain;
- tools/toolsets;
- enabled and eligible skills;
- active plugins/hooks;
- memory provider/store;
- working directory/backend;
- environment/credential owner;
- inbound authorization policy;
- expected positive scenario;
- expected forbidden scenario.

Compare to [`templates/profile-matrix.md`](../templates/profile-matrix.md). Any unexplained extra tool is a failure, not a harmless difference.

## End-to-end scenarios

### Private operator chat

1. Send from the authorized operator.
2. Confirm the intended profile receives it.
3. Perform one harmless real tool action.
4. Observe outbound response and logs.
5. Send from an unauthorized identity; confirm rejection before inference where possible.

### Provider fallback

1. Use a controlled invalid/missing primary credential or a documented test method.
2. Observe failure classification.
3. Confirm a different provider handles the request.
4. Confirm recovery returns future calls to the intended primary.
5. Verify no duplicate charge/retry storm.

### Research quarantine

1. Query a current fact with two sources.
2. Extract one static and one JavaScript-rendered page.
3. Confirm result contains bounded fields and URLs.
4. Return malformed JSON from a fixture; ensure orchestrator receives nothing.
5. Attempt `file:`, loopback, private-address, and metadata-service URLs; ensure rejection.
6. Confirm quarantine cannot call shell/write/private-memory tools.

### Knowledge handoff

1. Submit a sourced internal handoff.
2. Scribe updates the canonical topic and navigation/log as required.
3. Raw content remains in the untrusted/inbox location.
4. Concurrent human edit is preserved.
5. Secret-pattern and link checks pass.
6. Restore the edited note from backup to a temporary path.

### Optional Hermes–OMP broker

If enabled, run the current acceptance suite in
[hermes-omp-broker](https://github.com/ghosty-11/hermes-omp-broker). Independently collect:

- process owner;
- repository/worktree path chosen by broker policy;
- changed paths from Git;
- verification command exit status;
- descendant process cleanup;
- credential-file permissions and failed Hermes read attempt.

### Scheduled jobs

For one no-agent and one model job:

1. trigger manually;
2. observe start/end/status/delivery;
3. prove healthy no-agent output is empty;
4. induce a dependency/config failure; confirm preflight blocks before inference;
5. test stale-job external alert;
6. test shared-resource overlap and lock/serialization behavior;
7. confirm model/provider pin or cron default.

### Optional public bot

If enabled:

1. intended public interaction works;
2. unauthorized privileged commands have no corresponding tool;
3. one user cannot recall another user's memory;
4. rate/spend limit rejects excess;
5. bot volley terminates;
6. prompt injection cannot route to private profiles/bridge;
7. stopping the optional public bot leaves the private gateway path healthy.

### Local inference

If enabled:

1. exact model and context settings observed;
2. short, medium, and max operational prompts return correct fixtures;
3. memory/swap/latency captured;
4. induced cloud outage reaches local;
5. induced local failure stops/falls back without wedging gateway;
6. cloud recovery restores the normal lane.

### Backup and recovery

1. create a fresh encrypted snapshot;
2. list expected state classes;
3. restore representative files/database to temporary staging;
4. compare checksums or structured records;
5. verify permissions needed for recovery;
6. remove staging;
7. confirm external backup-age monitor returns healthy;
8. induce stale/missing snapshot fixture and confirm alert.

## Guard checks

Guards are deterministic policy checks: code or configuration that inspects resolved state and returns the same answer for the same input without asking a model to judge it. Use a guard when the requirement has a right answer—an allowlist matches, a forbidden tool is absent, a backup is recent, or a deployed revision equals a pin. Run guards before risky work, during deployment, and on a schedule where drift matters.

A useful guard:

- reads live or resolved state rather than trusting a declaration;
- checks one named invariant with an unambiguous pass/fail result;
- fails closed when required input cannot be inspected;
- is silent on pass and reports the exact mismatch on failure;
- has a failing fixture proving the check can detect its target defect;
- names an owner and a correction path so alerts remain actionable.

Guard resolved intent such as:

- every expected profile exists and no unexpected online profile appears;
- public/research/auditor forbidden tools are absent;
- gateway topology and allowlist match policy;
- platform admissions are not open accidentally;
- cron model pins/defaults and dangerous-command policy match;
- fallback chains cross providers and end in the expected local lane where configured;
- plugin/source/deployed revisions match pinned manifests;
- custom plugin upstream seam hashes/tests still match;
- knowledge-base writers and paths match policy;
- backup and external-monitor freshness are within thresholds;
- coding broker repository keys/policies and service permissions match.

Do not use a guard to score whether prose is helpful, research is insightful, or a model made a reasonable tradeoff. Those are behavioral questions for an eval. Do not weaken a guard until broken state passes; fix the state or change the policy explicitly. Every assertion needs a failing fixture. A guard that cannot be shown red is not trusted.

## Evals

Evals measure model behavior on representative tasks. They answer questions with judgment in them: whether a model routed work appropriately, preserved provenance, found the important defect, cited a claim, admitted uncertainty, or produced useful code. Unlike guards, evals may have variable outputs and often require a rubric, reference facts, deterministic checks on the resulting artifact, or human review.

Build evals from real use cases and recorded failures rather than invented trivia. Each eval should define:

- the profile, model/provider, tool surface, and starting state;
- a representative prompt or task with private details sanitized;
- observable success, failure, and partial-credit criteria;
- forbidden behavior and side effects;
- evidence to retain, such as sources, changed paths, test exits, latency, and cost;
- the number of runs needed before comparing variable model behavior;
- the decision the result informs: model routing, prompt change, tool change, or release readiness.

Useful examples include:

- orchestrator routes instead of doing specialist work;
- scribe preserves provenance and rejects raw promotion;
- auditor reports defects and does not apply changes;
- research returns bounded cited findings and admits uncertainty;
- optional public bot, if enabled, stays within interaction policy;
- coding work changes only allowed files, passes the relevant check, and reports observed evidence and residual risk;
- a cheaper model handles routine classification or summarization acceptably while escalation reaches a stronger model for difficult cases.

Do not tune an eval until one favored model passes, use a single lucky run as proof, or mix provider outages with response-quality scoring. Keep prompts and rubrics versioned, preserve representative failures, and rerun the same corpus when models, tools, skills, or instructions change.

Keep eval and guard outcomes separate. A good model response does not prove the tool boundary; a correct tool boundary does not prove useful behavior. Example: a guard can prove that a research profile has no shell tool, while an eval tests whether that profile returns a useful, cited answer.

Guards and evals together are the verification loop described in [Architecture](architecture.md). Two failure modes are worth naming because both read as success. A check that cannot be shown failing is not yet a check, so keep a failing fixture for every guard. And a reviewer that runs inside the context that produced the work approves that work: give the check a starting state the generator never touched, whether that means a separate profile, a fresh session, or a deterministic script.

## Operator-gated improvement loop

This is the improvement loop from [Architecture](architecture.md), and it is the one most deployments never build. A stack can evaluate and improve its own configuration without gaining the authority to rewrite itself, provided evaluation, proposal, approval, application, and verification stay separate states:

1. Deterministic guards, behavioral evals, audits, and compatibility checks collect current evidence.
2. A read-only reviewer converts material drift, repeated failures, or a useful upstream capability into a bounded proposal.
3. The proposal goes to one explicit operator destination, such as a private inbox or standup channel, and includes observed evidence, expected value, affected boundary, risk, rollback, and the verification that would prove the change.
4. The operator approves, rejects, or holds the proposal. Silence grants no authority.
5. A separately authorized change applies the exact approved scope and reruns the same guard/eval plus the affected end-to-end scenario.

This is an operator-gated self-improvement loop, not autonomous self-modification. The evaluator must not deploy, restart, publish, spend, widen credentials, or mark its own proposal approved.

Acceptance scenarios:

- a planted regression produces one proposal at the configured destination;
- healthy state is silent;
- repeated runs deduplicate an unchanged finding;
- rejection or no response changes nothing;
- an approved change records the proposal, authorization, diff, rollback target, and fresh verification;
- the proposing profile lacks the tools required to apply the recommendation.

## Completion record

For every phase, report:

```text
Goal:
Changed:
Failed:
Left undone:
Verdict: MET | PARTIALLY MET | NOT MET
Verification commands and observed results:
Next operator action:
```

A partial result is acceptable. An unstated gap is not.
