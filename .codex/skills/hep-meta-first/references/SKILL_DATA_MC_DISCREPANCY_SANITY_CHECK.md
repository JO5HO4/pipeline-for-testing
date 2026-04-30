---
skill_id: SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK
display_name: "Data-MC Discrepancy Sanity Check"
version: 1.0
category: validation

summary: "Data-MC disagreement is a diagnostic signal. It must be investigated and reported, not cosmetically reduced."

invocation_keywords:
  - "data mc discrepancy sanity check"
  - "data-mc discrepancy sanity check"
  - "validation"
  - "data"
  - "discrepancy"
  - "sanity"
  - "check"

when_to_use:
  - "Use when executing or validating the validation stage of the analysis workflow."
  - "Use when this context is available: data-vs-MC comparison plots and tables (pre-fit/post-fit where applicable)."
  - "Use when this context is available: region/category definitions."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: data_vs_mc_comparison_plots_and_tables
      type: artifact
      description: "data-vs-MC comparison plots and tables (pre-fit/post-fit where applicable)"
    - name: region_category_definitions
      type: artifact
      description: "region/category definitions"
    - name: cut_flow_and_yield_artifacts
      type: artifact
      description: "cut flow and yield artifacts"
    - name: normalization_artifacts
      type: artifact
      description: "normalization artifacts (cross section, k-factor, filter efficiency, luminosity, sum of weights)"
    - name: event_weight_definition_artifact
      type: artifact
      description: "event-weight-definition artifact"
    - name: sample_registry_mapping_artifacts
      type: artifact
      description: "sample registry/mapping artifacts"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: discrepancy_audit_artifact_listing_each_substantial_discrepancy_
    type: artifact
    description: "discrepancy-audit artifact listing each substantial discrepancy and its context:"
  - name: region_category
    type: artifact
    description: "region/category"
  - name: observable
    type: artifact
    description: "observable"
  - name: process_grouping
    type: artifact
    description: "process grouping"
  - name: discrepancy_type
    type: artifact
    description: "discrepancy type (shape, normalization, or both)"
  - name: approximate_magnitude_and_affected_bins_ranges
    type: artifact
    description: "approximate magnitude and affected bins/ranges"
  - name: check_log_artifact_documenting_which_sanity_checks_were_executed
    type: artifact
    description: "check-log artifact documenting which sanity checks were executed and outcomes"
  - name: reporting_note_artifact_that_states_whether_a_concrete_bug_was_f
    type: artifact
    description: "reporting note artifact that states whether a concrete bug was found/corrected or discrepancy remains unresolved"
  - name: explicit_no_substantial_discrepancy_status_path_so_zero_issue_ru
    type: artifact
    description: "explicit \"no substantial discrepancy\" status path so zero-issue runs are still machine-auditable"
  - name: outputs_report_data_mc_discrepancy_audit_json
    type: artifact
    description: "`outputs/report/data_mc_discrepancy_audit.json`"
  - name: outputs_report_data_mc_check_log_json
    type: artifact
    description: "`outputs/report/data_mc_check_log.json`"
  - name: discrepancy_summary_paragraph_in
    type: artifact
    description: "discrepancy summary paragraph in:"
  - name: outputs_report_report_md
    type: artifact
    description: "`outputs/report/report.md`"
  - name: reports_final_analysis_report_md
    type: artifact
    description: "`reports/final_analysis_report.md`"

preconditions:
  - "Dependency SKILL_PLOTTING_AND_REPORT has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_PLOTTING_AND_REPORT

  may_follow:
    - SKILL_PLOTTING_AND_REPORT
    - SKILL_VISUAL_VERIFICATION
    - SKILL_MC_NORMALIZATION_METADATA_STACKING
    - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF

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
  - "writes discrepancy_audit_artifact_listing_each_substantial_discrepancy_"
  - "writes region_category"
  - "writes observable"
  - "writes process_grouping"
  - "writes discrepancy_type"
  - "writes approximate_magnitude_and_affected_bins_ranges"
  - "writes check_log_artifact_documenting_which_sanity_checks_were_executed"
  - "writes reporting_note_artifact_that_states_whether_a_concrete_bug_was_f"
  - "writes explicit_no_substantial_discrepancy_status_path_so_zero_issue_ru"
  - "writes outputs_report_data_mc_discrepancy_audit_json"

failure_modes:
  - "per-sample normalization and duplicate/missing sample handling"

validation_checks:
  - "event-weight application"
  - "luminosity scaling and units"
  - "cross-section, k-factor, filter-efficiency, branching-ratio treatment"
  - "per-sample normalization and duplicate/missing sample handling"
  - "data-MC sample mapping and process grouping"
  - "region/category definitions and overlap logic"
  - "object selections, overlap removal, trigger requirements, trigger scale factors"
  - "blinding logic"
  - "histogram filling logic, variable definition, binning choice"
  - "preselection/cut-flow consistency"
  - "stitching/merging of subsamples"
  - "systematic-variation and pre-fit/post-fit normalization usage"
  - "CR transfer-factor or normalization-factor propagation"
  - "`outputs/report/data_mc_discrepancy_audit.json` exists and is readable for every run"

