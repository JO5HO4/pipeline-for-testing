---
skill_id: SKILL_JSON_SPEC_DRIVEN_EXECUTION
display_name: "JSON-Spec-Driven Analysis Execution"
version: 1.0
category: other

summary: "The structured analysis JSON is the execution source of truth. Trigger prompts should stay minimal and point to the JSON."

invocation_keywords:
  - "json spec driven execution"
  - "json-spec-driven analysis execution"
  - "translation"
  - "json"
  - "spec"
  - "driven"
  - "analysis"
  - "execution"

when_to_use:
  - "Use when executing or validating the translation stage of the analysis workflow."
  - "Use when this context is available: analysis JSON path provided by user/prompt."
  - "Use when this context is available: input data/MC directory."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: analysis_json_path_provided_by_user_prompt
      type: artifact
      description: "analysis JSON path provided by user/prompt"
    - name: input_data_mc_directory
      type: artifact
      description: "input data/MC directory"
    - name: runtime_constraints
      type: artifact
      description: "runtime constraints (if any)"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: outputs_report_spec_validation_summary_json
    type: artifact
    description: "`outputs/report/spec_validation_summary.json`"
  - name: outputs_report_spec_to_runtime_mapping_json
    type: artifact
    description: "`outputs/report/spec_to_runtime_mapping.json`"
  - name: outputs_report_deviations_from_spec_json
    type: artifact
    description: "`outputs/report/deviations_from_spec.json`"
  - name: outputs_report_execution_contract_json
    type: artifact
    description: "`outputs/report/execution_contract.json`"
  - name: checkpoint_entries_in_outputs_report_skill_refresh_log_jsonl_for
    type: artifact
    description: "checkpoint entries in `outputs/report/skill_refresh_log.jsonl` for JSON validation and execution-contract phases"

preconditions:
  - "Dependency SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_JSON_SPEC_DRIVEN_EXECUTION are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR

  may_follow:
    - SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR
    - SKILL_SKILL_REFRESH_AND_CHECKPOINTING
    - SKILL_READ_SUMMARY_AND_VALIDATE
    - SKILL_FULL_STATISTICS_EXECUTION_POLICY
    - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
    - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF

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
  - "writes outputs_report_spec_validation_summary_json"
  - "writes outputs_report_spec_to_runtime_mapping_json"
  - "writes outputs_report_deviations_from_spec_json"
  - "writes outputs_report_execution_contract_json"
  - "writes checkpoint_entries_in_outputs_report_skill_refresh_log_jsonl_for"

failure_modes:
  - "summary validation succeeds (or failure is surfaced and execution stops)"
  - "when mandatory method constraints cannot be satisfied, execution status is blocked and no substituted primary fit/significance claim is emitted"

validation_checks:
  - "analysis JSON exists and is readable"
  - "summary validation succeeds (or failure is surfaced and execution stops)"
  - "selected runtime regions/observables are traceable to JSON fields"
  - "each runtime override is listed with `source = user_override`"
  - "each approximation/substitution is listed with reason and expected analysis impact"
  - "for H->gammagamma primary outputs, `fit_backend_primary` resolves to `pyroot_roofit`"
  - "when mandatory method constraints cannot be satisfied, execution status is blocked and no substituted primary fit/significance claim is emitted"
  - "final report references the JSON path used for the run"
  - "JSON-validation and execution-contract checkpoints are present in skill-refresh artifacts"

handoff_to:
  - SKILL_READ_SUMMARY_AND_VALIDATE
  - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
  - SKILL_SKILL_REFRESH_AND_CHECKPOINTING
  - SKILL_FULL_STATISTICS_EXECUTION_POLICY
  - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
  - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF
---

# Purpose

