---
skill_id: SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB
display_name: "Asimov Expected Significance (S+B Generation)"
version: 1.0
category: stats

summary: "Expected H->gammagamma discovery significance must use signal-plus-background Asimov pseudo-data over `105-160 GeV`, including the blinded window, with explicit generation and fit-parameter provenance plus a mandatory full-range Asimov fit visualization."

invocation_keywords:
  - "asimov expected significance splusb"
  - "asimov expected significance (s+b generation)"
  - "fit"
  - "asimov"
  - "expected"
  - "significance"
  - "generation"

when_to_use:
  - "Use when executing or validating the fit stage of the analysis workflow."
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
  - name: asimov_expected_significance_artifact_per_fit_with
    type: artifact
    description: "Asimov expected-significance artifact per fit with:"
  - name: dataset_type_asimov
    type: artifact
    description: "`dataset_type = \"asimov\"`"
  - name: generation_hypothesis_signal_plus_background
    type: artifact
    description: "`generation_hypothesis = \"signal_plus_background\"`"
  - name: mu_gen_1
    type: artifact
    description: "`mu_gen = 1`"
  - name: background_parameter_source_describing_the_mu_0_data_fit_snapsho
    type: artifact
    description: "`background_parameter_source` describing the `mu = 0` data-fit snapshot used for background-PDF parameters"
  - name: fit_range_used_for_generation_evaluation
    type: artifact
    description: "`fit_range` used for generation/evaluation"
  - name: q0_and_z_discovery
    type: artifact
    description: "`q0` and `z_discovery`"
  - name: optional_sideband_background_fit_provenance_artifact_linking_par
    type: artifact
    description: "optional sideband/background-fit provenance artifact linking parameter values to the `mu = 0` fit used for shape determination"
  - name: asimov_construction_method_artifact
    type: artifact
    description: "Asimov-construction-method artifact recording whether the dataset was generated directly from RooFit tools or constructed explicitly as a weighted bin-center dataset over `105-160 GeV`"
  - name: fixed_vs_floating_parameter_policy_artifact
    type: artifact
    description: "artifact distinguishing fixed quantities used to generate the Asimov dataset from floating quantities used in the downstream significance fit"
  - name: asimov_expected_significance_fit_visualization_or_plot_payload_ar
    type: artifact
    description: "artifact or plot-payload enabling a full-range H->gammagamma Asimov fit visualization with Asimov pseudo-data, the fitted free-`mu` signal-plus-background model, and the corresponding background-only component"

preconditions:
  - "Dependency SKILL_WORKSPACE_AND_FIT_PYHF has completed successfully."
  - "Dependency SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_WORKSPACE_AND_FIT_PYHF
    - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE

  may_follow:
    - SKILL_WORKSPACE_AND_FIT_PYHF
    - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
    - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW

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
  - "writes asimov_expected_significance_artifact_per_fit_with"
  - "writes dataset_type_asimov"
  - "writes generation_hypothesis_signal_plus_background"
  - "writes mu_gen_1"
  - "writes background_parameter_source_describing_the_mu_0_data_fit_snapsho"
  - "writes fit_range_used_for_generation_evaluation"
  - "writes q0_and_z_discovery"
  - "writes optional_sideband_background_fit_provenance_artifact_linking_par"
  - "writes asimov_expected_significance_fit_visualization_or_plot_payload_ar"

failure_modes:
  - "Missing or ambiguous required inputs block execution."
  - "Schema, fit, or consistency checks fail and produce diagnostics."

validation_checks:
  - "expected-significance Asimov artifacts use `mu_gen = 1`"
  - "artifact provenance explicitly records that background-PDF parameters came from a `mu = 0` data fit"
  - "expected-significance claims in blinded mode do not rely on observed signal-region data"
  - "for H->gammagamma, Asimov generation/evaluation range for expected significance is the full `105-160 GeV` range including `120-130 GeV`"
  - "signal component in the Asimov dataset uses signal MC normalized to the MC prediction and a double-sided Crystal Ball shape with parameters taken from the signal-MC fit"
  - "background component in the Asimov dataset uses the background PDF fitted to observed sideband data only and then evaluated over the full `105-160 GeV` range"
  - "if direct generation support is unavailable, the Asimov dataset is explicitly constructed by binning `105-160 GeV`, placing one weighted entry at each bin center, and assigning the bin-integral weight from the PDF"
  - "artifacts distinguish fixed generation inputs from floating significance-fit parameters"
  - "for H->gammagamma, Asimov expected-significance artifacts are sufficient to render a full-range visualization with Asimov pseudo-data, the fitted free-`mu` signal-plus-background total, and the corresponding background-only component"
  - "for H->gammagamma, the free-`mu` Asimov fit records `mu_hat` for closure and flags a diagnostic if it is materially incompatible with `1` relative to the fitted uncertainty"
  - "expected (Asimov) and observed significance outputs are reported separately"

