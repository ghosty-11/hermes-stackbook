# Planning

Make the deployment decisions before creating profiles or installing community extensions.

## Minimum prerequisites

- A Linux or macOS host you administer, or a Windows host with Windows Subsystem for Linux 2 (WSL 2). Run the stack inside the WSL 2 Linux distribution; native Windows installation is not tested, recommended, or endorsed by this guide. Linux with systemd remains the simplest always-on target.
- Git, `curl`, an SSH client, and a supported container runtime if self-hosting search/extraction.
- Bun if using the recommended OMP package install.
- One private model-provider credential or subscription for Hermes.
- One coding-provider credential or subscription if OMP is enabled.
- A private messaging-platform bot token if chat control is required.
- A private network path such as Tailscale or WireGuard for remote administration.
- An encrypted backup destination that is not the same filesystem as the host.

Do not expose the Hermes dashboard, gateway, OMP auth broker, OMP auth gateway, Ollama, SearXNG, or Firecrawl directly to the public internet. Bind loopback services to `127.0.0.1`; use an authenticated private network or reverse proxy where remote access is required.

## Host sizing bands

These are planning bands, not benchmark promises. Measure the models and container versions you select.

| Deployment | CPU/RAM starting point | Storage | Notes |
|---|---|---|---|
| Hermes with optional OMP clients, hosted models, no local extractor | 2–4 cores, 8–16 GiB RAM | 40+ GiB SSD | Lowest operational weight. Use hosted extraction or add only SearXNG. |
| Hermes with optional OMP, SearXNG, and Firecrawl | 4–8 cores, 16–32 GiB RAM | 80+ GiB SSD | Firecrawl adds browser, queue, cache, and database containers. Cap worker concurrency. |
| Above plus CPU Ollama fallback | 8+ modern cores, 32–64+ GiB RAM | model size plus 50+ GiB headroom | A local model is an outage floor, not automatically cheaper or faster. Context length drives memory and prefill cost. |
| GPU inference | Hardware-specific | model and runtime artifacts | Validate exact GPU architecture, runtime, model quantization, context, and recovery behavior in a shadow service first. |

If the host is small, prefer Crawl4AI or a metered extraction fallback over an underprovisioned multi-container Firecrawl deployment.

## Account and identity plan

Use separate identities where their authority differs:

| Identity | Holds | Must not hold |
|---|---|---|
| Hermes service account | Hermes profile homes, messaging tokens, selected model keys, access to approved service sockets | Operator SSH keys, unrestricted GitHub auth, OMP subscription refresh tokens |
| Operator account | OMP, coding subscriptions, source repositories, local review tools | Optional public-bot runtime |
| Backup identity | Write access to backup destination, read access to explicit backup inputs | General shell or provider credentials |
| Optional public-bot profile/account | Its bot token, its model key, speaker-scoped memory if needed | Private wiki, shell, cron administration, coding bridge, operator credentials |

A Hermes profile has a separate `.env`, but a profile is not an operating-system security boundary. On the local terminal backend, profiles under one OS user can reach that user's files. Use separate OS users, Docker/another isolated backend, file permissions, or a service boundary when that matters.

This table is also the unit of separation for a [central secret store](secret-store.md): give each
identity its own encrypted file and its own key, so consolidating credentials does not quietly let
one identity decrypt another's. Deciding the store early is cheaper than migrating scattered
credential files later.

## Provider plan

For each role, record:

- primary provider and model;
- fallback provider and model;
- maximum context you have actually exercised;
- whether prompts may contain private host or wiki data;
- whether the provider trains on or retains prompts;
- rate limits and expected failure class;
- unattended spending ceiling;
- local fallback behavior, if any.

A fallback chain should cross provider boundaries. Three models behind one provider usually share the same outage and rate-limit domain.

Keep public-content roles on cheaper models if desired. Keep private operational context on providers whose data handling you accept. Pin cron models separately from interactive chat so a global model switch does not silently change unattended spend.

## Service choices

| Need | Default recommendation | Alternative | Decision criterion |
|---|---|---|---|
| Search | SearXNG on loopback | Hosted search API | Run cost and result quality versus provider quota. |
| Extraction | Firecrawl on loopback | Crawl4AI or hosted API | Firecrawl quality/features versus container weight. |
| Local inference floor | Ollama on loopback | llama.cpp, LM Studio, none | Measured context, latency, RAM, and operational burden. |
| Remote admin | Tailscale | WireGuard/SSH tunnel | Existing network and identity policy. |
| Knowledge base | Git-backed Markdown/Obsidian | A typed document store | Human readability, source control, and deterministic export. |
| Backups | restic to off-host repository | Borg, provider snapshots plus tested export | Encryption, retention, and restore verification. |
| Observability | Native logs + external health check | Langfuse and host metrics | Add tracing only when someone will read it. |

## Gateway topology decision

Start with one process per profile. Choose multiplexing only after answering yes to all of these:

- A shared restart domain is acceptable.
- Every secondary profile has a distinct bot token or an explicit supported route.
- HTTP-inbound platform configuration follows the `/p/<profile>/` contract.
- The allowlist names exactly the profiles the gateway should serve.
- Plugins and profile-specific credentials were tested under multiplexing.
- The optional public-facing profile, if enabled, does not need a stronger process boundary.

## Initial scope

The first deployment should contain only:

- one private Hermes profile;
- one private messaging surface or CLI;
- one primary model and one provider-diverse fallback;
- OMP installed for interactive use only when dedicated software engineering is selected;
- external backup of the minimal state;
- no community plugin and no autonomous model cron.

Add components in the order defined in [Build sequence](build-sequence.md). The sequence is designed so every phase leaves a useful, recoverable system.

## Decision worksheet

Copy this into your own private deployment record:

```text
Host OS and supervisor:
Hermes install method and pinned revision/version:
OMP install method and pinned version, if selected:
Gateway topology: separate | multiplexed | hybrid
Private messaging surface:
Public surface, if any:
Hermes service account:
OMP/operator account:
Primary/fallback provider per role:
Search backend, if selected:
Extraction backend, if selected:
Local inference floor, if selected:
Private network:
Knowledge-base repository, if selected:
Backup repository and retention:
Restore drill cadence:
Expected monthly model/service budget:
Approval owner:
Public-release owner:
```

Do not put credentials, account IDs, bot tokens, private hostnames, or recovery keys in this repository. Keep the completed worksheet in a private operations store.
