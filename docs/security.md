# Security

The threat is not only a malicious model. It includes an authorized model making a wrong decision, untrusted content steering a privileged turn, a community extension executing unexpected code, credential leakage, an unattended job spending or changing state, and an operator unable to recover the host.

Use the official [Hermes security guide](https://hermes-agent.nousresearch.com/docs/user-guide/security/) as the product reference. This document applies it to the two-harness architecture.

## Security invariants

1. Public input and raw web content never enter a context that can administer the host, read private credentials, or write production code.
2. Hermes cannot read OMP coding-provider refresh tokens when the bridge is enabled.
3. A profile's actual tool schema matches its documented capability matrix on every enabled surface.
4. Destructive or irreversible actions require authenticated human approval.
5. Unattended jobs have fixed models/providers or explicit spending policy, bounded runtime, named delivery, and no recursive scheduling.
6. Shared state has one routine writer or a real concurrency protocol.
7. All admin and local service endpoints are loopback/private-network only and independently authenticated.
8. Backups are encrypted, off-host, and restore-tested.
9. Community code is reviewed and pinned before enablement.
10. Publication review covers content, full Git history, commit messages, and author metadata.

## Threat boundaries

### Profiles are not sandboxes

A profile separates Hermes state. On a local terminal backend it still inherits the OS user's filesystem authority. Use:

- absent tools for capability minimization;
- write sandbox and deny rules for honest-but-wrong operations;
- Docker/other isolated terminal backend for execution isolation;
- separate OS identities and file permissions for credential/repository isolation;
- service brokers for the narrowest cross-identity operation.

### Prompts are not controls

`SOUL.md` and skills can improve decisions. They cannot prevent a tool call the model can make. Enforce non-negotiable policy through tool absence, authenticated admission, server-owned allowlists, filesystem permissions, containers, approval gates, and deterministic checks.

### Detection is defense in depth

Prompt-injection classifiers and content scanning can reduce accidental propagation. They cannot make arbitrary page text safe enough to share a context with a shell. The research profile's absent privileges are the control.

## Input classes

| Input | Trust | Allowed destination |
|---|---|---|
| Operator private message | Authenticated, not automatically correct | Orchestrator; privileged actions still need policy/approval |
| Public chat | Untrusted | Optional public profile only, if enabled |
| Search result/page extraction | Untrusted | Research quarantine only; bounded result crosses boundary |
| Community skill text | Untrusted executable instructions | Offline review before installation |
| Community plugin | Untrusted code | Offline code/dependency review; pin and sandbox |
| Project repository instructions | Trusted only to the repository's authority | OMP working on that repository; not host-global policy |
| Shared knowledge base | Internally curated, potentially stale | Relevant profiles via explicit read/search |
| Coding job body | Authenticated request but model-generated | Broker validation; OMP with repository policy |

## Hermes controls

Keep the current product defaults unless your threat model justifies a change:

- authorized-user allowlists or DM pairing;
- dangerous-command approvals;
- `approvals.cron_mode: deny` for unattended jobs;
- destructive slash-command confirmation;
- hardline blocklist and local deny rules;
- context-file scanning;
- file-write safety/sandboxing;
- isolated terminal backend for untrusted execution;
- MCP credential filtering;
- plugin opt-in and immutable pins;
- `hermes security audit` after dependency/plugin changes;
- `hermes --safe-mode` for customization-free diagnosis.

Do not use `--yolo` or approvals-off on a host-reaching backend. A container boundary can justify different approval behavior inside the disposable environment, but mounted host paths remain host-reaching.

## Secrets

- Put Hermes secrets in its supported secret store or profile `.env`, mode-restricted.
- Keep bot tokens per profile and reject duplicate tokens where the gateway enforces it.
- Keep OMP auth broker/gateway bearer files private and rotate them after suspected exposure.
- Prefer an external secret backend when operationally justified; do not place secrets in config examples, Git, wiki, task bodies, or logs.
- Pass only named environment variables to sandboxes and MCP servers.
- Do not let an agent print environment listings as diagnostics.
- Redact secret values before storing execution evidence.
- Treat OAuth refresh tokens, session cookies, SSH keys, Tailscale state, backup keys, and bot tokens as recovery-critical secrets.

A secret scanner is necessary but insufficient. Personal identifiers, hostnames, private topology, Discord IDs, and third-party personal data can leak without matching a credential pattern.

## Egress

Hermes includes an optional egress proxy for credential injection into remote terminal sandboxes. Evaluate it before writing a custom outbound-secret proxy.

For every profile, maintain an outbound allowlist by purpose:

- model provider endpoints;
- search/extract loopback endpoints;
- messaging platform APIs;
- reviewed MCP/plugin destinations;
- source-control hosts for profiles explicitly authorized to use them.

A public or quarantine profile should not reach private RFC1918/tailnet services except the exact loopback/private service it needs.

## Coding bridge security

The bridge must enforce server-owned values for:

- repository path;
- executable and arguments;
- OMP config overlays;
- model roles;
- allowed write/commit behavior;
- timeout and concurrency;
- environment;
- result size;
- cleanup policy.

Authenticate the Hermes caller. A local socket permission is useful but not sufficient if multiple profiles share the same Hermes OS identity; include profile/caller authorization at the protocol layer.

Collect Git and verification evidence outside the model response. Never grant push, merge, release, deployment, or service-restart authority just because a task requests it.

## Optional public bot rules

An optional public bot receives:

- no terminal, file, browser, cron-management, task-board, private-wiki, coding-delegate, or host-admin tool;
- its own provider key and spending limit;
- its own memory store, scoped by stable user ID;
- rate limits and a bot-to-bot volley breaker;
- authenticated platform identity in the prompt/tool context;
- no route to private profiles based solely on message text.

If adding ambient “sometimes respond” behavior to the optional public bot, admission is an adapter decision. A model prompt cannot reliably control whether a gateway creates an inference turn. [ghosty-11/hermes-discord-ambient](https://github.com/ghosty-11/hermes-discord-ambient) is one public implementation to review.

## Scheduled work

Prefer no-agent scripts for deterministic checks. For model jobs:

- pin model/provider or a deliberate cron default;
- keep preflight and model-drift guard enabled;
- deny dangerous commands headlessly;
- use fixed work directories and repository policies;
- cap runtime, retries, and concurrency;
- deliver to an explicit destination;
- stay silent on healthy checks;
- keep alarm channels for actionable host failures;
- monitor schedule staleness outside the job being monitored.

## Update policy

Before an update:

1. read release notes and current `--help`;
2. take a state backup;
3. inventory modified bundled skills/plugins;
4. identify custom plugins that wrap upstream methods;
5. run baseline/profile acceptance checks;
6. update one layer at a time;
7. re-run integration, negative-boundary, and restore checks;
8. keep the previous package/commit and config for rollback.

Do not patch upstream source in place. A locally modified bundled artifact may keep working while silently missing upstream changes.

## Optional public-release checklist

This checklist is not a deployment requirement. It is an optional security policy for whenever you choose to release any of your work publicly, including publishing a repository, changing repository visibility, or sharing code, documentation, configuration, images, or archives.

Before publishing the work:

1. Choose a license for the repository you are preparing to publish.
2. Scan the working tree for credentials, private paths, hostnames, internal role names, account IDs, bot IDs, emails, and third-party personal data.
3. Scan **all Git history**, not only `HEAD`.
4. Review every commit message.
5. Review author name and email on every commit; use a deliberate public identity/noreply address if desired.
6. Review issue templates, images, metadata, hidden files, archives, and generated outputs.
7. Confirm examples use fictional domains, IDs, and paths.
8. Verify every external link and every license/attribution obligation.
9. Clone the repository into a clean directory and run the documentation checks there.
10. Only then publish it or change repository visibility.

If sensitive identity data ever entered a private repository's history, rewriting and force-pushing may not make it irretrievable from the hosting provider. Before public release, the cleanest option can be creating a new repository from a reviewed snapshot with fresh history.

## Incident priorities

1. Contain: revoke ingress, stop the affected profile/plugin/job, rotate exposed credentials.
2. Preserve evidence: logs, job ID, session ID, plugin revision, config snapshot, changed paths.
3. Recover the narrowest component; avoid broad resets or deleting history.
4. Verify real behavior end to end.
5. Record root cause and the control that prevents recurrence.
6. Re-enable one boundary at a time.

Do not let the agent implicated in the incident be the sole investigator or recovery authority.
