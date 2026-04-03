---
skill_id: SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
display_name: "Signal/Background Strategy and CR Constraints"
version: 1.0
category: stats

summary: "Signal and background modeling choices must be explicitly classified and linked to control-to-signal normalization assumptions."

invocation_keywords:
  - "signal background strategy and cr constraints"
  - "signal/background strategy and cr constraints"
  - "design"
  - "signal"
  - "background"
  - "strategy"
  - "constraints"

when_to_use:
  - "Use when executing or validating the design stage of the analysis workflow."
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
  - name: sample_classification_artifact_listing_data_signal_background_sa
    type: artifact
    description: "sample-classification artifact listing data/signal/background sample memberships"
  - name: analysis_target_declaration_artifact_describing_which_process_ar
    type: artifact
    description: "analysis-target declaration artifact describing which process(es) are the signal hypothesis for this run"
  - name: background_modeling_strategy_artifact_describing_per_process_mod
    type: artifact
    description: "background-modeling-strategy artifact describing per-process modeling mode and normalization source"
  - name: control_to_signal_constraint_map_artifact_defining_constrained_b
    type: artifact
    description: "control-to-signal constraint-map artifact defining constrained backgrounds, source/control regions, target/signal regions, and correlation intent"
  - name: cr_sr_overlap_policy_artifact_for_each_constrained_mapping
    type: artifact
    description: "CR/SR overlap-policy artifact for each constrained mapping"
  - name: outputs_background_modeling_strategy_json
    type: artifact
    description: "`outputs/background_modeling_strategy.json`"
  - name: outputs_samples_classification_json
    type: artifact
    description: "`outputs/samples.classification.json`"
  - name: outputs_cr_sr_constraint_map_json
    type: artifact
    description: "`outputs/cr_sr_constraint_map.json`"

preconditions:
  - "Dependency SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION has completed successfully."
  - "Dependency SKILL_SELECTION_ENGINE_AND_REGIONS has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
    - SKILL_SELECTION_ENGINE_AND_REGIONS

  may_follow:
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
    - SKILL_SELECTION_ENGINE_AND_REGIONS
    - SKILL_SYSTEMATICS_AND_NUISANCES
    - SKILL_WORKSPACE_AND_FIT_PYHF
    - SKILL_PLOTTING_AND_REPORT

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
  - "writes sample_classification_artifact_listing_data_signal_background_sa"
  - "writes analysis_target_declaration_artifact_describing_which_process_ar"
  - "writes background_modeling_strategy_artifact_describing_per_process_mod"
  - "writes control_to_signal_constraint_map_artifact_defining_constrained_b"
  - "writes cr_sr_overlap_policy_artifact_for_each_constrained_mapping"
  - "writes outputs_background_modeling_strategy_json"
  - "writes outputs_samples_classification_json"
  - "writes outputs_cr_sr_constraint_map_json"

failure_modes:
  - "Missing or ambiguous required inputs block execution."
  - "Schema, fit, or consistency checks fail and produce diagnostics."

validation_checks:
  - "every sample is classified exactly once"
  - "process-role choices are consistent with the declared analysis target and are documented when deviating from an inclusive treatment"
  - "each background process has explicit modeling strategy metadata"
  - "each constrained background has explicit control-to-signal mapping metadata"
  - "each constrained CR->SR mapping declares overlap policy and passes overlap checks unless an explicit exception is recorded"
  - "downstream statistical modeling can consume these artifacts without ambiguity"

handoff_to:
  - SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION
  - SKILL_SYSTEMATICS_AND_NUISANCES
  - SKILL_WORKSPACE_AND_FIT_PYHF
  - SKILL_PLOTTING_AND_REPORT
  - SKILL_SELECTION_ENGINE_AND_REGIONS
---

# Purpose

This skill defines a structured execution contract for `analysis_strategy/signal_background_strategy_and_cr_constraints.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `analysis_strategy/signal_background_strategy_and_cr_constraints.md`
- Original stage: `design`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Signal/Background Strategy and CR Constraints

## Layer 1 — Physics Policy
Signal and background modeling choices must be explicitly classified and linked to control-to-signal normalization assumptions.

Policy requirements:
- classify all samples as data, signal, or background
- treat signal/background assignment as analysis-target dependent (for example inclusive Higgs analyses vs process-targeted analyses such as ttH)
- define whether each background is modeled by simulation templates or data-driven methods
- declare whether control-region constraints transfer to signal regions for each constrained background
- require constrained CR->SR mappings to be disjoint at event level by default; any overlap must be explicit and justified
- preserve compatibility with analyses where background shape is analytic and simulation is used mainly for functional-form studies

## Layer 2 — Workflow Contract
### Required Artifacts
- sample-classification artifact listing data/signal/background sample memberships
- analysis-target declaration artifact describing which process(es) are the signal hypothesis for this run
- background-modeling-strategy artifact describing per-process modeling mode and normalization source
- control-to-signal constraint-map artifact defining constrained backgrounds, source/control regions, target/signal regions, and correlation intent
- CR/SR overlap-policy artifact for each constrained mapping

### Acceptance Checks
- every sample is classified exactly once
- process-role choices are consistent with the declared analysis target and are documented when deviating from an inclusive treatment
- each background process has explicit modeling strategy metadata
- each constrained background has explicit control-to-signal mapping metadata
- each constrained CR->SR mapping declares overlap policy and passes overlap checks unless an explicit exception is recorded
- downstream statistical modeling can consume these artifacts without ambiguity

## Layer 3 — Example Implementation
### Expected Outputs (Current Repository)
- `outputs/background_modeling_strategy.json`
- `outputs/samples.classification.json`
- `outputs/cr_sr_constraint_map.json`

### CLI (Current Repository)
`python -m analysis.samples.strategy --registry outputs/samples.registry.json --regions analysis/regions.yaml --summary outputs/summary.normalized.json --out outputs/background_modeling_strategy.json`

### Downstream Reference
Use before:
- `core_pipeline/systematics_and_nuisances.md`
- `core_pipeline/workspace_and_fit_pyhf.md`

Summarize in:
- `core_pipeline/plotting_and_report.md`

# Examples

Example invocation context:
- `python -m analysis.samples.strategy --registry outputs/samples.registry.json --regions analysis/regions.yaml --summary outputs/summary.normalized.json --out outputs/background_modeling_strategy.json`

Example expected outputs:
- `outputs/background_modeling_strategy.json`
- `outputs/samples.classification.json`
- `outputs/cr_sr_constraint_map.json`
- `outputs/samples.registry.json`
- `outputs/summary.normalized.json`
