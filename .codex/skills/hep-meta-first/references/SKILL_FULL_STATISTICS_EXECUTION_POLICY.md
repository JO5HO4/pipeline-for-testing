---
skill_id: SKILL_FULL_STATISTICS_EXECUTION_POLICY
display_name: "Full-Statistics Execution Policy"
version: 1.0
category: governance

summary: "Final analysis claims must be based on full statistics for the selected samples."

invocation_keywords:
  - "full statistics execution policy"
  - "full-statistics execution policy"
  - "execution_policy"
  - "full"
  - "statistics"
  - "execution"
  - "policy"

when_to_use:
  - "Use when executing or validating the execution_policy stage of the analysis workflow."
  - "Use when this context is available: user request and constraints."
  - "Use when this context is available: analysis run configuration."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: user_request_and_constraints
      type: artifact
      description: "user request and constraints"
    - name: analysis_run_configuration
      type: artifact
      description: "analysis run configuration"
    - name: sample_file_inventory
      type: artifact
      description: "sample/file inventory"
    - name: runtime_control_flags
      type: artifact
      description: "runtime control flags (for example event caps)"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: statistics_policy_artifact
    type: artifact
    description: "statistics-policy artifact:"
  - name: outputs_report_statistics_policy_json
    type: artifact
    description: "`outputs/report/statistics_policy.json`"
  - name: fields
    type: artifact
    description: "fields:"
  - name: mode_in_full_required_partial_allowed_user_requested_fast_test_t
    type: artifact
    description: "`mode` in `{full_required, partial_allowed_user_requested, fast_test_then_full_required}`"
  - name: user_requested_partial
    type: artifact
    description: "`user_requested_partial` (bool)"
  - name: fast_test_used
    type: artifact
    description: "`fast_test_used` (bool)"
  - name: full_statistics_completed
    type: artifact
    description: "`full_statistics_completed` (bool)"
  - name: final_outputs_source
    type: artifact
    description: "`final_outputs_source` (`full_statistics` or `partial_statistics`)"
  - name: notes
    type: artifact
    description: "`notes` (list)"
  - name: run_manifest_must_clearly_record_event_cap_configuration_and_whe
    type: artifact
    description: "run manifest must clearly record event-cap configuration and whether full statistics were achieved"
  - name: if_fast_test_is_used_separate_output_roots_should_be_used_for_te
    type: artifact
    description: "if fast test is used, separate output roots should be used for test vs final runs"
  - name: runtime_recovery_artifact_when_missing_pipeline_tooling_was_cons
    type: artifact
    description: "runtime-recovery artifact when missing pipeline/tooling was constructed or repaired before execution"

preconditions:
  - "Dependency SKILL_AGENT_PRE_FLIGHT_FACT_CHECK has completed successfully."
  - "Dependency SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_FULL_STATISTICS_EXECUTION_POLICY are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
    - SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY

  may_follow:
    - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
    - SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY
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
  - "writes statistics_policy_artifact"
  - "writes outputs_report_statistics_policy_json"
  - "writes fields"
  - "writes mode_in_full_required_partial_allowed_user_requested_fast_test_t"
  - "writes user_requested_partial"
  - "writes fast_test_used"
  - "writes full_statistics_completed"
  - "writes final_outputs_source"
  - "writes notes"
  - "writes run_manifest_must_clearly_record_event_cap_configuration_and_whe"

failure_modes:
  - "when missing-but-buildable tooling/pipeline was detected, completion requires both a recovery record and a subsequent full-statistics production run"

validation_checks:
  - "if user did not explicitly request partial-only results, `full_statistics_completed` must be `true`"
  - "final report and handoff artifacts must point to full-statistics outputs unless user explicitly requested partial-only scope"
  - "any fast-test artifacts must be labeled non-final in report/handoff text"
  - "when missing-but-buildable tooling/pipeline was detected, completion requires both a recovery record and a subsequent full-statistics production run"
  - "no silent fallback from full to partial statistics is allowed"

handoff_to:
  - SKILL_HISTOGRAMMING_AND_TEMPLATES
  - SKILL_WORKSPACE_AND_FIT_PYHF
  - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
  - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
  - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF
---

# Purpose

