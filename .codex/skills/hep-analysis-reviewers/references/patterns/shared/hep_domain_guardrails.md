# HEP Domain Guardrails

These rules are binding across the new skill system.

## Source of truth and overrides

- The normalized analysis summary and approved execution contract define the run scope.
- Narrative text may clarify intent but cannot silently override the validated summary.
- Any override to luminosity, blinding, backend, category scope, or fit range must be explicit and logged.

## Blinding and significance

- Blinding is the default.
- Observed signal-region data must remain hidden until explicit unblinding instruction is recorded.
- For the H to gammagamma workflow, expected discovery significance uses signal-plus-background Asimov pseudo-data over `105-160 GeV`.
- Observed significance is allowed only after explicit unblinding and must use observed data over the full `105-160 GeV` range.
- Signal-region data in `120-130 GeV` must not be inspected in blinded mode.

## Fit backend policy

- Central H to gammagamma fit and significance claims require `pyroot_roofit`.
- Optional `pyhf` or other non-ROOT results are cross-checks only and must never be promoted to primary claims.
- If RooFit is unavailable, the central claim is blocked rather than substituted.

## Sample and normalization policy

- Default central luminosity for the current analysis project is `36.1 fb^-1` unless an explicit approved override is recorded.
- Legacy references to `36.0 fb^-1` in the source pack are treated as stale defaults and must not override the repository central-result policy.
- Use DSID or another stable sample identifier whenever possible.
- Normalization must use cross section, k-factor, filter efficiency, and signed generator-weight sum.
- Do not replace signed generator-weight sums with raw event counts.
- Do not double count nominal and alternative samples for the same process in central yields.

## Observed-data and template policy

- Data that enter the likelihood as observed distributions are distinct from data used to build templates, transfer factors, or auxiliary PDFs.
- If the same underlying dataset contributes in both ways, the event selections must be explicitly disjoint and the overlap policy must be reviewer-visible.
- Data-driven templates must declare their source region, target use, observable or relation, and closure or decorrelation rationale.
- In blinded mode, observed data from the blinded signal-region window must not be repurposed into template construction without explicit approval.

## Background-model and smoothing policy

- For the default H to gammagamma workflow, the nominal background template must be an explicit diphoton sample choice, not a silent merge of low-statistics auxiliary backgrounds.
- Sideband normalization must be explicit when used and should document the `105-120 GeV` and `130-160 GeV` sidebands.
- No smoothing is implicit. If smoothing is required, it must be declared, justified, and logged with provenance.
- Effective luminosity and smoothing thresholds must be reviewer-visible and machine-auditable.

## Reporting and discrepancy policy

- Data and MC disagreement is a diagnostic signal, not a cosmetic problem to hide.
- The report must distinguish central results from cross-checks.
- Assumptions, deviations, and unresolved issues must be explicit.
- Missing reviewer evidence blocks handoff readiness.
