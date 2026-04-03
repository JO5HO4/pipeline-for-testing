---
skill_id: SKILL_SYSTEMATICS_AND_NUISANCES
display_name: "Systematics and Nuisances"
version: 1.0
category: systematics

summary: "Systematic uncertainties must be represented as nuisance parameters with explicit scope and correlation assumptions."

invocation_keywords:
  - "systematics and nuisances"
  - "systematics"
  - "nuisances"

when_to_use:
  - "Use when executing or validating the systematics stage of the analysis workflow."
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
  - name: nuisance_model_artifact_listing_nuisance_names_types_affected_co
    type: artifact
    description: "nuisance-model artifact listing nuisance names, types, affected components, and correlations"
  - name: optional_shape_variation_artifact_set_for_up_down_template_varia
    type: artifact
    description: "optional shape-variation artifact set for up/down template variations"
  - name: uncertainty_provenance_artifact_documenting_assumptions_and_miss
    type: artifact
    description: "uncertainty-provenance artifact documenting assumptions and missing inputs"
  - name: nominal_vs_variation_sample_mapping_artifact_for_each_process_en
    type: artifact
    description: "nominal-vs-variation sample mapping artifact for each process entering systematics"

preconditions:
  - "Dependency SKILL_HISTOGRAMMING_AND_TEMPLATES has completed successfully."
  - "Dependency SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS has completed successfully."
  - "Dependency SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_SYSTEMATICS_AND_NUISANCES are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_HISTOGRAMMING_AND_TEMPLATES
    - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
    - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION

  may_follow:
    - SKILL_HISTOGRAMMING_AND_TEMPLATES
    - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
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
  - "writes nuisance_model_artifact_listing_nuisance_names_types_affected_co"
  - "writes optional_shape_variation_artifact_set_for_up_down_template_varia"
  - "writes uncertainty_provenance_artifact_documenting_assumptions_and_miss"
  - "writes nominal_vs_variation_sample_mapping_artifact_for_each_process_en"

failure_modes:
  - "Missing or ambiguous required inputs block execution."
  - "Schema, fit, or consistency checks fail and produce diagnostics."

validation_checks:
  - "every nuisance has declared type and affected scope"
  - "correlations across regions/processes are explicitly stated or defaulted with metadata"
  - "statistical model can be constructed using the nuisance artifact"
  - "stat-only fallback is explicitly flagged when applied"
  - "central yields used for fits/cut flows do not double count alternate generator/modeling samples"
  - "variation samples are linked to a nominal process and used only through nuisance variations"

handoff_to:
  - SKILL_WORKSPACE_AND_FIT_PYHF
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/systematics_and_nuisances.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `core_pipeline/systematics_and_nuisances.md`
- Original stage: `systematics`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Systematics and Nuisances

## Layer 1 — Physics Policy
Systematic uncertainties must be represented as nuisance parameters with explicit scope and correlation assumptions.

Policy requirements:
- support at least normalization and statistical uncertainties
- include shape uncertainties when variation templates are available
- define which samples and regions are affected by each nuisance
- encode CR/SR correlation assumptions for constrained backgrounds
- if only statistical uncertainties are available, record that limitation explicitly
- when multiple MC samples model one physics process, treat non-nominal samples as variation inputs for systematics rather than additional central-yield contributions

## Layer 2 — Workflow Contract
### Required Artifacts
- nuisance-model artifact listing nuisance names, types, affected components, and correlations
- optional shape-variation artifact set for up/down template variations
- uncertainty-provenance artifact documenting assumptions and missing inputs
- nominal-vs-variation sample mapping artifact for each process entering systematics

### Acceptance Checks
- every nuisance has declared type and affected scope
- correlations across regions/processes are explicitly stated or defaulted with metadata
- statistical model can be constructed using the nuisance artifact
- stat-only fallback is explicitly flagged when applied
- central yields used for fits/cut flows do not double count alternate generator/modeling samples
- variation samples are linked to a nominal process and used only through nuisance variations

## Layer 3 — Example Implementation
### Data Model (Current Repository)
`outputs/systematics.json` includes:
- nuisance name
- type: `norm | shape | stat`
- affected samples/regions
- optional correlation group

Additional inputs when available:
- `outputs/background_modeling_strategy.json`
- `outputs/cr_sr_constraint_map.json`
- `outputs/fit/*/spurious_signal.json`

### CLI (Current Repository)
`python -m analysis.stats.pyhf_workspace --summary outputs/summary.normalized.json --hists outputs/hists --systematics outputs/systematics.json --out outputs/fit/workspace.json`

# Examples

Example invocation context:
- `python -m analysis.stats.pyhf_workspace --summary outputs/summary.normalized.json --hists outputs/hists --systematics outputs/systematics.json --out outputs/fit/workspace.json`

Example expected outputs:
- `outputs/systematics.json`
- `outputs/background_modeling_strategy.json`
- `outputs/cr_sr_constraint_map.json`
- `outputs/fit/`
- `outputs/summary.normalized.json`
- `outputs/hists`
- `outputs/fit/workspace.json`
