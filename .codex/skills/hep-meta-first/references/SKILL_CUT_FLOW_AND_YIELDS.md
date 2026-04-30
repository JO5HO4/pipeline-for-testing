---
skill_id: SKILL_CUT_FLOW_AND_YIELDS
display_name: "Cut Flow and Yields"
version: 1.0
category: selections

summary: "A cut flow must describe event reduction step-by-step and preserve both unweighted and weighted interpretations."

invocation_keywords:
  - "cut flow and yields"
  - "selection"
  - "flow"
  - "yields"

when_to_use:
  - "Use when executing or validating the selection stage of the analysis workflow."
  - "Use when this context is available: analysis configuration and stage-specific upstream artifacts."
  - "Use when this context is available: repository paths and runtime context for the current run."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: analysis_configuration_and_stage_specific_upstream_artifacts
      type: artifact
      description: "analysis configuration and stage-specific upstream artifacts"
    - name: repository_paths_and_runtime_context_for_the_current_run
      type: artifact
      description: "repository paths and runtime context for the current run"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: cut_flow_table_artifact_per_sample_with_ordered_step_metrics
    type: artifact
    description: "cut-flow table artifact per sample with ordered step metrics"
  - name: region_yield_artifact_per_sample_with_unweighted_counts_weighted
    type: artifact
    description: "region-yield artifact per sample with unweighted counts, weighted yields, and uncertainty proxy terms (for example sum of squared weights)"
  - name: cut_flow_provenance_artifact_linking_steps_to_region_definitions
    type: artifact
    description: "cut-flow provenance artifact linking steps to region definitions"
  - name: process_aggregated_cut_flow_artifact
    type: artifact
    description: "process-aggregated cut-flow artifact (per process + combined signal/background totals)"
  - name: sample_resolved_cut_flow_artifact_unless_explicit_merged_process
    type: artifact
    description: "sample-resolved cut-flow artifact (individual MC samples) unless explicit merged-process configuration is requested"
  - name: nominal_sample_selection_audit_for_cut_flow_central_values
    type: artifact
    description: "nominal-sample selection audit for cut-flow central values"

preconditions:
  - "Dependency SKILL_SELECTION_ENGINE_AND_REGIONS has completed successfully."
  - "Dependency SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION has completed successfully."
  - "Dependency SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_CUT_FLOW_AND_YIELDS are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_SELECTION_ENGINE_AND_REGIONS
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
    - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION

  may_follow:
    - SKILL_SELECTION_ENGINE_AND_REGIONS
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
    - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION

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
  - "writes cut_flow_table_artifact_per_sample_with_ordered_step_metrics"
  - "writes region_yield_artifact_per_sample_with_unweighted_counts_weighted"
  - "writes cut_flow_provenance_artifact_linking_steps_to_region_definitions"
  - "writes process_aggregated_cut_flow_artifact"
  - "writes sample_resolved_cut_flow_artifact_unless_explicit_merged_process"
  - "writes nominal_sample_selection_audit_for_cut_flow_central_values"

failure_modes:
  - "Missing or ambiguous required inputs block execution."
  - "Schema, fit, or consistency checks fail and produce diagnostics."

validation_checks:
  - "cut-flow steps are ordered and complete"
  - "unweighted event counts do not increase across stricter sequential cuts"
  - "final cut-flow selection agrees with region-yield selection used downstream"
  - "weighted yields and uncertainty proxies are finite and reported"
  - "for H->gammagamma reporting, cut flow is reported separately for signal production modes, diphoton background MC, and data"
  - "MC statistical uncertainties are computed from event weights (for example `sqrt(sumw2)`) rather than naive event counts"
  - "process-level sums are consistent with combined signal/background totals within tolerance"
  - "cut-flow output defaults to individual MC sample rows when no explicit merge instruction/configuration is present"
  - "when merged rows are used, a merge map from process rows to MC sample IDs is recorded"
  - "alternative/systematic-only samples do not contribute to central cut-flow totals unless explicitly configured"

