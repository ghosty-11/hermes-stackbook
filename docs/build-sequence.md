# Build sequence

Implement in phases. Each phase has a useful result, explicit exit criteria, and a rollback point. Do not add the next trust boundary to make the current one pass.

## Phase 0 — decisions and recovery

Build:

- complete the private decision worksheet in [Planning](planning.md);
- choose OS identities, private network, provider accounts, backup destination, and expected budget;
- decide separate gateways versus hybrid/multiplexed topology;
- create a private deployment log outside this public-safe repository.

Exit:

- secrets have named owners and storage locations;
- off-host encrypted backup destination is reachable;
- operator has an out-of-band host access path;
- no service is public.

Rollback: none; no runtime changed.

## Phase 1 — one private Hermes profile

Build:

- install Hermes;
- configure one private model and a provider-diverse fallback;
- configure one authorized private CLI/chat surface;
- install the supported gateway service.

Exit:

- doctor/config checks pass;
- real primary and fallback calls observed;
- authorized message succeeds;
- unauthorized identity is rejected;
- service restart returns the chat path;
- baseline backup created.

Rollback: restore baseline config or uninstall the gateway service using the official CLI.

## Phase 2 — optional OMP independent baseline

Skip this phase when Hermes' own coding surface is sufficient. Complete it before any Hermes–OMP integration when dedicated software engineering is a major workload.

Build:

- install OMP under the operator/coding identity;
- configure coding-provider credentials;
- run an interactive disposable-repository task;
- exercise one-shot and RPC modes.

Exit:

- behavioral change verified in disposable repository;
- session resume works;
- one-shot returns and exits;
- RPC prompt/response/abort frames work;
- no Hermes integration and no credential sharing.

Rollback: remove OMP through its package manager; Hermes is unaffected.

## Phase 3 — optional private search quarantine

Build:

- deploy SearXNG on loopback;
- deploy chosen extractor on loopback;
- create research profile with only search/extract tools;
- create a bounded internal research call returning structured output.

Exit:

- fixed current query returns cited sources;
- static and JavaScript page extraction tested;
- malformed/oversized output is rejected;
- private/link-local/file URLs are blocked;
- research profile has no shell/write/private-memory tools;
- orchestrator receives no data on parse failure.

Rollback: disable the delegate tool/profile, then stop services. Private chat remains available.

## Phase 4 — optional knowledge base and scribe

Build:

- create a Git-backed Markdown knowledge base using the [proposed wiki structure](knowledge-base-structure.md) or an equally explicit local layout, with navigation, source/date convention, inbox, and untrusted-raw boundary;
- add adapted copies of the selected runbooks and templates, preserving the Stackbook source revision;
- link each installed copy from the knowledge-base navigation instead of relying on the external guide;
- create scribe profile;
- make scribe the sole routine canonical writer;
- disable conflicting wiki skills.

Exit:

- a sourced handoff becomes one canonical note and log entry;
- normal knowledge-base search finds the selected runbook or template, and its copy names live owners, paths, gates, and verification;
- raw web text remains outside trusted notes;
- concurrent human edit is preserved/reconciled;
- no secrets in the repository;
- restore one note from backup.

Rollback: pause scribe writes; repository remains human-editable.

## Phase 5 — optional Hermes-to-OMP coding broker

Build:

- install [hermes-omp-broker](https://github.com/ghosty-11/hermes-omp-broker);
- deploy OMP auth broker/gateway if remote/shared credential resolution is needed;
- register its narrow Hermes delegate tool;
- bind requests to task IDs and server-owned repository policy.

Exit:

- the package's current acceptance suite passes;
- Hermes identity cannot read OMP refresh tokens;
- unknown repository/path is rejected before launch;
- broker-observed Git/test evidence is returned;
- cancellation and timeout kill descendants;
- dirty failure evidence is preserved.

Rollback: disable the Hermes plugin/tool and stop broker; OMP remains interactive.

## Phase 6 — optional scheduled work and auditor

Build:

- convert deterministic routines to no-agent scripts;
- add only model jobs that require judgment;
- create auditor profile or scheduled OMP review lane;
- add external staleness/dead-man checks.

Exit:

- healthy deterministic jobs emit nothing;
- failures deliver to explicit destinations;
- model jobs are pinned or use deliberate cron defaults;
- dangerous cron commands fail closed;
- auditor cannot write/apply/deploy;
- orchestrator cannot silently self-approve an audit finding;
- overlapping shared-store job test respects a lock/serialization policy.

Rollback: pause jobs individually; do not delete execution history during diagnosis.

## Phase 7 — optional local inference

Build:

- deploy Ollama or selected local runtime on loopback;
- choose one model and measured context;
- add as final fallback only;
- implement fallback-specific context policy if required.

Exit:

- short, medium, and maximum operational canaries return correct answers;
- memory/swap/latency stay within limits;
- induced cloud failure reaches local degraded lane;
- cloud recovery returns to primary;
- local hang/failure does not wedge the gateway.

Rollback: remove local endpoint from fallback before stopping the service.

## Phase 8 — optional public bot

Build:

- separate profile and preferably separate process/OS identity;
- separate bot/provider credentials and budget;
- minimal public toolset;
- rate limit, identity scoping, bot-loop breaker, retention policy;
- optional ambient adapter—such as [ghosty-11/hermes-discord-ambient](https://github.com/ghosty-11/hermes-discord-ambient)—only after normal mention/direct-reply behavior is stable.

Exit:

- public user can use intended features;
- attempts to access wiki, shell, files, cron, board, coding bridge, or private agents are structurally impossible;
- cross-user memory test passes;
- bot-to-bot volley stops;
- spend/rate cap fires;
- disabling the public service does not affect private profiles.

Rollback: stop/revoke the optional public-bot token; private stack remains online.

## Phase 9 — observability and hardening

Build:

- resolved tool/profile assertions;
- plugin seam checks;
- external monitors;
- optional trace export;
- restore drills and incident playbooks;
- first eval corpus from real use cases.
- optional operator-gated improvement proposal lane fed by guard, eval, audit, and compatibility evidence.

Exit:

- every check has a demonstrated failing fixture;
- profile matrix and end-to-end scenarios pass;
- restore drill succeeds;
- alert path is actionable and quiet when healthy;
- custom plugin update compatibility is reproducible;
- public-release scan can run against full history.
- a planted regression produces one evidence-backed proposal at the configured operator destination, clean state stays silent, and no proposal can apply itself.

Rollback: observability should fail open for user work but fail loud to the operator; remove noisy checks rather than weakening assertions until they become meaningless.

## Definition of ready

The stack is ready for normal use when:

- phases for the selected and enabled modules meet their exit criteria;
- every enabled profile passes positive and negative capability tests;
- each enabled private chat, research, knowledge, coding, cron, mailbox, and backup path was exercised end to end;
- no required check relies only on config inspection;
- recovery commands and credential owners are documented privately;
- known untested behavior is explicitly listed rather than implied complete.
