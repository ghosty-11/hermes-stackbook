# Suggested scheduled jobs

Schedules are optional operating aids, not a reason to make the stack autonomous. Add a job only when it has an owner, an observable outcome, a bounded failure mode, and a destination someone reads.

Use the installed `hermes cron --help` and subcommand help before creating anything. Hermes changes faster than this guide, and exact command flags are intentionally not duplicated here.

## Choose the narrowest execution mode

1. **No-agent script:** deterministic checks, backup, cleanup, counts, checksums, and file movement.
2. **Script then model:** deterministic code collects and bounds evidence; a model interprets only the ambiguous part.
3. **Agent job:** search, synthesis, drafting, or judgment that cannot be expressed as a small workflow.

Healthy no-agent jobs should produce no output. Agent jobs should use Hermes' supported silence sentinel. Deliver findings to an explicit platform and channel; never rely on a bare platform default.

Two deliberate exceptions to silent-when-healthy, each still requiring an owner, a named
consumer, and an observable failure path:

- **Consumer-facing heartbeat/content jobs** (a daily briefing, a standing status post):
  their output *is* the product, and their **silence is the alert** — pair them with a
  check that notices a missed delivery.
- **Bounded collector-to-reviewer handoffs**: a quarantined collector may deliver to a
  local/internal destination that a privileged reviewer consumes across a trust boundary,
  instead of to a human channel. The destination is still explicit; "local" is a handoff,
  never a place for alerts.

## Starter schedule

These are examples, not universal defaults. Set an explicit timezone, offset neighboring jobs, and avoid known production or backup windows.

| Example job | Mode | Example cadence | Speaks when | Required proof |
|---|---|---|---|---|
| Gateway dead-man | External no-agent monitor | Every 5 minutes | Gateway is unreachable across a retry window | Monitor still alerts while Hermes is stopped; recovery clears it. |
| Failed or stale cron check | No-agent script | Every 15 minutes, offset from the hour | A job failed, is blocked, or missed its expected interval | Synthetic failed and overdue fixtures are detected; paused jobs are ignored. |
| Disk and memory pressure | No-agent script | Hourly at `:07` | A sustained threshold or growth-rate limit is crossed | A controlled threshold breach produces the expected alert. |
| Encrypted backup | No-agent script | Daily during a quiet window | Snapshot, retention, or repository access fails | Expected inputs appear in the snapshot and one file restores with matching content. |
| Backup staleness dead-man | External no-agent monitor | Daily after the backup window | No recent independently verified snapshot exists | An intentionally old timestamp is detected. |
| Knowledge link/freshness check | No-agent script | Daily at `:23` | Links, required metadata, or review dates fail policy | Planted broken link and stale date fail; clean fixture is silent. |
| Knowledge inbox digest | Script then model | Weekly | Bounded proposals or contradictions require review | Collector output is size-bounded and the model cites source paths. |
| Dependency/security advisory review | Script then model | Weekly on a different day | A relevant new advisory or incompatible release exists | A known fixture advisory reaches the intended destination once. |
| Stack improvement review | Deterministic collectors, then a read-only reviewer | Weekly on an offset day | Guard/eval regressions repeat or a useful upstream change justifies operator review | A planted finding produces one evidence-backed proposal at an explicit operator destination; clean state is silent, and the reviewer cannot apply it. |
| Provider/model canary | No-agent script or tiny bounded call | Daily or before an unattended model job | The smallest real completion fails or resolves to an unexpected provider/model | The check calls the endpoint; a catalog or configured model name alone does not pass. |
| Free-offer watch | Script then model | Weekly | A new or materially changed primary-source offer is found | The endpoint or program is re-checked before reporting it as usable. |
| Restore drill reminder | No-agent reminder; operator executes | Monthly | The drill is due or overdue | A completed drill records snapshot ID, restored object, comparison, and cleanup. |
| Optional public-bot retention cleanup | No-agent script | Daily if that optional feature is enabled | Cleanup fails or data exceeds policy | Expired test data is removed without touching active/private state. |

A schedule is not a lock. Any two jobs that can write the same repository, database, backup, or deployment state need an actual lock or single-writer queue.

## Job record

Keep one private record per job:

```text
Name and stable ID:
Owner:
Consumer:
Mode: no-agent | script-then-model | agent
Schedule and timezone:
Delivery destination:
Healthy/silent behavior:
Inputs and trust class:
Credentials and authority:
Work directory:
Lock or single-writer policy:
Model/provider pin, if any:
Call/token/spend ceiling:
Timeout and retry limit:
Preflight:
Success evidence:
Failure-path fixture:
Last real run:
Last delivery proof:
Disable/rollback command:
```

Do not store credential values in this record.

## Agent-job prompt contract

A scheduled model prompt should name:

- one outcome and one consumer;
- exact existing input paths or URLs;
- the deterministic sibling check that owns counts, dates, and status;
- an explicit source and output size limit;
- what requires a human;
- the supported silence response;
- the true schedule and timezone;
- the skills actually attached to the job;
- prohibited mutations and the allowed write boundary, if any.

Do not ask a model to calculate what code can decide reliably. Do not allow a review job to apply its own findings.

## Verification before enabling

1. Inventory paused and active jobs; do not assume the default listing includes both.
2. Run the preflight as the actual service identity and environment.
3. Prove the check's failure path with a safe fixture.
4. Trigger the job once and read the complete execution output.
5. Run a healthy/no-change case and confirm silence.
6. Confirm the explicit destination receives an actionable finding.
7. Confirm timeout or cancellation releases locks and child processes.
8. Confirm the job cannot create more scheduled jobs or obtain interactive approval while unattended.
9. Record the job, owner, last success, and expected next fire in the private operations inventory.

A manual run proves execution content, not necessarily the scheduler's natural delivery path. Keep an external staleness check until at least one scheduled fire has landed.
