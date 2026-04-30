---
name: multiagent-hep-running-stage-loop
description: Supporting skill for the multiagent HEP coordinator. Use only after multiagent-hep-coordinating-analysis is active, when advancing a staged workflow through planning, execution, audit, repair, and progression decisions.
---

# Multiagent HEP Running Stage Loop

## Purpose
Used by the coordinator when advancing any stage through planning, execution, audit, repair, and progression.

## See also
- [multiagent-hep-coordinating-analysis](../multiagent-hep-coordinating-analysis/SKILL.md)
- [multiagent-hep-logging-agent-timeline](../multiagent-hep-logging-agent-timeline/SKILL.md)
- [multiagent-hep-executing-worker-stage](../multiagent-hep-executing-worker-stage/SKILL.md)
- [multiagent-hep-reviewing-stage-outputs](../multiagent-hep-reviewing-stage-outputs/SKILL.md)
- [multiagent-hep-managing-analysis-budget](../multiagent-hep-managing-analysis-budget/SKILL.md)

## Loop
- For every stage, run PLAN -> EXECUTE -> AUDIT -> REPAIR -> PROCEED.
- Default max repair retries per stage: 3.
- A stage is approved only when the required audit reports no WARNING or PROBLEM.
- The first audit for a stage is cycle 1; increment the cycle before each fresh audit after repair.
- If retry limit is hit, mark the stage blocked, degraded, or needs_revisit and record consequences before continuing.
- For paper-reproduction or JSON-spec-driven analyses, the workflow must include these hard gates before any final report can be approved:
  SPEC_FEASIBILITY -> IMPLEMENTATION_DESIGN -> EXECUTE -> NUMERICAL_SANITY -> CLAIM_REVIEW -> FINALIZE.
- The coordinator may split EXECUTE into domain-specific stages, but it must not skip SPEC_FEASIBILITY, CLAIM_REVIEW, or FINALIZE when final physics claims are requested.

## Claim Discipline
- Treat the analysis JSON or paper summary as the faithful reference specification; do not edit it to describe open-data substitutions.
- If a reference ingredient is unavailable, the agent may implement a documented diagnostic replacement, but the replacement does not inherit the reference paper claim.
- Every final result must have a claim classification: reproduction, reinterpretation, diagnostic_proxy, or blocked.
- Paper-level observed significances, exclusions, mass limits, or cross-section limits are allowed only when the feasibility matrix and claim review support that classification.
- Smoke or capped runs validate code only. They must never be copied, summarized, or promoted as final physics outputs.

## SPEC_FEASIBILITY Gate
- Before implementation, create artifacts/spec_feasibility/reference_feasibility_matrix.json.
- Classify each critical reference requirement as available, substituted, unavailable, or not_applicable.
- For each substituted or unavailable requirement, record evidence, the proposed replacement if any, expected analysis impact, allowed_claims, and blocked_claims.
- Include checks for sample roles, real observed data availability, trigger/object branch availability, signal samples, control/fake/background methods, statistical model ingredients, and systematic inputs when relevant.
- Treat SPEC_FEASIBILITY as critical_analysis unless the user explicitly requested a purely mechanical exercise.
- Require independent review of the feasibility matrix before downstream implementation begins.
- If a critical paper ingredient is unavailable, continue only with an explicitly diagnostic or reinterpretation claim path, or mark the workflow blocked.

## PLAN
- Decide the next stage, required outputs, and required diagnostic plots.
- If the task does not define stages, infer a reasonable staged decomposition first.
- For paper-reproduction or JSON-spec-driven analyses, place SPEC_FEASIBILITY before implementation and FINALIZE after claim review.
- Classify the next stage as routine or critical_analysis before execution.
- Treat environment setup, file preparation, dependency checks, and other straightforward tasks as routine unless they materially affect analysis conclusions.
- Treat stages that materially affect physics conclusions, fit behavior, uncertainty treatment, or progression safety as critical_analysis.
- Log that inferred plan as the first decision entry in agent_timeline.jsonl.
- Include a brief rationale for the decomposition so later failures can be traced to stage-planning choices.
- Write handoff/<stage>/local_brief.txt before routine local execution.
- The local brief must include: stage, exact task, required input files, required output paths, local audit criteria.
- Write the required worker brief before spawning a worker for a critical_analysis stage.
- For critical_analysis stages, write handoff/<stage>/reviewer_brief_draft.txt during PLAN only when preliminary reviewer scope is useful.
- Log a decision entry in agent_timeline.jsonl.
- If budget is tight or critical, explicitly reduce review scope and log it.

