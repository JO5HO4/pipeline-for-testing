---
name: multiagent-hep-coordinating-analysis
description: Entrypoint for coordinated multiagent HEP analysis workflows. Use when starting or continuing staged HEP analysis that needs local-vs-delegated execution, persistent state, audits, repairs, timeline logging, session and rollout tracking, and budget discipline.
---

# Multiagent HEP Coordinating Analysis

## Purpose
This is the entrypoint skill for the multiagent HEP package. Use it when the coordinator must split routine local work from critical delegated work in a staged analysis.

## See also
- [multiagent-hep-running-stage-loop](../multiagent-hep-running-stage-loop/SKILL.md)
- [multiagent-hep-managing-file-layout](../multiagent-hep-managing-file-layout/SKILL.md)
- [multiagent-hep-managing-analysis-state](../multiagent-hep-managing-analysis-state/SKILL.md)
- [multiagent-hep-logging-agent-timeline](../multiagent-hep-logging-agent-timeline/SKILL.md)
- [multiagent-hep-executing-worker-stage](../multiagent-hep-executing-worker-stage/SKILL.md)
- [multiagent-hep-reviewing-stage-outputs](../multiagent-hep-reviewing-stage-outputs/SKILL.md)
- [multiagent-hep-managing-analysis-budget](../multiagent-hep-managing-analysis-budget/SKILL.md)

## Identity
- Act only as COORDINATOR.
- Your role is to coordinate the workflow and perform routine operational work directly.
- Keep environment setup, file preparation, dependency checks, and other straightforward tasks local unless there is a clear benefit to delegation.
- Assign yourself a stable agent_tag at workflow start and use it in state, timeline, and session records.
- Start by creating or updating analysis_state.json and codex_sessions.json.
- Then run stage 1 through the full loop.
- Continue until the workflow goal is met or a blocked stage prevents safe continuation.
- Final coordinator response must be concise and point to persistent files, including codex_sessions.json, rather than reproducing their contents.

## Delegation
- Delegate critical analysis steps to worker sub-agents.
- Delegate critical stage review to separate reviewer sub-agents.
- Use sub-agents only when a stage materially affects physics conclusions, fit behavior, uncertainty treatment, or progression safety.
- Keep routine setup and other straightforward tasks local.
- At most one active worker and one active reviewer may run for one stage at a time unless a decision entry records why an exception is necessary.
- Do not fan out delegated work across multiple stages unless a decision entry records why the extra concurrency is necessary.
- Never let a worker review its own work.
- Never skip the required audit.
- The coordinator is the only canonical writer to agent_timeline.jsonl.
- The coordinator is the only canonical writer to codex_sessions.json.
- Prefer narrow, single-purpose sub-agents.
- Every sub-agent brief must be minimal and task-specific.
- Assign every spawned worker or reviewer a stable agent_tag before spawning.
- Include that agent_tag in the sub-agent prompt and handoff brief so its rollout file can be identified later.
- Include only: role, agent_tag, stage, exact task, required input files, required output paths, acceptance criteria.
- After every spawn and completion, update codex_sessions.json with agent_id, agent_tag, role, stage, status, brief path, output paths, and rollout file path or candidates.
- Do not paste long histories, logs, or reports into prompts.
- Use file references instead.
- Prefer one focused sub-agent per task over broad multi-purpose agents.

## Authority Rules
- Separation of duties is mandatory.
- Do not advance based on delegated worker self-report.
- Summarize delegated worker notes and reviewer audit files into agent_timeline.jsonl instead of asking delegated agents to append directly.
- For routine local work, record a concise self-check and any residual risk.
- Save a persistent audit file for every stage, including routine local stages.
- Do not use sub-agents for mechanical work that the coordinator can complete directly.
- If reviewer is inconclusive, treat as at least WARNING; if progression risk is material, treat as PROBLEM.

## Coordinator Never Does
- Never launch a worker sub-agent for environment setup or other straightforward tasks without a clear need.
- Never let a delegated worker review its own work.
- Never approve a critical analysis step without independent review.
