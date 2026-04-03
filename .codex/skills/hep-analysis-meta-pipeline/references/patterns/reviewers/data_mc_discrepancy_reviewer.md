# Data-MC Discrepancy Reviewer

Pattern: Reviewer

Derived from:
- `SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK`

## Review scope

Check whether substantial disagreement between observed data and MC expectations has been investigated, classified, and reported honestly.

## Required evidence

- data-versus-MC plots and tables
- discrepancy audit
- discrepancy check log
- cut-flow and yield context
- normalization and sample-mapping artifacts

## Criteria

- `pass`: the audit exists and all substantial discrepancies are either explained or openly unresolved
- `conditional_pass`: no substantial discrepancy is present and the explicit zero-issue path is documented
- `block`: discrepancy artifacts are missing or incomplete
- `fail`: the workflow hid or cosmetically suppressed a material discrepancy

## Common failure modes

- discrepancy artifacts missing on a supposedly clean run
- changes to binning, selection, or sample composition made only to improve visual agreement
- bug and modeling-mismatch cases not distinguished

## Required remediation guidance

- send implementation issues to `../inversions/failure_to_skill_inversion.md`
- rerun the affected generator or wrapper with the smallest possible write scope
- keep the discrepancy visible in the report even when unresolved

## Verification Gate

### ASSERTIONS

1. A reviewer verdict artifact or conversation note for `Data-MC Discrepancy Reviewer` exists and records exactly one verdict from `pass`, `conditional_pass`, `block`, or `fail`.
2. The required evidence is present on disk or in the conversation: data-versus-MC plots and tables, the discrepancy audit, the discrepancy check log, cut-flow and yield context, and normalization and sample-mapping artifacts.
3. The evidence explicitly confirms either that every substantial discrepancy was classified and reported honestly or that the explicit zero-issue path was documented; no discrepancy is treated as resolved solely by cosmetic changes.

### REPAIR

- Soft failure: rerun the smallest affected generator or wrapper to restore the missing discrepancy artifact or context, then rerun this reviewer gate.
- Hard failure: return to Stage 8 of `hep_analysis_meta_pipeline.md`; if a material discrepancy would need to be hidden to continue, route through `failure_to_skill_inversion.md` or escalate to a human, and do not proceed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: data_mc_discrepancy_reviewer
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

- `../generators/report_package_generator.md`
- `reproducibility_and_handoff_reviewer.md`
