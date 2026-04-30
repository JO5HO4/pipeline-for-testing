---
skill_id: SKILL_SKILLS_PACK_INDEX
display_name: "Skills Repository (Semantic Structure)"
version: 1.0
category: other

summary: "The analysis skill pack must encode a complete, scientifically coherent HEP workflow from analysis definition to statistical interpretation."

invocation_keywords:
  - "readme"
  - "skills repository (semantic structure)"
  - "other"
  - "skills"
  - "repository"
  - "semantic"
  - "structure"

when_to_use:
  - "Use when executing or validating the other stage of the analysis workflow."
  - "Use when this context is available: Analysis summary JSON: `analysis/<analysis>.analysis.json`."
  - "Use when this context is available: Samples: `inputs/` (or a provided path)."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: analysis_summary_json_analysis_analysis_analysis_json
      type: artifact
      description: "Analysis summary JSON: `analysis/<analysis>.analysis.json`"
    - name: samples_inputs
      type: artifact
      description: "Samples: `inputs/` (or a provided path)"
    - name: output_directory_outputs
      type: artifact
      description: "Output directory: `outputs/`"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: normalized_analysis_definition_artifact_with_validated_region_an
    type: artifact
    description: "normalized analysis-definition artifact with validated region and fit semantics"
  - name: spec_to_runtime_mapping_artifact
    type: artifact
    description: "spec-to-runtime mapping artifact (required when runtime pipeline is not fully JSON-native)"
  - name: deviations_from_spec_artifact_with_explicit_substitutions_assump
    type: artifact
    description: "deviations-from-spec artifact with explicit substitutions/assumptions"
  - name: sample_classification_and_normalization_artifact
    type: artifact
    description: "sample-classification and normalization artifact"
  - name: process_role_and_nominal_vs_alternative_sample_mapping_artifacts
    type: artifact
    description: "process-role and nominal-vs-alternative sample mapping artifacts for context-dependent signal/background definitions"
  - name: mc_sample_disambiguation_and_nominal_selection_artifact_for_proc
    type: artifact
    description: "MC sample disambiguation and nominal-selection artifact for processes with multiple candidate datasets"
  - name: open_data_metadata_driven_normalization_artifact_for_multi_compo
    type: artifact
    description: "open-data metadata-driven normalization artifact for multi-component MC stacking (when this workflow is used)"
  - name: signal_background_strategy_artifact_including_control_to_signal_
    type: artifact
    description: "signal/background strategy artifact including control-to-signal normalization intent"
  - name: category_region_partition_specification_artifact
    type: artifact
    description: "category/region partition specification artifact (category axis x region axis)"
  - name: partition_completeness_exclusivity_check_artifact
    type: artifact
    description: "partition completeness/exclusivity check artifact"
  - name: partition_manifest_artifact_for_downstream_stages
    type: artifact
    description: "partition manifest artifact for downstream stages"
  - name: region_selection_artifact_with_cut_flow_and_yield_summaries
    type: artifact
    description: "region-selection artifact with cut flow and yield summaries"
  - name: process_resolved_cut_flow_artifact
    type: artifact
    description: "process-resolved cut-flow artifact (individual process contributions plus combined signal/background totals)"
  - name: region_overlap_audit_artifact_documenting_sr_cr_overlap_checks_a
    type: artifact
    description: "region-overlap audit artifact documenting SR/CR overlap checks and any explicit exceptions"

