# Analysis Summary Reviewer

Pattern: Reviewer

Derived from:
- `SKILL_READ_SUMMARY_AND_VALIDATE`
- `SKILL_JSON_SPEC_DRIVEN_EXECUTION`

## Review scope

Verify that the normalized analysis summary, partition semantics, and execution contract are internally consistent and precise enough for downstream sample, selection, and fit stages.

## Required evidence

- `outputs/summary.normalized.json`
- validation diagnostics and overlap policy artifacts
- execution contract and deviations log
- partition spec when categories or regions are already materialized

## Criteria

- `pass`: all cross references resolve and the runtime contract matches the summary
- `conditional_pass`: non-blocking cosmetic or naming issues are logged
- `block`: unresolved region, fit, observable, or overlap references remain
- `fail`: the summary is internally contradictory or the runtime contract silently dropped required scope

## Common failure modes

- fit regions or reported results reference missing region IDs
- overlap policy missing for SR and CR pairs used together
- runtime overrides not recorded
- category or observable names drift between summary and generated artifacts

## Required remediation guidance

- use `../tool_wrappers/summary_loader_wrapper.md` to regenerate normalized artifacts
- use `../generators/analysis_spec_generator.md` for summary contract repair
- use `../generators/event_model_and_partition_generator.md` when the summary is valid but partitions are incomplete

## Verification Gate

### ASSERTIONS

1. A reviewer verdict artifact or conversation note for `Analysis Summary Reviewer` exists and records exactly one verdict from `pass`, `conditional_pass`, `block`, or `fail`.
2. The required evidence is present on disk or in the conversation: `outputs/summary.normalized.json`, validation diagnostics and overlap policy artifacts, the execution contract, the deviations log, and the partition spec whenever categories or regions have already been materialized.
3. The evidence explicitly confirms that summary cross references resolve and that runtime overrides were logged rather than silently dropped from the execution contract.

### REPAIR

- Soft failure: rerun `summary_loader_wrapper.md` or `analysis_spec_generator.md` to repair the normalized summary, execution contract, or deviations log, then rerun this reviewer gate.
- Hard failure: return to Stage 3 of `spec_to_runtime_pipeline.md` when the normalized summary or diagnostics are incomplete, or return to Stage 4 of `spec_to_runtime_pipeline.md` when only execution-contract drift remains; escalate to a human if valid summary content cannot be recovered without inventing physics scope.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: analysis_summary_reviewer
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

- `../pipelines/spec_to_runtime_pipeline.md`
- `../shared/hep_domain_guardrails.md`
