---
name: multiagent-hep-managing-file-layout
description: Supporting skill for the multiagent HEP workflow. Use only after multiagent-hep-coordinating-analysis is active, when creating or referencing handoffs, artifacts, audits, state files, or timeline files.
---

# Multiagent HEP Managing File Layout

## Purpose
Used by any agent that creates, reads, or references persistent workflow files.

## See also
- [multiagent-hep-managing-analysis-state](../multiagent-hep-managing-analysis-state/SKILL.md)
- [multiagent-hep-logging-agent-timeline](../multiagent-hep-logging-agent-timeline/SKILL.md)
- [multiagent-hep-executing-worker-stage](../multiagent-hep-executing-worker-stage/SKILL.md)
- [multiagent-hep-reviewing-stage-outputs](../multiagent-hep-reviewing-stage-outputs/SKILL.md)

## Required Files
- analysis_state.json
- agent_timeline.jsonl
- handoff/<stage>/local_brief.txt for routine stages
- handoff/<stage>/worker_brief.txt for delegated critical_analysis stages
- handoff/<stage>/reviewer_brief_draft.txt during PLAN for delegated critical_analysis stages
- handoff/<stage>/reviewer_brief.txt finalized after EXECUTE for delegated critical_analysis stages
- artifacts/<stage>/
- artifacts/spec_feasibility/reference_feasibility_matrix.json for paper-reproduction or JSON-spec-driven analyses
- artifacts/claim_review/claim_classification.json before finalization
- artifacts/finalize/finalization_gate.json before final report approval
- reviews/<stage>/review_<cycle>.json for every stage audit

## Path Conventions
- Pass context by file path, not pasted text.
- All outputs must go under artifacts/<stage>/.
- Write handoff/<stage>/local_brief.txt before routine local execution.
- Write handoff/<stage>/worker_brief.txt before spawning a worker.
- Write handoff/<stage>/reviewer_brief_draft.txt during PLAN if reviewer scope is already known.
- Finalize handoff/<stage>/reviewer_brief.txt after EXECUTE using actual outputs, plots, and worker risk notes.
- Save each stage audit to reviews/<stage>/review_<cycle>.json.
- Use the shared audit schema for both local self-checks and independent reviews.
- Keep smoke, capped, and production outputs in clearly separate output directories.
- Do not copy smoke or capped outputs into final report paths unless the user explicitly requested partial-only output and the path/report label says so.
- Always use forward slashes.
