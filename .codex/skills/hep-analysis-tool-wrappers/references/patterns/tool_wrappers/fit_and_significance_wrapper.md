# Fit and Significance Wrapper

Pattern: Tool Wrapper

Derived from:
- `SKILL_WORKSPACE_AND_FIT_PYHF`
- `SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE`
- `SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB`
- `SKILL_STATTOOL_OPTIONAL_PYHF_BACKEND`

## When to use

Use this wrapper when the agent needs to execute the repository fit, systematics, or significance code after policy decisions have already established whether the result can support a central claim.

## Inputs

- reviewed model artifacts
- reviewed template artifacts
- fit identifier
- backend decision record
- output directory

## Outputs

- fit outputs under `outputs/fit/<FIT_ID>/`
- significance outputs under `outputs/fit/<FIT_ID>/`
- systematics outputs consumed by the final report

## Preconditions

- statistical readiness reviewer has not blocked the stage
- pipeline skill compliance auditor has passed or conditionally passed the planned executable code path for the intended central claims
- any central-result backend decision has already been made

## Postconditions

- fit and significance provenance are explicit
- cross-check results are labeled as cross-checks rather than silently promoted

## Call procedure

1. Use `.rootenv/bin/python -m analysis.stats.fit` for direct fit execution when the workspace is already prepared.
2. Use `.rootenv/bin/python -m analysis.stats.systematics` when nuisance artifacts need a focused refresh.
3. Use `.rootenv/bin/python -m analysis.cli run` when fit and significance should remain coupled to the integrated pipeline.
4. Use direct Python entrypoints for significance only when the stage contract explicitly documents the function-level invocation and provenance.

## Failure modes

- RooFit unavailable for a central H to gammagamma claim
- significance constructed with the wrong blinding scope or parameter-floating policy
- raw diagnostic Asimov `q0`/`Z` from a failed closure, poor fit status, bad covariance, or POI-at-bound fit promoted to a central expected-significance claim
- weighted bin-center RooDataSet plus extended unbinned likelihood used as the central H to gammagamma Asimov method
- any central output produced by a code path that the pipeline skill compliance audit marks `diagnostic_only` or `noncompliant_blocking`
- optional backends mislabeled as central outputs

## Verification expectations

- fit provenance names the backend
- significance provenance names the dataset type and generation hypothesis
- central expected-significance artifacts expose `claim_status`, `accepted_q0`, `accepted_z_discovery`, free/conditional fit status, covariance quality, POI-bound diagnostics, and closure status
- blocked or diagnostic-only Asimov artifacts keep raw `q0`/`Z` out of central report fields
- reviewer evidence distinguishes expected and observed significance
- pipeline skill compliance audit records the governing skills, executable code path, artifact paths, and compliance status for every central fit or significance claim

## Verification Gate

### ASSERTIONS

1. The wrapper outputs exist before handoff: `fit outputs under outputs/fit/<FIT_ID>/`, `significance outputs under outputs/fit/<FIT_ID>/`, and the `systematics outputs consumed by the final report`.
2. The fit provenance in `outputs/fit/<FIT_ID>/` names the backend explicitly, and any cross-check result is labeled as a cross-check rather than silently promoted.
3. The significance provenance names the dataset type and generation hypothesis; for a central H to gammagamma result the backend is `pyroot_roofit`, and if expected significance is present the provenance records `mu_gen = 1`, the full `105-160 GeV` range, `claim_status = "accepted"`, finite `accepted_q0`/`accepted_z_discovery`, successful closure, acceptable fit status/covariance quality, and no POI-at-bound condition.
4. A weighted bin-center RooDataSet in an extended unbinned likelihood is not used as the central H to gammagamma expected-significance method. Its raw `q0`/`Z` values are diagnostic-only and the gate is blocked for central reporting even if closure appears acceptable.
5. A pipeline skill compliance audit exists for this fit/significance stage and does not mark any central output as `diagnostic_only` or `noncompliant_blocking`.

### REPAIR

- Soft failure: rerun `fit_and_significance_wrapper.md` with the corrected backend, provenance, or output target and rerun this gate.
- Hard failure: return to Stage 7 of `hep_analysis_meta_pipeline.md`; if backend eligibility or significance policy is still unresolved, route through `blinding_and_fit_policy_inversion.md` or `statistical_readiness_reviewer.md`, and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: fit_and_significance_wrapper
assertions_checked:
  - assertion_1
  - assertion_2
  - assertion_3
  - assertion_4
  - assertion_5
assertion_results:
  assertion_1: pass|fail
  assertion_2: pass|fail
  assertion_3: pass|fail
  assertion_4: pass|fail
  assertion_5: pass|fail
violations_found: <integer>
repair_applied: true|false  # with one-line description if true
gate_outcome: PASS | CONDITIONAL_PASS | BLOCKED | ESCALATED
next_skill: <skill filename or "human">
```

The agent must not proceed if `gate_outcome` is `BLOCKED` or `ESCALATED`.

## Related skills

- `../generators/systematics_and_workspace_generator.md`
- `../reviewers/pipeline_skill_compliance_auditor.md`
- `../reviewers/statistical_readiness_reviewer.md`
- `../inversions/blinding_and_fit_policy_inversion.md`
