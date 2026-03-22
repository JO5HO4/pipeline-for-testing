from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import ROOT

from analysis.common import write_json
from analysis.stats.fit import FIT_ID
from analysis.stats.models import make_weighted_bin_center_dataset, pdf_to_counts

ROOT.gROOT.SetBatch(True)


def _set_generation_snapshot(fit_context: dict) -> None:
    for category, model_ctx in fit_context["final_models"].items():
        choice = fit_context["category_context"][category]["background_choice"]
        for param in model_ctx["background_params"]:
            source_key = param.GetName().replace(f"final_{category}", f"side_{category}")
            if source_key in choice["sideband_param_snapshot"]:
                param.setVal(choice["sideband_param_snapshot"][source_key])
            param.setConstant(False)
        model_ctx["nbkg"].setVal(float(fit_context["category_context"][category]["template_total_yield"]))
        model_ctx["nbkg"].setConstant(False)


def _snapshot_fit_state(fit_context: dict) -> dict[str, Any]:
    shared_mu = fit_context["shared_mu"]
    snapshot = {
        "shared_mu": {
            "value": float(shared_mu.getVal()),
            "error": float(shared_mu.getError()),
            "constant": bool(shared_mu.isConstant()),
        },
        "categories": {},
    }
    for category, model_ctx in fit_context["final_models"].items():
        snapshot["categories"][category] = {
            "nbkg": {
                "value": float(model_ctx["nbkg"].getVal()),
                "error": float(model_ctx["nbkg"].getError()),
                "constant": bool(model_ctx["nbkg"].isConstant()),
            },
            "background_params": {
                param.GetName(): {
                    "value": float(param.getVal()),
                    "error": float(param.getError()),
                    "constant": bool(param.isConstant()),
                }
                for param in model_ctx["background_params"]
            },
        }
    return snapshot


def _restore_fit_state(fit_context: dict, snapshot: dict[str, Any]) -> None:
    shared_mu = fit_context["shared_mu"]
    shared_mu.setVal(snapshot["shared_mu"]["value"])
    shared_mu.setConstant(snapshot["shared_mu"]["constant"])
    shared_mu.setError(snapshot["shared_mu"]["error"])

    for category, model_ctx in fit_context["final_models"].items():
        category_snapshot = snapshot["categories"].get(category, {})
        nbkg_snapshot = category_snapshot.get("nbkg")
        if nbkg_snapshot is not None:
            model_ctx["nbkg"].setVal(nbkg_snapshot["value"])
            model_ctx["nbkg"].setConstant(nbkg_snapshot["constant"])
            model_ctx["nbkg"].setError(nbkg_snapshot["error"])
        for param in model_ctx["background_params"]:
            param_snapshot = category_snapshot.get("background_params", {}).get(param.GetName())
            if param_snapshot is None:
                continue
            param.setVal(param_snapshot["value"])
            param.setConstant(param_snapshot["constant"])
            param.setError(param_snapshot["error"])


def _capture_model_counts(fit_context: dict) -> dict[str, dict[str, list[float]]]:
    category_payload: dict[str, dict[str, list[float]]] = {}
    for category, model_ctx in fit_context["final_models"].items():
        signal_counts = pdf_to_counts(
            model_ctx["signal_pdf"],
            fit_context["common_mass"],
            float(model_ctx["nsig"].getVal()),
        )
        background_counts = pdf_to_counts(
            model_ctx["background_pdf"],
            fit_context["common_mass"],
            float(model_ctx["nbkg"].getVal()),
        )
        total_counts = signal_counts + background_counts
        category_payload[category] = {
            "signal_counts": signal_counts.tolist(),
            "background_counts": background_counts.tolist(),
            "total_counts": total_counts.tolist(),
        }
    return category_payload


