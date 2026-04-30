---
skill_id: SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION
display_name: "Control/Signal Region Blinding and Visualization"
version: 1.0
category: validation

summary: "For H->gammagamma, blinded operation must prevent inspection of observed `120-130 GeV` data while still allowing full-range Asimov pseudo-data generation from sideband-fitted PDFs and requiring sideband-fit plots that show sideband data, the full-range background PDF, and stacked expected signal."

invocation_keywords:
  - "control region signal region blinding and visualization"
  - "control/signal region blinding and visualization"
  - "design"
  - "control"
  - "signal"
  - "region"
  - "blinding"
  - "visualization"

when_to_use:
  - "Use when executing or validating the design stage of the analysis workflow."
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
  - name: control_region_only_normalization_fit_artifact_containing_fitted
    type: artifact
    description: "control-region-only normalization-fit artifact containing fitted normalization parameters and fit status"
  - name: blinding_summary_artifact_indicating_region_classification_and_w
    type: artifact
    description: "blinding-summary artifact indicating region classification and whether data were shown, hidden, or masked"
  - name: region_visualization_artifact_set_covering_all_declared_control_
    type: artifact
    description: "region-visualization artifact set covering all declared control and signal regions"
  - name: pre_fit_control_region_visualization_artifact_set_with_data_back
    type: artifact
    description: "pre-fit control-region visualization artifact set with data, background, and signal overlays"
  - name: post_fit_control_region_visualization_artifact_set_with_data_bac
    type: artifact
    description: "post-fit control-region visualization artifact set with data, background, and signal overlays"
  - name: pre_fit_and_post_fit_signal_region_visualization_artifacts_in_un
    type: artifact
    description: "pre-fit and post-fit signal-region visualization artifacts in unblinded mode"
  - name: blinding_overlap_audit_artifact_confirming_sr_events_are_exclude
    type: artifact
    description: "blinding overlap-audit artifact confirming SR events are excluded from CR normalization scope by default"
  - name: sideband_only_background_fit_artifact_for_blinded_resonance_cate
    type: artifact
    description: "sideband-only background-fit artifact for blinded resonance categories (fit-range declaration + per-category parameters)"
  - name: sideband_background_fit_visualization_artifact_set_for_blinded_h
    type: artifact
    description: "mandatory H->gammagamma sideband-fit visualization set showing observed sideband data, the sideband-fitted background-only PDF extrapolated over `105-160 GeV`, and stacked expected signal across the blinded window"
  - name: blinded_category_mass_plot_artifact_set_with
    type: artifact
    description: "blinded category mass-plot artifact set with:"
  - name: observed_data_points_in_sidebands_only
    type: artifact
    description: "observed data points in sidebands only"
  - name: full_range_post_fit_background_curve
    type: artifact
    description: "full-range post-fit background curve"
  - name: stacked_signal_on_background_expectation
    type: artifact
    description: "stacked signal-on-background expectation"
  - name: outputs_fit_fit_id_blinded_cr_fit_json
    type: artifact
    description: "`outputs/fit/<fit_id>/blinded_cr_fit.json`"
  - name: outputs_report_blinding_summary_json
    type: artifact
    description: "`outputs/report/blinding_summary.json`"

preconditions:
  - "Dependency SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS has completed successfully."
  - "Dependency SKILL_SELECTION_ENGINE_AND_REGIONS has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
    - SKILL_SELECTION_ENGINE_AND_REGIONS

  may_follow:
    - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
    - SKILL_SELECTION_ENGINE_AND_REGIONS
    - SKILL_PLOTTING_AND_REPORT
    - SKILL_VISUAL_VERIFICATION

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
  - "writes control_region_only_normalization_fit_artifact_containing_fitted"
  - "writes blinding_summary_artifact_indicating_region_classification_and_w"
  - "writes region_visualization_artifact_set_covering_all_declared_control_"
  - "writes pre_fit_control_region_visualization_artifact_set_with_data_back"
  - "writes post_fit_control_region_visualization_artifact_set_with_data_bac"
  - "writes pre_fit_and_post_fit_signal_region_visualization_artifacts_in_un"
  - "writes blinding_overlap_audit_artifact_confirming_sr_events_are_exclude"
  - "writes sideband_only_background_fit_artifact_for_blinded_resonance_cate"
  - "writes sideband_background_fit_visualization_artifact_set_for_blinded_h"
  - "writes blinded_category_mass_plot_artifact_set_with"
  - "writes observed_data_points_in_sidebands_only"

failure_modes:
  - "Missing or ambiguous required inputs block execution."
  - "Schema, fit, or consistency checks fail and produce diagnostics."

