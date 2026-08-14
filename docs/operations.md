# Operations

A working chat reply is not an operated service. The stack is ready for unattended use only when its health, spend, backups, updates, and failure recovery are observable.

## Daily operating view

Check only signals that lead to action:

- gateway process/service state and restart count;
- profile/platform connection state;
- cron blocked/failed/stale jobs;
- provider failures, fallbacks, and unexpected spend;
- search/extract/local-model dependency health;
- disk, memory, swap, and backup age;
- unresolved coding jobs and dirty worktrees;
- external dead-man status.

Hermes provides useful built-ins:

```sh
hermes status
hermes gateway list
hermes logs
hermes cron list
hermes insights
hermes doctor
hermes security audit
hermes prompt-size
```

Run each command's `--help`; output and subcommands evolve.

## Service supervision

Use Hermes' supported gateway installer for normal systemd/launchd deployments. Use one profile service per process unless multiplexing was selected deliberately.

Requirements:

- restart on unexpected failure, not an unbounded tight loop;
- distinguish requested restart from crash where the platform supports it;
- preserve logs across restart;
- do not start a second unsupervised gateway with `nohup`/`&`;
- keep an external check that can report when Hermes itself is down;
- verify platform reconnection and a real message after a service/config change.

Process alive is not gateway healthy. The acceptance path is authorized inbound message → correct profile → model/tool action → outbound delivery.

## Cron design

Choose the narrowest execution mode:

1. **No-agent script:** deterministic status, cleanup, sync, backup, counts, checksums.
2. **Script then model:** script gathers bounded evidence; model interprets it.
3. **Full model job:** only where the job genuinely needs search, ambiguity, synthesis, or language generation.

Hermes supports no-agent cron jobs whose stdout is delivered without inference. Make healthy output empty. Send failures to an explicit platform/channel, never an ambiguous bare platform and never a general conversation channel.

For model jobs:

- pin per-job model/provider or set a deliberate `cron.model`/provider fleet default;
- keep preflight enabled;
- keep model drift guard enabled unless tracking global changes is intentional;
- attach only required skills;
- use an absolute work directory where repository instructions are required;
- remember workdir jobs may serialize because of process-global working-directory behavior;
- deny dangerous command approvals in headless runs;
- prohibit recursive schedule creation;
- set a timeout and bounded retries;
- record last success and alert on staleness externally.

Lock shared state instead of relying on schedule spacing. A database job scheduled five minutes apart can still overlap after a slow run.

See [Suggested scheduled jobs](scheduled-jobs.md) for a concrete starter schedule, job record, silence contract, and enablement checklist.

## Provider and spend operations

- Record primary, fallback, and auxiliary models by profile.
- Alert on provider changes for unattended jobs.
- Prefer provider-diverse fallback.
- Place local inference last and label degraded output.
- Use provider quotas/hard limits where available.
- Track completed/failed calls separately from estimated cost.
- Do not infer zero cost from a missing price field.
- Review scheduled-job and optional public-bot volume before increasing limits.

When a provider fails, avoid immediate retry storms. One retry with jitter may be reasonable for transport failure; persistent 429/5xx should move sideways to a different provider or stop.

## Logs and evidence

Keep:

- gateway/error logs with secret redaction;
- cron job ID, scheduled time, start/end, status, delivery status;
- coding job ID/card ID, broker decision, OMP session/job ID, changed paths, verification exit codes;
- plugin and framework revisions;
- backup snapshot ID and restore-check result;
- operator approvals for irreversible actions.

Do not retain:

- raw tokens/refresh credentials;
- complete environment dumps;
- public conversation forever by default;
- full untrusted page bodies in trusted operational logs;
- unnecessary coding transcripts containing proprietary source.

Define retention before volume forces an emergency deletion.

## Backup and restore

Use both product exports and filesystem-aware backups:

```sh
hermes backup
# restore/migration path:
hermes import <backup-archive>
```

Also back up supporting repositories, custom extensions, service definitions, and OMP auth/session state. A profile export strips keys for sharing; it is not automatically a complete disaster-recovery copy.

