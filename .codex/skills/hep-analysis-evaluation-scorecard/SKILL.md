---
name: hep-analysis-evaluation-scorecard
description: "Use when running or finalizing a HEP analysis workflow that must produce outputs/evaluation_scorecard.json and outputs/test_outcome_summary.json for baseline or multiagent testing. Covers run completeness, sample accounting, data provenance, feasibility, claim scope, finalization, review status, reproducibility, and comparison-ready quality signals."
---

# HEP Analysis Evaluation Scorecard

Use this skill in every baseline or multiagent HEP testing run. It creates compact machine-readable records that say what was actually run, what claims are allowed, and why handoff is or is not allowed.

## Required Outputs

- Write `outputs/evaluation_scorecard.json`.
- Write `outputs/test_outcome_summary.json`.
- Create or update both files at run start, after data provenance, after feasibility review, after production execution, after claim review, after finalization, and before the final response.
- If the workflow blocks early, still write both files with known evidence and blocking reasons.
- Do not invent a passing status. Use `missing`, `unknown`, `blocked`, or `not_applicable` when evidence is absent.
- All paths inside both JSON files must be relative to the repository root. Do not use paths relative to `outputs/`.

## Binding Gates

- Before observed results are computed or reported, classify every `input-data/data` ROOT file as `real_observed_collision_data`, `pseudo_observed_mc_like_data`, or `unusable`; record filename, tree/schema, branch, weight/metadata evidence when available, and the decision rule.
- Observed paper-level claims are allowed only when data provenance validates real observed collision data and the observed signal region was intentionally unblinded after the expected workflow was fixed.
- Pseudo-observed values may appear only as clearly labeled `diagnostic_proxy` outputs.
- A final report sourced from a smoke, capped, partial, still-running, or incomplete production run must be marked `blocked` or `diagnostic_complete`, not `complete`.
- If a ROOT-backed statistical backend is required for the intended claim, diagnostic fallback is allowed only after `hep-root-runtime-repair` writes a runtime repair-attempt artifact and the scorecard points to it.
- Negative or signed MC yields that are clipped, floored, or otherwise stabilized force the affected statistic to `diagnostic_proxy` or `blocked` unless a reviewed statistical model explicitly justifies the treatment.
- Mutually exclusive regions, categories, or flavor channels need mask-overlap sanity evidence. Identical yields across supposedly distinct regions require repair or an explicit blocking explanation.
- Every final result needs one claim classification: `reproduction`, `reinterpretation`, `diagnostic_proxy`, or `blocked`.

## Sample Accounting Rules

- Count all registered samples from the sample registry or authoritative discovery artifact, not just selected nominal samples.
- Record the exact scope definition used for execution in `sample_scope.sample_scope_definition`.
- If only a subset is valid for the implemented diagnostic, record both the registered totals and the central-or-usable subset totals.
- Record every exclusion class in `sample_scope.excluded_sample_reasons_path`; if no samples were excluded, write an artifact that says so.
- `production.all_usable_samples_processed` can be true only when `processed_central_or_usable_samples == central_or_usable_samples_total` and no unprocessed usable sample is hidden by the scope wording.
- A scorecard that lacks a sample registry, scope definition, processed counts, or exclusion reasons cannot allow final handoff.

## Branch Role Rules

- For `branch_role: baseline`, `gates.final_artifact_review` and `gates.final_claim_review` must be `not_applicable` unless actual review artifacts exist. Baseline handoff may be allowed without final review artifacts if all other required gates pass and the test outcome summary agrees.
- For `branch_role: multiagent`, `gates.final_artifact_review` and `gates.final_claim_review` are required for handoff. They must point to real review artifacts and have no veto findings.
- If `branch_role` is `unknown`, use the stricter multiagent rule for handoff.

## Scorecard Schema

Use this shape and keep all artifact paths repo-root-relative:

```json
{
  "schema_version": "1.1",
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
    "mc_files_total": null
  },
  "sample_scope": {
    "sample_registry_path": "<path or missing>",
    "sample_scope_definition": "<plain-language definition of registered, usable, and excluded samples>",
    "registered_samples_total": null,
    "registered_data_samples": null,
    "registered_mc_samples": null,
    "central_or_usable_samples_total": null,
    "processed_registered_samples": null,
    "processed_central_or_usable_samples": null,
    "excluded_samples_total": null,
    "excluded_sample_reasons_path": "<path or missing>",
    "scope_consistency": "pass|warning|fail|missing"
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
    "real_observed_data_validated": false,
    "observed_signal_region_unblinded": false,
    "observed_diagnostic_results_allowed": false,
    "observed_paper_level_claims_allowed": false,
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
    "final_artifact_review": "<path or not_applicable or missing>",
    "final_claim_review": "<path or not_applicable or missing>",
    "root_runtime_repair_attempts": "<path or not_applicable or missing>",
    "final_report": "<path or missing>",
    "reproducibility_commands": "<path or missing>",
    "test_outcome_summary": "outputs/test_outcome_summary.json"
  },
  "quality": {
    "tests_run": [],
    "pytest_status": "pass|fail|not_run|unavailable",
    "root_status": "available|unavailable|unknown",
    "root_runtime_repair_status": "available|repaired|unavailable_after_repair_attempts|not_required|missing",
    "plots_present": false,
    "report_number_trace_complete": false
  },
  "test_outcome_summary": {
    "final_status": "complete|blocked|diagnostic_complete|failed",
    "handoff_allowed": false,
    "paper_level_claims_allowed": false,
    "diagnostic_only": true,
    "primary_blockers": [],
    "headline_diagnostic_numbers": []
  },
  "handoff_allowed": false,
  "blocking_issues": [],
  "degraded_reasons": []
}
```

## Test Outcome Summary Schema

`outputs/test_outcome_summary.json` must duplicate the verdict fields needed for quick comparison:

```json
{
  "schema_version": "1.0",
  "updated_at_utc": "<ISO-8601 timestamp>",
  "analysis_target": "<short target name>",
  "branch_role": "baseline|multiagent|unknown",
  "final_status": "complete|blocked|diagnostic_complete|failed",
  "handoff_allowed": false,
  "paper_level_claims_allowed": false,
  "diagnostic_only": true,
  "primary_blockers": [],
  "headline_diagnostic_numbers": [],
  "scorecard_path": "outputs/evaluation_scorecard.json",
  "final_report": "<repo-root-relative path or missing>"
}
```

## Finalization Rule

The scorecard is not a substitute for the underlying artifacts. It is an index and verdict summary. Final handoff is allowed only when:

- `outputs/evaluation_scorecard.json` and `outputs/test_outcome_summary.json` agree on `final_status`, `handoff_allowed`, `paper_level_claims_allowed`, and diagnostic scope.
- The scorecard points to required source artifacts with repo-root-relative paths that resolve.
- Any unavailable ROOT-backed statistical backend has a resolving root-runtime repair-attempt artifact before fallback or blocked status is accepted.
- Sample accounting agrees with the registry, progress artifacts, and run manifest.
- Gate statuses support the claim scope printed in the report.
- Branch-role review requirements are satisfied.

Use `complete` only for a full production run whose supported claims are allowed by the evidence. Use `diagnostic_complete` for a completed diagnostic or reinterpretation run that intentionally blocks paper-level claims. Use `blocked` when required ingredients, dependencies, data, provenance, or feasibility prevent a valid run. Use `failed` when the workflow attempted the run but produced inconsistent, crashed, or unusable outputs.
