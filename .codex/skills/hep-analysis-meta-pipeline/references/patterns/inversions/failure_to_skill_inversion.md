# Failure-to-Skill Inversion

Pattern: Inversion

Derived from:
- `SKILL_EXTRACT_NEW_SKILL_FROM_FAILURE`
- `SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK`

## Trigger condition

Use this inversion when a reviewer finds a recurring failure, a discrepancy remains unresolved, or the workflow uncovers a missing reusable capability.

## Decision structure

1. Classify the failure as one of:
   - implementation defect
   - missing evidence or logging
   - scientific ambiguity requiring human input
   - repeated workflow pattern that should become a reusable skill
2. Identify the smallest component that owns the problem.
3. Decide whether to repair locally, escalate, or propose a new skill.

## Branch criteria

- Single-run implementation bug: route to the owning wrapper or generator.
- Missing evidence: route to the reviewer-paired generator or pipeline stage.
- Scientific ambiguity without repository evidence: escalate to a human.
- Repeated failure with reusable structure: write a candidate skill note and include it in the handoff package.

## Required evidence per branch

- reviewer findings
- blocked artifacts
- prior run history or repeated occurrence evidence
- current assumptions and deviation logs

## Output decision record

Record:

- failure class
- owning component
- smallest remediation path
- whether a new skill candidate should be proposed
- whether human escalation is required

## Verification Gate

### ASSERTIONS

1. A decision record exists before the inversion hands off, and it records the failure class, owning component, smallest remediation path, whether a new skill candidate should be proposed, and whether human escalation is required.
2. The evidence supporting the failure classification includes reviewer findings, blocked artifacts, prior run history or repeated occurrence evidence, and the current assumptions and deviation logs.
3. If the failure class is scientific ambiguity without repository evidence, the decision record explicitly records human escalation rather than pretending the ambiguity was resolved locally.

### REPAIR

- Soft failure: rerun `failure_to_skill_inversion.md` after collecting the missing reviewer findings, blocked artifacts, or run-history evidence, then rerun this gate.
- Hard failure: return to Stage 8 or Stage 10 of `hep_analysis_meta_pipeline.md`, depending on where the failure was detected; if the owning component or escalation path cannot be named, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: failure_to_skill_inversion
assertions_checked:
  - assertion_1
  - assertion_2
  - assertion_3
assertion_results:
  assertion_1: pass|fail
  assertion_2: pass|fail
  assertion_3: pass|fail
violations_found: <integer>
repair_applied: true|false  # with one-line description if true
gate_outcome: PASS | CONDITIONAL_PASS | BLOCKED | ESCALATED
next_skill: <skill filename or "human">
```

The agent must not proceed if `gate_outcome` is `BLOCKED` or `ESCALATED`.

## Related skills

- `../reviewers/data_mc_discrepancy_reviewer.md`
- `../reviewers/reproducibility_and_handoff_reviewer.md`
