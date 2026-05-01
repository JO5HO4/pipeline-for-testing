#!/usr/bin/env bash
set -euo pipefail

workspace="${1:-$PWD}"
workspace="$(cd "$workspace" && pwd)"
output="${2:-$workspace/outputs/report/root_runtime_probe.json}"
mkdir -p "$(dirname "$output")"

WORKSPACE="$workspace" OUTPUT="$output" python3 - <<'PY'
from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

workspace = Path(os.environ["WORKSPACE"])
output = Path(os.environ["OUTPUT"])


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def tail(text: str, limit: int = 2000) -> str:
    return text[-limit:]


def run(argv: list[str], *, timeout: int = 60) -> dict:
    try:
        proc = subprocess.run(argv, text=True, capture_output=True, timeout=timeout)
        status = "pass" if proc.returncode == 0 else "fail"
        return {
            "command": argv,
            "status": status,
            "returncode": proc.returncode,
            "stdout_tail": tail(proc.stdout),
            "stderr_tail": tail(proc.stderr),
        }
    except Exception as exc:
        return {
            "command": argv,
            "status": "fail",
            "returncode": None,
            "stdout_tail": "",
            "stderr_tail": repr(exc),
        }


pyroot_code = "import ROOT; print(ROOT.gROOT.GetVersion())"
roofit_code = r'''
import ROOT
ROOT.gROOT.SetBatch(True)
x = ROOT.RooRealVar("x", "x", -5.0, 5.0)
mean = ROOT.RooRealVar("mean", "mean", 0.0, -1.0, 1.0)
sigma = ROOT.RooRealVar("sigma", "sigma", 1.0, 0.1, 10.0)
gauss = ROOT.RooGaussian("gauss", "gauss", x, mean, sigma)
data = gauss.generate(ROOT.RooArgSet(x), 25)
result = gauss.fitTo(data, ROOT.RooFit.Save(True), ROOT.RooFit.PrintLevel(-1))
workspace = ROOT.RooWorkspace("w")
importer = getattr(workspace, "Import", None) or getattr(workspace, "import")
importer(gauss)
print({"root": ROOT.gROOT.GetVersion(), "fit_status": int(result.status())})
raise SystemExit(int(result.status()))
'''

python_candidates: list[tuple[str, str]] = []
rootenv_python = workspace / ".rootenv" / "bin" / "python"
python_candidates.append((".rootenv", str(rootenv_python)))
for name in ("python3", "python"):
    found = shutil.which(name)
    if found:
        python_candidates.append((name, found))

seen: set[str] = set()
attempts: list[dict] = []
selected = None

for kind, python in python_candidates:
    if python in seen:
        continue
    seen.add(python)
    if not Path(python).exists():
        attempts.append({
            "name": f"{kind}:exists",
            "command": [python],
            "status": "skipped",
            "reason": "python candidate does not exist",
        })
        continue
    pyroot = run([python, "-c", pyroot_code])
    pyroot["name"] = f"{kind}:pyroot"
    attempts.append(pyroot)
    roofit = run([python, "-c", roofit_code])
    roofit["name"] = f"{kind}:roofit"
    attempts.append(roofit)
    if pyroot["status"] == "pass" and roofit["status"] == "pass" and selected is None:
        selected = {
            "selected_python": python,
            "selected_runtime_kind": kind,
            "selected_root_version": pyroot["stdout_tail"].strip().splitlines()[-1] if pyroot["stdout_tail"].strip() else None,
        }

for cmd in ("root-config", "root"):
    found = shutil.which(cmd)
    attempts.append({
        "name": f"which:{cmd}",
        "command": ["which", cmd],
        "status": "pass" if found else "fail",
        "stdout_tail": found or "",
        "stderr_tail": "",
        "reason": "" if found else f"{cmd} not found on PATH",
    })
    if found and cmd == "root-config":
        probe = run([found, "--version"])
        probe["name"] = "root-config:version"
        attempts.append(probe)

status = "available" if selected else "unavailable_after_repair_attempts"
payload = {
    "schema_version": "root_runtime_repair.v1",
    "workspace": str(workspace),
    "updated_at_utc": now(),
    "root_runtime_status": status,
    "selected_python": selected["selected_python"] if selected else None,
    "selected_root_version": selected["selected_root_version"] if selected else None,
    "selected_runtime_kind": selected["selected_runtime_kind"] if selected else "none",
    "attempts": attempts,
    "pyroot_smoke": "pass" if selected else "fail",
    "roofit_smoke": "pass" if selected else "fail",
    "diagnostic_fallback_allowed": selected is None,
    "paper_level_root_claims_allowed": selected is not None,
}
output.write_text(json.dumps(payload, indent=2) + "\n")
print(json.dumps(payload, indent=2))
raise SystemExit(0 if selected else 1)
PY
