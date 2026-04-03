# Blinding and Visualization Reviewer

Pattern: Reviewer

Derived from:
- `SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION`
- `SKILL_VISUAL_VERIFICATION`
- `SKILL_HISTOGRAM_PLOTTING_INVARIANTS`

## Review scope

Verify that blinding, plot content, plot captions, and visual diagnostics satisfy repository physics and reporting rules.

## Required evidence

- blinding summary
- plot manifest
- report markdown or draft
- category, control-region, and signal-region plots

## Criteria

- `pass`: blinding and visual requirements are satisfied and traceable
- `conditional_pass`: minor style issues remain but the scientific message and blinding state are intact
- `block`: a required plot class or caption is missing, or blinding behavior is undocumented
- `fail`: observed data in a blinded window are exposed or required H to gammagamma plots are absent

## Common failure modes

- signal-region observed data shown in blinded mode
- control-region pre-fit and post-fit comparisons missing
- plot captions absent or detached from the figures
- category-resolved or statistical-input plots missing for H to gammagamma

## Required remediation guidance

- use `../inversions/blinding_and_fit_policy_inversion.md` to resolve policy ambiguity
- rerun `../generators/background_and_signal_model_generator.md` or `../generators/report_package_generator.md` for missing artifacts
- keep discrepancies visible; never remediate by hiding bins or relabeling plots cosmetically

## Verification Gate

### ASSERTIONS

1. A reviewer verdict artifact or conversation note for `Blinding and Visualization Reviewer` exists and records exactly one verdict from `pass`, `conditional_pass`, `block`, or `fail`.
2. The required evidence is present on disk or in the conversation: the `blinding summary`, the `plot manifest`, the report markdown or draft, and the category, control-region, and signal-region plots.
3. The evidence explicitly confirms that `120-130 GeV` is not exposed in blinded mode and that required plot classes and captions are present rather than assumed.

### REPAIR

- Soft failure: rerun `background_and_signal_model_generator.md`, `report_package_generator.md`, or the plotting stage that missed the required artifact, then rerun this reviewer gate.
- Hard failure: return to Stage 6 of `hep_analysis_meta_pipeline.md` for blinding-policy repair or Stage 9 of `hep_analysis_meta_pipeline.md` for report and plot repair; escalate to `blinding_and_fit_policy_inversion.md` or a human if blinded content would otherwise be exposed.
- If `gate_outcome` is `BLOCKED` or `ESCALATED`, do not proceed.

### HANDOFF RECORD

Emit this log entry before proceeding:

```yaml
stage_id: blinding_and_visualization_reviewer
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

- `../shared/plotting_invariants.md`
- `../generators/report_package_generator.md`
