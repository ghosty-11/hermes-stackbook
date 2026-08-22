# Installation

This guide establishes a working Hermes baseline before adding optional components. OMP is a separate, optional software-engineering layer; if you enable it, verify Hermes and OMP independently before connecting them. Do not debug Hermes, OMP, a message gateway, and a custom bridge in one step.

## 1. Prepare the host

Create separate OS identities if an enabled OMP installation and Hermes must not read each other's credentials. The exact user and service-management commands depend on your operating system and are intentionally not wrapped in an unreviewed installer here.

Baseline requirements:

- current Git and `curl`;
- Python and system packages required by Hermes' official installer;
- Bun only if using OMP's recommended package install;
- a service supervisor (systemd or launchd) for an always-on gateway;
- a container runtime only if you will add isolated terminal execution or supporting services.

Before installing, confirm the official requirements:

- [Hermes quickstart](https://hermes-agent.nousresearch.com/docs/)
- [OMP README](https://github.com/can1357/oh-my-pi), if installing OMP

## 2. Install Hermes

Official installer:

```sh
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

Configure the first private profile:

```sh
hermes setup
# or, if you deliberately choose Nous Portal:
hermes setup --portal
```

Inspect the live CLI before continuing:

```sh
hermes --help
hermes doctor
hermes status
hermes config check
```

Start with one model and one provider-diverse fallback. Use the interactive model and fallback commands documented by the installed CLI:

```sh
hermes model
hermes fallback
```

Do not copy provider IDs from this guide; catalogs and aliases change. Run one real private CLI turn and inspect its model/provider result before installing a gateway.

### First Hermes acceptance check

The first profile passes when:

- `hermes doctor` reports no blocking dependency/configuration problem;
- one question returns through the intended primary provider;
- an induced primary failure or explicit test reaches the selected fallback without changing credentials;
- `hermes logs` identifies the session and provider without exposing secrets;
- `hermes backup` can create an export and the archive can be listed/read by the operator.

## 3. Optional: install OMP

Skip this section if Hermes' own coding capabilities meet your needs. Install OMP when you want a dedicated software-engineering harness with integrated repository navigation, structured edits, LSP, debugging, browser automation, resumable sessions, and delegated coding workflows.

Recommended package install:

```sh
bun install -g @oh-my-pi/pi-coding-agent
```

Official script alternative:

```sh
curl -fsSL https://omp.sh/install | sh
```

OMP also documents Homebrew, Nix, native Windows, and other installation methods. For this stack on Windows, use WSL 2; native Windows installation is not tested, recommended, or endorsed by this guide. Pick one owner for upgrades inside the WSL Linux distribution; do not mix package managers.

Inspect and configure:

```sh
omp --help
omp --version
omp config path
omp config list
```

Use OMP's login/model interface to configure only the providers you intend to use. Keep persistent settings under the OMP config directory and project-specific overrides in `<repo>/.omp/config.yml` only when they belong to that repository.

### First OMP acceptance check

Create a disposable Git repository containing one small source file and one test. Ask OMP to make a trivial behavior change, then verify:

- it reads the repository instructions;
- it can edit and run the specific check;
- the requested behavior changes;
- the session can be resumed;
- no unrelated file changes;
- credentials are not printed by config or session output.

### Use the advisor for consequential engineering

For substantial software-engineering work, `/advisor on` is recommended after an advisor
model is configured. The advisor is a passive second-model reviewer: it examines completed
turns and can inject notes, concerns, or blockers that verify assumptions, correct likely
mistakes, and steer the primary agent while work is in progress. This independent review
usually raises result quality, especially across long or load-bearing changes.

The tradeoff is real: the advisor makes additional model calls, so it increases token usage
and cost and may add latency. Leave it off for trivial work or when the token budget matters
more than a second review. Use `/advisor status` to inspect its model, state, token usage, and
cost; use `/advisor off` to stop it for the current session. These commands are
session-scoped unless persistent advisor configuration is enabled separately.

Exercise the non-interactive entry point separately:

```sh
omp -p "Inspect this repository and return its primary language. Do not edit files."
```

For program integration, prefer RPC over parsing terminal prose:

```sh
omp --mode rpc --no-session
```

RPC accepts NDJSON commands and emits structured response/event frames. The Node SDK is a better fit when the caller already runs TypeScript. See [OMP's entry-point documentation](https://github.com/can1357/oh-my-pi#four-entry-points-interactive-one-shot-rpc-and-acp).

## 4. Install the private gateway surface

Configure a single private messaging platform through the current Hermes gateway setup flow:

```sh
hermes gateway setup
hermes gateway install
hermes gateway start
hermes gateway status
```

Use an allowlist or pairing policy. Never set an open own-policy merely to make initial testing easier. Send one message from the authorized operator account and one from an unauthorized test identity; expected result is answer and rejection, respectively.

For WSL 2 or containers, follow the upstream foreground/supervisor guidance rather than assuming `gateway start` owns a working service manager.

## 5. Take the baseline snapshot

Before profiles, custom skills, or plugins:

1. record the install method and exact installed version/revision in a private deployment log;
2. export or back up Hermes state;
3. back up OMP configuration and credential state using a secret-safe mechanism;
4. record the commands that proved the primary model, fallback, private chat, and OMP disposable-repo task;
5. ensure the backups are stored off-host or copied there immediately.

The baseline is the rollback point for every later phase.

## 6. Do not add these yet

Delay all of the following until the baseline passes:

- community plugins or skills;
- an optional public bot;
- multiplexed gateway mode;
- model-driven cron jobs;
- local inference;
- a custom Hermes–OMP bridge;
- automatic knowledge-base writes;
- an agent-authored skill creation loop.

Each adds a separate failure or trust boundary. The [Build sequence](build-sequence.md) introduces them with an exit test.

## Upgrade ownership

Use one update path for each product:

- Hermes: `hermes update --check`, then the current official update process and pre-update backup behavior.
- OMP: the package manager or installer that originally installed it.
- Supporting containers: pinned images or digests, updated deliberately.
- Community plugins: install from a reviewed repository at an immutable full commit when Hermes supports `--ref`.

Never edit bundled Hermes skills/plugins in place. User modifications are preserved, which also means upstream improvements stop replacing that artifact. Add a user plugin/skill alongside stock or maintain an explicit fork.