def _combined_counts(category_payload: dict[str, dict[str, list[float]]]) -> dict[str, list[float]]:
    if not category_payload:
        zeros = [0.0] * 55
        return {
            "signal_counts": zeros,
            "background_counts": zeros,
            "total_counts": zeros,
        }
    signal = [
        sum(float(payload["signal_counts"][idx]) for payload in category_payload.values())
        for idx in range(55)
    ]
    background = [
        sum(float(payload["background_counts"][idx]) for payload in category_payload.values())
        for idx in range(55)
    ]
    total = [signal[idx] + background[idx] for idx in range(55)]
    return {
        "signal_counts": signal,
        "background_counts": background,
        "total_counts": total,
    }


def _asimov_plot_payload(
    *,
    fit_context: dict,
    asimov_payload: dict[str, Any],
    fit_range: list[float],
    mu_hat: float,
    mu_uncertainty: float,
    free_result,
    mu0_result,
    free_fit_counts: dict[str, dict[str, list[float]]],
    mu0_fit_counts: dict[str, dict[str, list[float]]],
) -> dict[str, Any]:
    categories = {}
    for category, payload in asimov_payload.items():
        categories[category] = {
            "asimov_counts": payload["total_counts"],
            "generation_signal_counts": payload["signal_counts"],
            "generation_background_counts": payload["background_counts"],
            "free_fit": free_fit_counts[category],
            "mu0_fit": mu0_fit_counts[category],
        }

    combined_asimov = {
        "signal_counts": [
            sum(float(payload["signal_counts"][idx]) for payload in asimov_payload.values())
            for idx in range(55)
        ] if asimov_payload else [0.0] * 55,
        "background_counts": [
            sum(float(payload["background_counts"][idx]) for payload in asimov_payload.values())
            for idx in range(55)
        ] if asimov_payload else [0.0] * 55,
    }
    combined_asimov["total_counts"] = [
        combined_asimov["signal_counts"][idx] + combined_asimov["background_counts"][idx]
        for idx in range(55)
    ]

    return {
        "status": "ok",
        "fit_id": FIT_ID,
        "dataset_type": "asimov",
        "generation_hypothesis": "signal_plus_background",
        "mu_gen": 1.0,
        "binning": {"observable": "m_gg", "n_bins": 55, "range": fit_range},
        "categories": categories,
        "combined": {
            "asimov_counts": combined_asimov["total_counts"],
            "generation_signal_counts": combined_asimov["signal_counts"],
            "generation_background_counts": combined_asimov["background_counts"],
            "free_fit": _combined_counts(free_fit_counts),
            "mu0_fit": _combined_counts(mu0_fit_counts),
        },
        "free_fit": {
            "mu_hat": mu_hat,
            "mu_uncertainty": mu_uncertainty,
            "fit_status": int(free_result.status()),
            "cov_qual": int(free_result.covQual()),
        },
        "mu0_fit": {
            "mu_fixed": 0.0,
            "fit_status": int(mu0_result.status()),
            "cov_qual": int(mu0_result.covQual()),
        },
    }


def _asimov_dataset(fit_context: dict):
    _set_generation_snapshot(fit_context)
    common_mass = fit_context["common_mass"]
    channel = fit_context["channel"]
    shared_mu = fit_context["shared_mu"]
    shared_mu.setVal(1.0)
    shared_mu.setConstant(False)

    import_map = {}
    category_payload = {}
    for category, model_ctx in fit_context["final_models"].items():
        signal_yield = float(model_ctx["s_const"].getVal())
        background_yield = float(fit_context["category_context"][category]["template_total_yield"])
        signal_counts = pdf_to_counts(model_ctx["signal_pdf"], common_mass, signal_yield)
        background_counts = pdf_to_counts(model_ctx["background_pdf"], common_mass, background_yield)
        total_counts = signal_counts + background_counts
        dataset = make_weighted_bin_center_dataset(f"asimov_{category}", common_mass, total_counts)
        import_map[category] = dataset
        category_payload[category] = {
            "signal_counts": signal_counts.tolist(),
            "background_counts": background_counts.tolist(),
            "total_counts": total_counts.tolist(),
        }
    combined = ROOT.RooDataSet(
        "asimovData",
        "asimovData",
        ROOT.RooArgSet(common_mass, channel),
        Index=channel,
        Import=import_map,
    )
    return combined, category_payload