This skill defines a structured execution contract for `interfaces/json_spec_driven_execution.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `interfaces/json_spec_driven_execution.md`
- Original stage: `translation`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `no`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: JSON-Spec-Driven Analysis Execution

## Layer 1 — Physics Policy
The structured analysis JSON is the execution source of truth. Trigger prompts should stay minimal and point to the JSON.

Policy requirements:
- use the referenced analysis JSON as the primary specification for objectives, regions, observables, and fit scope
- run summary validation before production execution
- treat free-form narrative as secondary context unless the user gives an explicit override
- apply global workflow policies from the skills pack (blinding, reporting, discrepancy checks, handoff checks)
- default to full-statistics execution unless user scope explicitly requests partial statistics
- when the selected runtime pipeline is not fully JSON-native, create an explicit mapping from JSON intent to runtime configuration and document deviations
- if a user constraint overrides JSON content (for example luminosity, backend, or blinding scope), record the override explicitly
- mandatory physics-method constraints from skills (for example H->gammagamma primary RooFit analytic fits) are fail-closed and cannot be relaxed by runtime tool availability
- do not silently drop JSON-defined fit regions, observables, or process roles
- at execution-phase boundaries, record skill-refresh checkpoints per `governance/skill_refresh_and_checkpointing.md`

## Layer 2 — Workflow Contract
### Inputs
- analysis JSON path provided by user/prompt
- input data/MC directory
- runtime constraints (if any)

### Required Artifacts
- `outputs/report/spec_validation_summary.json`
- `outputs/report/spec_to_runtime_mapping.json`
- `outputs/report/deviations_from_spec.json`
- `outputs/report/execution_contract.json`
- checkpoint entries in `outputs/report/skill_refresh_log.jsonl` for JSON validation and execution-contract phases

### Acceptance Checks
- analysis JSON exists and is readable
- summary validation succeeds (or failure is surfaced and execution stops)
- selected runtime regions/observables are traceable to JSON fields
- each runtime override is listed with `source = user_override`
- each approximation/substitution is listed with reason and expected analysis impact
- for H->gammagamma primary outputs, `fit_backend_primary` resolves to `pyroot_roofit`
- when mandatory method constraints cannot be satisfied, execution status is blocked and no substituted primary fit/significance claim is emitted
- final report references the JSON path used for the run
- JSON-validation and execution-contract checkpoints are present in skill-refresh artifacts

### Minimum `execution_contract.json` fields
- `analysis_json`
- `inputs_path`
- `outputs_path`
- `full_statistics_required`
- `full_statistics_completed`
- `lumi_fb_runtime`
- `blinding_mode`
- `fit_backend_primary`
- `notes`

## Layer 3 — Example Implementation
### JSON Validation
`python -m analysis.config.load_summary --summary analysis/<analysis>.analysis.json --out outputs/summary.normalized.json`

### JSON-Native Pipeline (example)
`python -m analysis.cli run --summary analysis/<analysis>.analysis.json --inputs input-data --outputs outputs --all-samples`

### Non-JSON-Native Pipeline (example)
- run the dedicated pipeline
- write `spec_to_runtime_mapping.json` and `deviations_from_spec.json` to preserve JSON traceability

### Related Skills
- `core_pipeline/read_summary_and_validate.md`
- `governance/full_statistics_execution_policy.md`
- `core_pipeline/final_analysis_report_agent_workflow.md`
- `core_pipeline/final_report_review_and_handoff.md`
- `governance/skill_refresh_and_checkpointing.md`

# Examples

Example invocation context:
- `python -m analysis.config.load_summary --summary analysis/<analysis>.analysis.json --out outputs/summary.normalized.json`
- `python -m analysis.cli run --summary analysis/<analysis>.analysis.json --inputs input-data --outputs outputs --all-samples`

Example expected outputs:
- `outputs/report/spec_validation_summary.json`
- `outputs/report/spec_to_runtime_mapping.json`
- `outputs/report/deviations_from_spec.json`
- `outputs/report/execution_contract.json`
- `outputs/report/skill_refresh_log.jsonl`
- `outputs/summary.normalized.json`
