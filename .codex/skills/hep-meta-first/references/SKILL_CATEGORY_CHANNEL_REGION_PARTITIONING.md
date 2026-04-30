---
skill_id: SKILL_CATEGORY_CHANNEL_REGION_PARTITIONING
display_name: "Category/Channel x Region Partitioning (SR/CR/SB/VR) for LHC Analyses"
version: 1.0
category: selections

summary: "Represent the analysis phase space using two orthogonal concepts:"

invocation_keywords:
  - "category channel region partitioning"
  - "category/channel x region partitioning (sr/cr/sb/vr) for lhc analyses"
  - "design"
  - "category"
  - "channel"
  - "region"
  - "partitioning"
  - "analyses"

when_to_use:
  - "Use when executing or validating the design stage of the analysis workflow."
  - "Use when this context is available: Category/channel definition artifact:."
  - "Use when this context is available: category identifiers."

when_not_to_use:
  - "Do not use when its required upstream artifacts or dependencies are unresolved."

inputs:
  required:
    - name: category_channel_definition_artifact
      type: artifact
      description: "Category/channel definition artifact:"
    - name: category_identifiers
      type: artifact
      description: "category identifiers"
    - name: category_assignment_logic
      type: artifact
      description: "category assignment logic"
    - name: region_definition_artifact
      type: artifact
      description: "Region definition artifact:"
    - name: region_identifiers
      type: artifact
      description: "region identifiers"
    - name: associated_category
      type: artifact
      description: "associated category (directly or by cartesian mapping rule)"
    - name: region_type
      type: artifact
      description: "region type"
    - name: selection_basis_and_logic
      type: artifact
      description: "selection basis and logic"

  optional:
    - name: optional_context
      type: artifact
      description: "Optional stage context and previously generated diagnostics."

outputs:
  - name: partition_specification_artifact
    type: artifact
    description: "Partition specification artifact (machine-readable):"
  - name: category_list
    type: artifact
    description: "category list"
  - name: region_list
    type: artifact
    description: "region list"
  - name: category_region_mapping
    type: artifact
    description: "category-region mapping"
  - name: category_id
    type: artifact
    description: "`category_id`"
  - name: region_id
    type: artifact
    description: "`region_id`"
  - name: region_type
    type: artifact
    description: "`region_type`"
  - name: selection_basis
    type: artifact
    description: "`selection_basis`"
  - name: selection_definition
    type: artifact
    description: "`selection_definition`"
  - name: blinding_policy
    type: artifact
    description: "`blinding_policy`"
  - name: optional_notes_justification
    type: artifact
    description: "optional notes/justification"
  - name: mass_window
    type: artifact
    description: "`mass_window`"
  - name: control_variable
    type: artifact
    description: "`control_variable`"
  - name: topology_selection
    type: artifact
    description: "`topology_selection`"

preconditions:
  - "Dependency SKILL_READ_SUMMARY_AND_VALIDATE has completed successfully."
  - "Required inputs are present and readable."

postconditions:
  - "All declared outputs for SKILL_CATEGORY_CHANNEL_REGION_PARTITIONING are written with provenance."
  - "Validation checks complete without unresolved blocking failures."

dependencies:
  requires:
    - SKILL_READ_SUMMARY_AND_VALIDATE

  may_follow:
    - SKILL_READ_SUMMARY_AND_VALIDATE

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
  - "writes partition_specification_artifact"
  - "writes category_list"
  - "writes region_list"
  - "writes category_region_mapping"
  - "writes category_id"
  - "writes region_id"
  - "writes region_type"
  - "writes selection_basis"
  - "writes selection_definition"
  - "writes blinding_policy"

failure_modes:
  - "Missing or ambiguous required inputs block execution."
  - "Schema, fit, or consistency checks fail and produce diagnostics."

validation_checks:
  - "Category exclusivity:"
  - "no event can satisfy assignment rules for multiple categories"
  - "Category coverage:"
  - "selected events are assigned to a category or explicitly tracked as `unassigned`"
  - "Partition uniqueness:"
  - "each `(category, region)` appears exactly once"
  - "Region enumeration consistency:"
  - "all referenced regions appear in the manifest"
  - "Diphoton compatibility:"
  - "if `selection_basis = fit_domain`, artifact includes fit observable range metadata"
  - "Blinding readiness:"
  - "signal partitions default to `data_shown = false` unless explicit unblinding directive exists"
  - "Dynamic category compatibility:"
  - "downstream fit/plot workflows can run with arbitrary number of configured categories without code changes"

handoff_to:
  - SKILL_SELECTION_ENGINE_AND_REGIONS
  - SKILL_CONTROL_REGION_SIGNAL_REGION_BLINDING_AND_VISUALIZATION
  - SKILL_SIGNAL_BACKGROUND_STRATEGY_AND_CR_CONSTRAINTS
---

# Purpose

This skill defines a structured execution contract for `analysis_strategy/category_channel_region_partitioning.md`.
It preserves the original physics and workflow intent while exposing explicit invocation semantics for planning and dependency resolution.

# Procedure

1. read and normalize stage inputs and policy constraints
2. execute the stage-specific transformation or decision workflow
3. write required artifacts with provenance and diagnostics
4. run acceptance checks and hand off to downstream skills

# Notes

