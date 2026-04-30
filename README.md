# Testing Pipeline Main Setup

This branch is the normal shared setup for the April 30 testing pipeline repository. It carries the standard ATLAS open-data Higgs-to-diphoton scaffold that the Hyy test branches are based on.

## What Is Included

- `analysis/`: modular diphoton analysis package with CLI, selections, histogramming, fits, plotting, and report helpers
- `analysis/analysis.summary.json`: symlink to `analysis/Higgs-to-diphoton.json`
- `analysis/regions.yaml`: generated region configuration used by the pipeline
- `input-data/`: symlink to the open-data ROOT samples
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