preconditions:
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_SKILLS_PACK_INDEX are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - NONE

  may_follow:
    - SKILL_EXTRACT_NEW_SKILL_FROM_FAILURE
    - SKILL_BOOTSTRAP_REPO
    - SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR
    - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
    - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION
    - SKILL_SKILL_REFRESH_AND_CHECKPOINTING
    - SKILL_JSON_SPEC_DRIVEN_EXECUTION
    - SKILL_FULL_STATISTICS_EXECUTION_POLICY
    - SKILL_READ_SUMMARY_AND_VALIDATE
    - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
    - SKILL_MC_NORMALIZATION_METADATA_STACKING
    - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
    - SKILL_EVENT_IO_AND_COLUMNAR_MODEL
    - SKILL_OBJECT_DEFINITIONS
    - SKILL_SELECTION_ENGINE_AND_REGIONS
    - SKILL_CUT_FLOW_AND_YIELDS
    - SKILL_HISTOGRAMMING_AND_TEMPLATES
    - SKILL_FREEZE_ANALYSIS_HISTOGRAM_PRODUCTS
    - SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION
    - SKILL_SYSTEMATICS_AND_NUISANCES
    - SKILL_WORKSPACE_AND_FIT_PYHF
    - SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB
    - SKILL_PLOTTING_AND_REPORT
    - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
    - SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION
    - SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY
    - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
    - SKILL_CATEGORY_CHANNEL_REGION_PARTITIONING
    - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF
    - SKILL_VISUAL_VERIFICATION
    - SKILL_HISTOGRAM_PLOTTING_INVARIANTS
    - SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK
    - SKILL_ROOTMLTOOL_CACHED_ANALYSIS
    - SKILL_STATTOOL_OPTIONAL_PYHF_BACKEND

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
  - "writes normalized_analysis_definition_artifact_with_validated_region_an"
  - "writes spec_to_runtime_mapping_artifact"
  - "writes deviations_from_spec_artifact_with_explicit_substitutions_assump"
  - "writes sample_classification_and_normalization_artifact"
  - "writes process_role_and_nominal_vs_alternative_sample_mapping_artifacts"
  - "writes mc_sample_disambiguation_and_nominal_selection_artifact_for_proc"
  - "writes open_data_metadata_driven_normalization_artifact_for_multi_compo"
  - "writes signal_background_strategy_artifact_including_control_to_signal_"
  - "writes category_region_partition_specification_artifact"
  - "writes partition_completeness_exclusivity_check_artifact"

failure_modes:
  - "H->gammagamma runs with unresolved mandatory backend constraints are marked blocked/failed rather than completed with backend substitution"
  - "each central physics process with multiple candidate datasets has exactly one recorded nominal/reference selection, or the run is blocked pending clarification"
  - "if missing-but-buildable pipeline/tooling was detected, run artifacts include evidence of runtime construction and full-sample completion before handoff-ready status"

validation_checks:
  - "all pipeline-stage artifacts exist and are readable by downstream stages"
  - "each run references an explicit analysis JSON path"
  - "each declared fit has a fit-result artifact and significance artifact"
  - "each declared fit has an explicit backend declaration and backend-consistent diagnostics"
  - "each H->gammagamma fit declares `pyroot_roofit` as the primary backend"
  - "each H->gammagamma primary fit/significance claim is backed by RooFit analytic-function artifacts; non-ROOT artifacts, if present, are labeled cross-check-only"
  - "H->gammagamma runs with unresolved mandatory backend constraints are marked blocked/failed rather than completed with backend substitution"
  - "ROOT event-ingestion path is `uproot`-based unless an explicit, justified exception is recorded"
  - "region-level histograms, yields, and cut flows are mutually consistent within tolerance"
  - "signal and control regions used together in a fit are mutually exclusive at event level unless an explicit, justified overlap exception is declared"
  - "blinding metadata confirms signal-region data handling policy"
  - "required verification plots are present"
  - "substantial data-MC discrepancies are explicitly reported and not cosmetically tuned away"
  - "`outputs/report/data_mc_discrepancy_audit.json` exists, is readable, and declares `status` in `{no_substantial_discrepancy, discrepancy_investigated_bug_found, discrepancy_investigated_no_bug_found}`"

