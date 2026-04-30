---
skill_id: SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
display_name: "Profile Likelihood Discovery Significance"
version: 1.0
category: stats

summary: "For H->gammagamma, expected significance uses full-range S+B Asimov pseudo-data, while observed significance is allowed only after explicit unblinding and then uses observed data over the full `105-160 GeV` range; the skill must also expose the fit components needed to visualize expected and observed fits."

invocation_keywords:
  - "profile likelihood significance"
  - "profile likelihood discovery significance"
  - "fit"
  - "profile"
  - "likelihood"
  - "discovery"
  - "significance"

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
  - name: per_fit_significance_artifact_containing_fit_identifiers_poi_met
    type: artifact
    description: "per-fit significance artifact containing fit identifiers, POI metadata, NLL values, test statistic, significance, status diagnostics, and fit-range/blinding metadata for category-resolved fits"
  - name: optional_asimov_significance_artifact_per_fit_containing
    type: artifact
    description: "optional Asimov significance artifact per fit containing:"
  - name: asimov_dataset_type
    type: artifact
    description: "Asimov dataset type (`signal_plus_background` for expected discovery significance)"
  - name: source_pdf_model_provenance
    type: artifact
    description: "source PDF/model provenance"
  - name: parameter_source_provenance
    type: artifact
    description: "parameter-source provenance (for example data-fit snapshot used to generate Asimov)"
  - name: fit_range_used_for_asimov_generation_evaluation
    type: artifact
    description: "fit range used for Asimov generation/evaluation"
  - name: generation_hypothesis_details
    type: artifact
    description: "generation hypothesis details (for example `mu_gen = 1` for signal-plus-background expected discovery sensitivity)"
  - name: parameter_floating_policy_artifact
    type: artifact
    description: "parameter-floating-policy artifact declaring observed-vs-expected significance scope and the fixed/floating parameter policy used in the significance fits"
  - name: significance_fit_component_payload_artifact_for_plotting
    type: artifact
    description: "artifact exposing the signal-plus-background total and background-only components needed to render H->gammagamma expected-significance Asimov fits and, when explicitly unblinded, observed-data full-range fits"

preconditions:
  - "Dependency SKILL_WORKSPACE_AND_FIT_PYHF has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_WORKSPACE_AND_FIT_PYHF

  may_follow:
    - SKILL_WORKSPACE_AND_FIT_PYHF

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
  - "writes per_fit_significance_artifact_containing_fit_identifiers_poi_met"
  - "writes optional_asimov_significance_artifact_per_fit_containing"
  - "writes asimov_dataset_type"
  - "writes source_pdf_model_provenance"
  - "writes parameter_source_provenance"
  - "writes fit_range_used_for_asimov_generation_evaluation"
  - "writes generation_hypothesis_details"
  - "writes significance_fit_component_payload_artifact_for_plotting"

failure_modes:
  - "failed result includes actionable diagnostic information"

validation_checks:
  - "significance artifact exists for each fit under test"
  - "successful result satisfies `q0 >= 0`"
  - "successful result satisfies `z_discovery = sqrt(q0)` within numerical tolerance"
  - "failed result includes actionable diagnostic information"
  - "for the required PyROOT backend in H->gammagamma workflows, exported NLL values and POI conventions are mapped consistently into the standard significance schema"
  - "for H->gammagamma workflows, primary significance artifacts declare `pyroot_roofit`; any non-ROOT significance artifact is explicitly marked cross-check-only and excluded from central claims"
  - "significance artifacts for category-combined fits list categories included and whether `mu` is shared across them"
  - "Asimov significance artifacts explicitly declare that inputs are pseudo-data and include generation provenance"
  - "observed and Asimov significance outputs are not conflated in reporting"
  - "for H->gammagamma, observed significance is produced only after explicit user unblinding and then uses observed data over the full `105-160 GeV` range"
  - "for H->gammagamma, blinded workflows do not inspect observed data in `120-130 GeV` and do not produce central observed significance from blinded observed data"
  - "when an Asimov sensitivity result is reported in blinded workflows, Asimov generation/evaluation range includes the full `105-160 GeV` range including the signal region"
  - "discovery-sensitivity Asimov artifacts explicitly document signal-plus-background generation hypothesis (`mu_gen = 1`) and background-parameter provenance from the `mu = 0` fit snapshot"
  - "H->gammagamma significance fits keep signal DSCB shape parameters fixed, allow signal normalization to float through `mu`, and allow background normalization and background shape parameters to float"
  - "for H->gammagamma, significance-stage artifacts expose the fitted signal-plus-background total and corresponding background-only component needed to plot the expected Asimov fit"
  - "for H->gammagamma, observed-data significance/component outputs are produced only after explicit unblinding and are then sufficient to plot full-range observed data with the fitted free-`mu` signal-plus-background total and background-only component"

