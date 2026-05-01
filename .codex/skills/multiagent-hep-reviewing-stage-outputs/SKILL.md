---
name: multiagent-hep-reviewing-stage-outputs
description: Supporting skill for multiagent HEP audits. Use only after multiagent-hep-coordinating-analysis is active, when recording local self-checks or independent reviews for a workflow stage.
---

# Multiagent HEP Reviewing Stage Outputs

## Purpose
Used when a stage audit must be recorded; reviewer agents load it for critical_analysis stages, and the coordinator follows its shared audit schema for routine local self-checks.

## See also
- [multiagent-hep-managing-file-layout](../multiagent-hep-managing-file-layout/SKILL.md)
- [multiagent-hep-managing-analysis-state](../multiagent-hep-managing-analysis-state/SKILL.md)
- [multiagent-hep-managing-analysis-budget](../multiagent-hep-managing-analysis-budget/SKILL.md)

## Use Boundary
- Reviewer sub-agents load this skill only for a critical_analysis stage or when progression risk is material.
- The coordinator uses the same audit file schema for routine local self-checks.
- Final artifact and claim reviewers also load this skill for FINAL_ARTIFACT_REVIEW and FINAL_CLAIM_REVIEW and follow the stricter final-review contracts below.

## Reviewer Contract
- Reviewer is an independent auditor, not an implementer.
- Reviewer must read analysis_state.json and latest relevant review files first.
- Reviewer must inspect plots visually when present.
- Reviewer must inspect requested plots visually and check numerical outputs.
- Reviewer must reason about what could go wrong in this specific stage’s physics, not just follow a checklist.
- Reviewer must state consequence chains, not just local defects.
- Reviewer must check numerical invariants that protect final claims, including processed/all sample counts, event caps, region/category overlap, category or flavor distinctness, negative signed yields, and data provenance decisions.
- Reviewer must preserve the assigned agent_tag in the saved audit file where practical.
- Reviewer must not append to agent_timeline.jsonl; the coordinator summarizes the saved audit file.
- Reviewer has veto authority for progression when a stage would allow an unsupported physics claim, even if the code ran successfully.
- Reviewer must distinguish implementation success from claim validity.

## Final Artifact Review Contract
- The final artifact reviewer is an adversarial whole-analysis auditor focused on artifact integrity and reproducibility.
- The final artifact reviewer must not implement repairs or edit analysis outputs.
- Treat successful code execution as insufficient evidence for handoff.
- Review the prompt, state, session registry, outputs/evaluation_scorecard.json, outputs/test_outcome_summary.json, provenance, feasibility, execution, numerical outputs, plots, claim classification, finalization gate, report number trace, final report, and reproducibility command together.
- Veto progression to final claim review if required artifacts are missing, stale, contradictory, non-reproducible, incomplete, or sourced from smoke, capped, partial, or still-running production.
- If a problem is found, name the upstream stage that must be redone and specify the minimal required repair.

## Final Claim Review Contract
- The final claim reviewer is an adversarial whole-analysis auditor focused on report wording, claim scope, and numerical claim traceability.
- The final claim reviewer must not be the final artifact reviewer and must not implement repairs or edit analysis outputs.
- Veto final handoff if any headline claim, numerical table value, plot statement, or conclusion cannot be traced to a machine-readable source artifact.
- Veto final handoff if the report tone is stronger than the weakest valid claim classification.
- Veto final handoff if the report promotes pseudo-observed, partial, smoke, capped, clipped-yield, or unsupported-proxy results as paper-level physics.
- If a problem is found, name the upstream stage that must be redone and specify the minimal required repair.

## Priority Issue Classes
- data/MC agreement
- normalization offsets and downstream consequences
- fit quality and stability
- shape mismodeling
- uncertainty propagation gaps
- reference-spec feasibility and claim scope
- partial-statistics or smoke-output promotion
- observed-data provenance and blinding order
- signed-weight or negative-yield handling
- region/category mask overlap and duplicated yields
- pseudo-observed result labeling

