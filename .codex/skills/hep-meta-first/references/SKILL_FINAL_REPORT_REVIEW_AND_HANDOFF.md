---
skill_id: SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF
display_name: "Final Report Review and Handoff"
version: 1.0
category: reporting

summary: "After analysis execution and report generation, perform a structured review to detect anomalies, assess completion status, and prepare a handoff record for human or agent continuation, including fail-closed checks for required H->gammagamma fit-plot families."

invocation_keywords:
  - "final report review and handoff"
  - "reporting"
  - "final"
  - "report"
  - "review"
  - "handoff"

when_to_use:
  - "Use when executing or validating the reporting stage of the analysis workflow."
  - "Use when this context is available: final analysis report."
  - "Use when this context is available: cut-flow and yield tables/artifacts."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: final_analysis_report
      type: artifact
      description: "final analysis report"
    - name: cut_flow_and_yield_tables_artifacts
      type: artifact
      description: "cut-flow and yield tables/artifacts"
    - name: generated_plots
      type: artifact
      description: "generated plots"
    - name: fit_significance_artifacts
      type: artifact
      description: "fit/significance artifacts"
    - name: run_configuration_files
      type: artifact
      description: "run configuration files"
    - name: workflow_execution_logs_manifests
      type: artifact
      description: "workflow execution logs/manifests"
    - name: outputs_report_mc_sample_selection_json
      type: artifact
      description: "`outputs/report/mc_sample_selection.json`"
    - name: outputs_report_skill_extraction_summary_json
      type: artifact
      description: "`outputs/report/skill_extraction_summary.json`"
    - name: outputs_report_enforcement_handoff_gate_json
      type: artifact
      description: "`outputs/report/enforcement_handoff_gate.json`"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: overall_run_status
    type: artifact
    description: "overall run status"
  - name: detected_anomalies
    type: artifact
    description: "detected anomalies"
  - name: issues_requiring_human_attention
    type: artifact
    description: "issues requiring human attention"
  - name: handoff_readiness_statement
    type: artifact
    description: "handoff-readiness statement (sufficient/insufficient for continuation)"
  - name: skill_extraction_gate_result_and_any_blocking_gaps
    type: artifact
    description: "skill-extraction gate result and any blocking gaps"
  - name: data_mc_discrepancy_gate_result_and_any_blocking_gaps
    type: artifact
    description: "data-MC discrepancy gate result and any blocking gaps"
  - name: skill_refresh_checkpoint_gate_result_and_any_blocking_gaps
    type: artifact
    description: "skill-refresh/checkpoint gate result and any blocking gaps"

preconditions:
  - "Dependency SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW has completed successfully."
  - "Dependency SKILL_EXTRACT_NEW_SKILL_FROM_FAILURE has completed successfully."
  - "Dependency SKILL_SKILL_REFRESH_AND_CHECKPOINTING has completed successfully."
  - "Dependency SKILL_ENFORCEMENT_PRE_HANDOFF_GATE has completed successfully with `outputs/report/enforcement_handoff_gate.json` status `ok`."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
    - SKILL_EXTRACT_NEW_SKILL_FROM_FAILURE
    - SKILL_SKILL_REFRESH_AND_CHECKPOINTING
    - SKILL_ENFORCEMENT_PRE_HANDOFF_GATE

  may_follow:
    - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
    - SKILL_EXTRACT_NEW_SKILL_FROM_FAILURE
    - SKILL_SKILL_REFRESH_AND_CHECKPOINTING
    - SKILL_ENFORCEMENT_PRE_HANDOFF_GATE
    - SKILL_PLOTTING_AND_REPORT
    - SKILL_VISUAL_VERIFICATION
    - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION
    - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE

allowed_tools:
  - Read
  - Write
  - Edit
  - Bash

allowed_paths:
  - analysis/
  - input-data/
  - outputs*/
  - reports/
  - skills/
  - newskills/

