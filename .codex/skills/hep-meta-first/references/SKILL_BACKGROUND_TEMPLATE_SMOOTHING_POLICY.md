---
skill_id: SKILL_BACKGROUND_TEMPLATE_SMOOTHING_POLICY
display_name: "Background Template Smoothing Policy"
version: 1.0
category: validation

summary: "Enforce explicit, auditable smoothing policy for background templates with hard pass/fail outputs."

invocation_keywords:
  - "background template smoothing policy"
  - "template smoothing gate"
  - "smoothing policy"
  - "validation"
  - "background"
  - "templates"

when_to_use:
  - "Use after histogram/template production and before statistical fitting."
  - "Use when background templates feed spurious-signal scans or final likelihood fits."

when_not_to_use:
  - "Do not use when histogram/template artifacts are missing."

inputs:
  required:
    - name: histogram_template_artifacts
      type: artifact
      description: "Per-region/per-observable/per-sample template artifacts and metadata."
    - name: smoothing_policy_configuration
      type: artifact
      description: "Configured smoothing method, thresholds, and allowed regions/processes."
    - name: fit_region_definitions
      type: artifact
      description: "Fit-region observable map used downstream in statistical modeling."

outputs:
  - name: outputs_report_background_template_smoothing_check_json
    type: artifact
    description: "`outputs/report/background_template_smoothing_check.json`"
  - name: outputs_report_background_template_smoothing_provenance_json
    type: artifact
    description: "`outputs/report/background_template_smoothing_provenance.json`"

preconditions:
  - "Dependency SKILL_HISTOGRAMMING_AND_TEMPLATES has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "Both declared output artifacts exist and include pass/fail status plus evidence paths."
  - "If smoothing is required but missing/noncompliant, stage status is failed and downstream fit stages are blocked."

dependencies:
  requires:
    - SKILL_ENFORCEMENT_POLICY_DEFAULTS
    - SKILL_HISTOGRAMMING_AND_TEMPLATES

  may_follow:
    - SKILL_ENFORCEMENT_POLICY_DEFAULTS
    - SKILL_HISTOGRAMMING_AND_TEMPLATES
    - SKILL_MC_NORMALIZATION_METADATA_STACKING

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
  - "writes outputs/report/background_template_smoothing_check.json"
  - "writes outputs/report/background_template_smoothing_provenance.json"

failure_modes:
  - "required smoothing config missing or ambiguous"
  - "required templates missing in fit regions"
  - "smoothing-required templates have no smoothing provenance marker"
  - "post-smoothing validation metrics fail configured thresholds"

validation_checks:
  - "all fit-region background templates are enumerated and checked"
  - "required smoothing method matches declared policy"
  - "smoothing metadata includes method, parameters, and scope"
  - "smoothing did not silently alter binning or break template-yield compatibility"

handoff_to:
  - SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION
  - SKILL_SYSTEMATICS_AND_NUISANCES
  - SKILL_PLOTTING_AND_REPORT
  - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
---

# Purpose

This skill enforces a non-bypassable smoothing policy for background templates.
It requires machine-readable pass/fail outputs before statistical fitting and reporting.

# Procedure

1. Read smoothing policy and template metadata.
2. Evaluate all required fit-region background templates.
3. Write smoothing check and provenance artifacts with explicit status.
4. Block downstream fit/reporting when status is not `ok`.

# Skill: Background Template Smoothing Policy

## Layer 1 — Physics Policy
- If smoothing is required by policy, it must be applied and recorded.
- No implicit smoothing is allowed.
- No silent template replacement is allowed.

## Layer 2 — Workflow Contract
### Required Artifacts
- `outputs/report/background_template_smoothing_check.json`
- `outputs/report/background_template_smoothing_provenance.json`

### Required Fields in `background_template_smoothing_check.json`
- `status`: `ok|failed`
- `required`: boolean
- `method_expected`
- `method_observed`
- `checked_templates`
- `failed_templates`
- `evidence_paths`
- `blocking`: boolean

### Required Fields in `background_template_smoothing_provenance.json`
- `policy_version`
- `method`
- `parameters`
- `scope`
- `template_artifact_hashes`
- `timestamp_utc`

## Layer 3 — Failure Semantics
- If `status != ok`, downstream skills that build/fit/report must not claim handoff readiness.
