# Glossary

Only terms this guide uses in a specific way. It is not a general AI glossary. If a page uses
one of these words and you are unsure, the definition here is the one that page means.

## The core objects

| Term | Meaning here |
|---|---|
| **agent stack** | The programs, accounts, model connections, storage, and services that let an assistant keep working beyond a single chat reply. |
| **harness** | Software that gives a model a working environment — tools, instructions, and a workflow — rather than only a chat box. Hermes and OMP are both harnesses. |
| **gateway** | Hermes' long-running service. It receives requests from a chat platform or API and routes each one to the right profile. |
| **profile** | One separately configured Hermes assistant: its own settings, memory, credentials, instructions, and allowed tools. **A profile separates state, not filesystem access** — see [Profiles and models](profiles-and-models.md). |
| **surface** | A way to reach an agent: command line, chat gateway, scheduled job, or delegated worker. The same profile can have *different* tools on different surfaces. |
| **toolset** | The tools a profile actually has on a given surface (shell, file access, web search, image generation…). |
| **resolved** vs **configured** | Configured is what a file says. Resolved is what the running system actually grants after defaults, overrides, and extensions combine. When they disagree, resolved wins — so verification always checks resolved. |
| **provider** | The company and account through which prompts reach a model (a hosted API, or a local runtime). |
| **model lane** | A separately configured model use-case — interactive chat, vision, scheduled jobs, summarising, local fallback — which may each use a different model. |
| **fallback chain** | The ordered alternatives tried when the preferred model is unavailable or rate-limited. **Provider-diverse** means the alternatives are at different companies, so one outage does not disable everything. |
| **context window** | How much text a model can consider at once. |
| **compaction** | Shortening or summarising a long conversation so it still fits the context window. |

## Instructions versus permissions

The single most important distinction in this guide.

| Term | Meaning here |
|---|---|
| **persona / `SOUL.md`** | Behavioural instructions: tone, priorities, what an assistant *should* do. **Not a permission.** |
| **charter** | A written role boundary ("never edits code"). Also not a permission — a model can ignore prose. |
| **permission boundary** | Something that makes an action impossible rather than discouraged: an absent tool, a missing credential, a separate OS user, a network rule, a container without host mounts. |
| **capability matrix** | A record of what each profile can actually do on each surface, built from resolved state rather than intent. |
| **autonomy envelope** | Written-down limits on what an agent may decide alone, what it must escalate, and what it must never do. |
| **trust boundary** | A point where data or authority passes between differently trusted parts, so what crosses must be limited deliberately. |
| **quarantine** | A component that may handle untrusted material (public messages, fetched web pages) but has no tools or credentials to affect anything private. |
| **fail closed / fail open** | Fail closed denies when a check is missing or fails. Fail open allows by default — which is how access silently widens. |
| **blast radius** | How much breaks, or how much is exposed, when one component fails or is compromised. |

## Extending and automating

| Term | Meaning here |
|---|---|
| **skill** | A written procedure the model can load when the situation it describes applies. Text, not code. |
| **plugin** | Executable extension code that adds or changes tools, hooks, and behaviour. Code, so it carries code's risks. |
| **cron job / scheduled job** | Work configured to run automatically on a timer. |
| **no-agent job** | A scheduled job that runs a deterministic script and delivers its output, with **no model call** — cheaper, and it cannot misinterpret anything. |
| **silent when healthy** | A monitor that says nothing on success and speaks only when action is needed, so its output stays believable. |
| **preflight** | A read-only check run before work starts, so a job fails early rather than half-way. |
| **dead-man check** | An *independent* monitor that alerts when the system stops reporting — it must not depend on the system it watches. |
| **kanban / task ledger** | A durable record of work items, owners, and status, used instead of relying on chat memory. |
| **subagent / delegation** | A separate, bounded agent session given part of a larger task. |
| **broker** | A small service that accepts a narrow, structured request, checks it against policy, and performs it — instead of handing another component broad credentials. |
| **typed handoff** | A request with predefined machine-checkable fields, rather than free-form text one side has to interpret. |
| **multiplexing** | Serving several profiles from one gateway process instead of one process each. Fewer services, shared failure domain. |
| **ingress** | How requests get in: private chat, command line, a public endpoint. **Public ingress** means untrusted people can start a request. |

## Checking that it works

| Term | Meaning here |
|---|---|
| **guard** | A deterministic pass/fail check of a rule ("this tool must be absent"). Cheap, runs often, cannot judge behaviour. |
| **eval** | A repeatable test of *model behaviour* on representative work. Costs a real model call; needed for anything a guard cannot express. |
| **smoke test** | One small real exercise proving an important path works right now. |
| **negative test** | A deliberate attempt at a forbidden action, to prove it is actually blocked rather than merely discouraged. |
| **fixture** | Deliberately broken or controlled input, used to prove a check can fail. A check never seen failing is not yet a check. |
| **restore drill** | Actually restoring from backup and confirming the result is usable. |
| **drift** | A mismatch between source, what is installed, and what a running process has loaded. |

## Optional services

| Term | Meaning here |
|---|---|
| **loopback** | An address reachable only from the same machine (`127.0.0.1`). The default for every support service here. |
| **local inference** | Running a model on your own hardware instead of a hosted API. An outage floor, not automatically cheaper or faster. |
| **extraction** | Fetching a page and converting it to text an agent can use. Always treat the result as untrusted input. |
| **SearXNG / Firecrawl / Crawl4AI / Ollama** | Optional self-hosted pieces: metasearch; two page-extraction options; local model runtime. |

## Easy to confuse

- **Profile vs OS user vs VM.** A profile separates an assistant's *state*. An OS user separates *filesystem authority*. A VM separates *the machine*. Only the last two are isolation.
- **Skill vs plugin.** A skill is instructions the model reads. A plugin is code that runs.
- **Model vs provider.** The model is what answers; the provider is the account and endpoint it answers through. The same model may be available from several providers at different prices.
- **Backup vs sync.** Sync faithfully copies a deletion. Backup keeps a previous version you can restore.
- **Guard vs eval.** A guard asks "is the configuration right now?". An eval asks "does it behave correctly when asked?".
- **Scheduled job vs no-agent script.** Both run on a timer; only one spends a model call and can misread its instructions.