## Mandatory Veto Findings
Record severity PROBLEM and set can_proceed false when any of these apply to the audited stage or downstream claim:
- A partial, smoke, capped, or incomplete run is being treated as production or final.
- A run reports final physics results without clear processed/all sample counts and no event-cap evidence.
- The scorecard sample_scope is missing, ambiguous, contradicted by the sample registry/progress/run manifest, or omits exclusion reasons for unprocessed samples.
- A ROOT-backed backend was required or missing, but diagnostic fallback or blocked status lacks a resolving root-runtime repair-attempt artifact.
- A data provenance artifact is missing, inconclusive, or not independently reviewed before observed results are computed or reported.
- A paper-level claim is made from a substituted proxy implementation without an approved feasibility matrix and claim classification.
- Observed significance, limits, mass limits, or exclusions are reported when observed data are unavailable, are MC-like pseudo-data, or were used before the expected workflow was fixed.
- Pseudo-observed values are headlined, summarized, or phrased as observed physics results rather than clearly labeled diagnostic_proxy outputs.
- A dedicated signal model, background method, fake/nonprompt estimate, charge-misidentification estimate, systematic source, or likelihood ingredient required for the claim is unavailable and the result is not labeled diagnostic_proxy or blocked.
- Negative or signed MC yields are silently clipped, zeroed, or otherwise stabilized and then used to print significances or limits as if the statistical model were valid.
- Mutually exclusive regions, categories, or flavor channels have identical yields or unexplained overlaps without a reviewed mask sanity artifact.
- A result lacks one of these claim classifications: reproduction, reinterpretation, diagnostic_proxy, blocked.
- The final report source cannot be traced to a completed full-statistics production run.
- outputs/evaluation_scorecard.json is missing, stale, contradicted by source artifacts, or says handoff is blocked while the report claims final handoff.
- outputs/evaluation_scorecard.json uses artifact paths that are not repo-root-relative, or the listed paths do not resolve.
- outputs/test_outcome_summary.json is missing, contradicts outputs/evaluation_scorecard.json, or contradicts the final report tone.
- A baseline-style `not_applicable` final review gate is used in a multiagent run, or a final review gate is marked pass without a real review artifact.
- The report number trace is missing, incomplete, or contradicted by the source artifacts.
- A required final artifact review or final claim review is missing, or either was performed by the same agent that implemented or approved the affected final claim.

## Required Audit File Format
```json
{
"stage": "<stage>",
"cycle": 1,
"audit_mode": "local_self_check|independent_review",
"auditor_role": "coordinator|reviewer",
"auditor_id": "<agent id>",
"auditor_tag": "<stable agent_tag>",
"status": "OK|WARNING|PROBLEM",
"summary": "<short assessment>",
"artifacts_reviewed": {
    "files": ["<path>"],
    "plots": ["<path>"]
},
"findings": [
    {
    "id": "F1",
    "severity": "OK|WARNING|PROBLEM",
    "category": "data_mc|normalization|fit|shape|systematics|code|other",
    "artifact": "<path or logical name>",
    "issue": "<concise statement>",
    "evidence": "<specific visual or numerical evidence>",
    "consequence": "<downstream consequence chain>",
    "recommended_fix": "<actionable repair step>"
    }
],
"required_repairs": ["<short item>"],
"can_proceed": true,
"claim_classification_required": true,
"data_provenance_required": true,
"scope_note": "<short note if scope was reduced>"
}
```

## Final Artifact Review File Format
```json
{
"stage": "FINAL_ARTIFACT_REVIEW",
"cycle": 1,
"audit_mode": "final_artifact_review",
"auditor_role": "final_artifact_reviewer",
"auditor_id": "<agent id>",
"auditor_tag": "<stable agent_tag>",
"status": "PASS|CONDITIONAL_PASS|FAIL",
"handoff_allowed": false,
"paper_level_claims_allowed": false,
"diagnostic_claims_allowed": true,
"summary": "<short critical assessment>",
"artifacts_reviewed": {
    "files": ["<path>"],
    "plots": ["<path>"]
},
"artifact_checks": [
    {
    "check": "scorecard|test_outcome_summary|sample_scope|root_runtime_repair|artifact_paths|production_run|data_provenance|feasibility|claim_classification|number_trace|plots|reproducibility|final_report",
    "source_artifact": "<path or missing>",
    "status": "PASS|WARNING|PROBLEM",
    "issue": "<empty or concise issue>"
    }
],
"veto_findings": [
    {
    "id": "V1",
    "severity": "PROBLEM",
    "category": "scorecard|test_outcome_summary|sample_scope|root_runtime_repair|artifact_paths|data_provenance|partial_run|statistics|report_trace|plot|reproducibility|artifact|other",
    "artifact": "<path or logical name>",
    "issue": "<concise statement>",
    "evidence": "<specific evidence>",
    "consequence": "<downstream consequence>",
    "upstream_stage_to_revisit": "<stage>",
    "recommended_fix": "<actionable repair step>"
    }
],
"warning_findings": [],
"required_repairs": ["<short item>"],
"rerun_required_from_stage": "<stage or none>",
"scope_note": "<allowed degraded scope if any>"
}
```

