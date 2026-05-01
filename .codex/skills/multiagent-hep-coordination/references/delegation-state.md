# Delegation and State

Use this reference when writing coordinator state, handoffs, or session records.

## Delegation

- Delegate critical analysis stages to workers.
- Delegate critical stage review to separate reviewers.
- Keep environment setup, file preparation, and dependency checks local unless they materially affect claim scope.
- Assign a stable `agent_tag` before spawning any worker or reviewer.
- Include only role, agent_tag, stage, exact task, required input files, required output paths, and acceptance criteria in subagent briefs.

## Required Files

- `analysis_state.json`
- `codex_sessions.json`
- `agent_timeline.jsonl`
- `handoff/<stage>/local_brief.txt`
- `handoff/<stage>/worker_brief.txt`
- `handoff/<stage>/reviewer_brief.txt`
- `reviews/<stage>/review_<cycle>.json`
- `outputs/evaluation_scorecard.json`
- `outputs/test_outcome_summary.json`
- `artifacts/runtime/root_runtime_repair_attempts.json` when relevant

## analysis_state.json

Keep only the active stage detailed; collapse completed stages to short summaries. Include a `claim_policy` block with paths to:

- reference spec
- data provenance
- feasibility matrix
- claim classification
- report-number trace
- finalization gate
- scorecard
- test outcome summary
- root runtime repair attempts when relevant
- final artifact review
- final claim review

Also record booleans for real observed data, unblinding, paper-level permission, diagnostic permission, and handoff.

## codex_sessions.json

The coordinator is the canonical writer. Record coordinator, worker, and reviewer agent tags, roles, stages, status, brief paths, output paths, and rollout path candidates when available. Do not paste rollout contents into prompts or reports.
