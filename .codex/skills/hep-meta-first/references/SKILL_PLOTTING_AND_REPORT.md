---
skill_id: SKILL_PLOTTING_AND_REPORT
display_name: "Plotting and Report"
version: 1.0
category: plotting

summary: "Result communication must make agreement and discrepancies between data and expectations auditable, including mandatory H->gammagamma fit-visualization families for blinded sideband fits, Asimov expected-significance fits, and explicitly unblinded observed-data fits."

invocation_keywords:
  - "plotting and report"
  - "plotting"
  - "report"

when_to_use:
  - "Use when executing or validating the plotting stage of the analysis workflow."
  - "Use when this context is available: `outputs/background_modeling_strategy.json`."
  - "Use when this context is available: `outputs/fit/*/signal_pdf.json`."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: outputs_background_modeling_strategy_json
      type: artifact
      description: "`outputs/background_modeling_strategy.json`"
    - name: outputs_fit_signal_pdf_json
      type: artifact
      description: "`outputs/fit/*/signal_pdf.json`"
    - name: outputs_fit_background_pdf_choice_json
      type: artifact
      description: "`outputs/fit/*/background_pdf_choice.json`"
    - name: outputs_fit_spurious_signal_json
      type: artifact
      description: "`outputs/fit/*/spurious_signal.json`"
    - name: outputs_report_blinding_summary_json
      type: artifact
      description: "`outputs/report/blinding_summary.json`"
    - name: outputs_fit_blinded_cr_fit_json
      type: artifact
      description: "`outputs/fit/*/blinded_cr_fit.json`"
    - name: outputs_fit_results_json
      type: artifact
      description: "`outputs/fit/*/results.json`"
    - name: outputs_fit_significance_json
      type: artifact
      description: "`outputs/fit/*/significance.json`"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: region_plot_artifact_set_for_fit_observables
    type: artifact
    description: "region-plot artifact set for fit observables"
  - name: pre_fit_region_plot_artifact_set_for_control_regions
    type: artifact
    description: "pre-fit region-plot artifact set for control regions"
  - name: post_fit_region_plot_artifact_set_for_control_regions
    type: artifact
    description: "post-fit region-plot artifact set for control regions"
  - name: pre_fit_and_post_fit_signal_region_plot_artifact_sets_for_unblin
    type: artifact
    description: "pre-fit and post-fit signal-region plot artifact sets for unblinded mode"
  - name: blinded_signal_region_handling_artifact_documenting_whether_sr_p
    type: artifact
    description: "blinded signal-region handling artifact documenting whether SR plots are omitted or sensitive windows are masked"
  - name: cut_flow_visualization_artifact
    type: artifact
    description: "cut-flow visualization artifact"
  - name: narrative_report_artifact_integrating_methodology_yields_fit_out
    type: artifact
    description: "narrative report artifact integrating methodology, yields, fit outcomes, significance, and key diagnostics"
  - name: report_markdown_with_embedded_plot_images
    type: artifact
    description: "report markdown with embedded plot images (not path-only citation lists)"
  - name: artifact_link_inventory_enabling_traceability_from_report_statem
    type: artifact
    description: "artifact-link inventory enabling traceability from report statements to produced artifacts"
  - name: category_resolved_mass_plot_artifact_set_with_stacked_signal_ove
    type: artifact
    description: "category-resolved mass-plot artifact set with stacked signal overlays and explicit blinding behavior"
  - name: sideband_background_fit_visualization_artifact_set_for_hgg
    type: artifact
    description: "mandatory H->gammagamma sideband-fit plot set showing observed sideband data, the sideband-fitted background-only PDF over `105-160 GeV`, and stacked expected signal"
  - name: asimov_expected_significance_fit_visualization_artifact_set_for_h
    type: artifact
    description: "mandatory H->gammagamma Asimov expected-significance fit plot set showing Asimov pseudo-data, the fitted free-`mu` signal-plus-background total, and the corresponding background-only component over the full mass range"
  - name: observed_unblinded_full_range_fit_visualization_artifact_set_for
    type: artifact
    description: "mandatory H->gammagamma observed-data fit plot set in explicit unblinded mode showing full-range observed data, the fitted free-`mu` signal-plus-background total, and the fitted background-only component with shared `mu` across categories"
  - name: statistical_input_plot_artifact_set_for_hgg
    type: artifact
    description: "mandatory H->gammagamma statistical-input plot set containing per-category signal-shape fits, nominal diphoton-template display, selected spurious-signal-fit display, and an unsmoothed-vs-smoothed template overlay when smoothing is applied"
  - name: plot_caption_artifact_content_in_the_report_markdown
    type: artifact
    description: "plot-caption artifact content in the report markdown (caption text adjacent to each embedded image)"
  - name: discrepancy_artifacts_for_data_mc_checks
    type: artifact
    description: "discrepancy artifacts for data-MC checks:"
  - name: outputs_report_data_mc_discrepancy_audit_json
    type: artifact
    description: "`outputs/report/data_mc_discrepancy_audit.json`"
  - name: outputs_report_data_mc_check_log_json
    type: artifact
    description: "`outputs/report/data_mc_check_log.json`"

