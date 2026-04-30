---
skill_id: SKILL_OBJECT_DEFINITIONS
display_name: "Object Definitions"
version: 1.0
category: objects

summary: "Define reconstructed objects first, then construct event-level selections from those objects."

invocation_keywords:
  - "object definitions"
  - "design"
  - "object"
  - "definitions"

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
  - name: object_augmented_event_artifact_containing_selection_masks_multi
    type: artifact
    description: "object-augmented event artifact containing selection masks, multiplicities, and leading/subleading kinematics"
  - name: object_definition_metadata_artifact_documenting_thresholds_and_w
    type: artifact
    description: "object-definition metadata artifact documenting thresholds and working points used"
  - name: object_qa_summary_artifact_with_basic_rates
    type: artifact
    description: "object-QA summary artifact with basic rates (for example average object multiplicity)"

preconditions:
  - "Dependency SKILL_EVENT_IO_AND_COLUMNAR_MODEL has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_OBJECT_DEFINITIONS are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_EVENT_IO_AND_COLUMNAR_MODEL

  may_follow:
    - SKILL_EVENT_IO_AND_COLUMNAR_MODEL

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
  - "writes object_augmented_event_artifact_containing_selection_masks_multi"
  - "writes object_definition_metadata_artifact_documenting_thresholds_and_w"
  - "writes object_qa_summary_artifact_with_basic_rates"

failure_modes:
  - "missing required configuration is flagged with warning or explicit failure"

validation_checks:
  - "object masks and multiplicities are consistent with underlying collections"
  - "leading/subleading quantities are defined only where multiplicity requirements are satisfied"
  - "configured thresholds/working points are traceable in metadata"
  - "missing required configuration is flagged with warning or explicit failure"

handoff_to:
  - SKILL_SELECTION_ENGINE_AND_REGIONS
  - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
---

# Purpose

This skill defines a structured execution contract for `physics_facts/object_definitions.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `physics_facts/object_definitions.md`
- Original stage: `design`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Object Definitions

## Layer 1 — Physics Policy
Define reconstructed objects first, then construct event-level selections from those objects.

Policy requirements:
- object quality and kinematic selections must be explicit and reproducible
- leading/subleading object definitions must be deterministic
- event-level features should be derived from validated object collections
- analysis thresholds and working points should come from configuration, not hardcoded logic

## Layer 2 — Workflow Contract
### Required Artifacts
- object-augmented event artifact containing selection masks, multiplicities, and leading/subleading kinematics
- object-definition metadata artifact documenting thresholds and working points used
- object-QA summary artifact with basic rates (for example average object multiplicity)

### Acceptance Checks
- object masks and multiplicities are consistent with underlying collections
- leading/subleading quantities are defined only where multiplicity requirements are satisfied
- configured thresholds/working points are traceable in metadata
- missing required configuration is flagged with warning or explicit failure

## Layer 3 — Example Implementation
### Pattern (Current Repository)
- `build_photons(events, cfg) -> events` adds derived columns and masks
- analogous builders for jets/leptons as needed

### Configuration Sources (Current Repository)
- `analysis/regions.yaml` (preferred)
- structured summary fields when available

### CLI (Current Repository)
`python -m analysis.objects.photons --sample <ID> --registry outputs/samples.registry.json --regions analysis/regions.yaml --out outputs/cache/<ID>.objects.parquet`

# Examples

Example invocation context:
- `python -m analysis.objects.photons --sample <ID> --registry outputs/samples.registry.json --regions analysis/regions.yaml --out outputs/cache/<ID>.objects.parquet`

Example expected outputs:
- `outputs/samples.registry.json`
- `outputs/cache/<ID>.objects.parquet`
