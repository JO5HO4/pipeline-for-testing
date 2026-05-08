# Pipeline Skill Compliance Auditor

Pattern: Reviewer

Derived from:
- skill-governed pipeline failures observed in H to gammagamma Asimov fitting
- central-claim enforcement requirements in `hep_analysis_meta_pipeline.md`

## Review scope

Audit the executable pipeline against the binding skill contracts before central statistical outputs or final reports are accepted. This reviewer checks whether the code path and produced artifact metadata comply with the skills that govern each central claim, not merely whether the run completed.

## Required evidence

- active skill index and stage plan
- analysis JSON or normalized summary
- pipeline execution contract or run manifest
- code-path inventory for central outputs
- claim-to-skill mapping for every central or report-visible physics result
- produced artifacts for the audited stage
- report draft when final-report claims are audited
- grep or static-inspection notes for forbidden, diagnostic-only, or fallback implementation paths
- deterministic guard artifacts where available, including `outputs/report/vlq_scope_guard.json` for VLQ-style aggregate-yield handoff

## Required output

Write `outputs/report/pipeline_skill_compliance_audit.json` or the stage-local equivalent before fit/significance handoff and before final report approval.

The artifact must contain:

```json
{
  "status": "pass|conditional_pass|blocked",
  "audit_scope": "pre_fit|pre_statistics|pre_report|final",
  "claims": [
    {
      "claim_id": "<stable claim or output id>",
      "claim_classification": "central|diagnostic|blocked|cross_check",
      "governing_skills": ["<skill or pattern path>"],
      "code_paths": ["<file:function or CLI path>"],
      "artifact_paths": ["<path>"],
      "compliance_status": "compliant|diagnostic_only|noncompliant_blocking|not_applicable",
      "evidence": ["<specific code or artifact evidence>"],
      "required_repairs": ["<repair if noncompliant>"]
    }
  ],
  "forbidden_path_findings": [
    {
      "id": "<finding id>",
      "severity": "warning|blocking",
      "pattern": "<forbidden or diagnostic-only pattern>",
      "path": "<code or artifact path>",
      "evidence": "<specific evidence>",
      "required_repair": "<repair>"
    }
  ],
  "gate_outcome": "PASS|CONDITIONAL_PASS|BLOCKED"
}
```

## Criteria

- `pass`: all central claims are traceable to compliant code paths and artifact metadata.
- `conditional_pass`: only diagnostic or cross-check outputs use fallback paths, and central claims are explicitly blocked or absent.
- `blocked`: any central claim depends on an implementation mode forbidden by its governing skill, a diagnostic-only fallback, missing compliance evidence, or an artifact whose metadata contradicts the skill contract.

## Mandatory checks

1. Build a claim-to-skill map before auditing code. At minimum include expected significance, observed significance or limits, central yields, background estimates, signal proxies, plots used for claims, and final report headline numbers.
2. For each central claim, trace the executable path that produced it. Use CLI records, pipeline entrypoints, function names, and artifact provenance rather than prose-only descriptions.
3. Search the code and artifacts for forbidden or diagnostic-only modes named by the governing skills.
4. Compare artifact metadata with the allowed skill modes. Missing metadata is a blocking finding for central claims.
5. Verify that blocked, diagnostic-only, or cross-check results are not promoted in reports, summaries, scorecards, or handoff records.
6. Rerun this audit after any repair that changes central code paths, fit methods, sample roles, yield aggregation, or report claims.

## H to gammagamma Asimov hard gate

For central H to gammagamma expected-significance claims:

- `construction_mode` must be one of `direct_generation`, `binned_roodatahist`, or `binned_poisson`.
- `weighted_bin_center_dataset`, `weighted_dataset_object_type = RooDataSet`, or an extended unbinned weighted RooFit likelihood is `noncompliant_blocking` for central expected significance.
- Closure success alone does not promote a weighted bin-center RooDataSet path to central eligibility.
- The audit must inspect both `significance_asimov.json` and `significance_asimov_construction.json` when present.
- The audit must block if raw diagnostic `q0` or `z_discovery` is used in central report text while `claim_status` is not `accepted` or accepted fields are null.

## VLQ and counting-analysis hard gate

