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
  DATA_PROVENANCE -> SPEC_FEASIBILITY -> IMPLEMENTATION_DESIGN -> EXECUTE -> NUMERICAL_SANITY -> CLAIM_REVIEW -> FINALIZE -> FINAL_ARTIFACT_REVIEW -> FINAL_CLAIM_REVIEW.
- The coordinator may split EXECUTE into domain-specific stages, but it must not skip DATA_PROVENANCE, SPEC_FEASIBILITY, CLAIM_REVIEW, FINALIZE, FINAL_ARTIFACT_REVIEW, or FINAL_CLAIM_REVIEW when final physics claims are requested.

## Claim Discipline
- Treat the analysis JSON or paper summary as the faithful reference specification; do not edit it to describe open-data substitutions.
- If a reference ingredient is unavailable, the agent may implement a documented diagnostic replacement, but the replacement does not inherit the reference paper claim.
- Every final result must have a claim classification: reproduction, reinterpretation, diagnostic_proxy, or blocked.
- Paper-level observed significances, exclusions, mass limits, or cross-section limits are allowed only when the feasibility matrix and claim review support that classification.
- Smoke or capped runs validate code only. They must never be copied, summarized, or promoted as final physics outputs.
- Pseudo-observed data may be processed as diagnostics only; pseudo-observed numbers must not be headlined, summarized, or phrased as observed physics results.
- Negative or signed MC yields that are clipped, floored, or otherwise stabilized for a statistic force the affected result to diagnostic_proxy or blocked unless a reviewed statistical model justifies the treatment.

## DATA_PROVENANCE Gate
- Before implementation, create artifacts/data_provenance/data_provenance.json.
- Classify every input-data/data ROOT file as real_observed_collision_data, pseudo_observed_mc_like_data, or unusable.
- Record filename evidence, tree/schema evidence, branch evidence, event-weight or metadata evidence when available, and the decision rule.
- Include a top-level observed_claims_allowed boolean and a short reason.
- Treat DATA_PROVENANCE as critical_analysis when any observed result, discovery significance, limit, or data/MC comparison may be reported.
- Require independent review of the data provenance artifact before observed results are computed or reported.
- If data provenance is pseudo_observed_mc_like_data, unavailable, mixed, or inconclusive, observed paper-level claims are blocked. Pseudo-observed values may appear only as clearly labeled diagnostic_proxy outputs.

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
- For paper-reproduction or JSON-spec-driven analyses, place DATA_PROVENANCE and SPEC_FEASIBILITY before implementation and FINALIZE after claim review.
- Assign a stable agent_tag for the coordinator's local work or for each delegated worker/reviewer planned for this stage.
- Classify the next stage as routine or critical_analysis before execution.
- Treat environment setup, file preparation, dependency checks, and other straightforward tasks as routine unless they materially affect analysis conclusions.
- Treat stages that materially affect physics conclusions, fit behavior, uncertainty treatment, or progression safety as critical_analysis.
- Log that inferred plan as the first decision entry in agent_timeline.jsonl.
- Include a brief rationale for the decomposition so later failures can be traced to stage-planning choices.
- Write handoff/<stage>/local_brief.txt before routine local execution.
- The local brief must include: role, agent_tag, stage, exact task, required input files, required output paths, local audit criteria.
- Write the required worker brief before spawning a worker for a critical_analysis stage.
- For critical_analysis stages, write handoff/<stage>/reviewer_brief_draft.txt during PLAN only when preliminary reviewer scope is useful.
- Log a decision entry in agent_timeline.jsonl.
- If budget is tight or critical, explicitly reduce review scope and log it.

## EXECUTE
- For routine stages, the coordinator executes locally from handoff/<stage>/local_brief.txt and produces the required outputs, plots, and concise notes.
- For critical_analysis stages, spawn one worker for the current stage.
- Include the assigned worker agent_tag in the spawn prompt and immediately record the spawned agent_id and tag in codex_sessions.json.
- A delegated worker must produce stage outputs, diagnostic plots, and concise notes on assumptions and risks.
- For critical_analysis stages, finalize handoff/<stage>/reviewer_brief.txt after execution with actual outputs, plots, numerical summaries, and worker risk notes.
- Log local_execute for routine stages or spawn and complete for delegated stages; the coordinator writes all agent_timeline.jsonl entries.

