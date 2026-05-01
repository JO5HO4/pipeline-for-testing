# Reporting and Handoff Pipeline

Pattern: Pipeline

Derived from:
- `SKILL_PLOTTING_AND_REPORT`
- `SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK`
- `SKILL_ENFORCEMENT_PRE_HANDOFF_GATE`
- `SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF`

## Stage ordering

| Stage | Inputs | Producing skills | Gate | Exit criteria |
|---|---|---|---|---|
| Plot and report assembly | reviewed physics artifacts | `report_package_generator.md`, `report_packaging_wrapper.md` | `blinding_and_visualization_reviewer.md` | report draft, plot manifest, and captions exist |
| Discrepancy audit | report draft, plots, yields | `data_mc_discrepancy_reviewer.md` | same reviewer | discrepancy audit exists even for zero-issue runs |
| Handoff enforcement | report package, enforcement artifacts, `outputs/evaluation_scorecard.json` | `reproducibility_and_handoff_reviewer.md`, `../../../../hep-analysis-evaluation-scorecard/SKILL.md` | same reviewer | evaluation scorecard exists and enforcement handoff gate is `ok` |
| Failure extraction | reviewer findings and run logs | `failure_to_skill_inversion.md` | `reproducibility_and_handoff_reviewer.md` | handoff package includes remediation or candidate skill notes |

## Gates

- no final handoff without an explicit discrepancy artifact
- no final handoff without `outputs/evaluation_scorecard.json`
- no final handoff without an explicit enforcement gate result

## Dependencies

- `../shared/evidence_requirements.md`
- `../shared/pipeline_logging_contract.md`

## Escalation paths

- escalate if the report would have to omit a central blocker to appear complete
- escalate if a missing artifact would force the reviewer to infer handoff readiness

## Logging requirements

- log report paths, plot manifest paths, scorecard path, discrepancy verdicts, and final handoff status
- attach candidate-skill notes when repeated failures were observed

## Verification Gate

### ASSERTIONS

1. The `Plot and report assembly` stage produced the report draft, plot manifest, and caption evidence before the pipeline advanced to discrepancy review.
2. The `Discrepancy audit` stage produced an explicit discrepancy artifact even for a zero-issue run, and the `Handoff enforcement` stage recorded `outputs/evaluation_scorecard.json` plus an enforcement handoff gate result of `ok` before handoff.
3. The `Failure extraction` stage added remediation notes or explicit candidate-skill notes to the handoff package before the pipeline marked handoff complete, and each completed stage was backed by a `pass` or `conditional_pass` reviewer outcome.

### REPAIR

- Soft failure: rerun the blocked reporting stage in place to regenerate the missing report, discrepancy, enforcement, or failure-extraction artifact, then rerun this gate.
- Hard failure: return to the earliest blocked stage in the `## Stage ordering` table of `reporting_and_handoff_pipeline.md`; if the handoff package would need to hide a blocker to appear complete, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: reporting_and_handoff_pipeline
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

- `hep_analysis_meta_pipeline.md`
- `../reviewers/reproducibility_and_handoff_reviewer.md`
