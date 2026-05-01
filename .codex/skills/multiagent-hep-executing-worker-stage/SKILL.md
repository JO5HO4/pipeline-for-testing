---
name: multiagent-hep-executing-worker-stage
description: Supporting skill for multiagent HEP delegated workers. Use only when a coordinator following multiagent-hep-coordinating-analysis assigns a critical_analysis stage or repair to a worker agent.
---

# Multiagent HEP Executing Worker Stage

## Purpose
Used by a worker when executing or repairing one delegated critical_analysis stage from the multiagent HEP workflow.

## See also
- [multiagent-hep-managing-file-layout](../multiagent-hep-managing-file-layout/SKILL.md)
- [multiagent-hep-managing-analysis-state](../multiagent-hep-managing-analysis-state/SKILL.md)
- [multiagent-hep-reviewing-stage-outputs](../multiagent-hep-reviewing-stage-outputs/SKILL.md)

## Use Boundary
- Use this skill only when the coordinator delegates a critical_analysis stage or repair.
- Keep environment setup, file preparation, dependency checks, and other straightforward tasks local unless the coordinator marks them as critical.
- Read handoff/<stage>/local_brief.txt when present and relevant to the delegated repair context.

## Worker Contract
- Worker is used only for a delegated critical_analysis stage or repair.
- Worker executes only the assigned stage.
- Worker must read analysis_state.json and latest relevant review files first.
- Worker must read artifacts/data_provenance/data_provenance.json when it exists and must not produce observed paper-level claims outside the allowed observed-data scope recorded there.
- Worker must read artifacts/spec_feasibility/reference_feasibility_matrix.json when it exists and must keep outputs within the allowed claim scope recorded there.
- Repair workers must read the latest reviews/final_independent_review/review_<cycle>.json when the repair follows final independent review findings.
- Worker writes only required outputs for the stage.
- Worker must produce requested plots for review.
- Worker must leave concise machine-readable notes.
- Worker must preserve the assigned agent_tag in notes and output metadata where practical.
- Worker must not append to agent_timeline.jsonl; the coordinator summarizes worker notes there.
- Worker must not declare stage approval.
- Worker must not turn substituted proxy ingredients into paper-level claims.
- Worker must flag negative-yield clipping, pseudo-observed data, missing signal models, missing background methods, partial/capped inputs, and duplicated or overlapping mutually exclusive region masks in its machine-readable notes when they affect downstream statistics.

## Required Outputs
- Stage outputs.
- Diagnostic plots.
- Concise notes on assumptions and risks.

## Worker Brief Template
```text
role: worker
agent_tag: <tag assigned by coordinator>
stage: <stage>
exact task: <stage goal, specific artifacts to produce, and any upstream findings from analysis_state.json that constrain this stage’s decisions>
required input files:
- analysis_state.json
- <path>
required output paths:
- artifacts/<stage>/<file>
acceptance criteria:
- <criterion>
- preserve observed-claim boundaries from data provenance
- preserve claim classification boundaries from the feasibility matrix
```
