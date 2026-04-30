# Open-Data Dataset Facts

Use this reference when sample naming, metadata matching, or nominal background selection is ambiguous.

## Binding facts

- The metadata CSV artifact is the authoritative source for cross section, k-factor, filter efficiency, and signed generator-weight sums in the current analysis project. In this bundled reference pack it lives at `../metadata.csv`; some legacy repo layouts used `skills/metadata.csv`.
- Stable identifiers such as DSIDs should be preferred over free-form filename matching.
- The central Run-2 H to gammagamma normalization policy uses `36.1 fb^-1` unless an approved override is recorded.
- Effective luminosity should be documented for backgrounds that enter fit-critical template or smoothing decisions.

## H to gammagamma repository facts

- The nominal background template should be a clear diphoton MC choice rather than an opaque merge of many low-statistics auxiliary samples.
- The nominal template choice must document the selected mass window and any sideband normalization to observed data.
- Low-statistics auxiliary samples can inform checks or variations, but they should not silently become the central template.
- Prompt diphoton production is the default irreducible background class for the diphoton signature.
- Gamma-plus-jet and jet-plus-jet processes are reducible backgrounds only when fake-photon contamination is relevant at the analysis level.
- Processes that only produce the diphoton signature through vanishingly small higher-order or fake paths should remain negligible unless the analysis has evidence to keep them.
- NT-like or other inverted-quality data samples are template-source candidates, not observed-data likelihood terms, unless a disjoint and explicitly approved use says otherwise.

## When to escalate

- Multiple datasets appear equally valid as the nominal sample for a central process.
- Filename semantics and DSID semantics disagree.
- The repository summary, metadata table, and existing outputs imply inconsistent luminosity or process-role choices.
