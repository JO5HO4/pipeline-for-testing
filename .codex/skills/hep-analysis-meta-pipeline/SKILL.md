---
name: hep-analysis-meta-pipeline
description: Use when you want the refactored main HEP orchestration skill from this installed skill pack. This session-ready entrypoint loads the bundled HEP pipeline contracts for the current ATLAS Open Data H-to-gammagamma analysis project, covering runtime setup, sample preparation, selections, modeling, statistical stages, validation, and report or handoff flow.
---

# HEP Analysis Meta Pipeline

Use this as the single session-skill entrypoint for the refactored HEP workflow in the current analysis project.

## Quick Start

1. Read `references/patterns/pipelines/hep_analysis_meta_pipeline.md`.
2. Also read:
   - `references/patterns/shared/hep_domain_guardrails.md`
   - `references/patterns/shared/pipeline_logging_contract.md`
   - `references/patterns/shared/artifact_matrix.md`
   - `../hep-analysis-evaluation-scorecard/SKILL.md`
3. Load only the bundled local pattern file needed for the current stage or blocker.
4. Prefer the bundled local pattern files under `references/patterns/` over the legacy `.codex/skills/hep-meta-first/references/` contracts.

## Use This Skill For

- full end-to-end workflow orchestration
- stage-by-stage handoff planning
- deciding which reviewer or generator must run next
- deciding when sample semantics require intake, data-template, or likelihood-role review before modeling
- enforcing the refactored pipeline gates

## Stop Conditions

- a mandatory reviewer would be skipped
- a missing artifact would force guessed physics content
- a central-result policy would be violated by continuing
