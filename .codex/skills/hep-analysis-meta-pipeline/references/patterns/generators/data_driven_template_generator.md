# Data-Driven Template Generator

Pattern: Generator

Derived from:
- `SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION`
- `SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS`
- `SKILL_PLOTTING_AND_REPORT`

## Purpose

Generate the explicit contract for any template, transfer factor, or auxiliary PDF that is derived from data rather than taken directly from the observed-data term of the final likelihood.

## When to use

- the analysis uses NT-like, sideband, inverted-ID, inverted-isolation, or otherwise data-derived background templates
- a transfer factor or control-to-signal relation is built from data
- the background model needs an explicit contract for how data enter the PDF side of the likelihood

## Required inputs

- signal-signature and likelihood-intake decision record
- sample contract set
- region definitions and source event selection
- observable or relation definition for the template product
- blinding policy and allowed data visibility
- closure, decorrelation, or weak-correlation rationale

## Outputs

- data-driven template contract
- source event definition
- target use declaration
- normalization or relation mode
- event-overlap policy
- closure or validation plan

## Generation steps

1. Confirm from the intake decision that the proposed data source is allowed to act as a template or transfer-factor source.
2. Identify the source events, the target region or category, and the downstream use of the template product.
3. Declare whether the product is a shape-only template, analytic-PDF test sample, sideband-normalized template, transfer factor, or auxiliary-constraint input.
4. Record the observable or relation being modeled and any correlation assumption that makes the transfer scientifically plausible.
5. Declare the event-overlap policy between the template source and the observed-data terms of the likelihood.
6. Emit the closure or validation plan and the provenance needed for reviewer inspection.

## Output contract

- data used to build the template are never treated as the same likelihood term as observed data
- the template source, target use, and observable are explicit
- normalization mode is explicit, such as shape-only, sideband-normalized, CR-constrained, or auxiliary-only
- event overlap is either forbidden or proven disjoint
- closure or decorrelation assumptions are stated in reviewer-visible form

## Constraints

- no implicit reuse of observed signal-region data in blinded mode
- no template contract without an explicit source event definition
- no hidden assumption that a classifier shape or transfer factor is uncorrelated with the inverted object selection

## Verification Gate

### ASSERTIONS

1. The `data-driven template contract`, `source event definition`, `target use declaration`, `normalization or relation mode`, `event-overlap policy`, and `closure or validation plan` all exist before any downstream modeling step reads the template.
2. The `data-driven template contract` explicitly names the source region, target use, modeled observable or relation, and the normalization mode as `shape-only`, `sideband-normalized`, `CR-constrained`, or `auxiliary-only` rather than leaving those choices implicit.
3. The `event-overlap policy` proves the source events are disjoint from observed-data likelihood terms or explicitly blocks the template, and the `closure or validation plan` states the weak-correlation or decorrelation rationale in reviewer-visible form.
4. If blinded mode is active, the generated template inputs do not reuse observed signal-region data from the `120-130 GeV` window as if they were ordinary template source events.

### REPAIR

- Soft failure: rerun `data_driven_template_generator.md` to regenerate the missing contract, overlap policy, or closure plan and rerun the gate.
- Hard failure: return to Stage 5 of `sample_and_template_semantics_pipeline.md`; if the source region, overlap policy, or decorrelation rationale cannot be defended, escalate through `likelihood_sample_role_reviewer.md` or to a human, and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: data_driven_template_generator
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

- `../inversions/signal_signature_and_likelihood_intake_inversion.md`
- `../inversions/sample_strategy_inversion.md`
- `../reviewers/likelihood_sample_role_reviewer.md`
- `background_and_signal_model_generator.md`
- `../shared/likelihood_sample_contract_schema.md`
- `../shared/hep_domain_guardrails.md`
