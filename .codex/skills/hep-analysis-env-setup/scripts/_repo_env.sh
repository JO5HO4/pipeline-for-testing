#!/usr/bin/env bash
set -euo pipefail

repo_env_usage() {
  cat <<'EOF'
Usage:
  run_in_repo_env.sh <workspace> -- <command...>
  check_repo_env.sh [workspace]
EOF
}

repo_env_resolve_workspace() {
  local workspace="${1:-$PWD}"
  (
    cd "$workspace" >/dev/null 2>&1
    pwd
  )
}

repo_env_prepare() {
  local workspace
  workspace="$(repo_env_resolve_workspace "${1:-$PWD}")"

  mkdir -p "$workspace/.cache" "$workspace/.cache/matplotlib" "$workspace/.cache/fontconfig"

  export ANALYSIS_WORKSPACE="$workspace"
  export ANALYSIS_ROOTENV_PYTHON="$workspace/.rootenv/bin/python"
  export ANALYSIS_ROOTENV_PYTEST="$workspace/.rootenv/bin/pytest"
  export PATH="$workspace/.rootenv/bin:$PATH"
  export PYTHONPATH="$workspace${PYTHONPATH:+:$PYTHONPATH}"
  export MPLCONFIGDIR="$workspace/.cache/matplotlib"
  export XDG_CACHE_HOME="$workspace/.cache"
  export PYTHONNOUSERSITE=1
}

