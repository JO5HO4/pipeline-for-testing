# Signal Signature and Likelihood Intake Inversion

Pattern: Inversion

Derived from:
- `SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR`
- `SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS`
- `SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION`

## Trigger condition

Use this inversion before sample or template selection when the analysis target, signal signature, region roles, or allowed data-driven template usage are incomplete.

## Missing information categories

- physics target or measured parameter
- reconstructed signal signature
- region map and which regions contribute observed data to the likelihood
- whether any data sample may be used as a template, transfer-factor source, or auxiliary constraint input
- authority for nominal-versus-alternative MC choices
- source of the candidate sample inventory

## Clarification order

1. Record the central physics target, such as signal strength, width, or cross section.
2. Record the reconstructed signature that defines relevance, such as diphoton, dilepton plus missing energy, or multijet plus photon.
3. Record the region map and which data distributions enter the final likelihood as observed data.
4. Record whether data-driven templates or transfer factors are allowed, and if so, from which regions and observables.
5. Record whether nominal versus alternative samples are already fixed by the summary or require human triage.
6. Record the minimum output artifacts required from sample handling, such as contracts, normalization tables, or template records.

## Stop conditions

- Do not start sample relevance classification until the physics target and reconstructed signal signature are explicit.
- Do not treat any data sample as a template or transfer-factor source unless that use is explicitly allowed.
- If multiple incompatible signal signatures remain plausible, stop and escalate instead of averaging or guessing.
- If the authority for nominal-versus-alternative MC choice is unclear, mark the branch as requiring human triage.

## Sufficient specification criteria

Proceed only when all of the following are explicit:

- analysis target
- reconstructed signal signature
- region list with observed-data roles
- allowed or disallowed data-template policy
- source of the candidate sample inventory
- nominal-versus-alternative triage authority

## Allowed fallback assumptions

- Data-driven templates are disallowed unless explicitly approved.
- Alternative MC samples remain non-central until the summary or a human approves their use.
- A technically possible but scientifically unsupported background remains unresolved rather than silently promoted.

## Output decision record

Record:

- analysis target
- reconstructed signal signature
- region map and likelihood roles
- allowed data-template sources and blocked template uses
- nominal-versus-alternative authority
- blocked assumptions that still require human input

## Verification Gate

### ASSERTIONS

1. A decision record exists before the inversion hands off, and it records the analysis target, reconstructed signal signature, region map with likelihood roles, allowed data-template sources and blocked template uses, nominal-versus-alternative authority, and blocked assumptions requiring human input.
2. The decision record explicitly confirms that sample relevance classification has not started before the physics target and reconstructed signal signature were made explicit.
3. The decision record explicitly confirms that no data sample will be treated as a template or transfer-factor source unless that use was approved in the intake decision.

### REPAIR

- Soft failure: rerun `signal_signature_and_likelihood_intake_inversion.md` to complete the missing target, signature, region-role, or template-policy fields and rerun this gate.
- Hard failure: return to Stage 1 of `sample_and_template_semantics_pipeline.md`; if incompatible signal signatures remain plausible or the authority for nominal-versus-alternative MC choice is still unclear, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: signal_signature_and_likelihood_intake_inversion
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

- `sample_strategy_inversion.md`
- `../generators/sample_semantics_generator.md`
- `../generators/data_driven_template_generator.md`
- `../reviewers/likelihood_sample_role_reviewer.md`
- `../shared/decision_record_template.md`
- `../shared/likelihood_sample_contract_schema.md`
