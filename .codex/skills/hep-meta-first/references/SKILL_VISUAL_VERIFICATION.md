---
skill_id: SKILL_VISUAL_VERIFICATION
display_name: "Visualization-Based Verification"
version: 1.0
category: validation

summary: "Visual validation is mandatory for establishing that reconstructed objects, selections, categorization, and final signal extraction are physically reasonable, including the required H->gammagamma fit-plot families."

invocation_keywords:
  - "visual verification"
  - "visualization-based verification"
  - "validation"
  - "visualization"
  - "based"
  - "verification"

when_to_use:
  - "Use when executing or validating the validation stage of the analysis workflow."
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
  - name: object_level_diagnostic_plot_artifacts_for_leading_subleading_ph
    type: artifact
    description: "object-level diagnostic plot artifacts for leading/subleading photon kinematics and acceptance-sensitive observables"
  - name: event_level_diagnostic_plot_artifacts_for_diphoton_mass_preselec
    type: artifact
    description: "event-level diagnostic plot artifacts for diphoton mass preselection, diphoton transverse momentum, and angular separation"
  - name: selection_validation_artifacts_including_cut_flow_visualization_
    type: artifact
    description: "selection-validation artifacts including cut-flow visualization and photon multiplicity"
  - name: category_validation_plot_artifacts_for_each_active_category
    type: artifact
    description: "category-validation plot artifacts for each active category"
  - name: final_result_plot_artifacts_including_fitted_mass_spectrum_and_p
    type: artifact
    description: "final-result plot artifacts including fitted mass spectrum and pull/residual distribution"
  - name: blinded_sideband_fit_provenance_plot_artifacts_for_hgg
    type: artifact
    description: "mandatory H->gammagamma blinded sideband-fit provenance plots showing sideband data, the full-range sideband-fitted background-only PDF, and stacked expected signal"
  - name: expected_significance_asimov_fit_plot_artifacts_for_hgg
    type: artifact
    description: "mandatory H->gammagamma expected-significance Asimov fit plots showing Asimov pseudo-data, the fitted free-`mu` signal-plus-background total, and the corresponding background-only component"
  - name: observed_data_full_range_fit_plot_artifacts_for_hgg_when_unblind
    type: artifact
    description: "mandatory H->gammagamma observed-data full-range fit plots in explicit unblinded mode showing observed data, the fitted free-`mu` signal-plus-background total, and the fitted background-only component"
  - name: statistical_input_plot_artifacts_for_hgg
    type: artifact
    description: "mandatory H->gammagamma statistical-input plots covering per-category signal-shape fits, nominal diphoton template display, selected spurious-signal fit display, and smoothed-template fit display when smoothing is used"
  - name: pre_fit_and_post_fit_non_signal_region_comparison_plot_artifacts
    type: artifact
    description: "pre-fit and post-fit non-signal-region comparison plot artifacts"
  - name: verification_status_artifact_that_records_presence_absence_of_re
    type: artifact
    description: "verification-status artifact that records presence/absence of required diagnostics"
  - name: data_mc_discrepancy_artifacts
    type: artifact
    description: "data-MC discrepancy artifacts:"
  - name: outputs_report_data_mc_discrepancy_audit_json
    type: artifact
    description: "`outputs/report/data_mc_discrepancy_audit.json`"
  - name: outputs_report_data_mc_check_log_json
    type: artifact
    description: "`outputs/report/data_mc_check_log.json`"

preconditions:
  - "Dependency SKILL_PLOTTING_AND_REPORT has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_VISUAL_VERIFICATION are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_PLOTTING_AND_REPORT

  may_follow:
    - SKILL_PLOTTING_AND_REPORT
    - SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION
    - SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK

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
  - "writes object_level_diagnostic_plot_artifacts_for_leading_subleading_ph"
  - "writes event_level_diagnostic_plot_artifacts_for_diphoton_mass_preselec"
  - "writes selection_validation_artifacts_including_cut_flow_visualization_"
  - "writes category_validation_plot_artifacts_for_each_active_category"
  - "writes final_result_plot_artifacts_including_fitted_mass_spectrum_and_p"
  - "writes blinded_sideband_fit_provenance_plot_artifacts_for_hgg"
  - "writes expected_significance_asimov_fit_plot_artifacts_for_hgg"
  - "writes observed_data_full_range_fit_plot_artifacts_for_hgg_when_unblind"
  - "writes pre_fit_and_post_fit_non_signal_region_comparison_plot_artifacts"
  - "writes verification_status_artifact_that_records_presence_absence_of_re"
  - "writes data_mc_discrepancy_artifacts"
  - "writes outputs_report_data_mc_discrepancy_audit_json"
  - "writes outputs_report_data_mc_check_log_json"