validation_checks:
  - "normalization-fit artifact confirms control-region-only fit scope"
  - "blinding-summary artifact marks signal-region handling mode as one of: omitted, masked, or unblinded"
  - "number of produced region plots equals number of declared regions for the selected handling mode"
  - "for each declared control region, both pre-fit and post-fit plots exist"
  - "in unblinded mode, for each declared signal region, both pre-fit and post-fit plots exist and show observed data over full SR"
  - "in blinded H->gammagamma mode, the agent does not inspect observed data in `120-130 GeV` and resonance plots with observed data show only sidebands `105-120 GeV` and `130-160 GeV`"
  - "in blinded mode, signal-region observed data are hidden by omission or masking with explicit boundary declaration when masking is used"
  - "control-region plots show observed data points in both pre-fit and post-fit views"
  - "stacked composition places signal above background in expectation plots"
  - "overlap audit confirms zero SR/CR overlap for blinded normalization unless an explicit exception is declared"
  - "blinded resonance mass plots hide data points in the blinded peak window while preserving sideband data points"
  - "sideband-fit artifacts explicitly record sideband ranges used for fit constraints"
  - "for H->gammagamma, sideband-fit artifacts record `105-120 GeV` and `130-160 GeV` as the observed-data fit ranges and record that the fitted background PDF is used over the full `105-160 GeV` range"
  - "for H->gammagamma, each blinded resonance category has a sideband-fit visualization showing observed data only in `105-120 GeV` and `130-160 GeV`, the sideband-fitted background-only PDF over the full `105-160 GeV` range, and stacked expected signal across `120-130 GeV`"
  - "blinded mode does not block full-range Asimov pseudo-data generation; Asimov products are explicitly marked as pseudo-data and may include `120-130 GeV`"
  - "stacked expected signal contribution appears above expected background in blinded resonance plots"

handoff_to:
  - SKILL_PLOTTING_AND_REPORT
  - SKILL_VISUAL_VERIFICATION
  - SKILL_SELECTION_ENGINE_AND_REGIONS
  - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
---

# Purpose

