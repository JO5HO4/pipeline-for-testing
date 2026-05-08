from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any

import uproot

from analysis.common import ensure_dir, list_root_files, write_json


META_BRANCHES = [
    "num_events",
    "sum_of_weights",
    "sum_of_weights_squared",
    "xsec",
    "filteff",
    "kfac",
    "channelNumber",
]

OFFICIAL_METADATA_CANDIDATES = [
    Path(".codex/skills/hep-analysis-pipelines/references/patterns/metadata.csv"),
    Path(".codex/skills/hep-analysis-meta-pipeline/references/patterns/metadata.csv"),
    Path(".codex/skills/hep-analysis-tool-wrappers/references/patterns/metadata.csv"),
    Path("skills/metadata.csv"),
    Path("../ATLAS Open Data Metadata.csv"),
    Path("../../ATLAS Open Data Metadata.csv"),
    Path("../../../ATLAS Open Data Metadata.csv"),
]


def dsid_from_name(path: Path) -> str | None:
    match = re.search(r"_mc_(\d+)\.", path.name)
    return match.group(1) if match else None


def descriptor_from_name(path: Path) -> str:
    name = path.name
    if name.endswith(".root"):
        name = name[:-5]
    for stream_suffix in (".GamGam", ".1LMET30"):
        if name.endswith(stream_suffix):
            name = name[: -len(stream_suffix)]
    return name.split("_mc_", 1)[1].split(".", 1)[1]


def generator_from_descriptor(descriptor: str) -> tuple[str, str]:
    tokens = descriptor.split("_")
    generator = tokens[0]
    simulation = "_".join(tokens[1:]) if len(tokens) > 1 else descriptor
    return generator, simulation


def read_root_metadata(path: Path) -> dict[str, Any]:
    with uproot.open(path) as handle:
        tree = handle["analysis"]
        arrays = tree.arrays(META_BRANCHES, entry_stop=1, library="np")
        values = {branch: float(arrays[branch][0]) for branch in META_BRANCHES if branch in arrays}
        values["entries"] = int(tree.num_entries)
    return values


def _float_or_none(value: Any) -> float | None:
    if value in {None, ""}:
        return None
    try:
        return float(str(value).strip().replace(",", ""))
    except ValueError:
        return None


def _int_or_none(value: Any) -> int | None:
    parsed = _float_or_none(value)
    return None if parsed is None else int(parsed)


def _find_official_metadata_csv(start: Path | None = None) -> Path | None:
    base = (start or Path.cwd()).resolve()
    search_roots = [base, *base.parents]
    seen: set[Path] = set()
    for root in search_roots:
        for candidate in OFFICIAL_METADATA_CANDIDATES:
            path = (root / candidate).resolve()
            if path in seen:
                continue
            seen.add(path)
            if path.exists():
                return path
    return None


def official_metadata_lookup(start: Path | None = None) -> tuple[dict[str, dict[str, Any]], Path | None]:
    path = _find_official_metadata_csv(start)
    if path is None:
        return {}, None
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    lookup: dict[str, dict[str, Any]] = {}
    for row in rows:
        dsid = str(row.get("dataset_number") or row.get("dsid") or row.get("sample_id") or "").strip()
        if not dsid:
            continue
        lookup[dsid] = row
    return lookup, path


def canonical_metadata_row(row: dict[str, Any], *, dsid: str, descriptor: str, generator: str, simulation: str, path: Path, root_meta: dict[str, Any], source_path: Path | None) -> dict[str, Any]:
    xsec_pb = _float_or_none(row.get("crossSection_pb") or row.get("xsec_pb"))
    k_factor = _float_or_none(row.get("kFactor") or row.get("k_factor"))
    filter_eff = _float_or_none(row.get("genFiltEff") or row.get("filter_eff"))
    sumw = _float_or_none(row.get("sumOfWeights") or row.get("sumw"))
    sumw2 = _float_or_none(row.get("sumOfWeightsSquared") or row.get("sumw2"))
    num_events = _int_or_none(row.get("nEvents") or row.get("num_events"))
    denom = (xsec_pb or 0.0) * (k_factor or 0.0) * (filter_eff or 0.0) * 1000.0
    effective_lumi_fb = sumw / denom if sumw is not None and denom > 0.0 else None
    return {
        "sample_id": dsid,
        "dsid": dsid,
        "file": str(path),
        "filename": path.name,
        "descriptor": row.get("physics_short") or descriptor,
        "generator": row.get("generator") or generator,
        "simulation_config": simulation,
        "xsec_pb": xsec_pb,
        "k_factor": k_factor,
        "filter_eff": filter_eff,
        "sumw": sumw,
        "sumw2": sumw2,
        "num_events": num_events,
        "entries": root_meta["entries"],
        "effective_lumi_fb": effective_lumi_fb,
        "metadata_source": "official_atlas_open_data_metadata_csv",
        "metadata_source_path": str(source_path) if source_path else None,
        "root_num_events": root_meta.get("num_events"),
        "root_sumw": root_meta.get("sum_of_weights"),
        "root_sumw2": root_meta.get("sum_of_weights_squared"),
        "root_xsec_pb": root_meta.get("xsec"),
        "root_filter_eff": root_meta.get("filteff"),
        "root_k_factor": root_meta.get("kfac"),
    }


