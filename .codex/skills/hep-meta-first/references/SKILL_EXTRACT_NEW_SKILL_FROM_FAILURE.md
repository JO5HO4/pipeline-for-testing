---
skill_id: SKILL_EXTRACT_NEW_SKILL_FROM_FAILURE
display_name: "Extract New Skill from Failure"
version: 1.0
category: governance

summary: "After a run completes and the final report is produced, evaluate execution outcomes for reusable capability gaps. Convert recurring gaps into candidate skills for human review, without auto-promoting them into production skills."

invocation_keywords:
  - "extract new skill from failure"
  - "design"
  - "extract"
  - "skill"
  - "from"
  - "failure"

when_to_use:
  - "Use when executing or validating the design stage of the analysis workflow."
  - "Use when this context is available: final report."
  - "Use when this context is available: run logs and warning/error outputs."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: final_report
      type: artifact
      description: "final report"
    - name: run_logs_and_warning_error_outputs
      type: artifact
      description: "run logs and warning/error outputs"
    - name: execution_notes
      type: artifact
      description: "execution notes"
    - name: code_patches_workflow_adjustments_made_during_the_run
      type: artifact
      description: "code patches/workflow adjustments made during the run"
    - name: unusual_numerical_or_structural_outputs
      type: artifact
      description: "unusual numerical or structural outputs"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: candidate_skill_files
    type: artifact
    description: "candidate skill files:"
  - name: candidate_skills_candidate_name_md
    type: artifact
    description: "`candidate_skills/<candidate_name>.md`"
  - name: run_level_extraction_summary
    type: artifact
    description: "run-level extraction summary:"
  - name: outputs_report_skill_extraction_summary_json
    type: artifact
    description: "`outputs/report/skill_extraction_summary.json`"
  - name: status
    type: artifact
    description: "`status` (`none_found` or `candidates_created`)"
  - name: n_candidates
    type: artifact
    description: "`n_candidates`"
  - name: candidates
    type: artifact
    description: "`candidates` (list of file paths)"
  - name: evidence_sources
    type: artifact
    description: "`evidence_sources` (list of artifact paths)"
  - name: promotion_rule
    type: artifact
    description: "`promotion_rule` (`human_approval_required`)"

preconditions:
  - "Dependency SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_EXTRACT_NEW_SKILL_FROM_FAILURE are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW

  may_follow:
    - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
    - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF
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
  - "writes candidate_skill_files"
  - "writes candidate_skills_candidate_name_md"
  - "writes run_level_extraction_summary"
  - "writes outputs_report_skill_extraction_summary_json"
  - "writes status"
  - "writes n_candidates"
  - "writes candidates"
  - "writes evidence_sources"
  - "writes promotion_rule"

failure_modes:
  - "stage status is recorded as pass, blocked, or failed with diagnostics"

validation_checks:
  - "required artifacts exist and satisfy schema/consistency expectations"
  - "stage status is recorded as pass, blocked, or failed with diagnostics"

handoff_to:
  - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF
  - SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY
  - SKILL_SELECTION_ENGINE_AND_REGIONS
  - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
---

# Purpose

This skill defines a structured execution contract for `meta/extract_new_skill_from_failure.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `meta/extract_new_skill_from_failure.md`
- Original stage: `design`
- Logic type classification: `governance`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Extract New Skill from Failure

## Layer 1 — Physics Policy
After a run completes and the final report is produced, evaluate execution outcomes for reusable capability gaps. Convert recurring gaps into candidate skills for human review, without auto-promoting them into production skills.

Governance requirements:
- approved production skills exist only in `skills/`
- newly proposed skills must be written in `candidate_skills/`
- files in `candidate_skills/` are not active skills
- do not move/promote candidate skills into `skills/` without explicit human approval
- run this step after task completion and final report generation
- run this step for every completed production run (mandatory default)
- always emit `outputs/report/skill_extraction_summary.json`, including zero-candidate runs

Operational requirements:
- use only observable run artifacts (reports, logs, warnings/errors, patches, workflow notes, outputs)
- do not rely on hidden internal reasoning traces
- create candidate skills only for likely recurring patterns, not one-off mistakes

## Layer 2 — Workflow Contract
### Inputs
- final report
- run logs and warning/error outputs
- execution notes
- code patches/workflow adjustments made during the run
- unusual numerical or structural outputs

### Detection Targets
Identify whether execution exposed:
- workaround-required failures
- repeated friction points
- improvised missing procedures
- missing decision logic causing confusion
- missing factual info that forced guessing
- missing validation/safety checks

### Decision Rule
Create candidate skills only when the issue is likely to recur.

Do not create candidate skills for:
- simple coding mistakes
- typographical errors
- one-time environment problems
- trivial syntax fixes
- purely incidental issues

### Candidate Skill Requirements
For each candidate skill, create a file under `candidate_skills/` including:
- Skill name
- Status: `candidate`
- Problem solved
- Run evidence that motivated it
- Intended scope
- Inputs
- Outputs
- Trigger conditions
- Constraints/invariants
- Why this is reusable vs a local patch

### Required Human Summary
Produce a concise summary listing:
- number of candidate skills proposed
- each candidate skill name
- motivating failure/workaround
- expected future utility

Explicitly state:
- candidate skills require human approval before promotion into `skills/`

## Layer 3 — Example Implementation
### Required Artifacts
- candidate skill files:
  - `candidate_skills/<candidate_name>.md`
- run-level extraction summary:
  - `outputs/report/skill_extraction_summary.json`

Suggested `skill_extraction_summary.json` fields:
- `status` (`none_found` or `candidates_created`)
- `n_candidates`
- `candidates` (list of file paths)
- `evidence_sources` (list of artifact paths)
- `promotion_rule` (`human_approval_required`)

### Trigger Condition
- invoke after:
  1. analysis execution is complete
  2. final report has been generated
  3. final handoff/review is being prepared (completion gate)

### Related Skills
- `core_pipeline/final_report_review_and_handoff.md`
- `core_pipeline/final_analysis_report_agent_workflow.md`
- `infrastructure/smoke_tests_and_reproducibility.md`

# Examples

Example invocation context:
- Run this contract in the declared stage using the required inputs and dependencies.

Example expected outputs:
- `outputs/report/skill_extraction_summary.json`
