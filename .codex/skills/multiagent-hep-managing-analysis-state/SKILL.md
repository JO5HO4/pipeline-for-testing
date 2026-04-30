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
- budget: Shared budget state, note, and scope reductions.
