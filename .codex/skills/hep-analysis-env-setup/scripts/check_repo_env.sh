#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/_repo_env.sh"

workspace="${1:-$PWD}"
repo_env_prepare "$workspace"
cd "$ANALYSIS_WORKSPACE"

status=0

check_path() {
  local path="$1"
  local label="$2"
  if [[ -e "$path" ]]; then
    echo "[ok] $label: $path"
  else
    echo "[missing] $label: $path" >&2
    status=1
  fi
}

check_path "$ANALYSIS_ROOTENV_PYTHON" "rootenv python"
check_path "analysis/analysis.summary.json" "summary entrypoint"
check_path "input-data/data" "data directory"
check_path "input-data/MC" "MC directory"

if [[ $status -eq 0 ]]; then
  python - <<'PY' || status=1
import json
import sys
from pathlib import Path

import analysis  # noqa: F401
from analysis.runtime import check_pyroot

summary = Path("analysis/analysis.summary.json").resolve()
pyroot = check_pyroot()
payload = {
    "workspace": str(Path.cwd()),
    "python": sys.executable,
    "summary": str(summary),
    "pyroot": pyroot,
    "cache_dir": str(Path.cwd() / ".cache"),
}
print(json.dumps(payload, indent=2))
if not pyroot.get("available"):
    raise SystemExit(1)
PY
fi

if [[ $status -eq 0 ]]; then
  cat <<'EOF'
Recommended command patterns:
  scripts/run_in_repo_env.sh . -- pytest -q
  scripts/run_in_repo_env.sh . -- python -m analysis.preflight --summary analysis/Higgs-to-diphoton.json --inputs input-data --outputs outputs_preflight
  scripts/run_in_repo_env.sh . -- python -m analysis.cli run --summary analysis/Higgs-to-diphoton.json --inputs input-data --outputs outputs_smoke_env_check --max-events 20000
EOF
fi

exit $status

