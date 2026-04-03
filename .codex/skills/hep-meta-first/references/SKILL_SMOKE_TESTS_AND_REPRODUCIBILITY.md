---
skill_id: SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY
display_name: "Smoke Tests and Reproducibility"
version: 1.0
category: validation

summary: "Automated analysis execution must be reproducible and verifiable across runs."

invocation_keywords:
  - "smoke tests and reproducibility"
  - "validation"
  - "smoke"
  - "tests"
  - "reproducibility"

when_to_use:
  - "Use when executing or validating the validation stage of the analysis workflow."
  - "Use when this context is available: analysis configuration and stage-specific upstream artifacts."
  - "Use when this context is available: repository paths and runtime context for the current run."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: analysis_configuration_and_stage_specific_upstream_artifacts
      type: artifact
      description: "analysis configuration and stage-specific upstream artifacts"
    - name: repository_paths_and_runtime_context_for_the_current_run
      type: artifact
      description: "repository paths and runtime context for the current run"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: smoke_test_execution_artifact_with_pass_fail_status_per_critical
    type: artifact
    description: "smoke-test execution artifact with pass/fail status per critical stage"
  - name: run_manifest_artifact_with_inputs_configuration_fingerprint_and_
    type: artifact
    description: "run-manifest artifact with inputs, configuration fingerprint, and code version"
  - name: completion_status_artifact_indicating_whether_all_required_analy
    type: artifact
    description: "completion-status artifact indicating whether all required analysis outputs exist"
  - name: skill_refresh_plan_artifact_outputs_report_skill_refresh_plan_js
    type: artifact
    description: "skill-refresh plan artifact: `outputs/report/skill_refresh_plan.json`"
  - name: skill_refresh_log_artifact_outputs_report_skill_refresh_log_json
    type: artifact
    description: "skill-refresh log artifact: `outputs/report/skill_refresh_log.jsonl`"
  - name: skill_checkpoint_status_artifact_outputs_report_skill_checkpoint
    type: artifact
    description: "skill-checkpoint status artifact: `outputs/report/skill_checkpoint_status.json`"

preconditions:
  - "Dependency SKILL_BOOTSTRAP_REPO has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_BOOTSTRAP_REPO

  may_follow:
    - SKILL_BOOTSTRAP_REPO

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
  - "writes smoke_test_execution_artifact_with_pass_fail_status_per_critical"
  - "writes run_manifest_artifact_with_inputs_configuration_fingerprint_and_"
  - "writes completion_status_artifact_indicating_whether_all_required_analy"
  - "writes skill_refresh_plan_artifact_outputs_report_skill_refresh_plan_js"
  - "writes skill_refresh_log_artifact_outputs_report_skill_refresh_log_json"
  - "writes skill_checkpoint_status_artifact_outputs_report_skill_checkpoint"

failure_modes:
  - "for H->gammagamma, smoke checks fail if primary fit/significance backend is anything other than RooFit analytic-function path"
  - "if a mini-run is used after constructing/repairing missing runtime tooling, completion still requires a full-statistics production run in the same task"

validation_checks:
  - "summary validation stage passes"
  - "sample-registry and strategy stages pass"
  - "at least one end-to-end mini-run stage passes"
  - "fit and significance stages pass when workspace exists"
  - "blinding, histogram, yield, cut-flow, and report artifacts are all present for completion"
  - "reruns with same inputs/configuration produce consistent metadata fingerprints"
  - "ROOT event-ingestion smoke check validates `uproot` availability/import"
  - "for H->gammagamma resonance fitting, include a PyROOT/RooFit backend-specific smoke check and export the same standard fit/significance schemas"
  - "skill-refresh artifacts exist and indicate pass status before handoff"
  - "for H->gammagamma, smoke checks fail if primary fit/significance backend is anything other than RooFit analytic-function path"
  - "if a mini-run is used after constructing/repairing missing runtime tooling, completion still requires a full-statistics production run in the same task"

handoff_to:
  - SKILL_FULL_STATISTICS_EXECUTION_POLICY
  - SKILL_PLOTTING_AND_REPORT
---

# Purpose

