---
skill_id: SKILL_HISTOGRAMMING_AND_TEMPLATES
display_name: "Histogramming and Templates"
version: 1.0
category: histograms

summary: "Histogram templates must encode fit observables with consistent binning and statistical information."

invocation_keywords:
  - "histogramming and templates"
  - "histogramming"
  - "templates"

when_to_use:
  - "Use when executing or validating the histogramming stage of the analysis workflow."
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
  - name: per_region_per_observable_per_sample_histogram_template_artifact
    type: artifact
    description: "per-region, per-observable, per-sample histogram-template artifact containing edges, counts, and uncertainty terms"
  - name: histogram_metadata_artifact_with_observable_name_region_sample_a
    type: artifact
    description: "histogram-metadata artifact with observable name, region, sample, and binning provenance"
  - name: binning_decision_artifact_when_default_binning_is_used
    type: artifact
    description: "binning-decision artifact when default binning is used"

preconditions:
  - "Dependency SKILL_SELECTION_ENGINE_AND_REGIONS has completed successfully."
  - "Dependency SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_HISTOGRAMMING_AND_TEMPLATES are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_SELECTION_ENGINE_AND_REGIONS
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION

  may_follow:
    - SKILL_SELECTION_ENGINE_AND_REGIONS
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
    - SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION

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
  - "writes per_region_per_observable_per_sample_histogram_template_artifact"
  - "writes histogram_metadata_artifact_with_observable_name_region_sample_a"
  - "writes binning_decision_artifact_when_default_binning_is_used"

failure_modes:
  - "Missing or ambiguous required inputs block execution."
  - "Schema, fit, or consistency checks fail and produce diagnostics."

validation_checks:
  - "templates exist for every sample that enters each fit region"
  - "histogram binning is consistent within each fit observable definition"
  - "template integrals are consistent with region yields within tolerance"
  - "metadata identifies region, sample, and observable for every template"

handoff_to:
  - SKILL_FREEZE_ANALYSIS_HISTOGRAM_PRODUCTS
  - SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION
  - SKILL_SYSTEMATICS_AND_NUISANCES
  - SKILL_HISTOGRAM_PLOTTING_INVARIANTS
  - SKILL_PLOTTING_AND_REPORT
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/histogramming_and_templates.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `core_pipeline/histogramming_and_templates.md`
- Original stage: `histogramming`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Histogramming and Templates

## Layer 1 — Physics Policy
Histogram templates must encode fit observables with consistent binning and statistical information.

Policy requirements:
- observables and binning should follow the analysis definition
- if binning is unspecified, choose a deterministic default and document it
- each histogram must include statistical uncertainty information (for example sum of squared weights)
- template integrals should reproduce selected yields within tolerance

## Layer 2 — Workflow Contract
### Required Artifacts
- per-region, per-observable, per-sample histogram-template artifact containing edges, counts, and uncertainty terms
- histogram-metadata artifact with observable name, region, sample, and binning provenance
- binning-decision artifact when default binning is used

### Acceptance Checks
- templates exist for every sample that enters each fit region
- histogram binning is consistent within each fit observable definition
- template integrals are consistent with region yields within tolerance
- metadata identifies region, sample, and observable for every template

## Layer 3 — Example Implementation
### Portable Format (Current Repository)
`.npz` files with:
- bin edges
- counts
- sumw2
- metadata (region, sample, observable)

Suggested layout:
`outputs/hists/<region_id>/<observable>/<sample_id>.npz`

### CLI (Current Repository)
`python -m analysis.hists.histmaker --sample <ID> --registry outputs/samples.registry.json --regions analysis/regions.yaml --summary outputs/summary.normalized.json --out outputs/hists/`

### Downstream Reference
If analytic mass fits are used, run:
- `analysis_strategy/signal_shape_and_spurious_signal_model_selection.md`

# Examples

Example invocation context:
- `python -m analysis.hists.histmaker --sample <ID> --registry outputs/samples.registry.json --regions analysis/regions.yaml --summary outputs/summary.normalized.json --out outputs/hists/`

Example expected outputs:
- `outputs/hists/<region_id>/<observable>/<sample_id>.npz`
- `outputs/samples.registry.json`
- `outputs/summary.normalized.json`
- `outputs/hists/`
