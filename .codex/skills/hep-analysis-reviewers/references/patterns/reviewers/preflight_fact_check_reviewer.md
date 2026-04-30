# Preflight Fact Check Reviewer

Pattern: Reviewer

Derived from:
- `SKILL_AGENT_PRE_FLIGHT_FACT_CHECK`

## Review scope

Verify that the analysis objective, inputs, runtime scope, and repository readiness are unambiguous enough to start execution without inventing missing physics content.

## Required evidence

- user task or approved execution contract
- summary path or narrative source
- preflight outputs
- runtime and inputs path confirmation

## Criteria

- `pass`: objective, summary, inputs, and run scope are explicit
- `conditional_pass`: small non-physics ambiguities remain but are logged and non-blocking
- `block`: a missing fact would force the agent to guess analysis intent, luminosity, blinding scope, or central-result method
- `fail`: the repository or requested paths are not runnable for the requested task

## Common failure modes

- no validated summary or no approved narrative-to-summary translation
- missing explicit unblinding instruction when observed significance is requested
- unclear input data location or output location
- runtime environment missing required capabilities for the requested central claim

## Required remediation guidance

- route narrative ambiguity to `../generators/analysis_spec_generator.md`
- route runtime issues to `../tool_wrappers/runtime_and_preflight_wrapper.md`
- escalate to a human when the missing fact cannot be reconstructed from repository artifacts

## Verification Gate

### ASSERTIONS

1. A reviewer verdict artifact or conversation note for `Preflight Fact Check Reviewer` exists and records exactly one verdict from `pass`, `conditional_pass`, `block`, or `fail`.
2. The required evidence is present on disk or in the conversation: the user task or approved execution contract, the summary path or narrative source, the preflight outputs, and the runtime and inputs path confirmation.
3. The evidence explicitly confirms that the run objective, luminosity scope, blinding scope, and central-result method are explicit rather than inferred; if observed significance or unblinding is requested, the approval is recorded rather than assumed.

### REPAIR

- Soft failure: rerun `runtime_and_preflight_wrapper.md` or `analysis_spec_generator.md` to repair the missing preflight evidence or execution contract, then rerun this reviewer gate.
- Hard failure: return to Stage 1 of `spec_to_runtime_pipeline.md`; if the missing fact cannot be reconstructed from repository artifacts without guessing physics content, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: preflight_fact_check_reviewer
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

- `../pipelines/spec_to_runtime_pipeline.md`
- `../shared/review_rubric.md`
