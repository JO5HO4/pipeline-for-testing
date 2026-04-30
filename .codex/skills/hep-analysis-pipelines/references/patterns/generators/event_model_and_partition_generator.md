# Event Model and Partition Generator

Pattern: Generator

Derived from:
- `SKILL_EVENT_IO_AND_COLUMNAR_MODEL`
- `SKILL_OBJECT_DEFINITIONS`
- `SKILL_CATEGORY_CHANNEL_REGION_PARTITIONING`

## Purpose

Turn the reviewed analysis summary into executable object, category, channel, and region contracts that downstream selection stages can run without interpreting prose on the fly.

## When to use

- the summary reviewer has approved the overall schema
- category, object, or region logic changed
- downstream stages need a stable partition spec or object-definition record

## Required inputs

- normalized summary
- event column availability
- category and region intent
- sample semantics when category roles depend on process assignments

## Outputs

- object-definition record
- partition specification
- region definition contract
- overlap-policy manifest

## Generation steps

1. Resolve which observables and derived quantities are available from the event model.
2. Write object definitions before region logic.
3. Generate category and channel partitions with stable identifiers.
4. Encode SR, CR, SB, and VR roles explicitly.
5. Surface any ambiguity about overlap or region purpose before the selection engine runs.

## Output contract

- all identifiers are unique
- region logic is executable
- mutual exclusivity is the default for regions used together in a fit

## Constraints

- prose-only selections are not sufficient
- any overlap exception must be explicit and justified
- region definitions must stay aligned with the reviewed summary

## Verification Gate

### ASSERTIONS

1. The `object-definition record`, `partition specification`, `region definition contract`, and `overlap-policy manifest` all exist before selection or categorization proceeds.
2. Every identifier in the `partition specification` and `region definition contract` is unique and executable, and SR, CR, SB, and VR roles are explicit rather than inferred from prose.
3. The `overlap-policy manifest` records either the default mutual exclusivity for fit regions or every allowed overlap exception with its justification.

### REPAIR

- Soft failure: rerun `event_model_and_partition_generator.md` to rebuild the object, partition, or overlap artifacts and rerun the gate.
- Hard failure: return to Stage 3 of `hep_analysis_meta_pipeline.md` or Stage 5 of `hep_analysis_meta_pipeline.md` if category overlap remains unresolved; escalate to `analysis_summary_reviewer.md` or a human if executable region logic cannot be derived from the approved summary.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: event_model_and_partition_generator
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

- `../tool_wrappers/selection_and_partition_wrapper.md`
- `../reviewers/analysis_summary_reviewer.md`
- `../pipelines/hep_analysis_meta_pipeline.md`
