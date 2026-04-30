# Sample and Template Semantics Pipeline

Pattern: Pipeline

Derived from the sample-handling and background-strategy contracts in the source pack.

## Stage plan

| Stage | Entry criteria | Producing skills | Mandatory reviewer | Exit criteria |
|---|---|---|---|---|
| 1. Intake and likelihood scoping | analysis request exists | `../inversions/signal_signature_and_likelihood_intake_inversion.md` | none | physics target, signal signature, region roles, and template policy are explicit |
| 2. Registry and metadata resolution | intake decision exists | `../tool_wrappers/sample_registry_and_metadata_wrapper.md` | none | registry, metadata, and normalization inputs exist |
| 3. Relevance, nominality, and normalization strategy | registry exists | `../inversions/sample_strategy_inversion.md` | none | relevant processes, nominal samples, alternatives, and normalization modes are explicit |
| 4. Sample contract generation | strategy decision exists | `../generators/sample_semantics_generator.md` | `../reviewers/nominal_sample_and_normalization_reviewer.md` | sample contracts, nominal mapping, and normalization are reviewer-ready |
| 5. Data-driven template generation | intake and sample contracts allow template sources | `../generators/data_driven_template_generator.md` | `../reviewers/likelihood_sample_role_reviewer.md` | template-source contracts, overlap policy, and closure expectations are reviewer-approved |
| 6. Handoff to modeling | contracts and reviewer outcomes exist | `../generators/background_and_signal_model_generator.md` | `../reviewers/statistical_readiness_reviewer.md` | model inputs declare source class, normalization mode, and allowed downstream use |

## Gates

- Do not bypass the intake inversion when the signal signature or region roles are unclear.
- Do not advance to template generation before the central sample contracts are explicit.
- Do not advance to modeling if the reviewer cannot distinguish observed data from data-driven template sources.

## Logging requirements

- intake decision record
- sample-strategy decision record
- sample contract artifact inventory
- reviewer outcomes
- template overlap and closure notes when data-driven templates are used

## Escalation paths

- escalate when nominal-versus-alternative selection still requires human triage
- escalate when a data-driven template depends on an unsupported decorrelation assumption
- escalate when the same data sample would need to appear on both sides of the likelihood without a defensible disjoint-event policy

## Verification Gate

### ASSERTIONS

1. The pipeline log contains the `intake decision record`, `sample-strategy decision record`, `sample contract artifact inventory`, reviewer outcomes, and `template overlap and closure notes` whenever data-driven templates are used.
2. The pipeline did not advance past Stage 4 until `nominal_sample_and_normalization_reviewer.md` returned `pass` or `conditional_pass`, and it did not advance past Stage 5 until `likelihood_sample_role_reviewer.md` returned `pass` or `conditional_pass`.
3. The Stage 4 and Stage 5 artifacts explicitly preserve `36.1 fb^-1` as the central luminosity and preserve `cross section x k-factor x filter efficiency x signed generator-weight sum` as the central normalization basis rather than raw event counts.
4. The modeling handoff is blocked unless the artifacts explicitly distinguish observed data from data-driven template sources.

### REPAIR

- Soft failure: rerun the blocked stage in this pipeline to regenerate the missing decision record, contract set, reviewer outcome, or overlap note, then rerun this gate.
- Hard failure: return to the earliest blocked stage in the `## Stage plan` table of `sample_and_template_semantics_pipeline.md`; if nominality, normalization, or data-template separation still requires human triage, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: sample_and_template_semantics_pipeline
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

- `hep_analysis_meta_pipeline.md`
- `../shared/likelihood_sample_contract_schema.md`
- `../shared/hep_domain_guardrails.md`