This skill defines a structured execution contract for `analysis_strategy/control_region_signal_region_blinding_and_visualization.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `analysis_strategy/control_region_signal_region_blinding_and_visualization.md`
- Original stage: `design`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Control/Signal Region Blinding and Visualization

## Layer 1 — Physics Policy
Blinding protects against analysis bias by preventing inspection of signal-region data during model development and validation.

Policy requirements:
- blinded operation is the default mode for all analyses unless an explicit user unblinding directive is provided
- for `H -> gamma gamma`, blinded mode means the agent must not inspect observed data in the `120-130 GeV` window unless the user explicitly instructs unblinding
- control-region visualizations may show observed data and modeled expectations
- in blinded mode, all non-signal regions (CR/VR/SB) should show observed data overlaid with signal and background expectations
- signal expectation must be stacked on top of background expectation in region plots
- normalization used for expected region plots should be derived from control-region-only fitting when blinding is active
- produce both pre-fit and post-fit views for control regions:
  - pre-fit: nominal Monte Carlo normalization before fitting
  - post-fit: expectations normalized with fitted CR-constrained parameters
- produce both pre-fit and post-fit views for signal regions in unblinded mode
- in blinded mode, signal-region observed-data handling must use one of:
  - full SR omission (no observed-data SR plot in report), or
  - sensitive-window masking (hide data in sensitive signal window but allow sideband data when physically appropriate)
- control and signal region selections must be mutually exclusive for blinded workflows unless an explicit overlap exception is documented
- unblinding is an explicit, deliberate action outside the default workflow
- when unblinded, observed data must be shown across the full signal region
- for diphoton resonance category fits, background normalization/shape must be fitted to observed data using sidebands only: `105-120 GeV` and `130-160 GeV`
- for `H -> gamma gamma`, the blinded observed-data exclusion window is exactly `120-130 GeV`
- blinded category mass plots may show full-range expected background and expected signal+background curves, but observed data points must be shown only in sidebands unless explicit unblinding is requested
- expected signal overlay should be stacked on top of the post-fit background expectation in blinded category plots
- for `H -> gamma gamma`, a mandatory sideband-fit provenance plot must show the actual observed sideband data points, the background-only PDF fitted in `105-120 GeV` and `130-160 GeV` and extrapolated through `120-130 GeV`, and the expected signal stacked on top of that background expectation over the full `105-160 GeV` range
- Asimov pseudo-data products are exempt from observed-data blinding restrictions because they are generated from model PDFs, not real detector data
- when Asimov pseudo-data are shown, outputs must be explicitly labeled as Asimov/expected and must not be presented as observed data
- for blinded sensitivity evaluation, Asimov pseudo-data can and should be generated/evaluated over the full `105-160 GeV` mass range, including `120-130 GeV`, while observed-data fits remain sideband-constrained
- state explicitly in blinding artifacts that once the background PDF is fitted in sidebands it is defined over the full `105-160 GeV` range, so blinded mode does not forbid full-range Asimov generation

## Layer 2 — Workflow Contract
### Required Artifacts
- control-region-only normalization-fit artifact containing fitted normalization parameters and fit status
- blinding-summary artifact indicating region classification and whether data were shown, hidden, or masked
- blinding-summary artifact fields for `H -> gamma gamma` containing:
  - `blind_window = [120.0, 130.0]`
  - `sidebands = [[105.0, 120.0], [130.0, 160.0]]`
  - `observed_data_inspection_allowed_in_blind_window` (`false` unless explicitly unblinded)
  - `full_range_asimov_allowed = true`
  - `background_pdf_defined_over_full_range = true` once the sideband fit is complete
- region-visualization artifact set covering all declared control and signal regions
- pre-fit control-region visualization artifact set with data, background, and signal overlays
- post-fit control-region visualization artifact set with data, background, and signal overlays
- pre-fit and post-fit signal-region visualization artifacts in unblinded mode
- blinding overlap-audit artifact confirming SR events are excluded from CR normalization scope by default
- sideband-only background-fit artifact for blinded resonance categories (fit-range declaration + per-category parameters)
- mandatory `H -> gamma gamma` sideband-background-fit visualization artifact set with:
  - observed data points shown only in `105-120 GeV` and `130-160 GeV`
  - sideband-fitted background-only PDF evaluated over the full `105-160 GeV` range
  - stacked expected signal overlay shown across the blinded window for shape/provenance context
- blinded category mass-plot artifact set with:
  - observed data points in sidebands only
  - full-range post-fit background curve
  - stacked signal-on-background expectation

### Acceptance Checks
- normalization-fit artifact confirms control-region-only fit scope
- blinding-summary artifact marks signal-region handling mode as one of: omitted, masked, or unblinded
- for `H -> gamma gamma`, blinding-summary artifact records `120-130 GeV` as the observed-data blind window and `105-120 GeV`, `130-160 GeV` as the sidebands
- number of produced region plots equals number of declared regions for the selected handling mode
- for each declared control region, both pre-fit and post-fit plots exist
- in unblinded mode, for each declared signal region, both pre-fit and post-fit plots exist and show observed data over full SR
- in blinded `H -> gamma gamma` mode, observed data in `120-130 GeV` are not inspected and are not shown in resonance plots unless explicit unblinding is requested
- in blinded mode, signal-region observed data are hidden by omission or masking with explicit boundary declaration when masking is used
- control-region plots show observed data points in both pre-fit and post-fit views
- stacked composition places signal above background in expectation plots
- overlap audit confirms zero SR/CR overlap for blinded normalization unless an explicit exception is declared
- blinded resonance mass plots hide data points in the blinded peak window while preserving sideband data points
- sideband-fit artifacts explicitly record `105-120 GeV` and `130-160 GeV` as the observed-data fit ranges
- sideband-fit artifacts explicitly state that the fitted background PDF is defined over the full `105-160 GeV` range after the sideband fit
- mandatory `H -> gamma gamma` sideband-fit provenance plots exist for each active blinded resonance category and show sideband data, the full-range fitted background-only PDF, and stacked expected signal
- blinding artifacts explicitly state that full-range Asimov pseudo-data generation over `105-160 GeV` including `120-130 GeV` is allowed and required for expected-significance workflows
- stacked expected signal contribution appears above expected background in blinded resonance plots

## Layer 3 — Example Implementation
### CLI (Current Repository)
Blinded (default):
`python -m analysis.plotting.blinded_regions --outputs outputs --registry outputs/samples.registry.json --regions analysis/regions.yaml --fit-id FIT1`

Explicit unblind:
`python -m analysis.plotting.blinded_regions --outputs outputs --registry outputs/samples.registry.json --regions analysis/regions.yaml --fit-id FIT1 --unblind-sr`

### Expected Outputs (Current Repository)
- `outputs/fit/<fit_id>/blinded_cr_fit.json`
- `outputs/report/blinding_summary.json`
- `outputs/report/plots/blinded_region_<region_id>.png`
- `outputs/report/plots/prefit_region_<region_id>.png` (control regions)
- `outputs/report/plots/postfit_region_<region_id>.png` (control regions)
- `outputs/report/plots/prefit_signal_region_<region_id>.png` (unblinded mode)
- `outputs/report/plots/postfit_signal_region_<region_id>.png` (unblinded mode)
- `outputs/fit/<fit_id>/roofit_combined/sideband_fit_parameters.json` (required for H->gammagamma category-resolved workflows)
- `outputs/report/plots/roofit_combined_mgg_<category>.png` (required for H->gammagamma category-resolved workflows)

### Downstream Reference
Use with:
- `core_pipeline/plotting_and_report.md`
- `infrastructure/visual_verification.md`

# Examples

Example invocation context:
- `python -m analysis.plotting.blinded_regions --outputs outputs --registry outputs/samples.registry.json --regions analysis/regions.yaml --fit-id FIT1`
- `python -m analysis.plotting.blinded_regions --outputs outputs --registry outputs/samples.registry.json --regions analysis/regions.yaml --fit-id FIT1 --unblind-sr`

Example expected outputs:
- `outputs/samples.registry.json`
- `outputs/fit/<fit_id>/blinded_cr_fit.json`
- `outputs/report/blinding_summary.json`
- `outputs/report/plots/blinded_region_<region_id>.png`
- `outputs/report/plots/prefit_region_<region_id>.png`
- `outputs/report/plots/postfit_region_<region_id>.png`
- `outputs/report/plots/prefit_signal_region_<region_id>.png`
- `outputs/report/plots/postfit_signal_region_<region_id>.png`
