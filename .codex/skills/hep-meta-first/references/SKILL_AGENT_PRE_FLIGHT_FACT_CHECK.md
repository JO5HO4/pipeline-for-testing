---
skill_id: SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
display_name: "Agent Pre-Flight Fact Check"
version: 1.0
category: validation

summary: "Before launching a full analysis workflow, the agent must verify that critical analysis facts are defined unambiguously. If critical facts are missing or ambiguous, the agent must pause and request clarification before execution."

invocation_keywords:
  - "agent pre flight fact check"
  - "agent pre-flight fact check"
  - "validation"
  - "agent"
  - "flight"
  - "fact"
  - "check"

when_to_use:
  - "Use when executing or validating the validation stage of the analysis workflow."
  - "Use when this context is available: analysis specification or instruction prompt."
  - "Use when this context is available: analysis configuration JSON/YAML."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: analysis_specification_or_instruction_prompt
      type: artifact
      description: "analysis specification or instruction prompt"
    - name: analysis_configuration_json_yaml
      type: artifact
      description: "analysis configuration JSON/YAML"
    - name: dataset_description_files
      type: artifact
      description: "dataset description files"
    - name: links_to_analysis_documentation
      type: artifact
      description: "links to analysis documentation"
    - name: repository_configuration_files
      type: artifact
      description: "repository configuration files"

  optional:
    - name: previous_reports_notes_describing_intended_analysis
      type: artifact
      description: "previous reports/notes describing intended analysis"

outputs:
  - name: pass_fail_status
    type: artifact
    description: "pass/fail status"
  - name: clarified_items
    type: artifact
    description: "clarified items (if any)"
  - name: assumptions_recorded_before_execution
    type: artifact
    description: "assumptions recorded before execution"
  - name: skill_refresh_initialization_status_for_the_preflight_ready_chec
    type: artifact
    description: "skill-refresh initialization status for the `preflight_ready` checkpoint"
  - name: outputs_report_preflight_fact_check_json_with
    type: artifact
    description: "`outputs/report/preflight_fact_check.json` with:"
  - name: status
    type: artifact
    description: "`status` (`pass` or `blocked`)"
  - name: checked_items
    type: artifact
    description: "`checked_items` (list)"
  - name: missing_or_ambiguous
    type: artifact
    description: "`missing_or_ambiguous` (list)"
  - name: clarifications_received
    type: artifact
    description: "`clarifications_received` (list)"
  - name: assumptions
    type: artifact
    description: "`assumptions` (list)"
  - name: ready_to_execute
    type: artifact
    description: "`ready_to_execute` (bool)"
  - name: skill_refresh_initialized
    type: artifact
    description: "`skill_refresh_initialized` (bool)"
  - name: skill_refresh_checkpoint_id
    type: artifact
    description: "`skill_refresh_checkpoint_id` (string; expected `preflight_ready`)"
  - name: outputs_report_skill_compliance_gaps_json
    type: artifact
    description: "`outputs/report/skill_compliance_gaps.json` with non-compliant code/config components and owning skills"
  - name: outputs_report_skill_compliance_rewrite_plan_json
    type: artifact
    description: "`outputs/report/skill_compliance_rewrite_plan.json` with targeted rewrite actions, file scope, and acceptance checks"

preconditions:
  - "Dependency SKILL_BOOTSTRAP_REPO has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_AGENT_PRE_FLIGHT_FACT_CHECK are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_BOOTSTRAP_REPO

  may_follow:
    - SKILL_BOOTSTRAP_REPO
    - SKILL_READ_SUMMARY_AND_VALIDATE
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
    - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION
    - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
    - SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION
    - SKILL_SKILL_REFRESH_AND_CHECKPOINTING

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
  - "writes pass_fail_status"
  - "writes clarified_items"
  - "writes assumptions_recorded_before_execution"
  - "writes skill_refresh_initialization_status_for_the_preflight_ready_chec"
  - "writes outputs_report_preflight_fact_check_json_with"
  - "writes status"
  - "writes checked_items"
  - "writes missing_or_ambiguous"
  - "writes clarifications_received"
  - "writes assumptions"
  - "writes outputs_report_skill_compliance_gaps_json"
  - "writes outputs_report_skill_compliance_rewrite_plan_json"

failure_modes:
  - "if missing-but-buildable runtime/tooling is detected, plan construction/repair before production execution"

validation_checks:
  - "Measurement objective:"
  - "verify the scientific objective is explicit (for example search, significance, limits, fit scan)"
  - "Integrated luminosity:"
  - "verify luminosity value, units, and data-taking period are clear"
  - "Signal/background samples:"
  - "verify signal/background mapping and dataset identifiers are clear"
  - "verify nominal-vs-alternative sample selection is defined for each central physics process when multiple MC candidates exist"
  - "verify no decay-mismatched or inclusive samples are silently entering a decay-specific central signal definition"
  - "Systematic uncertainties:"
  - "verify there is an explicit statement:"
  - "systematics list"
  - "or omitted at this stage"
  - "or deferred with placeholder plan"
  - "Signal/control/sideband regions:"

handoff_to:
  - SKILL_READ_SUMMARY_AND_VALIDATE
  - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
  - SKILL_SKILL_REFRESH_AND_CHECKPOINTING
  - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION
  - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
  - SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION
  - SKILL_FULL_STATISTICS_EXECUTION_POLICY
