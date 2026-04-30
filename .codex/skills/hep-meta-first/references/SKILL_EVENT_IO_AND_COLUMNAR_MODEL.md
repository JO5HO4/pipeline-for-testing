---
skill_id: SKILL_EVENT_IO_AND_COLUMNAR_MODEL
display_name: "Event IO and Columnar Model"
version: 1.0
category: io

summary: "Event ingestion must preserve the information required for object definition, event selection, and weighting."

invocation_keywords:
  - "event io and columnar model"
  - "io"
  - "event"
  - "columnar"
  - "model"

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
  - name: columnar_event_artifact_containing_scalar_event_fields_and_jagge
    type: artifact
    description: "columnar event artifact containing scalar event fields and jagged object collections"
  - name: io_diagnostics_artifact_with_event_counts_and_available_field_in
    type: artifact
    description: "IO diagnostics artifact with event counts and available field inventory"
  - name: optional_cache_artifact_for_reuse_in_downstream_stages
    type: artifact
    description: "optional cache artifact for reuse in downstream stages"

preconditions:
  - "Dependency SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_EVENT_IO_AND_COLUMNAR_MODEL are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION

  may_follow:
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION

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
  - "writes columnar_event_artifact_containing_scalar_event_fields_and_jagge"
  - "writes io_diagnostics_artifact_with_event_counts_and_available_field_in"
  - "writes optional_cache_artifact_for_reuse_in_downstream_stages"

failure_modes:
  - "required analysis fields are present or explicitly flagged missing"
  - "H->gammagamma runs record PyROOT availability for downstream statistical stages and fail-closed for primary claims if unavailable"

validation_checks:
  - "loaded event count is reported and non-negative"
  - "required analysis fields are present or explicitly flagged missing"
  - "object collections preserve per-event multiplicity"
  - "event-weight information is retained or explicitly derived"
  - "ROOT event ingestion is executed with `uproot` unless an explicit exception artifact justifies an alternative path"
  - "H->gammagamma runs record PyROOT availability for downstream statistical stages and fail-closed for primary claims if unavailable"

handoff_to:
  - SKILL_OBJECT_DEFINITIONS
  - SKILL_SELECTION_ENGINE_AND_REGIONS
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/event_io_and_columnar_model.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `core_pipeline/event_io_and_columnar_model.md`
- Original stage: `io`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Event IO and Columnar Model

## Layer 1 — Physics Policy
Event ingestion must preserve the information required for object definition, event selection, and weighting.

Policy requirements:
- support event-level and object-level observables
- preserve variable-length object collections
- keep event weights available for downstream weighted yields and fits
- permit scalable reading for large samples without changing physics content
- process ROOT ntuples with `uproot` as the default ingestion backend for event processing
- keep event-ingestion logic independent of PyROOT where possible; reserve PyROOT for mandatory H->gammagamma statistical fitting stages
- for H->gammagamma production runs, confirm PyROOT is installed/importable before starting fit/significance stages

## Layer 2 — Workflow Contract
### Required Artifacts
- columnar event artifact containing scalar event fields and jagged object collections
- IO diagnostics artifact with event counts and available field inventory
- optional cache artifact for reuse in downstream stages

### Acceptance Checks
- loaded event count is reported and non-negative
- required analysis fields are present or explicitly flagged missing
- object collections preserve per-event multiplicity
- event-weight information is retained or explicitly derived
- ROOT event ingestion is executed with `uproot` unless an explicit exception artifact justifies an alternative path
- H->gammagamma runs record PyROOT availability for downstream statistical stages and fail-closed for primary claims if unavailable

## Layer 3 — Example Implementation
### Supported IO (Current Repository)
- ROOT via `uproot`
- Parquet via `pyarrow/pandas`
- Awkward Array internal representation

### Function Contract (Current Repository)
`load_events(files, tree_name, branches, max_events=None) -> events`

### CLI (Current Repository)
`python -m analysis.io.readers --registry outputs/samples.registry.json --sample <ID> --max-events 10000 --out outputs/cache/<ID>.parquet`

# Examples

Example invocation context:
- `python -m analysis.io.readers --registry outputs/samples.registry.json --sample <ID> --max-events 10000 --out outputs/cache/<ID>.parquet`

Example expected outputs:
- `outputs/samples.registry.json`
- `outputs/cache/<ID>.parquet`
