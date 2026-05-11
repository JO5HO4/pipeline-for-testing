# VLQ Baseline Agent Guide

## Mission

Work on the `vlq_baseline` branch of `pipeline-for-testing`. The goal is to
carry out the lepton plus jets VLQ analysis as faithfully as the available open
data and local pipeline allow, then compare the result against the paper-derived
reference material in `.codex/`.

## Canonical Files

Use this as the only editable analysis JSON:

```text
analysis/leptons-bjet-vlq-search.json
```

`analysis/analysis.summary.json` is a compatibility symlink to the canonical
JSON. Do not create or commit `analysis/analysis.json` or another duplicate JSON
manifest unless the user explicitly asks for it.

Use these notes before changing selections, samples, normalizations, or claims:

- `.codex/knowledge.md`
- `.codex/paper_results.md`
- `.codex/13TeV25_details.md`

## Data Expectations

Before assuming a sample exists, check the local data areas:

```text
/global/cfs/projectdirs/atlas/haichen/opendata/1lepMET30/MC
/global/cfs/projectdirs/atlas/haichen/opendata/1lepMET30/Data
```

Document missing samples and analysis compromises in the final report. The paper
uses ingredients that are not fully recoverable from open event files, especially
for data-driven fake-lepton and charge-misidentification estimates, so keep those
claims explicit and bounded.

## Working Rules

- Prefer the repository's existing pipeline code and configuration patterns.
- Keep changes scoped to the analysis, notes, or outputs requested by the user.
- Validate JSON after edits.
- Compare produced yields, cutflows, and efficiencies to `.codex/paper_results.md`
  whenever possible.
- Report blockers as physics or data limitations, not as silent assumptions.
