---
name: hep-analysis-evaluation-scorecard
description: Use when running or finalizing a HEP analysis workflow that must produce outputs/evaluation_scorecard.json for baseline or multiagent testing. Covers run completeness, data provenance, feasibility, claim scope, finalization, review status, reproducibility, and comparison-ready quality signals.
---

# HEP Analysis Evaluation Scorecard

Use this skill in every baseline or multiagent HEP testing run. It creates one compact machine-readable record that says what was actually run, what claims are allowed, and why handoff is or is not allowed.

## Required output

- Write `outputs/evaluation_scorecard.json`.
- Create or update it at run start, after data provenance, after feasibility review, after production execution, after claim review, after finalization, and before the final response.
- If the workflow blocks early, still write the scorecard with the known evidence and blocking reasons.
- Do not invent a passing status. Use `missing`, `unknown`, `blocked`, or `not_applicable` when evidence is absent.

## Binding gates

- Before observed results are computed or reported, classify every `input-data/data` ROOT file as `real_observed_collision_data`, `pseudo_observed_mc_like_data`, or `unusable`; record filename, tree/schema, branch, weight/metadata evidence when available, and the decision rule.
- Observed paper-level claims are allowed only when data provenance validates real observed collision data. Pseudo-observed values may appear only as clearly labeled `diagnostic_proxy` outputs.
- A final report sourced from a smoke, capped, partial, still-running, or incomplete production run must be marked blocked or diagnostic, not complete.
- Negative or signed MC yields that are clipped, floored, or otherwise stabilized force the affected statistic to `diagnostic_proxy` or `blocked` unless a reviewed statistical model explicitly justifies the treatment.
- Mutually exclusive regions, categories, or flavor channels need mask-overlap sanity evidence. Identical yields across supposedly distinct regions require repair or an explicit blocking explanation.
- Every final result needs one claim classification: `reproduction`, `reinterpretation`, `diagnostic_proxy`, or `blocked`.

## Scorecard schema

Use this shape and keep paths relative to the run workspace where possible:

```json
{
  "schema_version": "1.0",
  "updated_at_utc": "<ISO-8601 timestamp>",
  "analysis_target": "<short target name>",
  "branch_role": "baseline|multiagent|unknown",
  "reference_spec": "analysis/<spec>.json",
  "run_mode": "full|partial|smoke|capped|blocked|unknown",
  "workflow": {
    "skill_package": "baseline|multiagent|unknown",
    "git_commit": "<commit or unknown>",
    "primary_command": "<command or unknown>",
    "runtime_seconds": null,
    "session_registry": "codex_sessions.json|not_applicable"
  },
  "inputs": {
    "data_path": "input-data/data",
    "mc_path": "input-data/MC",
    "data_files_total": null,
    "mc_files_total": null,
    "usable_samples_total": null
  },
  "production": {
    "processed_samples": null,
    "total_usable_samples": null,
    "all_usable_samples_processed": false,
    "event_cap": null,
    "full_run_complete": false,
    "progress_artifact": "<path or missing>",
    "run_manifest": "<path or missing>"
  },
  "gates": {
    "data_provenance": "pass|warning|fail|missing|not_applicable",
    "spec_feasibility": "pass|warning|fail|missing|not_applicable",
    "mask_sanity": "pass|warning|fail|missing|not_applicable",
    "claim_review": "pass|warning|fail|missing|not_applicable",
    "finalization": "pass|warning|fail|missing|not_applicable",
    "final_artifact_review": "pass|warning|fail|missing|not_applicable",
    "final_claim_review": "pass|warning|fail|missing|not_applicable"
  },
  "claim_scope": {
    "observed_claims_allowed": false,
    "paper_level_claims_allowed": false,
    "diagnostic_claims_allowed": true,
    "allowed_final_claims": [],
    "blocked_final_claims": []
  },
  "artifacts": {
    "data_provenance": "<path or missing>",
    "feasibility_matrix": "<path or missing>",
    "claim_classification": "<path or missing>",
    "report_number_trace": "<path or missing>",
    "finalization_gate": "<path or missing>",
    "final_report": "<path or missing>",
    "reproducibility_commands": "<path or missing>"
  },
  "quality": {
    "tests_run": [],
    "pytest_status": "pass|fail|not_run|unavailable",
    "root_status": "available|unavailable|unknown",
    "plots_present": false,
    "report_number_trace_complete": false
  },
  "handoff_allowed": false,
  "blocking_issues": [],
  "degraded_reasons": []
}
```

## Finalization rule

The scorecard is not a substitute for the underlying artifacts. It is an index and verdict summary. Final handoff is allowed only when the scorecard points to the required source artifacts and the gate statuses support the claim scope printed in the report.
