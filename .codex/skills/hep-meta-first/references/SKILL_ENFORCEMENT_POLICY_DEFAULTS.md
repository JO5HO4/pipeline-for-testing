---
skill_id: SKILL_ENFORCEMENT_POLICY_DEFAULTS
display_name: "Enforcement Policy Defaults"
version: 1.0
category: governance

summary: "Define canonical policy defaults for enforcement-critical numerical constants and expose them as a machine-readable artifact."

invocation_keywords:
  - "enforcement policy defaults"
  - "policy defaults"
  - "lumi default policy"
  - "threshold default policy"
  - "governance"

when_to_use:
  - "Use before MC effective luminosity and smoothing enforcement gates."
  - "Use at run start when policy constants may be implied by analysis text but not explicit in runtime config."

when_not_to_use:
  - "Do not use when explicit user-approved overrides already exist and are documented."

inputs:
  required:
    - name: analysis_summary_specification
      type: artifact
      description: "Analysis summary JSON/YAML and metadata."
    - name: run_constraints_and_overrides
      type: artifact
      description: "User/runtime constraints including optional policy overrides."

outputs:
  - name: outputs_report_enforcement_policy_defaults_json
    type: artifact
    description: "`outputs/report/enforcement_policy_defaults.json`"

preconditions:
  - "Dependency SKILL_AGENT_PRE_FLIGHT_FACT_CHECK has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "Policy-default artifact exists with resolved defaults and override provenance."
  - "Downstream enforcement skills consume resolved constants from this artifact instead of hardcoded literals."

dependencies:
  requires:
    - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK

  may_follow:
    - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
    - SKILL_FULL_STATISTICS_EXECUTION_POLICY
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
  - "writes outputs/report/enforcement_policy_defaults.json"

failure_modes:
  - "target luminosity unresolved or non-physical"
  - "threshold multiplier unresolved or non-positive"
  - "conflicting overrides without explicit precedence"

validation_checks:
  - "artifact includes target_lumi_fb and threshold_multiplier as numeric values"
  - "default values are target_lumi_fb=36.0 and threshold_multiplier=10.0 when no override is approved"
  - "override provenance is explicitly recorded"

handoff_to:
  - SKILL_MC_EFFECTIVE_LUMI_COVERAGE_GATE
  - SKILL_BACKGROUND_TEMPLATE_SMOOTHING_POLICY
  - SKILL_ENFORCEMENT_PRE_HANDOFF_GATE
---

# Purpose

This skill creates one canonical source for enforcement constants so scratch-built pipelines do not drift.

# Procedure

1. Resolve policy constants from explicit override or default policy.
2. Validate constants for physical/logic sanity.
3. Write machine-readable defaults artifact with provenance.
4. Route downstream gates to consume this artifact.

# Skill: Enforcement Policy Defaults

## Canonical Defaults
- `target_lumi_fb = 36.0`
- `threshold_multiplier = 10.0`
- `required_min_effective_lumi_fb = target_lumi_fb * threshold_multiplier`

## Required Artifact
`outputs/report/enforcement_policy_defaults.json` with:
- `status`: `ok|failed`
- `target_lumi_fb`
- `threshold_multiplier`
- `required_min_effective_lumi_fb`
- `override_used`: boolean
- `override_source`
- `notes`
