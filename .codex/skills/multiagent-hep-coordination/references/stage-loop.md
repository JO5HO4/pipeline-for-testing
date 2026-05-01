# Stage Loop

Use this reference when advancing a workflow stage.

## Loop

For every stage, run:

```text
PLAN -> EXECUTE -> AUDIT -> REPAIR -> PROCEED
```

- Default max repair retries per stage: 3.
- A stage is approved only when the required audit has no `PROBLEM`.
- `WARNING` may proceed only as degraded when it does not change claim scope or final physics numbers.
- If retry limit is hit, mark the stage `blocked`, `degraded`, or `needs_revisit`.

## Required Gates

- `RUNTIME_REPAIR`: required when ROOT-backed statistical capability is needed or missing.
- `DATA_PROVENANCE`: classify observed data before observed results.
- `SPEC_FEASIBILITY`: map reference requirements to available, substituted, unavailable, or not applicable.
- `CLAIM_REVIEW`: classify every result as reproduction, reinterpretation, diagnostic_proxy, or blocked.
- `FINALIZE`: decide final status before final reviews.
- `FINAL_ARTIFACT_REVIEW` and `FINAL_CLAIM_REVIEW`: required for final multiagent handoff.

## Repair Rule

If a review finds a root cause in an upstream stage, mark that stage `needs_revisit`, rerun it, then rerun every downstream gate whose output may have changed.
For final-review findings, rerun from `CLAIM_REVIEW` unless the finding names an earlier stage.
