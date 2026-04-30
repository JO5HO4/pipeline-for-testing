---
skill_id: SKILL_HEP_ANALYSIS_ENV_SETUP
display_name: "HEP Analysis Environment Setup"
version: 1.0
category: bootstrap

summary: "Before bootstrap, tests, smoke runs, or fit execution, normalize the repository runtime by selecting the workspace-local interpreter, exporting repo-local Python/cache environment variables, and verifying PyROOT/RooFit plus required inputs."

invocation_keywords:
  - "hep analysis environment setup"
  - "environment setup"
  - "runtime"
  - "rootenv"
  - "pyroot"
  - "roofit"
  - "pytest"
  - "smoke"

when_to_use:
  - "Use when starting cold in this repository or after shell/import failures."
  - "Use before the first repo command that runs `pytest`, `analysis.cli`, fit/significance code, or ad hoc HEP studies."
  - "Use when this context is available: repository paths and runtime context for the current run."

when_not_to_use:
  - "Do not use when the repo runtime has already been verified in the current shell and no environment drift is suspected."

inputs:
  required:
    - name: repository_paths_and_runtime_context_for_the_current_run
      type: artifact
      description: "repository paths and runtime context for the current run"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional host-specific runtime notes."

outputs:
  - name: runtime_environment_readiness_state
    type: artifact
    description: "runtime-environment readiness state"
  - name: repo_runtime_wrapper_command_pattern
    type: artifact
    description: "repo-runtime wrapper command pattern"
  - name: writable_plot_cache_setup_state
    type: artifact
    description: "writable plot-cache setup state"

preconditions:
  - "Required inputs are present and readable."

postconditions:
  - "Runtime choice, cache setup, and PyROOT/RooFit readiness have been checked before downstream execution."

dependencies:
  requires:
    - NONE

  may_follow:
    - NONE

allowed_tools:
  - Read
  - Write
  - Edit
  - Bash

allowed_paths:
  - .codex/skills/hep-analysis-env-setup/
  - analysis/
  - input-data/
  - outputs*/
  - reports/
  - skills/
  - newskills/

side_effects:
  - "verifies workspace-local runtime and PyROOT/RooFit availability"
  - "normalizes wrapper command patterns for tests, preflight, smoke runs, and ad hoc studies"

failure_modes:
  - "if `.rootenv` is missing or `import ROOT` fails, primary H->gammagamma execution is blocked until runtime is repaired or an explicitly documented equivalent runtime is provided"

validation_checks:
  - "workspace-local `.rootenv/bin/python` exists or an explicitly documented equivalent runtime is provided"
  - "`analysis/analysis.summary.json` exists"
  - "`input-data/data` and `input-data/MC` exist"
  - "PyROOT/RooFit import succeeds in the chosen runtime"
  - "repo-local writable cache directories are created or already writable"

handoff_to:
  - SKILL_BOOTSTRAP_REPO
  - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
  - SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY
---

# Purpose

This contract routes cold-start runtime normalization through the reusable sibling skill at `../../hep-analysis-env-setup/`.

# Procedure

1. Verify the workspace runtime before the first repo command.
2. Use the env-wrapper command pattern for tests, bootstrap, preflight, smoke runs, and ad hoc studies.
3. Block primary H->gammagamma execution if PyROOT/RooFit is unavailable.

# Notes

- Source skill: `../../hep-analysis-env-setup/SKILL.md`
- Reusable scripts:
  - `../../hep-analysis-env-setup/scripts/check_repo_env.sh`
  - `../../hep-analysis-env-setup/scripts/run_in_repo_env.sh`
- Reusable reference:
  - `../../hep-analysis-env-setup/references/command-recipes.md`

## Layer 1 — Runtime Policy

- Prefer the workspace-local `.rootenv` interpreter for this repository.
- Export repo-local `PYTHONPATH` so `import analysis` works consistently.
- Export writable `MPLCONFIGDIR` and `XDG_CACHE_HOME` under the workspace to avoid plotting-cache permission failures.
- Treat `analysis/analysis.summary.json` as the canonical summary entrypoint.
- Expect `skills/metadata.csv` to be reconstructed in-task from ROOT metadata branches when the official metadata CSV is absent.
- On a different host, do not assume a copied `.rootenv` is portable; rebuild or document an equivalent runtime before continuing.

## Layer 2 — Example Commands

```bash
../../hep-analysis-env-setup/scripts/check_repo_env.sh .
../../hep-analysis-env-setup/scripts/run_in_repo_env.sh . -- pytest -q
../../hep-analysis-env-setup/scripts/run_in_repo_env.sh . -- python -m analysis.preflight --summary analysis/Higgs-to-diphoton.json --inputs input-data --outputs outputs_preflight
```
