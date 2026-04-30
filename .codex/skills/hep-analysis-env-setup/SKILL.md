---
name: hep-analysis-env-setup
description: Prepare the current analysis project for ATLAS Open Data H-to-gammagamma work by selecting the project-local `.rootenv` interpreter, exporting project-local `PYTHONPATH`, configuring writable Matplotlib and fontconfig caches, and verifying PyROOT, RooFit, and required inputs before tests or pipeline runs.
---

# HEP Analysis Env Setup

Use this skill before the first command in the current analysis project, after shell or import failures, or when a fresh agent needs a runnable HEP analysis environment quickly.

## Quick Start

1. Run `scripts/check_repo_env.sh <workspace>` to verify `.rootenv`, PyROOT/RooFit, the summary entrypoint, and the input directories.
2. Run repo commands through `scripts/run_in_repo_env.sh <workspace> -- <command...>`.
3. For `H -> gamma gamma` primary fits, stop if PyROOT/RooFit is unavailable. Do not substitute a non-ROOT backend as the primary path.

## What This Skill Normalizes

- Prepend `<workspace>/.rootenv/bin` to `PATH` so `python` and `pytest` resolve inside the workspace runtime.
- Export `PYTHONPATH=<workspace>` so `import analysis` works during tests and CLI runs.
- Export `MPLCONFIGDIR=<workspace>/.cache/matplotlib` and `XDG_CACHE_HOME=<workspace>/.cache` so plotting does not spend time failing on unwritable cache directories.
- Treat `analysis/analysis.summary.json` as the canonical summary entrypoint. In this repo it points to `analysis/Higgs-to-diphoton.json`.
- Verify `input-data/data` and `input-data/MC` before starting a run.
- Expect the runtime to reconstruct a metadata CSV artifact when the official metadata file is absent. Some repository versions still use the legacy path `skills/metadata.csv`; if that directory has been removed, patch or override the runtime path before running.

## Standard Flow

1. Run `scripts/check_repo_env.sh <workspace>`.
2. Use `scripts/run_in_repo_env.sh <workspace> -- ...` for tests, preflight, smoke runs, and ad hoc studies.
3. If blocked, inspect `outputs*/report/runtime_recovery.json` and `outputs*/report/preflight_fact_check.json`.
4. If running a smoke pipeline, use a fresh `outputs_smoke_*` directory and read `references/command-recipes.md` for repo-specific caveats.

## Resources

- `scripts/check_repo_env.sh`: fast readiness check for this repo
- `scripts/run_in_repo_env.sh`: command wrapper that enters the normalized repo environment
- `references/command-recipes.md`: copy-paste command patterns and known gotchas

## Stop Conditions

- `<workspace>/.rootenv/bin/python` is missing
- `import ROOT` fails inside `.rootenv`
- `analysis/analysis.summary.json` is missing
- `input-data/data` or `input-data/MC` is missing
