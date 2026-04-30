---
skill_id: SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION
display_name: "Signal Shape and Spurious-Signal Background Model Selection"
version: 1.0
category: stats

summary: "For analytic mass-fit analyses, derive signal and background parameterizations with explicit spurious-signal control."

invocation_keywords:
  - "signal shape and spurious signal model selection"
  - "signal shape and spurious-signal background model selection"
  - "design"
  - "signal"
  - "shape"
  - "spurious"
  - "background"
  - "model"

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
  - name: signal_pdf_artifact_with_fit_parameters_covariance_information_a
    type: artifact
    description: "signal-PDF artifact with fit parameters, covariance information (when available), and fit status"
  - name: background_template_selection_and_normalization_artifact
    type: artifact
    description: "background-template selection and normalization artifact for H->gammagamma spurious-signal studies, including nominal diphoton sample choice, selected generated-mass window, sideband-normalization inputs, and rationale"
  - name: effective_mc_luminosity_and_smoothing_artifact
    type: artifact
    description: "effective-MC-luminosity and smoothing artifact recording the computed effective luminosity, the `10 x 36 fb^-1` threshold test, whether TH1-based smoothing was applied, and why"
  - name: background_scan_artifact_listing_all_tested_functional_forms_and
    type: artifact
    description: "background-scan artifact listing all tested functional forms and complexity levels"
  - name: background_choice_artifact_recording_selected_model_and_explicit
    type: artifact
    description: "background-choice artifact recording selected model and explicit selection rationale"
  - name: spurious_signal_artifact_with_n_spur_sigma_nsig_r_spur_and_pass_
    type: artifact
    description: "spurious-signal artifact with `N_spur`, `sigma_Nsig`, `r_spur`, and pass/fail flag"
  - name: backend_provenance_artifact_recording_pyroot_roofit_as_primary_b
    type: artifact
    description: "backend-provenance artifact recording `pyroot_roofit` as primary backend and any optional cross-check backend"
  - name: category_wise_signal_shape_artifact_containing_ds_cb_parameters_
    type: artifact
    description: "category-wise signal-shape artifact containing DS-CB parameters and fit status per category for RooFit combined workflows"
  - name: outputs_fit_fit_id_signal_pdf_json
    type: artifact
    description: "`outputs/fit/<fit_id>/signal_pdf.json`"
  - name: outputs_fit_fit_id_background_pdf_scan_json
    type: artifact
    description: "`outputs/fit/<fit_id>/background_pdf_scan.json`"
  - name: outputs_fit_fit_id_background_pdf_choice_json
    type: artifact
    description: "`outputs/fit/<fit_id>/background_pdf_choice.json`"
  - name: outputs_fit_fit_id_spurious_signal_json
    type: artifact
    description: "`outputs/fit/<fit_id>/spurious_signal.json`"
  - name: outputs_fit_fit_id_roofit_combined_signal_dscb_parameters_json
    type: artifact
    description: "`outputs/fit/<fit_id>/roofit_combined/signal_dscb_parameters.json` (required for H->gammagamma category-resolved workflows)"
  - name: statistical_input_plot_artifact_set
    type: artifact
    description: "statistical-input plot artifact set containing per-category signal-shape fits, the nominal unsmoothed sideband-normalized diphoton template, the selected spurious-signal fit, and the smoothed-template fit when smoothing is applied"

preconditions:
  - "Dependency SKILL_HISTOGRAMMING_AND_TEMPLATES has completed successfully."
  - "Dependency SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_HISTOGRAMMING_AND_TEMPLATES
    - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS

  may_follow:
    - SKILL_HISTOGRAMMING_AND_TEMPLATES
    - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
    - SKILL_SYSTEMATICS_AND_NUISANCES
    - SKILL_WORKSPACE_AND_FIT_PYHF
    - SKILL_PLOTTING_AND_REPORT

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
  - "writes signal_pdf_artifact_with_fit_parameters_covariance_information_a"
  - "writes background_scan_artifact_listing_all_tested_functional_forms_and"
  - "writes background_choice_artifact_recording_selected_model_and_explicit"
  - "writes spurious_signal_artifact_with_n_spur_sigma_nsig_r_spur_and_pass_"
  - "writes backend_provenance_artifact_recording_pyroot_roofit_as_primary_b"
  - "writes category_wise_signal_shape_artifact_containing_ds_cb_parameters_"
  - "writes outputs_fit_fit_id_signal_pdf_json"
  - "writes outputs_fit_fit_id_background_pdf_scan_json"
  - "writes outputs_fit_fit_id_background_pdf_choice_json"
  - "writes outputs_fit_fit_id_spurious_signal_json"