handoff_to:
  - SKILL_PLOTTING_AND_REPORT
  - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
  - SKILL_HISTOGRAMMING_AND_TEMPLATES
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/cut_flow_and_yields.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `core_pipeline/cut_flow_and_yields.md`
- Original stage: `selection`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Cut Flow and Yields

## Layer 1 — Physics Policy
A cut flow must describe event reduction step-by-step and preserve both unweighted and weighted interpretations.

Policy requirements:
- cut flow is ordered and physically meaningful
- each step reports unweighted counts and weighted yields
- report per-step and cumulative efficiencies
- final selected yield must match the sample contribution used in downstream histogramming
- for `H -> gamma gamma`, cut flow must be reported separately for:
  - signal production modes
  - diphoton background MC
  - data
- for MC prediction yields, statistical uncertainties must be computed from event weights rather than naive event counts
- for signal and background, provide both:
  - per-process contributions (process-level breakdown)
  - combined totals (all signal processes combined, all background processes combined)
- unless explicitly overridden by user instruction or analysis configuration, cut-flow rows must be reported at individual Monte Carlo sample granularity
- if merged-process reporting is requested, keep a traceable mapping from merged rows back to contributing MC samples
- avoid double counting when multiple samples represent one physics process; only nominal/reference samples contribute to central cut-flow totals

## Layer 2 — Workflow Contract
### Required Artifacts
- cut-flow table artifact per sample with ordered step metrics
- region-yield artifact per sample with unweighted counts, weighted yields, and uncertainty proxy terms (for example sum of squared weights)
- cut-flow provenance artifact linking steps to region definitions
- process-aggregated cut-flow artifact (per process + combined signal/background totals)
- sample-resolved cut-flow artifact (individual MC samples) unless explicit merged-process configuration is requested
- nominal-sample selection audit for cut-flow central values
- for `H -> gamma gamma`, a reporting-ready cut-flow view that explicitly separates:
  - signal production modes
  - diphoton background MC
  - data
  - MC uncertainties computed from event weights (`sumw2` or equivalent)

### Acceptance Checks
- cut-flow steps are ordered and complete
- unweighted event counts do not increase across stricter sequential cuts
- final cut-flow selection agrees with region-yield selection used downstream
- weighted yields and uncertainty proxies are finite and reported
- for `H -> gamma gamma`, cut flow is reported separately for signal production modes, diphoton background MC, and data
- MC statistical uncertainties are computed from event weights (for example `sqrt(sumw2)`) rather than naive counts
- process-level sums are consistent with combined signal/background totals within tolerance
- cut-flow output defaults to individual MC sample rows when no explicit merge instruction/configuration is present
- when merged rows are used, a merge map from process rows to MC sample IDs is recorded
- alternative/systematic-only samples do not contribute to central cut-flow totals unless explicitly configured

## Layer 3 — Example Implementation
### Output Schema (Current Repository)
Cut flow entries:
- `name`, `n_raw`, `n_weighted`, `eff_step`, `eff_cum`

Yield entries:
- `n_raw`, `yield`, `sumw2`

For `H -> gamma gamma` reporting views:
- include separate rows or blocks for signal production modes, diphoton background MC, and data
- derive MC statistical uncertainties from `sumw2`, not from naive `sqrt(n_raw)`

Recommended process-level aggregate entries:
- `process_name`, `role` (`signal` or `background`), `is_nominal`, `yield`
- combined rows: `signal_total`, `background_total`

Recommended sample-level entries (default mode):
- `sample_id`, `sample_label`, `process_name`, `role`, `is_nominal`, `yield`

### CLI (Current Repository)
`python -m analysis.selections.engine --sample <ID> --registry outputs/samples.registry.json --regions analysis/regions.yaml --cutflow --out outputs/cutflows/<ID>.json`

# Examples

Example invocation context:
- `python -m analysis.selections.engine --sample <ID> --registry outputs/samples.registry.json --regions analysis/regions.yaml --cutflow --out outputs/cutflows/<ID>.json`

Example expected outputs:
- `outputs/samples.registry.json`
- `outputs/cutflows/<ID>.json`
