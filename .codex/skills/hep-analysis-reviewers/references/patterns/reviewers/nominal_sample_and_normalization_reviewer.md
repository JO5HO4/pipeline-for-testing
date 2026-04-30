# Nominal Sample and Normalization Reviewer

Pattern: Reviewer

Derived from:
- `SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION`
- `SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION`
- `SKILL_MC_NORMALIZATION_METADATA_STACKING`
- `SKILL_13TEV25_DETAILS`

## Review scope

Verify that sample identity, nominal-versus-alternative status, and normalization are explicit enough for central yields, templates, and fits.

## Required evidence

- signal-signature and likelihood-intake decision record
- sample registry
- sample contract set
- nominal sample selection record
- normalization table
- metadata resolution log
- sample-strategy decision record when ambiguity existed

## Criteria

- `pass`: each relevant process has one central nominal path, one explicit normalization mode, and any alternatives are segregated from the central prediction
- `conditional_pass`: non-central samples or optional metadata gaps are logged without affecting central outputs
- `block`: the central nominal sample set is ambiguous or the normalization inputs are incomplete
- `fail`: central yields would double count processes or misuse metadata

## Common failure modes

- multiple candidate nominal samples for the same process
- raw event counts used instead of signed generator-weight sums
- central results using `36.0 fb^-1` because of stale policy text instead of the repository default `36.1 fb^-1`
- background normalization mode is missing for a process that is intended to be theory-constrained, CR-constrained, or floating
- background template choice is not traceable to an explicit nominal diphoton sample

## Required remediation guidance

- rerun `../inversions/signal_signature_and_likelihood_intake_inversion.md` when the authority for nominal choice is missing
- use `../inversions/sample_strategy_inversion.md` to pick the correct branch
- rerun `../generators/sample_semantics_generator.md` after the decision record is updated
- run `likelihood_sample_role_reviewer.md` when data, template, or validation roles remain mixed
- escalate if repository facts and metadata cannot establish a unique central sample set

## Verification Gate

### ASSERTIONS

1. A reviewer verdict artifact or conversation note for `Nominal Sample and Normalization Reviewer` exists and records exactly one verdict from `pass`, `conditional_pass`, `block`, or `fail`.
2. The required evidence is present on disk or in the conversation: the signal-signature and likelihood-intake decision record, the sample registry, the sample contract set, the nominal sample selection record, the normalization table, the metadata resolution log, and the sample-strategy decision record when ambiguity existed.
3. The evidence explicitly confirms that `36.1 fb^-1` is the central luminosity and that `36.0 fb^-1` does not appear as the central luminosity for the reviewed run.
4. The normalization evidence explicitly confirms `cross section x k-factor x filter efficiency x signed generator-weight sum`, and raw event counts are not treated as the central normalization basis.

### REPAIR

- Soft failure: rerun `sample_semantics_generator.md` or `sample_registry_and_metadata_wrapper.md` to repair the missing nominal mapping, normalization table, or metadata log, then rerun this reviewer gate.
- Hard failure: return to Stage 4 of `sample_and_template_semantics_pipeline.md`; if multiple nominal candidates remain or the normalization inputs are still incomplete, route through `sample_strategy_inversion.md` or escalate to a human, and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: nominal_sample_and_normalization_reviewer
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

- `likelihood_sample_role_reviewer.md`
- `../shared/open_data_dataset_facts.md`
- `../shared/hep_domain_guardrails.md`
