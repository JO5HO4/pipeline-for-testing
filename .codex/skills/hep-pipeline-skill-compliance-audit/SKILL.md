---
name: hep-pipeline-skill-compliance-audit
description: Use when auditing an existing HEP analysis pipeline or generated run artifacts for noncompliance with the binding HEP skills before fit/significance handoff or final report approval, especially to catch diagnostic-only implementations being used for central claims.
---

# HEP Pipeline Skill Compliance Audit

Use this skill when the task is to compare the executable pipeline against the skills that govern its claims.

## Quick Start

1. For pre-fit or pre-significance gating, run the deterministic guard before any statistical command:

   ```bash
   python .codex/skills/hep-pipeline-skill-compliance-audit/scripts/pre_fit_compliance_guard.py \
     --summary analysis/analysis.summary.json \
     --repo .
   ```

   This writes `outputs/report/pipeline_skill_compliance_audit.json` with `scope: pre_fit` and exits nonzero on blocking findings.
2. Read `../hep-analysis-pipelines/references/patterns/reviewers/pipeline_skill_compliance_auditor.md`.
3. Also read the governing skill or pattern files for the claim under audit, such as:
   - `../hep-analysis-pipelines/references/patterns/tool_wrappers/fit_and_significance_wrapper.md`
   - `../hep-analysis-pipelines/references/patterns/reviewers/statistical_readiness_reviewer.md`
   - `../hep-analysis-pipelines/references/patterns/reviewers/data_mc_discrepancy_reviewer.md`
   - `../hep-analysis-pipelines/references/patterns/reviewers/likelihood_sample_role_reviewer.md`
   - `../hep-analysis-pipelines/references/patterns/reviewers/nominal_sample_and_normalization_reviewer.md`
4. Write a compliance artifact, usually `outputs/report/pipeline_skill_compliance_audit.json`.
5. Treat any `noncompliant_blocking` finding as a hard stop for central claims.

## What This Skill Covers

- claim-to-skill mapping
- code-path and artifact provenance checks
- static inspection for forbidden or diagnostic-only implementation modes
- report-scope checks that blocked diagnostics were not promoted
- same-sign and multilepton checks that raw reducible MC proxies were not promoted to central expected background without reviewed data-driven, hybrid, or closure-backed evidence

## Deterministic Pre-Fit Guard

The bundled `scripts/pre_fit_compliance_guard.py` is an executable precondition, not an LLM review. It statically inspects:

- `analysis/stats/fit.py`
- `analysis/stats/significance.py`
- `analysis/stats/models.py`
- planned or known metadata artifacts under `outputs/**` when present

It blocks central H to gammagamma expected-significance paths when it finds weighted bin-center `RooDataSet` Asimov construction, extended unbinned weighted RooFit on that data, a central Asimov mode outside `direct_generation`, `binned_roodatahist`, or `binned_poisson`, or inconsistent observed-count/template-yield provenance for central Asimov generation.

The guard result is binding. A post-run audit can diagnose damage, but it cannot satisfy this pre-fit precondition.

## Stop Conditions

- a central claim lacks a governing-skill map
- executable code path evidence is missing
- an artifact's metadata contradicts the skill contract
- a diagnostic-only method supports a central report claim
- a same-sign or multilepton report labels raw reducible `ttbar` or jets MC as central expected background without a prompt/reducible split and reviewed promotion evidence
- a statistical stage capable of central claims is run without a passing `scope: pre_fit` guard artifact
