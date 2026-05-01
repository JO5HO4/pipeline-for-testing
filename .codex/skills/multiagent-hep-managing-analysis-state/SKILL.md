---
name: multiagent-hep-managing-analysis-state
description: Supporting skill for the multiagent HEP coordinator. Use only after multiagent-hep-coordinating-analysis is active, when creating or updating analysis_state.json for staged workflow state.
---

# Multiagent HEP Managing Analysis State

## Purpose
Used by the coordinator when creating or updating the persistent state for the current workflow.

## See also
- [multiagent-hep-managing-file-layout](../multiagent-hep-managing-file-layout/SKILL.md)
- [multiagent-hep-running-stage-loop](../multiagent-hep-running-stage-loop/SKILL.md)
- [multiagent-hep-managing-analysis-budget](../multiagent-hep-managing-analysis-budget/SKILL.md)

## State Role
- analysis_state.json is the persistent memory file.
- codex_sessions.json is a coordinator-maintained session and rollout registry; analysis_state.json only points to it.
- Do not copy codex_sessions.json contents into analysis_state.json.
- Workers and reviewers should use assigned agent_tag values from their briefs rather than reading codex_sessions.json.
- Keep only the current stage detailed; collapse completed stages to short summaries.
- Use concise structured formats, not long prose.

## Required analysis_state.json Shape
```json
{
"workflow_goal": "<short string>",
"session_registry": "codex_sessions.json",
"current_stage": {
    "name": "<stage>",
    "classification": "routine|critical_analysis",
    "executor": "coordinator|worker",
    "status": "planned|running|repaired|approved|blocked|degraded|needs_revisit",
    "cycle": 1,
    "inputs": ["<path>"],
    "outputs": ["<path>"],
    "plots": ["<path>"],
    "reviews": ["<path>"],
    "summary": "<short summary>",
    "open_risks": ["<short item>"],
    "downstream_notes": ["<short item>"]
},
"completed_stages": [
  {
    "name": "<stage>",
    "classification": "routine|critical_analysis",
    "executor": "coordinator|worker",
    "status": "approved|degraded|blocked|needs_revisit",
    "summary": "<one-line summary>",
    "key_risks": ["<short item>"],
    "downstream_notes": ["<short item>"]
  }
],
"global_risks": ["<short item>"],
"claim_policy": {
    "reference_spec": "<path to authoritative analysis JSON or paper summary>",
    "data_provenance": "artifacts/data_provenance/data_provenance.json",
    "feasibility_matrix": "artifacts/spec_feasibility/reference_feasibility_matrix.json",
    "claim_classification": "artifacts/claim_review/claim_classification.json",
    "report_number_trace": "artifacts/claim_review/report_number_trace.json",
    "finalization_gate": "artifacts/finalize/finalization_gate.json",
    "evaluation_scorecard": "outputs/evaluation_scorecard.json",
    "test_outcome_summary": "outputs/test_outcome_summary.json",
    "sample_registry": "<repo-root-relative path or missing>",
    "sample_exclusion_reasons": "<repo-root-relative path or missing>",
    "final_artifact_review": "reviews/final_artifact_review/review_<cycle>.json",
    "final_claim_review": "reviews/final_claim_review/review_<cycle>.json",
    "real_observed_data_validated": false,
    "observed_signal_region_unblinded": false,
    "observed_diagnostic_results_allowed": false,
    "observed_paper_level_claims_allowed": false,
    "paper_level_claims_allowed": false,
    "diagnostic_claims_allowed": true,
    "handoff_allowed": false,
    "allowed_final_claims": ["<short item>"],
    "blocked_final_claims": ["<short item>"]
},
"budget": {
    "state": "healthy|tight|critical",
    "note": "<short estimate>",
    "scope_reductions": ["<short item>"]
}
}
```

## Field Definitions
- workflow_goal: Short overall goal for the workflow.
- session_registry: Path to the canonical session and rollout registry.
- current_stage: Full detail for the active stage only.
- current_stage.classification: Stage type chosen during PLAN; use routine for coordinator-run operational work and critical_analysis for delegated analysis work.
- current_stage.executor: Role responsible for execution; use coordinator for routine stages and worker for delegated critical_analysis stages.
- current_stage.cycle: Current audit-repair cycle number. The first audit for a stage is cycle 1; increment before each fresh audit after repair.
- current_stage.inputs, current_stage.outputs, current_stage.plots: Paths relevant to the active stage.
- current_stage.reviews: Paths to stage audit files, including local self-checks and independent reviews.
- current_stage.summary: Short stage summary.
- current_stage.open_risks: Short unresolved risk items for the active stage.
- current_stage.downstream_notes: Short notes that constrain later stages.
- completed_stages: Collapsed records for finished stages.
- completed_stages.classification and completed_stages.executor: Preserve the execution mode for auditability after collapsing the stage.
- completed_stages.summary: One-line summary.
- completed_stages.key_risks: Short retained risk items.
- completed_stages.downstream_notes: Short retained notes for downstream stages.
- global_risks: Cross-stage risk list.
- claim_policy.reference_spec: Path to the faithful paper/spec source of truth; do not rewrite it to match substitutions.
- claim_policy.data_provenance: Path to the reviewed data provenance artifact that decides whether observed paper-level claims are allowed.
- claim_policy.feasibility_matrix: Path to the reviewed requirement-by-requirement feasibility matrix.
- claim_policy.claim_classification: Path to the result-level claim classification artifact.
- claim_policy.report_number_trace: Path to the artifact mapping final report numbers and claims to machine-readable source artifacts.
- claim_policy.finalization_gate: Path to the final report gate artifact.
- claim_policy.evaluation_scorecard: Path to the shared run-quality scorecard.
- claim_policy.test_outcome_summary: Path to the short verdict summary that must agree with the scorecard.
- claim_policy.sample_registry: Path to the sample registry used for registered-vs-usable sample accounting.
- claim_policy.sample_exclusion_reasons: Path to the artifact explaining every excluded or unprocessed registered sample.
- claim_policy.final_artifact_review: Path to the latest final artifact/run-integrity review.
- claim_policy.final_claim_review: Path to the latest final claim/report-scope review.
- claim_policy.real_observed_data_validated: Boolean copied from data provenance review; false blocks observed paper-level claims.
- claim_policy.observed_signal_region_unblinded: Boolean recording whether observed signal-region results were intentionally unblinded after expected workflow completion.
- claim_policy.observed_diagnostic_results_allowed: Boolean recording whether pseudo-observed or observed diagnostics may be reported with diagnostic labels.
- claim_policy.observed_paper_level_claims_allowed: Boolean recording whether observed results may be used for paper-level claims.
- claim_policy.paper_level_claims_allowed: Boolean recording whether any paper-level claim is allowed by provenance, feasibility, execution, and claim review.
- claim_policy.diagnostic_claims_allowed: Boolean recording whether diagnostic or reinterpretation claims are allowed.
- claim_policy.handoff_allowed: Boolean copied from the final claim review and scorecard; false blocks final handoff.
- claim_policy.allowed_final_claims and blocked_final_claims: Short cross-stage claim boundaries that constrain reporting.
- budget: Shared budget state, note, and scope reductions.
