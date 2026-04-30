# HEP Analysis Meta Pipeline

Pattern: Pipeline

Derived from the source meta-skill and its reference library.

## Global rules

- Domain requirements override agent convenience.
- A stage is complete only when its mandatory reviewer passes.
- Every stage must log assumptions, deviations, unresolved issues, produced artifacts, and the next handoff target.
- If a central-result policy is violated, the stage blocks rather than silently downgrading itself.

## Stage plan

| Stage | Entry criteria | Producing skills | Mandatory reviewer | Exit criteria |
|---|---|---|---|---|
| 1. Runtime and environment setup | repo paths are known | `runtime_and_preflight_wrapper.md`, `spec_to_runtime_pipeline.md` | `preflight_fact_check_reviewer.md` | runtime readiness and authoritative summary path are explicit |
| 2. Sample identification and preparation | normalized summary exists | `sample_and_template_semantics_pipeline.md`, `signal_signature_and_likelihood_intake_inversion.md`, `sample_semantics_generator.md`, `sample_registry_and_metadata_wrapper.md`, `sample_strategy_inversion.md` | `nominal_sample_and_normalization_reviewer.md`, `likelihood_sample_role_reviewer.md` | central sample roles, nominal mapping, likelihood roles, and normalization are reviewer-approved |
| 3. Feature and variable preparation | sample semantics approved | `event_model_and_partition_generator.md`, `selection_and_partition_wrapper.md` | `analysis_summary_reviewer.md` | object, variable, and region contracts are executable |
| 4. Event selection and cut flow | region contracts executable | `selection_and_yield_generator.md` | `nominal_sample_and_normalization_reviewer.md` | yields and cut flows match the reviewed central sample set |
| 5. Categorization | selected events and reviewed partitions exist | `event_model_and_partition_generator.md`, `selection_and_partition_wrapper.md` | `analysis_summary_reviewer.md` | category definitions and overlap policy are explicit |
| 6. Background modeling or estimation | templates can be built | `histogram_and_template_generator.md`, `data_driven_template_generator.md`, `background_and_signal_model_generator.md`, `histogram_and_template_wrapper.md`, `sample_strategy_inversion.md`, `blinding_and_fit_policy_inversion.md` | `likelihood_sample_role_reviewer.md`, `statistical_readiness_reviewer.md` | background strategy, blinding state, template provenance, and model choices are reviewable |
| 7. Signal and background fitting or statistical setup | reviewed model artifacts exist | `systematics_and_workspace_generator.md`, `fit_and_significance_wrapper.md`, `blinding_and_fit_policy_inversion.md` | `statistical_readiness_reviewer.md` | workspace, fit, and significance outputs satisfy central-claim policy or are explicitly blocked |
| 8. Validation and cross-checks | statistical outputs exist or are explicitly blocked | `blinding_and_visualization_reviewer.md`, `data_mc_discrepancy_reviewer.md`, `reproducibility_and_handoff_reviewer.md` | same reviewers | visual, discrepancy, and reproducibility evidence are explicit |
| 9. Result packaging | validated outputs exist | `report_package_generator.md`, `report_packaging_wrapper.md` | `blinding_and_visualization_reviewer.md` | report package and plot manifest are reviewer-ready |
| 10. Report and log generation | report package exists | `reporting_and_handoff_pipeline.md`, `failure_to_skill_inversion.md` | `reproducibility_and_handoff_reviewer.md` | handoff package, enforcement status, and next-step notes are explicit |

## Stage-specific requirements

### 1. Runtime and environment setup

- confirm `.rootenv` or another approved interpreter path
- block immediately if the requested central claim requires capabilities the runtime does not have

### 2. Sample identification and preparation

- central luminosity defaults to `36.1 fb^-1` unless an approved override exists
- observed data, template-source data, and validation-only samples must be distinguishable in the contracts
- do not advance with unresolved nominal-sample ambiguity

### 3. Feature and variable preparation

- object definitions must exist before region logic
- executable definitions outrank prose summaries

### 4. Event selection and cut flow

- weighted and unweighted interpretations must both be preserved
- sample-resolved cut flows are the default

### 5. Categorization

- categories and regions must stay aligned with the reviewed summary
- any overlap exception requires justification

### 6. Background modeling or estimation

- nominal background template choice must be explicit
- data-driven templates require explicit source region, overlap policy, and closure expectations
- smoothing, if used, must be auditable

### 7. Signal and background fitting or statistical setup

- central H to gammagamma fits require RooFit
- expected significance in blinded development requires full-range Asimov pseudo-data

### 8. Validation and cross-checks

- discrepancies must be documented, not hidden
- cross-check backends remain labeled as cross-checks

### 9. Result packaging

- plots must be embedded inline with captions
- the report must separate central claims from blocked or cross-check outputs

### 10. Report and log generation

- handoff is invalid unless the enforcement gate and reviewer verdict both allow it
- every completed run must include failure-extraction notes or an explicit no-new-skill result

## Logging requirements

Use `../shared/pipeline_logging_contract.md` for every stage. The minimum log bundle is:

- run manifest
- execution contract
- stage-by-stage assumptions and deviations
- reviewer outcomes
- final handoff state

## Escalation paths

- human approval is required for unblinding, central-result luminosity overrides, or any attempt to treat a cross-check backend as primary
- escalate when central sample semantics cannot be resolved from repository evidence
- escalate when a reviewer would have to infer compliance from missing artifacts

## Verification Gate

### ASSERTIONS

1. For every completed stage in the `## Stage plan`, the pipeline log contains the mandatory artifacts, assumptions, deviations, unresolved issues, produced-artifact list, and next handoff target required by `../shared/pipeline_logging_contract.md`.
2. No stage is marked complete unless its mandatory reviewer returned `pass` or `conditional_pass`; a `block` or `fail` verdict is not bypassed anywhere in the stage log.
3. Stage 2 and Stage 6 artifacts explicitly preserve reviewer-approved sample roles, template provenance, and blinding behavior, including the rule that `120-130 GeV` is not exposed in blinded mode.
4. Stage 7 statistical artifacts explicitly preserve `pyroot_roofit` as the central H to gammagamma backend, and any expected significance path records `mu_gen = 1`, the signal-plus-background hypothesis, and the full `105-160 GeV` range.

### REPAIR

- Soft failure: repair the missing stage artifact or reviewer evidence in place at the blocked stage, rerun that stage, and then rerun this gate from the pipeline log.
- Hard failure: return to the earliest blocked stage in the `## Stage plan` table of `hep_analysis_meta_pipeline.md`; if a central-result policy would still be violated or a reviewer would need to infer compliance from missing artifacts, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: hep_analysis_meta_pipeline
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

- `../inversions/analysis_router_inversion.md`
- `../shared/hep_domain_guardrails.md`
- `../shared/artifact_matrix.md`
