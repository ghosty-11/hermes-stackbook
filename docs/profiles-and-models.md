# Profiles and models

Profiles are useful when they separate state and capabilities. A large cast with the same tools is role-play, not architecture.

## Workload-specific reference roster

This roster reflects one deployed workload: private orchestration, quarantined research,
controlled knowledge writes, auditing, software engineering, and an optional public bot.
It is a reference architecture, not a required cast. Select a profile only when separate
state, credentials, capabilities, ingress, or failure domains enforce a named boundary.

| Profile | Inbound surfaces | Required tools | Explicitly absent | Model posture | Example starting model |
|---|---|---|---|---|---|
| Orchestrator | Private operator chat, CLI | task/kanban, read-only knowledge lookup, messaging, narrow research and coding delegates | raw web/browser on privileged turns; unrestricted public ingress | Strong general model; provider-diverse fallback | `Qwen/Qwen3.6-35B-A3B-FP8` for evaluation |
| Scribe | Scheduled/internal dispatch, optional CLI | file operations restricted to knowledge repository, source/provenance lookup | shell where avoidable; public ingress; coding credentials | Reliable writing model; low concurrency | `Qwen/Qwen3.6-35B-A3B-FP8` |
| Research quarantine | Internal subprocess/API only | search and extract only | shell, file writes, messaging admin, task board, private memory | Cheap public-content model is acceptable | `Qwen/Qwen3.6-35B-A3B-FP8` on public inputs |
| Auditor | Scheduled/manual review | read-only repository and evidence tools; optionally a tightly constrained OMP review call | writes, deploy, service control, self-trigger from orchestrator | Careful model; explicit evidence output | `Qwen/Qwen3.6-35B-A3B-FP8`; use a different provider/model for independent second opinions |
| Engineer dispatcher | Internal dispatch only | one typed OMP delegate, or a sandboxed native engineering surface—not both by default | public ingress, raw web, host administration | Code-capable routing model; OMP does the implementation | `Qwen/Qwen3.6-35B-A3B-FP8`; OMP selects the coding model |
| Optional public bot | Public chat | reply/reaction tools; optional image, voice, GIF, speaker-scoped memory | shell, files, private wiki, cron admin, kanban, coding bridge | Cheap model; strict spending and rate limits | `Qwen/Qwen3.6-35B-A3B-FP8` or another evaluated low-cost model |

