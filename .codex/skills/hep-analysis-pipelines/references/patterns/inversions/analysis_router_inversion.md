# Analysis Router Inversion

Pattern: Inversion

Derived from:
- `SKILL.md` in the source pack
- `SKILL_SKILLS_PACK_INDEX`
- the legacy pack index
- the legacy routing guide

## Trigger condition

Use this inversion when the next action is unclear, when the workflow starts from a blocker or missing artifact instead of a clean stage boundary, or when multiple candidate skills look plausible.

## Decision structure

1. Identify the blocker in one sentence.
2. Classify the blocker as one of:
   - missing specification
   - missing runtime readiness
   - ambiguous sample semantics
   - missing region or selection artifacts
   - statistical gate failure
   - reporting or handoff failure
3. Choose the smallest skill set that can close that blocker.
4. Prefer the branch with the smallest write scope and the closest downstream handoff.

## Branch criteria

- Missing or ambiguous summary: route to `spec_to_runtime_pipeline.md`.
- Missing sample registry, normalization, or nominal mapping: route to `sample_semantics_generator.md` and its reviewer.
- Missing executable regions or yields: route to `event_model_and_partition_generator.md` or `selection_and_yield_generator.md`.
- Failed smoothing, effective-lumi, or backend gate: route to `blinding_and_fit_policy_inversion.md` and `statistical_readiness_reviewer.md`.
- Failed discrepancy or handoff gate: route to `reporting_and_handoff_pipeline.md` or `failure_to_skill_inversion.md`.

## Required evidence per branch

- normalized summary or explicit gap report
- current outputs inventory
- reviewer findings or blocking artifact
- prior decision records that constrain the next branch

## Output decision record

Write a decision record using `../shared/decision_record_template.md` that names:

- blocker
- chosen next skill or pipeline
- rejected alternatives
- required reviewer before advancement

## Verification Gate

### ASSERTIONS

1. A decision record exists using `../shared/decision_record_template.md` before the router hands off to the next skill.
2. The decision record names the blocker, the chosen next skill or pipeline, the rejected alternatives, and the required reviewer before advancement.
3. The evidence supporting the branch includes the normalized summary or explicit gap report, the current outputs inventory, reviewer findings or blocking artifact, and any prior decision record that constrains the branch.

### REPAIR

- Soft failure: rerun `analysis_router_inversion.md` with the missing blocker evidence and rewrite the decision record before rerunning this gate.
- Hard failure: return to the last completed stage in `hep_analysis_meta_pipeline.md` that produced the blocker; if the router would have to choose a branch without evidence or would skip a mandatory reviewer, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: analysis_router_inversion
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

- `../pipelines/hep_analysis_meta_pipeline.md`
- `../shared/artifact_matrix.md`
