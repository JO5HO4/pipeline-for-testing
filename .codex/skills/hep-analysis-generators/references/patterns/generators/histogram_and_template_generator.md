# Histogram and Template Generator

Pattern: Generator

Derived from:
- `SKILL_HISTOGRAMMING_AND_TEMPLATES`
- `SKILL_FREEZE_ANALYSIS_HISTOGRAM_PRODUCTS`

## Purpose

Generate the histogram and template artifacts that statistical and reporting stages consume, while keeping cache reuse or frozen products explicit and auditable.

## When to use

- reviewed selections and observables exist
- downstream modeling needs a stable template set
- a rerun should reuse or freeze expensive histogram products

## Required inputs

- processed samples or selection outputs
- reviewed observables
- normalization and sample semantics
- cache or freeze policy

## Outputs

- histogram template manifest
- per-sample or per-process template artifacts
- cache or freeze provenance
- template-level statistical bookkeeping

## Generation steps

1. Build templates from the reviewed nominal sample set.
2. Keep observable definitions and binning stable within a comparison set.
3. Preserve weighted yields and statistical uncertainty bookkeeping.
4. If products are reused, emit a manifest that proves exactly which products were frozen or loaded from cache.

## Output contract

- fit-critical templates remain traceable to the nominal sample set
- cache reuse is explicit
- smoothing is not implied by template production

## Constraints

- the generator does not decide whether smoothing is allowed
- frozen templates must remain immutable for the remainder of the reviewed run

## Verification Gate

### ASSERTIONS

1. The `histogram template manifest`, `per-sample or per-process template artifacts`, `cache or freeze provenance`, and `template-level statistical bookkeeping` all exist before the templates are handed to modeling or plotting.
2. The `histogram template manifest` traces every fit-critical template back to the reviewed nominal sample set and records whether products were built fresh, loaded from cache, or frozen for reuse.
3. The `template-level statistical bookkeeping` preserves weighted yields and uncertainty bookkeeping, and the generated artifacts do not imply smoothing decisions that belong to later statistical review.

### REPAIR

- Soft failure: rerun `histogram_and_template_generator.md` or `histogram_and_template_wrapper.md` to regenerate the missing manifest, templates, or bookkeeping and rerun the gate.
- Hard failure: return to Stage 6 of `hep_analysis_meta_pipeline.md`; if the nominal template set is no longer traceable or frozen products were mutated, roll back to `selection_and_yield_generator.md` or `sample_semantics_generator.md` and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: histogram_and_template_generator
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

- `../tool_wrappers/histogram_and_template_wrapper.md`
- `../reviewers/statistical_readiness_reviewer.md`
- `../shared/plotting_invariants.md`
