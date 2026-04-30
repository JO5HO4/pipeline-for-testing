# Background and Signal Model Generator

Pattern: Generator

Derived from:
- `SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS`
- `SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION`
- `SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION`

## Purpose

Create the strategy and model artifacts that define how backgrounds are constrained, how blinding is applied, and how signal and background parameterizations are chosen for the HEP fit workflow.

## When to use

- reviewed templates and sample semantics exist
- the analysis needs CR and SR transfer intent, blinding outputs, or signal and background PDF choices
- a fit or report stage needs explicit model provenance

## Required inputs

- template artifacts
- sample contracts, sample semantics, and nominal mapping
- data-driven template contracts when used
- fit-region definitions
- blinding and fit-policy decision record

## Outputs

- background modeling strategy
- CR and SR constraint map
- background input-role summary
- blinding summary
- signal PDF artifact
- background scan and chosen model artifacts
- spurious-signal artifact

## Generation steps

1. Use `sample_strategy_inversion.md` to resolve process roles and constraint intent.
2. Use `blinding_and_fit_policy_inversion.md` to resolve allowed data visibility and fit semantics.
3. For each background input, declare whether it is MC-driven, data-driven, or hybrid and record its normalization mode.
4. Build explicit background modeling and control-to-signal mappings.
5. Generate or record the signal parameterization, background scan, chosen model, and spurious-signal evidence.
6. Emit provenance for nominal template choice, sideband normalization, smoothing context, template-source role, and blinding behavior.

## Output contract

- every constrained background has an explicit CR to SR map
- blinding behavior is recorded as an artifact, not implied
- nominal background template choice and sideband normalization are explicit for H to gammagamma
- every background PDF or template declares its source class and normalization mode

## Constraints

- no silent merge of low-statistics auxiliary backgrounds into the central nominal template
- no implicit promotion of a data-driven template into the observed-data side of the likelihood
- no silent exposure of observed data in a blinded window
- no data-driven template without a reviewed template contract
- if model choice remains ambiguous, block and escalate through the inversion or reviewer path

## Verification Gate

### ASSERTIONS

1. The `background modeling strategy`, `CR and SR constraint map`, `background input-role summary`, `blinding summary`, `signal PDF artifact`, `background scan and chosen model artifacts`, and `spurious-signal artifact` all exist before the modeling stage hands off.
2. Every background input named in the `background modeling strategy` declares whether it is `MC-driven`, `data-driven`, or `hybrid`, and it declares a normalization mode rather than leaving normalization implicit.
3. If the analysis is blinded, the `blinding summary` confirms that `120-130 GeV` is not exposed in blinded mode; if fit or significance products are prepared, the model artifacts record the full `105-160 GeV` fit range.
4. If an H to gammagamma background template is central, the `background input-role summary` names an explicit nominal diphoton sample, and any data-driven input listed there points to a reviewed `data-driven template contract` rather than silently reusing observed data.

### REPAIR

- Soft failure: rerun `background_and_signal_model_generator.md` after refreshing the missing model artifact, `blinding summary`, or source-class declaration, then rerun this gate.
- Hard failure: return to Stage 6 of `hep_analysis_meta_pipeline.md`, routing through `data_driven_template_generator.md`, `sample_strategy_inversion.md`, or `blinding_and_fit_policy_inversion.md` as needed; escalate to `statistical_readiness_reviewer.md` or a human if the nominal model choice remains ambiguous.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: background_and_signal_model_generator
assertions_checked:
  - assertion_1
  - assertion_2
  - assertion_3
  - assertion_4
assertion_results:
  assertion_1: pass|fail
  assertion_2: pass|fail
  assertion_3: pass|fail
  assertion_4: pass|fail
violations_found: <integer>
repair_applied: true|false  # with one-line description if true
gate_outcome: PASS | CONDITIONAL_PASS | BLOCKED | ESCALATED
next_skill: <skill filename or "human">
```

The agent must not proceed if `gate_outcome` is `BLOCKED` or `ESCALATED`.

## Related skills

- `../inversions/sample_strategy_inversion.md`
- `../inversions/blinding_and_fit_policy_inversion.md`
- `data_driven_template_generator.md`
- `../reviewers/likelihood_sample_role_reviewer.md`
- `../reviewers/statistical_readiness_reviewer.md`
- `../reviewers/blinding_and_visualization_reviewer.md`
