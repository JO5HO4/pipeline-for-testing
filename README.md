# VLQ Quality Review Test Pipeline

This branch is the single-agent baseline plus final quality-review starting point for Codex/Claude runs on the ATLAS open-data same-charge leptons plus b-jets reinterpretation. It is built from the April 29 VLQ workspace and cleaned so the VLQ task summary is the only active analysis target, using the final quality-review package without the multiagent coordination package.

## Branch Role

- Branch: `vlq_quality_review`
- Skill package: baseline/refactored HEP analysis skills, ROOT runtime repair, and final quality review under `.codex/skills/`
- Agent mode: one session, no delegated subagents
- Reference target: `analysis/leptons-bjet-vlq-search.json`

## What Is Included

- `analysis/vlq_pipeline.py`: the runnable VLQ-style analysis pipeline
- `analysis/analysis.summary.json`: symlink to the VLQ reference summary
- `analysis/samples/metadata.py`: ROOT sample metadata helpers used by the pipeline
- `input-data/`: symlink to the 1lepMET30 open-data ROOT samples
- `prompt.txt`: baseline task prompt for the run agent
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