For VLQ-style or counting-proxy analyses:

- Before any plot, report, fit, significance, or central-yield claim consumes aggregate yields, run:

```bash
python .codex/skills/hep-pipeline-skill-compliance-audit/scripts/vlq_scope_guard.py --repo .
```

- Central region yields must trace to the reviewed central sample set.
- Noncentral generator, shower, radiation, systematic, or signal-hypothesis alternatives must not enter central backgrounds unless the analysis contract explicitly promotes them.
- In same-sign dilepton, trilepton, fake/nonprompt-lepton, or charge-misID-sensitive regions, raw reducible MC such as `ttbar`, inclusive `W+jets`, inclusive `Z+jets`, and multijet/photon samples must not support a central `expected background` claim unless a reviewed data-driven, hybrid, or closure-backed reducible-background method promotes them.
- Central yield artifacts for these channels must separate `prompt_mc_background`, `data_driven_reducible_background` if available, and `reducible_mc_proxy_diagnostic`; if the split is absent, central expected-background and data-MC agreement claims are `noncompliant_blocking`.
- Plots or reports that include raw reducible MC proxies must label the stack as diagnostic or explicitly show the prompt/reducible split; calling such a stack simply `expected background`, `total background`, or `MC prediction` is `noncompliant_blocking`.
- If a signal proxy yield is zero, below 1 weighted event, or has `S/B < 0.05`, the affected claim must be marked weak-proxy diagnostic or blocked unless a reviewed signal-proxy viability audit says otherwise.
- If `B/Data > 1.5`, `Data/B > 1.5`, or an equivalent discrepancy threshold is exceeded in a claim-visible region, a data-MC discrepancy audit must exist before report approval.
- If the guard artifact is missing, stale relative to the aggregate yields, or has `gate_outcome: BLOCKED`, central yield, background, data-MC agreement, and signal-sensitivity claims are `noncompliant_blocking`.

## Verification Gate

### ASSERTIONS

1. A pipeline skill compliance audit artifact exists for the current gate scope and records every central or report-visible result with a claim classification, governing skills, code paths, artifact paths, and compliance status.
2. Every central claim is backed by executable code-path evidence and artifact metadata that match the allowed modes in its governing skills.
3. No forbidden or diagnostic-only implementation path supports a central claim; H to gammagamma expected significance never uses weighted bin-center `RooDataSet` or extended unbinned weighted RooFit as central.
4. Blocked, diagnostic-only, or cross-check outputs are not promoted in report text, summaries, scorecards, or handoff records.
5. If the audit finds any `noncompliant_blocking` item, the audited stage does not proceed until repair and a fresh compliance audit pass or conditional pass is recorded.
6. For VLQ-style aggregate yields, `outputs/report/vlq_scope_guard.json` exists with `gate_outcome: PASS|CONDITIONAL_PASS`, and any required discrepancy or signal-proxy viability audit is present before report-visible claims are accepted.

### REPAIR

- Soft failure: update missing provenance, claim mapping, or report classification and rerun this auditor.
- Hard failure: return to the earliest stage that introduced the noncompliant code path or artifact. Repair the executable method, not just the report wording, when a central claim depends on a forbidden implementation.
- If `gate_outcome` is `BLOCKED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: pipeline_skill_compliance_auditor
assertions_checked:
  - assertion_1
  - assertion_2
  - assertion_3
  - assertion_4
  - assertion_5
  - assertion_6
assertion_results:
  assertion_1: pass|fail
  assertion_2: pass|fail
  assertion_3: pass|fail
  assertion_4: pass|fail
  assertion_5: pass|fail
  assertion_6: pass|fail
violations_found: <integer>
repair_applied: true|false
gate_outcome: PASS | CONDITIONAL_PASS | BLOCKED
next_skill: <skill filename or "human">
```

The agent must not proceed if `gate_outcome` is `BLOCKED`.

## Related skills

- `statistical_readiness_reviewer.md`
- `data_mc_discrepancy_reviewer.md`
- `../tool_wrappers/fit_and_significance_wrapper.md`
- `../generators/report_package_generator.md`
- `../pipelines/hep_analysis_meta_pipeline.md`
