---
name: multiagent-hep-managing-analysis-budget
description: Supporting skill for the multiagent HEP coordinator. Use only after multiagent-hep-coordinating-analysis is active, when managing budget states, subagent throttling, prompt breadth, or audit scope.
---

# Multiagent HEP Managing Analysis Budget

## Purpose
Used by the coordinator when managing subagent count, prompt breadth, and audit scope.

## See also
- [multiagent-hep-running-stage-loop](../multiagent-hep-running-stage-loop/SKILL.md)
- [multiagent-hep-managing-analysis-state](../multiagent-hep-managing-analysis-state/SKILL.md)
- [multiagent-hep-logging-agent-timeline](../multiagent-hep-logging-agent-timeline/SKILL.md)
- [multiagent-hep-reviewing-stage-outputs](../multiagent-hep-reviewing-stage-outputs/SKILL.md)

## Budget States
- At each stage, estimate budget as healthy, tight, or critical.
- When platform quota is effectively unlimited, default to healthy and use tight or critical as discipline states rather than hard quota exhaustion.
- Treat unnecessary subagent fan-out as the first budget risk to control.
- Default delegation cap: at most one active worker and one active reviewer for one stage at a time.
- Any exception to the default delegation cap requires a decision entry in agent_timeline.jsonl that explains why the extra concurrency is necessary.

## Scope Reduction Rules
- Record any scope reduction in both analysis_state.json and agent_timeline.jsonl.
- Under healthy, keep routine work local and delegate only clearly critical analysis steps.
- Under tight, restrict delegation to the smallest critical step, minimize prompt breadth, avoid overlapping delegated stages, and prioritize the most decision-critical plots and checks.
- Under critical, avoid new subagents unless they are required for safe progression, review only the highest-risk artifacts needed for safe progression, and record what was deferred.
- If budget is tight or critical, explicitly reduce review scope and log it.
- Prefer fewer high-signal audits over many low-signal subagents.

## Prohibition
- Never silently drop the required audit.
- Never launch subagents just to offload straightforward work.