## Final Claim Review File Format
```json
{
"stage": "FINAL_CLAIM_REVIEW",
"cycle": 1,
"audit_mode": "final_claim_review",
"auditor_role": "final_claim_reviewer",
"auditor_id": "<agent id>",
"auditor_tag": "<stable agent_tag>",
"status": "PASS|CONDITIONAL_PASS|FAIL",
"handoff_allowed": false,
"paper_level_claims_allowed": false,
"diagnostic_claims_allowed": true,
"summary": "<short critical assessment>",
"artifacts_reviewed": {
    "files": ["<path>"],
    "plots": ["<path>"]
},
"number_trace_checks": [
    {
    "report_location": "<section/table/claim>",
    "reported_value": "<value or claim>",
    "source_artifact": "<path>",
    "source_key": "<json path, table row, or plot id>",
    "claim_classification": "reproduction|reinterpretation|diagnostic_proxy|blocked",
    "status": "PASS|WARNING|PROBLEM",
    "issue": "<empty or concise issue>"
    }
],
"claim_scope_checks": [
    {
    "claim_or_section": "<report location>",
    "weakest_allowed_classification": "reproduction|reinterpretation|diagnostic_proxy|blocked",
    "reported_tone": "paper_level|reinterpretation|diagnostic|blocked",
    "status": "PASS|WARNING|PROBLEM",
    "issue": "<empty or concise issue>"
    }
],
"veto_findings": [
    {
    "id": "V1",
    "severity": "PROBLEM",
    "category": "claim|data_provenance|partial_run|statistics|report_trace|plot|reproducibility|scorecard|test_outcome_summary|other",
    "artifact": "<path or logical name>",
    "issue": "<concise statement>",
    "evidence": "<specific evidence>",
    "consequence": "<downstream consequence>",
    "upstream_stage_to_revisit": "<stage>",
    "recommended_fix": "<actionable repair step>"
    }
],
"warning_findings": [],
"required_repairs": ["<short item>"],
"rerun_required_from_stage": "<stage or none>",
"scope_note": "<allowed degraded scope if any>"
}
```

## Review Logic
- can_proceed must be false if any finding has severity PROBLEM.
- WARNING findings may proceed only as degraded: set can_proceed true, require the coordinator to mark the stage degraded, and copy the warning into downstream_notes or global_risks.
- OK findings may proceed without degradation when no WARNING or PROBLEM findings remain.
- Use audit_mode local_self_check for routine stages and audit_mode independent_review for delegated critical_analysis stages.
- If review scope was reduced, the auditor must say what was skipped in scope_note.
- For routine local self-checks, the coordinator must record any residual risk explicitly.
- Missing data provenance, feasibility, claim-classification, or finalization artifacts are PROBLEM findings for DATA_PROVENANCE, SPEC_FEASIBILITY, CLAIM_REVIEW, FINALIZE, or any stage that prints final physics claims.
- A WARNING that changes a physics number, region definition, sample role, data provenance decision, or claim scope must trigger repair unless the coordinator explicitly degrades the affected claim classification.
- A reviewer may approve diagnostic output while blocking paper-level claims; in that case can_proceed may be true only if the coordinator records the affected results as diagnostic_proxy or blocked.
- FINAL_ARTIFACT_REVIEW passes only when status is PASS or CONDITIONAL_PASS and veto_findings is empty.
- FINAL_ARTIFACT_REVIEW must fail if scorecard sample counts do not agree with the sample registry, progress artifact, and production manifest, or if scorecard artifact paths are not repo-root-relative and resolvable.
- FINAL_ARTIFACT_REVIEW must fail if a ROOT-backed statistical backend was required but fallback or blocked status has no root-runtime repair-attempt artifact.
- FINAL_CLAIM_REVIEW passes only when status is PASS or CONDITIONAL_PASS, handoff_allowed is true, veto_findings is empty, and outputs/evaluation_scorecard.json plus outputs/test_outcome_summary.json also record handoff_allowed true with matching claim scope.
- FINAL_CLAIM_REVIEW must fail if the report tone is stronger than outputs/test_outcome_summary.json final_status allows.
- Any final-review PROBLEM requires repair and fresh FINAL_ARTIFACT_REVIEW and FINAL_CLAIM_REVIEW cycles after the affected stage and downstream gates are rerun.
- Any final-review WARNING that changes a physics number, region definition, sample role, data provenance decision, claim classification, report wording, or handoff scope requires repair or explicit claim degradation before handoff.