failure_modes:
  - "spurious-signal result includes pass/fail status against the target criterion"
  - "if mandatory RooFit analytic modeling cannot be executed, stage status is blocked/failed for primary results"

validation_checks:
  - "signal-PDF fit converges or returns actionable diagnostics"
  - "background scan includes all tested candidate forms"
  - "chosen background model includes explicit rule-based justification"
  - "spurious-signal result includes pass/fail status against the target criterion"
  - "for H->gammagamma, the nominal background template used for spurious-signal studies is the default diphoton MC sample in the minimum generated-mass window that fully contains `105-160 GeV`"
  - "for H->gammagamma, the nominal background template is normalized by matching the weighted diphoton-MC sideband integral to observed data counts in `105-120 GeV` and `130-160 GeV`; absolute cross-section normalization is not the nominal template normalization for this purpose"
  - "for H->gammagamma, the prior failure mode of combining many individually low-statistics auxiliary background samples into the nominal template is explicitly rejected and documented"
  - "effective MC luminosity is computed as weighted MC entries divided by cross section and compared against `10 x 36 fb^-1`"
  - "if effective MC luminosity is below the threshold, a TH1-based smoothed template is used for function selection and the smoothing decision is recorded"
  - "required statistical-input plots exist: per-category signal MC with fitted DSCB, nominal unsmoothed sideband-normalized diphoton template, selected spurious-signal fit, and smoothed-template fit when smoothing is applied"
  - "fitted parameter values and fit status from PyROOT are exported in non-ROOT machine-readable form"
  - "H->gammagamma backend provenance records `pyroot_roofit` as primary and includes analytic PDF family per category"
  - "if mandatory RooFit analytic modeling cannot be executed, stage status is blocked/failed for primary results"

handoff_to:
  - SKILL_WORKSPACE_AND_FIT_PYHF
  - SKILL_SYSTEMATICS_AND_NUISANCES
  - SKILL_PLOTTING_AND_REPORT
  - SKILL_SELECTION_ENGINE_AND_REGIONS
  - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
---

# Purpose

