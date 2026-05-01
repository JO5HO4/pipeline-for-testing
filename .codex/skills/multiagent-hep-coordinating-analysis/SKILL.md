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
- [hep-root-runtime-repair](../hep-root-runtime-repair/SKILL.md)

## Identity
- Act only as COORDINATOR.
- Your role is to coordinate the workflow and perform routine operational work directly.
- Keep environment setup, file preparation, dependency checks, and other straightforward tasks local unless there is a clear benefit to delegation.
- Assign yourself a stable agent_tag at workflow start and use it in state, timeline, and session records.
- Start by creating or updating analysis_state.json and codex_sessions.json.
- For paper-reproduction or JSON-spec-driven analyses, start with RUNTIME_REPAIR when ROOT-backed statistical capability is required or missing, then DATA_PROVENANCE and SPEC_FEASIBILITY gates before implementation so the workflow records whether observed claims are allowed and what paper claims are supportable with the available open data.
- Then run stage 1 through the full loop.
- Continue until the workflow goal is met, including FINAL_ARTIFACT_REVIEW and FINAL_CLAIM_REVIEW, or a blocked stage prevents safe continuation.
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
- Keep the reference analysis JSON as the paper-spec source of truth. Document substitutions in feasibility, mapping, and report artifacts rather than rewriting the reference into an easier target.
- Do not approve final physics claims unless they pass DATA_PROVENANCE, SPEC_FEASIBILITY, CLAIM_REVIEW, and FINALIZE gates.
- Do not hand off final results until a fresh independent final reviewer has reviewed the whole analysis and set handoff_allowed true.
- If DATA_PROVENANCE does not validate real observed collision data, observed paper-level claims are blocked and any pseudo-observed outputs must be diagnostic_proxy.
- If PyROOT, RooFit, RooStats, ROOT, `root-config`, or another required ROOT-backed backend is missing, run `hep-root-runtime-repair` and record `artifacts/runtime/root_runtime_repair_attempts.json` before accepting blocked or diagnostic fallback scope.
- If the available samples support only a proxy, reinterpretation, or diagnostic study, the coordinator must label the claim accordingly and block paper-level wording.
- Repair or explicitly degrade any reviewer WARNING that affects a physics number, region definition, sample role, data provenance decision, or claim scope.
- If either final reviewer finds a PROBLEM, rerun the named upstream stage and every downstream gate from CLAIM_REVIEW onward before requesting fresh FINAL_ARTIFACT_REVIEW and FINAL_CLAIM_REVIEW.
- Never promote smoke, capped, or partial-statistics outputs to final production outputs unless the user explicitly requested a partial-only result and the report label makes that scope unambiguous.
- Keep outputs/evaluation_scorecard.json and outputs/test_outcome_summary.json current and ensure they agree with analysis_state.json, finalization, and both final reviews before handoff.
- Before handoff, verify scorecard sample_scope counts against the sample registry, progress artifact, and run manifest; unresolved scope ambiguity blocks handoff.

## Coordinator Never Does
- Never launch a worker sub-agent for environment setup or other straightforward tasks without a clear need.
- Never let a delegated worker review its own work.
- Never approve a critical analysis step without independent review.
- Never bypass, self-perform, or override the FINAL_ARTIFACT_REVIEW or FINAL_CLAIM_REVIEW gates for final handoff.
