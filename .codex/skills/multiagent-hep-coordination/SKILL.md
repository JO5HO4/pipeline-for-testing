---
name: multiagent-hep-coordination
description: "Single entrypoint package for coordinated multiagent HEP analysis workflows. Use when a HEP run needs staged local/delegated execution, persistent state, reviewer audits, repair cycles, final artifact/claim review, scorecard/test-summary consistency, and session tracking without loading many separate coordination skills."
---

# Multiagent HEP Coordination

Use this as the only multiagent HEP coordination entrypoint. It handles role mechanics; the analysis JSON is the source of truth for physics scope, available substitutions, blocked claims, sample policy, object definitions, and statistical interpretation.

## Core Rules

- Act as COORDINATOR.
- First derive the stage plan from the analysis JSON and repository state. For each selected stage, launch one generic `stage_worker`, then one independent generic `stage_reviewer`.
- Never let a worker review its own stage.
- Use file references in handoff briefs, not pasted logs.
- Maintain `analysis_state.json`, `codex_sessions.json`, `agent_timeline.jsonl`, `handoff/`, and `reviews/`.
- Treat `analysis/analysis.summary.json` as the contract when present; otherwise use the explicit analysis JSON named in the prompt.
- Do not change sample scope, object definitions, signal proxy policy, backend, statistic shape, blinding, or claim policy unless a stage writes `outputs/contracts/scope_change_decision.json` and the coordinator approves it.
- Any stage that creates, regenerates, modifies, or reviews plots must explicitly load `$plotting`; the yield/plot and reporting reviewers must check the plot manifest, style/label policy, and PDF/PNG outputs.

## Stage Loop

Run the same worker/reviewer loop for each dynamically selected stage:

```text
write handoff/stage_plan.json from the analysis contract
for stage in stage_plan.stages:
  write handoff/<stage>/stage_brief.json
  spawn stage_worker with the brief
  wait for required artifacts
  spawn stage_reviewer with the same brief and worker outputs
  if reviewer blocks, rerun a repair worker for the same stage
  proceed only after pass or allowed conditional_pass
```

Default stage templates:

```text
runtime
sample_branch
object_preselection
categorization
yield_plot
statistics
reporting
final_review
```

The coordinator may skip, merge, split, or add stages when the analysis JSON makes that appropriate. Every selected stage still needs a worker, an independent reviewer, and a recorded verdict.

## Load References As Needed

- [stage-loop.md](references/stage-loop.md): dynamic stage planning, generic stage worker/reviewer loop, and prompt templates.
- [delegation-state.md](references/delegation-state.md): state files, session registry, timeline, handoff briefs.
- [review-contracts.md](references/review-contracts.md): shared review schema and mandatory veto classes.
- [final-review-handoff.md](references/final-review-handoff.md): final artifact review, final claim review, and handoff requirements.

## Handoff Rule

Final handoff is allowed only when:

- no required stage is skipped;
- every stage has a separate worker and reviewer record;
- `outputs/evaluation_scorecard.json` and `outputs/test_outcome_summary.json` agree;
- runtime repair evidence exists when ROOT-backed fallback/blocking was needed;
- sample scope, number trace, plots, claims, and reproducibility pass the installed final quality review or the coordination-native final artifact/claim reviews.