handoff_to:
  - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
  - SKILL_VISUAL_VERIFICATION
  - SKILL_MC_NORMALIZATION_METADATA_STACKING
  - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF
  - SKILL_FULL_STATISTICS_EXECUTION_POLICY
---

# Purpose

This skill defines a structured execution contract for `governance/data_mc_discrepancy_sanity_check.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `governance/data_mc_discrepancy_sanity_check.md`
- Original stage: `validation`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Data-MC Discrepancy Sanity Check

## Layer 1 — Physics Policy
Data-MC disagreement is a diagnostic signal. It must be investigated and reported, not cosmetically reduced.

Policy requirements:
- explicitly call out substantial data-MC discrepancies in shape and/or normalization
- treat large discrepancies as mandatory triggers for implementation/procedure checks
- never change plotting, normalization, selection, weighting, binning, or sample composition solely to improve visual agreement
- do not treat disagreement alone as proof of implementation failure
- do not suppress, obscure, or de-emphasize discrepant regions/categories in plots or report text
- preserve the distinction between:
  - confirmed implementation bugs (fix + document)
  - unresolved modeling/physics mismatches (retain + report)
- always emit discrepancy-audit artifacts for every production run, including runs with no substantial discrepancy

## Layer 2 — Workflow Contract
### Required Inputs
- data-vs-MC comparison plots and tables (pre-fit/post-fit where applicable)
- region/category definitions
- cut flow and yield artifacts
- normalization artifacts (cross section, k-factor, filter efficiency, luminosity, sum of weights)
- event-weight-definition artifact
- sample registry/mapping artifacts

### Required Artifacts
- discrepancy-audit artifact listing each substantial discrepancy and its context:
  - region/category
  - observable
  - process grouping
  - discrepancy type (shape, normalization, or both)
  - approximate magnitude and affected bins/ranges
- check-log artifact documenting which sanity checks were executed and outcomes
- reporting note artifact that states whether a concrete bug was found/corrected or discrepancy remains unresolved
- explicit "no substantial discrepancy" status path so zero-issue runs are still machine-auditable

### Mandatory Checks When Substantial Discrepancy Is Found
- event-weight application
- luminosity scaling and units
- cross-section, k-factor, filter-efficiency, branching-ratio treatment
- per-sample normalization and duplicate/missing sample handling
- data-MC sample mapping and process grouping
- region/category definitions and overlap logic
- object selections, overlap removal, trigger requirements, trigger scale factors
- blinding logic
- histogram filling logic, variable definition, binning choice
- preselection/cut-flow consistency
- stitching/merging of subsamples
- systematic-variation and pre-fit/post-fit normalization usage
- CR transfer-factor or normalization-factor propagation

### Forbidden Actions
- tuning scale factors or normalization solely to improve agreement
- altering axis limits/binning solely to hide disagreement
- tightening/loosening selections solely to force better agreement
- dropping, merging, or relabeling samples to mask disagreement
- omitting problematic plots from report artifacts
- claiming disagreement is "fixed" without identifying and documenting a concrete implementation error

### Acceptance Checks
- `outputs/report/data_mc_discrepancy_audit.json` exists and is readable for every run
- `outputs/report/data_mc_check_log.json` exists and is readable for every run
- all substantial discrepancies in data-vs-MC plots are explicitly documented
- discrepancy-triggered sanity checks are recorded
- if a bug is found, the fix and impact are documented with updated artifacts
- if no bug is found, discrepancy remains visible in plots and report text
- no change log entry indicates cosmetic-only tuning to improve agreement

## Layer 3 — Example Implementation
### Required Output Artifacts (Current Repository)
- `outputs/report/data_mc_discrepancy_audit.json`
- `outputs/report/data_mc_check_log.json`
- discrepancy summary paragraph in:
  - `outputs/report/report.md`
  - `reports/final_analysis_report.md`

### Suggested `data_mc_discrepancy_audit.json` Fields
- `status` (`no_substantial_discrepancy`, `discrepancy_investigated_bug_found`, `discrepancy_investigated_no_bug_found`)
- `items` (list)
- `checks_performed` (list)
- `bugs_found` (list)
- `unresolved_items` (list)
- `notes`

### Decision Rule
- large discrepancy -> investigate
- confirmed bug -> fix, regenerate affected artifacts, and document
- no confirmed bug -> keep discrepancy visible and report honestly

### Related Skills
- `core_pipeline/plotting_and_report.md`
- `infrastructure/visual_verification.md`
- `physics_facts/mc_normalization_metadata_stacking.md`
- `core_pipeline/final_report_review_and_handoff.md`

# Examples

Example invocation context:
- Run this contract in the declared stage using the required inputs and dependencies.

Example expected outputs:
- `outputs/report/data_mc_discrepancy_audit.json`
- `outputs/report/data_mc_check_log.json`
- `outputs/report/report.md`