## EXECUTE
- For routine stages, the coordinator executes locally from handoff/<stage>/local_brief.txt and produces the required outputs, plots, and concise notes.
- For critical_analysis stages, spawn one worker for the current stage.
- A delegated worker must produce stage outputs, diagnostic plots, and concise notes on assumptions and risks.
- For critical_analysis stages, finalize handoff/<stage>/reviewer_brief.txt after execution with actual outputs, plots, numerical summaries, and worker risk notes.
- Log local_execute for routine stages or spawn and complete for delegated stages; the coordinator writes all agent_timeline.jsonl entries.

## AUDIT
- For routine stages, perform a concise local self-check, save findings to reviews/<stage>/review_<cycle>.json using the shared audit schema with audit_mode local_self_check, and log local_audit.
- For critical_analysis stages, spawn a separate reviewer for the same stage.
- Use a vision-capable reviewer whenever plots/images exist.
- Reviewer must inspect requested plots visually and check numerical outputs.
- Reviewer saves findings to reviews/<stage>/review_<cycle>.json using the shared audit schema with audit_mode independent_review.
- Log local_audit for routine stages or spawn and complete for delegated stages; summarize reviewer findings into agent_timeline.jsonl after reading the saved review file.

## REPAIR
- If a routine-stage self-check reports any PROBLEM, repair locally, save updated outputs, and rerun the local self-check with a fresh audit file.
- If review reports any PROBLEM on a critical_analysis stage, spawn a new worker for repair.
- If review reports WARNING with can_proceed true, proceed only as degraded and record the warning in downstream_notes or global_risks.
- Repair worker must read the latest review file before acting.
- Repair worker must address only the cited findings plus necessary adjacent fixes.
- After delegated repair, spawn a fresh reviewer.
- Repeat until no PROBLEM remains or retry limit is reached.
- Log local_repair for routine stages or repair, spawn, and complete for delegated stages.

## PROCEED
- Update analysis_state.json.
- Collapse completed stages to one-line summaries.
- Advance only after the required audit reports no PROBLEM; WARNING requires degraded status, while PROBLEM requires repair or blocked/needs_revisit status.

## CLAIM_REVIEW Gate
- Before finalization, create artifacts/claim_review/claim_classification.json mapping every reported result to reproduction, reinterpretation, diagnostic_proxy, or blocked.
- Verify every result against artifacts/spec_feasibility/reference_feasibility_matrix.json and the implemented runtime artifacts.
- Mark a result blocked when it depends on unavailable critical ingredients, clipped negative yields, zero usable signal proxy, invalid or unstable background models, unsupported observed data, or partial/capped inputs.
- Observed results must be computed only after the expected workflow is fixed and must be labeled separately from expected results.
- If observed data are unavailable or are actually MC-like files, observed discovery or limit claims must be blocked or explicitly labeled pseudo-observed diagnostic results.

## FINALIZE Gate
- Before writing or approving a final report, create artifacts/finalize/finalization_gate.json.
- The finalization gate must fail if any of these are true:
  - a smoke, test, capped, or partial-statistics run is being promoted as final without an explicit user request for partial-only results;
  - not all usable samples were processed, or progress/status artifacts do not show completion;
  - the final report source is not the full production run;
  - expected results were not computed before observed results where blinding or signal-sensitive regions apply;
  - a result lacks claim classification;
  - observed significance, limits, mass limits, or exclusions are printed for blocked or diagnostic-only regions as paper-level claims;
  - negative or signed MC yields were silently clipped and then used to print significance or limits;
  - the background model, signal model, or observed-data source is invalid for the printed claim.
- If the gate fails, write a blocked or diagnostic report instead of a paper-like final result, and record the failed checks in analysis_state.json and agent_timeline.jsonl.

## Upstream Revisit Rule
- If the required audit finds that the root cause is in an earlier stage, do not continue forward.
- Log a decision naming the upstream stage that must be revisited.
- Mark that earlier stage needs_revisit in analysis_state.json.
- Re-run that earlier stage through the full loop before resuming downstream work.

## Routine Local Brief Template
```text
stage: <stage>
exact task: <stage goal and specific artifacts to produce>
required input files:
- <path>
required output paths:
- artifacts/<stage>/<file>
local audit criteria:
- <criterion>
```
