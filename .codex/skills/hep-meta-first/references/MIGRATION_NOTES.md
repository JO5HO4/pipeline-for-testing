# Migration Notes: `skills/` -> `newskills/`

## Mapping Summary

Each original markdown source under `skills/` was transformed into one structured contract in `newskills/` with the schema requested by the refactor task.

| Original Source | Structured Contract | Notes |
|---|---|---|
| `README.md` | `newskills/SKILL_SKILLS_PACK_INDEX.md` | Repository index converted into contract-form index skill |
| `analysis_strategy/category_channel_region_partitioning.md` | `newskills/SKILL_CATEGORY_CHANNEL_REGION_PARTITIONING.md` | 1:1 mapping |
| `analysis_strategy/control_region_signal_region_blinding_and_visualization.md` | `newskills/SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION.md` | 1:1 mapping |
| `analysis_strategy/signal_background_strategy_and_cr_constraints.md` | `newskills/SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS.md` | 1:1 mapping |
| `analysis_strategy/signal_shape_and_spurious_signal_model_selection.md` | `newskills/SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION.md` | 1:1 mapping |
| `core_pipeline/asimov_expected_significance_splusb.md` | `newskills/SKILL_ASIMOV_EXPECTED_SIGNIFICANCE_SPLUSB.md` | 1:1 mapping |
| `core_pipeline/bootstrap_repo.md` | `newskills/SKILL_BOOTSTRAP_REPO.md` | 1:1 mapping |
| `core_pipeline/cut_flow_and_yields.md` | `newskills/SKILL_CUT_FLOW_AND_YIELDS.md` | 1:1 mapping |
| `core_pipeline/event_io_and_columnar_model.md` | `newskills/SKILL_EVENT_IO_AND_COLUMNAR_MODEL.md` | 1:1 mapping |
| `core_pipeline/final_analysis_report_agent_workflow.md` | `newskills/SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW.md` | 1:1 mapping |
| `core_pipeline/final_report_review_and_handoff.md` | `newskills/SKILL_FINAL_REPORT_REVIEW_AND_HANDOFF.md` | 1:1 mapping |
| `core_pipeline/histogramming_and_templates.md` | `newskills/SKILL_HISTOGRAMMING_AND_TEMPLATES.md` | 1:1 mapping |
| `core_pipeline/plotting_and_report.md` | `newskills/SKILL_PLOTTING_AND_REPORT.md` | 1:1 mapping |
| `core_pipeline/profile_likelihood_significance.md` | `newskills/SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE.md` | 1:1 mapping |
| `core_pipeline/read_summary_and_validate.md` | `newskills/SKILL_READ_SUMMARY_AND_VALIDATE.md` | 1:1 mapping |
| `core_pipeline/sample_registry_and_normalization.md` | `newskills/SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION.md` | 1:1 mapping |
| `core_pipeline/selection_engine_and_regions.md` | `newskills/SKILL_SELECTION_ENGINE_AND_REGIONS.md` | 1:1 mapping |
| `core_pipeline/systematics_and_nuisances.md` | `newskills/SKILL_SYSTEMATICS_AND_NUISANCES.md` | 1:1 mapping |
| `core_pipeline/workspace_and_fit_pyhf.md` | `newskills/SKILL_WORKSPACE_AND_FIT_PYHF.md` | 1:1 mapping |
| `governance/agent_pre_flight_fact_check.md` | `newskills/SKILL_AGENT_PRE_FLIGHT_FACT_CHECK.md` | 1:1 mapping |
| `governance/data_mc_discrepancy_sanity_check.md` | `newskills/SKILL_DATA_MC_DISCREPANCY_SANITY_CHECK.md` | 1:1 mapping |
| `governance/full_statistics_execution_policy.md` | `newskills/SKILL_FULL_STATISTICS_EXECUTION_POLICY.md` | 1:1 mapping |
| `governance/mc_sample_disambiguation_and_nominal_selection.md` | `newskills/SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION.md` | 1:1 mapping |
| `governance/skill_refresh_and_checkpointing.md` | `newskills/SKILL_SKILL_REFRESH_AND_CHECKPOINTING.md` | 1:1 mapping |
| `infrastructure/freeze_analysis_histogram_products.md` | `newskills/SKILL_FREEZE_ANALYSIS_HISTOGRAM_PRODUCTS.md` | 1:1 mapping |
| `infrastructure/rootmltool_cached_analysis.md` | `newskills/SKILL_ROOTMLTOOL_CACHED_ANALYSIS.md` | 1:1 mapping |
| `infrastructure/smoke_tests_and_reproducibility.md` | `newskills/SKILL_SMOKE_TESTS_AND_REPRODUCIBILITY.md` | 1:1 mapping |
| `infrastructure/stattool_optional_pyhf_backend.md` | `newskills/SKILL_STATTOOL_OPTIONAL_PYHF_BACKEND.md` | 1:1 mapping |
| `infrastructure/visual_verification.md` | `newskills/SKILL_VISUAL_VERIFICATION.md` | 1:1 mapping |
| `interfaces/json_spec_driven_execution.md` | `newskills/SKILL_JSON_SPEC_DRIVEN_EXECUTION.md` | 1:1 mapping |
| `interfaces/narrative_to_analysis_json_translator.md` | `newskills/SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR.md` | 1:1 mapping |
| `meta/extract_new_skill_from_failure.md` | `newskills/SKILL_EXTRACT_NEW_SKILL_FROM_FAILURE.md` | 1:1 mapping |
| `open_data_specific/13tev25_details.md` | `newskills/SKILL_13TEV25_DETAILS.md` | 1:1 mapping |
| `physics_facts/histogram_plotting_invariants.md` | `newskills/SKILL_HISTOGRAM_PLOTTING_INVARIANTS.md` | 1:1 mapping |
| `physics_facts/mc_normalization_metadata_stacking.md` | `newskills/SKILL_MC_NORMALIZATION_METADATA_STACKING.md` | 1:1 mapping |
| `physics_facts/object_definitions.md` | `newskills/SKILL_OBJECT_DEFINITIONS.md` | 1:1 mapping |

## Splits or Merges

- No semantic skill splits or merges were applied in this pass. Mapping is strictly 1:1 to avoid workflow-semantic drift.

## Ambiguities Discovered

- Some skills encode cross-cutting governance constraints that apply globally, making strict linear dependencies approximate.
- `skills/README.md` is an index/meta document rather than an executable stage skill; it was still represented as a structured contract (`SKILL_SKILLS_PACK_INDEX`) to avoid dropping knowledge.
- Optional backend/caching skills (`rootmltool`, optional `pyhf`, histogram freezing) are intentionally marked non-mandatory in baseline execution.

## Recommendations

- Add explicit machine-readable `produces` and `consumes` fields directly to source skills to reduce inference ambiguity.
- Add a canonical DAG file in source `skills/` to prevent duplicated dependency inference logic.
- Define mandatory/optional flags in source metadata to remove interpretation burden from agents.
