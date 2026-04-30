---
name: hep-analysis-inversions
description: "Use when you need the refactored HEP inversion skills from this installed skill pack: blocker routing, signal-signature and likelihood intake, sample-strategy branching, blinding and fit-policy decisions, or failure-to-skill diagnosis for the current analysis project."
---

# HEP Analysis Inversions

Use this skill when the workflow is blocked on a decision rather than on a command.

## Quick Start

1. Read `references/patterns/inversions/analysis_router_inversion.md` for blocker-to-next-skill routing.
2. Read `references/patterns/inversions/signal_signature_and_likelihood_intake_inversion.md` when sample roles or allowed data-template usage are underspecified.
3. Read `references/patterns/inversions/sample_strategy_inversion.md` for background relevance, nominal sample, alternative-sample, and normalization-mode decisions.
4. Read `references/patterns/inversions/blinding_and_fit_policy_inversion.md` for blinding, backend, smoothing, and significance-policy decisions.
5. Read `references/patterns/inversions/failure_to_skill_inversion.md` when a reviewer has already found a recurring failure or capability gap.
6. Use `references/patterns/shared/decision_record_template.md` for every non-trivial branch.

## What This Skill Covers

- routing from missing artifact to next skill
- signal-signature and likelihood-role intake
- nominal sample and background-strategy branching
- blinding and backend eligibility decisions
- failure classification and skill extraction

## Stop Conditions

- the required evidence for a branch is missing
- a human approval is needed for unblinding or central-result override
- the decision would promote a cross-check into a central claim
