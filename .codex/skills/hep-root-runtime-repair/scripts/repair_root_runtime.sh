#!/usr/bin/env bash
set -euo pipefail

workspace="${1:-$PWD}"
workspace="$(cd "$workspace" && pwd)"
output="${2:-$workspace/outputs/report/root_runtime_repair_attempts.json}"
log_dir="$workspace/outputs/report/root_runtime_repair_logs"
mkdir -p "$(dirname "$output")" "$log_dir"

probe_script="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/probe_root_runtime.sh"

if "$probe_script" "$workspace" "$output"; then
  exit 0
fi

installer=""
for candidate in micromamba mamba conda; do
  if command -v "$candidate" >/dev/null 2>&1; then
    installer="$candidate"
    break
  fi
done

if [[ -n "$installer" ]]; then
  install_log="$log_dir/conda_root_install.log"
  env_prefix="$workspace/.rootenv"
  rm -rf "$env_prefix"
  set +e
  "$installer" create -y -p "$env_prefix" -c conda-forge \
    python=3.11 root uproot awkward numpy scipy matplotlib pandas pyyaml pytest \
    >"$install_log" 2>&1
  install_status=$?
  set -e
  if [[ $install_status -eq 0 ]]; then
    if "$probe_script" "$workspace" "$output"; then
      WORKSPACE="$workspace" OUTPUT="$output" INSTALLER="$installer" INSTALL_LOG="$install_log" python3 - <<'PY'
import json
import os
from pathlib import Path

path = Path(os.environ["OUTPUT"])
payload = json.loads(path.read_text())
payload["root_runtime_status"] = "repaired"
payload["selected_runtime_kind"] = "conda_repair"
payload["attempts"].append({
    "name": "conda_repair:create_rootenv",
    "command": [os.environ["INSTALLER"], "create", "-p", str(Path(os.environ["WORKSPACE"]) / ".rootenv"), "-c", "conda-forge", "python=3.11", "root", "..."],
    "status": "pass",
    "stdout_tail": "",
    "stderr_tail": "",
    "reason": f"Full log saved at {os.environ['INSTALL_LOG']}",
})
payload["diagnostic_fallback_allowed"] = False
payload["paper_level_root_claims_allowed"] = True
path.write_text(json.dumps(payload, indent=2) + "\n")
PY
      exit 0
    fi
  fi
  WORKSPACE="$workspace" OUTPUT="$output" INSTALLER="$installer" INSTALL_LOG="$install_log" INSTALL_STATUS="$install_status" python3 - <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

path = Path(os.environ["OUTPUT"])
payload = json.loads(path.read_text()) if path.exists() else {
    "schema_version": "root_runtime_repair.v1",
    "workspace": os.environ["WORKSPACE"],
    "updated_at_utc": datetime.now(timezone.utc).isoformat(),
    "attempts": [],
}
payload["root_runtime_status"] = "unavailable_after_repair_attempts"
payload["selected_python"] = None
payload["selected_root_version"] = None
payload["selected_runtime_kind"] = "none"
payload["attempts"].append({
    "name": "conda_repair:create_rootenv",
    "command": [os.environ["INSTALLER"], "create", "-p", str(Path(os.environ["WORKSPACE"]) / ".rootenv"), "-c", "conda-forge", "python=3.11", "root", "..."],
    "status": "fail",
    "stdout_tail": "",
    "stderr_tail": "",
    "reason": f"Installer exited {os.environ['INSTALL_STATUS']}; full log saved at {os.environ['INSTALL_LOG']}",
})
payload["pyroot_smoke"] = "fail"
payload["roofit_smoke"] = "fail"
payload["diagnostic_fallback_allowed"] = True
payload["paper_level_root_claims_allowed"] = False
path.write_text(json.dumps(payload, indent=2) + "\n")
PY
else
  WORKSPACE="$workspace" OUTPUT="$output" python3 - <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

path = Path(os.environ["OUTPUT"])
payload = json.loads(path.read_text()) if path.exists() else {
    "schema_version": "root_runtime_repair.v1",
    "workspace": os.environ["WORKSPACE"],
    "updated_at_utc": datetime.now(timezone.utc).isoformat(),
    "attempts": [],
}
payload["root_runtime_status"] = "unavailable_after_repair_attempts"
payload["selected_python"] = None
payload["selected_root_version"] = None
payload["selected_runtime_kind"] = "none"
payload["attempts"].append({
    "name": "conda_repair:installer_discovery",
    "command": ["which", "micromamba|mamba|conda"],
    "status": "skipped",
    "stdout_tail": "",
    "stderr_tail": "",
    "reason": "No micromamba, mamba, or conda executable found on PATH.",
})
payload["pyroot_smoke"] = "fail"
payload["roofit_smoke"] = "fail"
payload["diagnostic_fallback_allowed"] = True
payload["paper_level_root_claims_allowed"] = False
path.write_text(json.dumps(payload, indent=2) + "\n")
PY
fi

exit 1
