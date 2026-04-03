---
skill_id: SKILL_SELECTION_ENGINE_AND_REGIONS
display_name: "Selection Engine and Regions"
version: 1.0
category: selections

summary: "Analysis regions must be defined as explicit, executable selection logic with clear semantic roles."

invocation_keywords:
  - "selection engine and regions"
  - "selection"
  - "engine"
  - "regions"

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
  - name: region_definition_artifact_with_executable_selection_expressions
    type: artifact
    description: "region-definition artifact with executable selection expressions"
  - name: per_sample_region_mask_yield_artifact
    type: artifact
    description: "per-sample region mask/yield artifact (weighted and unweighted)"
  - name: region_consistency_artifact_verifying_references_used_by_fit_con
    type: artifact
    description: "region-consistency artifact verifying references used by fit configurations"
  - name: sr_cr_overlap_matrix_artifact_with_pass_fail_status
    type: artifact
    description: "SR/CR overlap-matrix artifact (pairwise overlap counts/fractions) with pass/fail status"

preconditions:
  - "Dependency SKILL_OBJECT_DEFINITIONS has completed successfully."
  - "Dependency SKILL_CATEGORY_CHANNEL_REGION_PARTITIONING has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_SELECTION_ENGINE_AND_REGIONS are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_OBJECT_DEFINITIONS
    - SKILL_CATEGORY_CHANNEL_REGION_PARTITIONING

  may_follow:
    - SKILL_OBJECT_DEFINITIONS
    - SKILL_CATEGORY_CHANNEL_REGION_PARTITIONING
    - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS

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
  - "writes region_definition_artifact_with_executable_selection_expressions"
  - "writes per_sample_region_mask_yield_artifact"
  - "writes region_consistency_artifact_verifying_references_used_by_fit_con"
  - "writes sr_cr_overlap_matrix_artifact_with_pass_fail_status"

failure_modes:
  - "SR/CR overlap checks fail fast when non-zero overlap is found for pairs without explicit `allow_overlap=true` override"
  - "failures identify which region expression is missing or invalid"

validation_checks:
  - "each referenced region exists and has executable logic"
  - "region yields are produced for each processed sample"
  - "fit-configuration region references resolve successfully"
  - "SR/CR overlap checks fail fast when non-zero overlap is found for pairs without explicit `allow_overlap=true` override"
  - "failures identify which region expression is missing or invalid"

handoff_to:
  - SKILL_CUT_FLOW_AND_YIELDS
  - SKILL_HISTOGRAMMING_AND_TEMPLATES
  - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/selection_engine_and_regions.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `core_pipeline/selection_engine_and_regions.md`
- Original stage: `selection`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Selection Engine and Regions

## Layer 1 — Physics Policy
Analysis regions must be defined as explicit, executable selection logic with clear semantic roles.

Policy requirements:
- each region has an identifier and role: signal, control, or validation
- region selections must be machine-executable and scientifically interpretable
- control and signal assignments must be consistent with the statistical strategy
- signal and control regions used together in a fit must be mutually exclusive at event level unless explicitly overridden with justification
- unresolved prose-only selections are insufficient for production execution

## Layer 2 — Workflow Contract
### Required Artifacts
- region-definition artifact with executable selection expressions
- per-sample region mask/yield artifact (weighted and unweighted)
- region-consistency artifact verifying references used by fit configurations
- SR/CR overlap-matrix artifact (pairwise overlap counts/fractions) with pass/fail status

### Acceptance Checks
- each referenced region exists and has executable logic
- region yields are produced for each processed sample
- fit-configuration region references resolve successfully
- SR/CR overlap checks fail fast when non-zero overlap is found for pairs without explicit `allow_overlap=true` override
- failures identify which region expression is missing or invalid

## Layer 3 — Example Implementation
### Region Model (Current Repository)
Each region contains:
- `region_id`
- `kind`: `signal | control | validation`
- `selection`
- optional `cutflow_steps`

### CLI (Current Repository)
`python -m analysis.selections.regions --sample <ID> --registry outputs/samples.registry.json --regions analysis/regions.yaml --out outputs/regions/<ID>.regions.json`

### Coordination Note
Control-vs-signal assignments are consumed by:
- `analysis_strategy/signal_background_strategy_and_cr_constraints.md`

# Examples

Example invocation context:
- `python -m analysis.selections.regions --sample <ID> --registry outputs/samples.registry.json --regions analysis/regions.yaml --out outputs/regions/<ID>.regions.json`

Example expected outputs:
- `outputs/samples.registry.json`
- `outputs/regions/<ID>.regions.json`