This skill defines a structured execution contract for `governance/full_statistics_execution_policy.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. Determine runtime readiness:
2. if required pipeline/tooling is missing but buildable, construct/repair it before production execution
3. Determine run mode:
4. `full_required` by default
5. `partial_allowed_user_requested` only when user explicitly asks for partial statistics
6. `fast_test_then_full_required` when agent performs a short validation run first
7. For `full_required`:
8. disable event caps and process complete selected samples
9. For `fast_test_then_full_required`:
10. run fast test with explicit cap and test-labeled output directory
11. run full-statistics production pass in the same task with separate final output directory
12. Do not finalize the task until one of these is true:

# Notes

- Source file: `governance/full_statistics_execution_policy.md`
- Original stage: `execution_policy`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Full-Statistics Execution Policy

## Layer 1 — Physics Policy
Final analysis claims must be based on full statistics for the selected samples.

Policy requirements:
- default execution must use full statistics (all events in each selected sample/file)
- if required pipeline components or useful tooling are missing but buildable in-task, construct/repair them and continue toward full-statistics completion
- partial-statistics execution is allowed only when:
  - the user explicitly requests partial statistics, or
  - a fast test is needed for validation, with the explicit expectation that a full-statistics run is completed in the same task before handoff
- never present partial-statistics outputs as final analysis results unless the user explicitly requested a partial-only deliverable
- if a fast test is used first, clearly mark it as non-final and keep its outputs separate from final full-statistics outputs
- if full-statistics execution fails for technical reasons, report the blocker and classify the task as incomplete rather than silently handing off partial results

## Layer 2 — Workflow Contract
### Inputs
- user request and constraints
- analysis run configuration
- sample/file inventory
- runtime control flags (for example event caps)

### Decision Logic
1. Determine runtime readiness:
   - if required pipeline/tooling is missing but buildable, construct/repair it before production execution
2. Determine run mode:
   - `full_required` by default
   - `partial_allowed_user_requested` only when user explicitly asks for partial statistics
   - `fast_test_then_full_required` when agent performs a short validation run first
3. For `full_required`:
   - disable event caps and process complete selected samples
4. For `fast_test_then_full_required`:
   - run fast test with explicit cap and test-labeled output directory
   - run full-statistics production pass in the same task with separate final output directory
5. Do not finalize the task until one of these is true:
   - full-statistics run completed, or
   - user explicitly approved partial-only scope

### Required Artifacts
- statistics-policy artifact:
  - `outputs/report/statistics_policy.json`
  - fields:
    - `mode` in `{full_required, partial_allowed_user_requested, fast_test_then_full_required}`
    - `user_requested_partial` (bool)
    - `fast_test_used` (bool)
    - `full_statistics_completed` (bool)
    - `final_outputs_source` (`full_statistics` or `partial_statistics`)
    - `notes` (list)
- run manifest must clearly record event-cap configuration and whether full statistics were achieved
- if fast test is used, separate output roots should be used for test vs final runs
- runtime-recovery artifact when missing pipeline/tooling was constructed or repaired before execution

### Acceptance Checks
- if user did not explicitly request partial-only results, `full_statistics_completed` must be `true`
- final report and handoff artifacts must point to full-statistics outputs unless user explicitly requested partial-only scope
- any fast-test artifacts must be labeled non-final in report/handoff text
- when missing-but-buildable tooling/pipeline was detected, completion requires both a recovery record and a subsequent full-statistics production run
- no silent fallback from full to partial statistics is allowed

## Layer 3 — Example Implementation
### Current Repository (W+jets pipeline)
Full-statistics run:
```bash
.venv/bin/python -m analysis.wplus_highpt_pipeline \
  --inputs input-data \
  --lumi-fb 36.0 \
  --max-events-per-file 0
```

Fast test then full-statistics run (same task):
```bash
# Non-final fast test
.venv/bin/python -m analysis.wplus_highpt_pipeline \
  --inputs input-data \
  --lumi-fb 36.0 \
  --max-events-per-file 20000 \
  --outputs outputs_wplus_fasttest

# Final full-statistics production run
.venv/bin/python -m analysis.wplus_highpt_pipeline \
  --inputs input-data \
  --lumi-fb 36.0 \
  --max-events-per-file 0 \
  --outputs outputs_wplus_fullstat
```

Suggested `statistics_policy.json`:
- set `mode = full_required` for default runs
- set `mode = fast_test_then_full_required` when a fast test precedes a same-task full run
- set `mode = partial_allowed_user_requested` only when explicitly requested by the user

### Related Skills
- `governance/agent_pre_flight_fact_check.md`
- `infrastructure/smoke_tests_and_reproducibility.md`
- `core_pipeline/final_analysis_report_agent_workflow.md`
- `core_pipeline/final_report_review_and_handoff.md`

# Examples

Example invocation context:
- `bash
.venv/bin/python -m analysis.wplus_highpt_pipeline \
  --inputs input-data \
  --lumi-fb 36.0 \
  --max-events-per-file 0`
- `bash
# Non-final fast test
.venv/bin/python -m analysis.wplus_highpt_pipeline \
  --inputs input-data \
  --lumi-fb 36.0 \
  --max-events-per-file 20000 \
  --outputs outputs_wplus_fasttest

# Final full-statistics production run
.venv/bin/python -m analysis.wplus_highpt_pipeline \
  --inputs input-data \
  --lumi-fb 36.0 \
  --max-events-per-file 0 \
  --outputs outputs_wplus_fullstat`

Example expected outputs:
- `outputs/report/statistics_policy.json`
