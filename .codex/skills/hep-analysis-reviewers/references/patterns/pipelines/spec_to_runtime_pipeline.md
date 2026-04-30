# Spec-to-Runtime Pipeline

Pattern: Pipeline

Derived from:
- `SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR`
- `SKILL_JSON_SPEC_DRIVEN_EXECUTION`
- `SKILL_READ_SUMMARY_AND_VALIDATE`

## Stage ordering

| Stage | Inputs | Producing skills | Gate | Exit criteria |
|---|---|---|---|---|
| Preflight intent check | user request, repo paths | `runtime_and_preflight_wrapper.md` | `preflight_fact_check_reviewer.md` | run objective and paths are explicit |
| Spec generation or refinement | narrative or JSON | `analysis_spec_generator.md` | `preflight_fact_check_reviewer.md` | draft summary and gap report exist |
| Summary normalization | summary path | `summary_loader_wrapper.md` | `analysis_summary_reviewer.md` | normalized summary and diagnostics exist |
| Runtime contract finalization | normalized summary, overrides | `analysis_spec_generator.md` | `analysis_summary_reviewer.md` | execution contract and deviations log are reviewer-approved |

## Gates

- no downstream stage may start without a reviewed normalized summary
- all runtime overrides must be logged before sample processing

## Dependencies

- `../shared/hep_domain_guardrails.md`
- `../shared/pipeline_logging_contract.md`

## Escalation paths

- escalate when the summary cannot be made valid without inventing physics content
- escalate when unblinding or luminosity scope is requested but not approved explicitly

## Logging requirements

- record every assumption, override, and unresolved field
- record which summary path became the authoritative run input

## Verification Gate

### ASSERTIONS

1. The pipeline produced the `Preflight intent check` artifacts, the draft summary and `gap report`, the normalized summary with diagnostics, and the final `execution contract` with `deviations log` before it advanced past Stage 4.
2. The pipeline did not advance downstream before `analysis_summary_reviewer.md` returned `pass` or `conditional_pass` on the normalized summary and runtime contract artifacts.
3. The final `execution contract` explicitly records summary path, inputs path, outputs path, blinding mode, and luminosity scope, and no stale `36.0 fb^-1` value silently replaced the central luminosity when `36.1 fb^-1` is intended.

### REPAIR

- Soft failure: rerun the blocked stage in this pipeline to regenerate the missing preflight, summary, diagnostics, execution-contract, or deviations artifact, then rerun this gate.
- Hard failure: return to the earliest blocked stage in the `## Stage ordering` table of `spec_to_runtime_pipeline.md`; if the summary cannot be made valid without inventing physics content or if unblinding or luminosity scope is still unapproved, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: spec_to_runtime_pipeline
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

- `hep_analysis_meta_pipeline.md`
- `../inversions/analysis_router_inversion.md`
