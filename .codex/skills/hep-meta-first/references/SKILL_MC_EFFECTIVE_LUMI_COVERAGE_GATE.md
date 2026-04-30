---
skill_id: SKILL_MC_EFFECTIVE_LUMI_COVERAGE_GATE
display_name: "MC Effective Luminosity Coverage Gate"
version: 1.0
category: validation

summary: "Enforce minimum effective-MC-luminosity coverage relative to target data luminosity with hard pass/fail outputs."

invocation_keywords:
  - "mc effective lumi coverage gate"
  - "effective luminosity gate"
  - "10x luminosity check"
  - "normalization validation"
  - "validation"

when_to_use:
  - "Use after MC normalization artifacts are produced and before final fitting/handoff."

when_not_to_use:
  - "Do not use when normalization artifacts are missing."

inputs:
  required:
    - name: outputs_normalization_norm_table_json
      type: artifact
      description: "`outputs/normalization/norm_table.json` with per-sample normalization terms."
    - name: target_luminosity_lumi_fb
      type: scalar
      description: "Target integrated luminosity in fb^-1 for the analysis."
    - name: threshold_multiplier
      type: scalar
      description: "Required minimum multiplier over target luminosity (default 10.0)."
    - name: sample_to_process_mapping
      type: artifact
      description: "Process mapping for required background processes in fit regions."

outputs:
  - name: outputs_report_mc_effective_lumi_check_json
    type: artifact
    description: "`outputs/report/mc_effective_lumi_check.json`"

preconditions:
  - "Dependency SKILL_MC_NORMALIZATION_METADATA_STACKING has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "Effective-luminosity gate artifact exists and records computed values and thresholds."
  - "If required process coverage fails threshold, status is failed and downstream handoff is blocked."

dependencies:
  requires:
    - SKILL_ENFORCEMENT_POLICY_DEFAULTS
    - SKILL_MC_NORMALIZATION_METADATA_STACKING

  may_follow:
    - SKILL_ENFORCEMENT_POLICY_DEFAULTS
    - SKILL_MC_NORMALIZATION_METADATA_STACKING
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION

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
  - "writes outputs/report/mc_effective_lumi_check.json"

failure_modes:
  - "norm table missing effective-luminosity-computable fields"
  - "missing background-process mapping for fit regions"
  - "effective luminosity below required multiplier threshold"

validation_checks:
  - "per-process effective luminosity computed and recorded"
  - "threshold rule evaluated as effective_lumi_fb >= threshold_multiplier * target_lumi_fb"
  - "for H->gammagamma baseline policy, threshold_multiplier defaults to 10.0"

handoff_to:
  - SKILL_BACKGROUND_TEMPLATE_SMOOTHING_POLICY
  - SKILL_WORKSPACE_AND_FIT_PYHF
  - SKILL_PLOTTING_AND_REPORT
  - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
---

# Purpose

This skill enforces a quantitative coverage gate for MC backgrounds.
It makes the `10 x target_lumi_fb` policy machine-checkable and non-bypassable.

# Procedure

1. Load normalization table and process mapping.
2. Compute effective luminosity per required process.
3. Evaluate threshold against `threshold_multiplier * target_lumi_fb`.
4. Emit machine-readable pass/fail artifact.

# Skill: MC Effective Luminosity Coverage Gate

## Layer 1 — Physics Policy
- Required background process coverage must be demonstrably sufficient.
- Policy default for this workflow: `effective_lumi_fb >= 10 * target_lumi_fb`.

## Layer 2 — Required Artifact
`outputs/report/mc_effective_lumi_check.json` with:
- `status`: `ok|failed`
- `target_lumi_fb`
- `threshold_multiplier`
- `required_min_lumi_fb`
- `per_process_effective_lumi_fb`
- `failing_processes`
- `blocking`: boolean

## Layer 3 — Failure Semantics
- If `status != ok`, final report handoff must remain blocked.