side_effects:
  - "writes overall_run_status"
  - "writes detected_anomalies"
  - "writes issues_requiring_human_attention"
  - "writes handoff_readiness_statement"
  - "writes skill_extraction_gate_result_and_any_blocking_gaps"
  - "writes data_mc_discrepancy_gate_result_and_any_blocking_gaps"
  - "writes skill_refresh_checkpoint_gate_result_and_any_blocking_gaps"

failure_modes:
  - "stage status is recorded as pass, blocked, or failed with diagnostics"

validation_checks:
  - "required artifacts exist and satisfy schema/consistency expectations"
  - "stage status is recorded as pass, blocked, or failed with diagnostics"
  - "for H->gammagamma, the review verifies that the default diphoton nominal sample was used for the background template and that low-statistics auxiliary samples were not silently combined into the nominal template"
  - "for H->gammagamma, the review verifies correct sideband normalization, effective-MC-luminosity calculation, smoothing-threshold logic, blinding behavior, full-range Asimov generation, fixed signal-shape policy, and required statistical-input plots"
  - "for H->gammagamma, the review verifies the mandatory fit-plot families: blinded sideband-fit provenance plots, expected-significance Asimov fit plots, and explicitly unblinded observed-data full-range fit plots when unblinding was requested"
  - "for H->gammagamma, the review verifies that the spurious-signal background-function scan respects the degree/complexity cap of `3`, and that any failure persisting at the cap is reported explicitly as a capped noncompliant outcome"
  - "`outputs/report/enforcement_handoff_gate.json` exists and has status `ok` before handoff is marked ready"

handoff_to:
  - SKILL_PLOTTING_AND_REPORT
  - SKILL_VISUAL_VERIFICATION
  - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION
  - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/final_report_review_and_handoff.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. Completeness check:
2. confirm required sections are present:
3. introduction/task summary
4. dataset description
5. object definitions and selections
6. signal/control regions
7. cut flow tables
8. distribution plots
9. statistical interpretation
10. summary
11. confirm sample descriptions include:
12. separate data and Monte Carlo descriptions

# Notes

- Source file: `core_pipeline/final_report_review_and_handoff.md`
- Original stage: `reporting`
- Logic type classification: `reporting`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Final Report Review and Handoff

## Layer 1 — Physics Policy
After analysis execution and report generation, perform a structured review to detect anomalies, assess completion status, and prepare a handoff record for human or agent continuation.

Policy requirements:
- run this review immediately after report generation for each production run
- treat the final report as both:
  - a human-readable result narrative
  - a technical state record for continuation
- flag suspicious values and inconsistencies instead of silently accepting them
- separate hard failures from warnings
- ensure continuation-critical metadata and artifact paths are explicitly documented
- preserve blinding policy when reviewing statistical/plot outputs
- enforce post-run skill extraction as a completion gate; missing extraction summary is a handoff blocker
- enforce data-MC discrepancy artifact completion as a gate; missing discrepancy artifacts are handoff blockers
- enforce skill-refresh/checkpoint completion as a gate; missing or failing checkpoint status is a handoff blocker
- for `H -> gamma gamma`, the review must explicitly verify:
  - the default diphoton nominal sample was used for the background template
  - low-statistics auxiliary background samples were not silently combined into the nominal template
  - sideband normalization was applied correctly
  - effective MC luminosity was computed
  - smoothing logic followed the `10 x 36 fb^-1` threshold rule
  - the spurious-signal background-function scan respected the degree/complexity cap of `3`
  - any failure persisting at the cap was labeled explicitly as a capped noncompliant outcome rather than a compliant pass
  - blinded analyses did not inspect observed data in `120-130 GeV`
  - blinded expected significance still used full-range Asimov generation over `105-160 GeV`
  - signal shape parameters were fixed in significance fits
  - required statistical-input plots were produced

## Layer 2 — Workflow Contract
### Inputs
- final analysis report
- cut-flow and yield tables/artifacts
- generated plots
- fit/significance artifacts
- run configuration files
- workflow execution logs/manifests
- `outputs/report/mc_sample_selection.json`
- `outputs/report/skill_extraction_summary.json`
- `outputs/report/data_mc_discrepancy_audit.json`
- `outputs/report/data_mc_check_log.json`
- `outputs/report/skill_refresh_plan.json`
- `outputs/report/skill_refresh_log.jsonl`
- `outputs/report/skill_checkpoint_status.json`

