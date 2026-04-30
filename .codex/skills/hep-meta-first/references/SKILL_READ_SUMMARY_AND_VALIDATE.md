---
skill_id: SKILL_READ_SUMMARY_AND_VALIDATE
display_name: "Read Summary and Validate"
version: 1.0
category: validation

summary: "The structured analysis definition is the source of truth for analysis intent and must be internally consistent."

invocation_keywords:
  - "read summary and validate"
  - "validation"
  - "read"
  - "summary"
  - "validate"

when_to_use:
  - "Use when executing or validating the validation stage of the analysis workflow."
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
  - name: normalized_analysis_definition_artifact_with_canonicalized_ident
    type: artifact
    description: "normalized analysis-definition artifact with canonicalized identifiers and fields"
  - name: validation_inventory_artifact_summarizing_number_of_regions_fit_
    type: artifact
    description: "validation-inventory artifact summarizing number of regions, fit IDs, observables, and POIs"
  - name: validation_diagnostic_artifact_describing_any_schema_or_cross_re
    type: artifact
    description: "validation-diagnostic artifact describing any schema or cross-reference failures"
  - name: overlap_policy_validation_artifact_listing_sr_cr_pairs_and_overl
    type: artifact
    description: "overlap-policy validation artifact listing SR/CR pairs and overlap allowance flags"
  - name: outputs_summary_normalized_json
    type: artifact
    description: "`outputs/summary.normalized.json`"
  - name: console_inventory_with_number_of_sr_cr_fit_ids_observables_and_p
    type: artifact
    description: "console inventory with number of SR/CR, fit IDs, observables, and POIs"

preconditions:
  - "Dependency SKILL_AGENT_PRE_FLIGHT_FACT_CHECK has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_READ_SUMMARY_AND_VALIDATE are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK

  may_follow:
    - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK

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
  - "writes normalized_analysis_definition_artifact_with_canonicalized_ident"
  - "writes validation_inventory_artifact_summarizing_number_of_regions_fit_"
  - "writes validation_diagnostic_artifact_describing_any_schema_or_cross_re"
  - "writes overlap_policy_validation_artifact_listing_sr_cr_pairs_and_overl"
  - "writes outputs_summary_normalized_json"
  - "writes console_inventory_with_number_of_sr_cr_fit_ids_observables_and_p"

failure_modes:
  - "Missing or ambiguous required inputs block execution."
  - "Schema, fit, or consistency checks fail and produce diagnostics."

validation_checks:
  - "all required keys and enums validate"
  - "signal-region and control-region identifiers are unique"
  - "each fit region reference resolves to an existing region"
  - "each signal-signature reference resolves to an existing signature"
  - "each result-to-fit reference resolves to an existing fit configuration"
  - "each SR/CR pair used together in a fit has declared overlap policy; default is `allow_overlap = false`"

handoff_to:
  - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
  - SKILL_CATEGORY_CHANNEL_REGION_PARTITIONING
  - SKILL_FULL_STATISTICS_EXECUTION_POLICY
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/read_summary_and_validate.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `core_pipeline/read_summary_and_validate.md`
- Original stage: `validation`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Read Summary and Validate

## Layer 1 — Physics Policy
The structured analysis definition is the source of truth for analysis intent and must be internally consistent.

Policy requirements:
- region identifiers must be unique and unambiguous
- fit-region references must resolve to declared regions
- signal-signature associations must resolve to declared signatures
- reported fit references must resolve to declared fits
- SR/CR overlap policy must be explicit: mutually exclusive by default, with any exception declared and justified
- invalid or ambiguous analysis definitions must fail fast
- this validation skill is executed after `governance/agent_pre_flight_fact_check.md` has confirmed execution readiness

## Layer 2 — Workflow Contract
### Required Artifacts
- normalized analysis-definition artifact with canonicalized identifiers and fields
- validation-inventory artifact summarizing number of regions, fit IDs, observables, and POIs
- validation-diagnostic artifact describing any schema or cross-reference failures
- overlap-policy validation artifact listing SR/CR pairs and overlap allowance flags

### Acceptance Checks
- all required keys and enums validate
- signal-region and control-region identifiers are unique
- each fit region reference resolves to an existing region
- each signal-signature reference resolves to an existing signature
- each result-to-fit reference resolves to an existing fit configuration
- each SR/CR pair used together in a fit has declared overlap policy; default is `allow_overlap = false`

## Layer 3 — Example Implementation
### CLI (Current Repository)
`python -m analysis.config.load_summary --summary analysis/analysis.summary.json --out outputs/summary.normalized.json`

### Outputs (Current Repository)
- `outputs/summary.normalized.json`
- console inventory with number of SR/CR, fit IDs, observables, and POIs

### Related Skills
- `governance/agent_pre_flight_fact_check.md`

# Examples

Example invocation context:
- `python -m analysis.config.load_summary --summary analysis/analysis.summary.json --out outputs/summary.normalized.json`

Example expected outputs:
- `outputs/summary.normalized.json`
