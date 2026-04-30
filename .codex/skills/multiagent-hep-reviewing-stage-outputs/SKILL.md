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
- Reviewer must preserve the assigned agent_tag in the saved audit file where practical.
- Reviewer must not append to agent_timeline.jsonl; the coordinator summarizes the saved audit file.

## Priority Issue Classes
- data/MC agreement
- normalization offsets and downstream consequences
- fit quality and stability
- shape mismodeling
- uncertainty propagation gaps

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
- save findings in the required audit schema
```