### Review Steps
1. Completeness check:
   - confirm required sections are present:
     - introduction/task summary
     - dataset description
     - object definitions and selections
     - signal/control regions
     - cut flow tables
     - distribution plots
     - statistical interpretation
     - summary
   - confirm sample descriptions include:
     - separate data and Monte Carlo descriptions
     - MC generator and simulation configuration
     - MC process modeling and signal/background role
   - when multiple candidate MC samples existed, confirm the report contains a dedicated appendix describing the nominal/reference sample selection rationale
   - flag missing sections
2. Narrative-scope check:
   - verify event-selection narrative discusses only regions entering the log-likelihood fit
   - verify each fit region has its fit observable documented
3. Numerical sanity checks:
   - detect suspicious patterns:
     - zero yields where events are expected
   - unusually large yields
   - placeholders (`0`, `NaN`, dummy constants)
   - fit parameters at boundaries
   - zero/unrealistic uncertainties
   - significance values inconsistent with yields/model
  - for `H -> gamma gamma`, verify that reported effective MC luminosity and smoothing decision are numerically consistent with the documented threshold rule
  - for `H -> gamma gamma`, verify that the spurious-signal scan did not escalate beyond degree/complexity `3` once the target criterion remained unsatisfied and that the capped outcome is documented consistently
4. Plot validation:
   - detect issues:
     - empty histograms
     - missing distributions
     - axis-range mismatch
     - missing expected data points
     - stack mismatch vs totals
   - verify fit-state normalization semantics:
     - pre-fit plots use nominal MC prediction
     - post-fit plots use fitted normalization values
   - verify blinding semantics:
     - blinded mode hides sensitive SR data by omission or masking
     - unblinded mode shows observed data across full SR
   - for `H -> gamma gamma`, verify the blinded sideband-fit provenance plots:
     - show observed data points only in `105-120 GeV` and `130-160 GeV`
     - show the background-only PDF fitted in the sidebands and evaluated across `105-160 GeV`
     - show stacked expected signal across the blinded window for context
   - for `H -> gamma gamma`, verify the expected-significance Asimov fit plots:
     - show signal-plus-background Asimov pseudo-data over the full `105-160 GeV` range
     - show the fitted free-`mu` signal-plus-background total
     - show the corresponding background-only component
   - for `H -> gamma gamma`, verify the observed-data full-range fit plots only in explicit unblinded mode:
     - show observed data across `105-160 GeV`
     - show the fitted free-`mu` signal-plus-background total
     - show the fitted background-only component
   - for `H -> gamma gamma`, verify the mandatory statistical-input plots:
     - one signal `m_gg` + fitted-signal-PDF plot per category
     - nominal unsmoothed sideband-normalized diphoton template plot
     - selected spurious-signal fit plot
     - unsmoothed-vs-smoothed sideband-normalized template overlay when smoothing was applied
     - any separate smoothed-template-vs-fit view is treated as supplemental and does not satisfy the mandatory smoothing-effect diagnostic by itself
5. Consistency checks:
   - verify:
     - table yields align with histogram integrals/fit summaries
     - categories referenced in text exist in plots/artifacts
     - regions used in text match fit configuration
   - for `H -> gamma gamma`, verify that the report and machine-readable artifacts agree on:
     - nominal background sample choice
     - sideband ranges `105-120 GeV` and `130-160 GeV`
     - blind window `120-130 GeV`
     - expected-vs-observed significance labeling
     - fixed-vs-floating fit parameter policy
     - degree/complexity cap of `3` for the spurious-signal scan
     - whether the selected background function passed or remained noncompliant at the cap
6. Workflow outcome assessment:
   - classify run status:
     - completed successfully
     - completed with warnings
     - partially completed
     - major failure
