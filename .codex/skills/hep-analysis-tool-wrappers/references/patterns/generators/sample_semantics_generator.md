# Sample Semantics Generator

Pattern: Generator

Derived from:
- `SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION`
- `SKILL_MC_NORMALIZATION_METADATA_STACKING`

## Purpose

Generate the reviewed sample registry, machine-readable likelihood sample contracts, normalization records, and nominal-versus-alternative mapping needed for central yields, templates, and fits.

## When to use

- normalized summary is ready
- sample inventory or metadata changed
- a reviewer blocked central results because the sample semantics are ambiguous

## Required inputs

- normalized summary
- input sample inventory
- metadata CSV artifact or equivalent metadata source; in this vendored pack the file is `../metadata.csv`, while some legacy repo layouts used `skills/metadata.csv`
- luminosity policy
- signal-signature and likelihood-intake decision record
- sample-strategy decision record
- likelihood sample contract schema

## Outputs

- sample registry
- likelihood sample contract set
- MC sample selection or nominal mapping record
- normalization table
- sample classification and process-role metadata
- relevance and exclusion log
- metadata resolution log

## Generation steps

1. Build the registry keyed by stable sample identifiers.
2. Match metadata rows and compute normalization factors with explicit unit handling.
3. Instantiate one contract record per central or reviewer-visible sample using the likelihood-sample schema.
4. Separate data, signal, irreducible background, reducible background, and negligible semantics.
5. Mark one nominal sample set per central process and record alternatives, validation-only samples, or discarded candidates separately.
6. Emit provenance linking the summary, intake decision, strategy decision, metadata source, and selected luminosity.

## Output contract

- central outputs never double count nominal and alternative samples
- each contract declares provenance, likelihood role, physics role, nominality, normalization mode, and event-overlap policy
- observed data and template-source data never share the same contract record
- default central luminosity is `36.1 fb^-1` unless an approved override is recorded
- signed generator-weight sums remain intact

## Constraints

- intake ambiguity routes to `../inversions/signal_signature_and_likelihood_intake_inversion.md`
- relevance or nominality ambiguity routes to `../inversions/sample_strategy_inversion.md`
- the generator never invents missing cross section or sum-of-weights values
- the generator never invents fake-rate arguments, closure evidence, or decorrelation claims
- sample names alone are insufficient when stable identifiers are available

## Verification Gate

### ASSERTIONS

1. The `sample registry`, `likelihood sample contract set`, `MC sample selection or nominal mapping record`, `normalization table`, `sample classification and process-role metadata`, `relevance and exclusion log`, and `metadata resolution log` all exist before yields, templates, or fits treat the sample configuration as central.
2. Every record in the `likelihood sample contract set` declares `provenance`, `likelihood role`, `physics role`, `nominality`, `normalization mode`, and `event-overlap policy`, and no record silently mixes observed data with template-source data.
3. The `normalization table` and contract set use `36.1 fb^-1` as the central luminosity unless an approved override is recorded, and `36.0 fb^-1` does not appear as the central luminosity.
4. Central normalization is traceable to `cross section x k-factor x filter efficiency x signed generator-weight sum`, and raw event counts are not used as the central normalization basis.

### REPAIR

- Soft failure: rerun `sample_semantics_generator.md` to regenerate the missing registry, contract, nominal mapping, or normalization artifacts and rerun the gate.
- Hard failure: return to Stage 4 of `sample_and_template_semantics_pipeline.md`; if metadata cannot establish a unique nominal path or the normalization inputs remain incomplete, route through `signal_signature_and_likelihood_intake_inversion.md`, `sample_strategy_inversion.md`, or escalate to a human, and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: sample_semantics_generator
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

- `../tool_wrappers/sample_registry_and_metadata_wrapper.md`
- `data_driven_template_generator.md`
- `../reviewers/nominal_sample_and_normalization_reviewer.md`
- `../reviewers/likelihood_sample_role_reviewer.md`
- `../shared/likelihood_sample_contract_schema.md`
- `../inversions/sample_strategy_inversion.md`
