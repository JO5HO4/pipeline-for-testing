---
name: hep-analysis-reviewers
description: Use when you need the refactored HEP reviewer skills from this installed skill pack to judge whether a stage in the current analysis project is actually acceptable. This covers preflight fact checks, nominal-sample and normalization validation, likelihood sample-role validation, blinding and visualization checks, statistical readiness, data-MC discrepancy review, and reproducibility or handoff gates.
---

# HEP Analysis Reviewers

Use this skill when the task is to validate a stage, block unsafe progression, or certify handoff readiness.

## Quick Start

1. Read only the bundled reviewer reference that matches the current gate:
   - `references/patterns/reviewers/preflight_fact_check_reviewer.md`
   - `references/patterns/reviewers/analysis_summary_reviewer.md`
   - `references/patterns/reviewers/nominal_sample_and_normalization_reviewer.md`
   - `references/patterns/reviewers/likelihood_sample_role_reviewer.md`
   - `references/patterns/reviewers/blinding_and_visualization_reviewer.md`
   - `references/patterns/reviewers/statistical_readiness_reviewer.md`
   - `references/patterns/reviewers/data_mc_discrepancy_reviewer.md`
   - `references/patterns/reviewers/reproducibility_and_handoff_reviewer.md`
2. Pair the reviewer with:
   - `references/patterns/shared/review_rubric.md`
   - `references/patterns/shared/evidence_requirements.md`
   - `../hep-analysis-evaluation-scorecard/SKILL.md` when finalization, handoff, or claim scope is affected
3. When a reviewer blocks, route to the smallest matching inversion or generator instead of rerunning everything.

## What This Skill Covers

- factual readiness before execution
- schema and partition consistency
- nominal sample and normalization validity
- likelihood sample-role and data-template boundary validity
- blinding and plot correctness
- statistical-readiness gates
- discrepancy handling
- reproducibility and final handoff gates

## Stop Conditions

- reviewer evidence is missing
- the run would advance without a mandatory gate
- the only possible conclusion would rely on inference rather than artifacts
