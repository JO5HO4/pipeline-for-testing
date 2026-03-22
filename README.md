# H->gammagamma Analysis Pipeline

This repository packages the standalone `analysis/` code for the ATLAS open-data Higgs-to-diphoton workflow. It contains the modular pipeline, configuration assets, and a small portable test suite extracted from the larger analysis workspace.

## What is included

- `analysis/`: the analysis package, including CLI entrypoints, histogramming, selection logic, statistical modeling, plotting, and report generation
- `analysis/analysis.summary.json`: example normalized-analysis input summary
- `analysis/Higgs-to-diphoton.json`: reference problem description
- `analysis/regions.yaml`: generated region configuration
- `tests/`: portable tests for summary normalization and reporting artifact contracts

## Prerequisites

Core Python dependencies are handled by `pyproject.toml`, but the statistical stages also require CERN ROOT with PyROOT and RooFit available in the runtime environment. That dependency is not installed through pip here.

For lightweight development work that does not execute RooFit stages, a standard virtual environment is enough. For full pipeline execution, use a Python environment where `import ROOT` succeeds. The runtime prefers a repo-local `.rootenv` when present, but it now falls back to the active interpreter if that interpreter already provides PyROOT.

## Install

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -e '.[dev]'
```

## Common entrypoints

```bash
hgg-load-summary --summary analysis/analysis.summary.json --out outputs/summary.normalized.json
hgg-preflight --summary analysis/analysis.summary.json --inputs /path/to/input-data --outputs outputs
hgg-analysis run --summary analysis/analysis.summary.json --inputs /path/to/input-data --outputs outputs
```

You can also invoke the modules directly with `python -m analysis.<module>`.

## Development

Run the portable tests with:

```bash
pytest
```

The extracted repository intentionally omits the workspace-specific test that asserted the presence of an existing `.rootenv`, because that assumption does not hold in a fresh standalone checkout.
