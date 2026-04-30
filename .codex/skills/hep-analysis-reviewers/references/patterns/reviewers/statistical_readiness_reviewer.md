# Statistical Readiness Reviewer

Pattern: Reviewer

Derived from:
- `SKILL_BACKGROUND_TEMPLATE_SMOOTHING_POLICY`
- `SKILL_MC_EFFECTIVE_LUMI_COVERAGE_GATE`
- `SKILL_SYSTEMATICS_AND_NUISANCES`
- `SKILL_WORKSPACE_AND_FIT_PYHF`
- `SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE`
- `SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB`
- `SKILL_STATTOOL_OPTIONAL_PYHF_BACKEND`

## Review scope

Verify that templates, model choices, systematics, fit backend, and significance semantics satisfy the repository rules for central statistical claims.

## Required evidence

- likelihood sample role review note
- effective-luminosity check artifact
- smoothing check and provenance artifacts
- signal and background model artifacts
- data-driven template contracts when used
- nuisance or systematics outputs
- fit backend provenance
- significance artifacts and parameter-floating policy

## Criteria

- `pass`: the model is auditable and allowed to support a central claim
- `conditional_pass`: a cross-check product is valid but explicitly not central
- `block`: a required gate artifact is missing or a central-result policy decision is unresolved
- `fail`: the statistical output violates binding repository policy

## Common failure modes

- effective luminosity below the required threshold for a fit-critical background without an explicit blocking status
- smoothing required but no provenance or pass artifact exists
- a data-driven template enters the model without closure expectations or without reviewed separation from observed data
- `pyhf` or another non-ROOT backend presented as the primary H to gammagamma result
- Asimov significance generated with the wrong range, the wrong hypothesis, or undocumented fixed and floating parameters

## Required remediation guidance

- resolve policy ambiguity through `../inversions/blinding_and_fit_policy_inversion.md`
- rerun `likelihood_sample_role_reviewer.md` when observed-data and template-source roles are mixed
- regenerate data-template artifacts with `../generators/data_driven_template_generator.md`
- regenerate model artifacts with `../generators/background_and_signal_model_generator.md`
- rerun fit products through `../generators/systematics_and_workspace_generator.md`

## Verification Gate

### ASSERTIONS

1. A reviewer verdict artifact or conversation note for `Statistical Readiness Reviewer` exists and records exactly one verdict from `pass`, `conditional_pass`, `block`, or `fail`.
2. The required evidence is present on disk or in the conversation: the likelihood sample role review note, effective-luminosity check artifact, smoothing check and provenance artifacts, signal and background model artifacts, data-driven template contracts when used, nuisance or systematics outputs, fit backend provenance, and significance artifacts with parameter-floating policy.
3. For a central H to gammagamma claim, the evidence explicitly confirms `pyroot_roofit` as the primary backend rather than an optional backend.
4. If expected significance is used, the evidence explicitly confirms `mu_gen = 1`, the signal-plus-background hypothesis, and the full `105-160 GeV` range; if a data-driven template enters the model, the evidence also confirms reviewed separation from observed data.

### REPAIR

- Soft failure: rerun the smallest blocked statistical component such as `data_driven_template_generator.md`, `background_and_signal_model_generator.md`, or `systematics_and_workspace_generator.md`, then rerun this reviewer gate.
- Hard failure: return to Stage 6 of `hep_analysis_meta_pipeline.md` for model or template repair, or return to Stage 7 of `hep_analysis_meta_pipeline.md` for fit and significance repair; if backend eligibility or central-result policy remains unresolved, route through `blinding_and_fit_policy_inversion.md` or escalate to a human, and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: statistical_readiness_reviewer
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
- `../shared/hep_domain_guardrails.md`
- `../shared/evidence_requirements.md`
