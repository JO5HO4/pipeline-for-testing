# Summary Loader Wrapper

Pattern: Tool Wrapper

Derived from:
- `SKILL_READ_SUMMARY_AND_VALIDATE`
- `SKILL_JSON_SPEC_DRIVEN_EXECUTION`

## When to use

Use this wrapper when the agent needs a normalized analysis summary, schema validation, inventory counts, or overlap-policy outputs derived from the repository summary loader.

## Inputs

- analysis summary JSON path
- output directory

## Outputs

- `outputs/summary.normalized.json`
- `outputs/validation/inventory.json`
- `outputs/validation/diagnostics.json`
- `outputs/validation/overlap_policy.json`

## Preconditions

- the summary file exists
- preflight has not already blocked execution

## Postconditions

- the repository summary loader is the only source of normalized summary structure used downstream
- any normalization or schema error is surfaced instead of repaired silently

## Call procedure

1. Run `.rootenv/bin/python -m analysis.config.load_summary --summary <summary> --out <outputs/summary.normalized.json>` when a direct normalized summary artifact is needed.
2. Use `analysis.cli bootstrap` when the surrounding bootstrap outputs are also needed.
3. Hand the produced artifacts to the summary reviewer before downstream generation begins.

## Failure modes

- invalid enums or missing required keys
- unresolved region, fit, or signature references
- missing or contradictory overlap policy

## Verification expectations

- the normalized summary exists
- diagnostics are empty or explicitly blocking
- reviewer findings cite the normalized summary rather than the raw narrative prompt

## Verification Gate

### ASSERTIONS

1. The wrapper outputs exist before handoff: `outputs/summary.normalized.json`, `outputs/validation/inventory.json`, `outputs/validation/diagnostics.json`, and `outputs/validation/overlap_policy.json`.
2. The `outputs/validation/diagnostics.json` artifact is either empty of blocking issues or explicitly records blocking issues; normalization and schema errors are surfaced rather than repaired silently.
3. Downstream stages are using `outputs/summary.normalized.json` as the authoritative summary structure instead of falling back to raw narrative text or an unnormalized summary file.

### REPAIR

- Soft failure: rerun `summary_loader_wrapper.md` or `analysis_spec_generator.md` to regenerate the normalized summary and validation artifacts and rerun this gate.
- Hard failure: return to Stage 3 of `spec_to_runtime_pipeline.md`; if the summary cannot be normalized without inventing missing physics fields, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: summary_loader_wrapper
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

- `../reviewers/analysis_summary_reviewer.md`
- `../generators/analysis_spec_generator.md`
- `../pipelines/spec_to_runtime_pipeline.md`