handoff_to:
  - SKILL_PLOTTING_AND_REPORT
  - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
  - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/asimov_expected_significance_splusb.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. Fit observed data in sidebands only (`105-120 GeV` and `130-160 GeV`) to determine background-PDF parameters with `mu` fixed to `0`.
2. Snapshot those background parameters as the Asimov-generation baseline.
3. Fit the signal MC `m_gg` distribution with a double-sided Crystal Ball function and use the fitted signal-shape parameters as the signal-shape input.
4. Normalize the signal component to the MC signal prediction.
5. Set `mu_gen = 1` and generate Asimov pseudo-data from the full S+B model over `105-160 GeV`.
6. If direct generation support is unavailable, construct the Asimov dataset explicitly in RooFit style:
   - choose the desired binning over `105-160 GeV`
   - for each bin, place one entry at the bin center
   - assign the entry weight equal to the integral of the PDF over that bin
   - use RooFit dataset objects or equivalent weighted dataset objects for this construction
7. On this Asimov dataset, compute discovery significance with:
   - conditional fit at `mu = 0`
   - unconditional fit with free `mu`
   - `q0 = max(2 * (NLL_mu0 - NLL_free), 0)` and `Z = sqrt(q0)`
8. Save expected-significance output with explicit provenance of:
   - background-shape fit hypothesis (`mu_fit_for_bkg = 0`)
   - Asimov generation hypothesis (`mu_gen = 1`)
   - full generation/evaluation range `105-160 GeV`
   - fixed generation inputs versus floating fit parameters

# Notes

- Source file: `core_pipeline/asimov_expected_significance_splusb.md`
- Original stage: `fit`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Asimov Expected Significance (S+B Generation)

## Layer 1 — Physics Policy
Expected discovery significance must use signal-plus-background Asimov pseudo-data with `mu_gen = 1`.

Policy requirements:
- determine background-PDF parameters from a fit where signal strength is fixed to background-only (`mu = 0`) using observed sideband data only when blinding is active
- for `H -> gamma gamma`, the observed-data sidebands are `105-120 GeV` and `130-160 GeV`
- keep this background-parameter snapshot as the background-shape provenance for Asimov generation
- fit the signal MC `m_gg` distribution with a double-sided Crystal Ball function and use the fitted signal-shape parameters as the Asimov signal-shape input
- normalize the signal component to the MC signal prediction
- generate expected-significance Asimov pseudo-data from the full model with `mu_gen = 1` (signal plus background)
- for `H -> gamma gamma`, generate the Asimov background component from the fitted background PDF over the full `105-160 GeV` range, including `120-130 GeV`
- do not conflate the background-shape fit hypothesis (`mu = 0`) with the Asimov generation hypothesis (`mu_gen = 1`)
- do not exclude `120-130 GeV` from blinded expected-significance Asimov generation; once the background PDF is fit in sidebands it is defined over the full `105-160 GeV` range and should be used over that full range
- if direct tool support is unavailable, construct the Asimov dataset explicitly in RooFit style by choosing binning over `105-160 GeV`, placing one entry at each bin center, and assigning the entry weight equal to the bin integral of the PDF
- evaluate discovery `q0` on the generated Asimov dataset using the standard conditional (`mu = 0`) versus unconditional (free `mu`) fits
- record explicitly which quantities were fixed to generate the Asimov dataset and which quantities are later allowed to float in the significance fit
- for `H -> gamma gamma`, produce a mandatory full-range Asimov fit visualization or plot-payload that shows the signal-plus-background Asimov pseudo-data, the fitted free-`mu` signal-plus-background total, and the corresponding background-only component so the excess near `125 GeV` is visible against the smooth continuum expectation
- for `H -> gamma gamma`, record the fitted `mu_hat` from the free-`mu` Asimov closure fit and flag a warning diagnostic if it is not compatible with `1` within the fitted uncertainty
- label outputs as expected/Asimov and record both hypotheses in metadata