failure_modes:
  - "verification stage fails if any required diagnostic artifact is missing"
  - "reporting-stage integration should fail if required verification plots are embedded without explanatory captions"

validation_checks:
  - "all required object-level diagnostics exist"
  - "all required event-level diagnostics exist"
  - "cut-flow visualization and multiplicity diagnostics exist"
  - "category diagnostics exist for every active category"
  - "final fit and pull diagnostics exist"
  - "for H->gammagamma, blinded sideband-fit provenance plots exist for every active category"
  - "for H->gammagamma, expected-significance Asimov fit plots exist for every active category and the combined fit"
  - "for H->gammagamma, observed-data full-range fit plots exist only after explicit unblinding and are otherwise explicitly absent or blocked"
  - "for H->gammagamma, one signal `m_gg` plot per category exists with the signal MC distribution overlaid by the fitted signal PDF"
  - "for H->gammagamma, a plot of the nominal unsmoothed sideband-normalized diphoton template used for the spurious-signal study exists"
  - "for H->gammagamma, a plot of the selected background-function-plus-signal fit used in the spurious-signal procedure exists"
  - "for H->gammagamma, if smoothing was triggered, a plot of the selected-function fit to the smoothed template used for actual function selection exists"
  - "pre-fit and post-fit non-signal-region diagnostics exist"
  - "blinding behavior matches policy: data shown in non-signal regions, hidden in signal regions unless explicitly unblinded"
  - "verification stage fails if any required diagnostic artifact is missing"
  - "reporting-stage integration should fail if required verification plots are embedded without explanatory captions"
  - "substantial discrepancies must be logged to discrepancy-audit artifacts or explicitly stated as absent"
  - "discrepancy artifacts must exist even when no substantial discrepancy is found"

handoff_to:
  - SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK
  - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
  - SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION
  - SKILL_FULL_STATISTICS_EXECUTION_POLICY
---

# Purpose

