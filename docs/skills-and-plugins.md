# Skills and plugins

> **Scope:** optional. A first private profile needs no added skills or plugins — skip this
> while evaluating and return when you have a specific job for one.

A skill is model-readable procedure. A plugin is executable code that can add tools, hooks, commands, platforms, model backends, memory providers, or context engines. Treat those risk levels differently.

## Start with upstream inventories

Before searching the community, inspect what the installed Hermes already contains:

```sh
hermes skills list
hermes skills browse
hermes plugins
hermes tools
```

Official references:

- [Hermes built-in skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog)
- [Hermes optional skills catalog](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog)
- [Hermes skills guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- [Hermes built-in plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins)
- [Hermes plugin system](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)
- [Agent Skills open format](https://agentskills.io)

Do not copy skill counts into deployment policy. The catalogs change. Query the installed release.

## Community directories

Use both major catalogs; they overlap but organize the ecosystem differently.

| Directory | Strength | Caveat |
|---|---|---|
| [ZeroPointRepo/awesome-hermes-skills](https://github.com/ZeroPointRepo/awesome-hermes-skills) | Install-ready inventory of built-in, optional, and community skills plus plugins, profiles, memory providers, surfaces, and tools | Editorial status is not a security review; entries and counts are release-specific. |
| [0xNyk/awesome-hermes-agent](https://github.com/0xNyk/awesome-hermes-agent) | Broad ecosystem map with skills, plugins, memory, deployment, GUIs, bridges, guides, and operational playbooks | Independent project; maturity labels are snapshots. |
| [42-evey/hermes-plugins](https://github.com/42-evey/hermes-plugins) | Concrete patterns for research, Discord/voice, inter-agent bridges, proactive behavior, and cost control | Review each plugin and upstream seam; do not install the suite as one trusted unit. |
| [Hermes Skills Hub](https://agentskills.io) / `hermes skills browse` | Portable discovery and installation | Community instructions are untrusted content and may assume broad tools. |

Useful ecosystem projects to evaluate when the matching need exists:

- [hermes-workspace](https://github.com/outsourc-e/hermes-workspace) — community web workspace/GUI;
- [SkillClaw](https://github.com/AMAP-ML/SkillClaw) — skill evolution/maintenance, only after a real eval corpus exists;
- [hermes-eval](https://github.com/Saurav0989/hermes-eval) — skill regression and trajectory evaluation;
- [lintlang](https://github.com/hermes-labs-ai/lintlang) — deterministic instruction/tool-description linting;
- [custom-dangerous-patterns](https://github.com/scross01/hermes-custom-dangerous-patterns-plugin) — additional command-approval patterns;
- [OptMem](https://github.com/VictorTaelin/OptMem) — compact append-only memory approach;
- [VigilGuard](https://github.com/42-evey/vigilguard) — design reference for intent/config checks.

These are candidates, not a recommended bundle. Read source, release history, issue state, install scripts, permissions, network destinations, and license before use.

### First-party packages from this project

These are this guide's own released plugins, each running in the reference deployment. They
are listed here so the review procedure below applies to them exactly as it applies to any
third-party extension — being first-party is provenance, not an exemption.

| Package | Category | Read this before enabling it |
|---|---|---|
| [hermes-optmem-tools](https://github.com/ghosty-11/hermes-optmem-tools) | Registered memory tools | Wraps the upstream OptMem store listed above. It exists so a profile can hold persistent memory *without* a terminal toolset; the model never supplies a command, path, or executable. Profiles with no memory directory configured never see the tools. |
| [hermes-mailbox](https://github.com/ghosty-11/hermes-mailbox) | Cross-harness transport | Message bodies are information, not authority. Grant it to a profile only when a task ledger alone cannot deliver the work. |
| [hermes-omp-broker](https://github.com/ghosty-11/hermes-omp-broker) | Coding delegation | Registers one narrow tool whose repository argument is validated against server-side policy. Its broker runs as a separate identity from the agent that calls it. |
| [hermes-discord-ambient](https://github.com/ghosty-11/hermes-discord-ambient) | Platform adapter | Replaces a bundled platform adapter, so it must be enabled in the profile that owns that adapter — enabling it at the root profile does not cover a multiplexed profile's own adapter scope. |
| [hermes-trace](https://github.com/ghosty-11/hermes-trace) | Observer hooks | Registers no tools and returns nothing from every handler, so it cannot influence a turn. Read what a trace file contains before enabling it: tool names, clipped tool arguments and results, model names and skill names make trace output as sensitive as the conversations it observes. |
| [hermes-web-research](https://github.com/ghosty-11/hermes-web-research) | Delegated tool | The quarantine profile's own tool surface is the blast radius: an injection that owns its turn gets whatever that seat holds. Verify that seat's *resolved* schema per surface before enabling this anywhere — config membership is not resolved capability. Raising the answer or source caps widens exactly the channel the boundary exists to narrow. |

## Minimal Hermes skill set

A private orchestrator or engineer usually benefits from:

- `hermes-agent` for framework operations;
- `systematic-debugging`;
- `test-driven-development`;
- planning/review/simplification skills that match your workflow;
- GitHub skills only when that profile actually has `gh`, Git credentials, and authorization;
- research/citation skills only on a profile with the required research tools;
- document/media skills only when their runtime dependencies are installed and exercised.

Disable or omit:

- coding-CLI delegation skills when OMP is the selected coding bridge;
- any skill whose verbs require tools the profile does not have;
- duplicate skills with the same trigger and conflicting procedures;
- broad offensive-security or “god mode” skills on live profiles;
- a bundled wiki skill when it conflicts with your canonical knowledge-base conventions;
- autonomous skill creation until writes require approval and created skills are reviewed before loading.

A large index adds selection ambiguity and prompt cost. Curate per profile.

## OMP skill sources

OMP loads skills from configured directories and reads them on demand. Keep one reviewed repository as the canonical custom skill directory; do not point OMP at a pile of mutable checkouts.

Good public sources:

| Source | Useful starting points | Adaptation required |
|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | systematic debugging, TDD, verification, skill authoring | Remove ceremony unsupported by your workflow; keep observable contracts. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | grilling/interviewing, domain modeling, wayfinding | Avoid duplicate TDD/review triggers. |
| [anthropics/skills](https://github.com/anthropics/skills) | skill creation and document workflows | Install only formats you produce. |
| [OMP's own skills docs](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md) | discovery/configuration behavior | Follow current custom-directory and precedence rules. |
| [Agent Skills](https://agentskills.io) | portable format | Host capabilities and security semantics still differ. |

## Suggested custom skills to develop

This is a capability roadmap, not a bundle to install wholesale. Develop a skill only when
the procedure is repeatedly non-obvious, then narrow its trigger to the profiles and tools
that can actually perform it.

| Suggested skill | General purpose | Release gate |
|---|---|---|
| Design and architecture decisions | Distinguish decisions that belong in code, configuration, deterministic checks, operator choices, or model judgment. | Worked examples show that it avoids unnecessary automation without blocking legitimate judgment. |
| Shared knowledge bases | Reconcile durable facts, decisions, claim evidence, links, and concurrent writers in a Git-backed knowledge base. | Private paths and facts are removed; link, vocabulary, freshness, and conflicting-writer checks pass. |
| Scheduled-job authoring | Design owned, observable, silent-when-healthy scheduled work and choose code instead of inference when the result has one right answer. | A manual failure fixture and one natural scheduled delivery prove the monitoring boundary. |
| Systematic debugging | Establish root cause from evidence before changing code or configuration, with a stop after repeated failed fixes. | A representative defect proves the procedure rejects symptom suppression and follows evidence across components. |
| Test-driven implementation | Put behavioral assertions, harness guards, agent evals, and temporal monitors at the layer able to answer the intended question. | The assertion is observed failing for the intended reason before the implementation makes it pass. |
| Verification before completion | Match each completion claim to fresh independent evidence from the real changed surface. | Examples cover code, configuration, services, scheduled work, UI, and delegated changes without treating source inspection as proof. |
| Honest outcome reporting | Report what changed, what failed, what remains, and a clear MET, PARTIALLY MET, or NOT MET verdict. | Evaluation includes partial success and blocked work, not only clean completions. |
| Operator decisions and escalation | Present the question, live evidence, recommendation, strongest counterargument, impact, authority, and rollback at a real decision gate. | Nearby routine actions do not trigger unnecessary operator interruption. |
| Agent-to-agent handoffs | Transfer bounded work with ownership, inputs, acceptance criteria, evidence provenance, and a safe fallback when the receiving agent fails. | Multi-writer and partial-failure scenarios preserve attribution and do not claim unverified delegated work. |
| Runbook operations | Execute controlled recovery or maintenance with authority checks, preflight, one writer, stop conditions, independent verification, and rollback evidence. | A tabletop or safe fixture proves that missing authority and changed live state stop mutation. |
| Long-running stateful jobs | Protect warehouses, indexes, backups, and other stateful stores with locks, production windows, resumability, and post-run coverage checks. | Interruption, stale-lock, concurrent-writer, and recovery paths are exercised against disposable state. |
| Skill authoring and maintenance | Define triggers, progressive disclosure, source ownership, discovery, collision checks, drift detection, and positive plus nearby-negative selection tests. | A fresh harness process resolves the intended source and the negative prompt does not select it. |
| Domain modeling and requirements grilling | Sharpen terminology, invariants, decision trees, acceptance boundaries, and architectural decisions before implementation. | The process converges to reviewable decisions without inventing requirements or prolonging resolved questions. |
| Repository audits and change review | Review complete repository scope, prioritize actionable defects, separate historical evidence from current behavior, and record remediation status. | Coverage is attributable to an immutable revision and every finding has evidence, consequence, and verification. |
| Harness engineering | Evaluate context cost, tool surfaces, compaction, delegation boundaries, observability, and the smallest honest behavioral eval. | Guidance is verified against at least one real harness seam and does not treat configuration as reachable behavior. |

This roadmap does not publish or copy private skill bodies. It describes reusable capability
gaps so readers can build procedures that fit their own harness, authority model, tools, and
deployment.

Separately, reviewed public skill releases are planned, with no promised release dates. A
candidate should be released only after provenance and licensing review, removal of
deployment-specific identities and paths, explicit tool and security assumptions, trigger
collision checks, positive and nearby-negative selection evidence, and a maintenance owner.
Until then, the table is design guidance rather than a promise that an installable artifact
exists.

Stable facts belong in documentation. Deterministic prohibitions belong in permissions,
hooks, or code.

## Hermes skill selection constraints

Hermes' skill index description budget is intentionally short. Put the trigger first:

```text
Use when debugging unexpected behavior before proposing fixes.
```

Do not begin with genre filler such as “A comprehensive guide to…”. Verify the current installed description limit before authoring; do not depend on a remembered number.

Eligibility and enablement are separate:

- per-profile disabled lists;
- platform-specific disabled lists;
- OS/platform frontmatter;
- required toolsets/environments;
- profile tool availability;
- attached/preloaded cron skills.

A skill listed on disk can still be unreachable. Exercise its trigger on the intended profile and surface.

## Plugin policy

Plugins execute code at discovery/load/runtime. Review them as software dependencies.

For each plugin:

1. Name the exact need and consumer.
2. Read `plugin.yaml`, entry point, handlers, hooks, install scripts, dependencies, and outbound requests.
3. Check whether it registers model-facing tools, invisible hooks, platform admission, an LLM call, or a credential reader.
4. Pin an immutable full commit where the installer supports it.
5. Enable it only on the intended profile/process.
6. Inspect the resolved tool schema and prompt size.
7. Run positive, negative, failure, and restart tests.
8. Record upstream methods/files it wraps.
9. Re-run seam tests before every Hermes or plugin update.
10. Keep rollback to the prior commit and config state.

Hermes supports user plugins without modifying core. Prefer that seam. A user plugin with the same name as a bundled plugin can override it; avoid accidental collisions.

## Official plugins to consider first

Enable only when consumed:

- `disk-cleanup` for managed Hermes temporary files;
- `security-guidance` for write/patch warnings;
- one image-generation backend for a profile that generates images;
- Langfuse observability when someone will inspect traces.

Built-in platform, memory, context-engine, and model-provider plugin categories have different activation rules. Read the current [plugin guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins) rather than assuming `plugins.enabled` gates every category.

## Supply-chain checklist

Before installation:

- license is compatible with intended public/private use;
- repository owner and maintenance history are understood;
- full dependency tree and install commands reviewed;
- no `curl | sh` or opaque binary accepted without provenance/checksum;
- secrets and network destinations documented;
- tool descriptions match handler behavior;
- irreversible actions require human approval;
- update source can be pinned;
- removal and data cleanup are documented;
- test can fail when the plugin is broken.

After installation:

```sh
hermes security audit
hermes plugins
hermes prompt-size
```

Then run the profile-specific acceptance scenario. A clean dependency scan does not prove safe behavior, and a catalog badge does not replace review.
