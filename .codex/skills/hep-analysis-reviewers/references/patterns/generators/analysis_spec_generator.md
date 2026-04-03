# Analysis Spec Generator

Pattern: Generator

Derived from:
- `SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR`
- `SKILL_JSON_SPEC_DRIVEN_EXECUTION`

## Purpose

Create or refine the analysis specification so the validated summary, execution contract, and deviation log become the only authoritative inputs to the runtime pipeline.

## When to use

- a user provided narrative instructions rather than a ready analysis JSON
- the runtime pipeline needs an explicit `spec_to_runtime` contract
- summary validation found missing but representable fields

## Required inputs

- narrative description or analysis JSON
- repository schema expectations
- approved runtime constraints

## Outputs

- analysis JSON draft or revised JSON
- gap report
- source trace map
- execution contract
- deviations-from-spec log

## Generation steps

1. Extract objective, target process, observables, regions, fit scope, and result types.
2. Mark unknown values explicitly instead of guessing.
3. Normalize naming so the summary loader can validate it.
4. Record every assumption and every user override.
5. Produce an execution contract that names summary path, inputs path, outputs path, blinding mode, luminosity, and primary fit backend expectation.

## Output contract

- no field invented without being labeled as an assumption
- every unresolved item appears in the gap report
- every runtime override is listed with source and expected impact

## Constraints

- never fabricate physics numbers
- preserve the distinction between user-provided facts and agent assumptions
- do not bypass the summary reviewer

## Verification Gate

### ASSERTIONS

1. The `analysis JSON draft or revised JSON`, `gap report`, `source trace map`, `execution contract`, and `deviations-from-spec log` all exist before this generator hands off.
2. The `execution contract` explicitly names summary path, inputs path, outputs path, blinding mode, luminosity, and primary fit backend expectation, and every runtime override appears in the `deviations-from-spec log`.
3. Every unresolved item appears in the `gap report`, and no field in the `analysis JSON draft or revised JSON` is introduced without being labeled as an assumption or traced in the `source trace map`.

### REPAIR

- Soft failure: rerun `analysis_spec_generator.md` to regenerate the missing `gap report`, `source trace map`, `execution contract`, or `deviations-from-spec log`, then rerun this gate.
- Hard failure: return to Stage 2 of `spec_to_runtime_pipeline.md` for narrative/spec repair, or return to Stage 4 of `spec_to_runtime_pipeline.md` when only the execution contract or deviations log is incomplete; escalate to `analysis_summary_reviewer.md` or a human if physics content would need to be guessed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: analysis_spec_generator
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

- `../tool_wrappers/summary_loader_wrapper.md`
- `../reviewers/preflight_fact_check_reviewer.md`
- `../reviewers/analysis_summary_reviewer.md`
- `../pipelines/spec_to_runtime_pipeline.md`
