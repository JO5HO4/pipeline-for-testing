# VLQ Multiagent Test Pipeline

This branch is the multiagent starting point for Codex/Claude runs on the ATLAS open-data same-charge leptons plus b-jets reinterpretation. It is built from the April 29 VLQ workspace and cleaned so the VLQ task summary is the only active analysis target, using the multiagent coordination package without the final quality-review package.

## Branch Role

- Branch: `vlq_multiagent`
- Skill package: baseline/refactored HEP analysis skills, ROOT runtime repair, and multiagent coordination under `.codex/skills/`
- Agent mode: coordinator plus delegated workers/reviewers when useful
- Reference target: `analysis/leptons-bjet-vlq-search.json`

## What Is Included

- `analysis/vlq_pipeline.py`: the runnable VLQ-style analysis pipeline
- `analysis/analysis.summary.json`: symlink to the VLQ reference summary
- `analysis/samples/metadata.py`: ROOT sample metadata helpers used by the pipeline
- `input-data/`: symlink to the 1lepMET30 open-data ROOT samples
- `prompt.txt`: multiagent task prompt for the run coordinator
- `tests/`: portable checks for the VLQ branch contract

Generated products belong under `outputs/`; report exports under `reports/` are ignored by git.

## Install

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -e '.[dev]'
```

## Common Entrypoints

```bash
vlq-analysis bootstrap --summary analysis/analysis.summary.json --outputs outputs/bootstrap
vlq-analysis preflight --summary analysis/analysis.summary.json --inputs input-data --outputs outputs/preflight
vlq-analysis run --summary analysis/analysis.summary.json --inputs input-data --outputs outputs/vlq
```

For a quick code check:

```bash
pytest
```
