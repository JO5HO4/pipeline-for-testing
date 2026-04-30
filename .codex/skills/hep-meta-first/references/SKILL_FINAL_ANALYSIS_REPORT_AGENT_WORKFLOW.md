---
skill_id: SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
display_name: "Final Analysis Report (ATLAS Open Data Agent Workflow)"
version: 1.0
category: reporting

summary: "The final analysis report must communicate the physics analysis in a concise note-style format while preserving transparency of agent decisions."

invocation_keywords:
  - "final analysis report agent workflow"
  - "final analysis report (atlas open data agent workflow)"
  - "reporting"
  - "final"
  - "analysis"
  - "report"
  - "atlas"
  - "open"

when_to_use:
  - "Use when executing or validating the reporting stage of the analysis workflow."
  - "Use when this context is available: analysis summary specification."
  - "Use when this context is available: region definitions."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: analysis_summary_specification
      type: artifact
      description: "analysis summary specification"
    - name: region_definitions
      type: artifact
      description: "region definitions"
    - name: metadata_table_for_open_data_sample_normalization
      type: artifact
      description: "metadata table for open-data sample normalization"
    - name: cut_flow_yield_fit_significance_and_blinding_artifacts_produced_
      type: artifact
      description: "cut-flow, yield, fit, significance, and blinding artifacts produced by pipeline stages"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: final_report_artifact_in_markdown_with_the_following_sections_in
    type: artifact
    description: "final report artifact in Markdown with the following sections in order:"
  - name: introduction
    type: artifact
    description: "Introduction"
  - name: data_and_monte_carlo_samples
    type: artifact
    description: "Data and Monte Carlo Samples"
  - name: object_definition_and_event_selection
    type: artifact
    description: "Object Definition and Event Selection"
  - name: overview_of_the_analysis_strategy
    type: artifact
    description: "Overview of the Analysis Strategy"
  - name: signal_and_control_regions
    type: artifact
    description: "Signal and Control Regions"
  - name: cut_flow
    type: artifact
    description: "Cut Flow"
  - name: distributions_in_signal_and_control_regions
    type: artifact
    description: "Distributions in Signal and Control Regions"
  - name: systematic_uncertainties
    type: artifact
    description: "Systematic Uncertainties"
  - name: statistical_interpretation
    type: artifact
    description: "Statistical Interpretation"
  - name: summary
    type: artifact
    description: "Summary"
  - name: monte_carlo_sample_table_artifact_within_the_report_containing_d
    type: artifact
    description: "Monte Carlo sample-table artifact within the report containing DSID, sample label, process, role (`signal`/`background`), generator, simulation configuration, cross section, k-factor, and filter efficiency"
  - name: mc_sample_selection_artifact_at_outputs_report_mc_sample_selecti
    type: artifact
    description: "MC sample-selection artifact at `outputs/report/mc_sample_selection.json`"
  - name: cut_flow_table_artifact_with_data_counts_and_weighted_simulated_
    type: artifact
    description: "cut-flow table artifact with data counts and weighted simulated yields"

preconditions:
  - "Dependency SKILL_PLOTTING_AND_REPORT has completed successfully."
  - "Dependency SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK has completed successfully."
  - "Dependency SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB has completed successfully."
  - "Dependency SKILL_SKILL_REFRESH_AND_CHECKPOINTING has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_PLOTTING_AND_REPORT
    - SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK
    - SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB
    - SKILL_SKILL_REFRESH_AND_CHECKPOINTING

  may_follow:
    - SKILL_PLOTTING_AND_REPORT
    - SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK
    - SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB
    - SKILL_SKILL_REFRESH_AND_CHECKPOINTING
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
    - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION
    - SKILL_MC_NORMALIZATION_METADATA_STACKING
    - SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION
    - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
    - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF
    - SKILL_EXTRACT_NEW_SKILL_FROM_FAILURE

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
  - "writes final_report_artifact_in_markdown_with_the_following_sections_in"
  - "writes introduction"
  - "writes data_and_monte_carlo_samples"
  - "writes object_definition_and_event_selection"
  - "writes overview_of_the_analysis_strategy"
  - "writes signal_and_control_regions"
  - "writes cut_flow"
  - "writes distributions_in_signal_and_control_regions"
  - "writes systematic_uncertainties"
  - "writes statistical_interpretation"

failure_modes:
  - "report does not present non-ROOT H->gammagamma numbers as primary results; if only cross-check numbers exist, this is explicitly labeled and central claim is blocked"
  - "report (or linked handoff note) references `outputs/report/skill_checkpoint_status.json` with its status (`pass` or `fail`)"

