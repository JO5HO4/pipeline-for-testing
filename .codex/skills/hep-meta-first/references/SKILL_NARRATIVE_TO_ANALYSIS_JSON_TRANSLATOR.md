---
skill_id: SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR
display_name: "Narrative-to-Analysis-JSON Translator"
version: 1.0
category: other

summary: "Convert free-form analysis narratives into the repository analysis JSON schema before execution. This translation is for specification quality control, not for inventing physics content."

invocation_keywords:
  - "narrative to analysis json translator"
  - "narrative-to-analysis-json translator"
  - "translation"
  - "narrative"
  - "analysis"
  - "json"
  - "translator"

when_to_use:
  - "Use when executing or validating the translation stage of the analysis workflow."
  - "Use when this context is available: narrative analysis text (prompt, note, or document)."
  - "Use when this context is available: optional reference JSON to reuse naming conventions."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: narrative_analysis_text
      type: artifact
      description: "narrative analysis text (prompt, note, or document)"

  optional:
    - name: optional_reference_json_to_reuse_naming_conventions
      type: artifact
      description: "optional reference JSON to reuse naming conventions"

outputs:
  - name: generated_analysis_json_draft_analysis_name_analysis_json
    type: artifact
    description: "generated analysis JSON draft: `analysis/<name>.analysis.json`"
  - name: gap_report_outputs_report_analysis_json_gap_report_json
    type: artifact
    description: "gap report: `outputs/report/analysis_json_gap_report.json`"
  - name: source_trace_map_outputs_report_analysis_json_source_trace_json
    type: artifact
    description: "source trace map: `outputs/report/analysis_json_source_trace.json`"

preconditions:
  - "Dependency SKILL_AGENT_PRE_FLIGHT_FACT_CHECK has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK

  may_follow:
    - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
    - SKILL_READ_SUMMARY_AND_VALIDATE
    - SKILL_JSON_SPEC_DRIVEN_EXECUTION

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
  - "writes generated_analysis_json_draft_analysis_name_analysis_json"
  - "writes gap_report_outputs_report_analysis_json_gap_report_json"
  - "writes source_trace_map_outputs_report_analysis_json_source_trace_json"

failure_modes:
  - "Missing or ambiguous required inputs block execution."
  - "Schema, fit, or consistency checks fail and produce diagnostics."

validation_checks:
  - "generated JSON passes `analysis.config.load_summary` validation"
  - "all top-level sections required by schema are present"
  - "every unresolved item is listed in the gap report"
  - "each assumption is tracked with rationale and expected impact"
  - "output clearly distinguishes `provided_by_user` vs `assumed_by_agent`"

handoff_to:
  - SKILL_JSON_SPEC_DRIVEN_EXECUTION
  - SKILL_READ_SUMMARY_AND_VALIDATE
---

# Purpose

This skill defines a structured execution contract for `interfaces/narrative_to_analysis_json_translator.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. Extract core metadata (analysis name, energy, luminosity context, objective).
2. Extract signal signature and background-process definitions.
3. Extract SR/CR definitions, region purposes, and fit observables.
4. Extract fit setup and expected reported result types.
5. Fill unresolved fields with explicit placeholders (`not_specified`) and log them.
6. Run summary validation and iterate until schema/cross-reference checks pass.
7. Emit gap report and unresolved-questions list.

# Notes

- Source file: `interfaces/narrative_to_analysis_json_translator.md`
- Original stage: `translation`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `no`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Narrative-to-Analysis-JSON Translator

## Layer 1 — Physics Policy
Convert free-form analysis narratives into the repository analysis JSON schema before execution. This translation is for specification quality control, not for inventing physics content.

Policy requirements:
- convert narrative statements into structured JSON fields used by the analysis summary schema
- preserve user-provided facts; do not fabricate missing numerical values or unsupported claims
- represent unknown or missing details explicitly (for example `not_specified`) instead of guessing
- produce a gap report that identifies missing, ambiguous, and non-actionable items
- validate the produced JSON with existing summary validation tools
- require explicit assumptions/deviations log before using the generated JSON for production

## Layer 2 — Workflow Contract
### Inputs
- narrative analysis text (prompt, note, or document)
- optional reference JSON to reuse naming conventions

### Required Artifacts
- generated analysis JSON draft: `analysis/<name>.analysis.json`
- gap report: `outputs/report/analysis_json_gap_report.json`
- source trace map: `outputs/report/analysis_json_source_trace.json`

### Translation Steps
1. Extract core metadata (analysis name, energy, luminosity context, objective).
2. Extract signal signature and background-process definitions.
3. Extract SR/CR definitions, region purposes, and fit observables.
4. Extract fit setup and expected reported result types.
5. Fill unresolved fields with explicit placeholders (`not_specified`) and log them.
6. Run summary validation and iterate until schema/cross-reference checks pass.
7. Emit gap report and unresolved-questions list.

### Acceptance Checks
- generated JSON passes `analysis.config.load_summary` validation
- all top-level sections required by schema are present
- every unresolved item is listed in the gap report
- each assumption is tracked with rationale and expected impact
- output clearly distinguishes `provided_by_user` vs `assumed_by_agent`

### Minimum `analysis_json_gap_report.json` fields
- `status` (`pass_with_gaps` or `pass_no_gaps`)
- `missing_required_details` (list)
- `ambiguous_items` (list)
- `non_actionable_narrative_items` (list)
- `assumptions_applied` (list)
- `questions_for_user` (list)

## Layer 3 — Example Implementation
### Validate Draft JSON
`python -m analysis.config.load_summary --summary analysis/<name>.analysis.json --out outputs/summary.normalized.json`

### Suggested Handoff Rule
- do not start production execution until `analysis_json_gap_report.json` is produced and reviewed

### Related Skills
- `core_pipeline/read_summary_and_validate.md`
- `governance/agent_pre_flight_fact_check.md`
- `interfaces/json_spec_driven_execution.md`

# Examples

Example invocation context:
- `python -m analysis.config.load_summary --summary analysis/<name>.analysis.json --out outputs/summary.normalized.json`

Example expected outputs:
- `outputs/report/analysis_json_gap_report.json`
- `outputs/report/analysis_json_source_trace.json`
- `outputs/summary.normalized.json`
