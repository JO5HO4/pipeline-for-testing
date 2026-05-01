# Codex Skills Index

This runtime pack is generated from `skill_src/` by `scripts/build_runtime_skills.py`.

Canonical entry:

- `$hep-analysis-meta-pipeline`

Generated runtime skill packages:

- `hep-analysis-meta-pipeline`: main HEP orchestration entrypoint
- `hep-analysis-pipelines`: pipeline-focused entry skill
- `hep-analysis-inversions`: decision and routing entry skill
- `hep-analysis-generators`: artifact-generation entry skill
- `hep-analysis-reviewers`: validation and gate entry skill
- `hep-analysis-tool-wrappers`: repository command and workflow wrapper entry skill
- `hep-analysis-env-setup`: runtime environment setup helper
- `hep-root-runtime-repair`: ROOT/PyROOT/RooFit runtime discovery and repair gate before diagnostic fallback
- `hep-analysis-evaluation-scorecard`: shared run-quality scorecard required for baseline and multiagent testing
- `hep-meta-first`: preserved legacy single-entry pack
- `hep-final-quality-review`: general final HEP quality gate for artifacts, statistics, plots, number trace, claim scope, and handoff
- `multiagent-hep-coordination`: single package-style multiagent coordination entrypoint with staged delegation, review, repair, and handoff references

Refactored runtime skills are self-contained.
Each one bundles its local pattern references under:

- `references/patterns/`

The legacy `hep-meta-first` pack is preserved for comparison and migration history.