Monthly or after material state changes:

1. select a recent snapshot;
2. restore one knowledge file, one config file, and one small database/archive into a temporary location;
3. compare checksums or structured contents;
4. validate permissions and ownership metadata where required;
5. delete staging;
6. record snapshot ID, commands, and result.

At a longer cadence, restore into an isolated replacement host/profile and prove a real gateway/model path with non-production credentials.

## Update runbook

For Hermes:

```sh
hermes update --check
hermes config check
hermes skills list-modified
```

Then:

1. read release notes;
2. take a backup;
3. record current revision/version and plugin pins;
4. stop creating new long jobs;
5. update Hermes;
6. run config migration/checks as directed by the live CLI;
7. restart the intended gateway process(es);
8. run profile matrix, platform message, cron preflight, plugin seam, research, and coding-bridge checks;
9. keep or roll back based on observed behavior.

For OMP:

1. update through the original package manager;
2. inspect changelog and `omp --help`;
3. run config listing and credential health;
4. run disposable-repository interactive and one-shot/RPC checks;
5. run coding-bridge positive/negative/cancellation tests;
6. verify auth broker/gateway if enabled.

Update search/extract/local-model containers separately. One change at a time preserves attribution.

## Drift runbooks

Use [Skill drift](skill-drift.md) when Agent Skills source, discovery policy, resolved
identity, or selection behavior may disagree. Use
[Extension and file drift](extension-and-file-drift.md) for plugins, hooks, profiles,
generated files, service units, or other artifacts whose source, deployment, loader, and
runtime state can diverge. Both require a silent-when-healthy deterministic check and
consumer-visible verification after reconciliation.

The public versions are starting points, not live operational state. Create a private
operational copy of each selected runbook in the LLM wiki or knowledge base your agents
actually use, adapt it to real owners, paths, authority, rollback, and checks, then link it
from the local runbook index so it is available through normal knowledge-base search. Preserve
the Stackbook source revision for provenance and revise the copy after field use.

## Failure playbooks

### Gateway unavailable

- Check supervisor state and Hermes logs.
- Confirm disk/memory and config validity.
- Start/restart only through the supported supervisor.
- Verify a real authorized message and profile route.
- Confirm cron resumed and no duplicate gateway exists.

### Search/extract unavailable

- Check loopback service health and resource pressure.
- Run a fixed canary query/URL.
- Keep the research profile unable to fabricate current results; return dependency failure.
- Use the metered fallback only within its budget.

### Local model unavailable

- Remove it from active fallback if calls hang or pressure the host.
- Verify cloud lanes still work.
- Restart only the local service if authorized.
- Re-run short and maximum operational context canaries before re-enabling.

### Coding bridge failure

- Stop accepting new jobs.
- Classify active process and worktree state.
- Preserve logs and Git evidence.
- Kill the verified process tree on cancellation/timeout.
- Do not auto-reset a dirty checkout.
- Verify OMP independently, then broker policy, then end-to-end delivery.

### Credential exposure

- Disable affected ingress/job/plugin.
- Rotate provider, bot, broker, and source-control credentials in the relevant scope.
- Invalidate cached snapshots/sessions as required.
- Search logs and history for propagation.
- Restore service with a fresh credential and a real end-to-end check.

## Maintenance cadence

| Cadence | Work |
|---|---|
| Continuous | External gateway dead-man, disk/backup age, failed/stale cron, resource pressure. |
| Daily | Exception-only operator brief; no “all good” chatter. |
| Weekly | Review failed jobs, unexpected fallback/spend, plugin/security advisories, unprocessed knowledge inbox, and evidence-backed improvement proposals. |
| Monthly | Restore sample, profile/tool matrix, unauthorized-input negative tests, dependency/security audit. |
| Before every update | Backup, release notes, seam inventory, baseline tests. |
| Quarterly | Re-evaluate providers, host sizing, optional public-bot data policy, skill/plugin necessity, retention, and recovery contacts. |

A monitor that routinely lies will be muted. Keep alarms few, reproducible, and actionable.
