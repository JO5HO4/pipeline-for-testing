# Selection and Partition Wrapper

Pattern: Tool Wrapper

Derived from:
- `SKILL_EVENT_IO_AND_COLUMNAR_MODEL`
- `SKILL_CATEGORY_CHANNEL_REGION_PARTITIONING`
- `SKILL_SELECTION_ENGINE_AND_REGIONS`

## When to use

Use this wrapper when the agent needs to materialize region partitions, process events into executable selections, or inspect per-sample region yields through repository code.

## Inputs

- normalized summary
- sample registry
- region or partition configuration
- input data paths
- optional event cap

## Outputs

- partition specs under `outputs/partition/`
- per-sample selection or region artifacts
- region yield and overlap evidence consumed by downstream generators

## Preconditions

- object and region intent are defined in the summary or generator contract
- sample semantics are available

## Postconditions

- selection logic is executable rather than prose-only
- overlap evidence exists for reviewer checks

## Call procedure

1. Use `.rootenv/bin/python -m analysis.selections.partitioning` to materialize category and region partitions.
2. Use `.rootenv/bin/python -m analysis.selections.engine` for per-sample selection and cut-flow execution.
3. Use `.rootenv/bin/python -m analysis.io.readers` only for focused event-ingestion inspection, not as a substitute for partition or selection evidence.

## Failure modes

- partition identifiers not aligned with the normalized summary
- SR and CR overlap unresolved
- selection expressions not executable

## Verification expectations

- partition and selection artifacts exist
- overlap checks are explicit
- downstream cut-flow and template generators consume the same region definitions

## Verification Gate

### ASSERTIONS

1. The wrapper outputs exist before handoff: `partition specs under outputs/partition/`, `per-sample selection or region artifacts`, and the `region yield and overlap evidence` consumed downstream.
2. The partition and selection artifacts use executable region logic that stays aligned with the normalized summary rather than drifting into prose-only semantics.
3. The overlap evidence is explicit, and the downstream cut-flow and template generators are pointed at the same region definitions rather than a silently different partition set.

### REPAIR

- Soft failure: rerun `selection_and_partition_wrapper.md` to regenerate the missing partition, selection, or overlap outputs and rerun this gate.
- Hard failure: return to Stage 3 of `hep_analysis_meta_pipeline.md`; if region logic remains non-executable or overlap cannot be resolved, route through `event_model_and_partition_generator.md` or `analysis_summary_reviewer.md`, and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: selection_and_partition_wrapper
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

- `../generators/event_model_and_partition_generator.md`
- `../generators/selection_and_yield_generator.md`
- `../reviewers/analysis_summary_reviewer.md`
