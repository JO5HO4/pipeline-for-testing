# Statistical Quality

Use when checking whether final statistical results are valid for their claimed scope.

## Checks

- The statistical model matches the reference contract or the substitution is explicitly classified.
- Expected results are computed before observed results when blinding or signal-sensitive regions apply.
- Fit convergence, parameter bounds, covariance quality, and NLL behavior are recorded when a fit is used.
- Limit or significance methods identify the likelihood/counting model, nuisance treatment, and test statistic.
- Signed or negative MC yields are preserved in raw artifacts and any nonnegative stabilization is labeled diagnostic.
- Missing signal models, data-driven backgrounds, fake/nonprompt estimates, charge-flip estimates, systematics, or correlations are reflected in claim scope.
- Observed signal-region claims require validated real observed data and an explicit unblinding gate.

## Veto Conditions

- A failed, unstable, or approximate statistic is presented as paper-level.
- A fallback backend is promoted to the primary reference method without validated parity.
- Negative/signed yields are silently clipped for a statistic.
- Observed limits/significances are reported before expected workflow validation and unblinding.
- Paper-level exclusions, measurements, or discoveries are claimed without the required model ingredients.
