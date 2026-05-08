---
name: hep-analysis-meta-pipeline
description: Use when you want the refactored main HEP orchestration skill from this installed skill pack. This session-ready entrypoint loads the bundled HEP pipeline contracts for the current ATLAS Open Data H-to-gammagamma analysis project, covering runtime setup, sample preparation, selections, modeling, statistical stages, validation, and report or handoff flow.
---

# HEP Analysis Meta Pipeline

Use this as the single session-skill entrypoint for the refactored HEP workflow in the current analysis project.

## Quick Start

1. Before executing any end-to-end run that can reach Stage 7, run the pipeline skill compliance auditor in `pre_fit` mode. If the artifact is missing or its `gate_outcome` is not `PASS` or an explicitly allowed `CONDITIONAL_PASS`, do not run the pipeline.
2. Read `references/patterns/pipelines/hep_analysis_meta_pipeline.md`.
3. Also read:
   - `references/patterns/shared/hep_domain_guardrails.md`
   - `references/patterns/shared/pipeline_logging_contract.md`
   - `references/patterns/shared/artifact_matrix.md`
4. Load only the bundled local pattern file needed for the current stage or blocker.
5. Prefer the bundled local pattern files under `references/patterns/` over the legacy `.codex/skills/hep-meta-first/references/` contracts.

## Hard Stop: Pre-Fit Compliance

A pipeline may not execute a statistical stage capable of producing central claims unless the planned executable code path has already passed compliance audit.

Before any `analysis.cli run` invocation that can reach fit/significance, or before any direct fit/significance command, run:

```bash
python .codex/skills/hep-pipeline-skill-compliance-audit/scripts/pre_fit_compliance_guard.py \
  --summary analysis/analysis.summary.json \
  --repo .
```

The guard must write a `scope: pre_fit` compliance artifact, normally `outputs/report/pipeline_skill_compliance_audit.json`. If the artifact is missing, stale, `BLOCKED`, or `ESCALATED`, stop. `CONDITIONAL_PASS` may continue only when the condition explicitly downgrades the affected statistical path to diagnostic-only or confirms that no central statistical stage will run.

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
- the pre-fit compliance audit artifact is missing or does not allow the planned statistical stage
