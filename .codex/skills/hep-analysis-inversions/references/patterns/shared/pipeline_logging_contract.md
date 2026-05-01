# Pipeline Logging Contract

Every pipeline stage must leave a compact, machine-readable trail.

## Required log records per stage

- `stage_id`
- `started_at_utc`
- `ended_at_utc`
- `inputs_used`
- `outputs_written`
- `assumptions`
- `deviations`
- `unresolved_issues`
- `reviewers_run`
- `review_outcomes`
- `blocking_reasons`
- `next_skill`

## Required run-level records

- run manifest
- execution contract
- skill refresh or checkpoint log
- artifact inventory
- `outputs/evaluation_scorecard.json`
- final handoff status

## Logging rules

- Log explicit no-op decisions; silence is not evidence.
- Record when a stage was skipped and why.
- If a reviewer blocks, log the smallest remedial scope instead of rerunning the full pipeline blindly.
