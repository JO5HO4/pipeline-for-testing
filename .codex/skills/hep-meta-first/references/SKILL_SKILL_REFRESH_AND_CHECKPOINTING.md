---
skill_id: SKILL_SKILL_REFRESH_AND_CHECKPOINTING
display_name: "Skill Refresh and Checkpointing"
version: 1.0
category: governance

summary: "Long, multi-stage analysis runs can drift away from required skill constraints. Skill-policy compliance must therefore be re-validated during execution, not only at run start."

invocation_keywords:
  - "skill refresh and checkpointing"
  - "governance"
  - "skill"
  - "refresh"
  - "checkpointing"

when_to_use:
  - "Use when executing or validating the governance stage of the analysis workflow."
  - "Use when this context is available: active task objective and selected analysis JSON."
  - "Use when this context is available: list of skills used in the run."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: active_task_objective_and_selected_analysis_json
      type: artifact
      description: "active task objective and selected analysis JSON"
    - name: list_of_skills_used_in_the_run
      type: artifact
      description: "list of skills used in the run"
    - name: canonical_phase_boundaries
      type: artifact
      description: "canonical phase boundaries"
    - name: execution_timeline_and_failure_recovery_events
      type: artifact
      description: "execution timeline and failure/recovery events"
    - name: required_output_artifact_matrix_for_each_phase
      type: artifact
      description: "required output-artifact matrix for each phase"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: outputs_report_skill_refresh_plan_json
    type: artifact
    description: "`outputs/report/skill_refresh_plan.json`:"
  - name: policy_version
    type: artifact
    description: "`policy_version`"
  - name: refresh_interval_minutes
    type: artifact
    description: "`refresh_interval_minutes`"
  - name: checkpoint_ids
    type: artifact
    description: "`checkpoint_ids` (ordered list)"
  - name: checkpoint_requirements
    type: artifact
    description: "`checkpoint_requirements` (mapping: checkpoint -> skills + required artifacts)"
  - name: status
    type: artifact
    description: "`status`"
  - name: outputs_report_skill_refresh_log_jsonl
    type: artifact
    description: "`outputs/report/skill_refresh_log.jsonl`:"
  - name: one_json_object_per_line_with
    type: artifact
    description: "one JSON object per line with:"
  - name: timestamp_utc
    type: artifact
    description: "`timestamp_utc`"
  - name: checkpoint_id
    type: artifact
    description: "`checkpoint_id`"
  - name: trigger
    type: artifact
    description: "`trigger`"
  - name: skills_reloaded
    type: artifact
    description: "`skills_reloaded` (list of paths)"
  - name: required_artifacts_checked
    type: artifact
    description: "`required_artifacts_checked` (list)"
  - name: decision
    type: artifact
    description: "`decision` (`pass`, `warn`, or `fail`)"

preconditions:
  - "Dependency SKILL_BOOTSTRAP_REPO has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_SKILL_REFRESH_AND_CHECKPOINTING are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_BOOTSTRAP_REPO

  may_follow:
    - SKILL_BOOTSTRAP_REPO
    - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
    - SKILL_JSON_SPEC_DRIVEN_EXECUTION
    - SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY
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
  - "writes outputs_report_skill_refresh_plan_json"
  - "writes policy_version"
  - "writes refresh_interval_minutes"
  - "writes checkpoint_ids"
  - "writes checkpoint_requirements"
  - "writes status"
  - "writes outputs_report_skill_refresh_log_jsonl"
  - "writes one_json_object_per_line_with"
  - "writes timestamp_utc"
  - "writes checkpoint_id"

failure_modes:
  - "`failure_recovery`:"
  - "refresh immediately after a technical failure and before resuming"
  - "every failure event has a subsequent `failure_recovery` refresh before resumed stage completion"

validation_checks:
  - "`run_start`:"
  - "create plan artifact and first refresh entry"
  - "`phase_boundary`:"
  - "refresh before entering each major phase"
  - "`elapsed_interval`:"
  - "refresh when elapsed time since previous refresh exceeds policy interval (default 20 minutes)"
  - "`failure_recovery`:"
  - "refresh immediately after a technical failure and before resuming"
  - "`pre_handoff_gate`:"
  - "refresh and run final compliance assertion before handoff classification"
  - "`preflight_ready`"
  - "`summary_validated`"
  - "`execution_contract_recorded`"
  - "`selection_hist_complete`"

handoff_to:
  - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF
  - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
  - SKILL_JSON_SPEC_DRIVEN_EXECUTION
  - SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY
---

# Purpose

