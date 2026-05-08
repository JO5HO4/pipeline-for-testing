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
- pipeline skill compliance audit covering report-visible claims
- prompt-MC versus reducible-MC-proxy split and reducible-background role audit when the analysis has same-sign, trilepton, fake/nonprompt-lepton, or charge-misID-sensitive regions
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
4. In same-sign or multilepton reports, distinguish `prompt_mc_background`, `data_driven_reducible_background` if available, and `reducible_mc_proxy_diagnostic`; do not call a raw reducible-MC stack the expected background.
5. State expected versus observed significance explicitly, using accepted Asimov fields for expected claims.
6. Append assumptions, deviations, unresolved issues, and reviewer-linked evidence.
7. Check every headline number and physics-result table against the pipeline skill compliance audit before writing central language.

## Output contract

- the report distinguishes data and MC sample descriptions
- the report cites only central claims that passed reviewer gates
- blocked central claims stay blocked in the narrative
- same-sign or multilepton yield plots that include raw reducible MC proxies are labeled diagnostic or show the prompt/reducible split
- raw diagnostic `q0`/`Z` values from blocked or diagnostic-only Asimov fits appear only in a diagnostics/audit section, never as the expected-significance headline or physics-result value
- any result marked `diagnostic_only`, `blocked`, or `noncompliant_blocking` by the pipeline skill compliance audit is not phrased as a central claim

## Constraints

- do not hide data-MC discrepancies
- do not label raw reducible `ttbar`, inclusive `W+jets`, inclusive `Z+jets`, or multijet/photon MC as central expected background in same-sign or multilepton regions without a reviewed data-driven, hybrid, or closure-backed method
- do not cite plot paths without embedding the plots
- do not mix observed and expected significance language
- do not present `q0`/`z_discovery` as central expected significance when `claim_status` is blocked or `accepted_z_discovery` is null
- do not publish a final report until `pipeline_skill_compliance_auditor.md` has passed or conditionally passed the report-visible claim set

## Verification Gate

### ASSERTIONS

1. The `report markdown`, `final report in reports/`, `plot manifest and artifact inventory`, `report-ready sample selection summary`, and `report appendix inputs for assumptions, deviations, and unresolved issues` all exist before handoff.
2. The `report markdown` distinguishes data and MC sample descriptions, cites only central claims that passed reviewer gates, and keeps blocked claims explicitly blocked in the narrative.
3. Every plot cited in the report is embedded with a caption adjacent to the image, and expected versus observed significance language is kept separate rather than conflated.
4. For H to gammagamma expected significance, the reported physics value comes from `accepted_z_discovery`; if `claim_status` is blocked or `accepted_z_discovery` is null, the report says the expected-significance claim is blocked and may list raw diagnostic values only with the block reason.
5. A report-scope pipeline skill compliance audit exists and no report-visible central result is marked `diagnostic_only` or `noncompliant_blocking`.
6. For same-sign, trilepton, fake/nonprompt-lepton, or charge-misID-sensitive regions, the report labels any raw reducible MC stack as diagnostic or explicitly shows the prompt/reducible split; central expected-background language is used only for reviewed prompt MC plus approved data-driven or hybrid reducible estimates.

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
  - assertion_4
  - assertion_5
  - assertion_6
assertion_results:
  assertion_1: pass|fail
  assertion_2: pass|fail
  assertion_3: pass|fail
  assertion_4: pass|fail
  assertion_5: pass|fail
  assertion_6: pass|fail
violations_found: <integer>
repair_applied: true|false  # with one-line description if true
gate_outcome: PASS | CONDITIONAL_PASS | BLOCKED | ESCALATED
next_skill: <skill filename or "human">
```

The agent must not proceed if `gate_outcome` is `BLOCKED` or `ESCALATED`.

## Related skills

- `../tool_wrappers/report_packaging_wrapper.md`
- `../reviewers/pipeline_skill_compliance_auditor.md`
- `../reviewers/blinding_and_visualization_reviewer.md`
- `../reviewers/data_mc_discrepancy_reviewer.md`
- `../pipelines/reporting_and_handoff_pipeline.md`