def _free_parameter_policy(observed_significance_allowed: bool) -> dict[str, Any]:
    return {
        "observed_significance_allowed": bool(observed_significance_allowed),
        "explicit_unblinding_required": True,
        "explicit_unblinding_performed": bool(observed_significance_allowed),
        "signal_shape_parameter_policy": "fixed_from_signal_mc_fit",
        "signal_strength_parameter": "mu",
        "background_parameter_policy": "floating_shape_and_normalization",
        "background_parameter_source": "mu=0 sideband data-fit snapshot from background_pdf_choice.json",
    }


def _background_parameter_source(summary: dict, fit_dir: Path) -> dict[str, Any]:
    return {
        "source_artifact": str(fit_dir / "background_pdf_choice.json"),
        "fit_hypothesis": "mu=0 background-only sideband data fit",
        "sideband_ranges_gev": summary["runtime_defaults"]["sidebands_gev"],
    }


def _fit_with_mu(fit_context: dict, dataset, *, mu_value: float | None):
    shared_mu = fit_context["shared_mu"]
    if mu_value is None:
        shared_mu.setConstant(False)
    else:
        shared_mu.setVal(float(mu_value))
        shared_mu.setConstant(True)
    return fit_context["simultaneous"].fitTo(
        dataset,
        ROOT.RooFit.Save(True),
        ROOT.RooFit.PrintLevel(-1),
        ROOT.RooFit.Strategy(1),
        ROOT.RooFit.SumW2Error(False),
        ROOT.RooFit.Extended(True),
        ROOT.RooFit.Range("full"),
    )


def _blocked_observed_artifact(
    *,
    fit_context: dict,
    fit_range: list[float],
    signal_window: list[float],
    blinding: dict[str, Any],
) -> dict[str, Any]:
    return {
        "fit_id": FIT_ID,
        "status": "blocked",
        "dataset_type": "observed",
        "backend": "pyroot_roofit",
        "poi_name": "signal_strength_mu",
        "observed_significance_allowed": bool(blinding["observed_significance_allowed"]),
        "fit_range": fit_range,
        "blind_window_in_observed_data": signal_window,
        "categories": fit_context["fit_summary"]["categories"],
        "shared_mu": True,
        "signal_shape_parameter_policy": "fixed_from_signal_mc_fit",
        "background_parameter_policy": "floating_shape_and_normalization",
        "error": "Observed significance is disabled by blinding policy; central claims use Asimov expected significance only.",
    }


