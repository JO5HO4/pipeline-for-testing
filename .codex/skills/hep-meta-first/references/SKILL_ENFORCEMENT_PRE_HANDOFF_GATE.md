---
skill_id: SKILL_ENFORCEMENT_PRE_HANDOFF_GATE
display_name: "Enforcement Pre-Handoff Gate"
version: 1.0
category: reporting

summary: "Final non-bypass gate that requires smoothing and effective-luminosity policy artifacts to be present and passing before handoff."

invocation_keywords:
  - "enforcement pre handoff gate"
  - "pre handoff gate"
  - "policy enforcement gate"
  - "reporting gate"
  - "governance"

when_to_use:
  - "Use immediately before final report review and handoff."

when_not_to_use:
  - "Do not use before required upstream check artifacts are produced."

inputs:
  required:
    - name: outputs_report_background_template_smoothing_check_json
      type: artifact
      description: "`outputs/report/background_template_smoothing_check.json`"
    - name: outputs_report_mc_effective_lumi_check_json
      type: artifact
      description: "`outputs/report/mc_effective_lumi_check.json`"
    - name: outputs_report_data_mc_discrepancy_audit_json
      type: artifact
      description: "`outputs/report/data_mc_discrepancy_audit.json`"
    - name: outputs_report_enforcement_policy_defaults_json
      type: artifact
      description: "`outputs/report/enforcement_policy_defaults.json`"
    - name: outputs_report_skill_extraction_summary_json
      type: artifact
      description: "`outputs/report/skill_extraction_summary.json`"

outputs:
  - name: outputs_report_enforcement_handoff_gate_json
    type: artifact
    description: "`outputs/report/enforcement_handoff_gate.json`"

preconditions:
  - "Dependency SKILL_BACKGROUND_TEMPLATE_SMOOTHING_POLICY has completed successfully."
  - "Dependency SKILL_MC_EFFECTIVE_LUMI_COVERAGE_GATE has completed successfully."
  - "Dependency SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "Handoff gate artifact exists with explicit pass/fail status and blocking reasons."
  - "If gate status is failed, handoff-ready state must be false."

dependencies:
  requires:
    - SKILL_BACKGROUND_TEMPLATE_SMOOTHING_POLICY
    - SKILL_MC_EFFECTIVE_LUMI_COVERAGE_GATE
    - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW

  may_follow:
    - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
    - SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK
    - SKILL_EXTRACT_NEW_SKILL_FROM_FAILURE

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
  - "writes outputs/report/enforcement_handoff_gate.json"

failure_modes:
  - "required enforcement check artifact missing"
  - "required enforcement check status not ok"
  - "required governance artifact missing"

validation_checks:
  - "smoothing check artifact exists and has status ok"
  - "effective lumi check artifact exists and has status ok"
  - "required governance artifacts exist"
  - "policy-default artifact exists and is consistent with downstream gate thresholds"
  - "outputs/report/enforcement_handoff_gate.json marks blocking=true when any required gate fails"

handoff_to:
  - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF
---

# Purpose

This skill provides a strict final enforcement gate before handoff.
It prevents successful handoff when required policy checks are missing or failing.

# Procedure

1. Load required enforcement and governance artifacts.
2. Evaluate mandatory statuses.
3. Write a single machine-readable handoff gate artifact.
4. Block final handoff when any mandatory gate fails.

# Skill: Enforcement Pre-Handoff Gate

## Required Artifact
`outputs/report/enforcement_handoff_gate.json` with:
- `status`: `ok|failed`
- `required_checks`
- `failed_checks`
- `blocking`: boolean
- `notes`

## Non-Bypass Rule
- Final report review/handoff must not claim `handoff_ready: true` unless this gate is `ok`.
