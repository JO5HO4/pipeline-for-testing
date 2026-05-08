# Command Recipes

## Quick Check

```bash
./.codex/skills/hep-analysis-env-setup/scripts/check_repo_env.sh .
```

## Unit Tests

```bash
./.codex/skills/hep-analysis-env-setup/scripts/run_in_repo_env.sh . -- pytest -q
```

## Preflight

```bash
./.codex/skills/hep-analysis-env-setup/scripts/run_in_repo_env.sh . -- \
  python -m analysis.preflight \
  --summary analysis/Higgs-to-diphoton.json \
  --inputs input-data \
  --outputs outputs_preflight
```

## Smoke Statistics Run

```bash
./.codex/skills/hep-analysis-env-setup/scripts/run_in_repo_env.sh . -- \
  python -m analysis.cli run \
  --summary analysis/Higgs-to-diphoton.json \
  --inputs input-data \
  --outputs outputs_smoke_env_check \
  --max-events 20000
```

## Ad Hoc Smoothing Study

```bash
./.codex/skills/hep-analysis-env-setup/scripts/run_in_repo_env.sh . -- \
  python -m analysis.ad_hoc_smoothing_method_study \
  --outputs outputs \
  --fit-id FIT1
```

## Repo-Specific Gotchas

- Use the workspace-local `.rootenv` as the default runtime for all `H -> gamma gamma` work. Primary fit and significance stages require PyROOT/RooFit.
- Use the wrapper script instead of raw `pytest` or `python` so `PYTHONPATH`, `MPLCONFIGDIR`, and `XDG_CACHE_HOME` are set consistently.
- The pipeline should use the bundled ATLAS Open Data metadata CSV as the normalization authority. If it writes `skills/metadata.csv`, that file must be generated from the official table; ROOT metadata branches are diagnostics only for skimmed datasets.
- Smoke runs currently write shared files under `reports/` through `analysis/report/make_report.py`. If a smoke run rewrites the main report view, restore it from `outputs/report/report.md`.
- The first diagnostics to inspect for environment problems are `outputs*/report/runtime_recovery.json` and `outputs*/report/preflight_fact_check.json`.
