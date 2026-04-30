---
skill_id: SKILL_FREEZE_ANALYSIS_HISTOGRAM_PRODUCTS
display_name: "Freeze Analysis Histogram Products"
version: 1.0
category: histograms

summary: "Histogram templates produced from expensive event processing should be frozen into immutable, reusable artifacts so downstream analysis can iterate without rerunning event loops."

invocation_keywords:
  - "freeze analysis histogram products"
  - "caching"
  - "freeze"
  - "analysis"
  - "histogram"
  - "products"

when_to_use:
  - "Use when executing or validating the caching stage of the analysis workflow."
  - "Use when this context is available: `outputs/hists/` templates (`<region>/<observable>/<sample>.npz`)."
  - "Use when this context is available: `outputs/summary.normalized.json`."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."
  - "Do not use for central physics claims when the source skill marks this path as optional or cross-check only."

inputs:
  required:
    - name: outputs_hists_templates
      type: artifact
      description: "`outputs/hists/` templates (`<region>/<observable>/<sample>.npz`)"
    - name: outputs_summary_normalized_json
      type: artifact
      description: "`outputs/summary.normalized.json`"
    - name: outputs_samples_registry_json
      type: artifact
      description: "`outputs/samples.registry.json` (if available)"
    - name: run_provenance
      type: artifact
      description: "run provenance:"
    - name: analysis_name_version
      type: artifact
      description: "analysis name/version"
    - name: git_commit
      type: artifact
      description: "git commit"
    - name: config_hash
      type: artifact
      description: "config hash"
    - name: timestamp
      type: artifact
      description: "timestamp"

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
  - "All declared outputs for SKILL_FREEZE_ANALYSIS_HISTOGRAM_PRODUCTS are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_HISTOGRAMMING_AND_TEMPLATES

  may_follow:
    - SKILL_HISTOGRAMMING_AND_TEMPLATES
    - SKILL_WORKSPACE_AND_FIT_PYHF
    - SKILL_PLOTTING_AND_REPORT
    - SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY

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
  - SKILL_ROOTMLTOOL_CACHED_ANALYSIS
  - SKILL_PLOTTING_AND_REPORT
  - SKILL_WORKSPACE_AND_FIT_PYHF
  - SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY
---

# Purpose

