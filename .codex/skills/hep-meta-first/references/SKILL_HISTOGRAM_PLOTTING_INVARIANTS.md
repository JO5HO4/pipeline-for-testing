---
skill_id: SKILL_HISTOGRAM_PLOTTING_INVARIANTS
display_name: "Histogram Plotting Invariants"
version: 1.0
category: plotting

summary: "All 1D histogram plots must satisfy consistent statistical and visual invariants unless the user explicitly overrides them."

invocation_keywords:
  - "histogram plotting invariants"
  - "plotting"
  - "histogram"
  - "invariants"

when_to_use:
  - "Use when executing or validating the plotting stage of the analysis workflow."
  - "Use when this context is available: analysis configuration and stage-specific upstream artifacts."
  - "Use when this context is available: repository paths and runtime context for the current run."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: analysis_configuration_and_stage_specific_upstream_artifacts
      type: artifact
      description: "analysis configuration and stage-specific upstream artifacts"
    - name: repository_paths_and_runtime_context_for_the_current_run
      type: artifact
      description: "repository paths and runtime context for the current run"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: 1d_histogram_figures_with_visible_statistical_uncertainties
    type: artifact
    description: "1D histogram figures with visible statistical uncertainties."
  - name: overlay_figures_with_shared_binning_and_ratio_panels
    type: artifact
    description: "Overlay figures with shared binning and ratio panels."
  - name: ratio_panels_with_fixed_0_5_1_5_y_range_and_r_1_reference_line
    type: artifact
    description: "Ratio panels with fixed `[0.5, 1.5]` y-range and `R=1` reference line."
  - name: plot_metadata_showing_binning_and_normalization_choice
    type: artifact
    description: "Plot metadata (or reproducible code path) showing binning and normalization choice."

preconditions:
  - "Dependency SKILL_HISTOGRAMMING_AND_TEMPLATES has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_HISTOGRAM_PLOTTING_INVARIANTS are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_HISTOGRAMMING_AND_TEMPLATES

  may_follow:
    - SKILL_HISTOGRAMMING_AND_TEMPLATES

allowed_tools:
  - Read
  - Write
  - Edit
  - Bash

allowed_paths:
  - analysis/
  - input-data/
  - outputs*/
  - reports/
  - skills/
  - newskills/

side_effects:
  - "writes 1d_histogram_figures_with_visible_statistical_uncertainties"
  - "writes overlay_figures_with_shared_binning_and_ratio_panels"
  - "writes ratio_panels_with_fixed_0_5_1_5_y_range_and_r_1_reference_line"
  - "writes plot_metadata_showing_binning_and_normalization_choice"

failure_modes:
  - "Missing or ambiguous required inputs block execution."
  - "Schema, fit, or consistency checks fail and produce diagnostics."

validation_checks:
  - "No fill-style histogram rendering unless explicitly requested."
  - "Overlays use identical bin edges."
  - "Default binning falls back to 20 if not otherwise set."
  - "X-axis range follows the statistical `mean ± 3 sigma` policy unless overridden."
  - "Every histogram includes visible error bars/uncertainty representation."
  - "Ratio panels are present for overlays and contain no NaN/Inf values."
  - "Division-by-zero bins are masked, not plotted as undefined values."
  - "Ratio uncertainty propagation uses the invariant formula above."
  - "Normalization and uncertainty scaling are internally consistent."

handoff_to:
  - SKILL_PLOTTING_AND_REPORT
  - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
---

# Purpose

This skill defines a structured execution contract for `physics_facts/histogram_plotting_invariants.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `physics_facts/histogram_plotting_invariants.md`
- Original stage: `plotting`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Histogram Plotting Invariants

## Layer 1 — Physics Policy
All 1D histogram plots must satisfy consistent statistical and visual invariants unless the user explicitly overrides them.

Policy requirements:
- Applies to all 1D histograms, overlays, and ratio-panel comparisons.
- Use line-only (step) style by default: no filled histogram areas.
- Distinguish overlays by line color/style/width, not fill.
- Use common bin edges across overlaid distributions.
- Default bin count is 20 when not explicitly specified.
- Compute x-axis range from distribution statistics using global `[min(mean_i - 3*sigma_i), max(mean_i + 3*sigma_i)]`.
- Display per-bin statistical uncertainties for every plotted histogram.
- Keep normalization mode consistent within a figure (counts, density, or area-normalized).
- If normalized, scale uncertainties consistently after normalization.
- For overlays, include a ratio panel with shared x-axis.
- Ratio convention is `A_i / B`, where `B` is nominal (first distribution if not provided).
- Ratio y-range is fixed to `[0.5, 1.5]` with a horizontal reference line at `1.0`.
- Propagate ratio uncertainty as:
  - `sigma_R = R * sqrt((sigma_A/A)^2 + (sigma_B/B)^2)` (independent-statistics assumption).
- Handle edge cases safely:
  - If `B == 0`, mask/omit ratio bin.
  - If `A == 0` and `B != 0`, ratio is `0` with safe uncertainty handling.
- Include nominal-reference behavior in ratio panel (reference line/band around 1.0 with nominal uncertainty context).
- Rules are backend-agnostic (ROOT/matplotlib/mplhep/etc.).

## Layer 2 — Workflow Contract
### Required Artifacts
- 1D histogram figures with visible statistical uncertainties.
- Overlay figures with shared binning and ratio panels.
- Ratio panels with fixed `[0.5, 1.5]` y-range and `R=1` reference line.
- Plot metadata (or reproducible code path) showing binning and normalization choice.

### Acceptance Checks
- No fill-style histogram rendering unless explicitly requested.
- Overlays use identical bin edges.
- Default binning falls back to 20 if not otherwise set.
- X-axis range follows the statistical `mean ± 3 sigma` policy unless overridden.
- Every histogram includes visible error bars/uncertainty representation.
- Ratio panels are present for overlays and contain no NaN/Inf values.
- Division-by-zero bins are masked, not plotted as undefined values.
- Ratio uncertainty propagation uses the invariant formula above.
- Normalization and uncertainty scaling are internally consistent.

## Layer 3 — Example Implementation
### Uncertainty Rules
- Unweighted: `sigma_bin = sqrt(N_bin)`
- Weighted: `sigma_bin = sqrt(sum(w^2)_bin)`

### Ratio Rules
- `R = A / B`
- `sigma_R = R * sqrt((sigma_A/A)^2 + (sigma_B/B)^2)`
- If `B == 0`, do not compute ratio for that bin.

### Override Policy
- Any exception to these invariants must be explicitly requested by user instruction or required by non-1D-plot context.

# Examples

Example invocation context:
- Run this contract in the declared stage using the required inputs and dependencies.

Example expected outputs:
- `1d_histogram_figures_with_visible_statistical_uncertainties`
- `overlay_figures_with_shared_binning_and_ratio_panels`
- `ratio_panels_with_fixed_0_5_1_5_y_range_and_r_1_reference_line`
- `plot_metadata_showing_binning_and_normalization_choice`
