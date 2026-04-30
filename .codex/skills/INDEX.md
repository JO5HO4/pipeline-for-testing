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
- `hep-meta-first`: preserved legacy single-entry pack

Refactored runtime skills are self-contained.
Each one bundles its local pattern references under:

- `references/patterns/`

The legacy `hep-meta-first` pack is preserved for comparison and migration history.