validation_checks:
  - "section headers exist and appear in required order"
  - "report explicitly states metadata-driven MC normalization inputs and formula"
  - "report states the luminosity value used in normalization and, for default central results, shows `36.1 fb^-1`"
  - "sample table includes required Monte Carlo normalization columns, generator field, simulation-configuration field, and `signal/background` role field"
  - "report clearly separates data-sample description from Monte Carlo-sample description and does not rely on file-name dumps"
  - "report main body describes only central nominal/reference MC samples used in the actual yields and fits"
  - "for H->gammagamma, the final report explicitly documents which nominal background sample was selected, why it was selected, the sideband-normalization method, effective MC luminosity, and the smoothing decision"
  - "for H->gammagamma, the final report explicitly documents blinded vs unblinded status, the Asimov construction method, the fixed-vs-floating parameter policy in significance fits, and the expected-vs-observed significance distinction"
  - "event-selection narrative is restricted to regions used in the log-likelihood fit and states each fit-region observable"
  - "cut-flow presentation distinguishes per-process contributions from combined signal/background totals when multi-process signal/background is used"
  - "for H->gammagamma, cut flow is reported separately for signal production modes, diphoton background MC, and data, with MC statistical uncertainties derived from event weights"
  - "cut-flow defaults to individual MC sample rows unless explicit merged-process instruction is provided by user/config"
  - "report avoids central-yield double counting of nominal and alternative samples for the same physics process"
  - "report embeds produced plots directly via markdown image tags instead of citation-only file lists"
  - "each embedded plot has an adjacent caption sentence/paragraph explaining entries and motivation"
  - "report explicitly states that blinding is default and records whether explicit unblinding was requested"
  - "in blinded mode, signal-region data are hidden either by omitting SR observed-data plots or by explicit sensitive-window masking"

handoff_to:
  - SKILL_EXTRACT_NEW_SKILL_FROM_FAILURE
  - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF
  - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
  - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION
  - SKILL_MC_NORMALIZATION_METADATA_STACKING
  - SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION
  - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
---

# Purpose

