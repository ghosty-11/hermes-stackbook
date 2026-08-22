# Proposed wiki structure

This proposed layout mirrors a working Git-backed Markdown wiki shared by humans and agents.
Keep authored content one folder below the root; `inbox/processed/` is the deliberate exception.

```text
wiki/
├── Home.md                 — Navigational map. Links the current canonical notes by area.
├── README.md               — Entry point. Explains the wiki's scope and where to start.
├── log.md                  — Append-only action log. Records what changed and why it matters.
│
├── agents/                 — Living agent and harness documentation: architecture, profiles,
│                             capability boundaries, evaluation design, and upgrade plans.
├── projects/               — One living note per active project: plans, design, current state,
│                             operating context, and project-specific decisions.
├── services/               — Current service profiles: purpose, ownership, dependencies,
│                             health checks, data boundaries, and recovery pointers.
├── runbooks/               — Executable procedures: triggers, prechecks, ordered actions,
│                             stop conditions, rollback, and independent verification.
├── reviews/                — Dated evidence: audits, postmortems, posture reviews, repository
│                             reviews, and session handoffs that should not become living pages.
├── reference/              — Living atlases and inventories that need periodic re-verification:
│                             schedules, providers, security controls, policies, and stack maps.
├── meta/                   — Wiki governance: conventions, claim-state rules, durable decisions,
│                             parked plans, controlled vocabularies, and writer coordination.
├── templates/              — Approved documentation skeletons and their index. Copy a template
│                             into a live folder; do not treat the skeleton as live state.
│
├── inbox/                  — Unprocessed captures and dated agent reports awaiting distillation.
│   └── processed/          — Original captures after compilation, with a pointer to the
│                             canonical notes that received the durable knowledge.
├── concepts/               — Synthesized topics and methods compiled from multiple sources.
├── raw/                    — Immutable fetched source material. Untrusted input, never authority.
│
├── _archive/               — Superseded notes retained for provenance. Do not delete or garden.
├── _meta/                  — Machine-maintained wiki state such as dashboard data; no authored
│                             knowledge documents belong here.
│
├── .obsidian/              — Optional Obsidian client configuration; tool-owned, not knowledge.
├── .stversions/            — Optional sync-version history; tool-owned, not canonical content.
├── .stfolder/              — Optional sync-folder marker; tool-owned, not canonical content.
└── .git/                   — Version history and collaboration state; tool-owned.
```

The dot-directories are deployment details, not required parts of the content model. Include
or ignore them according to the chosen editor, synchronization tool, backup policy, and public
repository boundary.

## Plan the information lifecycle

A folder tree controls where information lives, not whether it remains useful. Without an
explicit lifecycle, human and automated writers can produce duplicate notes, stale claims,
unreviewed raw material, and sensitive information that is easy to retrieve but unsafe to trust.

Before enabling routine writes, plan:

- a canonical owner and canonical note for each topic, plus one routine writer or a reconciliation
  process for concurrent edits;
- an intake, distillation, review, and archive path, with limits for inbox age and size;
- source and provenance requirements, review dates, and automatic link and freshness checks;
- which sensitive information must be excluded, kept private, encrypted, or separated from
  untrusted captures;
- split, deduplication, retention, and archival rules before volume forces emergency cleanup; and
- versioned backups and periodic restore drills that prove useful knowledge can be recovered.

Treat a growing inbox, overdue reviews, unresolved links, repeated topics, and failed restores as
maintenance signals. Assign an owner and review cadence before they become routine background noise.