- Source file: `analysis_strategy/category_channel_region_partitioning.md`
- Original stage: `design`
- Logic type classification: `physics`
- Mandatory for baseline workflow: `yes`

## Preserved Source Content

_Verbatim body preserved from the original markdown source._


# Skill: Category/Channel x Region Partitioning (SR/CR/SB/VR) for LHC Analyses

## Layer 1 - Physics Policy

### Objective
Represent the analysis phase space using two orthogonal concepts:

1. Category/Channel axis (topology or sensitivity partition)
2. Region axis (statistical usage partition)

This structure must support both complex analyses (multiple categories/channels) and simple analyses (single inclusive selection).

### Category/Channel Definition

Categories/channels divide events into mutually exclusive subsets with different signal-to-background behavior or physics topology.

Examples:
- diphoton analysis categories
- jet multiplicity channels (`0-jet`, `1-jet`, `2-jet`)
- VBF-tagged events
- boosted Higgs events

Rules:
- each event must be assigned to exactly one category/channel
- category assignment must be mutually exclusive
- categories should cover all selected events unless an explicit `unassigned` bucket is documented

Inclusive fallback:
- if no natural category split exists, define a single category:
- `category_id = inclusive`

### Region Definition

Regions define statistical usage of events:
- `SR` signal region
- `CR` control region
- `SB` sideband
- `VR` validation region

The atomic statistical key is:
- `(category, region)`

### Diphoton Mass-Spectrum Analyses

For analyses such as `H -> gamma gamma`, both approaches must be supported:

1. Explicit windows:
- `SR` peak window
- `SB` sideband windows

2. Conceptual regions within a full-spectrum fit:
- fit uses full mass range (for example `105-160 GeV`)
- `SR` corresponds to peak interpretation
- `SB` corresponds to sideband interpretation

### Consistency Rules

- category assignments must be exclusive
- category assignments must be complete unless explicitly documented otherwise
- regions must be explicitly defined via selection logic or statistical interpretation
- region definitions must declare type (`SR`, `CR`, `SB`, `VR`, or `OTHER`)
- if blinding is active, it must operate at `(category, region)` granularity
- downstream statistical tools must consume category lists dynamically; no fixed category count should be assumed

## Layer 2 - Workflow Contract

### Inputs

1. Category/channel definition artifact:
- category identifiers
- category assignment logic

2. Region definition artifact:
- region identifiers
- associated category (directly or by cartesian mapping rule)
- region type
- selection basis and logic

3. Optional observable definitions when regions depend on mass/fit-domain ranges.

### Required Artifacts

1. Partition specification artifact (machine-readable):
- category list
- region list
- category-region mapping

For each `(category, region)` entry:
- `category_id`
- `region_id`
- `region_type`
- `selection_basis`
- `selection_definition`
- `blinding_policy`
- optional notes/justification

Selection basis examples:
- `mass_window`
- `control_variable`
- `topology_selection`
- `fit_domain`

2. Partition completeness/exclusivity report (machine-readable):
- category assignment exclusivity
- category assignment coverage
- region enumeration consistency
- duplicate partition checks

3. Partition manifest artifact:
- flat authoritative list of atomic partitions
- fields:
  - `category_id`
  - `region_id`
  - `region_type`

Downstream users:
- cut flow
- histogramming
- statistical model building
- plotting

### Acceptance Checks

1. Category exclusivity:
- no event can satisfy assignment rules for multiple categories

2. Category coverage:
- selected events are assigned to a category or explicitly tracked as `unassigned`

3. Partition uniqueness:
- each `(category, region)` appears exactly once

4. Region enumeration consistency:
- all referenced regions appear in the manifest

5. Diphoton compatibility:
- if `selection_basis = fit_domain`, artifact includes fit observable range metadata

6. Blinding readiness:
- signal partitions default to `data_shown = false` unless explicit unblinding directive exists

7. Dynamic category compatibility:
- downstream fit/plot workflows can run with arbitrary number of configured categories without code changes

## Layer 3 - Tool Binding (Current Repository)

### Example Inputs
- `analysis/categories.yaml`
- `analysis/regions.yaml`

### Expected Outputs
- `outputs/report/partition_spec.json`
- `outputs/report/partition_checks.json`
- `outputs/manifest/partitions.json`

### CLI
`python -m analysis.partitioning.build_partitions --categories analysis/categories.yaml --regions analysis/regions.yaml --out-spec outputs/report/partition_spec.json --out-manifest outputs/manifest/partitions.json --out-checks outputs/report/partition_checks.json`

### Implementation Notes
- exclusivity checks can be declarative or event-level, but must be explicit in checks metadata
- region definitions should remain structured for machine interpretation
- diphoton mass analyses should support both window-based and full-fit-domain semantics
- downstream tools should consume `outputs/manifest/partitions.json` rather than re-deriving partition logic

# Examples

Example invocation context:
- `python -m analysis.partitioning.build_partitions --categories analysis/categories.yaml --regions analysis/regions.yaml --out-spec outputs/report/partition_spec.json --out-manifest outputs/manifest/partitions.json --out-checks outputs/report/partition_checks.json`

Example expected outputs:
- `outputs/report/partition_spec.json`
- `outputs/report/partition_checks.json`
- `outputs/manifest/partitions.json`
