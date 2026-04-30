# Report Package Generator

Pattern: Generator

Derived from:
- `SKILL_PLOTTING_AND_REPORT`
- `SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW`

## Purpose

Generate the plot-rich, note-style report package that communicates the analysis while preserving traceability to the artifacts and reviewer outcomes that support each claim.

## When to use

- fit, significance, blinding, discrepancy, and normalization artifacts exist
- the workflow is ready to produce a human-readable report and a machine-readable handoff package

## Required inputs

- normalized summary
- sample semantics and normalization artifacts
- cut-flow and yield artifacts
- fit and significance artifacts
- blinding and discrepancy artifacts
- plot manifest inputs

## Outputs

- report markdown
- final report in `reports/`
- plot manifest and artifact inventory
- report-ready sample selection summary
- report appendix inputs for assumptions, deviations, and unresolved issues

## Generation steps

1. Assemble the required sections in a stable order.
2. Embed plots inline and place a caption directly next to each embedded image.
3. Distinguish central nominal samples from alternatives in the narrative.
4. State expected versus observed significance explicitly.
5. Append assumptions, deviations, unresolved issues, and reviewer-linked evidence.

## Output contract

- the report distinguishes data and MC sample descriptions
- the report cites only central claims that passed reviewer gates
- blocked central claims stay blocked in the narrative

## Constraints

- do not hide data-MC discrepancies
- do not cite plot paths without embedding the plots
- do not mix observed and expected significance language

## Verification Gate

### ASSERTIONS

1. The `report markdown`, `final report in reports/`, `plot manifest and artifact inventory`, `report-ready sample selection summary`, and `report appendix inputs for assumptions, deviations, and unresolved issues` all exist before handoff.
2. The `report markdown` distinguishes data and MC sample descriptions, cites only central claims that passed reviewer gates, and keeps blocked claims explicitly blocked in the narrative.
3. Every plot cited in the report is embedded with a caption adjacent to the image, and expected versus observed significance language is kept separate rather than conflated.

### REPAIR

- Soft failure: rerun `report_package_generator.md` to regenerate the report package, missing appendix inputs, or plot inventory and rerun the gate.
- Hard failure: return to Stage 9 of `hep_analysis_meta_pipeline.md` or the `Plot and report assembly` stage of `reporting_and_handoff_pipeline.md`; escalate to `blinding_and_visualization_reviewer.md` or a human if the report would otherwise hide a blocked claim or unresolved discrepancy.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: report_package_generator
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

- `../tool_wrappers/report_packaging_wrapper.md`
- `../reviewers/blinding_and_visualization_reviewer.md`
- `../reviewers/data_mc_discrepancy_reviewer.md`
- `../pipelines/reporting_and_handoff_pipeline.md`
