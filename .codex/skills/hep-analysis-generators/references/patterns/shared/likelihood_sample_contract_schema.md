# Likelihood Sample Contract Schema

Use this reference when a skill must describe how data or MC enter the analysis.

## Required axes

Every central or reviewer-visible sample contract should declare:

- `sample_key`: stable identifier for the contract record
- `provenance`: `data`, `mc`, or `hybrid`
- `likelihood_role`: `observed_data`, `template_source`, `transfer_factor_source`, `aux_constraint`, or `validation_only`
- `physics_role`: `signal`, `irreducible_background`, `reducible_background`, `negligible`, or `not_applicable`
- `nominality`: `nominal`, `alternative`, `template_only`, `observed_only`, or `unused_candidate`
- `normalization_mode`: `profiled_signal_strength`, `theory_constrained`, `cr_constrained`, `sr_cr_constrained`, `floating`, `shape_only`, or `not_applicable`
- `constraint_source`: free-form record of which region or prior constrains the normalization
- `systematic_use`: how an alternative sample is used, or `none`
- `template_observable`: the modeled observable or relation when the sample is a template source
- `event_overlap_policy`: how overlap with observed data is prevented, tested, or declared impossible

## Contract rules

- A single contract record must not be both `observed_data` and `template_source`.
- If the same underlying dataset contributes in two ways, create separate contract records with disjoint event definitions.
- `negligible` samples may be logged, but they do not become central without explicit approval.
- `alternative` MC samples do not become central predictions without explicit approval.
- Every data-driven template contract must carry reviewer-visible closure or decorrelation expectations.

## Normalization guidance

- Signal MC is often `profiled_signal_strength` rather than treated as a trusted fixed normalization.
- Background MC may be `theory_constrained`, `cr_constrained`, `sr_cr_constrained`, `floating`, or `shape_only` depending on the fit design.
- Data-driven templates still need an explicit normalization or relation mode, even when they are built from observed events.

## Minimal example

- prompt diphoton MC used as the central background template:
  - `provenance = mc`
  - `likelihood_role = template_source`
  - `physics_role = irreducible_background`
  - `nominality = nominal`
  - `normalization_mode = shape_only` or `cr_constrained`, depending on the fit design

- NT-like data used to build a classifier-shape template:
  - `provenance = data`
  - `likelihood_role = template_source`
  - `physics_role = reducible_background`
  - `nominality = template_only`
  - `event_overlap_policy = explicit disjoint source selection`
