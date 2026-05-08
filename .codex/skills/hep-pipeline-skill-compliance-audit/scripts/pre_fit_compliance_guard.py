#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALLOWED_CENTRAL_ASIMOV_MODES = {"direct_generation", "binned_roodatahist", "binned_poisson"}
DEFAULT_OUTPUT = Path("outputs/report/pipeline_skill_compliance_audit.json")
SOURCE_FILES = (
    Path("analysis/stats/fit.py"),
    Path("analysis/stats/significance.py"),
    Path("analysis/stats/models.py"),
)
ARTIFACT_GLOBS = (
    "outputs/**/significance_asimov*.json",
    "outputs/**/pipeline_skill_compliance_audit.json",
    "outputs/**/pre_fit_compliance_audit.json",
    "outputs/**/background_pdf_choice.json",
    "outputs/**/fit_context*.json",
)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _read_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _flatten_json(value: Any, prefix: str = "") -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            rows.extend(_flatten_json(child, f"{prefix}.{key}" if prefix else str(key)))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            rows.extend(_flatten_json(child, f"{prefix}[{idx}]"))
    else:
        rows.append((prefix, value))
    return rows


def _finding(check_id: str, severity: str, message: str, *, path: str | None = None, evidence: str | None = None) -> dict[str, Any]:
    payload = {
        "check_id": check_id,
        "severity": severity,
        "message": message,
    }
    if path is not None:
        payload["path"] = path
    if evidence is not None:
        payload["evidence"] = evidence
    return payload


def _contains_hyy_signal(summary_path: Path, repo: Path, sources: dict[Path, str]) -> bool:
    summary_text = _read_text(summary_path).lower()
    analysis_json = " ".join(_read_text(path).lower() for path in repo.joinpath("analysis").glob("*.json"))
    source_text = " ".join(text.lower() for text in sources.values())
    haystack = "\n".join([summary_text, analysis_json, source_text])
    return any(token in haystack for token in ("h->gammagamma", "h to gammagamma", "higgs-to-diphoton", "diphoton", "m_gg", "mgg"))


def _check_static_sources(repo: Path, summary_path: Path) -> tuple[list[dict[str, Any]], list[str], dict[Path, str]]:
    findings: list[dict[str, Any]] = []
    inspected: list[str] = []
    sources: dict[Path, str] = {}
    for rel_path in SOURCE_FILES:
        path = repo / rel_path
        text = _read_text(path)
        if text:
            inspected.append(str(rel_path))
            sources[rel_path] = text
        else:
            findings.append(
                _finding(
                    "missing_static_source",
                    "warning",
                    "Expected static source file was not present; guard could not inspect this part of the fit path.",
                    path=str(rel_path),
                )
            )

    significance = sources.get(Path("analysis/stats/significance.py"), "")
    fit_source = sources.get(Path("analysis/stats/fit.py"), "")
    models = sources.get(Path("analysis/stats/models.py"), "")
    is_hyy = _contains_hyy_signal(summary_path, repo, sources)

    weighted_bin_center_asimov = bool(
        is_hyy
        and "make_weighted_bin_center_dataset" in significance
        and re.search(r"def\s+_asimov_dataset\b", significance)
        and re.search(r"_fit_with_mu\s*\([^)]*asimov_data", significance)
    )
    if weighted_bin_center_asimov:
        findings.append(
            _finding(
                "hyy_weighted_bin_center_dataset_central_path",
                "blocking",
                "Central H to gammagamma Asimov significance path builds weighted bin-center pseudo-data.",
                path="analysis/stats/significance.py",
                evidence="make_weighted_bin_center_dataset is used in _asimov_dataset and then passed to _fit_with_mu.",
            )
        )

    if is_hyy and "RooDataSet" in significance and ("WeightVar" in significance or "asimov_weight" in significance):
        findings.append(
            _finding(
                "hyy_weighted_roodataset_asimov",
                "blocking",
                "Central H to gammagamma Asimov pseudo-data uses a weighted RooDataSet.",
                path="analysis/stats/significance.py",
                evidence="RooDataSet with WeightVar/asimov_weight appears in the Asimov significance source.",
            )
        )

    if weighted_bin_center_asimov and "fitTo(" in significance and "Extended(True)" in significance:
        findings.append(
            _finding(
                "hyy_extended_unbinned_weighted_asimov_fit",
                "blocking",
                "Extended RooFit fit is applied to weighted bin-center Asimov data.",
                path="analysis/stats/significance.py",
                evidence="fitTo(... RooFit.Extended(True) ...) is present on the Asimov fit path.",
            )
        )

    mode_match = re.search(r"[\"']construction_mode[\"']\s*:\s*[\"']([^\"']+)[\"']", significance)
    if is_hyy and mode_match and mode_match.group(1) not in ALLOWED_CENTRAL_ASIMOV_MODES:
        findings.append(
            _finding(
                "hyy_central_asimov_mode_not_allowed",
                "blocking",
                "Central H to gammagamma Asimov construction mode is not one of the allowed binned/direct modes.",
                path="analysis/stats/significance.py",
                evidence=f"construction_mode={mode_match.group(1)}",
            )
        )

    if is_hyy and "\"asimov_source\": \"weighted_bin_center_dataset\"" in significance:
        findings.append(
            _finding(
                "hyy_asimov_source_not_allowed",
                "blocking",
                "Central H to gammagamma Asimov source is declared as weighted_bin_center_dataset.",
                path="analysis/stats/significance.py",
                evidence='asimov_source="weighted_bin_center_dataset"',
            )
        )

    observed_scaled_template = (
        "data_sidebands / mc_sidebands" in fit_source
        or "observed_data_sideband_count" in fit_source
        or "sideband_scale_factor" in fit_source
    )
    asimov_uses_template_yield = "template_total_yield" in significance
    if is_hyy and observed_scaled_template and asimov_uses_template_yield:
        findings.append(
            _finding(
                "hyy_observed_bound_template_asimov_mismatch",
                "blocking",
                "Observed sideband-derived normalization metadata is present while Asimov generation uses template_total_yield; this needs an explicit approved provenance check before central Asimov claims.",
                path="analysis/stats/fit.py, analysis/stats/significance.py",
                evidence="sideband_scale_factor/observed_data_sideband_count and template_total_yield both appear on the planned fit path.",
            )
        )

    if is_hyy and "make_weighted_bin_center_dataset" in models and "RooDataHist" not in significance:
        findings.append(
            _finding(
                "hyy_missing_binned_asimov_backend",
                "warning",
                "Weighted bin-center helper exists, but no RooDataHist/direct/binned Poisson Asimov path was found in significance.py.",
                path="analysis/stats/models.py",
            )
        )

    return findings, inspected, sources