## Reviewer Brief Template
```text
role: reviewer
agent_tag: <tag assigned by coordinator>
stage: <stage>
exact task: <artifacts and plots to examine, and upstream risks to watch for>
required input files:
- analysis_state.json
- reviews/<stage>/review_<previous_cycle>.json when applicable
- handoff/<stage>/reviewer_brief_draft.txt when present
- artifacts/<stage>/<file>
- <path>
required output paths:
- reviews/<stage>/review_<cycle>.json
acceptance criteria:
- write audit_mode: independent_review
- inspect requested plots visually when present
- check numerical outputs
- check reference feasibility, claim classification, observed-data provenance, and partial-run status when relevant
- check processed/all sample counts, event caps, region/category overlap sanity, flavor/category distinctness, negative-yield handling, and pseudo-observed labeling when relevant
- save findings in the required audit schema
```

## Final Artifact Reviewer Brief Template
```text
role: final_artifact_reviewer
agent_tag: <tag assigned by coordinator>
stage: FINAL_ARTIFACT_REVIEW
exact task: Critically review artifact integrity and run completeness end to end. Do not summarize success; look for missing, stale, partial, contradictory, or non-reproducible artifacts.
required input files:
- prompt.txt
- analysis_state.json
- codex_sessions.json
- outputs/evaluation_scorecard.json
- outputs/test_outcome_summary.json
- artifacts/runtime/root_runtime_repair_attempts.json when ROOT-backed capability was required or missing
- artifacts/data_provenance/data_provenance.json
- artifacts/spec_feasibility/reference_feasibility_matrix.json
- artifacts/claim_review/claim_classification.json
- artifacts/claim_review/report_number_trace.json
- artifacts/finalize/finalization_gate.json
- <production run manifest>
- <sample registry>
- <sample exclusion reasons>
- <yields and statistics artifacts>
- <plot manifest and selected plots>
- <final report>
- <reproducibility commands>
required output paths:
- reviews/final_artifact_review/review_<cycle>.json
acceptance criteria:
- use audit_mode: final_artifact_review
- verify outputs/evaluation_scorecard.json against source artifacts
- verify outputs/test_outcome_summary.json agrees with outputs/evaluation_scorecard.json and the final report
- verify ROOT-backed fallback or blocked status is backed by a resolving root-runtime repair-attempt artifact when relevant
- verify every scorecard artifact path is repo-root-relative and resolves
- verify every reported final number appears in report_number_trace.json
- inspect selected plots visually when present
- verify processed/all sample counts, registered-vs-usable sample scope, excluded-sample reasons, and event-cap status against the registry, progress artifact, and production manifest
- verify data provenance, feasibility, claim classification, finalization gate, production manifest, and reproducibility evidence agree
- set handoff_allowed false and name rerun_required_from_stage if repair is needed
```

## Final Claim Reviewer Brief Template
```text
role: final_claim_reviewer
agent_tag: <tag assigned by coordinator>
stage: FINAL_CLAIM_REVIEW
exact task: Critically review the final report claims and wording end to end. Do not summarize success; look for overclaims, unsupported numbers, pseudo-observed misuse, clipped-yield misuse, or paper-level claims that should be blocked.
required input files:
- prompt.txt
- analysis_state.json
- outputs/evaluation_scorecard.json
- outputs/test_outcome_summary.json
- reviews/final_artifact_review/review_<cycle>.json
- artifacts/data_provenance/data_provenance.json
- artifacts/spec_feasibility/reference_feasibility_matrix.json
- artifacts/claim_review/claim_classification.json
- artifacts/claim_review/report_number_trace.json
- artifacts/finalize/finalization_gate.json
- <selected plots>
- <final report>
required output paths:
- reviews/final_claim_review/review_<cycle>.json
acceptance criteria:
- use audit_mode: final_claim_review
- verify every headline claim and reported number against report_number_trace.json and source artifacts
- verify report tone matches the weakest allowed claim classification
- verify report tone matches outputs/test_outcome_summary.json final_status, including blocked or diagnostic-only status
- inspect selected plots visually when present and check captions/conclusions
- verify outputs/evaluation_scorecard.json and outputs/test_outcome_summary.json agree with the allowed handoff scope
- set handoff_allowed false and name rerun_required_from_stage if repair is needed
```
