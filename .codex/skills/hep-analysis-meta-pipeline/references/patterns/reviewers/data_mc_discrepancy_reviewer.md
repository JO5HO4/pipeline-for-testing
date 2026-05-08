# Data-MC Discrepancy Reviewer

Pattern: Reviewer

Derived from:
- `SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK`

## Review scope

Check whether substantial disagreement between observed data and MC expectations has been investigated, classified, and reported honestly.

## Required evidence

- data-versus-MC plots and tables
- discrepancy audit
- discrepancy check log
- cut-flow and yield context
- normalization and sample-mapping artifacts
- prompt-MC versus reducible-MC-proxy yield split for same-sign, trilepton, fake-lepton, nonprompt-lepton, or charge-misID-sensitive channels
- reducible-background role audit listing raw `ttbar`, inclusive `W+jets`, inclusive `Z+jets`, multijet/photon, fake/nonprompt, and charge-misID proxy inputs with their central-expected eligibility
- data-driven fake/nonprompt and charge-misID availability artifact, including blocked inputs when calibrated methods are absent
- top per-sample MC contributors for any region or cut-flow step with material normalization disagreement
- central-only versus all-MC cross-check when alternative-sample double counting is plausible

## Criteria

- `pass`: the audit exists and all substantial discrepancies are either explained or openly unresolved
- `conditional_pass`: no substantial discrepancy is present and the explicit zero-issue path is documented
- `block`: discrepancy artifacts are missing or incomplete
- `fail`: the workflow hid or cosmetically suppressed a material discrepancy

## Same-sign and multilepton reducible-background hard gate

For same-sign dilepton, trilepton, fake/nonprompt-lepton, or charge-misID-sensitive regions:

- raw `ttbar`, inclusive `W+jets`, inclusive `Z+jets`, and multijet/photon MC may be shown only as `reducible_mc_proxy` unless a reviewed data-driven or hybrid fake/nonprompt or charge-misID method promotes the component to central expected background
- central expected background must be separated into `prompt_mc_background`, `data_driven_reducible_background`, and `reducible_mc_proxy_diagnostic` components, or must block the central expected-background claim
- a plot or table that includes raw reducible MC proxies must not be labeled simply `expected background`, `total background`, or `MC prediction`; it must say `diagnostic MC stack` or name the prompt/reducible split
- if raw reducible MC proxies make MC exceed data in a claim-visible region, the audit must classify the issue as a central-background-role violation unless a reviewed closure or data-driven estimate justifies the central use

## Common failure modes

- discrepancy artifacts missing on a supposedly clean run
- changes to binning, selection, or sample composition made only to improve visual agreement
- expected MC much larger than data because noncentral generator/shower/radiation alternatives were stacked with central samples
- expected MC much larger than data because raw reducible `ttbar` or jets MC was stacked as validated expected background in a same-sign or multilepton region
- report or plot labels hide that a stack is a diagnostic reducible-MC proxy rather than a validated expected background
- bug and modeling-mismatch cases not distinguished

## Required remediation guidance

- send implementation issues to `../inversions/failure_to_skill_inversion.md`
- rerun the affected generator or wrapper with the smallest possible write scope
- keep the discrepancy visible in the report even when unresolved

## Verification Gate

### ASSERTIONS

1. A reviewer verdict artifact or conversation note for `Data-MC Discrepancy Reviewer` exists and records exactly one verdict from `pass`, `conditional_pass`, `block`, or `fail`.
2. The required evidence is present on disk or in the conversation: data-versus-MC plots and tables, the discrepancy audit, the discrepancy check log, cut-flow and yield context, normalization and sample-mapping artifacts, and top-contributor diagnostics for material normalization disagreements.
3. The evidence explicitly confirms either that every substantial discrepancy was classified and reported honestly or that the explicit zero-issue path was documented; no discrepancy is treated as resolved solely by cosmetic changes.
4. If MC is materially above data, the evidence includes a central-only versus all-MC comparison or explains why alternative-sample double counting is impossible.
5. For same-sign, trilepton, fake/nonprompt-lepton, or charge-misID-sensitive regions, the evidence includes a prompt-MC versus reducible-MC-proxy split and a data-driven reducible-background availability artifact.
6. Raw reducible MC proxies are not used as central expected background unless a reviewed data-driven, hybrid, or closure-backed method explicitly promotes them; report-visible labels distinguish `prompt_mc_background` from `reducible_mc_proxy_diagnostic`.

### REPAIR

- Soft failure: rerun the smallest affected generator or wrapper to restore the missing discrepancy artifact or context, then rerun this reviewer gate.
- Hard failure: return to Stage 8 of `hep_analysis_meta_pipeline.md`; if a material discrepancy would need to be hidden to continue, route through `failure_to_skill_inversion.md` or escalate to a human, and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: data_mc_discrepancy_reviewer
assertions_checked:
  - assertion_1
  - assertion_2
  - assertion_3
  - assertion_4
  - assertion_5
  - assertion_6
assertion_results:
  assertion_1: pass|fail
  assertion_2: pass|fail
  assertion_3: pass|fail
  assertion_4: pass|fail
  assertion_5: pass|fail
  assertion_6: pass|fail
violations_found: <integer>
repair_applied: true|false  # with one-line description if true
gate_outcome: PASS | CONDITIONAL_PASS | BLOCKED | ESCALATED
next_skill: <skill filename or "human">
```

The agent must not proceed if `gate_outcome` is `BLOCKED` or `ESCALATED`.

## Related skills

- `../generators/report_package_generator.md`
- `reproducibility_and_handoff_reviewer.md`
