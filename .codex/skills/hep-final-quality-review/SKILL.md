---
name: hep-final-quality-review
description: "Use when reviewing, finalizing, or handing off any HEP analysis result. Provides a general final quality gate for artifact integrity, sample accounting, statistical validity, plot/caption accuracy, number traceability, claim scope, reproducibility, and scorecard/test-summary consistency across baseline or multiagent runs."
---

# HEP Final Quality Review

Use this skill before final handoff of any HEP analysis, whether the result is paper-level, reinterpretation, diagnostic-only, blocked, or failed.

## Core Contract

- Treat review as adversarial: successful execution is not enough.
- Review the final report together with machine-readable source artifacts.
- Verify that every printed result is traceable, every claim is allowed, and every limitation is visible.
- For baseline runs, this may be a local final self-review saved under `outputs/report/`.
- For multiagent runs, this should be a fresh independent final reviewer, separate from implementation workers and earlier reviewers.

## Required Output

Write a review artifact:

- Baseline default: `outputs/report/final_quality_review.json`
- Multiagent default: `reviews/final_quality_review/review_<cycle>.json`

The review artifact must include:

```json
{
  "schema_version": "hep_final_quality_review.v1",
  "stage": "FINAL_QUALITY_REVIEW",
  "status": "PASS|CONDITIONAL_PASS|FAIL",
  "handoff_allowed": false,
  "paper_level_claims_allowed": false,
  "diagnostic_claims_allowed": true,
  "artifacts_reviewed": {
    "files": [],
    "plots": []
  },
  "checks": [
    {
      "check": "scorecard|sample_scope|runtime|statistics|number_trace|plot_caption|claim_scope|reproducibility|final_report",
      "status": "PASS|WARNING|PROBLEM",
      "issue": ""
    }
  ],
  "veto_findings": [],
  "warning_findings": [],
  "required_repairs": [],
  "rerun_required_from_stage": "none",
  "summary": ""
}
```

## Review Modules

Load only the reference file needed for the current review question:

- [artifact-integrity.md](references/artifact-integrity.md): scorecard, test summary, paths, sample accounting, runtime repair, reproducibility.
- [statistical-quality.md](references/statistical-quality.md): likelihoods, fits, limits, significance, signed yields, systematics, expected/observed ordering.
- [number-trace.md](references/number-trace.md): report-number trace requirements and table/value coverage.
- [plot-caption.md](references/plot-caption.md): plot existence, blinding, visual sanity, captions, and diagnostic wording.
- [claim-scope.md](references/claim-scope.md): final wording, paper-level vs diagnostic vs blocked claims, substitution boundaries.

## Mandatory Vetoes

Record `PROBLEM` and set `handoff_allowed: false` when any apply:

- `outputs/evaluation_scorecard.json` or `outputs/test_outcome_summary.json` is missing, stale, contradictory, or has unresolved paths.
- Sample counts disagree between scorecard, registry, progress, manifest, and exclusion reasons.
- A ROOT-backed backend was required or missing, but fallback/blocking lacks a runtime repair-attempt artifact.
- A smoke, capped, partial, failed, or still-running run is promoted as final production.
- A final report number or table cell lacks a resolving source in the report-number trace.
- A statistic affected by proxy samples, missing nuisance model, signed/negative yield stabilization, or unsupported fit behavior is presented above diagnostic scope.
- Observed signal-region results are reported before the expected workflow and unblinding gates are valid.
- Plot captions or conclusions overstate what the plot can support.
- Reproducibility commands are missing or do not identify the final production run.

## Handoff Rule

Final handoff is allowed only when:

- no veto findings remain;
- required repair cycles are complete;
- scorecard and test outcome summary agree;
- report wording matches the weakest valid claim classification;
- all final numbers and plots are traceable to resolving artifacts.
