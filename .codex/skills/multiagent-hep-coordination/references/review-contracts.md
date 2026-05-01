# Review Contracts

Use this reference when writing stage audits.

## Shared Audit Schema

```json
{
  "stage": "<stage>",
  "cycle": 1,
  "audit_mode": "local_self_check|independent_review|final_artifact_review|final_claim_review",
  "auditor_role": "coordinator|reviewer|final_artifact_reviewer|final_claim_reviewer",
  "auditor_tag": "<agent_tag>",
  "status": "OK|WARNING|PROBLEM|PASS|CONDITIONAL_PASS|FAIL",
  "summary": "",
  "artifacts_reviewed": {"files": [], "plots": []},
  "findings": [],
  "veto_findings": [],
  "warning_findings": [],
  "required_repairs": [],
  "can_proceed": false,
  "handoff_allowed": false,
  "rerun_required_from_stage": "none"
}
```

## Mandatory Veto Classes

Set `PROBLEM` or `FAIL` when any apply:

- missing data provenance before observed results;
- unsupported paper-level claim;
- partial/smoke/capped run promoted as final;
- missing ROOT runtime repair evidence for ROOT-backed fallback/blocking;
- missing sample scope or contradictory sample counts;
- invalid statistical model, silent negative-yield stabilization, or unsupported observed result;
- missing report-number trace for final numbers;
- plot/caption overclaims or unblinding violation;
- scorecard/test summary mismatch;
- final reviewer not independent from implementation.

Reviewers may approve diagnostic output while blocking paper-level claims only when the allowed scope is explicitly recorded.
