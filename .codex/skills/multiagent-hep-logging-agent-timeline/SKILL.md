---
name: multiagent-hep-logging-agent-timeline
description: Supporting skill for the multiagent HEP coordinator. Use only after multiagent-hep-coordinating-analysis is active, when the coordinator records decisions, execution, audits, repairs, delegated lifecycle events, findings, or summaries.
---

# Multiagent HEP Logging Agent Timeline

## Purpose
Used by the coordinator as the only canonical writer to the shared timeline log.

## See also
- [multiagent-hep-running-stage-loop](../multiagent-hep-running-stage-loop/SKILL.md)
- [multiagent-hep-managing-file-layout](../multiagent-hep-managing-file-layout/SKILL.md)

## Format
- The coordinator appends one JSON object per line to agent_timeline.jsonl.
- Workers and reviewers do not append directly; they emit required stage notes, artifacts, or review files for the coordinator to summarize.

## Required Schema
```json
{
"timestamp": "<ISO 8601 or sequential index>",
"agent_role": "coordinator|worker|reviewer",
"agent_id": "<unique id>",
"stage": "<stage>",
"action": "spawn|complete|finding|decision|repair|summary|local_execute|local_audit|local_repair",
"detail": "<concise description>",
"inputs": ["<path>"],
"outputs": ["<path>"],
"token_note": "<optional short note>"
}
```

## Logging Rules
- Coordinator must log every decision, local_execute, local_audit, local_repair, spawn, completion, repair, and final summary.
- Use spawn and complete for delegated worker and reviewer lifecycle events.
- Use local_execute, local_audit, and local_repair for coordinator-run routine-stage work.
- Use finding entries to summarize worker notes and reviewer audit findings after reading their output files.
- Workers and reviewers must not write agent_timeline.jsonl directly.
- For delegated entries, agent_role identifies the delegated role being summarized while the coordinator remains the writer.

## Final Summary Entry
- Include total agents spawned.
- Include total audit-repair cycles.
- Include stages retried.
- Include stages revisited upstream.
- Include stages with reduced review scope.