handoff_to:
  - SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB
  - SKILL_PLOTTING_AND_REPORT
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/profile_likelihood_significance.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `core_pipeline/profile_likelihood_significance.md`
- Original stage: `fit`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Profile Likelihood Discovery Significance

## Layer 1 — Physics Policy
Discovery significance is computed with a profile-likelihood-ratio test comparing background-only and unconstrained fits.

Policy requirements:
- perform a conditional fit with signal strength fixed to the background-only hypothesis (`mu = 0`)
- perform an unconditional fit where signal strength is free
- construct the one-sided discovery test statistic
- for H->gammagamma workflows, compute primary significance with `pyroot_roofit`; if an optional cross-check backend is used, apply the same `q0` definition
- for H->gammagamma primary claims, significance must come from RooFit analytic-function likelihood fits; unavailable RooFit capability is a blocked condition, not a fallback condition
- for category-combined fits, construct a single combined likelihood over all configured categories with one shared POI (`mu`) and category-specific background parameters
- when blinding is active for resonance windows, significance metadata must declare whether fits used full range or sideband-only ranges
- for `H -> gamma gamma`, expected significance during blinded analysis development must be computed using Asimov pseudo-data rather than observed signal-region data
- for `H -> gamma gamma`, observed significance may be computed only if the user explicitly instructs unblinding; when unblinded, use observed data over the full `105-160 GeV` range
- for `H -> gamma gamma`, blinded mode forbids inspection of observed data in `120-130 GeV` and therefore forbids central observed significance from blinded observed data
- Asimov pseudo-data for expected sensitivity must be generated over the full observable range `105-160 GeV`, including the signal region
- Asimov generation must use PDFs loaded with parameter values obtained from fits to real data (sideband-constrained under blinding for the background component)
- for expected discovery-significance sensitivity evaluation, generate the Asimov dataset under the signal-plus-background hypothesis (`mu_gen = 1`)
- background-shape parameters used for this generation may come from a data fit with `mu = 0`; record both hypotheses explicitly
- distinguish clearly between fixed quantities used to generate the Asimov dataset and floating quantities used in the later significance fit
- for `H -> gamma gamma`, signal DSCB shape parameters from the signal-MC fit must remain fixed in downstream significance fits
- for `H -> gamma gamma`, signal normalization must float only through the shared signal-strength parameter `mu`
- for `H -> gamma gamma`, background normalization is free and background shape parameters are free in the significance fit
- then evaluate incompatibility of the background-only hypothesis with the signal-plus-background model via the profile-likelihood discovery test statistic
- Asimov datasets are pseudo-data (not observed data), so they can be evaluated/visualized in the full mass range including the signal window
- for `H -> gamma gamma`, the significance stage must emit or preserve the signal-plus-background total and the corresponding background-only component so downstream plotting can render the expected Asimov fit and, after explicit unblinding, the observed-data full-range fit
- significance results must clearly label whether they are observed-data or Asimov-based expected results

Test statistic definition:
`q0 = -2 ln lambda(0) = 2 * (NLL_mu0 - NLL_muhat)`

One-sided discovery convention:
- `q0 = max(q0, 0)`

Asymptotic significance:
- `Z = sqrt(q0)`

## Layer 2 — Workflow Contract
### Required Artifacts
- per-fit significance artifact containing fit identifiers, POI metadata, NLL values, test statistic, significance, status diagnostics, and fit-range/blinding metadata for category-resolved fits
- optional Asimov significance artifact per fit containing:
  - Asimov dataset type (`signal_plus_background` for expected discovery significance)
  - source PDF/model provenance
  - parameter-source provenance (for example data-fit snapshot used to generate Asimov)
  - fit range used for Asimov generation/evaluation
  - generation hypothesis details (for example `mu_gen = 1` for signal-plus-background expected discovery sensitivity)