preconditions:
  - "Dependency SKILL_HISTOGRAMMING_AND_TEMPLATES has completed successfully."
  - "Dependency SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE has completed successfully."
  - "Dependency SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION has completed successfully."
  - "Dependency SKILL_HISTOGRAM_PLOTTING_INVARIANTS has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_PLOTTING_AND_REPORT are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_HISTOGRAMMING_AND_TEMPLATES
    - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
    - SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION
    - SKILL_HISTOGRAM_PLOTTING_INVARIANTS

  may_follow:
    - SKILL_HISTOGRAMMING_AND_TEMPLATES
    - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
    - SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION
    - SKILL_HISTOGRAM_PLOTTING_INVARIANTS
    - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
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
  - "writes region_plot_artifact_set_for_fit_observables"
  - "writes pre_fit_region_plot_artifact_set_for_control_regions"
  - "writes post_fit_region_plot_artifact_set_for_control_regions"
  - "writes pre_fit_and_post_fit_signal_region_plot_artifact_sets_for_unblin"
  - "writes blinded_signal_region_handling_artifact_documenting_whether_sr_p"
  - "writes cut_flow_visualization_artifact"
  - "writes narrative_report_artifact_integrating_methodology_yields_fit_out"
  - "writes report_markdown_with_embedded_plot_images"
  - "writes artifact_link_inventory_enabling_traceability_from_report_statem"
  - "writes category_resolved_mass_plot_artifact_set_with_stacked_signal_ove"
  - "writes sideband_background_fit_visualization_artifact_set_for_hgg"
  - "writes asimov_expected_significance_fit_visualization_artifact_set_for_h"
  - "writes observed_unblinded_full_range_fit_visualization_artifact_set_for"

failure_modes:
  - "Missing or ambiguous required inputs block execution."
  - "Schema, fit, or consistency checks fail and produce diagnostics."

validation_checks:
  - "at least one observable plot exists for each fit region"
  - "pre-fit and post-fit control-region plots both exist and are embedded in reporting artifacts"
  - "in unblinded mode, pre-fit and post-fit signal-region plots exist and include observed data across full SR"
  - "in blinded mode, signal-region observed data are either omitted or explicitly masked in sensitive windows with documented boundaries"
  - "control-region pre-fit/post-fit plots display data points and stacked signal/background expectations"
  - "for H->gammagamma, blinded sideband-fit plots exist and show observed sideband data, the full-range sideband-fitted background-only PDF, and stacked expected signal"
  - "for H->gammagamma, expected-significance Asimov fit plots exist for each active category and the combined fit and show Asimov pseudo-data, the fitted free-`mu` signal-plus-background total, and the corresponding background-only component over `105-160 GeV`"
  - "for H->gammagamma, observed-data full-range free-`mu` fit plots exist only after explicit unblinding and then show observed data, the fitted signal-plus-background total, and the fitted background-only component for each active category and the combined fit"
  - "for H->gammagamma, required statistical-input plots exist and are treated as mandatory artifacts rather than optional diagnostics"
  - "for H->gammagamma reporting, cut flow is presented separately for signal production modes, diphoton background MC, and data"
  - "for H->gammagamma reporting, MC statistical uncertainties are derived from event weights rather than naive counts"
  - "report includes event-selection summary, cut flow summary, and fit result summary"
  - "report includes significance summary when significance artifacts exist"
  - "report includes blinding summary when blinding artifacts exist"
  - "report uses inline markdown image tags (for example `![](plots/<name>.png)`) for produced plots"
  - "when category-resolved resonance plots are produced, there is one plot per active category and blinded windows hide data points unless unblinded"
  - "every embedded image in report markdown is immediately accompanied by a caption that explains entries and motivation"
  - "substantial data-MC discrepancies are explicitly called out and not hidden by cosmetic-only changes"
  - "discrepancy artifacts exist even when no substantial discrepancy is found"

