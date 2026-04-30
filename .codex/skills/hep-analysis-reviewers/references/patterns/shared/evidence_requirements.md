# Evidence Requirements

No stage is complete unless the claim is backed by artifacts, provenance, and an explicit reviewer outcome.

## Always required

- input paths or identifiers used for the stage
- output artifact paths
- provenance showing which summary, samples, and runtime configuration were used
- an assumptions log
- a deviations log
- unresolved issues
- reviewer verdicts when a reviewer is mandatory

## Stage-specific evidence

| Stage | Minimum evidence |
|---|---|
| Spec and setup | normalized summary, gap report if translated, execution contract |
| Samples and normalization | sample registry, nominal-vs-alternative mapping, norm table, metadata resolution |
| Regions and selections | partition spec, executable region definitions, overlap policy, cut-flow provenance |
| Histogramming | template manifest, binning definition, statistical bookkeeping, cache or freeze manifest when used |
| Modeling and fits | background strategy, signal PDF choice, spurious-signal metrics, systematics model, fit provenance |
| Significance | significance artifact, Asimov provenance when used, parameter-floating policy |
| Reporting | report markdown, plot manifest, discrepancy audit, artifact link inventory |
| Handoff | run manifest, checkpoint log, enforcement gate, final reviewer verdict |

## Binding rule

Missing evidence is a blocker, not a warning, when the missing item supports a central claim or a downstream reviewer gate.
