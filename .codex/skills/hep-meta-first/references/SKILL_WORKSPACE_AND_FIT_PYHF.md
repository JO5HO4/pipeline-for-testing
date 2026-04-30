---
skill_id: SKILL_WORKSPACE_AND_FIT_PYHF
display_name: "Workspace and Fit (RooFit-Primary for H->gammagamma)"
version: 1.0
category: stats

summary: "Statistical inference must map selected regions, signal/background models, and nuisance parameters into a likelihood model with explicit parameters of interest."

invocation_keywords:
  - "workspace and fit pyhf"
  - "workspace and fit (roofit-primary for h->gammagamma)"
  - "fit"
  - "workspace"
  - "roofit"
  - "primary"
  - "gammagamma"

when_to_use:
  - "Use when executing or validating the fit stage of the analysis workflow."
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
  - name: statistical_workspace_artifact_per_fit_configuration
    type: artifact
    description: "statistical-workspace artifact per fit configuration"
  - name: fit_result_artifact_containing_best_fit_poi_estimates_uncertaint
    type: artifact
    description: "fit-result artifact containing best-fit POI estimates, uncertainties, status, and diagnostics"
  - name: fit_configuration_hash_provenance_artifact_to_ensure_reproducibi
    type: artifact
    description: "fit-configuration hash/provenance artifact to ensure reproducibility of the model setup"
  - name: fit_backend_artifact_declaring_primary_backend_and_configuration
    type: artifact
    description: "fit-backend artifact declaring primary backend (`pyroot_roofit` for H->gammagamma) and configuration provenance"

preconditions:
  - "Dependency SKILL_SYSTEMATICS_AND_NUISANCES has completed successfully."
  - "Dependency SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_WORKSPACE_AND_FIT_PYHF are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_SYSTEMATICS_AND_NUISANCES
    - SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION

  may_follow:
    - SKILL_SYSTEMATICS_AND_NUISANCES
    - SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION
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
  - "writes statistical_workspace_artifact_per_fit_configuration"
  - "writes fit_result_artifact_containing_best_fit_poi_estimates_uncertaint"
  - "writes fit_configuration_hash_provenance_artifact_to_ensure_reproducibi"
  - "writes fit_backend_artifact_declaring_primary_backend_and_configuration"

failure_modes:
  - "H->gammagamma fit stage is marked blocked/failed (not auto-substituted) when RooFit analytic-fit capability is unavailable"

validation_checks:
  - "workspace artifact loads successfully in the chosen inference backend"
  - "fit execution completes with converged status or actionable diagnostics"
  - "POI estimates and uncertainties are present when fit succeeds"
  - "model provenance metadata is attached to fit results"
  - "fit artifact schema remains consistent across backends for downstream significance/reporting stages"
  - "H->gammagamma fit artifacts declare `pyroot_roofit` as the primary backend"
  - "H->gammagamma fit stage is marked blocked/failed (not auto-substituted) when RooFit analytic-fit capability is unavailable"
  - "any non-ROOT H->gammagamma fit result includes explicit `cross_check_only` semantics and is excluded from primary claims"

handoff_to:
  - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
  - SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB
  - SKILL_STATTOOL_OPTIONAL_PYHF_BACKEND
  - SKILL_PLOTTING_AND_REPORT
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/workspace_and_fit_pyhf.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `core_pipeline/workspace_and_fit_pyhf.md`
- Original stage: `fit`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Workspace and Fit (RooFit-Primary for H->gammagamma)

## Layer 1 — Physics Policy
Statistical inference must map selected regions, signal/background models, and nuisance parameters into a likelihood model with explicit parameters of interest.

Policy requirements:
- each fit configuration defines channels, samples, POIs, and nuisance terms
- control-region information may constrain signal-region background normalizations when correlations are defined
- analytic mass-shape choices (when used) must feed the final statistical model consistently
- fit diagnostics and parameter estimates must be preserved for interpretation
- for H->gammagamma resonance workflows, the primary backend must be `pyroot_roofit` with analytic-function modeling; `pyhf` may be used only as an explicitly labeled cross-check
- for H->gammagamma primary results, if RooFit analytic fitting cannot run, the fit stage is blocked (do not substitute `pyhf` as primary)
- for category-resolved resonance fits, support arbitrary category counts from configuration (do not hard-code a fixed number of categories)
- for combined category fits, allow one shared signal-strength parameter (`mu`) correlated across categories while keeping background-shape parameters independent per category

## Layer 2 — Workflow Contract
### Required Artifacts
- statistical-workspace artifact per fit configuration
- fit-result artifact containing best-fit POI estimates, uncertainties, status, and diagnostics
- fit-configuration hash/provenance artifact to ensure reproducibility of the model setup
- fit-backend artifact declaring primary backend (`pyroot_roofit` for H->gammagamma) and configuration provenance

### Acceptance Checks
- workspace artifact loads successfully in the chosen inference backend
- fit execution completes with converged status or actionable diagnostics
- POI estimates and uncertainties are present when fit succeeds
- model provenance metadata is attached to fit results
- fit artifact schema remains consistent across backends for downstream significance/reporting stages
- H->gammagamma fit artifacts declare `pyroot_roofit` as the primary backend
- H->gammagamma fit stage is marked blocked/failed (not auto-substituted) when RooFit analytic-fit capability is unavailable
- any non-ROOT H->gammagamma fit result includes explicit `cross_check_only` semantics and is excluded from primary claims

## Layer 3 — Example Implementation
### Mapping (Current Repository)
A fit configuration maps to:
- channels: included regions
- samples: signal/background/data
- POIs: parameters of interest
- nuisances: from systematics artifact
- CR/SR correlations: from constraint-map artifact when available
- analytic mass-model choice: from signal/background PDF artifacts when available
- backend: primary `pyroot_roofit` for H->gammagamma resonance analytic-function fits; optional `pyhf` cross-check only
- category cardinality: derived from configured `regions_included` or explicit category list override (arbitrary `N`)

### CLI (Current Repository)
`python -m analysis.stats.fit --workspace outputs/fit/workspace.json --fit-id FIT1 --out outputs/fit/FIT1/results.json`

Category-resolved RooFit combined likelihood (arbitrary number of categories):
`python -m analysis.stats.roofit_combined --outputs outputs --registry outputs/samples.registry.json --regions analysis/regions.yaml --fit-id FIT1 --subdir roofit_combined`

### Downstream Reference
After this skill, run:
- `core_pipeline/profile_likelihood_significance.md`

# Examples

Example invocation context:
- `python -m analysis.stats.fit --workspace outputs/fit/workspace.json --fit-id FIT1 --out outputs/fit/FIT1/results.json`
- `python -m analysis.stats.roofit_combined --outputs outputs --registry outputs/samples.registry.json --regions analysis/regions.yaml --fit-id FIT1 --subdir roofit_combined`

Example expected outputs:
- `outputs/fit/workspace.json`
- `outputs/fit/FIT1/results.json`
- `outputs/samples.registry.json`