handoff_to:
  - SKILL_VISUAL_VERIFICATION
  - SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK
  - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/plotting_and_report.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `core_pipeline/plotting_and_report.md`
- Original stage: `plotting`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Plotting and Report

## Layer 1 — Physics Policy
Result communication must make agreement and discrepancies between data and expectations auditable.

Policy requirements:
- provide region-level observable visualizations with consistent binning and axis semantics
- when blinded mode is active, show observed data in non-signal regions and hide observed data in sensitive signal-region content
- provide both pre-fit and post-fit region visualizations for control regions
- provide both pre-fit and post-fit region visualizations for signal regions in unblinded mode
- in blinded mode, signal-region visualizations must either:
  - omit observed-data signal-region plots, or
  - mask the sensitive signal window (for example a resonance window such as `125 +/- 5 GeV`) while keeping allowed sidebands visible when appropriate
- pre-fit must represent nominal Monte Carlo normalization before fitting
- post-fit must use fitted normalization/nuisance values derived from fit constraints
- include cut flow summaries and fit summaries in the final narrative
- for `H -> gamma gamma`, cut flow in reporting is mandatory and must be shown separately for signal production modes, diphoton background MC, and data
- for `H -> gamma gamma`, MC statistical uncertainties in reported cut flow/yield tables must be computed from event weights rather than naive event counts
- include signal/background modeling rationale and uncertainty context
- include blinding policy behavior when the analysis is blinded
- for category-resolved resonance fits, provide one mass distribution per active category with data points (sidebands-only when blinded), post-fit background, and stacked signal-on-background expectation
- for `H -> gamma gamma`, provide a mandatory blinded sideband-fit provenance plot for each active category showing the actual sideband data, the background-only PDF fitted in `105-120 GeV` and `130-160 GeV` and evaluated over the full `105-160 GeV` range, and the expected signal stacked on top of the background expectation
- for `H -> gamma gamma`, provide a mandatory expected-significance fit plot set showing the signal-plus-background Asimov pseudo-data, the fitted free-`mu` signal-plus-background total, and the corresponding background-only component; these plots must cover the full `105-160 GeV` range and may include the blinded window because the inputs are pseudo-data
- for `H -> gamma gamma`, reserve the observed-data full-range free-`mu` fit plot set for explicit unblinding only; once unblinded, show full-range observed data together with the fitted signal-plus-background total and fitted background-only component, and declare that `mu` is shared across categories
- for `H -> gamma gamma`, the statistical-input plots are mandatory:
  - one signal `m_gg` plot per category with the fitted signal PDF overlaid on signal MC
  - one plot showing the nominal unsmoothed sideband-normalized diphoton template used for the spurious-signal study
  - one plot showing the selected background-function-plus-signal fit used in the spurious-signal procedure
  - when smoothing is applied, one additional plot overlaying the unsmoothed and smoothed sideband-normalized diphoton templates on the same axes so the effect of smoothing is directly visible
  - the unsmoothed-vs-smoothed overlay is the primary smoothing-effect diagnostic; separate template-vs-fit panels may be kept as supplemental diagnostics but must not replace the overlay
- for `H -> gamma gamma`, resonance plots with observed data must show only sidebands in blinded mode unless explicit unblinding is requested
- every embedded plot in narrative outputs must include a caption that:
  - explains plotted entries (for example data points, background expectation, signal expectation, fit components)
  - states why the plot is produced (motivation/justification in analysis workflow)

## Layer 2 — Workflow Contract
### Required Artifacts
- region-plot artifact set for fit observables
- pre-fit region-plot artifact set for control regions
- post-fit region-plot artifact set for control regions
- pre-fit and post-fit signal-region plot artifact sets for unblinded mode
- blinded signal-region handling artifact documenting whether SR plots are omitted or sensitive windows are masked
- cut-flow visualization artifact
- narrative report artifact integrating methodology, yields, fit outcomes, significance, and key diagnostics
- report markdown with embedded plot images (not path-only citation lists)
- artifact-link inventory enabling traceability from report statements to produced artifacts
- category-resolved mass-plot artifact set with stacked signal overlays and explicit blinding behavior
- mandatory `H -> gamma gamma` sideband-background-fit visualization artifact set with:
  - observed sideband data points
  - sideband-fitted background-only PDF evaluated over the full `105-160 GeV` range
  - stacked expected signal shown for context in the blinded window