## AUDIT
- For routine stages, perform a concise local self-check, save findings to reviews/<stage>/review_<cycle>.json using the shared audit schema with audit_mode local_self_check, and log local_audit.
- For critical_analysis stages, spawn a separate reviewer for the same stage.
- Include the assigned reviewer agent_tag in the spawn prompt and immediately record the spawned agent_id and tag in codex_sessions.json.
- Use a vision-capable reviewer whenever plots/images exist.
- Reviewer must inspect requested plots visually and check numerical outputs.
- Reviewer saves findings to reviews/<stage>/review_<cycle>.json using the shared audit schema with audit_mode independent_review.
- Log local_audit for routine stages or spawn and complete for delegated stages; summarize reviewer findings into agent_timeline.jsonl after reading the saved review file.

## REPAIR
- If a routine-stage self-check reports any PROBLEM, repair locally, save updated outputs, and rerun the local self-check with a fresh audit file.
- If review reports any PROBLEM on a critical_analysis stage, spawn a new worker for repair.
- If review reports WARNING with can_proceed true, proceed only as degraded and record the warning in downstream_notes or global_risks.
- A WARNING that changes a physics number, region definition, sample role, data provenance decision, or claim scope requires repair or an explicit degraded claim classification before proceeding.
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
- Verify every result against artifacts/data_provenance/data_provenance.json, artifacts/spec_feasibility/reference_feasibility_matrix.json, and the implemented runtime artifacts.
- Mark a result blocked when it depends on unavailable critical ingredients, clipped negative yields, zero usable signal proxy, invalid or unstable background models, unsupported observed data, or partial/capped inputs.
- Observed results must be computed only after the expected workflow is fixed and must be labeled separately from expected results.
- If observed data are unavailable or are actually MC-like files, observed discovery or limit claims must be blocked or explicitly labeled pseudo-observed diagnostic results.
- If a statistic uses clipped, floored, or nonnegative-stabilized signed MC yields, classify that statistic as diagnostic_proxy or blocked and explain the raw signed yields and stabilization rule.
- For mutually exclusive regions or categories, verify a mask sanity artifact that records event counts and overlap checks; identical yields across supposedly distinct regions require repair or a blocked result.
- Create artifacts/claim_review/report_number_trace.json mapping every numerical value or final claim printed in the report to its source artifact, source JSON path or table row, claim classification, and allowed_in_final_report boolean.
- Update outputs/evaluation_scorecard.json with the claim-review status, report-number-trace status, and allowed or blocked final-claim scope.

## FINALIZE Gate
- Before writing or approving a final report, create artifacts/finalize/finalization_gate.json.
- The finalization gate must fail if any of these are true:
  - a smoke, test, capped, or partial-statistics run is being promoted as final without an explicit user request for partial-only results;
  - not all usable samples were processed, or progress/status artifacts do not show completion;
  - the final report source is not the full production run;
  - artifacts/data_provenance/data_provenance.json is missing, inconclusive, or not independently reviewed before observed results are reported;
  - expected results were not computed before observed results where blinding or signal-sensitive regions apply;
  - a result lacks claim classification;
  - observed significance, limits, mass limits, or exclusions are printed for blocked or diagnostic-only regions as paper-level claims;
  - pseudo-observed values are headlined, summarized, or phrased as observed physics results;
  - negative or signed MC yields were silently clipped and then used to print significance or limits;
  - mutually exclusive region or category masks lack an overlap sanity check, or supposedly distinct regions have identical yields without a reviewed explanation;
  - the background model, signal model, or observed-data source is invalid for the printed claim.
- If the gate fails, write a blocked or diagnostic report instead of a paper-like final result, and record the failed checks in analysis_state.json and agent_timeline.jsonl.
- Update outputs/evaluation_scorecard.json with the finalization status before any final review is spawned.

