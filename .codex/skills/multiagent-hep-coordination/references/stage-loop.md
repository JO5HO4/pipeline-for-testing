# Stage Worker/Reviewer Loop

Use this reference when coordinating a staged multiagent analysis. There are only two delegated roles:

- `stage_worker`
- `stage_reviewer`

The coordinator first derives the stage plan from the analysis JSON, then launches fresh worker/reviewer instances for each selected stage with a stage-specific brief.

## Dynamic Stage Planning

Before launching workers, write `handoff/stage_plan.json`.

The plan must be derived from:

- `analysis/analysis.summary.json` when present, otherwise the analysis JSON in `analysis/`
- available input data
- existing repository code
- whether ROOT/RooFit or another backend is required
- whether observed results, validation regions, control proxies, or diagnostic-only outputs are allowed

The coordinator may skip, merge, split, or add stages. Examples:

- Skip `runtime` only if no runtime-sensitive backend is required and a minimal Python smoke test passes.
- Split `sample_branch` when branch audit and sample-role classification are independently complex.
- Merge `yield_plot` into `reporting` only for a tiny smoke analysis.
- Add `roofit_repair` when Hyy central fitting needs RooFit and no passing runtime exists.
- Add `proxy_policy` when the analysis JSON defines open-data signal proxies.

## Stage Templates

Use these as default templates, not a fixed list:

1. `runtime`
2. `sample_branch`
3. `object_preselection`
4. `categorization`
5. `yield_plot`
6. `statistics`
7. `reporting`
8. `final_review`

## Stage Plan Schema

```json
{
  "analysis_contract": "analysis/analysis.summary.json",
  "planning_basis": {
    "analysis_json_features": [],
    "repo_features": [],
    "input_data_features": []
  },
  "stages": [
    {
      "stage_id": "sample_branch",
      "reason": "analysis requires sample discovery and branch audit",
      "required": true,
      "may_skip": false,
      "depends_on": [],
      "required_artifacts": [],
      "review_checks": []
    }
  ],
  "skipped_templates": [
    {
      "stage_id": "runtime",
      "reason": "no ROOT-backed or environment-sensitive backend requested"
    }
  ]
}
```

## Loop

For each stage in `handoff/stage_plan.json`:

```text
WRITE_STAGE_BRIEF -> SPAWN_WORKER -> WAIT_FOR_ARTIFACTS -> SPAWN_REVIEWER -> REPAIR_IF_NEEDED -> PROCEED_OR_BLOCK
```

Default max repair retries per stage: 2.

Proceed only when the reviewer returns `pass` or an explicitly allowed `conditional_pass`.

Block when the reviewer returns `blocked` or `fail` after repair attempts, or when a contract change is requested without `outputs/contracts/scope_change_decision.json`.

## Stage Brief Schema

Write `handoff/<stage>/stage_brief.json` before spawning the worker:

```json
{
  "stage_id": "sample_branch",
  "role_model": "generic_stage_worker_then_generic_stage_reviewer",
  "analysis_contract": "analysis/analysis.summary.json",
  "entry_criteria": [],
  "required_inputs": [],
  "required_artifacts": [],
  "review_checks": [],
  "blocking_conditions": [],
  "claim_policy": "follow the analysis JSON; do not promote diagnostic outputs"
}
```

## Default Stage Requirements

### runtime

Artifacts:

- `outputs/contracts/runtime_contract.json`
- `outputs/report/root_runtime_repair_attempts.json` when ROOT/RooFit is needed or fails

Review checks:

- PyROOT import is not enough; RooFit needs a fit smoke test with timeout
- Hyy central fit blocks unless RooFit smoke passes
- selected runtime path is used by downstream commands

### sample_branch

Artifacts:

- `outputs/samples/all_discovered_samples.json`
- `outputs/samples/central_samples.json`
- `outputs/report/branch_audit.json`
- `outputs/normalization/norm_table.json`

Review checks:

- required branches exist in central samples
- excluded samples have reasons
- sample scope follows the analysis JSON
- missing official inputs are classified as blocked, diagnostic, or not applicable

### object_preselection

Artifacts:

- `outputs/report/object_definitions.json`
- `outputs/report/preselection_cutflow.json`
- `outputs/report/event_prefilter_policy.json`

Review checks:

- object definitions use available branches
- b-tag and trigger approximations are honestly named
- I/O prefilters are separate from physics cuts

### categorization

Artifacts:

- `outputs/report/category_definitions.json`
- `outputs/report/region_masks.json`
- `outputs/report/region_overlap_sanity.json`

Review checks:

- categories and regions match the analysis JSON
- overlap is measured before any combined statistic is claimed

### yield_plot

Artifacts:

- `outputs/report/yields_by_region.json`
- `outputs/report/validation_yields.json` when applicable
- `outputs/report/control_proxy_yields.json` when applicable
- `outputs/report/plots/manifest.json`

Review checks:

- expected/background/signal-proxy separation is preserved
- raw signed MC yields are preserved
- plots referenced by the report exist

### statistics

Artifacts:

- `outputs/stats/expected_results.json`
- `outputs/stats/observed_results.json` when observed results are allowed
- `outputs/report/statistics_policy.json`

Review checks:

- expected model is fixed before observed counts
- Hyy central result uses RooFit if required
- VLQ proxy results are not official CLs/mass limits
- fallback outputs are labeled diagnostic

### reporting

Artifacts:

- final report
- `outputs/evaluation_scorecard.json`
- reproducibility commands

Review checks:

- report language follows the weakest valid claim classification
- substitutions and blocked claims are explicit

### final_review

Artifacts:

- `reviews/final_artifact_review.json`
- `reviews/final_claim_review.json`

Review checks:

- final package is complete and reproducible
- no central claim exceeds analysis JSON, runtime contract, or claim policy

## Worker Prompt Template

```text
You are the stage_worker for <stage_id>. Read handoff/<stage_id>/stage_brief.json and the analysis contract. Work only on this stage. Produce the required artifacts. Do not change sample scope, object definitions, backend, statistic shape, blinding, or claim policy unless you write outputs/contracts/scope_change_decision.json and stop. Return files changed, artifacts produced, commands run, blockers, and reviewer focus.
```

## Reviewer Prompt Template

```text
You are the stage_reviewer for <stage_id>. Read handoff/<stage_id>/stage_brief.json, the analysis contract, and the worker artifacts. Do not repair. Return pass, conditional_pass, blocked, non_comparable, or fail. Cite missing artifacts, contract violations, and required repair actions.
```

## Repair Rule

If a review identifies an upstream root cause, mark the upstream stage `needs_revisit`, rerun it, then rerun every downstream stage whose artifacts may have changed.
