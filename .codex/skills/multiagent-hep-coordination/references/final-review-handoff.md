# Final Review and Handoff

Use this reference after finalization.

## Final Artifact Review

Spawn a fresh independent final artifact reviewer. The reviewer must inspect:

- prompt/run request;
- `analysis_state.json`;
- `codex_sessions.json`;
- scorecard and test outcome summary;
- root runtime repair attempts when relevant;
- data provenance;
- feasibility/reference contract;
- production manifest, progress, sample registry, and exclusion reasons;
- yields, statistics, plots, plot manifest;
- claim classification and report-number trace;
- finalization gate;
- final report;
- reproducibility commands.

The artifact reviewer must fail if artifacts are missing, stale, contradictory, non-reproducible, or sourced from a smoke/capped/partial run promoted as final.

## Final Claim Review

Spawn a separate final claim reviewer after artifact review passes. The reviewer must inspect final report wording, captions, headline numbers, tables, conclusions, and claim scope.

When `hep-final-quality-review` is installed, use its modules for:

- artifact integrity;
- statistical quality;
- number trace;
- plot/caption review;
- claim scope.

When it is not installed, the final artifact and claim reviewers must still cover the same topics using this package's review contracts and the required inputs above.

## Handoff

Set handoff allowed only when:

- final artifact review has no veto;
- final claim review has no veto;
- scorecard and test outcome summary agree;
- report tone matches the weakest valid claim classification;
- all required repair cycles are complete.
