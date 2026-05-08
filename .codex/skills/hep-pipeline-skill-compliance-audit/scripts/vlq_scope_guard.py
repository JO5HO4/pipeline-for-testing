#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT = Path("outputs/report/vlq_scope_guard.json")
MATERIAL_RATIO_THRESHOLD = 1.5
LOW_SIGNAL_YIELD_THRESHOLD = 1.0
LOW_SIGNAL_SB_THRESHOLD = 0.05


def _read_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _first_existing(repo: Path, candidates: list[str]) -> Path | None:
    for candidate in candidates:
        path = repo / candidate
        if path.exists():
            return path
    return None


def _finding(check_id: str, severity: str, message: str, *, path: str | None = None, evidence: Any | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"check_id": check_id, "severity": severity, "message": message}
    if path is not None:
        payload["path"] = path
    if evidence is not None:
        payload["evidence"] = evidence
    return payload


def _samples_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("samples", "registry", "sample_registry", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        if all(isinstance(value, dict) for value in payload.values()):
            return [value for value in payload.values() if isinstance(value, dict)]
    return []


def _sample_id(sample: dict[str, Any]) -> str:
    for key in ("sample_id", "dsid", "dataset_number", "id"):
        if sample.get(key) is not None:
            return str(sample[key])
    return "unknown"


def _explicit_noncentral_ids(repo: Path) -> set[str]:
    ids: set[str] = set()
    for path in (repo / "analysis").glob("*.json"):
        payload = _read_json(path)
        if not isinstance(payload, dict):
            continue
        text = json.dumps(payload).lower()
        if "vector-like" not in text and "same-sign" not in text and "trilepton" not in text and "vlq" not in text:
            continue
        stack = [payload]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                if "explicit_noncentral_background_sample_ids" in value and isinstance(
                    value["explicit_noncentral_background_sample_ids"], dict
                ):
                    ids.update(str(key) for key in value["explicit_noncentral_background_sample_ids"])
                stack.extend(value.values())
            elif isinstance(value, list):
                stack.extend(value)
    return ids


def _count(payload: dict[str, Any], name: str) -> float:
    value = payload.get(name, {})
    if isinstance(value, dict):
        return float(value.get("weighted", 0.0) or 0.0)
    return 0.0


def _group_sum(groups: Any) -> float:
    if not isinstance(groups, dict):
        return 0.0
    return sum(float(value.get("weighted", 0.0) or 0.0) for value in groups.values() if isinstance(value, dict))


def _check_registry(repo: Path, findings: list[dict[str, Any]], inspected: dict[str, str | None]) -> None:
    registry_path = _first_existing(
        repo,
        [
            "outputs/vlq/samples/sample_registry.json",
            "outputs/samples/sample_registry.json",
            "outputs/preflight/samples.registry.json",
            "outputs/sample_branch_preflight/samples.registry.json",
        ],
    )
    inspected["sample_registry"] = str(registry_path.relative_to(repo)) if registry_path else None
    if registry_path is None:
        findings.append(
            _finding(
                "missing_sample_registry",
                "warning",
                "No sample registry artifact was found; sample-scope guard can only inspect static policy.",
            )
        )
        return
    samples = _samples_from_payload(_read_json(registry_path))
    explicit_noncentral = _explicit_noncentral_ids(repo)
    bad_alternatives = []
    bad_signal_alternatives = []
    for sample in samples:
        role = str(sample.get("role") or sample.get("analysis_role") or "")
        process_group = str(sample.get("process_group") or sample.get("physics_role") or "")
        sid = _sample_id(sample)
        central = bool(sample.get("central_sample", False))
        noncentral_reason = sample.get("noncentral_reason")
        descriptor = str(sample.get("descriptor") or sample.get("process_name") or sample.get("file") or "")
        alt_like = (
            role == "background_alternative"
            or sid in explicit_noncentral
            or any(token.lower() in descriptor.lower() for token in ("pthard", "herwig", "h7ue", "showersys", "_shw", "ds_dyn"))
        )
        if alt_like and central:
            bad_alternatives.append({"sample_id": sid, "role": role, "process_group": process_group, "descriptor": descriptor})
        if alt_like and not noncentral_reason:
            findings.append(
                _finding(
                    "noncentral_background_missing_reason",
                    "warning",
                    "A noncentral background alternative lacks a concrete exclusion reason.",
                    path=str(registry_path.relative_to(repo)),
                    evidence={"sample_id": sid, "descriptor": descriptor},
                )
            )
        if role == "signal_proxy_alternative" and central:
            bad_signal_alternatives.append({"sample_id": sid, "process_group": process_group, "descriptor": descriptor})
    if bad_alternatives:
        findings.append(
            _finding(
                "noncentral_background_in_central_scope",
                "blocking",
                "Generator/shower/radiation or explicit noncentral background alternatives are marked central.",
                path=str(registry_path.relative_to(repo)),
                evidence=bad_alternatives[:20],
            )
        )
    if bad_signal_alternatives:
        findings.append(
            _finding(
                "visualization_signal_alternative_in_central_scope",
                "blocking",
                "Signal alternatives intended for visualization/diagnostics are marked central.",
                path=str(registry_path.relative_to(repo)),
                evidence=bad_signal_alternatives[:20],
            )
        )


def _check_yields(repo: Path, findings: list[dict[str, Any]], inspected: dict[str, str | None]) -> None:
    yields_path = _first_existing(repo, ["outputs/vlq/yields/aggregate_yields.json", "outputs/yields/aggregate_yields.json"])
    inspected["aggregate_yields"] = str(yields_path.relative_to(repo)) if yields_path else None
    if yields_path is None:
        findings.append(
            _finding(
                "missing_aggregate_yields",
                "blocking",
                "VLQ scope guard must run after aggregate yields exist and before plots/statistics/reporting consume them.",
            )
        )
        return
    payload = _read_json(yields_path)
    regions = payload.get("regions", {}) if isinstance(payload, dict) else {}
    if not isinstance(regions, dict):
        findings.append(_finding("bad_aggregate_yields_schema", "blocking", "Aggregate yields artifact has no regions object.", path=str(yields_path.relative_to(repo))))
        return
    material = []
    low_signal = []
    alt_double_count_candidates = []
    missing_prompt_split = []
    saw_reducible_sensitive_yields = False
    for region, values in regions.items():
        if not isinstance(values, dict):
            continue
        bkg = _count(values, "background_total")
        data = _count(values, "data")
        signal = _count(values, "signal_proxy_primary")
        bkg_groups = _group_sum(values.get("background_groups"))
        alt_groups = _group_sum(values.get("background_alternative_groups"))
        if bkg_groups and not math.isclose(bkg, bkg_groups, rel_tol=1e-6, abs_tol=1e-6):
            if alt_groups and math.isclose(bkg, bkg_groups + alt_groups, rel_tol=1e-6, abs_tol=1e-6):
                alt_double_count_candidates.append({"region": region, "background_total": bkg, "central_groups": bkg_groups, "alternative_groups": alt_groups})
            else:
                findings.append(
                    _finding(
                        "background_total_not_traceable_to_central_groups",
                        "blocking",
                        "Region background_total is not traceable to the central background groups.",
                        path=str(yields_path.relative_to(repo)),
                        evidence={"region": region, "background_total": bkg, "central_groups": bkg_groups, "alternative_groups": alt_groups},
                    )
                )
        if data > 0 and bkg / data > MATERIAL_RATIO_THRESHOLD:
            material.append({"region": region, "observed_data": data, "background": bkg, "ratio_b_over_data": bkg / data})
        if bkg > 0 and data / bkg > MATERIAL_RATIO_THRESHOLD:
            material.append({"region": region, "observed_data": data, "background": bkg, "ratio_data_over_b": data / bkg})
        if signal < LOW_SIGNAL_YIELD_THRESHOLD or (bkg > 0 and signal / bkg < LOW_SIGNAL_SB_THRESHOLD):
            low_signal.append({"region": region, "signal": signal, "background": bkg, "s_over_b": None if bkg <= 0 else signal / bkg})
        if "prompt_mc_background" not in values and "reducible_mc_proxy_diagnostic" not in values:
            missing_prompt_split.append(region)
        else:
            saw_reducible_sensitive_yields = True
    if alt_double_count_candidates:
        findings.append(
            _finding(
                "noncentral_alternatives_stacked_with_nominal_background",
                "blocking",
                "A central background total appears to include background_alternative_groups.",
                path=str(yields_path.relative_to(repo)),
                evidence=alt_double_count_candidates,
            )
        )
    if missing_prompt_split:
        findings.append(
            _finding(
                "missing_prompt_reducible_yield_split",
                "blocking",
                "Same-sign/trilepton VLQ yields must expose prompt MC and reducible-MC proxy components.",
                path=str(yields_path.relative_to(repo)),
                evidence={"regions": missing_prompt_split},
            )
        )
    discrepancy_path = _first_existing(repo, ["outputs/report/data_mc_discrepancy_audit.json"])
    inspected["data_mc_discrepancy_audit"] = str(discrepancy_path.relative_to(repo)) if discrepancy_path else None
    if material and discrepancy_path is None:
        findings.append(
            _finding(
                "missing_data_mc_discrepancy_audit",
                "blocking",
                "Material data-MC discrepancies require data_mc_discrepancy_audit.json before reporting.",
                evidence=material,
            )
        )
    role_audit_path = _first_existing(
        repo,
        [
            "outputs/report/reducible_background_role_audit.json",
            "outputs/vlq/samples/reducible_background_role_audit.json",
            "outputs/samples/reducible_background_role_audit.json",
        ],
    )
    inspected["reducible_background_role_audit"] = str(role_audit_path.relative_to(repo)) if role_audit_path else None
    if saw_reducible_sensitive_yields and role_audit_path is None:
        findings.append(
            _finding(
                "missing_reducible_background_role_audit",
                "blocking",
                "Same-sign/trilepton VLQ yields require a reducible-background role audit before central background labels.",
            )
        )
    viability_path = _first_existing(repo, ["outputs/report/signal_proxy_viability_audit.json"])
    inspected["signal_proxy_viability_audit"] = str(viability_path.relative_to(repo)) if viability_path else None
    if low_signal and viability_path is None:
        findings.append(
            _finding(
                "missing_signal_proxy_viability_audit",
                "blocking",
                "Low or invisible signal proxy regions require signal_proxy_viability_audit.json before sensitivity language.",
                evidence=low_signal,
            )
        )


def _check_report_labels(repo: Path, findings: list[dict[str, Any]], inspected: dict[str, str | None]) -> None:
    report_path = _first_existing(repo, ["outputs/vlq/report/final_report.md", "outputs/report/final_report.md", "reports/final_report.md"])
    inspected["final_report"] = str(report_path.relative_to(repo)) if report_path else None
    if report_path is None:
        return
    text = _read_text(report_path)
    if re.search(r"Expected background|Background used for stat|total background|MC prediction", text, flags=re.IGNORECASE) and not re.search(
        r"diagnostic MC|reducible_mc_proxy|prompt.*reducible", text, flags=re.IGNORECASE | re.DOTALL
    ):
        findings.append(
            _finding(
                "vlq_report_background_label_overclaims",
                "blocking",
                "VLQ same-sign/trilepton report labels raw MC stack like a validated expected background without diagnostic/proxy wording.",
                path=str(report_path.relative_to(repo)),
            )
        )


def run_guard(repo: Path, output: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    inspected: dict[str, str | None] = {}
    _check_registry(repo, findings, inspected)
    _check_yields(repo, findings, inspected)
    _check_report_labels(repo, findings, inspected)
    blocking = [item for item in findings if item["severity"] == "blocking"]
    warnings = [item for item in findings if item["severity"] == "warning"]
    gate_outcome = "BLOCKED" if blocking else ("CONDITIONAL_PASS" if warnings else "PASS")
    payload = {
        "schema_version": "vlq_scope_guard.v1",
        "updated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scope": "pre_plot_stat_report",
        "status": "blocked" if blocking else ("conditional_pass" if warnings else "pass"),
        "gate_outcome": gate_outcome,
        "material_ratio_threshold": MATERIAL_RATIO_THRESHOLD,
        "low_signal_yield_threshold": LOW_SIGNAL_YIELD_THRESHOLD,
        "low_signal_s_over_b_threshold": LOW_SIGNAL_SB_THRESHOLD,
        "inspected_artifacts": inspected,
        "findings": findings,
        "blocking_findings": len(blocking),
        "warning_findings": len(warnings),
        "scorecard_update": {
            "sample_scope_guard": {"present": True, "gate_outcome": gate_outcome, "artifact": str(output.relative_to(repo) if output.is_relative_to(repo) else output)},
            "data_mc_discrepancy_audit": {"present": inspected.get("data_mc_discrepancy_audit") is not None, "artifact": inspected.get("data_mc_discrepancy_audit") or "missing"},
            "reducible_background_role_audit": {
                "present": inspected.get("reducible_background_role_audit") is not None,
                "artifact": inspected.get("reducible_background_role_audit") or "missing",
            },
            "signal_proxy_viability_audit": {"present": inspected.get("signal_proxy_viability_audit") is not None, "artifact": inspected.get("signal_proxy_viability_audit") or "missing"},
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic VLQ sample-scope and diagnostic-claim guard.")
    parser.add_argument("--repo", default=".", help="Repository root to inspect.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output guard artifact.")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    output = (repo / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output)
    payload = run_guard(repo, output)
    print(f"VLQ scope gate: {payload['gate_outcome']} ({payload['blocking_findings']} blocking, {payload['warning_findings']} warning)")
    print(f"artifact: {output}")
    return 2 if payload["gate_outcome"] == "BLOCKED" else 0


if __name__ == "__main__":
    sys.exit(main())