handoff_to:
  - SKILL_BOOTSTRAP_REPO
  - SKILL_AGENT_PRE_FLIGHT_FACT_CHECK
  - SKILL_EXTRACT_NEW_SKILL_FROM_FAILURE
  - SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR
  - SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION
  - SKILL_SKILL_REFRESH_AND_CHECKPOINTING
  - SKILL_JSON_SPEC_DRIVEN_EXECUTION
  - SKILL_FULL_STATISTICS_EXECUTION_POLICY
  - SKILL_READ_SUMMARY_AND_VALIDATE
  - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
  - SKILL_MC_NORMALIZATION_METADATA_STACKING
  - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
  - SKILL_EVENT_IO_AND_COLUMNAR_MODEL
  - SKILL_OBJECT_DEFINITIONS
  - SKILL_SELECTION_ENGINE_AND_REGIONS
  - SKILL_CUT_FLOW_AND_YIELDS
  - SKILL_HISTOGRAMMING_AND_TEMPLATES
  - SKILL_FREEZE_ANALYSIS_HISTOGRAM_PRODUCTS
  - SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION
  - SKILL_SYSTEMATICS_AND_NUISANCES
  - SKILL_WORKSPACE_AND_FIT_PYHF
  - SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB
  - SKILL_PLOTTING_AND_REPORT
  - SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW
  - SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION
  - SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY
  - SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE
  - SKILL_CATEGORY_CHANNEL_REGION_PARTITIONING
  - SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF
  - SKILL_VISUAL_VERIFICATION
  - SKILL_HISTOGRAM_PLOTTING_INVARIANTS
  - SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK
  - SKILL_ROOTMLTOOL_CACHED_ANALYSIS
  - SKILL_STATTOOL_OPTIONAL_PYHF_BACKEND
---

# Purpose