This skill defines a structured execution contract for `analysis_strategy/signal_shape_and_spurious_signal_model_selection.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `analysis_strategy/signal_shape_and_spurious_signal_model_selection.md`
- Original stage: `design`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Signal Shape and Spurious-Signal Background Model Selection

## Layer 1 — Physics Policy
For analytic mass-fit analyses, derive signal and background parameterizations with explicit spurious-signal control.

Policy requirements:
- obtain the signal mass distribution from selected signal simulation with proper weights
- for `H -> gamma gamma`, fit the signal `m_gg` distribution in each category with a double-sided Crystal Ball function and export the fitted shape parameters
- scan candidate background functional forms with increasing complexity
- for `H -> gamma gamma`, cap the scanned background-function degree/complexity at `3` for the spurious-signal selection workflow; do not escalate to higher-degree candidates after a failed spurious-signal test at that cap
- evaluate spurious signal by fitting signal-plus-background to a background-only template
- for `H -> gamma gamma`, the nominal background template used for the spurious-signal/background-function workflow must be the default diphoton MC sample in the minimum available generated-mass window that fully contains `105-160 GeV`
- for `H -> gamma gamma`, do not construct the nominal background template by combining a large number of low-statistics background MC samples; this prior failure mode inflates statistical fluctuations and degrades the spurious-signal test
- for `H -> gamma gamma`, define sidebands as `105-120 GeV` and `130-160 GeV`
- for `H -> gamma gamma`, normalize the diphoton-MC background template so that the weighted diphoton-MC integral in the sidebands matches the number of observed data events in those sidebands
- for `H -> gamma gamma`, record explicitly that the real data background contains diphoton, `gamma + jet`, and multijet contributions, but the nominal spurious-signal template is still the diphoton MC sample normalized to data in sidebands; absolute cross-section normalization is not the nominal template normalization for this purpose
- compute effective MC luminosity for the selected diphoton background sample as `effective_luminosity = weighted_number_of_mc_entries / cross_section`
- use target data luminosity `36 fb^-1`
- if effective MC luminosity is at least `10 x 36 fb^-1`, the unsmoothed diphoton template is acceptable for function selection
- otherwise, smooth the `m_gg` template before background-function selection using a TH1-based ROOT smoothing method such as `TH1::Smooth`
- when smoothing is applied, use the smoothed template for the actual background-function selection workflow, but keep the unsmoothed sideband-normalized diphoton template as the nominal template to display
- record the effective MC luminosity, the threshold comparison, whether smoothing was applied, and the reason
- for resonance searches in this repository (notably `H->gammagamma`), PyROOT/RooFit is the mandatory primary backend for analytic-function fitting
- for H->gammagamma primary interpretation, non-RooFit or binned-template substitutions are not valid replacements for the mandatory RooFit analytic-function path
- backend choice must remain transparent: export machine-readable JSON summaries even when PyROOT is used
- for category-resolved diphoton fits, fit a double-sided Crystal Ball signal shape independently in each category
- category-resolved workflows must support arbitrary category counts from fit configuration (not fixed to a specific number)

Spurious-signal metric:
- `N_spur`: fitted signal yield on background-only template
- `sigma_Nsig`: uncertainty on fitted signal yield
- `r_spur = |N_spur| / sigma_Nsig`

Selection policy:
- target `r_spur < 0.2`
- choose lowest-complexity candidate that passes
- if multiple candidates pass at same complexity, prefer smaller `|N_spur|`
- if none pass at lower complexity, escalate only up to degree/complexity `3`
- if no candidate passes by degree/complexity `3`, do not test higher-degree candidates; choose the candidate with the smallest `r_spur` among those tested up to the cap, flag noncompliance, and record explicitly that the degree/complexity cap was reached

## Layer 2 — Workflow Contract
### Required Artifacts
- signal-PDF artifact with fit parameters, covariance information (when available), and fit status
- background-template selection and normalization artifact containing:
  - selected nominal diphoton sample ID
  - selected generated-mass window
  - statement that the selected window is the minimum available window fully containing `105-160 GeV`
  - rejected low-statistics auxiliary background samples
  - sideband definitions `105-120 GeV` and `130-160 GeV`
  - weighted diphoton-MC sideband integral
  - observed data sideband count
  - scale factor applied to normalize the diphoton template to data in sidebands
  - explicit note that diphoton MC normalized to data sidebands is the nominal template even though the real data background also contains `gamma + jet` and multijet events
- effective-MC-luminosity and smoothing artifact containing:
  - `effective_luminosity`
  - target luminosity `36 fb^-1`
  - threshold `360 fb^-1`
  - `smoothing_applied`
  - smoothing method (for example `TH1::Smooth`)
  - smoothing rationale
- background-scan artifact listing all tested functional forms and complexity levels, including the maximum tested degree/complexity and whether the scan terminated at the `3`-DOF cap
- background-choice artifact recording selected model and explicit selection rationale, including whether the `3`-DOF cap was reached before the spurious-signal target was satisfied
- spurious-signal artifact with `N_spur`, `sigma_Nsig`, `r_spur`, and pass/fail flag
- background-template provenance block describing sample IDs/process keys used for spurious-signal testing and their mass-range relevance status
- backend-provenance artifact recording `pyroot_roofit` as primary backend and any optional cross-check backend
- category-wise signal-shape artifact containing DS-CB parameters and fit status per category for RooFit combined workflows
- mandatory statistical-input plot artifact set containing:
  - one signal `m_gg` plot per category with the signal MC distribution overlaid by the fitted signal PDF
  - one plot showing the nominal unsmoothed sideband-normalized diphoton template used for the spurious-signal study
  - one plot showing the selected background-function-plus-signal fit used in the spurious-signal procedure
  - when smoothing is applied, one additional plot showing the selected-function fit to the smoothed template used for the actual function-selection step

### Acceptance Checks
- signal-PDF fit converges or returns actionable diagnostics
- background scan includes all tested candidate forms
- chosen background model includes explicit rule-based justification
- spurious-signal result includes pass/fail status against the target criterion
- for `H -> gamma gamma`, the spurious-signal scan records the maximum tested degree/complexity and does not exceed `3` when the target criterion is still not satisfied
- for `H -> gamma gamma`, if no candidate passes by degree/complexity `3`, the selected background model is the smallest-`r_spur` candidate among those tested up to the cap and the noncompliant capped outcome is explicit
- for `H -> gamma gamma`, the nominal background template is the default diphoton MC sample in the minimum generated-mass window that fully contains `105-160 GeV`
- for `H -> gamma gamma`, low-statistics auxiliary background samples are not silently combined into the nominal spurious-signal template
- for `H -> gamma gamma`, sideband normalization uses `105-120 GeV` and `130-160 GeV` and matches the weighted diphoton-MC sideband integral to observed data sideband counts
- effective MC luminosity is computed as weighted MC entries divided by cross section and is recorded in machine-readable form
- the `10 x 36 fb^-1` threshold decision is recorded and smoothing is applied exactly when the threshold is not met
- if smoothing is applied, the smoothed template is used for actual function selection and the unsmoothed template remains the nominal template displayed for provenance
- required statistical-input plots exist: per-category signal MC with fitted DSCB, nominal unsmoothed sideband-normalized diphoton template, selected spurious-signal fit, and smoothed-template fit when smoothing is applied
- fitted parameter values and fit status from PyROOT are exported in non-ROOT machine-readable form
- H->gammagamma backend provenance records `pyroot_roofit` as primary and includes analytic PDF family per category
- if mandatory RooFit analytic modeling cannot be executed, stage status is blocked/failed for primary results

## Layer 3 — Example Implementation
### Expected Outputs (Current Repository)
- `outputs/fit/<fit_id>/signal_pdf.json`
- `outputs/fit/<fit_id>/background_pdf_scan.json`
- `outputs/fit/<fit_id>/background_pdf_choice.json`
- `outputs/fit/<fit_id>/spurious_signal.json`
- `outputs/fit/<fit_id>/roofit_combined/signal_dscb_parameters.json` (required for H->gammagamma category-resolved workflows)
- `outputs/fit/<fit_id>/background_template_normalization.json` (recommended)
- `outputs/fit/<fit_id>/background_template_effective_lumi.json` (recommended)
- `outputs/report/plots/signal_shape_<category>.png`
- `outputs/report/plots/spurious_nominal_template.png`
- `outputs/report/plots/spurious_selected_fit.png`
- `outputs/report/plots/spurious_selected_fit_smoothed.png` (when smoothing is applied)

### CLI (Current Repository)
`python -m analysis.stats.mass_model_selection --fit-id FIT1 --summary outputs/summary.normalized.json --hists outputs/hists --strategy outputs/background_modeling_strategy.json --out outputs/fit/FIT1/background_pdf_choice.json`

### Downstream Reference
Use outputs in:
- `core_pipeline/systematics_and_nuisances.md`
- `core_pipeline/workspace_and_fit_pyhf.md`
- `core_pipeline/plotting_and_report.md`

# Examples

Example invocation context:
- `python -m analysis.stats.mass_model_selection --fit-id FIT1 --summary outputs/summary.normalized.json --hists outputs/hists --strategy outputs/background_modeling_strategy.json --out outputs/fit/FIT1/background_pdf_choice.json`

Example expected outputs:
- `outputs/fit/<fit_id>/signal_pdf.json`
- `outputs/fit/<fit_id>/background_pdf_scan.json`
- `outputs/fit/<fit_id>/background_pdf_choice.json`
- `outputs/fit/<fit_id>/spurious_signal.json`
- `outputs/fit/<fit_id>/roofit_combined/signal_dscb_parameters.json`
- `outputs/summary.normalized.json`
- `outputs/hists`
- `outputs/background_modeling_strategy.json`