This skill defines a structured execution contract for `infrastructure/smoke_tests_and_reproducibility.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `infrastructure/smoke_tests_and_reproducibility.md`
- Original stage: `validation`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Smoke Tests and Reproducibility

## Layer 1 — Physics Policy
Automated analysis execution must be reproducible and verifiable across runs.

Policy requirements:
- each critical stage must be testable in a minimal run
- nondeterministic behavior must be controlled
- configuration and code provenance must be recorded
- completion claims require both physics outputs and validation artifacts
- mandatory-method constraints must be enforced as fail-closed gates

## Layer 2 — Workflow Contract
### Required Artifacts
- smoke-test execution artifact with pass/fail status per critical stage
- run-manifest artifact with inputs, configuration fingerprint, and code version
- completion-status artifact indicating whether all required analysis outputs exist
- skill-refresh plan artifact: `outputs/report/skill_refresh_plan.json`
- skill-refresh log artifact: `outputs/report/skill_refresh_log.jsonl`
- skill-checkpoint status artifact: `outputs/report/skill_checkpoint_status.json`

### Acceptance Checks
- summary validation stage passes
- sample-registry and strategy stages pass
- at least one end-to-end mini-run stage passes
- fit and significance stages pass when workspace exists
- blinding, histogram, yield, cut-flow, and report artifacts are all present for completion
- reruns with same inputs/configuration produce consistent metadata fingerprints
- ROOT event-ingestion smoke check validates `uproot` availability/import
- for H->gammagamma resonance fitting, include a PyROOT/RooFit backend-specific smoke check and export the same standard fit/significance schemas
- skill-refresh artifacts exist and indicate pass status before handoff
- for H->gammagamma, smoke checks fail if primary fit/significance backend is anything other than RooFit analytic-function path
- if a mini-run is used after constructing/repairing missing runtime tooling, completion still requires a full-statistics production run in the same task

## Layer 3 — Example Implementation
### Smoke Tests (Current Repository)
1. `python -c "import uproot"`
2. `python -m analysis.config.load_summary --summary analysis/analysis.summary.json --out outputs/summary.normalized.json`
3. `python -m analysis.samples.registry --inputs inputs/ --summary analysis/analysis.summary.json --out outputs/samples.registry.json`
4. `python -m analysis.samples.strategy --registry outputs/samples.registry.json --regions analysis/regions.yaml --summary outputs/summary.normalized.json --out outputs/background_modeling_strategy.json`
5. `python -m analysis.stats.mass_model_selection --fit-id FIT1 --summary outputs/summary.normalized.json --hists outputs/hists --strategy outputs/background_modeling_strategy.json --out outputs/fit/FIT1/background_pdf_choice.json`
6. `python -m analysis.cli run --summary analysis/analysis.summary.json --inputs inputs/ --outputs outputs --max-events 20000 --samples <one_data_sample> <one_mc_sample>`
7. `python -c "import ROOT"`
8. `python -m analysis.stats.fit --workspace outputs/fit/workspace.json --fit-id FIT1 --out outputs/fit/FIT1/results.json`
9. `python -m analysis.stats.significance --workspace outputs/fit/workspace.json --fit-id FIT1 --out outputs/fit/FIT1/significance.json`
10. `python -m analysis.plotting.blinded_regions --outputs outputs --registry outputs/samples.registry.json --regions analysis/regions.yaml --fit-id FIT1`

### Reproducibility Notes (Current Repository)
- include config hash from normalized summary, regions config, and systematics config
- use stable file ordering and fixed seeds when sampling
- store run manifests under a dedicated run directory
- record fit backend in run metadata, with `pyroot_roofit` as primary for H->gammagamma workflows
- record cross-check backend outputs separately from primary outputs when optional non-ROOT cross-checks are run

# Examples

Example invocation context:
- `python -m analysis.config.load_summary --summary analysis/analysis.summary.json --out outputs/summary.normalized.json`
- `python -m analysis.samples.registry --inputs inputs/ --summary analysis/analysis.summary.json --out outputs/samples.registry.json`
- `python -m analysis.samples.strategy --registry outputs/samples.registry.json --regions analysis/regions.yaml --summary outputs/summary.normalized.json --out outputs/background_modeling_strategy.json`

Example expected outputs:
- `outputs/report/skill_refresh_plan.json`
- `outputs/report/skill_refresh_log.jsonl`
- `outputs/report/skill_checkpoint_status.json`
- `outputs/summary.normalized.json`
- `outputs/samples.registry.json`
- `outputs/background_modeling_strategy.json`
- `outputs/hists`
- `outputs/fit/FIT1/background_pdf_choice.json`
