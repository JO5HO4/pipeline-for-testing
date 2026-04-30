---
skill_id: SKILL_ROOTMLTOOL_CACHED_ANALYSIS
display_name: "RootMLTool Cached Analysis Backend Selection"
version: 1.0
category: other

summary: "Switching event I/O backends must not change physics conclusions beyond defined numerical tolerance."

invocation_keywords:
  - "rootmltool cached analysis"
  - "rootmltool cached analysis backend selection"
  - "caching"
  - "rootmltool"
  - "cached"
  - "analysis"
  - "backend"
  - "selection"

when_to_use:
  - "Use when executing or validating the caching stage of the analysis workflow."
  - "Use when this context is available: analysis configuration and stage-specific upstream artifacts."
  - "Use when this context is available: repository paths and runtime context for the current run."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."
  - "Do not use for central physics claims when the source skill marks this path as optional or cross-check only."

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
  - name: stage_output_artifacts_required_by_downstream_skills
    type: artifact
    description: "stage output artifacts required by downstream skills"
  - name: machine_readable_metadata_describing_execution_provenance
    type: artifact
    description: "machine-readable metadata describing execution provenance"

preconditions:
  - "Dependency SKILL_HISTOGRAMMING_AND_TEMPLATES has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_ROOTMLTOOL_CACHED_ANALYSIS are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_HISTOGRAMMING_AND_TEMPLATES

  may_follow:
    - SKILL_HISTOGRAMMING_AND_TEMPLATES

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
  - "writes stage_output_artifacts_required_by_downstream_skills"
  - "writes machine_readable_metadata_describing_execution_provenance"

failure_modes:
  - "stage status is recorded as pass, blocked, or failed with diagnostics"

validation_checks:
  - "required artifacts exist and satisfy schema/consistency expectations"
  - "stage status is recorded as pass, blocked, or failed with diagnostics"

handoff_to:
  - SKILL_HISTOGRAMMING_AND_TEMPLATES
  - SKILL_PLOTTING_AND_REPORT
---

# Purpose

This skill defines a structured execution contract for `infrastructure/rootmltool_cached_analysis.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `infrastructure/rootmltool_cached_analysis.md`
- Original stage: `caching`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `no`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: RootMLTool Cached Analysis Backend Selection

## Layer 1 — Physics Policy
Switching event I/O backends must not change physics conclusions beyond defined numerical tolerance.

Policy requirements:
- Existing native pipeline behavior must remain present and unchanged.
- Only the ingestion/cache stage may change when selecting `rootmltool`; object definitions, selections, histogramming, and statistical fitting must remain unchanged.
- `rootmltool` is a candidate/operational backend, not an automatic physics-model change.
- Backend promotion to default requires a documented parity pass against a native-baseline run.

## Layer 2 — Workflow Contract
### Runtime Backend Selection
- Default behavior is `analysis.cli run --event-backend native`.
- Use `analysis.cli run --event-backend auto` when you want runtime backend selection.
- `auto` resolves to `rootmltool` when vendored source is available/importable; otherwise it resolves to `native`.
- Use `--event-backend native` for baseline/reference production.
- Use `--event-backend rootmltool` when JSON intermediates are required for fast reruns.

### RootMLTool Cache Behavior
- RootML cache artifacts are written under `outputs/cache/rootmltool/`.
- Per-sample artifacts:
  - `<sample_id>.arrays.json`
  - `<sample_id>.arrays.meta.json`
- Cache reuse is enabled by default.
- Force rebuild with `--no-rootml-cache-reuse`.

### Parity Gate (Required Before Promotion)
- Run baseline and candidate with identical inputs, region config, and event cap.
- Compare outputs with:
  - `python -m analysis.cli parity-check --baseline <native_outputs> --candidate <rootml_outputs> --out <report.json> --fail-on-mismatch`
- Promotion requirement:
  - parity status must be `pass` (no failed metrics, no missing metrics, no extra metrics).

## Layer 3 — Example Implementation
### Baseline Run
```bash
python -m analysis.cli run \
  --summary analysis/ATLAS_2012_H_to_gammagamma_discovery.analysis.json \
  --inputs input-data \
  --outputs outputs_native_ref \
  --event-backend native
```

### Candidate Run (Runtime Choice)
```bash
python -m analysis.cli run \
  --summary analysis/ATLAS_2012_H_to_gammagamma_discovery.analysis.json \
  --inputs input-data \
  --outputs outputs_auto_candidate \
  --event-backend auto
```

### Required Parity Check
```bash
python -m analysis.cli parity-check \
  --baseline outputs_native_ref \
  --candidate outputs_auto_candidate \
  --out outputs_auto_candidate/report/parity_native_vs_auto.json \
  --fail-on-mismatch
```

# Examples

Example invocation context:
- `python -m analysis.cli parity-check --baseline <native_outputs> --candidate <rootml_outputs> --out <report.json> --fail-on-mismatch`
- `bash
python -m analysis.cli run \
  --summary analysis/ATLAS_2012_H_to_gammagamma_discovery.analysis.json \
  --inputs input-data \
  --outputs outputs_native_ref \
  --event-backend native`
- `bash
python -m analysis.cli run \
  --summary analysis/ATLAS_2012_H_to_gammagamma_discovery.analysis.json \
  --inputs input-data \
  --outputs outputs_auto_candidate \
  --event-backend auto`

Example expected outputs:
- `outputs/cache/rootmltool/`
