---
skill_id: SKILL_BOOTSTRAP_REPO
display_name: "Bootstrap Repo"
version: 1.0
category: bootstrap

summary: "The analysis software foundation must support faithful propagation of physics intent from configuration to results."

invocation_keywords:
  - "bootstrap repo"
  - "bootstrap"
  - "repo"

when_to_use:
  - "Use when executing or validating the bootstrap stage of the analysis workflow."
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
  - name: analysis_package_scaffold_artifact_with_stage_oriented_modules
    type: artifact
    description: "analysis package scaffold artifact with stage-oriented modules"
  - name: stage_entrypoint_artifact_enabling_each_stage_to_run_independent
    type: artifact
    description: "stage entrypoint artifact enabling each stage to run independently"
  - name: end_to_end_orchestrator_artifact_that_executes_all_stages_consis
    type: artifact
    description: "end-to-end orchestrator artifact that executes all stages consistently"
  - name: minimal_test_artifact_that_verifies_package_integrity
    type: artifact
    description: "minimal test artifact that verifies package integrity"
  - name: runtime_recovery_artifact_documenting_constructed_restored_pipel
    type: artifact
    description: "runtime-recovery artifact documenting constructed/restored pipeline modules and tooling when initial runtime capability was missing"

preconditions:
  - "Dependency SKILL_HEP_ANALYSIS_ENV_SETUP has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_BOOTSTRAP_REPO are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_HEP_ANALYSIS_ENV_SETUP

  may_follow:
    - SKILL_HEP_ANALYSIS_ENV_SETUP

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
  - "writes analysis_package_scaffold_artifact_with_stage_oriented_modules"
  - "writes stage_entrypoint_artifact_enabling_each_stage_to_run_independent"
  - "writes end_to_end_orchestrator_artifact_that_executes_all_stages_consis"
  - "writes minimal_test_artifact_that_verifies_package_integrity"
  - "writes runtime_recovery_artifact_documenting_constructed_restored_pipel"

failure_modes:
  - "tests can be invoked and report pass/fail status"

validation_checks:
  - "repo runtime has been normalized before bootstrap via SKILL_HEP_ANALYSIS_ENV_SETUP or an explicitly documented equivalent path"
  - "stage entrypoints are executable"
  - "orchestrator entrypoint is discoverable and runnable"
  - "at least one validation stage executes from the orchestrator"
  - "tests can be invoked and report pass/fail status"
  - "if the repository initially lacked a functioning pipeline/tooling, bootstrap produces a runnable replacement path for required stages before handoff"
  - "bootstrapped event-ingestion path supports ROOT processing through `uproot`"
  - "H->gammagamma production pipeline is runnable with required PyROOT/RooFit backend support; non-resonance paths may remain runnable without PyROOT"

handoff_to:
  - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
  - SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY
  - SKILL_READ_SUMMARY_AND_VALIDATE
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/bootstrap_repo.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `core_pipeline/bootstrap_repo.md`
- Original stage: `bootstrap`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Bootstrap Repo

## Layer 1 — Physics Policy
The analysis software foundation must support faithful propagation of physics intent from configuration to results.

Policy requirements:
- Normalize the repo runtime before bootstrap so `.rootenv`, `PYTHONPATH`, and writable plotting caches are not rediscovered ad hoc.
- Separate analysis logic into clear stages so each physics decision is traceable.
- Keep infrastructure generic enough to support multiple channels and observables.
- Ensure the end-to-end pipeline can be rerun reproducibly.
- Avoid embedding analysis-specific thresholds directly in infrastructure code.
- If required pipeline modules or useful tooling are missing but buildable in-repository, construct/restore them as part of execution rather than stopping with placeholder-only artifacts.
- If an existing pipeline component is non-compliant with active skill requirements, rewrite only the owning component/module and preserve unaffected stages.
- Keep PyROOT dependencies isolated and available as a first-class requirement for H->gammagamma resonance-fit workflows.
- Keep ROOT event-ingestion dependencies centered on `uproot` for event processing.

## Layer 2 — Workflow Contract
### Required Artifacts
- analysis package scaffold artifact with stage-oriented modules
- stage entrypoint artifact enabling each stage to run independently
- end-to-end orchestrator artifact that executes all stages consistently
- minimal test artifact that verifies package integrity
- runtime-recovery artifact documenting constructed/restored pipeline modules and tooling when initial runtime capability was missing

### Acceptance Checks
- stage entrypoints are executable
- orchestrator entrypoint is discoverable and runnable
- at least one validation stage executes from the orchestrator
- tests can be invoked and report pass/fail status
- if the repository initially lacked a functioning pipeline/tooling, bootstrap produces a runnable replacement path for required stages before handoff
- if compliance gaps are detected, rewritten component(s) satisfy required skill acceptance checks without regressions in untouched stages
- bootstrapped event-ingestion path supports ROOT processing through `uproot`
- H->gammagamma production pipeline is runnable with required PyROOT/RooFit backend support; non-resonance paths may remain runnable without PyROOT

## Layer 3 — Example Implementation
### Required Structure (Current Repository)
```text
analysis/
  __init__.py
  cli.py
  config/
    __init__.py
    summary_schema.py
    load_summary.py
  samples/
    __init__.py
    registry.py
    weights.py
  io/
    __init__.py
    readers.py
    columnar.py
  objects/
    __init__.py
    photons.py
    jets.py
    leptons.py
  selections/
    __init__.py
    engine.py
    regions.py
  hists/
    __init__.py
    histmaker.py
  stats/
    __init__.py
    pyhf_workspace.py
    fit.py
  plotting/
    __init__.py
    plots.py
  report/
    __init__.py
    make_report.py
tests/
analysis/analysis.summary.json
analysis/regions.yaml
outputs/  (gitignored)
```

### CLI Convention (Current Repository)
- `python -m analysis.config.load_summary --summary analysis/analysis.summary.json`
- `python -m analysis.samples.registry --inputs inputs/ --summary analysis/analysis.summary.json`
- `python -m analysis.selections.regions --regions analysis/regions.yaml ...`
- `python -m analysis.cli run --summary ... --inputs ... --outputs ...`

### Acceptance Commands (Current Repository)
- `python -m analysis.cli --help`
- `python -m analysis.config.load_summary --summary analysis/analysis.summary.json`
- `pytest -q`

# Examples

Example invocation context:
- `python -m analysis.config.load_summary --summary analysis/analysis.summary.json`
- `python -m analysis.samples.registry --inputs inputs/ --summary analysis/analysis.summary.json`
- `python -m analysis.selections.regions --regions analysis/regions.yaml ...`

Example expected outputs:
- `analysis_package_scaffold_artifact_with_stage_oriented_modules`
- `stage_entrypoint_artifact_enabling_each_stage_to_run_independent`
- `end_to_end_orchestrator_artifact_that_executes_all_stages_consis`
- `minimal_test_artifact_that_verifies_package_integrity`