def _observed_significance(
    *,
    fit_context: dict,
    fit_range: list[float],
    signal_window: list[float],
    blinding: dict[str, Any],
    background_parameter_source: dict[str, Any],
) -> dict[str, Any]:
    measurement_snapshot = _snapshot_fit_state(fit_context)
    shared_mu = fit_context["shared_mu"]
    shared_mu.setVal(1.0)

    free_result = _fit_with_mu(fit_context, fit_context["combined_data"], mu_value=None)
    twice_nll_free = 2.0 * float(free_result.minNll())
    mu_hat = float(shared_mu.getVal())
    mu_uncertainty = float(shared_mu.getError())

    mu0_result = _fit_with_mu(fit_context, fit_context["combined_data"], mu_value=0.0)
    twice_nll_mu0 = 2.0 * float(mu0_result.minNll())
    q0_raw = max(twice_nll_mu0 - twice_nll_free, 0.0)
    q0 = q0_raw if mu_hat > 0.0 else 0.0
    z_discovery = math.sqrt(q0)
    shared_mu.setConstant(False)

    diagnostics = []
    if free_result.status() != 0:
        diagnostics.append("Free-mu observed significance fit returned a non-zero RooFit status.")
    if mu0_result.status() != 0:
        diagnostics.append("Mu=0 observed significance fit returned a non-zero RooFit status.")
    if free_result.covQual() < 2:
        diagnostics.append("Free-mu observed significance fit covariance quality is below the acceptable threshold of 2.")
    if mu0_result.covQual() < 2:
        diagnostics.append("Mu=0 observed significance fit covariance quality is below the acceptable threshold of 2.")
    if mu_hat <= 0.0:
        diagnostics.append("Best-fit signal strength is non-positive, so the one-sided discovery test statistic is clipped to q0 = 0.")
    status = "ok" if not diagnostics else "warning"

    artifact = {
        "fit_id": FIT_ID,
        "status": status,
        "dataset_type": "observed",
        "backend": "pyroot_roofit",
        "poi_name": "signal_strength_mu",
        "mu_hat": mu_hat,
        "mu_uncertainty": mu_uncertainty,
        "twice_nll_mu0": twice_nll_mu0,
        "twice_nll_free": twice_nll_free,
        "q0": q0,
        "z_discovery": z_discovery,
        "fit_range": fit_range,
        "blind_window_in_observed_data": signal_window if blinding["plot_signal_window"] else None,
        "observed_significance_allowed": bool(blinding["observed_significance_allowed"]),
        "signal_shape_parameter_policy": "fixed_from_signal_mc_fit",
        "background_parameter_policy": "floating_shape_and_normalization",
        "background_parameter_source": background_parameter_source,
        "categories": fit_context["fit_summary"]["categories"],
        "shared_mu": True,
        "fit_status_free": int(free_result.status()),
        "fit_status_mu0": int(mu0_result.status()),
        "cov_qual_free": int(free_result.covQual()),
        "cov_qual_mu0": int(mu0_result.covQual()),
        "diagnostics": diagnostics,
    }
    _restore_fit_state(fit_context, measurement_snapshot)
    return artifact