This skill defines a structured execution contract for `README.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `README.md`
- Original stage: `other`
- Logic type classification: `engineering`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._

# Skills Repository (Semantic Structure)

This README replaces `00_INDEX.md` and serves as the top-level navigator for the refactored skills tree.

## Directory Layout
- `core_pipeline/`: end-to-end procedural analysis workflow stages
- `analysis_strategy/`: analysis-design and strategy decisions
- `physics_facts/`: domain facts and invariant technical rules
- `governance/`: policy and integrity guardrails
- `infrastructure/`: operational support, caching, and reproducibility
- `meta/`: skill-lifecycle governance
- `interfaces/`: translation/execution interfaces (JSON and narrative)
- `open_data_specific/`: dataset-release-specific references

## Legacy Index Content (Refactored Paths)

# Skill: Skills Pack Index

## Layer 1 — Physics Policy
The analysis skill pack must encode a complete, scientifically coherent HEP workflow from analysis definition to statistical interpretation.

Core policy requirements:
- Keep analysis decisions config-driven and reproducible.
- Start execution from a referenced analysis JSON file; trigger prompts should be minimal and JSON-first.
- Preserve a clear chain from event selection through statistical inference.
- Treat signal and background modeling choices as explicit methodological choices.
- Process ROOT ntuples with `uproot` as the default event-ingestion backend.
- For the default Run-2 H->gammagamma workflow in this repository, central MC normalization must use `lumi_fb = 36.1`.
- For H->gammagamma resonance analyses in this repository, analytic-function fits in `pyroot_roofit` are the mandatory primary path for mass fits and significance.
- For H->gammagamma production workflows, PyROOT must be installed/importable before fit and significance stages begin.
- If the mandatory H->gammagamma RooFit analytic path is unavailable, execution is blocked for primary results (fail-closed; no automatic primary-backend substitution).
- Non-ROOT backends may be used only as explicitly labeled cross-checks and must not replace primary fit/significance artifacts.
- Never replace existing workflow implementations when adding tools from other projects; keep new tools as additive, selectable options.
- At run start and before handoff, perform a skill-compliance audit of existing code/configuration; if non-compliant, force targeted rewrites of the owning pipeline components before completion.
- If a functioning analysis pipeline or required tooling is missing but can be built in-repository, construct it as part of the task rather than stopping at placeholder-only outputs.
- Enforce blinding where required by the analysis strategy.
- Require visual and statistical validation before declaring completion.
- Require execution of post-run skill extraction (`meta/extract_new_skill_from_failure.md`) for every completed run; missing extraction blocks handoff-ready status.
- Use the term **cut flow** consistently.
- Default production runs must use full statistics unless partial scope is explicitly requested or a same-task fast-test then full-run pattern is declared.
- Require skill-refresh/checkpoint governance during execution; missing refresh/checkpoint artifacts block handoff-ready status.

## Layer 2 — Workflow Contract
### Required Artifacts
- normalized analysis-definition artifact with validated region and fit semantics
- spec-to-runtime mapping artifact (required when runtime pipeline is not fully JSON-native)
- deviations-from-spec artifact with explicit substitutions/assumptions
- sample-classification and normalization artifact
- process-role and nominal-vs-alternative sample mapping artifacts for context-dependent signal/background definitions
- MC sample disambiguation and nominal-selection artifact for processes with multiple candidate datasets
- open-data metadata-driven normalization artifact for multi-component MC stacking (when this workflow is used)
- signal/background strategy artifact including control-to-signal normalization intent
- category/region partition specification artifact (category axis x region axis)
- partition completeness/exclusivity check artifact
- partition manifest artifact for downstream stages
- region-selection artifact with cut flow and yield summaries
- process-resolved cut-flow artifact (individual process contributions plus combined signal/background totals)
- region-overlap audit artifact documenting SR/CR overlap checks and any explicit exceptions
- histogram-template artifact for fit observables
- signal-shape and background-model-selection artifacts when analytic mass modeling is used
- category-resolved RooFit artifacts for the H->gammagamma analytic resonance workflow (per-category DS-CB parameters, sideband-fit parameters, blinded category mass plots, and mass-window expected-yield table)
- systematic-uncertainty artifact
- statistical-workspace artifact and per-fit result artifacts
- fit-backend declaration artifact per fit with `pyroot_roofit` primary-backend provenance and any optional cross-check backend notes
- discovery-significance artifact per fit
- optional Asimov expected-significance artifact per fit with generation provenance
- Asimov sensitivity artifacts should document full-range generation/evaluation and tested generation hypothesis (for expected discovery sensitivity: `mu_gen = 1` with background-shape parameters sourced from a `mu = 0` data fit)
- blinding-summary artifact and blinded region-visualization artifact set
- visual-verification artifact set for required diagnostics
- data-MC discrepancy artifacts (`outputs/report/data_mc_discrepancy_audit.json`, `outputs/report/data_mc_check_log.json`) for every run, including zero-discrepancy runs
- narrative analysis report artifact
- final publication-style report artifact with agent decision appendix
- skill-extraction summary artifact at `outputs/report/skill_extraction_summary.json` (required even when no candidates are found)
- skill-refresh plan artifact at `outputs/report/skill_refresh_plan.json`
- skill-refresh event log artifact at `outputs/report/skill_refresh_log.jsonl`
- skill-checkpoint status artifact at `outputs/report/skill_checkpoint_status.json`
- skill-compliance gap artifact at `outputs/report/skill_compliance_gaps.json`
- skill-compliance rewrite-plan artifact at `outputs/report/skill_compliance_rewrite_plan.json`

### Acceptance Checks
- all pipeline-stage artifacts exist and are readable by downstream stages
- each run references an explicit analysis JSON path
- each declared fit has a fit-result artifact and significance artifact
- each declared fit has an explicit backend declaration and backend-consistent diagnostics
- each H->gammagamma fit declares `pyroot_roofit` as the primary backend
- each H->gammagamma primary fit/significance claim is backed by RooFit analytic-function artifacts; non-ROOT artifacts, if present, are labeled cross-check-only
- H->gammagamma runs with unresolved mandatory backend constraints are marked blocked/failed rather than completed with backend substitution
- ROOT event-ingestion path is `uproot`-based unless an explicit, justified exception is recorded
- region-level histograms, yields, and cut flows are mutually consistent within tolerance
- signal and control regions used together in a fit are mutually exclusive at event level unless an explicit, justified overlap exception is declared
- blinding metadata confirms signal-region data handling policy
- required verification plots are present
- substantial data-MC discrepancies are explicitly reported and not cosmetically tuned away
- `outputs/report/data_mc_discrepancy_audit.json` exists, is readable, and declares `status` in `{no_substantial_discrepancy, discrepancy_investigated_bug_found, discrepancy_investigated_no_bug_found}`
- `outputs/report/data_mc_check_log.json` exists and is readable
- final report summarizes selection, modeling, fit, significance, and implementation differences
- partition checks confirm category coverage/exclusivity and unique `(category, region)` keys
- central yields/cut flows do not double count physics processes represented by both nominal and alternative MC samples
- each central physics process with multiple candidate datasets has exactly one recorded nominal/reference selection, or the run is blocked pending clarification
- if missing-but-buildable pipeline/tooling was detected, run artifacts include evidence of runtime construction and full-sample completion before handoff-ready status
- `outputs/report/skill_extraction_summary.json` exists, is readable, and has `status` in `{none_found, candidates_created}`
- `outputs/report/skill_refresh_plan.json` exists and is readable
- `outputs/report/skill_refresh_log.jsonl` exists and is readable
- `outputs/report/skill_checkpoint_status.json` exists, is readable, and has `status = pass` for handoff-ready runs

## Layer 3 — Example Implementation
### Required Inputs (Current Repository)
- Analysis summary JSON: `analysis/<analysis>.analysis.json`
- Samples: `inputs/` (or a provided path)
- Output directory: `outputs/`

### Minimum Outputs (Current Repository)
- `outputs/cutflows/*.json`
- `outputs/cutflows_process_breakdown.json` (or equivalent process-resolved cut-flow artifact)
- `outputs/yields/*.json`
- `outputs/hists/**/*.npz` (or ROOT, but be consistent)
- `outputs/fit/*/results.json`
- `outputs/fit/*/significance.json`
- `outputs/background_modeling_strategy.json`
- `outputs/samples.classification.json`
- `outputs/report/mc_sample_selection.json`
- `outputs/cr_sr_constraint_map.json`
- `outputs/report/partition_spec.json`
- `outputs/report/partition_checks.json`
- `outputs/manifest/partitions.json`
- `outputs/fit/*/signal_pdf.json`
- `outputs/fit/*/background_pdf_scan.json`
- `outputs/fit/*/background_pdf_choice.json`
- `outputs/fit/*/spurious_signal.json`
- `outputs/fit/*/blinded_cr_fit.json`
- `outputs/fit/*/roofit_combined/significance.json` (required for H->gammagamma workflows)
- `outputs/fit/*/roofit_combined/signal_dscb_parameters.json` (required for H->gammagamma workflows)
- `outputs/fit/*/roofit_combined/sideband_fit_parameters.json` (required for H->gammagamma workflows)
- `outputs/fit/*/roofit_combined/cutflow_mass_window_125pm2.json` (required for H->gammagamma workflows)
- `outputs/report/plots/roofit_combined_mgg_*.png` (required for H->gammagamma workflows)
- `outputs/report/blinding_summary.json`
- `outputs/report/plots/blinded_region_*.png`
- `outputs/report/report.md`
- `outputs/report/*.png`
- `outputs/report/data_mc_discrepancy_audit.json`
- `outputs/report/data_mc_check_log.json`
- `outputs/report/skill_extraction_summary.json`
- `outputs/report/skill_refresh_plan.json`
- `outputs/report/skill_refresh_log.jsonl`
- `outputs/report/skill_checkpoint_status.json`

### Canonical Pipeline Stages (Current Repository)
1. Optional: convert narrative analysis text into structured analysis JSON and produce a gap report.
2. Run agent pre-flight fact check and resolve critical ambiguities.
3. Initialize skill-refresh/checkpoint plan and execute refresh checkpoints at phase boundaries, elapsed-time intervals, and failure-recovery boundaries.
4. Parse and validate summary JSON.
5. Apply JSON-spec-driven execution contract (including runtime mapping/deviation logging).
6. Build sample registry.
7. Resolve MC sample disambiguation and nominal/reference sample selection for central yields and fits.
8. Build metadata-driven MC normalization factors for stacked components (when metadata workflow is used).
9. Build category/region partition specification, checks, and manifest.
10. Build signal/background strategy and CR/SR normalization map.
11. Ingest events.
12. Build objects.
13. Apply selections and region masks.
14. Produce cut flow and yields.
15. Produce histograms for fit observables.
16. Build signal/background mass-shape models and run spurious-signal model selection.
17. Build statistical model and run fits.
18. Compute discovery significance from profile likelihood ratio.
19. Produce blinded CR/SR visualization products.
20. Make plots and report.
21. Run smoke tests.
22. Run final report review and handoff assessment (including skill-refresh/checkpoint gate).
23. Mandatory: run extract-new-skill-from-failure assessment and write any proposals to `candidate_skills/`, plus `outputs/report/skill_extraction_summary.json` even when zero candidates are created.

### Skill List (Current Repository)
Core pipeline skills:
- `core_pipeline/bootstrap_repo.md`
- `interfaces/narrative_to_analysis_json_translator.md`
- `governance/agent_pre_flight_fact_check.md`
- `governance/mc_sample_disambiguation_and_nominal_selection.md`
- `governance/skill_refresh_and_checkpointing.md`
- `interfaces/json_spec_driven_execution.md`
- `governance/full_statistics_execution_policy.md`
- `core_pipeline/read_summary_and_validate.md`
- `core_pipeline/sample_registry_and_normalization.md`
- `physics_facts/mc_normalization_metadata_stacking.md`
- `analysis_strategy/signal_background_strategy_and_cr_constraints.md`
- `core_pipeline/event_io_and_columnar_model.md`
- `physics_facts/object_definitions.md`
- `core_pipeline/selection_engine_and_regions.md`
- `core_pipeline/cut_flow_and_yields.md`
- `core_pipeline/histogramming_and_templates.md`
- `infrastructure/freeze_analysis_histogram_products.md`
- `analysis_strategy/signal_shape_and_spurious_signal_model_selection.md`
- `core_pipeline/systematics_and_nuisances.md`
- `core_pipeline/workspace_and_fit_pyhf.md`
- `core_pipeline/asimov_expected_significance_splusb.md`
- `core_pipeline/plotting_and_report.md`
- `core_pipeline/final_analysis_report_agent_workflow.md`
- `analysis_strategy/control_region_signal_region_blinding_and_visualization.md`
- `infrastructure/smoke_tests_and_reproducibility.md`
- `core_pipeline/profile_likelihood_significance.md`
- `analysis_strategy/category_channel_region_partitioning.md`
- `core_pipeline/final_report_review_and_handoff.md`
- `meta/extract_new_skill_from_failure.md`

Verification skills:
- `infrastructure/visual_verification.md`
- `physics_facts/histogram_plotting_invariants.md`
- `governance/data_mc_discrepancy_sanity_check.md`
- `infrastructure/rootmltool_cached_analysis.md`
- `infrastructure/stattool_optional_pyhf_backend.md`

# Examples

Example invocation context:
- Run this contract in the declared stage using the required inputs and dependencies.

Example expected outputs:
- `outputs/report/data_mc_discrepancy_audit.json`
- `outputs/report/data_mc_check_log.json`
- `outputs/report/skill_extraction_summary.json`
- `outputs/report/skill_refresh_plan.json`
- `outputs/report/skill_refresh_log.jsonl`
- `outputs/report/skill_checkpoint_status.json`
- `outputs/cutflows/`
- `outputs/cutflows_process_breakdown.json`
