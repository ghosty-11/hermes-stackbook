# Profile capability matrix

Copy this file into the private deployment repository. Fill it from resolved runtime state, not intended config.

The example rows reflect the deployed workload documented by this guide. Replace, add, or remove profiles to match your own jobs and trust boundaries; do not create example roles that have no consumer.

## Profile inventory

| Profile | Online | Gateway process/topology | OS identity | Home/state path owner | Inbound surfaces | Authorization policy |
|---|---:|---|---|---|---|---|
| Orchestrator |  |  |  |  |  |  |
| Scribe |  |  |  |  |  |  |
| Research |  |  |  |  |  |  |
| Auditor |  |  |  |  |  |  |
| Engineer |  |  |  |  |  |  |
| Optional public bot |  |  |  |  |  |  |

## Model and memory

| Profile/lane | Primary provider/model | Fallback providers/models | Context exercised | Memory provider/store | Private-data class | Spend limit |
|---|---|---|---|---|---|---|
| Orchestrator |  |  |  |  |  |  |
| Scribe |  |  |  |  |  |  |
| Research |  |  |  |  |  |  |
| Auditor |  |  |  |  |  |  |
| Engineer |  |  |  |  |  |  |
| Optional public bot |  |  |  |  |  |  |
| Vision |  |  |  | n/a |  |  |
| Compression |  |  |  | n/a |  |  |
| Cron default |  |  |  | varies |  |  |
| Local floor |  |  |  | n/a | on-host |  |

## Resolved surface matrix

Make one row per profile and surface. “Expected absent” must be proven by resolved schema or a rejected tool call, not a model statement.

| Profile | Surface | Required tools | Expected absent | Active skills | Active plugins/hooks | Working directory/backend | Evidence command/result |
|---|---|---|---|---|---|---|---|
| Orchestrator | CLI |  |  |  |  |  |  |
| Orchestrator | private chat |  |  |  |  |  |  |
| Scribe | cron/dispatch |  | shell, public ingress |  |  |  |  |
| Research | internal | search, extract | terminal, write, private memory |  |  |  |  |
| Auditor | cron/manual | read/review | write, execute, deploy |  |  |  |  |
| Engineer | dispatch | typed coding delegate | raw web, public ingress |  |  |  |  |
| Optional public bot | public chat | messaging/approved media | shell, files, wiki, cron, board, coding |  |  |  |  |

## Positive and negative scenarios

| Profile | Positive scenario | Observed result | Negative scenario | Observed result | Date |
|---|---|---|---|---|---|
| Orchestrator | Route a real bounded task |  | Unauthorized sender rejected |  |  |
| Scribe | Update canonical sourced note |  | Write outside knowledge tree unavailable |  |  |
| Research | Return bounded cited finding |  | Shell/private URL unavailable |  |  |
| Auditor | Report actionable defect |  | Apply/edit unavailable |  |  |
| Engineer | Submit allowed coding job |  | Unknown repository rejected |  |  |
| Optional public bot | Intended public interaction |  | Private tool/other-user memory unavailable |  |  |

## Change gate

Re-run the matrix after:

- Hermes/OMP update;
- profile config/model change;
- plugin/skill install or update;
- gateway topology change;
- messaging adapter change;
- credential or OS-identity change;
- coding-bridge change;
- memory-provider change.

Any unexplained extra capability blocks deployment.
