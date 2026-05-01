# Reproducibility and Handoff Reviewer

Pattern: Reviewer

Derived from:
- `SKILL_FULL_STATISTICS_EXECUTION_POLICY`
- `SKILL_SKILL_REFRESH_AND_CHECKPOINTING`
- `SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY`
- `SKILL_ENFORCEMENT_PRE_HANDOFF_GATE`
- `SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF`

## Review scope

Verify that the run used the approved statistics scope, produced reproducibility evidence, passed mandatory checkpoint gates, and is genuinely ready for handoff.

## Required evidence

- run manifest
- smoke or reproducibility artifacts
- skill refresh or checkpoint logs
- enforcement handoff gate
- `outputs/evaluation_scorecard.json`
- final report package
- skill extraction summary

## Criteria

- `pass`: handoff is supported by full evidence and all mandatory gates pass
- `conditional_pass`: non-blocking follow-up items remain but central claims are intact
- `block`: any mandatory gate artifact is missing or failing
- `fail`: the run claims central results without full-statistics or without required enforcement evidence

## Common failure modes

- partial-statistics run presented as final
- missing or contradictory evaluation scorecard
- checkpoint artifacts missing at stage boundaries
- enforcement handoff gate absent or failing
- no skill extraction summary after a completed run

## Required remediation guidance

- rerun the blocked stage through the central pipeline or the smallest matching wrapper
- use `../inversions/failure_to_skill_inversion.md` to classify recurring failure modes
- escalate to a human if central-result scope cannot be recovered without changing the approved run contract

## Verification Gate

### ASSERTIONS

1. A reviewer verdict artifact or conversation note for `Reproducibility and Handoff Reviewer` exists and records exactly one verdict from `pass`, `conditional_pass`, `block`, or `fail`.
2. The required evidence is present on disk or in the conversation: the run manifest, smoke or reproducibility artifacts, skill refresh or checkpoint logs, `outputs/evaluation_scorecard.json`, the enforcement handoff gate, the final report package, and the skill extraction summary.
3. The evidence explicitly confirms that the evaluation scorecard and enforcement handoff gate are passing and that no partial-statistics run is being presented as a final central result.

### REPAIR

- Soft failure: rerun the blocked reporting or reproducibility stage to regenerate the missing handoff evidence, then rerun this reviewer gate.
- Hard failure: return to the `Handoff enforcement` or `Failure extraction` stage of `reporting_and_handoff_pipeline.md`, or return to Stage 10 of `hep_analysis_meta_pipeline.md`; if central-result scope cannot be recovered from the approved run contract, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: reproducibility_and_handoff_reviewer
assertions_checked:
  - assertion_1
  - assertion_2
  - assertion_3
assertion_results:
  assertion_1: pass|fail
  assertion_2: pass|fail
  assertion_3: pass|fail
violations_found: <integer>
repair_applied: true|false  # with one-line description if true
gate_outcome: PASS | CONDITIONAL_PASS | BLOCKED | ESCALATED
next_skill: <skill filename or "human">
```

The agent must not proceed if `gate_outcome` is `BLOCKED` or `ESCALATED`.

## Related skills

- `../pipelines/reporting_and_handoff_pipeline.md`
- `../shared/pipeline_logging_contract.md`
