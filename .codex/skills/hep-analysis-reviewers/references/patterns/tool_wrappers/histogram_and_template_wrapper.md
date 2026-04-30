# Histogram and Template Wrapper

Pattern: Tool Wrapper

Derived from:
- `SKILL_HISTOGRAMMING_AND_TEMPLATES`
- `SKILL_FREEZE_ANALYSIS_HISTOGRAM_PRODUCTS`

## When to use

Use this wrapper when the agent needs repository code to build histograms, create fit templates, or reuse cached histogram products.

## Inputs

- processed samples or selection outputs
- runtime defaults and observable definitions
- histogram output path
- optional cache or freeze settings

## Outputs

- histogram products under `outputs/hists/`
- cache artifacts under `outputs/cache/`
- freeze or manifest metadata when histogram products are intentionally reused

## Preconditions

- nominal sample selection is reviewable
- selections and observables are fixed for the current stage

## Postconditions

- histogram artifacts preserve statistical bookkeeping and provenance
- template reuse is explicit rather than implicit

## Call procedure

1. Use `.rootenv/bin/python -m analysis.hists.histmaker` for direct histogram production where a focused stage run is enough.
2. Use `analysis.pipeline.run_all_stages` or `.rootenv/bin/python -m analysis.cli run` when histogram production must stay aligned with the integrated pipeline outputs.
3. Record whether cache reuse or frozen products were used before statistical stages begin.

## Failure modes

- mismatched binning across compared templates
- missing provenance for reused histogram products
- histogram products not aligned with the reviewed nominal sample set

## Verification expectations

- template manifests exist
- statistical bookkeeping such as weighted yields or `sumw2` is preserved
- smoothing and effective-luminosity reviewers receive the same template set that the fits will consume

## Verification Gate

### ASSERTIONS

1. The wrapper outputs exist before handoff: `histogram products under outputs/hists/`, `cache artifacts under outputs/cache/` when reuse is requested, and `freeze or manifest metadata` when histogram products are intentionally reused.
2. The produced template manifest explicitly records whether histograms were built fresh, loaded from cache, or frozen, and the statistical bookkeeping such as weighted yields or `sumw2` is preserved.
3. The wrapper output remains aligned with the reviewed nominal sample set and does not silently introduce smoothing or a different template set than the one statistical reviewers will inspect.

### REPAIR

- Soft failure: rerun `histogram_and_template_wrapper.md` to regenerate the missing histogram products, cache metadata, or manifest and rerun this gate.
- Hard failure: return to Stage 6 of `hep_analysis_meta_pipeline.md`; if the template set no longer matches the reviewed nominal samples, roll back through `histogram_and_template_generator.md` or `sample_semantics_generator.md`, and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: histogram_and_template_wrapper
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

- `../generators/histogram_and_template_generator.md`
- `../reviewers/statistical_readiness_reviewer.md`
- `../shared/plotting_invariants.md`
