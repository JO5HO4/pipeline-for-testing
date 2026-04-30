# Meta-First Routing Guide

## Core Loop

1. Identify the current blocker in one sentence: missing artifact, unresolved policy, failed validation, or next stage.
2. If starting cold, route first to `SKILL_HEP_ANALYSIS_ENV_SETUP`, then use `00_INDEX.md` and follow the dependency-ordered execution spine until you hit the current blocker.
3. If targeting a specific artifact, search `manifest.yaml` outputs first and load the matching `references/SKILL_*.md` contract file.
4. Filter candidate contracts by `preconditions` and `dependencies.requires`.
5. Before production execution and before handoff, run a code/config compliance audit against the active skills and produce a machine-readable gap list.
6. If any gap is found, route to the smallest-write-scope contract(s) that own the non-compliant component and rewrite that component to comply.
7. Load the minimum contract set that closes the blocker.
8. Use `handoff_to` to choose the next contract once the current step is complete.

## Fast Paths

- Environment/runtime normalization before any repo command: `SKILL_HEP_ANALYSIS_ENV_SETUP`
- Policy-default resolution for enforcement constants: `SKILL_ENFORCEMENT_POLICY_DEFAULTS`
- Non-bypass enforcement gates before handoff: `SKILL_MC_EFFECTIVE_LUMI_COVERAGE_GATE`, `SKILL_BACKGROUND_TEMPLATE_SMOOTHING_POLICY`, `SKILL_ENFORCEMENT_PRE_HANDOFF_GATE`

- Fresh repo or workflow bootstrap: `SKILL_HEP_ANALYSIS_ENV_SETUP`, then `SKILL_BOOTSTRAP_REPO`, then `SKILL_AGENT_PRE_FLIGHT_FACT_CHECK`
- Narrative or JSON spec translation: `SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR`, `SKILL_JSON_SPEC_DRIVEN_EXECUTION`
- Sample registry, normalization, or sample semantics: `SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION`, `SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION`
- Event model, object definitions, or regions: `SKILL_EVENT_IO_AND_COLUMNAR_MODEL`, `SKILL_OBJECT_DEFINITIONS`, `SKILL_SELECTION_ENGINE_AND_REGIONS`
- Cut flows, templates, or cached histogram products: `SKILL_CUT_FLOW_AND_YIELDS`, `SKILL_HISTOGRAMMING_AND_TEMPLATES`, `SKILL_FREEZE_ANALYSIS_HISTOGRAM_PRODUCTS`
- Statistical modeling and significance: `SKILL_SIGNAL_SHAPE_AND_SPURIOUS_SIGNAL_MODEL_SELECTION`, `SKILL_WORKSPACE_AND_FIT_PYHF`, `SKILL_PROFILE_LIKELIHOOD_SIGNIFICANCE`
- Plotting, validation, or final reporting: `SKILL_PLOTTING_AND_REPORT`, `SKILL_VISUAL_VERIFICATION`, `SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW`

## Ambiguity Rules

- No final report handoff is valid unless `outputs/report/background_template_smoothing_check.json`, `outputs/report/mc_effective_lumi_check.json`, and `outputs/report/enforcement_handoff_gate.json` all exist and report `status: ok`.

- If runtime readiness is unknown or shell/import failures appear likely, prefer `SKILL_HEP_ANALYSIS_ENV_SETUP` before bootstrap, tests, smoke runs, or production execution.
- Prefer contracts whose `requires` set is already satisfied over contracts that merely appear later in the spine.
- Treat `SKILL_13TEV25_DETAILS` as a fact source, not an automatic execution stage.
- When a contract is listed as a weak dependency inference case in `skills_refactor_audit.md`, verify with both the manifest and the contract body before committing.
- When multiple contracts look reasonable, choose the one with the smallest write scope and nearest downstream handoff.

## Contract File Convention

- The copied contract files live directly under `references/`.
- Their filenames match the `filename` field in `manifest.yaml`, for example `SKILL_SELECTION_ENGINE_AND_REGIONS.md`.
- The contract body remains preserved, so this pack changes routing behavior without discarding source content.