def _root_fallback_row(*, dsid: str, descriptor: str, generator: str, simulation: str, path: Path, root_meta: dict[str, Any]) -> dict[str, Any]:
    denom = root_meta["xsec"] * root_meta["kfac"] * root_meta["filteff"] * 1000.0
    effective_lumi_fb = root_meta["sum_of_weights"] / denom if denom > 0 else None
    return {
        "sample_id": dsid,
        "dsid": dsid,
        "file": str(path),
        "filename": path.name,
        "descriptor": descriptor,
        "generator": generator,
        "simulation_config": simulation,
        "xsec_pb": root_meta["xsec"],
        "k_factor": root_meta["kfac"],
        "filter_eff": root_meta["filteff"],
        "sumw": root_meta["sum_of_weights"],
        "sumw2": root_meta["sum_of_weights_squared"],
        "num_events": int(root_meta["num_events"]),
        "entries": root_meta["entries"],
        "effective_lumi_fb": effective_lumi_fb,
        "metadata_source": "root_metadata_fallback_unapproved",
        "metadata_source_path": None,
        "root_num_events": root_meta.get("num_events"),
        "root_sumw": root_meta.get("sum_of_weights"),
        "root_sumw2": root_meta.get("sum_of_weights_squared"),
        "root_xsec_pb": root_meta.get("xsec"),
        "root_filter_eff": root_meta.get("filteff"),
        "root_k_factor": root_meta.get("kfac"),
    }


def build_metadata_rows(inputs: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    official, source_path = official_metadata_lookup()
    for path in list_root_files(inputs / "MC"):
        dsid = dsid_from_name(path)
        descriptor = descriptor_from_name(path)
        generator, simulation = generator_from_descriptor(descriptor)
        meta = read_root_metadata(path)
        if dsid in official:
            rows.append(canonical_metadata_row(official[dsid], dsid=dsid, descriptor=descriptor, generator=generator, simulation=simulation, path=path, root_meta=meta, source_path=source_path))
        else:
            rows.append(_root_fallback_row(dsid=dsid, descriptor=descriptor, generator=generator, simulation=simulation, path=path, root_meta=meta))
    return rows


def write_metadata_csv(rows: list[dict[str, Any]], path: Path) -> Path:
    ensure_dir(path.parent)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_metadata_resolution(rows: list[dict[str, Any]], outputs: Path) -> None:
    write_json(
        {
            "status": "ok",
            "column_mapping": {
                "xsec_pb": "xsec",
                "k_factor": "kfac",
                "filter_eff": "filteff",
                "sumw": "sum_of_weights",
            },
            "row_count": len(rows),
            "source": "official ATLAS Open Data metadata CSV when DSID-matched; ROOT branch metadata is diagnostic only for skimmed datasets",
            "metadata_sources": sorted({row.get("metadata_source", "unknown") for row in rows}),
            "root_metadata_policy": "Do not normalize skimmed samples to ROOT file entries or file-local sums of weights when official table metadata is available.",
        },
        outputs / "normalization" / "metadata_resolution.json",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True)
    parser.add_argument("--csv-out", default="skills/metadata.csv")
    parser.add_argument("--resolution-out", default="outputs/normalization/metadata_resolution.json")
    args = parser.parse_args()
    rows = build_metadata_rows(Path(args.inputs))
    write_metadata_csv(rows, Path(args.csv_out))
    write_metadata_resolution(rows, Path(args.resolution_out).parents[1])
    print(f"metadata rows: {len(rows)}")


if __name__ == "__main__":
    main()