This skill defines a structured execution contract for `core_pipeline/final_analysis_report_agent_workflow.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `core_pipeline/final_analysis_report_agent_workflow.md`
- Original stage: `reporting`
- Logic type classification: `reporting`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Final Analysis Report (ATLAS Open Data Agent Workflow)

## Layer 1 — Physics Policy
The final analysis report must communicate the physics analysis in a concise note-style format while preserving transparency of agent decisions.

Policy requirements:
- follow the user-defined analysis goal; do not invent new physics objectives
- document the studied process, discriminating observable, and tested hypothesis
- describe data and simulated samples, including integrated luminosity and run period
- describe data samples and Monte Carlo samples in separate subsections
- in the main body Monte Carlo subsection, discuss only the MC samples actually used for central results
- for Monte Carlo sample descriptions, include:
  - generator and simulation configuration
  - modeled physics process
  - role classification (`signal` or `background`)
- do not require a full file-by-file listing; require a clear sample-level description instead
- for this repository's Run-2 H->gammagamma workflow, the reported central normalization luminosity must be `36.1 fb^-1` unless an explicit override is declared and justified
- report Monte Carlo normalization based on cross section, k-factor, filter efficiency, and signed generator-weight sum
- for `H -> gamma gamma`, explicitly document which nominal background sample was selected for the spurious-signal/background-function workflow and why it was selected
- for `H -> gamma gamma`, explicitly document that the nominal background template uses the default diphoton MC sample in the minimum mass window containing `105-160 GeV`, not a combination of many low-statistics auxiliary background samples
- for `H -> gamma gamma`, explicitly document that the spurious-signal background-function scan is capped at degree/complexity `3`; if no candidate passes by that cap, state that higher-degree candidates were not used and that the selected model is the least-bad capped noncompliant choice
- for `H -> gamma gamma`, explicitly document the sideband-normalization method:
  - sidebands `105-120 GeV` and `130-160 GeV`
  - diphoton MC normalized so its weighted sideband integral matches observed data sideband counts
  - real data background contains diphoton, `gamma + jet`, and multijet contributions, but the nominal template is still diphoton MC normalized to data in sidebands
- for `H -> gamma gamma`, explicitly document the effective MC luminosity calculation `effective_luminosity = weighted_mc_entries / cross_section`
- for `H -> gamma gamma`, explicitly document the smoothing decision and whether the `10 x 36 fb^-1` threshold triggered TH1-based smoothing
- define reconstructed objects and event selections using available dataset observables
- document signal and control region purposes and selection logic
- in the event-selection narrative, discuss only regions that enter the log-likelihood fit
- for each fit region, document the primary fit observable used in that region
- treat blinded analysis as default; only show SR data after explicit unblinding instruction
- for non-signal regions, document both pre-fit and post-fit comparisons between data and MC signal/background
- preserve blinding by hiding signal-region data before unblinding
- include pre-fit and post-fit signal-region plots in unblinded analyses
- in blinded analyses, either:
  - omit signal-region observed-data plots entirely, or
  - mask the sensitive sub-window (for example around a resonance peak) while allowing sideband data display when appropriate
- when unblinded, display observed data across the full signal region (including previously sensitive windows)
- describe the statistical interpretation framework and expected (pre-unblinding) results using Asimov-based fits when applicable
- for H->gammagamma workflows, explicitly state `pyroot_roofit` as the primary fit backend when presenting fit/significance results; any `pyhf` result must be labeled as a cross-check
- for H->gammagamma workflows, if RooFit analytic-fit primary results are unavailable, report blocked status instead of promoting non-ROOT results to central claims
- when expected sensitivity is derived from Asimov pseudo-data, state how Asimov data were generated (source PDF + parameter values from data fit) and whether generation/evaluation used sidebands-only or full mass range
- Asimov pseudo-data figures/tables may include the full mass range (including signal window) in blinded workflows, but must be clearly labeled as expected/Asimov
- for blinded sensitivity claims, expected significance must come from Asimov fits over the full observable range (including signal region), not from observed signal-window data
- when discovery sensitivity is reported from Asimov pseudo-data, document that generation used the signal-plus-background hypothesis (`mu_gen = 1`) while background-shape parameters were taken from a data fit with `mu = 0`
- for `H -> gamma gamma`, explicitly document the Asimov construction method; if explicit weighted bin-center construction was used, say so
- for `H -> gamma gamma`, explicitly distinguish fixed quantities used to generate the Asimov dataset from floating quantities in the later significance fit
- for `H -> gamma gamma`, explicitly state that signal shape parameters from the signal-MC DSCB fit were fixed in significance fits while signal normalization floated through `mu` and background normalization/shape parameters floated
- for `H -> gamma gamma`, explicitly distinguish expected significance from observed significance and state that observed significance requires explicit unblinding
- avoid inventing systematic uncertainties when not provided; use explicit placeholder language instead
- include a mandatory appendix that documents all agent deviations, substitutions, and assumptions with justification
- for category-resolved resonance analyses, include a category-by-category mass-window table at `m_gg = 125 +/- 2 GeV` with expected signal and expected background yields
- in cut-flow reporting, include data, signal, and background contributions
- for `H -> gamma gamma`, cut-flow reporting must show separate contributions for signal production modes, diphoton background MC, and data
- for `H -> gamma gamma`, MC statistical uncertainties in cut-flow and yield tables must be computed from event weights rather than naive event counts
- by default, cut-flow reporting must be broken down to individual Monte Carlo samples
- if the user or analysis JSON explicitly requests merged-process reporting, merged rows may be added
- always provide combined signal/background totals when multiple processes contribute
- when alternative MC samples exist for the same process, central cut-flow/report yields must use nominal/reference samples only, with alternatives discussed under systematics
- include a separate appendix section that explains why the nominal/reference MC samples were selected from the available candidate files
- the appendix must record rejected or alternative candidates and any human clarification used to resolve ambiguity
- for category-resolved resonance analyses, include one diphoton invariant-mass plot per category with:
  - observed data points (sidebands only in blinded mode)
  - expected post-fit background
  - expected signal stacked on top of background
- for `H -> gamma gamma`, when smoothing is applied to the nominal diphoton template used in the spurious-signal/background-function workflow, include or reference an overlay plot with the unsmoothed and smoothed sideband-normalized templates on the same axes so the smoothing effect is directly visible
- do not use a smoothed-template-vs-fit panel as the sole visualization of smoothing impact; any such fit-comparison panel is supplemental to the required unsmoothed-vs-smoothed overlay
- when reporting category-combined significance, explicitly state that the combined likelihood uses category-specific background parameters and a shared signal-strength parameter across categories
- every plot embedded in the final report must include a caption that explains plot entries and gives motivation/justification for why the plot is part of the evidence chain
- run-level skill extraction must be executed after report generation, and the report/handoff record must reference `outputs/report/skill_extraction_summary.json`
- report/handoff records must reference skill-refresh/checkpoint compliance artifacts from `governance/skill_refresh_and_checkpointing.md`

Normalization relation to state in report:
- `norm_factor = (sigma_pb * k_factor * filter_eff * lumi_pb) / sumw`
- `w_final = w_event * norm_factor`

## Layer 2 — Workflow Contract
### Required Artifacts
- final report artifact in Markdown with the following sections in order:
  1. Introduction
  2. Data and Monte Carlo Samples
  3. Object Definition and Event Selection
  4. Overview of the Analysis Strategy
  5. Signal and Control Regions
  6. Cut Flow
  7. Distributions in Signal and Control Regions
  8. Systematic Uncertainties
  9. Statistical Interpretation
  10. Summary
  Appendix A: Agent Decisions and Deviations
  Appendix B: Monte Carlo Sample Selection Rationale
- Monte Carlo sample-table artifact within the report containing DSID, sample label, process, role (`signal`/`background`), generator, simulation configuration, cross section, k-factor, and filter efficiency
- MC sample-selection artifact at `outputs/report/mc_sample_selection.json`
- cut-flow table artifact with data counts and weighted simulated yields
- process-resolved cut-flow breakdown artifact (individual processes + combined signal/background totals)
- sample-resolved cut-flow breakdown artifact (individual MC samples), unless explicit merged-process configuration is requested
- embedded region-plot artifacts including blinded signal-region visualizations
- embedded pre-fit and post-fit non-signal-region plots
- embedded pre-fit and post-fit signal-region plots for unblinded analyses
- in blinded analyses, signal-region plotting artifact must explicitly declare whether SR is omitted or sensitive-window masked
- caption text for each embedded plot (entries + motivation/justification)
- statistical-summary artifact reporting expected sensitivity outputs produced before unblinding
- Asimov-provenance note in the statistical section when Asimov expected significance is reported
- explicit Asimov-hypothesis note (`mu_gen` and model used) when Asimov expected significance is reported
- H->gammagamma background-template note documenting:
  - selected nominal background sample and DSID
  - why that sample was chosen
  - sideband-normalization method
  - effective MC luminosity calculation
  - smoothing decision
- H->gammagamma background-function-selection note documenting:
  - target spurious-signal criterion
  - degree/complexity cap of `3`
  - whether the cap was reached
  - selected background function and its complexity
  - whether the selected function passed the criterion or was retained as the least-bad capped noncompliant choice
- H->gammagamma significance-fit policy note documenting:
  - blinded vs unblinded status
  - Asimov construction method
  - fixed signal-shape parameters
  - floating signal-strength/background parameters
  - expected-versus-observed significance distinction
- category mass-window yield-table artifact (expected signal/background per category at `125 +/- 2 GeV`)
- per-category diphoton mass-plot artifact set with stacked signal-over-background expectation
- agent-decision audit artifact in Appendix A with issue, decision, and justification for each deviation
- data-MC discrepancy artifacts:
  - `outputs/report/data_mc_discrepancy_audit.json`
  - `outputs/report/data_mc_check_log.json`
- post-run skill-extraction summary artifact at `outputs/report/skill_extraction_summary.json` (required even when no candidates are proposed)
- skill-refresh/checkpoint artifacts:
  - `outputs/report/skill_refresh_plan.json`
  - `outputs/report/skill_refresh_log.jsonl`
  - `outputs/report/skill_checkpoint_status.json`

### Acceptance Checks
- section headers exist and appear in required order
- report explicitly states metadata-driven MC normalization inputs and formula
- report states the luminosity value used in normalization and, for default central results, shows `36.1 fb^-1`
- sample table includes required Monte Carlo normalization columns, generator field, simulation-configuration field, and `signal/background` role field
- report clearly separates data-sample description from Monte Carlo-sample description and does not rely on file-name dumps
- report main body describes only central nominal/reference MC samples used in the actual yields and fits
- event-selection narrative is restricted to regions used in the log-likelihood fit and states each fit-region observable
- cut-flow presentation distinguishes per-process contributions from combined signal/background totals when multi-process signal/background is used
- for `H -> gamma gamma`, cut flow is reported separately for signal production modes, diphoton background MC, and data
- for `H -> gamma gamma`, MC statistical uncertainties in cut-flow and yield tables are derived from event weights rather than naive event counts
- cut-flow defaults to individual MC sample rows unless explicit merged-process instruction is provided by user/config
- report avoids central-yield double counting of nominal and alternative samples for the same physics process
- report embeds produced plots directly via markdown image tags instead of citation-only file lists
- each embedded plot has an adjacent caption sentence/paragraph explaining entries and motivation
- report explicitly states that blinding is default and records whether explicit unblinding was requested
- in blinded mode, signal-region data are hidden either by omitting SR observed-data plots or by explicit sensitive-window masking
- when blinded and sensitive-window masking is used, masked window boundaries are explicitly stated
- in unblinded mode, report plots show observed data across full signal regions
- non-signal-region pre-fit and post-fit comparisons are clearly identified and use visible data overlays
- when blinded category mass plots are used, data points are shown in sidebands and hidden in the blinded window unless explicit unblinding is requested
- report includes a category-wise `125 +/- 2 GeV` expected-yield table for signal and background
- report includes one diphoton-mass distribution per active category used in the combined fit
- systematics section contains explicit placeholder statement when systematics are unspecified
- statistical interpretation section documents Asimov/pre-unblinding treatment when blinding is active
- when Asimov significance is reported, the report explicitly distinguishes expected (Asimov) from observed significance and records generation provenance
- when Asimov discovery sensitivity is reported, the report explicitly documents `mu_gen = 1` signal-plus-background generation, the background-parameter source from the `mu = 0` fit, and full-range evaluation including the signal region
- for `H -> gamma gamma`, the report explicitly documents the nominal background sample choice, sideband normalization, effective MC luminosity calculation, and smoothing decision
- for `H -> gamma gamma`, the report explicitly documents the degree/complexity cap of `3` used in the spurious-signal scan and, when no candidate passes by that cap, clearly labels the selected background function as a capped noncompliant choice rather than a compliant pass
- for `H -> gamma gamma`, the report explicitly documents the Asimov construction method and the fixed-vs-floating parameter policy used in significance fits
- for `H -> gamma gamma`, the report explicitly states whether the analysis remained blinded or was explicitly unblinded
- statistical interpretation section states the backend used for the reported fit/significance numbers and confirms `pyroot_roofit` is primary for H->gammagamma
- report does not present non-ROOT H->gammagamma numbers as primary results; if only cross-check numbers exist, this is explicitly labeled and central claim is blocked
- Appendix A exists and contains at least one structured entry whenever substitutions/deviations occurred
- Appendix B exists and explains the nominal/reference MC sample choice per central physics process, including rejected or alternative candidates
- `outputs/report/mc_sample_selection.json` exists, is readable, and is consistent with the report's main-body sample discussion
- report (or linked handoff note) references data-MC discrepancy status from `outputs/report/data_mc_discrepancy_audit.json`
- report (or linked handoff note) references `outputs/report/skill_extraction_summary.json` with its status (`none_found` or `candidates_created`)
- report (or linked handoff note) references `outputs/report/skill_checkpoint_status.json` with its status (`pass` or `fail`)

## Layer 3 — Example Implementation
### Output Location (Current Repository Workflow)
- `reports/final_analysis_report.md`

### Inputs to Reference (Current Repository Workflow)
- analysis summary specification
- region definitions
- metadata table for open-data sample normalization
- cut-flow, yield, fit, significance, and blinding artifacts produced by pipeline stages

### Related Skills
- `core_pipeline/sample_registry_and_normalization.md`
- `governance/mc_sample_disambiguation_and_nominal_selection.md`
- `physics_facts/mc_normalization_metadata_stacking.md`
- `core_pipeline/plotting_and_report.md`
- `analysis_strategy/control_region_signal_region_blinding_and_visualization.md`
- `core_pipeline/profile_likelihood_significance.md`
- `core_pipeline/final_report_review_and_handoff.md`
- `meta/extract_new_skill_from_failure.md`
- `governance/skill_refresh_and_checkpointing.md`

### Example Generation Path (Current Repository Workflow)
- generate a baseline report from pipeline report stage
- enrich/reshape to match this final section structure
- write final artifact to `reports/final_analysis_report.md`

# Examples

Example invocation context:
- Run this contract in the declared stage using the required inputs and dependencies.

Example expected outputs:
- `outputs/report/skill_extraction_summary.json`
- `outputs/report/mc_sample_selection.json`
- `outputs/report/data_mc_discrepancy_audit.json`
- `outputs/report/data_mc_check_log.json`
- `outputs/report/skill_refresh_plan.json`
- `outputs/report/skill_refresh_log.jsonl`
- `outputs/report/skill_checkpoint_status.json`
