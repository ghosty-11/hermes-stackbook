# Supporting services

Supporting services exist to make the agent stack more available and auditable. Each one adds an update, backup, and failure surface; install it only when its consumer exists.

## Network policy

Default bindings:

- SearXNG: loopback only.
- Firecrawl or Crawl4AI: loopback only.
- Ollama or other local inference: loopback only.
- OMP auth broker and auth gateway: loopback or authenticated private network only.
- Hermes dashboard/API: loopback or authenticated private network only.
- Metrics: loopback/private network; redact labels and logs.

Do not publish these ports directly. If another host needs them, use Tailscale/WireGuard or a TLS reverse proxy with authentication and an allowlist.

## SearXNG

Purpose: self-hosted metasearch for routine agent research.

Project: [searxng/searxng](https://github.com/searxng/searxng)

Deployment requirements:

- pin an image/tag or immutable digest;
- bind the published port to `127.0.0.1`;
- include JSON in `search.formats`, because programmatic clients require it;
- configure a private-instance limiter policy rather than inheriting public-instance assumptions;
- set timeouts and a bounded result count;
- keep no provider keys in agent-visible prompts;
- test at least two upstream engines and a query with no results.

Hermes supports a SearXNG search backend. Use the current official configuration docs and resolved config rather than copying an old key path. The readiness test is a real `web_search` call from the research profile, not an HTTP 200 from the SearXNG homepage.

## Firecrawl or Crawl4AI

Purpose: convert pages into bounded, cleaner text/Markdown for research.

- [Firecrawl](https://github.com/firecrawl/firecrawl) offers a broader extraction/crawl stack and requires several supporting services in a typical self-hosted deployment.
- [Crawl4AI](https://github.com/unclecode/crawl4ai) is a lighter alternative when full Firecrawl orchestration is unnecessary.

Hermes includes an upstream [Firecrawl web search/extraction plugin](https://github.com/NousResearch/hermes-agent/tree/main/plugins/web/firecrawl) with direct and self-hosted URL support. Use that maintained seam before writing another integration; a separate custom Firecrawl plugin is not required. Re-check the installed source because plugin activation and configuration can change by release.

For Firecrawl:

- follow the current upstream self-hosting compose files;
- prefer published images over an accidental source build;
- bind only the API surface required by Hermes;
- cap browser and worker concurrency to host memory;
- persist only required database/queue state;
- treat extracted text as untrusted;
- test JavaScript-rendered, static, blocked, oversized, and malformed pages.

For either extractor:

- cap response bytes and execution time;
- accept only `http`/`https` URLs;
- reject loopback, link-local, private-address, metadata-service, and file URLs at the trust boundary;
- do not automatically save extracted page text into the trusted knowledge base;
- return source URL and retrieval time with the extraction.

A hosted extraction API can be the emergency fallback. Put a spending cap on it; unattended retries can consume quota quickly.

## Ollama

Purpose: local degraded-mode inference when cloud providers are unavailable or private local processing is required.

Project: [ollama/ollama](https://github.com/ollama/ollama)

Operational rules:

- loopback bind only;
- one intentionally selected **loaded** model — enforce a single loaded model and single
  parallel request on memory-constrained hosts. A small on-disk inventory of alternates
  (a fallback tier, an emergency small model) is compatible with this rule; a zoo of
  routinely served models is not;
- cap concurrent requests on memory-constrained hosts;
- pin context and batch settings based on measurement;
- place the local lane last in fallback chains;
- label local results as degraded if the model cannot meet the normal contract;
- monitor memory pressure, swap, load time, prefill latency, and output correctness;
- prove cloud recovery returns traffic to the intended primary.

Test short, medium, and maximum operational contexts. Verify the answer, not only process survival. A model that loads but stalls during prompt prefill is not an available fallback.

Cloud and local models may have very different context windows. Avoid one global compaction threshold that unnecessarily clamps cloud sessions or overflows the local lane. If the framework cannot express fallback-specific context policy, add a narrow plugin only after reproducing the need.

## Private remote access

[Tailscale](https://tailscale.com) is a low-friction default; plain WireGuard or SSH tunnels are valid alternatives.

Keep these controls:

- device and user approval;
- least-privilege ACLs;
- no public funnel for admin surfaces;
- recovery procedure if identity state is lost;
- an out-of-band path to the host if the agent stack breaks networking;
- logs that do not expose auth tokens.

A private network is transport, not application authorization. OMP broker/gateway bearer tokens and Hermes user allowlists still apply.

## Knowledge base

Use a Git-backed Markdown repository when humans and several harnesses must share durable facts.
The [proposed wiki structure](knowledge-base-structure.md) is a field-tested starting layout;
adapt or omit folders rather than creating empty categories with no consumer.

Minimum conventions:

- a navigation page;
- canonical topic files instead of repeated session dumps;
- source links and dates for mutable claims;
- an append-only activity log if multiple writers need reconciliation;
- one routine writer for canonical files;
- an `inbox/` or equivalent for proposed/raw material;
- a separate path for untrusted captures;
- no secrets, tokens, private keys, or raw credential-bearing logs;
- regular link and freshness checks;
- normal Git review and backup.

Do not load the whole vault into every prompt. Search, read the relevant note, and keep raw web captures outside the trusted instruction path.

For a new agent-maintained knowledge base, [Andrej Karpathy's LLM Wiki method](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) is a useful starting pattern: humans curate sources and direct analysis; the assistant compiles durable interlinked Markdown, maintains it, and queries the compiled knowledge. Hermes ships a [built-in `research/llm-wiki` skill](https://github.com/NousResearch/hermes-agent/tree/main/skills/research/llm-wiki) that implements that method. Use it as-is for a fresh compatible wiki or adapt it to your own filename, metadata, provenance, trust-boundary, and multi-writer conventions; do not run two competing wiki procedures against one knowledge base.

## Backups

Back up state, not just source code:

- every Hermes profile home: config, auth, memory, skills/plugins, cron, sessions/state needed for recovery;
- OMP config, sessions needed for continuity, and credential database or broker database;
- knowledge repository;
- custom plugin/skill repositories;
- service configuration and deployment manifests;
- container volumes that cannot be recreated;
- mapping of bot/application credentials and their re-enrollment procedure.

Use encrypted off-host storage. [restic](https://restic.net) is one suitable option. Keep the repository password/recovery material outside the backed-up host.

A backup job passes only after:

1. the snapshot command exits successfully;
2. the expected paths exist in the snapshot;
3. retention is applied without deleting the only good generation;
4. a representative file is restored to a temporary directory;
5. restored content matches the source or a recorded checksum;
6. temporary restore data is removed;
7. failure or staleness is reported by an external monitor.

Field principles that earned their place:

- **The backup plane must survive the agent plane.** Supervise the backup as its own
  service/timer, not as part of the agent service group — stopping or crashing the agents
  must not cancel the backup.
- **Stage live databases consistently.** Copy SQLite through its online-backup API (and
  dump PostgreSQL logically) into a staging directory that the snapshot then captures;
  never snapshot raw live database files with their write-ahead logs. Refuse the snapshot
  when staging fails, loudly.
- **Expose a narrow non-secret status projection** (for example, last local and last
  off-host success timestamps in a world-readable file) so monitors and dashboards can
  assert freshness without reading the repository or its credentials.

## Sync and dashboards

Optional:

- Syncthing for an editable phone/laptop copy of the Markdown knowledge base;
- Hermes' native web dashboard for profile/config/session administration;
- [`hermes-workspace`](https://github.com/outsourc-e/hermes-workspace) for a community workspace UI after review;
- Netdata or another host monitor for CPU, memory, disk, and process health;
- Langfuse through Hermes' official plugin when trace review has a real owner.

Sync is not backup. A deleted or corrupted file can synchronize perfectly. A dashboard is not a health monitor. Keep recovery and dead-man checks independent.
