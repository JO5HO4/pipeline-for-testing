# Blinding and Fit Policy Inversion

Pattern: Inversion

Derived from:
- `SKILL_ENFORCEMENT_POLICY_DEFAULTS`
- `SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION`
- `SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION`
- `SKILL_WORKSPACE_AND_FIT_PYHF`
- `SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE`
- `SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB`
- `SKILL_STATTOOL_OPTIONAL_PYHF_BACKEND`
- `SKILL_ROOTMLTOOL_CACHED_ANALYSIS`

## Trigger condition

Use this inversion when the agent must decide whether a fit, significance result, smoothing choice, or backend can legitimately support a central claim.

## Decision structure

1. Decide whether the run is blinded or explicitly unblinded.
2. Decide whether the requested statistical output is expected or observed.
3. Decide whether the available backend can support a central claim or only a cross-check.
4. Decide whether effective-luminosity and smoothing rules are satisfied or should block the stage.

## Branch criteria

- Blinded run: observed significance is blocked; expected significance may proceed only with full-range Asimov pseudo-data.
- Explicitly unblinded run: observed significance may proceed if the reviewer evidence is complete.
- RooFit available: central H to gammagamma fit path is allowed.
- Only non-ROOT backend available: cross-check only, or block if the user requested a central claim.
- Effective luminosity below policy or smoothing required without provenance: block central fit progression.

## Required evidence per branch

- enforcement or luminosity artifacts
- smoothing artifacts
- backend availability evidence
- blinding summary
- user-approved unblinding status when applicable

## Output decision record

Record:

- blinding state
- allowed significance modes
- allowed backend role
- smoothing and effective-luminosity disposition
- blocking reasons

## Verification Gate

### ASSERTIONS

1. A decision record exists before the inversion hands off, and it records the blinding state, allowed significance modes, allowed backend role, and the smoothing and effective-luminosity disposition.
2. If the run is blinded, the decision record explicitly confirms that `120-130 GeV` will not be exposed; if observed significance is allowed, the required human unblinding approval is recorded explicitly.
3. For central H to gammagamma claims, the decision record confirms `pyroot_roofit` as the allowed primary backend; if expected significance is allowed, it records `mu_gen = 1`, the signal-plus-background hypothesis, and the full `105-160 GeV` range.

### REPAIR

- Soft failure: rerun `blinding_and_fit_policy_inversion.md` to rewrite the decision record with the missing blinding, backend, smoothing, or significance policy evidence, then rerun this gate.
- Hard failure: return to Stage 6 of `hep_analysis_meta_pipeline.md` for blinding or modeling policy repair, or return to Stage 7 of `hep_analysis_meta_pipeline.md` for fit and significance policy repair; if required approvals are missing, escalate to a human and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: blinding_and_fit_policy_inversion
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

- `../reviewers/statistical_readiness_reviewer.md`
- `../shared/hep_domain_guardrails.md`
