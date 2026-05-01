---
name: multiagent-hep-logging-agent-timeline
description: Supporting skill for the multiagent HEP coordinator. Use only after multiagent-hep-coordinating-analysis is active, when the coordinator records decisions, execution, audits, repairs, delegated lifecycle events, session and rollout records, findings, or summaries.
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
- Entries that refer to an agent must include the stable agent_tag when known.

## Required Schema
```json
{
"timestamp": "<ISO 8601 or sequential index>",
"agent_role": "coordinator|worker|reviewer",
"agent_id": "<unique id>",
"agent_tag": "<stable human-readable tag>",
"stage": "<stage>",
"action": "spawn|complete|finding|decision|repair|summary|local_execute|local_audit|local_repair|session_update",
"detail": "<concise description>",
"inputs": ["<path>"],
"outputs": ["<path>"],
"rollout_files": ["<absolute rollout jsonl path when known>"],
"token_note": "<optional short note>"
}
```

## Logging Rules
- Coordinator must log every decision, local_execute, local_audit, local_repair, spawn, completion, repair, session_update, and final summary.
- Use spawn and complete for delegated worker and reviewer lifecycle events.
- Use session_update whenever codex_sessions.json is created, refreshed, or gains rollout-file evidence.
- Use local_execute, local_audit, and local_repair for coordinator-run routine-stage work.
- Use finding entries to summarize worker notes and reviewer audit findings after reading their output files.
- Workers and reviewers must not write agent_timeline.jsonl directly.
- For delegated entries, agent_role identifies the delegated role being summarized while the coordinator remains the writer.

## Codex Session Registry
- The coordinator maintains codex_sessions.json as the canonical registry of all Codex sessions participating in the workflow.
- Treat codex_sessions.json as a compact pointer artifact, not context to load into prompts.
- Assign a stable agent_tag to the coordinator and to every worker or reviewer before it starts work.
- Use short tags that include role, stage, cycle, and sequence when applicable, for example coordinator, worker:selection:c1:n1, reviewer:fit:c2:n1.
- Include the assigned agent_tag in every sub-agent prompt, handoff brief, worker note, and reviewer audit where practical.
- Refresh codex_sessions.json at workflow start, after every spawn, after every delegated completion, and before the final summary.
- Discover rollout files by checking ~/.codex/sessions/**/*.jsonl and ~/.codex/archived_sessions/rollout-*.jsonl with filename-only shell output.
- Prefer exact rollout matches found by searching for the agent_tag with tools such as `rg -l --fixed-strings`; never print or paste rollout JSONL contents.
- Record rollout file paths only; do not copy full rollout contents into the workflow artifacts.
- Keep at most five candidate_rollout_files per agent; if there are more, record a short note and leave rollout_match_status as missing or candidate.
- If the exact rollout file cannot be identified, record candidate_rollout_files with the reason and set rollout_match_status to candidate or missing.
- Workers and reviewers should not read codex_sessions.json; their assigned tag in the brief is sufficient.

## Required codex_sessions.json Shape
```json
{
"registry_version": 1,
"updated_at": "<ISO 8601 timestamp>",
"rollout_search_roots": ["~/.codex/sessions", "~/.codex/archived_sessions"],
"agents": [
  {
    "agent_tag": "<stable tag>",
    "agent_role": "coordinator|worker|reviewer",
    "agent_id": "<tool/session id when available>",
    "stage": "<stage or workflow>",
    "status": "planned|running|completed|closed|blocked|unknown",
    "spawned_at": "<ISO 8601 timestamp or null>",
    "completed_at": "<ISO 8601 timestamp or null>",
    "brief_path": "<handoff path or null>",
    "outputs": ["<path>"],
    "rollout_files": ["<absolute rollout jsonl path>"],
    "candidate_rollout_files": ["<absolute rollout jsonl path>"],
    "rollout_match_status": "matched|candidate|missing",
    "notes": "<short note>"
  }
]
}
```

## Final Summary Entry
- Include total agents spawned.
- Include path to codex_sessions.json and total matched rollout files.
- Include total audit-repair cycles.
- Include stages retried.
- Include stages revisited upstream.
- Include stages with reduced review scope.
