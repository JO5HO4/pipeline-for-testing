# Claim Scope

Use when checking final wording and allowed conclusions.

## Claim Classes

- `reproduction`: the required ingredients and statistical method match the reference sufficiently for the stated result.
- `reinterpretation`: the result is a valid analysis under changed signal, sample, or model assumptions.
- `diagnostic_proxy`: the result is useful for workflow, sanity, or approximate sensitivity only.
- `blocked`: the result must not be used as a final claim.

## Checks

- The report states the weakest valid claim class for every headline result.
- Paper-level language is used only when paper-level claims are allowed.
- Substitutions identify the missing reference ingredient, replacement, impact, and blocked claims.
- Diagnostic-only runs can still hand off, but only as diagnostic outputs.
- Blocked runs still provide useful artifacts, but the final status and report must clearly say blocked.

## Veto Conditions

- Diagnostic or proxy numbers are described as official, paper-level, reproduced, observed discovery, exclusion, or limit results.
- Missing ingredients are hidden in prose or absent from the final report.
- The conclusion is stronger than `outputs/test_outcome_summary.json` allows.
- Observed results are conflated with expected or pseudo-observed results.