## FINAL_ARTIFACT_REVIEW Gate
- After FINALIZE, spawn a fresh independent reviewer whose only task is artifact and run-integrity review.
- The artifact reviewer must not be the coordinator, any implementation worker, or any reviewer whose earlier approval is being relied on for final artifact integrity.
- Use an adversarial brief: the reviewer is trying to find missing, stale, partial, contradictory, or non-reproducible artifacts.
- Required artifact-review inputs include the prompt, analysis_state.json, codex_sessions.json, outputs/evaluation_scorecard.json, artifacts/data_provenance/data_provenance.json, artifacts/spec_feasibility/reference_feasibility_matrix.json, artifacts/claim_review/claim_classification.json, artifacts/claim_review/report_number_trace.json, artifacts/finalize/finalization_gate.json, the production run manifest, sample registry, yields, statistics, plot manifest, selected plots, reproducibility commands, and final report.
- The artifact reviewer must verify that outputs/evaluation_scorecard.json agrees with the source artifacts, that the production run processed all usable samples or is explicitly blocked, that no smoke/capped/partial run is promoted as final, that plot files exist and are inspectable when plots exist, and that every final report number is present in artifacts/claim_review/report_number_trace.json.
- The artifact reviewer must write reviews/final_artifact_review/review_<cycle>.json using the final-artifact-review schema from multiagent-hep-reviewing-stage-outputs.
- If the artifact review finds any PROBLEM, do not proceed to FINAL_CLAIM_REVIEW. Mark the relevant upstream stage needs_revisit, spawn a repair worker or repair locally as appropriate, rerun the affected stage and all downstream gates from CLAIM_REVIEW onward, then rerun FINAL_ARTIFACT_REVIEW with a fresh cycle.
- If the artifact review finds any WARNING that changes a physics number, region definition, sample role, data provenance decision, claim classification, final report source, reproducibility status, or handoff scope, repair or explicitly degrade the affected claim, rerun CLAIM_REVIEW and FINALIZE, then rerun FINAL_ARTIFACT_REVIEW.

## FINAL_CLAIM_REVIEW Gate
- After FINAL_ARTIFACT_REVIEW passes or conditionally passes with handoff-compatible limitations, spawn a separate fresh independent reviewer whose only task is final claim and report-scope review.
- The claim reviewer must not be the coordinator, any implementation worker, the final artifact reviewer, or any reviewer whose earlier approval is being relied on for the final claim.
- Use an adversarial brief: the reviewer is trying to find overclaims, misleading wording, unsupported numbers, pseudo-observed misuse, or paper-level claims that should be blocked.
- Required claim-review inputs include all FINAL_ARTIFACT_REVIEW inputs plus reviews/final_artifact_review/review_<cycle>.json.
- The claim reviewer must verify that every headline result and every numerical report claim traces through artifacts/claim_review/report_number_trace.json to a machine-readable source artifact, that report wording matches the weakest valid claim classification, and that outputs/evaluation_scorecard.json agrees with the allowed handoff scope.
- The claim reviewer must inspect selected plots visually when plots exist and check that captions and conclusions do not overstate diagnostic or blocked outputs.
- The claim reviewer must write reviews/final_claim_review/review_<cycle>.json using the final-claim-review schema from multiagent-hep-reviewing-stage-outputs.
- Final handoff is allowed only when FINAL_ARTIFACT_REVIEW and FINAL_CLAIM_REVIEW have no PROBLEM findings, the final claim review sets handoff_allowed true, and outputs/evaluation_scorecard.json records handoff_allowed true.
- If the claim review finds any PROBLEM, do not hand off. Mark the relevant upstream stage needs_revisit, spawn a repair worker or repair locally as appropriate, rerun the affected stage and all downstream gates from CLAIM_REVIEW onward, then rerun FINAL_ARTIFACT_REVIEW and FINAL_CLAIM_REVIEW with fresh cycles.
- If the claim review finds any WARNING that changes a physics number, region definition, sample role, data provenance decision, claim classification, final report wording, or handoff scope, repair or explicitly degrade the affected claim, rerun CLAIM_REVIEW and FINALIZE, then rerun both final reviews.
- If both final reviews find only documented limitations that do not change claim scope, the coordinator may proceed as degraded only if the final claim review explicitly sets handoff_allowed true and records the allowed claim scope.

## Upstream Revisit Rule
- If the required audit finds that the root cause is in an earlier stage, do not continue forward.
- Log a decision naming the upstream stage that must be revisited.
- Mark that earlier stage needs_revisit in analysis_state.json.
- Re-run that earlier stage through the full loop before resuming downstream work.

## Routine Local Brief Template
```text
stage: <stage>
agent_tag: <tag assigned by coordinator>
exact task: <stage goal and specific artifacts to produce>
required input files:
- <path>
required output paths:
- artifacts/<stage>/<file>
local audit criteria:
- <criterion>
```
