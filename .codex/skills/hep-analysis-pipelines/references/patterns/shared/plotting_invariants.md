# Plotting Invariants

These invariants apply to histogram, region, fit, and report plots unless an explicit override is approved and logged.

- Axis labels must identify the observable and units when applicable.
- Binning must be stable across compared samples unless the plot explicitly documents a rebinning step.
- MC statistical uncertainties must come from weighted bookkeeping such as `sumw2`, not naive event counts.
- Data, signal, and background roles must remain visually distinguishable.
- Blinded signal windows must be omitted or masked, never shown accidentally.
- Control-region plots should exist in both pre-fit and post-fit forms when fit constraints are used.
- Required H to gammagamma statistical-input plots are mandatory deliverables, not optional diagnostics.
- Report plots must be embedded inline with adjacent captions that explain what the viewer should learn from the figure.
