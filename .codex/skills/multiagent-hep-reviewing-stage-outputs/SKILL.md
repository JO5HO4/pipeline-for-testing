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

## Reviewer Contract
- Reviewer is an independent auditor, not an implementer.
- Reviewer must read analysis_state.json and latest relevant review files first.
- Reviewer must inspect plots visually when present.
- Reviewer must inspect requested plots visually and check numerical outputs.
- Reviewer must reason about what could go wrong in this specific stage’s physics, not just follow a checklist.
- Reviewer must state consequence chains, not just local defects.
- Reviewer must not append to agent_timeline.jsonl; the coordinator summarizes the saved audit file.
- Reviewer has veto authority for progression when a stage would allow an unsupported physics claim, even if the code ran successfully.
- Reviewer must distinguish implementation success from claim validity.

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

## Mandatory Veto Findings
Record severity PROBLEM and set can_proceed false when any of these apply to the audited stage or downstream claim:
- A partial, smoke, capped, or incomplete run is being treated as production or final.
- A paper-level claim is made from a substituted proxy implementation without an approved feasibility matrix and claim classification.
- Observed significance, limits, mass limits, or exclusions are reported when observed data are unavailable, are MC-like pseudo-data, or were used before the expected workflow was fixed.
- A dedicated signal model, background method, fake/nonprompt estimate, charge-misidentification estimate, systematic source, or likelihood ingredient required for the claim is unavailable and the result is not labeled diagnostic_proxy or blocked.
- Negative or signed MC yields are silently clipped, zeroed, or otherwise stabilized and then used to print significances or limits as if the statistical model were valid.
- A result lacks one of these claim classifications: reproduction, reinterpretation, diagnostic_proxy, blocked.
- The final report source cannot be traced to a completed full-statistics production run.

## Required Audit File Format
```json
{
"stage": "<stage>",
"cycle": 1,
"audit_mode": "local_self_check|independent_review",
"auditor_role": "coordinator|reviewer",
"auditor_id": "<agent id>",
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
"scope_note": "<short note if scope was reduced>"
}
```

## Review Logic
- can_proceed must be false if any finding has severity PROBLEM.
- WARNING findings may proceed only as degraded: set can_proceed true, require the coordinator to mark the stage degraded, and copy the warning into downstream_notes or global_risks.
- OK findings may proceed without degradation when no WARNING or PROBLEM findings remain.
- Use audit_mode local_self_check for routine stages and audit_mode independent_review for delegated critical_analysis stages.
- If review scope was reduced, the auditor must say what was skipped in scope_note.
- For routine local self-checks, the coordinator must record any residual risk explicitly.
- Missing feasibility or finalization artifacts are PROBLEM findings for SPEC_FEASIBILITY, CLAIM_REVIEW, FINALIZE, or any stage that prints final physics claims.
- A reviewer may approve diagnostic output while blocking paper-level claims; in that case can_proceed may be true only if the coordinator records the affected results as diagnostic_proxy or blocked.

## Reviewer Brief Template
```text
role: reviewer
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
- save findings in the required audit schema
```
