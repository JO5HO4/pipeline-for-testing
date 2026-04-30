---
skill_id: SKILL_STATTOOL_OPTIONAL_PYHF_BACKEND
display_name: "StatTool Optional PyHF Backend"
version: 1.0
category: stats

summary: "`stattool` is an additive pyhf tool option and must not replace existing native statistics workflows."

invocation_keywords:
  - "stattool optional pyhf backend"
  - "caching"
  - "stattool"
  - "optional"
  - "pyhf"
  - "backend"

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
  - "Dependency SKILL_WORKSPACE_AND_FIT_PYHF has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_STATTOOL_OPTIONAL_PYHF_BACKEND are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_WORKSPACE_AND_FIT_PYHF

  may_follow:
    - SKILL_WORKSPACE_AND_FIT_PYHF

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
  - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
  - SKILL_PLOTTING_AND_REPORT
---

# Purpose

This skill defines a structured execution contract for `infrastructure/stattool_optional_pyhf_backend.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. Default is native pyhf path: `--pyhf-backend native`.
2. Optional values:
3. `--pyhf-backend stattool`
4. `--pyhf-backend auto` (uses `stattool` only when vendored/importable)
5. Applies when `--fit-backend pyhf` or when pyhf cross-checks run.
6. For H->gammagamma workflows, this skill applies only to cross-check mode and must not override primary RooFit outputs.

# Notes

- Source file: `infrastructure/stattool_optional_pyhf_backend.md`
- Original stage: `caching`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `no`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: StatTool Optional PyHF Backend

## Layer 1 — Physics Policy
`stattool` is an additive pyhf tool option and must not replace existing native statistics workflows.

Policy requirements:
- Keep existing in-repo stats implementation intact.
- Use `stattool` only as an optional backend for pyhf fit operations.
- Preserve existing RooFit-primary policy for H->gammagamma workflows.
- For H->gammagamma primary inference, pyhf/stattool is never a substitute for RooFit analytic-function fits.
- Record which pyhf implementation backend was requested and resolved at runtime.

## Layer 2 — Workflow Contract
### Runtime Selection
- Default is native pyhf path: `--pyhf-backend native`.
- Optional values:
  - `--pyhf-backend stattool`
  - `--pyhf-backend auto` (uses `stattool` only when vendored/importable)
- Applies when `--fit-backend pyhf` or when pyhf cross-checks run.
- For H->gammagamma workflows, this skill applies only to cross-check mode and must not override primary RooFit outputs.

### Add-Only Constraint
- Never remove or bypass existing native stats code.
- If `stattool` is unavailable, `auto` must fall back to native.
- If `stattool` is explicitly requested and unavailable, fail clearly with actionable error.
- If RooFit primary capability is unavailable in H->gammagamma workflows, block primary execution instead of promoting pyhf/stattool to primary.

### Provenance Requirements
- Run artifacts must include:
  - `pyhf_backend_requested`
  - `pyhf_backend_resolved`
  - `stattool_available`
  - `stattool_availability_reason`
  - `cross_check_only` (required when pyhf/stattool is used in H->gammagamma workflows)

## Layer 3 — Example Implementation
### Native Default
```bash
python -m analysis.cli run \
  --summary analysis/ATLAS_2012_H_to_gammagamma_discovery.analysis.json \
  --inputs input-data \
  --outputs outputs_native_stats \
  --fit-backend pyhf
```

### Runtime Auto Selection
```bash
python -m analysis.cli run \
  --summary analysis/ATLAS_2012_H_to_gammagamma_discovery.analysis.json \
  --inputs input-data \
  --outputs outputs_auto_stats \
  --fit-backend pyhf \
  --pyhf-backend auto
```

### Force StatTool
```bash
python -m analysis.cli run \
  --summary analysis/ATLAS_2012_H_to_gammagamma_discovery.analysis.json \
  --inputs input-data \
  --outputs outputs_stattool_stats \
  --fit-backend pyhf \
  --pyhf-backend stattool
```

# Examples

Example invocation context:
- `bash
python -m analysis.cli run \
  --summary analysis/ATLAS_2012_H_to_gammagamma_discovery.analysis.json \
  --inputs input-data \
  --outputs outputs_native_stats \
  --fit-backend pyhf`
- `bash
python -m analysis.cli run \
  --summary analysis/ATLAS_2012_H_to_gammagamma_discovery.analysis.json \
  --inputs input-data \
  --outputs outputs_auto_stats \
  --fit-backend pyhf \
  --pyhf-backend auto`
- `bash
python -m analysis.cli run \
  --summary analysis/ATLAS_2012_H_to_gammagamma_discovery.analysis.json \
  --inputs input-data \
  --outputs outputs_stattool_stats \
  --fit-backend pyhf \
  --pyhf-backend stattool`

Example expected outputs:
- `stage_output_artifacts_required_by_downstream_skills`
- `machine_readable_metadata_describing_execution_provenance`
