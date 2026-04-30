#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/_repo_env.sh"

if [[ $# -lt 3 || "$2" != "--" ]]; then
  repo_env_usage >&2
  exit 2
fi

workspace="$1"
shift 2
repo_env_prepare "$workspace"

if [[ ! -x "$ANALYSIS_ROOTENV_PYTHON" ]]; then
  echo "Missing workspace runtime: $ANALYSIS_ROOTENV_PYTHON" >&2
  echo "This repo requires the workspace-local .rootenv for PyROOT/RooFit-primary H->gammagamma work." >&2
  exit 2
fi

cd "$ANALYSIS_WORKSPACE"
exec "$@"

