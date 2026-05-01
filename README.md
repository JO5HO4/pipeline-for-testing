# Hyy Multiagent Test Pipeline

This branch is the multiagent starting point for Codex/Claude runs on the ATLAS open-data Higgs-to-diphoton workflow. It keeps the normal diphoton scaffold, reference summary, portable checks, and multiagent coordination package without the final quality-review package.

## Branch Role

- Branch: `hyy_multiagent`
- Skill package: baseline/refactored HEP analysis skills, ROOT runtime repair, and multiagent coordination under `.codex/skills/`
- Agent mode: coordinator plus delegated workers/reviewers when useful
- Reference target: `analysis/Higgs-to-diphoton.json`

## What Is Included

- `analysis/`: modular diphoton analysis package with CLI, selections, histogramming, fits, plotting, and report helpers
- `analysis/analysis.summary.json`: symlink to the diphoton reference summary
- `analysis/regions.yaml`: generated region configuration used by the pipeline
- `input-data/`: symlink to the open-data ROOT samples
- `prompt.txt`: multiagent task prompt for the run coordinator
- `tests/`: portable checks for summary normalization and reporting contracts

Generated products belong under `outputs/`; report exports under `reports/` are ignored by git.

## Install

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -e '.[dev]'
```

The fit stages require a Python environment with PyROOT/RooFit. Lightweight checks that do not run fits can use a standard virtual environment.

## Common Entrypoints

```bash
hgg-load-summary --summary analysis/analysis.summary.json --out outputs/summary.normalized.json
hgg-preflight --summary analysis/analysis.summary.json --inputs input-data --outputs outputs/preflight
hgg-analysis run --summary analysis/analysis.summary.json --inputs input-data --outputs outputs/hyy
```

For a quick code check:

```bash
pytest
```
