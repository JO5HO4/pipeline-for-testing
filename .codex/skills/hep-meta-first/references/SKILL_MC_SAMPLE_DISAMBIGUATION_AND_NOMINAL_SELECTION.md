---
skill_id: SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION
display_name: "MC Sample Disambiguation and Nominal Selection"
version: 1.0
category: validation

summary: "When multiple MC datasets can represent the same nominal physics process, the agent must identify one unique central sample set per process before computing central yields or building the statistical model."

invocation_keywords:
  - "mc sample disambiguation and nominal selection"
  - "validation"
  - "sample"
  - "disambiguation"
  - "nominal"
  - "selection"

when_to_use:
  - "Use when executing or validating the validation stage of the analysis workflow."
  - "Use when this context is available: available MC file inventory."
  - "Use when this context is available: sample registry with file paths and dataset names."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: available_mc_file_inventory
      type: artifact
      description: "available MC file inventory"
    - name: sample_registry_with_file_paths_and_dataset_names
      type: artifact
      description: "sample registry with file paths and dataset names"
    - name: analysis_objective_and_target_final_state
      type: artifact
      description: "analysis objective and target final state"
    - name: prior_reports_or_notes_describing_intended_signal_background_def
      type: artifact
      description: "prior reports or notes describing intended signal/background definitions"

  optional:
    - name: open_data_metadata_tables_when_available
      type: artifact
      description: "open-data metadata tables when available"

outputs:
  - name: mc_sample_disambiguation_artifact_at_outputs_report_mc_sample_se
    type: artifact
    description: "MC sample disambiguation artifact at `outputs/report/mc_sample_selection.json` containing:"
  - name: status
    type: artifact
    description: "`status` (`resolved` or `blocked`)"
  - name: analysis_target
    type: artifact
    description: "`analysis_target`"
  - name: processes
    type: artifact
    description: "`processes` (list of per-process decisions)"
  - name: ambiguous_processes
    type: artifact
    description: "`ambiguous_processes` (list)"
  - name: human_clarifications
    type: artifact
    description: "`human_clarifications` (list)"
  - name: notes
    type: artifact
    description: "`notes`"
  - name: per_process_entries_in_processes_containing
    type: artifact
    description: "per-process entries in `processes` containing:"
  - name: process_key
    type: artifact
    description: "`process_key`"
  - name: analysis_role
    type: artifact
    description: "`analysis_role`"
  - name: selected_nominal_samples
    type: artifact
    description: "`selected_nominal_samples`"
  - name: alternative_samples
    type: artifact
    description: "`alternative_samples`"
  - name: excluded_samples
    type: artifact
    description: "`excluded_samples`"
  - name: selection_basis
    type: artifact
    description: "`selection_basis`"

preconditions:
  - "Dependency SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION

  may_follow:
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
    - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
    - SKILL_MC_NORMALIZATION_METADATA_STACKING
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
  - "writes mc_sample_disambiguation_artifact_at_outputs_report_mc_sample_se"
  - "writes status"
  - "writes analysis_target"
  - "writes processes"
  - "writes ambiguous_processes"
  - "writes human_clarifications"
  - "writes notes"
  - "writes per_process_entries_in_processes_containing"
  - "writes process_key"
  - "writes analysis_role"

failure_modes:
  - "ambiguous nominal choices block execution until clarified by a human"

validation_checks:
  - "each central physics process has exactly one nominal/reference sample set"
  - "central-yield and fit inputs exclude alternative or non-matching-decay samples unless an explicit policy says otherwise"
  - "for H->gammagamma spurious-signal/background-function studies, the nominal background-template source is the default diphoton MC sample rather than a combination of many low-statistics auxiliary background samples"
  - "for H->gammagamma spurious-signal/background-function studies, the selected diphoton nominal sample window is the minimum available mass window that fully contains `105-160 GeV`"
  - "resonance-background slice selection documents fit-range coverage and blocks if relevance/coverage cannot be verified"
  - "sample-selection logic relies on physics-meaning tokens and metadata, not simple index ordering"
  - "ambiguous nominal choices block execution until clarified by a human"
  - "final report main body discusses the samples used, while the appendix explains why those samples were selected over other available files"

