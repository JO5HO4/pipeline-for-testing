# Artifact Integrity

Use when checking whether the final result is backed by complete, current, resolving artifacts.

## Required Inputs

- prompt or run request
- `outputs/evaluation_scorecard.json`
- `outputs/test_outcome_summary.json`
- sample registry
- sample exclusion reasons
- progress or processed-sample artifact
- production run manifest
- data provenance artifact
- feasibility or reference-contract artifact
- claim classification
- report-number trace
- finalization gate
- final report
- reproducibility commands
- root-runtime repair attempts when ROOT-backed capability was required or missing

## Checks

- All paths are repo-root-relative and resolve.
- Scorecard and test summary agree on final status, handoff, paper-level permission, and diagnostic scope.
- Registered, usable, processed, and excluded sample counts agree across artifacts.
- Excluded samples have explicit reasons.
- Final report source is the final uncapped production run, or it is explicitly blocked/diagnostic.
- Runtime repair attempts exist when a ROOT-backed backend was needed but unavailable.
- Reproducibility commands identify the same summary, inputs, outputs, event cap, unblinding state, and backend used for the final artifacts.

## Veto Conditions

- Missing or contradictory scorecard/test summary.
- Missing sample-scope definition or excluded-sample reasons.
- Missing root-runtime repair artifact for a ROOT-backed fallback.
- Artifact paths that only work relative to `outputs/` instead of the repository root.
- Final report sourced from a smoke/capped/partial run without explicit partial-only scope.
