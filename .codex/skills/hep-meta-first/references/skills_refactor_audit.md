# Skills Refactor Audit

## Scope

- Total number of original markdown documents in `skills/`: 36
- Number of structured contracts created in `newskills/`: 36
- Mapping mode: 1:1 conversion preserving all source markdown body content in each contract (`## Preserved Source Content`).

## Dependency Graph Summary

- Nodes (skills): 36
- Directed edges (`requires`): 54
- Skills with zero incoming dependencies: 3
- Skills with zero outgoing handoff intent: 0

Top dependency hubs (out-degree):
- `SKILL_HISTOGRAMMING_AND_TEMPLATES` -> 6 dependent skills
- `SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION` -> 6 dependent skills
- `SKILL_SELECTION_ENGINE_AND_REGIONS` -> 4 dependent skills
- `SKILL_AGENT_PRE_FLIGHT_FACT_CHECK` -> 3 dependent skills
- `SKILL_BOOTSTRAP_REPO` -> 3 dependent skills
- `SKILL_PLOTTING_AND_REPORT` -> 3 dependent skills
- `SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS` -> 3 dependent skills
- `SKILL_WORKSPACE_AND_FIT_PYHF` -> 3 dependent skills
- `SKILL_FINAL_ANALYSIS_REPORT_AGENT_WORKFLOW` -> 2 dependent skills
- `SKILL_MC_SAMPLE_DISAMBIGUATION_AND_NOMINAL_SELECTION` -> 2 dependent skills

## Skills with Weak Dependency Inference

- `SKILL_ROOTMLTOOL_CACHED_ANALYSIS`
- `SKILL_JSON_SPEC_DRIVEN_EXECUTION`
- `SKILL_NARRATIVE_TO_ANALYSIS_JSON_TRANSLATOR`
- `SKILL_13TEV25_DETAILS`

## Areas Needing Further Human Curation

- Cross-cutting governance skills (`pre-flight`, `skill-refresh`, `full-statistics policy`) apply at multiple points and may need per-analysis DAG overrides.
- Optional backend/caching paths (`rootmltool`, optional `pyhf`, histogram freezing) should be tied to explicit runtime feature flags in future metadata.
- Dataset-specific fact skill (`13tev25_details`) is a knowledge source and not always an executable stage; downstream invocation policy may need stricter gating.
- `skills/README.md` was represented as a contract for completeness; teams may prefer keeping it index-only and excluding it from executable DAGs.

## Agent-Readiness Assessment

- Readiness: **High for contract-driven planning**, with moderate ambiguity in cross-cutting governance ordering.
- Strengths: explicit inputs/outputs, preconditions/postconditions, dependencies/handoffs, validation checks, and preserved source knowledge per skill.
- Remaining risk: inferred dependency edges are heuristic where source docs do not explicitly declare machine-readable producers/consumers.
