# Report Packaging Wrapper

Pattern: Tool Wrapper

Derived from:
- `SKILL_PLOTTING_AND_REPORT`
- `SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW`

## When to use

Use this wrapper when the agent needs repository code to assemble plots, report text, or final package artifacts after the upstream artifacts have already been generated and reviewed.

## Inputs

- normalized summary
- fit and significance artifacts
- registry and normalization artifacts
- discrepancy and blinding artifacts
- output and reports directories

## Outputs

- report artifacts under `outputs/report/`
- rendered final report under `reports/`
- plot manifests and artifact link inventories

## Preconditions

- required statistical and validation artifacts exist
- blinding policy and discrepancy posture are explicit

## Postconditions

- the report package is reviewer-ready
- plot embedding and caption evidence exist

## Call procedure

1. Use the integrated pipeline via `.rootenv/bin/python -m analysis.cli run` when report assembly should stay synchronized with upstream production.
2. Use `analysis.report.make_report.build_report` through a controlled Python entrypoint only when focused report regeneration is required and the inputs are frozen.

## Failure modes

- report text describes artifacts that were not produced
- plots are cited by path only instead of embedded with captions
- expected and observed significance are conflated

## Verification expectations

- report markdown exists
- plot manifests exist
- final reviewers can trace narrative claims to concrete artifacts

## Verification Gate

### ASSERTIONS

1. The wrapper outputs exist before handoff: `report artifacts under outputs/report/`, the `rendered final report under reports/`, and the `plot manifests and artifact link inventories`.
2. The generated report package is reviewer-ready and includes embedded plots with captions rather than path-only references.
3. Narrative claims in the rendered report trace back to reviewed artifacts, and expected versus observed significance remain explicitly distinct.

### REPAIR

- Soft failure: rerun `report_packaging_wrapper.md` or `report_package_generator.md` to regenerate the missing report, manifest, or artifact inventory and rerun this gate.
- Hard failure: return to Stage 9 of `hep_analysis_meta_pipeline.md` or the `Plot and report assembly` stage of `reporting_and_handoff_pipeline.md`; if the report would need to omit a blocker to look complete, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: report_packaging_wrapper
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

- `../generators/report_package_generator.md`
- `../reviewers/blinding_and_visualization_reviewer.md`
- `../pipelines/reporting_and_handoff_pipeline.md`