This skill defines a structured execution contract for `infrastructure/freeze_analysis_histogram_products.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. Search existing frozen bundles for matching `cache_key`.
2. Validate checksum(s) and required files.
3. Reuse only if both key and checksum validation pass.
4. write a new `freeze_id` bundle (do not overwrite existing bundle content).

# Notes

- Source file: `infrastructure/freeze_analysis_histogram_products.md`
- Original stage: `caching`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `no`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Freeze Analysis Histogram Products

## Layer 1 — Physics Policy
Histogram templates produced from expensive event processing should be frozen into immutable, reusable artifacts so downstream analysis can iterate without rerunning event loops.

Policy requirements:
- Freeze only after histogram production has passed basic integrity checks.
- Preserve statistical content required for physics reuse (`counts`, `sumw2`, bin edges).
- Keep repository-native histogram format (`.npz`) as the authoritative physics artifact in this codebase.
- JSON exports are secondary agent-readable sidecars.
- Never replace existing baseline workflows; freezing is additive and optional.
- Frozen artifacts are immutable once finalized.

## Layer 2 — Workflow Contract
### When To Use
- Run immediately after `core_pipeline/histogramming_and_templates.md` is complete.
- Use for repeated downstream tasks:
  - plotting
  - workspace building
  - fit and significance reruns
  - report updates
  - optimization scans

### Required Inputs
- `outputs/hists/` templates (`<region>/<observable>/<sample>.npz`)
- `outputs/summary.normalized.json`
- `outputs/samples.registry.json` (if available)
- run provenance:
  - analysis name/version
  - git commit
  - config hash
  - timestamp

### Required Frozen Bundle Artifacts
- `outputs/frozen/<freeze_id>/manifest_index.json`
- `outputs/frozen/<freeze_id>/<sample>/<region>/<observable>/nominal.npz`
- `outputs/frozen/<freeze_id>/<sample>/<region>/<observable>/manifest.json`
- `outputs/frozen/<freeze_id>/<sample>/<region>/<observable>/nominal.json` (agent-readable sidecar)
- `outputs/frozen/<freeze_id>/validation_report.json`

`freeze_id` must be deterministic and include at least:
- analysis version
- config hash prefix
- git commit prefix

### Cache Key Rules
Each frozen histogram manifest must include a deterministic `cache_key` computed from canonical JSON over:
- analysis version
- sample/process id
- region id
- observable
- bin edges
- config hash
- git commit
- weight/modeling metadata available at freeze time

Recommended hash:
- `sha256(canonical_json_bytes)`

Canonicalization rules:
- sort keys
- UTF-8 encoding
- no whitespace-dependent formatting

### Reuse Logic
Before writing a new frozen artifact:
1. Search existing frozen bundles for matching `cache_key`.
2. Validate checksum(s) and required files.
3. Reuse only if both key and checksum validation pass.

If mismatch or corruption is found:
- write a new `freeze_id` bundle (do not overwrite existing bundle content).

### Invalidation Rules
Must invalidate (regenerate freeze artifacts) when any of these change:
- region selections or cut logic
- observable definitions or binning
- dataset membership
- event weighting recipe
- object definitions / working points
- systematic configuration
- histogramming code affecting numerical content

May reuse frozen artifacts when only these change:
- plotting style
- axis ranges
- report formatting/text
- visualization grouping that does not alter bin content

### Validation Requirements
Each frozen artifact must be validated:
- `len(counts) == len(edges) - 1`
- `len(sumw2) == len(counts)`
- no NaN/Inf in `counts` or `sumw2`
- manifest includes required provenance fields
- checksum recorded and reproducible

`validation_report.json` must include:
- status (`pass`/`fail`)
- number of artifacts checked
- failed checks (if any)
- missing files (if any)

### Safety Rules
- Never silently overwrite an existing finalized artifact file.
- Use temp-file write + atomic rename for each artifact.
- If target path exists with different checksum, create a new bundle directory.

## Layer 3 — Example Implementation
### Repository-Native Source Layout
- `outputs/hists/<region>/<observable>/<sample>.npz`

### Frozen Layout
```text
outputs/frozen/<freeze_id>/
  manifest_index.json
  validation_report.json
  <sample>/
    <region>/
      <observable>/
        nominal.npz
        nominal.json
        manifest.json
```

### Minimum Manifest Fields (`manifest.json`)
- `freeze_id`
- `cache_key`
- `sample`
- `region`
- `observable`
- `bin_edges`
- `checksum_nominal_npz`
- `source_npz_path`
- `analysis_version`
- `config_hash`
- `git_commit`
- `timestamp_utc`
- `blinding_state` (if available)

### Related Skills
- `core_pipeline/histogramming_and_templates.md`
- `core_pipeline/workspace_and_fit_pyhf.md`
- `core_pipeline/plotting_and_report.md`
- `infrastructure/smoke_tests_and_reproducibility.md`

# Examples

Example invocation context:
- Run this contract in the declared stage using the required inputs and dependencies.

Example expected outputs:
- `outputs/hists/`
- `outputs/summary.normalized.json`
- `outputs/samples.registry.json`
- `outputs/frozen/<freeze_id>/manifest_index.json`
- `outputs/frozen/<freeze_id>/<sample>/<region>/<observable>/nominal.npz`
- `outputs/frozen/<freeze_id>/<sample>/<region>/<observable>/manifest.json`
- `outputs/frozen/<freeze_id>/<sample>/<region>/<observable>/nominal.json`
- `outputs/frozen/<freeze_id>/validation_report.json`