This skill defines a structured execution contract for `governance/skill_refresh_and_checkpointing.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. Build checkpoint plan:
2. map each checkpoint ID to required skills and required output artifacts
3. At each trigger:
4. re-open the mapped skills
5. record a refresh event in `skill_refresh_log.jsonl`
6. For each checkpoint:
7. assert required artifacts exist and are readable
8. record pass/fail outcome
9. After failures:
10. require a `failure_recovery` refresh event before any resumed stage output is accepted
11. Finalize status:
12. if any mandatory checkpoint fails, set `status = fail` and `handoff_blocker = true`

# Notes

- Source file: `governance/skill_refresh_and_checkpointing.md`
- Original stage: `governance`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Skill Refresh and Checkpointing

## Layer 1 — Physics Policy
Long, multi-stage analysis runs can drift away from required skill constraints. Skill-policy compliance must therefore be re-validated during execution, not only at run start.

Policy requirements:
- initialize a run-scoped refresh/checkpoint plan before large-scale execution
- re-open relevant skill files at deterministic phase boundaries
- re-open relevant skill files when a fixed elapsed-time interval is exceeded
- re-open relevant skill files after any failure before resuming execution
- emit machine-readable refresh/checkpoint artifacts for every production run
- treat missing refresh/checkpoint artifacts as handoff blockers
- never mark a run handoff-ready when skill checkpoint status is failing or missing

## Layer 2 — Workflow Contract
### Inputs
- active task objective and selected analysis JSON
- list of skills used in the run
- canonical phase boundaries
- execution timeline and failure/recovery events
- required output-artifact matrix for each phase

### Definitions
- refresh event: re-open and re-check the skill files relevant to the next execution phase
- checkpoint: a refresh event plus an artifact-completeness assertion for that phase

### Required Triggers
1. `run_start`:
   - create plan artifact and first refresh entry
2. `phase_boundary`:
   - refresh before entering each major phase
3. `elapsed_interval`:
   - refresh when elapsed time since previous refresh exceeds policy interval (default 20 minutes)
4. `failure_recovery`:
   - refresh immediately after a technical failure and before resuming
5. `pre_handoff_gate`:
   - refresh and run final compliance assertion before handoff classification

### Required Artifacts
- `outputs/report/skill_refresh_plan.json`:
  - `policy_version`
  - `refresh_interval_minutes`
  - `checkpoint_ids` (ordered list)
  - `checkpoint_requirements` (mapping: checkpoint -> skills + required artifacts)
  - `status`
- `outputs/report/skill_refresh_log.jsonl`:
  - one JSON object per line with:
    - `timestamp_utc`
    - `checkpoint_id`
    - `trigger`
    - `skills_reloaded` (list of paths)
    - `required_artifacts_checked` (list)
    - `decision` (`pass`, `warn`, or `fail`)
    - `notes`
- `outputs/report/skill_checkpoint_status.json`:
  - `status` (`pass` or `fail`)
  - `checkpoints` (list of per-checkpoint results)
  - `missing_artifacts` (list)
  - `interval_violations` (list)
  - `recovery_refresh_violations` (list)
  - `handoff_blocker` (bool)
  - `notes`

### Minimum Checkpoint IDs
- `preflight_ready`
- `summary_validated`
- `execution_contract_recorded`
- `compliance_rewrite_synced`
- `selection_hist_complete`
- `fit_complete`
- `report_complete`
- `handoff_gate`

### Decision Logic
1. Build checkpoint plan:
   - map each checkpoint ID to required skills and required output artifacts
2. At each trigger:
   - re-open the mapped skills
   - record a refresh event in `skill_refresh_log.jsonl`
3. For each checkpoint:
   - assert required artifacts exist and are readable
   - record pass/fail outcome
   - if checkpoint requirements include unresolved compliance rewrites, enforce `fail`
4. After failures:
   - require a `failure_recovery` refresh event before any resumed stage output is accepted
5. Finalize status:
   - if any mandatory checkpoint fails, set `status = fail` and `handoff_blocker = true`

### Acceptance Checks
- all three refresh artifacts exist and are readable
- plan declares all minimum checkpoint IDs
- each minimum checkpoint ID appears in both refresh log and status artifact
- no elapsed interval violations unless explicitly justified in `notes`
- every failure event has a subsequent `failure_recovery` refresh before resumed stage completion
- final handoff review includes skill-refresh gate result from `skill_checkpoint_status.json`
- if `skill_checkpoint_status.json.status != pass`, run must be classified as not handoff-ready
- compliance rewrite artifacts (`outputs/report/skill_compliance_gaps.json`, `outputs/report/skill_compliance_rewrite_plan.json`, rewrite completion evidence) must be present and passing before `handoff_gate`

## Layer 3 — Example Implementation
### Suggested `skill_refresh_plan.json` Skeleton
```json
{
  "policy_version": "1.0",
  "refresh_interval_minutes": 20,
  "checkpoint_ids": [
    "preflight_ready",
    "summary_validated",
    "execution_contract_recorded",
    "selection_hist_complete",
    "fit_complete",
    "report_complete",
    "handoff_gate"
  ],
  "checkpoint_requirements": {
    "preflight_ready": {
      "skills": [
        "governance/agent_pre_flight_fact_check.md",
        "governance/skill_refresh_and_checkpointing.md"
      ],
      "artifacts": [
        "outputs/report/preflight_fact_check.json"
      ]
    }
  },
  "status": "active"
}
```

### Related Skills
- `governance/agent_pre_flight_fact_check.md`
- `interfaces/json_spec_driven_execution.md`
- `infrastructure/smoke_tests_and_reproducibility.md`
- `core_pipeline/final_report_review_and_handoff.md`

# Examples

Example invocation context:
- Run this contract in the declared stage using the required inputs and dependencies.

Example expected outputs:
- `outputs/report/skill_refresh_plan.json`
- `outputs/report/skill_refresh_log.jsonl`
- `outputs/report/skill_checkpoint_status.json`
- `outputs/report/preflight_fact_check.json`