7. Handoff preparation:
   - confirm report/handoff includes:
     - datasets used
     - MC sample-selection rationale artifact and appendix location
     - normalization method/luminosity
     - region/category definitions
     - key configuration parameters
     - systematics model scope
     - statistical model and backend
     - exact output artifact locations
   - flag missing continuation-critical information
8. Skill-extraction completion gate:
   - verify `outputs/report/skill_extraction_summary.json` exists and is readable
   - verify summary `status` is either `none_found` or `candidates_created`
   - if `candidates_created`, verify listed `candidate_skills/*` files exist
   - if this gate fails, classify run status as `partially completed` or `major failure` (not handoff-ready)
9. Data-MC discrepancy completion gate:
   - verify `outputs/report/data_mc_discrepancy_audit.json` exists and is readable
   - verify discrepancy-audit `status` is one of:
     - `no_substantial_discrepancy`
     - `discrepancy_investigated_bug_found`
     - `discrepancy_investigated_no_bug_found`
   - verify `outputs/report/data_mc_check_log.json` exists and is readable
   - if this gate fails, classify run status as `partially completed` or `major failure` (not handoff-ready)
10. Skill-refresh/checkpoint completion gate:
   - verify `outputs/report/skill_refresh_plan.json` exists and is readable
   - verify `outputs/report/skill_refresh_log.jsonl` exists and is readable
   - verify `outputs/report/skill_checkpoint_status.json` exists and is readable
   - verify checkpoint status is `pass`
   - if this gate fails, classify run status as `partially completed` or `major failure` (not handoff-ready)

### Required Output
Produce a structured review summary containing:
- overall run status
- detected anomalies
- issues requiring human attention
- handoff-readiness statement (sufficient/insufficient for continuation)
- skill-extraction gate result and any blocking gaps
- data-MC discrepancy gate result and any blocking gaps
- skill-refresh/checkpoint gate result and any blocking gaps
- H->gammagamma policy-gate results covering:
  - background-template sample choice
  - background-function DOF/complexity-cap compliance
  - sideband normalization
  - effective MC luminosity and smoothing
  - blinding/window handling
  - full-range Asimov generation
  - fixed signal-shape policy
  - required statistical-input plots

## Layer 3 — Example Implementation
### Recommended Output Artifact
- `outputs/report/final_report_review.json` containing:
  - `status`
  - `anomalies` (list)
  - `consistency_issues` (list)
  - `missing_sections` (list)
  - `handoff_ready` (bool)
  - `handoff_gaps` (list)
  - `checked_artifacts` (paths)
  - `skill_extraction_checked` (bool)
  - `skill_extraction_status` (`none_found`, `candidates_created`, or `missing`)
  - `data_mc_discrepancy_checked` (bool)
  - `data_mc_discrepancy_status` (`no_substantial_discrepancy`, `discrepancy_investigated_bug_found`, `discrepancy_investigated_no_bug_found`, or `missing`)
  - `skill_refresh_checked` (bool)
  - `skill_refresh_status` (`pass` or `missing_or_failed`)

### Minimum Human Summary
- one concise run-status paragraph
- bulleted anomaly list (or explicit "none found")
- handoff readiness confirmation with any blocking gaps

### Related Skills
- `core_pipeline/plotting_and_report.md`
- `infrastructure/visual_verification.md`
- `core_pipeline/final_analysis_report_agent_workflow.md`
- `governance/mc_sample_disambiguation_and_nominal_selection.md`
- `core_pipeline/profile_likelihood_significance.md`
- `governance/skill_refresh_and_checkpointing.md`

# Examples

Example invocation context:
- Run this contract in the declared stage using the required inputs and dependencies.

Example expected outputs:
- `outputs/report/mc_sample_selection.json`
- `outputs/report/skill_extraction_summary.json`
- `outputs/report/data_mc_discrepancy_audit.json`
- `outputs/report/data_mc_check_log.json`
- `outputs/report/skill_refresh_plan.json`
- `outputs/report/skill_refresh_log.jsonl`
- `outputs/report/skill_checkpoint_status.json`
- `outputs/report/final_report_review.json`