This skill defines a structured execution contract for `infrastructure/visual_verification.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `infrastructure/visual_verification.md`
- Original stage: `validation`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Visualization-Based Verification

## Layer 1 — Physics Policy
Visual validation is mandatory for establishing that reconstructed objects, selections, categorization, and final signal extraction are physically reasonable.

Policy requirements:
- validate object-level behavior before interpreting final fits
- validate event-level observables used in selection and fitting
- validate selection behavior via cut flow and multiplicity diagnostics
- validate category behavior when categories are used
- validate final fit quality and residual structure
- validate control/non-signal region agreement in both pre-fit and post-fit views
- for `H -> gamma gamma`, validate the blinded sideband-fit provenance plots that show observed sideband data, the full-range sideband-fitted background-only PDF, and stacked expected signal
- for `H -> gamma gamma`, validate the expected-significance Asimov fit plots that show pseudo-data, the fitted free-`mu` signal-plus-background total, and the corresponding background-only component over the full mass range
- for `H -> gamma gamma`, validate the observed-data full-range free-`mu` fit plots only after explicit unblinding; these plots must show observed data, the fitted signal-plus-background total, and the fitted background-only component
- for `H -> gamma gamma`, the statistical-input plots are mandatory:
  - for each category, show the signal `m_gg` distribution from signal MC with the fitted signal PDF overlaid
  - show the nominal background template used for the spurious-signal study; this is the default diphoton MC sample normalized to data in sidebands
  - show the selected background-function-plus-signal fit used in the spurious-signal procedure
  - if smoothing was triggered because effective MC luminosity was below threshold, also show the selected-function fit to the smoothed template used for the actual function-selection step
- for `H -> gamma gamma`, the unsmoothed sideband-normalized diphoton template remains the nominal template to display even when a smoothed template is used operationally for function selection
- explicitly flag substantial data-MC discrepancies and trigger discrepancy checks instead of cosmetic retuning
- in blinded mode, verify that non-signal plots show data while signal-region plots hide data
- apply clear plotting conventions: physical axis labels, uncertainty display where available, consistent binning, appropriate scaling, no misleading smoothing
- when verification plots are embedded in reports, each plot should include a caption explaining plotted entries and why this diagnostic is required

## Layer 2 — Workflow Contract
### Required Artifacts
- object-level diagnostic plot artifacts for leading/subleading photon kinematics and acceptance-sensitive observables
- event-level diagnostic plot artifacts for diphoton mass preselection, diphoton transverse momentum, and angular separation
- selection-validation artifacts including cut-flow visualization and photon multiplicity
- category-validation plot artifacts for each active category
- final-result plot artifacts including fitted mass spectrum and pull/residual distribution
- mandatory `H -> gamma gamma` blinded sideband-fit provenance plot artifacts:
  - one plot per active category with sideband data, full-range sideband-fitted background-only PDF, and stacked expected signal
- mandatory `H -> gamma gamma` expected-significance Asimov fit plot artifacts:
  - one plot per active category plus one combined plot with Asimov pseudo-data, fitted free-`mu` signal-plus-background total, and the corresponding background-only component
- mandatory `H -> gamma gamma` observed-data full-range fit plot artifacts in explicit unblinded mode:
  - one plot per active category plus one combined plot with observed full-range data, fitted free-`mu` signal-plus-background total, and fitted background-only component
- mandatory `H -> gamma gamma` statistical-input plot artifacts:
  - one signal `m_gg` plot per category with signal MC and the fitted signal PDF overlaid
  - one plot of the nominal unsmoothed sideband-normalized diphoton template used for the spurious-signal study
  - one plot of the selected background-function-plus-signal fit used in the spurious-signal procedure
  - when smoothing is applied, one additional plot of the selected-function fit to the smoothed template used for actual function selection
- pre-fit and post-fit non-signal-region comparison plot artifacts
- verification-status artifact that records presence/absence of required diagnostics
- data-MC discrepancy artifacts:
  - `outputs/report/data_mc_discrepancy_audit.json`
  - `outputs/report/data_mc_check_log.json`

### Acceptance Checks
- all required object-level diagnostics exist
- all required event-level diagnostics exist
- cut-flow visualization and multiplicity diagnostics exist
- category diagnostics exist for every active category
- final fit and pull diagnostics exist
- for `H -> gamma gamma`, blinded sideband-fit provenance plots exist for every active category
- for `H -> gamma gamma`, expected-significance Asimov fit plots exist for every active category and the combined fit
- for `H -> gamma gamma`, observed-data full-range fit plots exist only after explicit unblinding and are otherwise explicitly absent/blocked
- for `H -> gamma gamma`, one signal `m_gg` + fitted-signal-PDF plot exists for every active category
- for `H -> gamma gamma`, the nominal unsmoothed sideband-normalized diphoton template plot exists
- for `H -> gamma gamma`, the selected background-function-plus-signal fit plot used in the spurious-signal procedure exists
- for `H -> gamma gamma`, if smoothing was triggered, the selected-function fit to the smoothed template exists
- pre-fit and post-fit non-signal-region diagnostics exist
- blinding behavior matches policy: data shown in non-signal regions, hidden in signal regions unless explicitly unblinded
- verification stage fails if any required diagnostic artifact is missing
- reporting-stage integration should fail if required verification plots are embedded without explanatory captions
- substantial discrepancies must be logged to discrepancy-audit artifacts or explicitly stated as absent
- discrepancy artifacts must exist even when no substantial discrepancy is found

## Layer 3 — Example Implementation
### Required Plot Names (Current Repository)
- `photon_pt_leading.png`
- `photon_pt_subleading.png`
- `photon_eta_leading.png`
- `photon_eta_subleading.png`
- `diphoton_mass_preselection.png`
- `diphoton_pt.png`
- `diphoton_deltaR.png`
- `photon_multiplicity.png`
- `cutflow_plot.png`
- `cutflow_table.json`
- `diphoton_mass_category_*.png`
- `diphoton_mass_fit.png`
- `diphoton_mass_pull.png`

### Output Location (Current Repository)
- `outputs/report/plots/`

### Blinding Coordination
If blinded operation is active, also apply:
- `analysis_strategy/control_region_signal_region_blinding_and_visualization.md`
- `governance/data_mc_discrepancy_sanity_check.md`

# Examples

Example invocation context:
- Run this contract in the declared stage using the required inputs and dependencies.

Example expected outputs:
- `outputs/report/data_mc_discrepancy_audit.json`
- `outputs/report/data_mc_check_log.json`
- `outputs/report/plots/`
