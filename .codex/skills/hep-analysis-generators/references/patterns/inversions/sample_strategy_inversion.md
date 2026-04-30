# Sample Strategy Inversion

Pattern: Inversion

Derived from:
- `SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION`
- `SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS`
- `SKILL_13TEV25_DETAILS`

## Trigger condition

Use this inversion when the workflow must work backward from the recorded signal signature and sample inventory to determine background relevance, nominal sample choice, alternative-sample status, or the normalization mode for each process.

## Decision structure

1. Read the signal-signature and likelihood-intake decision record.
2. Determine which candidate processes directly produce the signal signature, mimic it through misidentification or misreconstruction, or are negligible for the current analysis.
3. For each relevant process, decide whether there is exactly one nominal sample set and which remaining samples are alternatives or validation-only.
4. Decide whether each relevant background is theory-constrained, control-region-constrained, jointly constrained across SR and CR, floating, or shape-only.
5. Decide whether any data sample is allowed to act as a template or transfer-factor source rather than as observed data.

## Branch criteria

- If DSIDs and metadata establish a unique nominal sample set, accept it and record the evidence.
- If only filenames are available, treat the choice as provisional and block central claims until the reviewer accepts it.
- If a process directly reproduces the reconstructed signature, treat it as signal or irreducible background unless the summary says otherwise.
- If a process reaches the signature only through fake, nonprompt, or misreconstructed objects, treat it as reducible background only when the analysis has a plausible mechanism and supporting rate argument.
- If the process is only technically capable of producing the signature through a vanishingly small higher-order or fake path, classify it as `negligible` and log the reason rather than promoting it.
- If the H to gammagamma background template is under discussion, require an explicit nominal diphoton sample choice and reject silent merges of low-statistics auxiliary samples.
- If multiple plausible nominal MC samples remain after metadata resolution, stop and require approved analysis input or human triage.
- If a data-driven template is proposed, require an explicit source region, observable, overlap policy, and closure expectation.

## Required evidence per branch

- signal-signature and likelihood-intake decision record
- sample registry draft
- metadata resolution output
- open-data dataset facts
- reviewed summary and partition artifacts

## Output decision record

Record:

- analysis target and reconstructed signal signature
- relevant processes by class
- selected nominal samples by process
- alternative samples by process
- normalization mode and constraint intent for each background
- data-template sources and blocked template uses
- blocking ambiguities

## Verification Gate

### ASSERTIONS

1. A decision record exists before the inversion hands off, and it records the analysis target, reconstructed signal signature, relevant processes by class, selected nominal samples by process, alternative samples by process, normalization modes, data-template sources, and blocking ambiguities.
2. The evidence supporting process relevance includes the signal-signature and likelihood-intake decision record, the sample registry draft, metadata resolution output, open-data dataset facts, and the reviewed summary or partition artifacts.
3. If an H to gammagamma background template is central, the decision record names an explicit nominal diphoton sample, and if multiple plausible nominal MC samples remain, the record marks the branch as blocked pending approved analysis input or human triage.

### REPAIR

- Soft failure: rerun `sample_strategy_inversion.md` after collecting the missing registry, metadata, or signature evidence and rewrite the decision record before rerunning this gate.
- Hard failure: return to Stage 3 of `sample_and_template_semantics_pipeline.md`; if relevance, nominality, or normalization intent cannot be supported from repository evidence, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: sample_strategy_inversion
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

- `signal_signature_and_likelihood_intake_inversion.md`
- `../generators/sample_semantics_generator.md`
- `../generators/data_driven_template_generator.md`
- `../reviewers/nominal_sample_and_normalization_reviewer.md`
- `../reviewers/likelihood_sample_role_reviewer.md`
- `../shared/likelihood_sample_contract_schema.md`
- `../shared/open_data_dataset_facts.md`
