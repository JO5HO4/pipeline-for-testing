# Decision Record Template

Use this template for Inversions and for any Generator that depends on a non-trivial branch decision.

```yaml
decision_id:
trigger:
question:
options_considered:
chosen_option:
why_chosen:
rejected_options:
required_evidence:
observed_evidence:
assumptions:
risks:
downstream_impacts:
escalate_to_human: false
blocking_if_unresolved: true
related_artifacts:
related_skills:
```

The record should be written before executing a branch that could change central physics outputs or reviewer outcomes.