def run_significance(fit_context: dict, summary: dict, outputs: Path) -> dict[str, Any]:
    fit_dir = outputs / "fit" / FIT_ID
    fit_range = summary["runtime_defaults"]["fit_mass_range_gev"]
    signal_window = summary["runtime_defaults"]["signal_window_gev"]
    blinding = summary["runtime_defaults"]["blinding"]
    policy = _free_parameter_policy(bool(blinding["observed_significance_allowed"]))
    write_json(policy, fit_dir / "significance_parameter_policy.json")
    background_parameter_source = _background_parameter_source(summary, fit_dir)

    if blinding["observed_significance_allowed"]:
        observed_artifact = _observed_significance(
            fit_context=fit_context,
            fit_range=fit_range,
            signal_window=signal_window,
            blinding=blinding,
            background_parameter_source=background_parameter_source,
        )
    else:
        observed_artifact = _blocked_observed_artifact(
            fit_context=fit_context,
            fit_range=fit_range,
            signal_window=signal_window,
            blinding=blinding,
        )
    write_json(observed_artifact, fit_dir / "significance.json")

    measurement_snapshot = _snapshot_fit_state(fit_context)
    asimov_data, asimov_payload = _asimov_dataset(fit_context)
    shared_mu = fit_context["shared_mu"]
    simultaneous = fit_context["simultaneous"]

    shared_mu.setVal(1.0)
    free_result = _fit_with_mu(fit_context, asimov_data, mu_value=None)
    twice_nll_free = 2.0 * float(free_result.minNll())
    mu_hat = float(shared_mu.getVal())
    mu_uncertainty = float(shared_mu.getError())
    free_fit_counts = _capture_model_counts(fit_context)

    mu0_result = _fit_with_mu(fit_context, asimov_data, mu_value=0.0)
    twice_nll_mu0 = 2.0 * float(mu0_result.minNll())
    q0 = max(twice_nll_mu0 - twice_nll_free, 0.0)
    z_discovery = math.sqrt(q0)
    mu0_fit_counts = _capture_model_counts(fit_context)
    shared_mu.setConstant(False)

    diagnostics = []
    if free_result.status() != 0:
        diagnostics.append("Free-mu Asimov significance fit returned a non-zero RooFit status.")
    if mu0_result.status() != 0:
        diagnostics.append("Mu=0 Asimov significance fit returned a non-zero RooFit status.")
    if free_result.covQual() < 2:
        diagnostics.append("Free-mu Asimov significance fit covariance quality is below the acceptable threshold of 2.")
    if mu0_result.covQual() < 2:
        diagnostics.append("Mu=0 Asimov significance fit covariance quality is below the acceptable threshold of 2.")
    status = "ok" if not diagnostics else "warning"
    asimov_artifact = {
        "fit_id": FIT_ID,
        "status": status,
        "dataset_type": "asimov",
        "generation_hypothesis": "signal_plus_background",
        "mu_gen": 1.0,
        "backend": "pyroot_roofit",
        "poi_name": "signal_strength_mu",
        "mu_hat": mu_hat,
        "mu_uncertainty": mu_uncertainty,
        "twice_nll_mu0": twice_nll_mu0,
        "twice_nll_free": twice_nll_free,
        "q0": q0,
        "z_discovery": z_discovery,
        "fit_range": fit_range,
        "background_parameter_source": background_parameter_source,
        "asimov_source": "weighted_bin_center_dataset",
        "observed_significance_allowed": bool(blinding["observed_significance_allowed"]),
        "signal_shape_parameter_policy": "fixed_from_signal_mc_fit",
        "background_parameter_policy": "floating_shape_and_normalization",
        "categories": fit_context["fit_summary"]["categories"],
        "shared_mu": True,
        "fit_status_free": int(free_result.status()),
        "fit_status_mu0": int(mu0_result.status()),
        "cov_qual_free": int(free_result.covQual()),
        "cov_qual_mu0": int(mu0_result.covQual()),
        "diagnostics": diagnostics,
    }
    construction_artifact = {
        "fit_id": FIT_ID,
        "status": "ok",
        "dataset_type": "asimov",
        "generation_range": fit_range,
        "blind_window_in_observed_data": summary["runtime_defaults"]["signal_window_gev"],
        "construction_mode": "weighted_bin_center_dataset",
        "binning": {"observable": "m_gg", "n_bins": 55, "range": fit_range},
        "weighted_dataset_object_type": "RooDataSet",
        "fixed_generation_inputs": [
            "signal yield normalized to MC prediction",
            "signal DSCB shape parameters from the signal-MC fit",
            "background PDF parameters from the mu=0 sideband-data fit snapshot",
        ],
        "floating_fit_parameters": [
            "signal strength mu",
            "background normalization",
            "background shape parameters",
        ],
        "category_payload": asimov_payload,
    }
    plot_payload = _asimov_plot_payload(
        fit_context=fit_context,
        asimov_payload=asimov_payload,
        fit_range=fit_range,
        mu_hat=mu_hat,
        mu_uncertainty=mu_uncertainty,
        free_result=free_result,
        mu0_result=mu0_result,
        free_fit_counts=free_fit_counts,
        mu0_fit_counts=mu0_fit_counts,
    )

    _restore_fit_state(fit_context, measurement_snapshot)
    fit_context["asimov_plot_payload"] = plot_payload

    write_json(asimov_artifact, fit_dir / "significance_asimov.json")
    write_json(construction_artifact, fit_dir / "significance_asimov_construction.json")
    write_json(plot_payload, fit_dir / "significance_asimov_plot_payload.json")
    return {
        "observed": observed_artifact,
        "asimov": asimov_artifact,
        "construction": construction_artifact,
        "plot_payload": plot_payload,
        "policy": policy,
    }