- mandatory `H -> gamma gamma` expected-significance Asimov fit visualization artifact set with:
  - signal-plus-background Asimov pseudo-data
  - fitted free-`mu` signal-plus-background total
  - corresponding background-only component
  - one plot per active category plus one combined plot
- mandatory `H -> gamma gamma` observed-data full-range fit visualization artifact set in explicit unblinded mode with:
  - observed data over the full `105-160 GeV` range
  - fitted free-`mu` signal-plus-background total
  - fitted background-only component
  - one plot per active category plus one combined plot
- mandatory `H -> gamma gamma` statistical-input plot artifact set with:
  - per-category signal `m_gg` distributions from signal MC overlaid with fitted signal PDFs
  - the nominal unsmoothed sideband-normalized diphoton template used for the spurious-signal study
  - the selected background-function-plus-signal fit used in the spurious-signal procedure
  - the unsmoothed-vs-smoothed sideband-normalized diphoton-template overlay when smoothing is applied
- plot-caption artifact content in the report markdown (caption text adjacent to each embedded image)
- discrepancy artifacts for data-MC checks:
  - `outputs/report/data_mc_discrepancy_audit.json`
  - `outputs/report/data_mc_check_log.json`

### Acceptance Checks
- at least one observable plot exists for each fit region
- pre-fit and post-fit control-region plots both exist and are embedded in reporting artifacts
- in unblinded mode, pre-fit and post-fit signal-region plots exist and include observed data across full SR
- in blinded mode, signal-region observed data are either omitted or explicitly masked in sensitive windows with documented boundaries
- control-region pre-fit/post-fit plots display data points and stacked signal/background expectations
- for `H -> gamma gamma`, blinded sideband-fit provenance plots exist for every active category and show sideband data, the full-range sideband-fitted background-only PDF, and stacked expected signal
- for `H -> gamma gamma`, expected-significance Asimov fit plots exist for every active category and the combined fit and show Asimov pseudo-data, the fitted free-`mu` signal-plus-background total, and the corresponding background-only component over `105-160 GeV`
- for `H -> gamma gamma`, observed-data full-range fit plots exist only after explicit unblinding and then show observed data, the fitted free-`mu` signal-plus-background total, and the fitted background-only component for every active category and the combined fit
- for `H -> gamma gamma`, the required statistical-input plots exist and are not treated as optional
- for `H -> gamma gamma`, cut flow is presented separately for signal production modes, diphoton background MC, and data
- for `H -> gamma gamma`, MC statistical uncertainties in reported yields are derived from event weights rather than naive event counts
- report includes event-selection summary, cut flow summary, and fit result summary
- report includes significance summary when significance artifacts exist
- report includes blinding summary when blinding artifacts exist
- report uses inline markdown image tags (for example `![](plots/<name>.png)`) for produced plots
- when category-resolved resonance plots are produced, there is one plot per active category and blinded windows hide data points unless unblinded
- every embedded image in report markdown is immediately accompanied by a caption that explains entries and motivation
- substantial data-MC discrepancies are explicitly called out and not hidden by cosmetic-only changes
- discrepancy artifacts exist even when no substantial discrepancy is found

## Layer 3 — Example Implementation
### Report Inputs (Current Repository)
- `outputs/background_modeling_strategy.json`
- `outputs/fit/*/signal_pdf.json`
- `outputs/fit/*/background_pdf_choice.json`
- `outputs/fit/*/spurious_signal.json`
- `outputs/report/blinding_summary.json`
- `outputs/fit/*/blinded_cr_fit.json`
- `outputs/fit/*/results.json`
- `outputs/fit/*/significance.json`

### CLI (Current Repository)
`python -m analysis.report.make_report --summary outputs/summary.normalized.json --outputs outputs --out outputs/report/report.md`

### Downstream Reference
Use:
- `analysis_strategy/control_region_signal_region_blinding_and_visualization.md`
- `core_pipeline/final_analysis_report_agent_workflow.md`
- `governance/data_mc_discrepancy_sanity_check.md`

# Examples

Example invocation context:
- `python -m analysis.report.make_report --summary outputs/summary.normalized.json --outputs outputs --out outputs/report/report.md`

Example expected outputs:
- `outputs/report/data_mc_discrepancy_audit.json`
- `outputs/report/data_mc_check_log.json`
- `outputs/background_modeling_strategy.json`
- `outputs/fit/`
- `outputs/report/blinding_summary.json`
- `outputs/summary.normalized.json`
- `outputs/report/report.md`
