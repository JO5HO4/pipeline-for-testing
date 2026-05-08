---
name: hep-pipeline-skill-compliance-audit
description: Use when auditing an existing HEP analysis pipeline or generated run artifacts for noncompliance with the binding HEP skills before fit/significance handoff or final report approval, especially to catch diagnostic-only implementations being used for central claims.
---

# HEP Pipeline Skill Compliance Audit

Use this skill when the task is to compare the executable pipeline against the skills that govern its claims.

## Quick Start

1. Read `../hep-analysis-pipelines/references/patterns/reviewers/pipeline_skill_compliance_auditor.md`.
2. Also read the governing skill or pattern files for the claim under audit, such as:
   - `../hep-analysis-pipelines/references/patterns/tool_wrappers/fit_and_significance_wrapper.md`
   - `../hep-analysis-pipelines/references/patterns/reviewers/statistical_readiness_reviewer.md`
   - `../hep-analysis-pipelines/references/patterns/reviewers/data_mc_discrepancy_reviewer.md`
   - `../hep-analysis-pipelines/references/patterns/reviewers/likelihood_sample_role_reviewer.md`
   - `../hep-analysis-pipelines/references/patterns/reviewers/nominal_sample_and_normalization_reviewer.md`
3. Write a compliance artifact, usually `outputs/report/pipeline_skill_compliance_audit.json`.
4. Treat any `noncompliant_blocking` finding as a hard stop for central claims.

## What This Skill Covers

- claim-to-skill mapping
- code-path and artifact provenance checks
- static inspection for forbidden or diagnostic-only implementation modes
- report-scope checks that blocked diagnostics were not promoted
- same-sign and multilepton checks that raw reducible MC proxies were not promoted to central expected background without reviewed data-driven, hybrid, or closure-backed evidence

## Stop Conditions

- a central claim lacks a governing-skill map
- executable code path evidence is missing
- an artifact's metadata contradicts the skill contract
- a diagnostic-only method supports a central report claim
- a same-sign or multilepton report labels raw reducible `ttbar` or jets MC as central expected background without a prompt/reducible split and reviewed promotion evidence
