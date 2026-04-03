# Selection and Yield Generator

Pattern: Generator

Derived from:
- `SKILL_SELECTION_ENGINE_AND_REGIONS`
- `SKILL_CUT_FLOW_AND_YIELDS`

## Purpose

Produce the cut-flow, region-yield, and provenance artifacts that connect executable selections to the event counts and weighted yields used later in histogramming and reporting.

## When to use

- reviewed partition and region contracts exist
- nominal sample semantics are available
- a downstream stage needs cut-flow evidence or central yields

## Required inputs

- region definitions
- sample registry
- nominal sample mapping
- event model or processed sample access

## Outputs

- cut-flow tables
- region-yield tables
- process-aggregated views
- sample-resolved views
- cut-flow provenance

## Generation steps

1. Run the executable region logic over the nominal sample set.
2. Record both unweighted counts and weighted yields.
3. Compute process-level and combined totals without hiding sample-level detail by default.
4. Record uncertainty proxies from event weights.
5. Link final selected yields to the same region semantics that downstream histogramming will use.

## Output contract

- cut-flow steps are ordered
- unweighted counts do not increase across stricter sequential cuts
- MC uncertainties come from weighted bookkeeping
- H to gammagamma cut-flow views separate signal production modes, prompt diphoton background, and data

## Constraints

- merged process rows require an explicit merge map
- alternative samples do not enter central totals unless the decision record says so

## Verification Gate

### ASSERTIONS

1. The `cut-flow tables`, `region-yield tables`, `process-aggregated views`, `sample-resolved views`, and `cut-flow provenance` all exist before histogramming or reporting consumes the yields.
2. The `cut-flow tables` preserve step ordering and show that unweighted event counts do not increase across stricter sequential cuts unless an explicit branch reset is documented in the provenance.
3. The `process-aggregated views` can be traced back to the `sample-resolved views`, and alternative samples are excluded from central totals unless the decision record explicitly promotes them.

### REPAIR

- Soft failure: rerun `selection_and_yield_generator.md` to regenerate the missing cut-flow, yield, or provenance artifacts and rerun the gate.
- Hard failure: return to Stage 4 of `hep_analysis_meta_pipeline.md`; if central totals depend on unresolved nominal-sample ambiguity or non-executable region logic, roll back through `selection_and_partition_wrapper.md` or `sample_semantics_generator.md` and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: selection_and_yield_generator
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
- `../reviewers/nominal_sample_and_normalization_reviewer.md`
- `histogram_and_template_generator.md`