- parameter-floating-policy artifact containing:
  - observed-significance enable/disable status
  - explicit unblinding requirement for observed significance
  - fixed signal-shape parameters from the signal-MC DSCB fit
  - floating signal-strength parameter `mu`
  - floating background normalization
  - floating background shape parameters
- significance-fit component payload artifact for downstream plotting containing:
  - expected-significance Asimov fit components over `105-160 GeV`
  - signal-plus-background total and corresponding background-only component
  - when explicitly unblinded, the same component breakdown for the observed-data full-range free-`mu` fit

### Acceptance Checks
- significance artifact exists for each fit under test
- successful result satisfies `q0 >= 0`
- successful result satisfies `z_discovery = sqrt(q0)` within numerical tolerance
- failed result includes actionable diagnostic information
- for the required PyROOT backend in H->gammagamma workflows, exported NLL values and POI conventions are mapped consistently into the standard significance schema
- for H->gammagamma workflows, primary significance artifacts declare `pyroot_roofit`; any non-ROOT significance artifact is explicitly marked cross-check-only and excluded from central claims
- significance artifacts for category-combined fits list categories included and whether `mu` is shared across them
- Asimov significance artifacts explicitly declare that inputs are pseudo-data and include generation provenance
- observed and Asimov significance outputs are not conflated in reporting
- for `H -> gamma gamma`, observed significance is produced only after explicit user unblinding and then uses observed data over the full `105-160 GeV` range
- for `H -> gamma gamma`, blinded workflows do not inspect observed data in `120-130 GeV` and do not produce central observed significance from blinded observed data
- when an Asimov sensitivity result is reported in blinded workflows, Asimov generation/evaluation range includes the full `105-160 GeV` range including the signal region
- discovery-sensitivity Asimov artifacts explicitly document signal-plus-background generation hypothesis (`mu_gen = 1`) and background-parameter provenance from the `mu = 0` fit snapshot
- `H -> gamma gamma` significance fits keep signal DSCB shape parameters fixed, allow signal normalization to float through `mu`, and allow background normalization and background shape parameters to float
- `H -> gamma gamma` significance-stage artifacts are sufficient to draw the expected Asimov fit with pseudo-data, fitted signal-plus-background total, and background-only component over the full mass range
- if observed-data significance or full-range observed component payloads are produced, explicit unblinding is declared and the artifact contains observed full-range data plus the fitted free-`mu` signal-plus-background total and background-only component

## Layer 3 — Example Implementation
### Required Fields (Current Repository)
- `fit_id`
- `status`
- `poi_name`
- `mu_hat`
- `twice_nll_mu0`
- `twice_nll_free`
- `q0`
- `z_discovery`
- `error` (if failed)
- `dataset_type` (recommended: `observed` or `asimov`)
- `asimov_source` (required when `dataset_type=asimov`)
- `fit_range` (recommended for blinded workflows)
- `mu_gen` (required when `dataset_type=asimov`)
- `background_parameter_source` (required when `dataset_type=asimov`)
- `observed_significance_allowed` (recommended)
- `signal_shape_parameter_policy` (recommended: `fixed_from_signal_mc_fit`)
- `background_parameter_policy` (recommended)

### CLI (Current Repository)
`python -m analysis.stats.significance --workspace outputs/fit/workspace.json --fit-id FIT1 --out outputs/fit/FIT1/significance.json`

Asimov expected-significance artifact (example):
`python -m analysis.stats.significance --workspace outputs/fit/workspace.json --fit-id FIT1 --out outputs/fit/FIT1/significance_asimov.json`

# Examples

Example invocation context:
- `python -m analysis.stats.significance --workspace outputs/fit/workspace.json --fit-id FIT1 --out outputs/fit/FIT1/significance.json`
- `python -m analysis.stats.significance --workspace outputs/fit/workspace.json --fit-id FIT1 --out outputs/fit/FIT1/significance_asimov.json`

Example expected outputs:
- `outputs/fit/workspace.json`
- `outputs/fit/FIT1/significance.json`
- `outputs/fit/FIT1/significance_asimov.json`
