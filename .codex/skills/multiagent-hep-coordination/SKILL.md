---
name: multiagent-hep-coordination
description: "Single entrypoint package for coordinated multiagent HEP analysis workflows. Use when a HEP run needs staged local/delegated execution, persistent state, reviewer audits, repair cycles, final quality review, scorecard/test-summary consistency, and session tracking without loading many separate coordination skills."
---

# Multiagent HEP Coordination

Use this as the only multiagent HEP coordination entrypoint. It handles the workflow mechanics; physics quality gates come from the analysis spec, HEP skills, `hep-root-runtime-repair`, `hep-analysis-evaluation-scorecard`, and `hep-final-quality-review`.

## Core Rules

- Act as COORDINATOR.
- Keep routine setup local; delegate critical analysis and review work.
- Never let a worker review its own work.
- Use file references in handoff briefs, not pasted logs.
- Maintain `analysis_state.json`, `codex_sessions.json`, `agent_timeline.jsonl`, `handoff/`, and `reviews/`.
- Do not hand off final results until independent final review and scorecard/test-summary checks pass.

## Stage Spine

For paper-reproduction, reinterpretation, or JSON-spec-driven HEP analyses, run:

```text
RUNTIME_REPAIR when ROOT-backed capability is required or missing
DATA_PROVENANCE
SPEC_FEASIBILITY
IMPLEMENTATION_DESIGN
EXECUTE
NUMERICAL_SANITY
CLAIM_REVIEW
FINALIZE
FINAL_ARTIFACT_REVIEW
FINAL_CLAIM_REVIEW
```

`RUNTIME_REPAIR` uses `hep-root-runtime-repair`. Final review uses `hep-final-quality-review`.

## Load References As Needed

- [stage-loop.md](references/stage-loop.md): PLAN -> EXECUTE -> AUDIT -> REPAIR -> PROCEED mechanics and required gates.
- [delegation-state.md](references/delegation-state.md): state files, session registry, timeline, handoff briefs.
- [review-contracts.md](references/review-contracts.md): shared review schema and mandatory veto classes.
- [final-review-handoff.md](references/final-review-handoff.md): final artifact review, final claim review, and handoff requirements.

## Handoff Rule

Final handoff is allowed only when:

- no required stage is skipped;
- all critical stages are independently reviewed or explicitly blocked;
- `outputs/evaluation_scorecard.json` and `outputs/test_outcome_summary.json` agree;
- runtime repair evidence exists when ROOT-backed fallback/blocking was needed;
- sample scope, number trace, plots, claims, and reproducibility pass final quality review.
