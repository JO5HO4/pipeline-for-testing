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
These files must exist or be referenced when relevant; not every agent should read every file.

- analysis_state.json
- codex_sessions.json
- agent_timeline.jsonl
- outputs/evaluation_scorecard.json for run-quality summary and handoff status
- outputs/test_outcome_summary.json for compact final status, claim permission, blockers, and headline diagnostic numbers
- handoff/<stage>/local_brief.txt for routine stages
- handoff/<stage>/worker_brief.txt for delegated critical_analysis stages
- handoff/<stage>/reviewer_brief_draft.txt during PLAN for delegated critical_analysis stages
- handoff/<stage>/reviewer_brief.txt finalized after EXECUTE for delegated critical_analysis stages
- artifacts/<stage>/
- reviews/<stage>/review_<cycle>.json for every stage audit

## Path Conventions
- Pass context by file path, not pasted text.
- codex_sessions.json lives at the workflow root and is the canonical registry of coordinator, worker, and reviewer sessions.
- codex_sessions.json is a coordinator-maintained pointer artifact. Workers and reviewers should not read it unless their brief explicitly requires it.
- codex_sessions.json may record absolute read-only rollout paths under ~/.codex/sessions or ~/.codex/archived_sessions, but do not copy rollout contents into the project or paste rollout contents into prompts.
- All outputs must go under artifacts/<stage>/.
- Write handoff/<stage>/local_brief.txt before routine local execution.
- Write handoff/<stage>/worker_brief.txt before spawning a worker.
- Write handoff/<stage>/reviewer_brief_draft.txt during PLAN if reviewer scope is already known.
- Finalize handoff/<stage>/reviewer_brief.txt after EXECUTE using actual outputs, plots, and worker risk notes.
- Save each stage audit to reviews/<stage>/review_<cycle>.json.
- Save final artifact reviews to reviews/final_artifact_review/review_<cycle>.json and final claim reviews to reviews/final_claim_review/review_<cycle>.json.
- Use the shared audit schema for both local self-checks and independent reviews.
- Always use forward slashes.
- Paths written into scorecard and summary artifacts must be repo-root-relative.