---

# Purpose

This skill defines a structured execution contract for `governance/agent_pre_flight_fact_check.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `governance/agent_pre_flight_fact_check.md`
- Original stage: `validation`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Agent Pre-Flight Fact Check

## Layer 1 — Physics Policy
Before launching a full analysis workflow, the agent must verify that critical analysis facts are defined unambiguously. If critical facts are missing or ambiguous, the agent must pause and request clarification before execution.

Policy requirements:
- invoke this skill immediately after receiving the analysis task and before large-scale execution
- treat this as a one-time checkpoint before run start
- do not start large computation on incomplete specifications
- after pre-flight passes and execution begins, do not interrupt again until completion unless a hard technical failure prevents continuation
- record any assumptions explicitly
- initialize skill-refresh/checkpoint planning at run start and emit the first refresh checkpoint record
- verify mandatory method constraints are technically satisfiable before run start

## Layer 2 — Workflow Contract
### Inputs
- analysis specification or instruction prompt
- analysis configuration JSON/YAML
- dataset description files
- links to analysis documentation
- repository configuration files
- previous reports/notes describing intended analysis

### Required Fact Checks
1. Measurement objective:
   - verify the scientific objective is explicit (for example search, significance, limits, fit scan)
2. Integrated luminosity:
   - verify luminosity value, units, and data-taking period are clear
3. Signal/background samples:
   - verify signal/background mapping and dataset identifiers are clear
   - verify nominal-vs-alternative sample selection is defined for each central physics process when multiple MC candidates exist
   - verify no decay-mismatched or inclusive samples are silently entering a decay-specific central signal definition
4. Systematic uncertainties:
   - verify there is an explicit statement:
     - systematics list
     - or omitted at this stage
     - or deferred with placeholder plan
5. Signal/control/sideband regions:
   - verify region definitions exist and are logically consistent
   - verify no unintended SR/CR overlap unless explicitly intended
6. Blinding status:
   - verify blinded / partially blinded / unblinded status is explicit
   - if blinded, verify SR data handling policy is explicit
7. Statistical method:
   - verify requested statistical procedure and outputs are explicit
8. Mandatory backend/method capability:
   - verify required primary backend capabilities are available in the runtime
   - for H->gammagamma, verify PyROOT/RooFit analytic-function fit capability for primary fit and significance
9. Runtime/tooling readiness:
   - verify a functioning analysis pipeline/toolchain is available for required stages
   - verify ROOT event ingestion is supported through `uproot`
   - if missing-but-buildable runtime/tooling is detected, plan construction/repair before production execution
10. Skill compliance audit:
   - verify existing code and configuration satisfy currently active skill requirements
   - emit machine-readable non-compliance gaps with owning file/module scope
   - emit a targeted rewrite plan for each non-compliant component

### Escalation Rule
- if any critical item above is missing or ambiguous:
  - pause execution
  - present a concise missing/ambiguous-items list to the human
  - request clarification
- if functioning runtime/tooling is missing but buildable in-task:
  - construct/repair the missing pipeline/tooling first
  - run a limited-entry validation pass if needed
  - continue to full-sample execution before declaring completion
- if any code/config component is non-compliant with active skill requirements:
  - force rewrite of the smallest relevant pipeline component before production execution
  - do not proceed with production claims until rewritten component passes acceptance checks
- if mandatory backend/method capability is unavailable for the analysis target:
  - block execution for primary results
  - do not auto-substitute a different primary backend
- after clarification is received, proceed and avoid further interruption during run execution

### Required Output
Produce a short pre-flight summary containing:
- pass/fail status
- clarified items (if any)
- assumptions recorded before execution
- skill-refresh initialization status for the `preflight_ready` checkpoint
- compliance-audit status with gap list and rewrite plan references

## Layer 3 — Example Implementation
### Recommended Artifact
- `outputs/report/preflight_fact_check.json` with:
  - `status` (`pass` or `blocked`)
  - `checked_items` (list)
  - `missing_or_ambiguous` (list)
  - `clarifications_received` (list)
  - `assumptions` (list)
  - `ready_to_execute` (bool)
  - `skill_refresh_initialized` (bool)
  - `skill_refresh_checkpoint_id` (string; expected `preflight_ready`)
- `outputs/report/skill_compliance_gaps.json` with:
  - `status` (`pass` or `fail`)
  - `gaps` (list of non-compliant components with file/module ownership and required skill)
- `outputs/report/skill_compliance_rewrite_plan.json` with:
  - `status` (`ready` or `blocked`)
  - `actions` (ordered targeted rewrites with expected artifacts and acceptance checks)

### Minimum Human Message
- one concise statement that pre-flight passed or is blocked
- if blocked, a compact list of required clarifications

### Related Skills
- `core_pipeline/read_summary_and_validate.md`
- `core_pipeline/sample_registry_and_normalization.md`
- `governance/mc_sample_disambiguation_and_nominal_selection.md`
- `analysis_strategy/signal_background_strategy_and_cr_constraints.md`
- `analysis_strategy/control_region_signal_region_blinding_and_visualization.md`
- `governance/skill_refresh_and_checkpointing.md`

# Examples

Example invocation context:
- Run this contract in the declared stage using the required inputs and dependencies.

Example expected outputs:
- `outputs/report/preflight_fact_check.json`
