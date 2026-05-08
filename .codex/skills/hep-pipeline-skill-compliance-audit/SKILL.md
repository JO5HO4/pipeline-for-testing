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
4. For VLQ-style same-sign or trilepton analyses, run the deterministic scope guard before any plot, report, fit, significance, or central-yield claim consumes aggregate yields:

```bash
python .codex/skills/hep-pipeline-skill-compliance-audit/scripts/vlq_scope_guard.py --repo .
```

5. Treat any `noncompliant_blocking` finding or guard `BLOCKED` outcome as a hard stop for central claims.

## What This Skill Covers

- claim-to-skill mapping
- code-path and artifact provenance checks
- static inspection for forbidden or diagnostic-only implementation modes
- report-scope checks that blocked diagnostics were not promoted
- same-sign and multilepton checks that raw reducible MC proxies were not promoted to central expected background without reviewed data-driven, hybrid, or closure-backed evidence
- deterministic VLQ scope checks that central stacks use only `central_sample: true`, material data-MC discrepancies have an audit, weak signal proxies are classified, and report labels do not overclaim diagnostic MC stacks

## Stop Conditions

- a central claim lacks a governing-skill map
- executable code path evidence is missing
- an artifact's metadata contradicts the skill contract
- a diagnostic-only method supports a central report claim
- a same-sign or multilepton report labels raw reducible `ttbar` or jets MC as central expected background without a prompt/reducible split and reviewed promotion evidence
- `outputs/report/vlq_scope_guard.json` is missing or has `gate_outcome: BLOCKED` before VLQ plot, report, fit, significance, or central-yield handoff
