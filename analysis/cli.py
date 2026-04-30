from __future__ import annotations

import argparse
from pathlib import Path

from analysis.common import read_json, write_json
from analysis.runtime import write_runtime_recovery
from analysis.vlq_pipeline import (
    build_vlq_registry,
    inspect_inputs,
    is_vlq_summary,
    normalize_vlq_summary,
    run_vlq_analysis,
)


def _load_vlq_summary(summary: Path) -> tuple[dict, dict]:
    source_summary = read_json(summary)
    if not is_vlq_summary(source_summary, summary):
        raise SystemExit(f"{summary} is not a VLQ same-charge leptons plus b-jets summary")
    return source_summary, normalize_vlq_summary(source_summary, summary)


def bootstrap(summary: Path, outputs: Path) -> None:
    _, normalized = _load_vlq_summary(summary)
    write_json(normalized, outputs / "summary.normalized.json")
    write_runtime_recovery(outputs / "report" / "runtime_recovery.json")


def preflight(summary: Path, inputs: Path, outputs: Path) -> None:
    _, normalized = _load_vlq_summary(summary)
    registry, registry_roles = build_vlq_registry(inputs, normalized)
    branch_inventory = (
        inspect_inputs(inputs, registry)
        if registry
        else {"status": "blocked", "reason": "No data or MC ROOT files were found under input-data/."}
    )
    write_json(normalized, outputs / "summary.normalized.json")
    write_json(normalized["inventory"], outputs / "validation" / "inventory.json")
    write_json(branch_inventory, outputs / "validation" / "branch_inventory.json")
    write_json(registry, outputs / "samples.registry.json")
    write_json(registry_roles, outputs / "samples.classification.json")
    write_runtime_recovery(outputs / "report" / "runtime_recovery.json")
    if branch_inventory.get("status") != "ok":
        raise SystemExit(1)


def run_pipeline(
    summary: Path,
    inputs: Path,
    outputs: Path,
    max_events: int | None,
    unblind_observed_significance: bool = False,
) -> None:
    source_summary = read_json(summary)
    if not is_vlq_summary(source_summary, summary):
        raise SystemExit(f"{summary} is not a VLQ same-charge leptons plus b-jets summary")
    run_vlq_analysis(
        source_summary=source_summary,
        summary_path=summary,
        inputs=inputs,
        outputs=outputs,
        max_events=max_events,
        unblind_observed_significance=unblind_observed_significance,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap_parser = subparsers.add_parser("bootstrap")
    bootstrap_parser.add_argument("--summary", required=True)
    bootstrap_parser.add_argument("--outputs", required=True)

    preflight_parser = subparsers.add_parser("preflight")
    preflight_parser.add_argument("--summary", required=True)
    preflight_parser.add_argument("--inputs", required=True)
    preflight_parser.add_argument("--outputs", required=True)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--summary", required=True)
    run_parser.add_argument("--inputs", required=True)
    run_parser.add_argument("--outputs", required=True)
    run_parser.add_argument("--max-events", type=int)
    run_parser.add_argument("--unblind-observed-significance", action="store_true")

    args = parser.parse_args()
    if args.command == "bootstrap":
        bootstrap(Path(args.summary), Path(args.outputs))
    elif args.command == "preflight":
        preflight(Path(args.summary), Path(args.inputs), Path(args.outputs))
    else:
        run_pipeline(
            Path(args.summary),
            Path(args.inputs),
            Path(args.outputs),
            args.max_events,
            args.unblind_observed_significance,
        )


if __name__ == "__main__":
    main()
