# Common Frontmatter Template

Use this template when a skill benefits from machine-readable metadata:

```yaml
---
name: sample_semantics_generator
pattern: generator
purpose: Create sample registry, normalization, and nominal-sample artifacts.
stage: sample_preparation
derived_from:
  - SKILL_SAMPLE_REGISTRY_AND_NORMALIZATION
  - SKILL_MC_NORMALIZATION_METADATA_STACKING
inputs:
  - outputs/summary.normalized.json
  - metadata CSV artifact path
outputs:
  - outputs/samples.registry.json
  - outputs/normalization/norm_table.json
reviewers:
  - ../reviewers/nominal_sample_and_normalization_reviewer.md
requires:
  - ../pipelines/spec_to_runtime_pipeline.md
escalation:
  - Human approval required for any central-result override to luminosity or blinding policy.
---
```

Use frontmatter to summarize the contract, not to replace the body.
