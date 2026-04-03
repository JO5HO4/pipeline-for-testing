# Runtime and Preflight Wrapper

Pattern: Tool Wrapper

Derived from:
- `SKILL_BOOTSTRAP_REPO`
- `SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY`
- `SKILL_ROOTMLTOOL_CACHED_ANALYSIS`

## When to use

Use this wrapper when the agent needs to verify that the repository can execute safely before any production claim or when a run must be bootstrapped from the repo entrypoints.

## Inputs

- repository root
- summary path
- inputs path
- outputs path
- optional `max_events` for smoke or scoped runs
- optional backend selection notes

## Outputs

- preflight outputs under `outputs/report/`
- normalized bootstrap outputs when `analysis.cli bootstrap` is used
- smoke or run manifest evidence when `analysis.cli run` is used

## Preconditions

- the repo checkout is readable
- the requested summary and input paths exist

## Postconditions

- runtime readiness is explicit as `ready`, `blocked`, or `failed`
- any fallback or backend choice is logged before downstream stages run

## Call procedure

1. Prefer the project-local interpreter: `.rootenv/bin/python`.
2. For bootstrap-only work, run `analysis.cli bootstrap`.
3. For readiness checks, run `analysis.cli preflight` or `analysis.preflight`.
4. For integrated smoke or production execution, run `analysis.cli run`.
5. If backend parity or cache promotion is in scope, keep the native path as the reference path and record parity evidence before promoting alternatives.

## Failure modes

- PyROOT or RooFit unavailable for a workflow that requires central H to gammagamma claims
- missing summary, inputs, or outputs path permissions
- backend parity not demonstrated for optional cached backends

## Verification expectations

- preflight artifacts exist
- bootstrap writes a normalized summary when requested
- smoke or run outputs produce a run manifest, verification artifacts, and reviewer-consumable logs

## Verification Gate

### ASSERTIONS

1. The wrapper outputs exist before handoff: `preflight outputs under outputs/report/`, `normalized bootstrap outputs` when `analysis.cli bootstrap` is used, and `smoke or run manifest evidence` when `analysis.cli run` is used.
2. Runtime readiness is recorded explicitly as `ready`, `blocked`, or `failed`, and any fallback or backend choice is logged before downstream stages run.
3. If the requested workflow can support a central H to gammagamma claim, the readiness evidence confirms RooFit availability and preserves `pyroot_roofit` as the central fit backend expectation.

### REPAIR

- Soft failure: rerun `runtime_and_preflight_wrapper.md` with corrected paths or runtime settings and rerun this gate.
- Hard failure: return to Stage 1 of `hep_analysis_meta_pipeline.md`; if the runtime cannot satisfy the requested central-result scope, escalate to `preflight_fact_check_reviewer.md` or a human, and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: runtime_and_preflight_wrapper
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

- `../reviewers/preflight_fact_check_reviewer.md`
- `../reviewers/reproducibility_and_handoff_reviewer.md`
- `../pipelines/hep_analysis_meta_pipeline.md`
