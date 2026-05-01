---
name: hep-root-runtime-repair
description: "Use when a HEP analysis needs PyROOT, RooFit, ROOT, root-config, CLs/RooStats, or a ROOT-backed statistical backend and the current runtime cannot import ROOT or lacks a working .rootenv. Attempts local runtime discovery and generic conda/mamba repair, writes root runtime repair evidence, and only then allows diagnostic fallback or blocked status."
---

# HEP ROOT Runtime Repair

Use this skill before accepting a diagnostic fallback caused by missing PyROOT, RooFit, ROOT, RooStats, `root-config`, or a missing `.rootenv`.

## Required Artifacts

- Write `outputs/report/root_runtime_repair_attempts.json` for baseline-style layouts, or `artifacts/runtime/root_runtime_repair_attempts.json` for multiagent/stateful layouts.
- If a fallback or block is still needed, point `outputs/evaluation_scorecard.json` and any feasibility or finalization artifact at the repair-attempt artifact.
- Do not claim ROOT/RooFit is unavailable unless this skill records the attempted discovery and repair path.

## Repair Order

1. Probe existing runtimes:
   - `<workspace>/.rootenv/bin/python`
   - active `python3` and `python`
   - `root-config`, `root`, `$ROOTSYS`, and `thisroot.sh` when present
   - host module hints such as `module avail root`, when the module command exists
2. For every Python candidate, run both:
   - `import ROOT; print(ROOT.gROOT.GetVersion())`
   - a minimal RooFit smoke test that creates a `RooWorkspace`, `RooRealVar`, `RooGaussian`, toy dataset, and fit result.
3. If no valid runtime exists and a conda-like tool is available, try to create `<workspace>/.rootenv` with conda-forge ROOT:
   - Prefer `micromamba`, then `mamba`, then `conda`.
   - Use an explicit prefix: `<workspace>/.rootenv`.
   - Include at least: `python=3.11`, `root`, `uproot`, `awkward`, `numpy`, `scipy`, `matplotlib`, `pandas`, `pyyaml`, `pytest`.
   - Never use `pip install ROOT` as the primary repair path; PyPI packages are not a reliable ROOT/RooFit runtime.
4. If the user or local notes provide a host-specific container command, the agent may try it after generic probes. Record the exact command and result, but keep host-specific container details out of reusable prompt text.
5. Rerun the PyROOT and RooFit smoke tests after every repair attempt.

## Decision Rules

- If RooFit smoke passes, use that runtime for ROOT-backed analysis stages and record `root_runtime_status: repaired`.
- If a ROOT runtime exists but RooFit smoke fails, treat it as unavailable for RooFit-primary claims.
- If conda/mamba repair fails or is not available, record `root_runtime_status: unavailable_after_repair_attempts`.
- Diagnostic fallback is allowed only after the repair artifact exists and explains why the ROOT-backed path cannot be used.
- For H->gammagamma primary signal-strength or significance claims, missing RooFit after repair attempts blocks paper-level claims; a non-ROOT fallback may only be diagnostic.

## Helper Scripts

From the repository root:

```bash
.codex/skills/hep-root-runtime-repair/scripts/probe_root_runtime.sh .
.codex/skills/hep-root-runtime-repair/scripts/repair_root_runtime.sh .
```

The repair script is intentionally generic. It tries local discovery and conda/mamba repair, then writes a JSON artifact. It does not encode site-specific container setup.

## Artifact Fields

The repair artifact should include:

```json
{
  "schema_version": "root_runtime_repair.v1",
  "workspace": "<absolute workspace path>",
  "updated_at_utc": "<ISO-8601 timestamp>",
  "root_runtime_status": "available|repaired|unavailable_after_repair_attempts",
  "selected_python": "<path or null>",
  "selected_root_version": "<version or null>",
  "selected_runtime_kind": ".rootenv|active_python|system_root|conda_repair|container|none",
  "attempts": [
    {
      "name": "<short attempt name>",
      "command": ["<argv>"],
      "status": "pass|fail|skipped",
      "stdout_tail": "<short tail>",
      "stderr_tail": "<short tail>",
      "reason": "<short reason>"
    }
  ],
  "pyroot_smoke": "pass|fail|not_run",
  "roofit_smoke": "pass|fail|not_run",
  "diagnostic_fallback_allowed": false,
  "paper_level_root_claims_allowed": false
}
```

Keep output concise; do not paste long module lists, install logs, or container logs into final reports. Save those as separate logs only when needed.