## Layer 2 — Workflow Contract
### Required Artifacts
- Asimov expected-significance artifact per fit with:
  - `dataset_type = "asimov"`
  - `generation_hypothesis = "signal_plus_background"`
  - `mu_gen = 1`
  - `background_parameter_source` describing the `mu = 0` data-fit snapshot used for background-PDF parameters
  - `fit_range` used for generation/evaluation
  - `q0` and `z_discovery`
- optional sideband/background-fit provenance artifact linking parameter values to the `mu = 0` fit used for shape determination
- Asimov-construction-method artifact containing:
  - `generation_range = [105.0, 160.0]`
  - `blind_window_in_observed_data = [120.0, 130.0]`
  - `construction_mode` (`direct_generation` or `weighted_bin_center_dataset`)
  - `binning`
  - `weighted_dataset_object_type`
- fixed-vs-floating-parameter-policy artifact containing:
  - fixed inputs at generation time:
    - signal yield normalized to MC prediction
    - signal DSCB shape parameters from the signal-MC fit
    - background PDF parameters from the sideband data fit with `mu = 0`
  - later floating fit parameters:
    - signal strength parameter `mu`
    - background normalization
    - background shape parameters
- Asimov expected-significance fit visualization or plot-payload artifact containing:
  - Asimov pseudo-data over the full `105-160 GeV` range
  - the fitted free-`mu` signal-plus-background total
  - the corresponding background-only component from the same fitted model context
  - `mu_hat` and `mu`-closure diagnostics for the Asimov free fit

### Acceptance Checks
- expected-significance Asimov artifacts use `mu_gen = 1`
- artifact provenance explicitly records that background-PDF parameters came from a `mu = 0` data fit
- expected-significance claims in blinded mode do not rely on observed signal-region data
- for `H -> gamma gamma`, Asimov generation/evaluation range for expected significance is the full `105-160 GeV` range including `120-130 GeV`
- the signal Asimov component uses signal MC normalized to the MC prediction and DSCB parameters from the signal-MC fit
- the background Asimov component uses the background PDF fitted to observed sideband data only and then evaluated over the full `105-160 GeV` range
- if direct generation support is unavailable, the weighted bin-center construction method is used and recorded explicitly
- artifacts distinguish fixed generation inputs from floating significance-fit parameters
- mandatory `H -> gamma gamma` Asimov fit visualization or plot-payload exists and contains Asimov pseudo-data, fitted free-`mu` signal-plus-background total, and the corresponding background-only component over `105-160 GeV`
- free-`mu` Asimov closure records `mu_hat` and produces a warning diagnostic if `mu_hat` is materially inconsistent with `1` relative to the fit uncertainty
- expected (Asimov) and observed significance outputs are reported separately

## Layer 3 — Example Implementation
### Procedure
1. Fit real data to determine background-shape parameters with `mu` fixed to `0` (often sideband-constrained when blinded).
2. Snapshot those background parameters as the Asimov-generation baseline.
3. Set `mu_gen = 1` and generate Asimov pseudo-data from the S+B model over the full analysis range.
4. On this Asimov dataset, compute discovery significance with:
   - conditional fit at `mu = 0`
   - unconditional fit with free `mu`
   - `q0 = max(2 * (NLL_mu0 - NLL_free), 0)` and `Z = sqrt(q0)`
5. Save expected-significance output with explicit provenance of both:
   - background-shape fit hypothesis (`mu_fit_for_bkg = 0`)
   - Asimov generation hypothesis (`mu_gen = 1`)

### Related Skills
- `core_pipeline/profile_likelihood_significance.md`
- `core_pipeline/workspace_and_fit_pyhf.md`
- `core_pipeline/final_analysis_report_agent_workflow.md`

# Examples

Example invocation context:
- Run this contract in the declared stage using the required inputs and dependencies.

Example expected outputs:
- `asimov_expected_significance_artifact_per_fit_with`
- `dataset_type_asimov`
- `generation_hypothesis_signal_plus_background`
- `mu_gen_1`
