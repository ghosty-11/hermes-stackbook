# Sources and further reading

Reviewed 2026-08-14. Prefer official documentation and source repositories for behavior. Community directories are discovery aids, not security endorsements. Re-check all links and installed CLI help before a deployment or public release.

## Hermes Agent — primary

- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — source, releases, issues, examples, and bundled artifacts.
- [Official documentation](https://hermes-agent.nousresearch.com/docs/) — current quickstart and product guide.
- [CLI commands reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md) — terminal command families including status, backup/import, security audit, skills, plugins, profiles, gateway, egress, and cron.
- [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration/) — config precedence, secrets, terminal backends, provider timeouts, updates, and managed settings.
- [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles/) — profile state, creation, services, and the explicit warning that profiles are not sandboxes.
- [Running Many Gateways](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways) — separate-process default, multiplexing, allowlists, token conflicts, and profile routes.
- [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security/) — authorization, approvals, deny rules, file safety, isolation, and input controls.
- [Cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) — model pins, no-agent mode, preflight, model drift, work directories, delivery, and job lifecycle.
- [Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) — discovery, installation, enablement, authoring, and bundles.
- [Built-in skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) — current bundled inventory.
- [Optional skills catalog](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog) — official optional inventory.
- [Plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins) — plugin APIs, discovery, activation categories, immutable pins, and distribution.
- [Built-in plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins) — official plugin inventory.
- [Kanban](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban) — profile collaboration and task routing.
- [Memory providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers) — external memory architecture.
- [MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) — server/tool integration and credential considerations.
- [Web dashboard](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard) — machine-level profile/config/session administration.

## OMP — primary

- [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) — source, README, releases/changelog, issues, and install methods.
- [omp.sh](https://omp.sh) — project site and installer.
- [Settings](https://github.com/can1357/oh-my-pi/blob/main/docs/settings.md) — global/project/CLI precedence and settings schema.
- [Models](https://github.com/can1357/oh-my-pi/blob/main/docs/models.md) and [providers](https://github.com/can1357/oh-my-pi/blob/main/docs/providers.md) — model/provider configuration and auth resolution.
- [Auth broker and gateway](https://github.com/can1357/oh-my-pi/blob/main/docs/auth-broker-gateway.md) — centralized OAuth/API-key storage, refresh, authenticated model gateway, cache, and operator-owned transport security.
- [Skills](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md) — skill discovery and configuration.
- [Context files](https://github.com/can1357/oh-my-pi/blob/main/docs/context-files.md) — project/user instruction discovery.
- [LSP configuration](https://github.com/can1357/oh-my-pi/blob/main/docs/lsp-config.md) — language-server integration.
- [Agent Hub](https://github.com/can1357/oh-my-pi/blob/main/docs/agent-hub.md) — subagent supervision and coordination.
- [RPC](https://github.com/can1357/oh-my-pi/blob/main/docs/rpc.md) — structured process integration.
- [SDK](https://github.com/can1357/oh-my-pi/blob/main/docs/sdk.md) — Node/TypeScript embedding.
- [Hooks](https://github.com/can1357/oh-my-pi/blob/main/docs/hooks.md) and [extensions](https://github.com/can1357/oh-my-pi/blob/main/docs/extensions.md) — local integration surfaces.
- [Local models](https://github.com/can1357/oh-my-pi/blob/main/docs/local-models.md) — local endpoint considerations.

## Skill standards and public skill sources

- [Agent Skills](https://agentskills.io) — portable skill format.
- [obra/superpowers](https://github.com/obra/superpowers) — engineering workflow skills and skill-authoring patterns.
- [mattpocock/skills](https://github.com/mattpocock/skills) — engineering interview, domain, and planning skills.
- [anthropics/skills](https://github.com/anthropics/skills) — Anthropic's public skill examples and document workflows.
- [Andrej Karpathy's LLM Wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and [Hermes' implementing `llm-wiki` skill](https://github.com/NousResearch/hermes-agent/tree/main/skills/research/llm-wiki) — compiled, persistent, agent-maintained Markdown knowledge bases.

## Hermes ecosystem directories

- [ZeroPointRepo/awesome-hermes-skills](https://github.com/ZeroPointRepo/awesome-hermes-skills) — dedicated install-ready skills directory plus plugins, profiles, providers, surfaces, and tools.
- [0xNyk/awesome-hermes-agent](https://github.com/0xNyk/awesome-hermes-agent) — broad independent ecosystem directory and operational resources.
- [42-evey/hermes-plugins](https://github.com/42-evey/hermes-plugins) — community plugin implementations and design patterns.
- [42-evey/vigilguard](https://github.com/42-evey/vigilguard) — config/intent guard reference.

First-party packages from this project, listed here so their provenance is explicit rather than
implied: [ghosty-11/hermes-omp-broker](https://github.com/ghosty-11/hermes-omp-broker),
[ghosty-11/hermes-mailbox](https://github.com/ghosty-11/hermes-mailbox),
[ghosty-11/hermes-optmem-tools](https://github.com/ghosty-11/hermes-optmem-tools),
[ghosty-11/hermes-trace](https://github.com/ghosty-11/hermes-trace) and
[ghosty-11/hermes-discord-ambient](https://github.com/ghosty-11/hermes-discord-ambient).
Each carries its own tests and documentation; review the current release and the upstream seam
it depends on before use.

## Free endpoint and developer-program starting points

- [Hetzner experimental Inference API](https://docs.hetzner.com/general/company-and-policy/experiments/inference/) — OpenAI-compatible experimental inference with no production guarantee.
- [OpenRouter Free](https://openrouter.ai/openrouter/free) — free router and zero-price model SKUs.
- [NVIDIA API Catalog](https://build.nvidia.com/models) — hosted model evaluation endpoints and account-dependent developer credits.
- [AMD AI Developer Program](https://developer.amd.com/ai-developer-program/) — time-limited developer cloud credits, not a permanent endpoint.
- [Google AI Studio rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) and [Groq rate limits](https://console.groq.com/docs/rate-limits) — model-specific developer tiers.

## Supporting services

- [SearXNG](https://github.com/searxng/searxng) — self-hosted metasearch.
- [Firecrawl](https://github.com/firecrawl/firecrawl) — extraction and crawling stack.
- [Hermes Firecrawl plugin](https://github.com/NousResearch/hermes-agent/tree/main/plugins/web/firecrawl) — bundled direct/self-hosted Firecrawl integration; a custom adapter is not required for the basic path.
- [Crawl4AI](https://github.com/unclecode/crawl4ai) — lighter extraction/crawling alternative.
- [Ollama](https://github.com/ollama/ollama) — local model runtime and OpenAI-compatible endpoint.
- [restic](https://restic.net) — encrypted deduplicating backup.
- [Tailscale](https://tailscale.com) and [WireGuard](https://www.wireguard.com) — private network options.
- [Syncthing](https://syncthing.net) — file synchronization, not backup.
- [Obsidian](https://obsidian.md) — optional human interface for a Markdown knowledge base.
- [Langfuse](https://langfuse.com) — optional trace/observability backend supported by an official Hermes plugin.

## Security and architecture references

- [Meta: Practical AI agent security](https://ai.meta.com/blog/practical-ai-agent-security/) — capability/trust-boundary framing, including the Rule of Two.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — common application risks.
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — governance and risk vocabulary.
- [The Update Framework](https://theupdateframework.io) and [SLSA](https://slsa.dev) — software supply-chain concepts relevant to plugin and binary distribution.

## How to use this index

1. Start with the installed CLI's `--help`.
2. Read the official page for the surface being changed.
3. Inspect source when behavior or security semantics matter.
4. Use community catalogs to discover alternatives.
5. Review and pin the selected artifact.
6. Measure the real path on your host.
7. Record the installed revision and evidence privately.

Do not infer production readiness from stars, catalog inclusion, a maturity badge, or a README alone.