handoff_to:
  - SKILL_CUT_FLOW_AND_YIELDS
  - SKILL_SYSTEMATICS_AND_NUISANCES
  - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
  - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
  - SKILL_MC_NORMALIZATION_METADATA_STACKING
  - SKILL_FULL_STATISTICS_EXECUTION_POLICY
---

# Purpose

This skill defines a structured execution contract for `governance/mc_sample_disambiguation_and_nominal_selection.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. Enumerate all candidate MC files relevant to the target process family.
2. Group candidates by physics meaning, not by filename order:
3. production mode
4. decay/final state
5. generator / shower / PDF implementation
6. For resonance-search mass-fit workflows, determine the fit mass interval and map candidate background datasets/slices to that interval.
7. Reject candidates whose final state does not match the central analysis target unless they are explicitly designated as alternative or cross-check samples.
8. For resonance-search mass-fit workflows, exclude out-of-range background slices from central templates unless an explicit policy justifies inclusion.
9. For each physics process, identify one nominal/reference sample set for central yields and fits.
10. If two or more candidates remain equally plausible and the repository context does not resolve them, block and request human clarification.
11. Record the chosen nominal sample set and the rejected/alternative candidates with justification.

# Notes

- Source file: `governance/mc_sample_disambiguation_and_nominal_selection.md`
- Original stage: `validation`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: MC Sample Disambiguation and Nominal Selection

## Layer 1 — Physics Policy
When multiple MC datasets can represent the same nominal physics process, the agent must identify one unique central sample set per process before computing central yields or building the statistical model.

Policy requirements:
- inspect all available MC candidates before assigning central signal/background sample sets
- define a stable physics-process key that separates production mode, decay/final state, and analysis role
- use semantically meaningful dataset-name tokens and metadata to identify candidates, especially:
  - generator
  - parton shower / hadronization configuration
  - PDF / tune markers
  - decay or final-state markers
- do not use simple numeric indexing alone (for example `001`, `002`, `v1`, `v2`) as evidence that two datasets are physically distinct or ordered
- for a decay-specific analysis, central signal samples must match the targeted decay/final state exactly
- inclusive-Higgs samples or Higgs samples for other decays must not enter central `H -> gamma gamma` signal yields unless an explicit and justified combination policy is declared
- for resonance-search analyses with an explicit mass-fit observable (for example `H -> gamma gamma`), central background MC must be restricted to samples/slices that are relevant to the fitted mass range
- for `H -> gamma gamma`, the nominal background-template source used by the spurious-signal/background-function workflow must be the default diphoton Monte Carlo sample in the minimum available generated-mass window that fully contains `105-160 GeV`
- for `H -> gamma gamma`, the agent must not construct the nominal background template by combining many relevant but individually low-statistics auxiliary background samples; this prior failure mode inflates statistical fluctuations and degrades the spurious-signal test
- low-statistics auxiliary background samples may be retained only as alternatives, cross-checks, or excluded samples; they must not silently enter the nominal spurious-signal template
- when background datasets are provided in mass slices, central templates must include only slices that overlap the fit range (optionally with a documented safety buffer); for `H -> gamma gamma`, the nominal-template rule above is stricter and overrides generic slice aggregation
- if mass-range relevance or slice coverage is unclear, or if selected slices do not provide adequate support for the fit interval, execution must block until a human-approved policy is recorded
- when multiple plausible candidates remain for one process, select one nominal/reference dataset and mark the rest as alternatives, cross-checks, or systematic-only inputs
- if the meaning of candidate samples or the nominal choice is ambiguous, stop and ask the human before execution continues
- record the human clarification and selection rationale in machine-readable artifacts and in the final report appendix

## Layer 2 — Workflow Contract
### Inputs
- available MC file inventory
- sample registry with file paths and dataset names
- open-data metadata tables when available
- analysis objective and target final state
- prior reports or notes describing intended signal/background definitions

### Required Artifacts
- MC sample disambiguation artifact at `outputs/report/mc_sample_selection.json` containing:
  - `status` (`resolved` or `blocked`)
  - `analysis_target`
  - `processes` (list of per-process decisions)
  - `ambiguous_processes` (list)
  - `human_clarifications` (list)
  - `notes`
- per-process entries in `processes` containing:
  - `process_key`
  - `analysis_role`
  - `selected_nominal_samples`
  - `alternative_samples`
  - `excluded_samples`
  - `fit_mass_range` (or `not_applicable`)
  - `selected_mass_relevant_samples`
  - `excluded_out_of_range_samples`
  - `mass_range_relevance_status` (`verified`, `not_applicable`, or `blocked`)
  - `nominal_background_template_policy` (`default_diphoton_minimum_window`, `not_applicable`, or `blocked`)
  - `selected_nominal_background_template_sample`
  - `selected_nominal_background_template_mass_window`
  - `rejected_low_statistics_auxiliary_background_samples`
  - `selection_failure_mode_avoided`
  - `selection_basis`
  - `ambiguity_status`
  - `requires_human_clarification`
- final report appendix section documenting why each nominal sample set was chosen from the available candidates

### Decision Procedure
1. Enumerate all candidate MC files relevant to the target process family.
2. Group candidates by physics meaning, not by filename order:
   - production mode
   - decay/final state
   - generator / shower / PDF implementation
3. For resonance-search mass-fit workflows, determine the fit mass interval and map candidate background datasets/slices to that interval.
4. Reject candidates whose final state does not match the central analysis target unless they are explicitly designated as alternative or cross-check samples.
5. For `H -> gamma gamma` spurious-signal/background-function studies, identify the default diphoton MC candidates and select the smallest available generated-mass window that fully contains `105-160 GeV`.
6. For `H -> gamma gamma`, explicitly reject the construction of the nominal background template from many relevant but individually low-statistics auxiliary samples; record those samples as rejected or alternative and explain that this avoids inflated statistical fluctuations in the spurious-signal test.
7. For other resonance-search mass-fit workflows, exclude out-of-range background slices from central templates unless an explicit policy justifies inclusion.
8. For each physics process, identify one nominal/reference sample set for central yields and fits.
9. If two or more candidates remain equally plausible and the repository context does not resolve them, block and request human clarification.
10. Record the chosen nominal sample set and the rejected/alternative candidates with justification.

### Acceptance Checks
- each central physics process has exactly one nominal/reference sample set
- central-yield and fit inputs exclude alternative or non-matching-decay samples unless an explicit policy says otherwise
- for `H -> gamma gamma` spurious-signal/background-function studies, the nominal background-template source is the default diphoton MC sample rather than a combination of many low-statistics auxiliary background samples
- for `H -> gamma gamma`, the selected diphoton nominal sample window is the minimum available mass window that fully contains `105-160 GeV`
- resonance-background slice selection documents fit-range coverage and blocks if relevance/coverage cannot be verified
- sample-selection logic relies on physics-meaning tokens and metadata, not simple index ordering
- ambiguous nominal choices block execution until clarified by a human
- final report main body discusses the samples used, while the appendix explains why those samples were selected over other available files

## Layer 3 — Example Implementation
### Recommended `mc_sample_selection.json` Shape
```json
{
  "status": "resolved",
  "analysis_target": "pp -> H -> gamma gamma",
  "processes": [
    {
      "process_key": "ggF_Hyy",
      "analysis_role": "signal_nominal",
      "selected_nominal_samples": ["343981"],
      "alternative_samples": ["346797"],
      "excluded_samples": ["345060", "345097"],
      "fit_mass_range": [105.0, 160.0],
      "selected_mass_relevant_samples": ["343981"],
      "excluded_out_of_range_samples": [],
      "mass_range_relevance_status": "verified",
      "selection_basis": [
        "matches H->gammagamma target final state",
        "Powheg+Pythia8 nominal over alternative Herwig shower sample"
      ],
      "ambiguity_status": "resolved",
      "requires_human_clarification": false
    }
  ],
  "ambiguous_processes": [],
  "human_clarifications": [],
  "notes": []
}
```

### Related Skills
- `governance/agent_pre_flight_fact_check.md`
- `core_pipeline/sample_registry_and_normalization.md`
- `physics_facts/mc_normalization_metadata_stacking.md`
- `core_pipeline/final_analysis_report_agent_workflow.md`

# Examples

Example invocation context:
- Run this contract in the declared stage using the required inputs and dependencies.

Example expected outputs:
- `outputs/report/mc_sample_selection.json`