def _check_artifacts(repo: Path) -> tuple[list[dict[str, Any]], list[str]]:
    findings: list[dict[str, Any]] = []
    scanned: list[str] = []
    seen: set[Path] = set()
    for pattern in ARTIFACT_GLOBS:
        for path in repo.glob(pattern):
            if path in seen or not path.is_file():
                continue
            seen.add(path)
            rel = path.relative_to(repo)
            payload = _read_json(path)
            if payload is None:
                continue
            scanned.append(str(rel))
            flat = _flatten_json(payload)
            flat_map = {key: value for key, value in flat}
            for key, value in flat:
                if key.endswith("construction_mode") and isinstance(value, str) and value not in ALLOWED_CENTRAL_ASIMOV_MODES:
                    findings.append(
                        _finding(
                            "artifact_central_asimov_mode_not_allowed",
                            "blocking",
                            "Artifact records an Asimov construction mode that is not central-claim eligible.",
                            path=str(rel),
                            evidence=f"{key}={value}",
                        )
                    )
                if key.endswith("weighted_dataset_object_type") and value == "RooDataSet":
                    findings.append(
                        _finding(
                            "artifact_weighted_roodataset_asimov",
                            "blocking",
                            "Artifact records weighted RooDataSet as Asimov data.",
                            path=str(rel),
                            evidence=f"{key}=RooDataSet",
                        )
                    )
                if key.endswith("asimov_source") and value == "weighted_bin_center_dataset":
                    findings.append(
                        _finding(
                            "artifact_weighted_bin_center_asimov_source",
                            "blocking",
                            "Artifact records weighted bin-center Asimov source.",
                            path=str(rel),
                            evidence=f"{key}=weighted_bin_center_dataset",
                        )
                    )
            if (
                flat_map.get("dataset_type") == "asimov"
                and flat_map.get("construction_mode") not in (None, *ALLOWED_CENTRAL_ASIMOV_MODES)
            ):
                findings.append(
                    _finding(
                        "artifact_asimov_dataset_mode_blocked",
                        "blocking",
                        "Asimov dataset metadata is not compatible with central H to gammagamma expected-significance claims.",
                        path=str(rel),
                    )
                )
    return findings, scanned


def run_guard(repo: Path, summary: Path, output: Path) -> dict[str, Any]:
    source_findings, inspected_sources, _sources = _check_static_sources(repo, summary)
    artifact_findings, scanned_artifacts = _check_artifacts(repo)
    findings = source_findings + artifact_findings
    blocking = [item for item in findings if item["severity"] == "blocking"]
    warnings = [item for item in findings if item["severity"] == "warning"]
    gate_outcome = "BLOCKED" if blocking else ("CONDITIONAL_PASS" if warnings else "PASS")
    status = "blocked" if blocking else ("conditional_pass" if warnings else "pass")
    payload = {
        "schema_version": "pre_fit_compliance_guard.v1",
        "updated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scope": "pre_fit",
        "mode": "pre_fit",
        "status": status,
        "gate_outcome": gate_outcome,
        "policy_invariant": "A pipeline may not execute a statistical stage capable of producing central claims unless the planned executable code path has already passed compliance audit.",
        "allowed_central_asimov_modes": sorted(ALLOWED_CENTRAL_ASIMOV_MODES),
        "repo": str(repo),
        "summary": str(summary.relative_to(repo) if summary.is_relative_to(repo) else summary),
        "inspected_static_sources": inspected_sources,
        "scanned_artifact_metadata": scanned_artifacts,
        "findings": findings,
        "blocking_findings": len(blocking),
        "warning_findings": len(warnings),
        "scorecard_update": {
            "pre_fit_compliance_audit": {
                "present": True,
                "scope": "pre_fit",
                "gate_outcome": gate_outcome,
                "artifact": str(output.relative_to(repo) if output.is_relative_to(repo) else output),
            }
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic pre-fit compliance guard for HEP analysis pipelines.")
    parser.add_argument("--repo", default=".", help="Repository root to inspect.")
    parser.add_argument("--summary", default="analysis/analysis.summary.json", help="Planned analysis summary JSON path.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Compliance artifact path.")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    summary = (repo / args.summary).resolve() if not Path(args.summary).is_absolute() else Path(args.summary)
    output = (repo / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output)
    payload = run_guard(repo, summary, output)
    print(f"pre-fit compliance gate: {payload['gate_outcome']} ({payload['blocking_findings']} blocking, {payload['warning_findings']} warning)")
    print(f"artifact: {output}")
    return 2 if payload["gate_outcome"] == "BLOCKED" else 0


if __name__ == "__main__":
    sys.exit(main())
