from __future__ import annotations

import argparse
from pathlib import Path

from analysis.common import read_json, write_json
from analysis.runtime import write_runtime_recovery
from analysis.vlq_pipeline import discover_samples, parse_regions, run_vlq_pipeline


def _load_vlq_summary(summary: Path) -> dict:
    source_summary = read_json(summary)
    metadata = source_summary.get("analysis_metadata", {})
    if metadata.get("analysis_short_name") != "same_charge_leptons_bjets":
        raise SystemExit(f"{summary} is not a VLQ same-charge leptons plus b-jets summary")
    return source_summary


def _normalized_summary(source_summary: dict, summary: Path) -> dict:
    regions = parse_regions(source_summary)
    return {
        "source_summary": str(summary),
        "analysis_short_name": source_summary["analysis_metadata"]["analysis_short_name"],
        "inventory": {
            "n_signal_regions": len(regions),
            "n_control_regions": len(source_summary.get("control_regions", [])),
            "fit_ids": [fit.get("fit_id") for fit in source_summary.get("fit_setup", [])],
            "region_names": [region.name for region in regions],
        },
    }


def bootstrap(summary: Path, outputs: Path) -> None:
    source_summary = _load_vlq_summary(summary)
    write_json(_normalized_summary(source_summary, summary), outputs / "summary.normalized.json")
    write_runtime_recovery(outputs / "report" / "runtime_recovery.json")


def preflight(summary: Path, inputs: Path, outputs: Path) -> None:
    source_summary = _load_vlq_summary(summary)
    samples, discovery_notes = discover_samples(inputs)
    write_json(_normalized_summary(source_summary, summary), outputs / "summary.normalized.json")
    write_json(_normalized_summary(source_summary, summary)["inventory"], outputs / "validation" / "inventory.json")
    write_json(samples, outputs / "samples.registry.json")
    write_json(discovery_notes, outputs / "samples.discovery_notes.json")
    write_runtime_recovery(outputs / "report" / "runtime_recovery.json")
    if not samples:
        raise SystemExit(1)


def run_pipeline(summary: Path, inputs: Path, outputs: Path, max_events: int | None, workers: int) -> None:
    _load_vlq_summary(summary)
    run_vlq_pipeline(summary, inputs, outputs, max_events=max_events, workers=workers)


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
    run_parser.add_argument("--workers", type=int, default=1)

    args = parser.parse_args()
    if args.command == "bootstrap":
        bootstrap(Path(args.summary), Path(args.outputs))
    elif args.command == "preflight":
        preflight(Path(args.summary), Path(args.inputs), Path(args.outputs))
    else:
        run_pipeline(Path(args.summary), Path(args.inputs), Path(args.outputs), args.max_events, args.workers)