The named Qwen model was listed by the [Hetzner experimental Inference API](https://docs.hetzner.com/general/company-and-policy/experiments/inference/) on 2026-08-14. It is a concrete evaluation starting point, not a universal default or production recommendation: Hetzner explicitly provides the experiment without availability guarantees, and the catalog can change. Re-check the live catalog, provider data terms, tool use, structured output, context, and latency. A shared starting model simplifies comparison; availability-critical fallbacks must cross provider boundaries.

You do not need all six. For a similar workload, start with orchestrator, add research before granting web, add scribe before automated knowledge writes, and add the optional public bot last—only if you want that hosted-for-fun feature. For a different workload, start with the smallest role that serves it and add a profile only when separate state, credentials, capabilities, or ingress enforce a real boundary.

## Create profiles

Use the installed CLI's `--help` first. Current upstream examples:

```sh
hermes profile create scribe --description "Maintains the approved Markdown knowledge base from sourced handoffs."
hermes profile create research --description "Searches and extracts public sources; returns bounded cited findings."
hermes profile create auditor --description "Performs read-only evidence-backed reviews and proposes changes."
hermes profile create engineer --description "Routes bounded software tasks to the coding harness."
hermes profile create public-bot --description "Optional public chat with no private or host capabilities."
```

A blank profile receives its own `config.yaml`, `.env`, `SOUL.md`, memory, sessions, skills, cron jobs, and state. Avoid `--clone-all` when profiles should not share tokens, memory, plugins, or schedules.

Inspect each profile:

```sh
hermes profile list
hermes profile show research
hermes -p research doctor
hermes -p research tools
hermes -p research skills list
```

## SOUL, project instructions, and controls

Use each layer for its actual job:

- **`SOUL.md`:** profile identity, decision posture, escalation rules, output style.
- **Project `AGENTS.md`/`CLAUDE.md`/`.cursorrules`:** repository-local engineering instructions loaded from the working directory where supported.
- **Tool configuration:** capabilities the model can invoke.
- **Platform policy:** who may send messages and which profile receives them.
- **OS/container boundary:** files, processes, and credentials the runtime can reach.
- **Plugins/hooks:** deterministic interception or new typed tools.
- **Skills:** procedures loaded when their trigger matches.

Do not put prohibitions only in `SOUL.md`. “Never writes files” is untrue if the profile still receives file-write or terminal tools.

Starter profile text lives in [Profile SOUL templates](../templates/profile-souls.md). Keep it short; tool schemas and relevant skills already consume the system prompt.

## Toolset method

For each profile:

1. Begin with no optional tools.
2. Add the minimum toolset required by one acceptance scenario.
3. Inspect the resolved tools on every surface: CLI, gateway/chat, cron, and delegated worker.
4. Run one positive test (required operation succeeds).
5. Run one negative test (forbidden operation is unavailable, not merely declined in prose).
6. Record the result in the deployment's private profile matrix.

Use [the profile matrix template](../templates/profile-matrix.md). Re-run it after upgrades and plugin changes.

## Terminal and filesystem boundaries

Hermes profiles isolate state, but upstream explicitly warns that they do not sandbox filesystem access. On the local terminal backend, the process has the OS user's access.

Choices, from weakest to strongest:

1. `terminal.cwd` sets a predictable starting directory; it is not confinement.
2. `terminal.home_mode: profile` gives subprocesses profile-local CLI config; it does not prevent traversal to other readable paths.
3. Hermes write sandbox and tool restrictions narrow file operations.
4. Docker, Singularity, Modal, Daytona, or Vercel Sandbox isolate execution according to the backend.
5. A separate OS user plus filesystem permissions separates host credentials and repositories.
6. A dedicated service/broker exposes only typed operations across the boundary.

Use the strongest boundary required by the data, not by the role name.

## Gateway deployment

### Separate processes

Install and start one service per online profile:

```sh
scribe gateway install
scribe gateway start
research gateway install
research gateway start
```

Use this for the first deployment and for an optional public bot, if enabled.

### Multiplexed private profiles

On the default profile:

```sh
hermes config set gateway.multiplex_profiles true
```

Set an explicit `gateway.multiplex_profile_allowlist` in `config.yaml`, then restart only after reviewing the official [multiplexing contract](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways). Do not run secondary gateway services for profiles served by the multiplexer.

Test per-profile model, `.env`, memory, skill, cron, and platform resolution. A shared process reduces service count; it does not reduce the need for profile-by-profile verification.

## Model routing

Create a private model ledger with one row per profile and auxiliary lane:

| Lane | Primary | Provider | Fallback | Privacy class | Context tested | Spend cap |
|---|---|---|---|---|---|---|
| Orchestrator |  |  |  | private |  |  |
| Scribe |  |  |  | private |  |  |
| Research |  |  |  | public content |  |  |
| Auditor |  |  |  | private source |  |  |
| Optional public bot |  |  |  | public |  |  |
| Vision |  |  |  | varies |  |  |
| Compression |  |  |  | same as parent |  |  |
| Cron default |  |  |  | varies |  |  |
| Local floor |  | local | none | on-host |  |  |

Rules:

- Pin a primary and provider-diverse fallback per profile where failure matters.
- Configure cron inference separately; keep Hermes' model drift guard unless changing global models should deliberately reroute cron spend.
- Treat vision, compression, extraction, and decomposition as independent auxiliary lanes with their own credentials and failure modes.
- A local fallback is degraded mode. It may require a lower task size, smaller tool schema, and different compaction threshold.
- Test the exact context length and workload. A model's advertised context is not an operational guarantee on local hardware.
- Do not use identity-linked free providers for private wiki or host context unless their data handling is acceptable.

## Memory

Give each profile one canonical memory system. Two active stores produce confident misses.

Options:

- Hermes built-in memory;
- an upstream memory provider such as Honcho;
- a reviewed append-only local memory exposed through narrow tools;
- no persistent memory for stateless quarantine/auditor jobs.

For an optional public bot, scope facts by stable numeric platform user ID, not display name. Do not let a public identity recall another user's information. Subagents should not mutate persistent memory unless that is the explicit task.

## Profile acceptance

A profile is ready only when:

- an authorized positive scenario works on its real surface;
- an unauthorized sender is rejected;
- every forbidden tool is absent from the resolved schema;
- its model and fallback are observed in a real call;
- its memory writes only to its own store;
- its credentials are distinct where required;
- stopping/restarting it has the expected blast radius;
- its logs identify failures without leaking secrets.
