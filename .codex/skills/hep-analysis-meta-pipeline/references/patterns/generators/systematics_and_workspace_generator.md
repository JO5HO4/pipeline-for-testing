# Systematics and Workspace Generator

Pattern: Generator

Derived from:
- `SKILL_SYSTEMATICS_AND_NUISANCES`
- `SKILL_WORKSPACE_AND_FIT_PYHF`
- `SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE`
- `SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB`

## Purpose

Generate nuisance, workspace, fit, and significance artifacts after the policy decisions and reviewer gates have established what statistical products are allowed to count as central results.

## When to use

- modeling artifacts are reviewed
- template readiness is reviewed
- the workflow is ready to construct workspaces, fits, and significance products

## Required inputs

- reviewed modeling artifacts
- reviewed templates
- systematics scope
- fit-policy decision record
- fit identifier

## Outputs

- nuisance model
- workspace and fit provenance
- fit results
- significance artifacts
- Asimov provenance and parameter-floating policy

## Generation steps

1. Build nuisance and correlation metadata.
2. Materialize the workspace and fit configuration.
3. Execute the fit wrapper with the approved backend choice.
4. Construct observed or expected significance only if the fit-policy inversion allows it.
5. Record which quantities were fixed or floating, especially for H to gammagamma DSCB and background parameters.

## Output contract

- central H to gammagamma claims name `pyroot_roofit` as the primary backend
- Asimov generation records full-range provenance and `mu_gen = 1` when used for expected discovery significance
- expected and observed significance are never conflated

## Constraints

- a blocked central fit remains blocked rather than downgraded silently into a cross-check
- reviewer gates must pass before the report treats these artifacts as central claims

## Verification Gate

### ASSERTIONS

1. The `nuisance model`, `workspace and fit provenance`, `fit results`, `significance artifacts`, and `Asimov provenance and parameter-floating policy` all exist before any central statistical claim is handed forward.
2. For central H to gammagamma claims, the `workspace and fit provenance` names `pyroot_roofit` as the primary backend rather than treating an optional backend as central.
3. If expected significance is produced, the `Asimov provenance and parameter-floating policy` records `mu_gen = 1`, the signal-plus-background hypothesis, and the full `105-160 GeV` range.
4. The `fit results` and `significance artifacts` keep expected and observed significance distinct and do not silently downgrade a blocked central fit into a cross-check.

### REPAIR

- Soft failure: rerun `systematics_and_workspace_generator.md` or `fit_and_significance_wrapper.md` to regenerate the missing nuisance, workspace, fit, or significance artifacts and rerun the gate.
- Hard failure: return to Stage 7 of `hep_analysis_meta_pipeline.md`; if backend eligibility, Asimov construction, or parameter-floating policy is still unresolved, route through `blinding_and_fit_policy_inversion.md` or `statistical_readiness_reviewer.md` and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: systematics_and_workspace_generator
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

- `../tool_wrappers/fit_and_significance_wrapper.md`
- `../reviewers/statistical_readiness_reviewer.md`
- `../inversions/blinding_and_fit_policy_inversion.md`
