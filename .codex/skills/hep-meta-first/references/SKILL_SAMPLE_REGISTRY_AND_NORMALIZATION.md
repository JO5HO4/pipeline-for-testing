---
skill_id: SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
display_name: "Sample Registry and Normalization"
version: 1.0
category: normalization

summary: "Each sample must be mapped to a physics process and classified as data, signal, or background with an explicit normalization convention."

invocation_keywords:
  - "sample registry and normalization"
  - "io"
  - "sample"
  - "registry"
  - "normalization"

when_to_use:
  - "Use when executing or validating the io stage of the analysis workflow."
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
  - name: sample_registry_artifact_containing_sample_identity_process_mapp
    type: artifact
    description: "sample-registry artifact containing sample identity, process mapping, classification, and normalization inputs"
  - name: process_role_mapping_artifact_declaring_per_analysis_target_whic
    type: artifact
    description: "process-role mapping artifact declaring, per analysis target, which processes are treated as signal vs background"
  - name: nominal_vs_alternative_sample_mapping_artifact_per_physics_proce
    type: artifact
    description: "nominal-vs-alternative sample mapping artifact per physics process"
  - name: mc_sample_disambiguation_artifact_when_multiple_candidate_datase
    type: artifact
    description: "MC sample disambiguation artifact when multiple candidate datasets exist for the same central physics process"
  - name: normalization_expression_artifact_describing_how_per_event_weigh
    type: artifact
    description: "normalization-expression artifact describing how per-event weights are formed"
  - name: normalization_audit_artifact_listing_missing_inputs_and_warnings
    type: artifact
    description: "normalization-audit artifact listing missing inputs and warnings"

preconditions:
  - "Dependency SKILL_READ_SUMMARY_AND_VALIDATE has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_READ_SUMMARY_AND_VALIDATE

  may_follow:
    - SKILL_READ_SUMMARY_AND_VALIDATE
    - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION
    - SKILL_MC_NORMALIZATION_METADATA_STACKING
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
  - "writes sample_registry_artifact_containing_sample_identity_process_mapp"
  - "writes process_role_mapping_artifact_declaring_per_analysis_target_whic"
  - "writes nominal_vs_alternative_sample_mapping_artifact_per_physics_proce"
  - "writes mc_sample_disambiguation_artifact_when_multiple_candidate_datase"
  - "writes normalization_expression_artifact_describing_how_per_event_weigh"
  - "writes normalization_audit_artifact_listing_missing_inputs_and_warnings"

failure_modes:
  - "process-role assignment is unambiguous for the active analysis objective"

validation_checks:
  - "every registered sample has exactly one classification among data, signal, background"
  - "each sample contains process identity and source-file linkage"
  - "process-role assignment is unambiguous for the active analysis objective"
  - "normalization terms are present or explicitly marked as not specified"
  - "normalization value is computable when all required terms are available"
  - "default central-yield registry rows for MC have `lumi_fb = 36.1`"
  - "central-yield workflows include only nominal/reference samples per physics process; alternatives are flagged as non-central"
  - "if multiple candidate datasets exist for one central process, one nominal/reference choice is recorded and any unresolved ambiguity blocks execution"

handoff_to:
  - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION
  - SKILL_EVENT_IO_AND_COLUMNAR_MODEL
  - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
  - SKILL_MC_NORMALIZATION_METADATA_STACKING
  - SKILL_OBJECT_DEFINITIONS
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/sample_registry_and_normalization.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `core_pipeline/sample_registry_and_normalization.md`
- Original stage: `io`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Sample Registry and Normalization

## Layer 1 — Physics Policy
Each sample must be mapped to a physics process and classified as data, signal, or background with an explicit normalization convention.

Policy requirements:
- preserve process identity and sample provenance
- distinguish data from simulated samples
- support analysis-context-dependent process roles (the same physics process may be signal in one analysis and background in another)
- apply a consistent MC normalization based on cross section, correction factors, luminosity, and generator-weight sum
- for this ATLAS Open Data Run-2 H->gammagamma workflow, use `lumi_fb = 36.1` for central MC normalization unless an explicit analysis-level override is requested and documented
- record missing normalization inputs explicitly rather than silently assuming values
- when multiple MC samples exist for one physics process (for example alternate generators/modeling), define one nominal/reference sample set for central yields and mark alternative samples for systematic variations only
- for decay-specific analyses, central signal samples must match the target decay/final state; inclusive or other-decay Higgs samples require explicit exclusion or non-central labeling
- when dataset-name semantics are insufficient to determine a unique nominal sample set, invoke the MC sample disambiguation skill and block on unresolved ambiguity

Normalization convention for simulated samples:
`w_norm = (xsec_pb * k_factor * filter_eff * lumi_fb * 1000.0) / sumw`

## Layer 2 — Workflow Contract
### Required Artifacts
- sample-registry artifact containing sample identity, process mapping, classification, and normalization inputs
- process-role mapping artifact declaring, per analysis target, which processes are treated as signal vs background
- nominal-vs-alternative sample mapping artifact per physics process
- MC sample disambiguation artifact when multiple candidate datasets exist for the same central physics process
- normalization-expression artifact describing how per-event weights are formed
- normalization-audit artifact listing missing inputs and warnings

### Acceptance Checks
- every registered sample has exactly one classification among data, signal, background
- each sample contains process identity and source-file linkage
- process-role assignment is unambiguous for the active analysis objective
- normalization terms are present or explicitly marked as not specified
- normalization value is computable when all required terms are available
- default central-yield registry rows for MC have `lumi_fb = 36.1`
- central-yield workflows include only nominal/reference samples per physics process; alternatives are flagged as non-central
- if multiple candidate datasets exist for one central process, one nominal/reference choice is recorded and any unresolved ambiguity blocks execution

## Layer 3 — Example Implementation
### Registry Fields (Current Repository)
For each sample:
- `sample_id`
- `process_name`
- `kind`: `data | signal | background`
- `analysis_role` (recommended): `signal_nominal | background_nominal | signal_alternative | background_alternative`
- `is_nominal` (recommended boolean)
- `nominal_process_key` (recommended stable physics-process key)
- `files`
- `xsec_pb`
- `k_factor`
- `filter_eff`
- `sumw`
- `lumi_fb`
- `weight_expr`

### CLI (Current Repository)
`python -m analysis.samples.registry --inputs inputs/ --summary analysis/analysis.summary.json --out outputs/samples.registry.json --target-lumi-fb 36.1`

### Downstream Reference
After this skill, run:
- `governance/mc_sample_disambiguation_and_nominal_selection.md` to resolve unique nominal/reference MC sample sets before central yields and fits
- `physics_facts/mc_normalization_metadata_stacking.md` for metadata.csv-driven normalization of multi-sample MC stacks in ATLAS Open Data workflows
- `analysis_strategy/signal_background_strategy_and_cr_constraints.md`

# Examples

Example invocation context:
- `python -m analysis.samples.registry --inputs inputs/ --summary analysis/analysis.summary.json --out outputs/samples.registry.json --target-lumi-fb 36.1`

Example expected outputs:
- `outputs/samples.registry.json`
