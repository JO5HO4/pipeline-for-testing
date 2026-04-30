from __future__ import annotations

import argparse
import math
import os
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import awkward as ak
import matplotlib
import numpy as np
import uproot

from analysis.common import ensure_dir, list_root_files, read_json, stable_hash, utcnow_iso, write_json, write_text

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


LUMI_FB = 36.1
TREE_NAME = "analysis"
BTAG_MV2C10_70_WP = 0.8244273
BACKGROUND_REL_UNCERTAINTY = 0.30

BRANCH_CANDIDATES: dict[str, list[str]] = {
    "event": ["eventNumber", "event_number"],
    "run": ["runNumber", "run_number"],
    "mc_weight": ["mcWeight", "weight_mc", "generatorWeight"],
    "lep_pt": ["lep_pt", "lepton_pt"],
    "lep_eta": ["lep_eta", "lepton_eta"],
    "lep_phi": ["lep_phi", "lepton_phi"],
    "lep_charge": ["lep_charge", "lepton_charge"],
    "lep_type": ["lep_type", "lepton_type", "lep_flavour", "lepton_flavour"],
    "lep_tight": ["lep_isTightID", "lep_isTight", "lepton_isTightID"],
    "lep_ptcone": ["lep_ptvarcone30", "lep_ptcone30", "lep_ptcone20", "lepton_ptcone30"],
    "lep_etcone": ["lep_topoetcone20", "lep_etcone20", "lepton_etcone20"],
    "jet_pt": ["jet_pt"],
    "jet_eta": ["jet_eta"],
    "jet_phi": ["jet_phi"],
    "jet_btag": ["jet_btag_quantile", "jet_MV2c10", "jet_mv2c10", "jet_btag", "jet_isbtagged", "jet_isbtagged_70"],
    "met": ["met_et", "met_met", "MET", "met"],
    "trig_e": ["trigE", "trigger_e", "passTrigE"],
    "trig_m": ["trigM", "trigger_m", "passTrigM"],
    "sig_lep": ["sig_lep"],
    "n_sig_lep": ["n_sig_lep"],
}

META_BRANCHES = [
    "num_events",
    "sum_of_weights",
    "sum_of_weights_squared",
    "xsec",
    "filteff",
    "kfac",
    "channelNumber",
]

SCALE_FACTOR_CANDIDATES = [
    "ScaleFactor_PILEUP",
    "ScaleFactor_ELE",
    "ScaleFactor_MUON",
    "ScaleFactor_BTAG",
    "ScaleFactor_JVT",
]

CUTFLOW_STEPS = [
    "all_events",
    "trigger",
    "two_or_more_selected_leptons",
    "same_sign_dilepton_or_trilepton",
    "one_or_more_selected_jets",
    "one_or_more_btags",
    "any_signal_region",
]

HIST_SPECS = {
    "ht": {"bins": np.linspace(0.0, 2200.0, 45), "xlabel": "H_T [GeV]"},
    "met": {"bins": np.linspace(0.0, 800.0, 41), "xlabel": "E_T^miss [GeV]"},
    "n_jets": {"bins": np.arange(-0.5, 12.5, 1.0), "xlabel": "selected jet multiplicity"},
    "n_btags": {"bins": np.arange(-0.5, 6.5, 1.0), "xlabel": "b-tagged jet multiplicity"},
    "n_leptons": {"bins": np.arange(-0.5, 6.5, 1.0), "xlabel": "selected lepton multiplicity"},
}

PLOT_COLORS = {
    "ttbar": "#4C78A8",
    "rare_top": "#F58518",
    "wjets": "#54A24B",
    "zjets": "#B279A2",
    "diboson_triboson": "#E45756",
    "higgs": "#72B7B2",
    "multijet_photon": "#EECA3B",
    "other_sm": "#9D755D",
}


@dataclass(frozen=True)
class RegionSpec:
    name: str
    search_family: str
    lepton_category: str
    lepton_flavour_treatment: str
    charge_requirement: str
    n_jets_min: int
    n_jets_max: int | None
    n_btags_min: int
    n_btags_max: int | None
    ht_min: float
    met_min: float
    dphi_min: float | None
    dphi_max: float | None


def _limit_value(payload: Any, key: str, default: float | None) -> float | None:
    if not isinstance(payload, dict):
        return default
    value = payload.get(key, default)
    if value in {None, "not_specified"}:
        return default
    return float(value)


def _int_limit(payload: Any, key: str, default: int | None) -> int | None:
    value = _limit_value(payload, key, default)
    return None if value is None else int(value)


def parse_regions(summary: dict[str, Any]) -> list[RegionSpec]:
    regions: list[RegionSpec] = []
    for item in summary.get("signal_regions", []):
        regions.append(
            RegionSpec(
                name=str(item["region_name"]),
                search_family=str(item.get("search_family", "unspecified")),
                lepton_category=str(item.get("lepton_category", "2l")),
                lepton_flavour_treatment=str(item.get("lepton_flavour_treatment", "inclusive")),
                charge_requirement=str(item.get("lepton_charge_requirement", "")),
                n_jets_min=_int_limit(item.get("n_jets"), "min", 0) or 0,
                n_jets_max=_int_limit(item.get("n_jets"), "max", None),
                n_btags_min=_int_limit(item.get("n_btags"), "min", 0) or 0,
                n_btags_max=_int_limit(item.get("n_btags"), "max", None),
                ht_min=_limit_value(item.get("HT_GeV"), "min", 0.0) or 0.0,
                met_min=_limit_value(item.get("ETmiss_GeV"), "min", 0.0) or 0.0,
                dphi_min=_limit_value(item.get("delta_phi_ll_radians"), "min", None),
                dphi_max=_limit_value(item.get("delta_phi_ll_radians"), "max", None),
            )
        )
    return regions


def _descriptor_from_mc_name(path: Path) -> tuple[str, str]:
    match = re.search(r"_mc_(\d+)\.(.+?)\.1LMET30\.root$", path.name)
    if match:
        return match.group(1), match.group(2)
    fallback = re.search(r"_mc_(\d+)\.(.+?)\.root$", path.name)
    if fallback:
        return fallback.group(1), fallback.group(2)
    return path.stem, path.stem


def _data_id(path: Path) -> str:
    return path.name.replace("ODEO_FEB2025_v0_1LMET30_", "").replace(".1LMET30.root", "")


def _classify_sample(descriptor: str, dsid: str) -> tuple[str, str, str]:
    text = descriptor.lower()
    if dsid == "412043" or "sm4topsnlo" in text:
        return "signal_proxy_primary", "four_top_signal_proxy", "SM four-top proxy signal"
    if dsid == "412044":
        return "signal_proxy_alternative", "four_top_signal_proxy_alt", "SM four-top alternate-shower proxy"
    bsm_tokens = [
        "tt_rpv",
        "tt_tn1",
        "gg_ttn1",
        "gg_direct",
        "dm_4top",
        "higgsinorpv",
        "wp_l",
        "wpl_",
        "zprime",
        "wprime",
        "lq",
        "ggm",
        "c1n2",
        "n2c1",
        "stau",
        "ss_onestep",
        "2dp20",
        "rpvdirect",
    ]
    if any(token in text for token in bsm_tokens):
        return "signal_proxy_alternative", "bsm_signal_alternative", "BSM signal alternative"
    if "ttw" in text or "ttz" in text or "ttgamma" in text or "ttbarww" in text or "3top" in text or "twz" in text or "tz_" in text:
        return "background", "rare_top", "ttV/rare-top background"
    if "ttbar" in text or re.search(r"(^|_)tt(_|$)", text) or "singlelep" in text or "dil" in text or "tchan" in text or "schan" in text or "tw_dyn" in text:
        return "background", "ttbar", "top background"
    if re.search(r"(^|_)w(enu|munu|taunu|qq|lv)", text) or "wjets" in text:
        return "background", "wjets", "W+jets background"
    if re.search(r"(^|_)z(ee|mumu|tautau|nunu|bb|qq|tt)", text) or "zjets" in text or "ptz" in text:
        return "background", "zjets", "Z+jets background"
    if any(token in text for token in ["llll", "lllv", "llvv", "wlvz", "wqqz", "zzz", "vv", "www", "wwz", "wzz", "yyy"]):
        return "background", "diboson_triboson", "diboson/triboson background"
    if any(token in text for token in ["ggh125", "vbfh125", "wh125", "zh125", "tth125", "hyy", "gamgam", "hgam", "hzz", "htautau"]):
        return "background", "higgs", "Higgs background"
    if any(token in text for token in ["jetjet", "gammajet", "singlephoton", "diphoton", "gamma", "eegamma", "mugamma"]):
        return "background", "multijet_photon", "multijet/photon-associated background"
    return "background", "other_sm", "other SM background"


def _resolve_branches(fields: set[str]) -> dict[str, str | None]:
    return {key: next((candidate for candidate in candidates if candidate in fields), None) for key, candidates in BRANCH_CANDIDATES.items()}


def _required_missing(branches: dict[str, str | None]) -> list[str]:
    required = ["lep_pt", "lep_eta", "lep_phi", "lep_charge", "jet_pt", "jet_eta", "jet_phi", "jet_btag", "met"]
    return [key for key in required if branches.get(key) is None]


def _read_metadata(path: Path) -> dict[str, Any]:
    with uproot.open(path) as handle:
        tree = handle[TREE_NAME]
        fields = set(tree.keys())
        out = {"entries": int(tree.num_entries)}
        wanted = [branch for branch in META_BRANCHES if branch in fields]
        if wanted:
            arrays = tree.arrays(wanted, entry_stop=1, library="np")
            for branch in wanted:
                value = arrays[branch][0]
                out[branch] = float(value)
        return out


def _norm_factor(sample: dict[str, Any]) -> float:
    if sample["kind"] == "data":
        return 1.0
    denom = float(sample.get("sum_of_weights") or sample.get("num_events") or sample.get("entries") or 0.0)
    xsec = float(sample.get("xsec") or 0.0)
    kfac = float(sample.get("kfac") or 1.0)
    filteff = float(sample.get("filteff") or 1.0)
    if denom == 0.0 or xsec == 0.0:
        return 1.0
    return xsec * kfac * filteff * LUMI_FB * 1000.0 / denom


def discover_samples(inputs: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    unreadable: list[dict[str, str]] = []
    for path in list_root_files(inputs / "data"):
        try:
            meta = _read_metadata(path)
        except Exception as exc:  # pragma: no cover - recorded in run artifacts
            unreadable.append({"file": str(path), "reason": repr(exc)})
            continue
        samples.append(
            {
                "sample_id": _data_id(path),
                "kind": "data",
                "role": "observed_data",
                "process_group": "data",
                "process_name": "observed data",
                "descriptor": "data",
                "file": str(path),
                "entries": meta["entries"],
                "norm_factor": 1.0,
            }
        )
    for path in list_root_files(inputs / "MC"):
        try:
            meta = _read_metadata(path)
        except Exception as exc:  # pragma: no cover - recorded in run artifacts
            unreadable.append({"file": str(path), "reason": repr(exc)})
            continue
        dsid, descriptor = _descriptor_from_mc_name(path)
        role, group, process_name = _classify_sample(descriptor, dsid)
        sample = {
            "sample_id": dsid,
            "kind": "mc",
            "role": role,
            "process_group": group,
            "process_name": process_name,
            "descriptor": descriptor,
            "file": str(path),
            "entries": meta["entries"],
            "num_events": meta.get("num_events"),
            "sum_of_weights": meta.get("sum_of_weights"),
            "sum_of_weights_squared": meta.get("sum_of_weights_squared"),
            "xsec": meta.get("xsec"),
            "filteff": meta.get("filteff"),
            "kfac": meta.get("kfac"),
            "channelNumber": meta.get("channelNumber"),
        }
        sample["norm_factor"] = _norm_factor(sample)
        samples.append(sample)
    primary_signal = [sample["sample_id"] for sample in samples if sample["role"] == "signal_proxy_primary"]
    return samples, {"unreadable_files": unreadable, "primary_signal_samples": primary_signal}


def _empty_count() -> dict[str, float | int]:
    return {"weighted": 0.0, "sumw2": 0.0, "unweighted": 0}


def _add_count(counter: dict[str, float | int], weights: np.ndarray, mask: np.ndarray) -> None:
    selected = weights[mask]
    counter["weighted"] = float(counter["weighted"]) + float(np.sum(selected))
    counter["sumw2"] = float(counter["sumw2"]) + float(np.sum(selected * selected))
    counter["unweighted"] = int(counter["unweighted"]) + int(np.sum(mask))


def _ak_numpy(values: Any, default: float = 0.0) -> np.ndarray:
    return np.asarray(ak.to_numpy(ak.fill_none(values, default)))


def _event_factor(values: Any, n_events: int) -> np.ndarray:
    try:
        out = np.asarray(ak.to_numpy(ak.fill_none(values, 1.0)), dtype=float)
        if out.shape == (n_events,):
            out[~np.isfinite(out)] = 1.0
            return out
    except Exception:
        pass
    try:
        out = np.asarray(ak.to_numpy(ak.prod(ak.fill_none(values, 1.0), axis=-1)), dtype=float)
        if out.shape == (n_events,):
            out[~np.isfinite(out)] = 1.0
            return out
    except Exception:
        pass
    return np.ones(n_events, dtype=float)


def _infer_scale(values: Any) -> float:
    try:
        flat = np.asarray(ak.to_numpy(ak.flatten(values, axis=None)), dtype=float)
        flat = flat[np.isfinite(flat) & (flat > 0.0)]
    except Exception:
        flat = np.array([], dtype=float)
    if flat.size == 0:
        return 1.0
    return 0.001 if float(np.nanmedian(flat)) > 1000.0 else 1.0


def _as_bool(values: Any, n_events: int) -> np.ndarray:
    try:
        out = np.asarray(ak.to_numpy(values), dtype=bool)
        if out.shape == (n_events,):
            return out
    except Exception:
        pass
    return np.zeros(n_events, dtype=bool)


def _delta_phi(phi1: Any, phi2: Any) -> Any:
    return np.arctan2(np.sin(phi1 - phi2), np.cos(phi1 - phi2))


def _initial_histograms() -> dict[str, Any]:
    payload = {}
    for var, spec in HIST_SPECS.items():
        n_bins = len(spec["bins"]) - 1
        payload[var] = {
            "bins": spec["bins"],
            "data": np.zeros(n_bins),
            "background": defaultdict(lambda n_bins=n_bins: np.zeros(n_bins)),
            "signal": defaultdict(lambda n_bins=n_bins: np.zeros(n_bins)),
        }
    return payload


def _fill_histograms(histograms: dict[str, Any], sample: dict[str, Any], features: dict[str, np.ndarray], weights: np.ndarray, mask: np.ndarray) -> None:
    if not np.any(mask):
        return
    if sample["kind"] == "data":
        target_kind = "data"
        group = "data"
    elif sample["role"].startswith("signal_proxy"):
        target_kind = "signal"
        group = sample["process_group"]
    else:
        target_kind = "background"
        group = sample["process_group"]
    for var, hist in histograms.items():
        counts, _ = np.histogram(features[var][mask], bins=hist["bins"], weights=weights[mask])
        if target_kind == "data":
            hist["data"] += counts
        else:
            hist[target_kind][group] += counts


def _region_mask(region: RegionSpec, features: dict[str, np.ndarray]) -> np.ndarray:
    if region.lepton_category.lower().startswith("2"):
        mask = features["is_ss2l"]
    elif "exactly 2" in region.lepton_category.lower():
        mask = features["is_ss2l"]
    elif region.lepton_category.lower().startswith("3"):
        mask = features["is_3l"]
    else:
        mask = features["is_ss2l"] | features["is_3l"]
    flavour = region.lepton_flavour_treatment.lower().replace("-", " ").strip()
    lead_type = features["lead_lepton_type"]
    sublead_type = features["sublead_lepton_type"]
    if flavour in {"ee", "e e"}:
        mask = mask & (lead_type == 11) & (sublead_type == 11)
    elif flavour in {"e mu", "emu", "e/mu", "e-mu"}:
        mask = mask & (((lead_type == 11) & (sublead_type == 13)) | ((lead_type == 13) & (sublead_type == 11)))
    elif flavour in {"mu mu", "mumu", "mu/mu", "mu-mu"}:
        mask = mask & (lead_type == 13) & (sublead_type == 13)
    charge = region.charge_requirement.lower()
    if "+" in charge and "--" not in charge and "++ or --" not in charge and "same charge" not in charge:
        mask = mask & (features["lead_lepton_charge"] > 0) & (features["sublead_lepton_charge"] > 0)
    if "-" in charge and "++" not in charge and "++ or --" not in charge and "same charge" not in charge:
        mask = mask & (features["lead_lepton_charge"] < 0) & (features["sublead_lepton_charge"] < 0)
    mask = mask & (features["n_jets"] >= region.n_jets_min) & (features["n_btags"] >= region.n_btags_min)
    mask = mask & (features["ht"] >= region.ht_min) & (features["met"] >= region.met_min)
    if region.n_jets_max is not None:
        mask = mask & (features["n_jets"] <= region.n_jets_max)
    if region.n_btags_max is not None:
        mask = mask & (features["n_btags"] <= region.n_btags_max)
    if region.dphi_min is not None:
        mask = mask & (features["delta_phi_ll"] >= region.dphi_min)
    if region.dphi_max is not None:
        mask = mask & (features["delta_phi_ll"] <= region.dphi_max)
    return mask


def _process_batch(batch: ak.Array, sample: dict[str, Any], branch_map: dict[str, str | None], fields: set[str]) -> tuple[np.ndarray, dict[str, np.ndarray], dict[str, np.ndarray], dict[str, Any]]:
    event_branch = branch_map.get("event") or next(iter(batch.fields))
    n_events = len(batch[event_branch])
    weights = np.ones(n_events, dtype=float)
    if sample["kind"] != "data":
        if branch_map.get("mc_weight") in batch.fields:
            weights *= _event_factor(batch[branch_map["mc_weight"]], n_events)
        weights *= float(sample.get("norm_factor", 1.0))
        for branch in SCALE_FACTOR_CANDIDATES:
            if branch in fields:
                weights *= _event_factor(batch[branch], n_events)

    scale = _infer_scale(batch[branch_map["lep_pt"]])
    lep_pt = batch[branch_map["lep_pt"]] * scale
    lep_eta = batch[branch_map["lep_eta"]]
    lep_phi = batch[branch_map["lep_phi"]]
    lep_charge = batch[branch_map["lep_charge"]]
    if branch_map.get("lep_type") in batch.fields:
        lep_type = np.abs(batch[branch_map["lep_type"]])
    else:
        lep_type = ak.zeros_like(lep_charge)
    lep_mask = (lep_pt > 28.0) & (np.abs(lep_eta) < 2.5) & (np.abs(lep_charge) > 0)
    if branch_map.get("lep_type") in batch.fields:
        lep_mask = lep_mask & ((lep_type == 11) | (lep_type == 13))
    if branch_map.get("sig_lep") in batch.fields:
        lep_mask = lep_mask & (batch[branch_map["sig_lep"]] != 0)
    else:
        if branch_map.get("lep_tight") in batch.fields:
            lep_mask = lep_mask & (batch[branch_map["lep_tight"]] != 0)
        if branch_map.get("lep_ptcone") in batch.fields:
            ptcone = batch[branch_map["lep_ptcone"]] * scale
            lep_mask = lep_mask & ((ptcone / ak.where(lep_pt > 0.0, lep_pt, 1.0)) < 0.15)
        if branch_map.get("lep_etcone") in batch.fields:
            etcone = batch[branch_map["lep_etcone"]] * scale
            lep_mask = lep_mask & ((etcone / ak.where(lep_pt > 0.0, lep_pt, 1.0)) < 0.20)

    selected_pt = lep_pt[lep_mask]
    selected_eta = lep_eta[lep_mask]
    selected_phi = lep_phi[lep_mask]
    selected_charge = lep_charge[lep_mask]
    selected_type = lep_type[lep_mask]
    order = ak.argsort(selected_pt, axis=1, ascending=False)
    selected_pt = selected_pt[order]
    selected_eta = selected_eta[order]
    selected_phi = selected_phi[order]
    selected_charge = selected_charge[order]
    selected_type = selected_type[order]
    n_leptons = _ak_numpy(ak.num(selected_pt), 0).astype(int)

    charge_pad = ak.fill_none(ak.pad_none(selected_charge, 2, clip=True), 0)
    phi_pad = ak.fill_none(ak.pad_none(selected_phi, 2, clip=True), 0.0)
    type_pad = ak.fill_none(ak.pad_none(selected_type, 2, clip=True), 0)
    q0 = _ak_numpy(charge_pad[:, 0], 0)
    q1 = _ak_numpy(charge_pad[:, 1], 0)
    t0 = _ak_numpy(type_pad[:, 0], 0).astype(int)
    t1 = _ak_numpy(type_pad[:, 1], 0).astype(int)
    is_ss2l = (n_leptons == 2) & ((q0 * q1) > 0)
    is_3l = n_leptons >= 3
    delta_phi_ll = np.abs(_ak_numpy(_delta_phi(phi_pad[:, 0], phi_pad[:, 1]), 0.0))

    jet_pt = batch[branch_map["jet_pt"]] * scale
    jet_eta = batch[branch_map["jet_eta"]]
    jet_phi = batch[branch_map["jet_phi"]]
    jet_mask = (jet_pt > 25.0) & (np.abs(jet_eta) < 2.5)
    if branch_map.get("jet_btag") in batch.fields:
        btag_values = batch[branch_map["jet_btag"]]
        btag_branch = str(branch_map["jet_btag"])
        if "quantile" in btag_branch.lower():
            btag_mask = btag_values >= 4
        elif str(ak.type(btag_values)).startswith("var * bool"):
            btag_mask = btag_values == 1
        else:
            btag_mask = btag_values > BTAG_MV2C10_70_WP
    else:
        btag_mask = jet_pt < 0.0

    try:
        deta = jet_eta[:, :, None] - selected_eta[:, None, :]
        dphi = _delta_phi(jet_phi[:, :, None], selected_phi[:, None, :])
        min_dr = ak.min(np.sqrt(deta * deta + dphi * dphi), axis=2, initial=999.0)
        jet_mask = jet_mask & (min_dr > 0.4)
    except Exception:
        pass

    selected_jet_pt = jet_pt[jet_mask]
    selected_btag = btag_mask[jet_mask]
    n_jets = _ak_numpy(ak.num(selected_jet_pt), 0).astype(int)
    n_btags = _ak_numpy(ak.sum(selected_btag, axis=1), 0).astype(int)
    ht = _ak_numpy(ak.sum(selected_pt, axis=1) + ak.sum(selected_jet_pt, axis=1), 0.0)
    met = _ak_numpy(batch[branch_map["met"]] * scale, 0.0)

    trigger_available = False
    trigger = np.ones(n_events, dtype=bool)
    trigger_bits = []
    for key in ("trig_e", "trig_m"):
        branch = branch_map.get(key)
        if branch in batch.fields:
            trigger_available = True
            trigger_bits.append(_as_bool(batch[branch], n_events))
    if trigger_bits:
        trigger = np.logical_or.reduce(trigger_bits)

    features = {
        "n_leptons": n_leptons,
        "n_jets": n_jets,
        "n_btags": n_btags,
        "ht": ht,
        "met": met,
        "delta_phi_ll": delta_phi_ll,
        "lead_lepton_type": t0,
        "sublead_lepton_type": t1,
        "lead_lepton_charge": q0,
        "sublead_lepton_charge": q1,
        "is_ss2l": is_ss2l,
        "is_3l": is_3l,
        "trigger": trigger,
    }
    cut_masks = {
        "all_events": np.ones(n_events, dtype=bool),
        "trigger": trigger,
        "two_or_more_selected_leptons": trigger & (n_leptons >= 2),
        "same_sign_dilepton_or_trilepton": trigger & (is_ss2l | is_3l),
        "one_or_more_selected_jets": trigger & (is_ss2l | is_3l) & (n_jets >= 1),
        "one_or_more_btags": trigger & (is_ss2l | is_3l) & (n_jets >= 1) & (n_btags >= 1),
    }
    diagnostics = {
        "energy_unit_scale": scale,
        "trigger_available": trigger_available,
    }
    return weights, features, cut_masks, diagnostics


def _process_sample(sample: dict[str, Any], regions: list[RegionSpec], histograms: dict[str, Any], max_events: int | None = None) -> dict[str, Any]:
    cutflow = {step: _empty_count() for step in CUTFLOW_STEPS}
    region_counts = {region.name: _empty_count() for region in regions}
    diagnostics = {"files": [], "missing_required": [], "batches": 0, "processed_entries": 0, "trigger_available": False, "energy_unit_scales": []}
    path = Path(sample["file"])
    with uproot.open(path) as handle:
        tree = handle[TREE_NAME]
        fields = set(tree.keys())
        branch_map = _resolve_branches(fields)
        missing = _required_missing(branch_map)
        diagnostics["branch_map"] = branch_map
        diagnostics["missing_required"] = missing
        diagnostics["tree_entries"] = int(tree.num_entries)
        if missing:
            return {
                "sample": sample,
                "status": "skipped",
                "skip_reason": "missing required branches: " + ", ".join(missing),
                "cutflow": cutflow,
                "regions": region_counts,
                "diagnostics": diagnostics,
            }
        branches = sorted({branch for branch in branch_map.values() if branch} | {branch for branch in SCALE_FACTOR_CANDIDATES if branch in fields})
        event_prefilter = "n_sig_lep >= 2" if "n_sig_lep" in fields else None
        diagnostics["event_prefilter"] = event_prefilter
        iterate_kwargs: dict[str, Any] = {
            "step_size": 50000,
            "library": "ak",
        }
        if event_prefilter is not None:
            iterate_kwargs["cut"] = event_prefilter
        if max_events is not None:
            iterate_kwargs["entry_stop"] = max_events
        for batch in tree.iterate(branches, **iterate_kwargs):
            weights, features, cut_masks, batch_diag = _process_batch(batch, sample, branch_map, fields)
            diagnostics["batches"] += 1
            diagnostics["processed_entries"] += len(weights)
            diagnostics["trigger_available"] = bool(diagnostics["trigger_available"] or batch_diag["trigger_available"])
            diagnostics["energy_unit_scales"].append(batch_diag["energy_unit_scale"])
            any_region = np.zeros(len(weights), dtype=bool)
            for step, mask in cut_masks.items():
                _add_count(cutflow[step], weights, mask)
            for region in regions:
                mask = cut_masks["one_or_more_btags"] & _region_mask(region, features)
                any_region |= mask
                _add_count(region_counts[region.name], weights, mask)
            _add_count(cutflow["any_signal_region"], weights, any_region)
            baseline = cut_masks["one_or_more_btags"]
            _fill_histograms(histograms, sample, features, weights, baseline)
    return {
        "sample": sample,
        "status": "processed",
        "cutflow": cutflow,
        "regions": region_counts,
        "diagnostics": diagnostics,
    }


def _aggregate_results(sample_results: list[dict[str, Any]], regions: list[RegionSpec]) -> dict[str, Any]:
    aggregate = {
        "regions": {
            region.name: {
                "data": _empty_count(),
                "background_total": _empty_count(),
                "signal_proxy_primary": _empty_count(),
                "background_groups": defaultdict(_empty_count),
                "signal_groups": defaultdict(_empty_count),
            }
            for region in regions
        },
        "cutflow": {step: {"data": _empty_count(), "background": _empty_count(), "signal_proxy_primary": _empty_count()} for step in CUTFLOW_STEPS},
        "samples": [],
    }
    for result in sample_results:
        sample = result["sample"]
        aggregate["samples"].append(
            {
                "sample_id": sample["sample_id"],
                "file": sample["file"],
                "kind": sample["kind"],
                "role": sample["role"],
                "process_group": sample["process_group"],
                "status": result["status"],
                "skip_reason": result.get("skip_reason"),
                "entries": sample.get("entries"),
                "processed_entries": result["diagnostics"].get("processed_entries", 0),
                "norm_factor": sample.get("norm_factor"),
                "cutflow": result["cutflow"],
                "regions": result["regions"],
            }
        )
        for step, count in result["cutflow"].items():
            if sample["kind"] == "data":
                target = aggregate["cutflow"][step]["data"]
            elif sample["role"] == "signal_proxy_primary":
                target = aggregate["cutflow"][step]["signal_proxy_primary"]
            elif sample["role"] == "background":
                target = aggregate["cutflow"][step]["background"]
            else:
                continue
            for key in target:
                target[key] += count[key]
        for region_name, count in result["regions"].items():
            region_payload = aggregate["regions"][region_name]
            if sample["kind"] == "data":
                target = region_payload["data"]
            elif sample["role"] == "signal_proxy_primary":
                target = region_payload["signal_proxy_primary"]
                signal_group = region_payload["signal_groups"][sample["process_group"]]
                for key in signal_group:
                    signal_group[key] += count[key]
            elif sample["role"] == "background":
                target = region_payload["background_total"]
                background_group = region_payload["background_groups"][sample["process_group"]]
                for key in background_group:
                    background_group[key] += count[key]
            else:
                signal_group = region_payload["signal_groups"][sample["process_group"]]
                for key in signal_group:
                    signal_group[key] += count[key]
                continue
            for key in target:
                target[key] += count[key]
    for region_payload in aggregate["regions"].values():
        region_payload["background_groups"] = dict(region_payload["background_groups"])
        region_payload["signal_groups"] = dict(region_payload["signal_groups"])
    return aggregate


def _background_uncertainty(count: dict[str, Any]) -> float:
    b = float(count["weighted"])
    mc_stat = math.sqrt(max(float(count["sumw2"]), 0.0))
    rel = BACKGROUND_REL_UNCERTAINTY * abs(b)
    return math.sqrt(mc_stat * mc_stat + rel * rel)


def _stat_results(aggregate: dict[str, Any]) -> dict[str, Any]:
    regions = {}
    best_region = None
    best_mu95 = math.inf
    for region_name, payload in aggregate["regions"].items():
        b_raw = float(payload["background_total"]["weighted"])
        s_raw = float(payload["signal_proxy_primary"]["weighted"])
        b = max(b_raw, 0.0)
        s = max(s_raw, 0.0)
        n = float(payload["data"]["unweighted"])
        sigma_b = _background_uncertainty(payload["background_total"])
        denom = math.sqrt(max(b + sigma_b * sigma_b, 1e-12))
        z_exp = s / denom if s > 0.0 else None
        mu95_exp = 1.64 * denom / s if s > 0.0 else None
        z_obs = (n - b) / denom if b > 0.0 else None
        mu95_obs = ((max(0.0, n - b) + 1.64 * math.sqrt(max(n, b, 1.0) + sigma_b * sigma_b)) / s) if s > 0.0 else None
        regions[region_name] = {
            "observed_count": n,
            "expected_background": b_raw,
            "expected_background_for_stat": b,
            "background_uncertainty": sigma_b,
            "signal_proxy_yield_mu1": s_raw,
            "signal_proxy_yield_for_stat": s,
            "expected_z_approx": z_exp,
            "expected_mu95_approx": mu95_exp,
            "observed_z_approx": z_obs,
            "observed_mu95_approx": mu95_obs,
        }
        if mu95_exp is not None and mu95_exp < best_mu95:
            best_region = region_name
            best_mu95 = mu95_exp
    return {
        "status": "ok",
        "backend": "simplified_binned_counting_likelihood",
        "confidence_level": 0.95,
        "background_relative_uncertainty_floor": BACKGROUND_REL_UNCERTAINTY,
        "signal_model": "available SM four-top sample used as the central top-rich signal proxy",
        "combination_policy": "regions are reported separately; no combined likelihood is claimed because orthogonality and nuisance correlations are unavailable",
        "best_expected_region": best_region,
        "regions": regions,
    }


def _jsonable_histograms(histograms: dict[str, Any]) -> dict[str, Any]:
    payload = {}
    for var, hist in histograms.items():
        payload[var] = {
            "bins": hist["bins"].tolist(),
            "data": hist["data"].tolist(),
            "background": {key: value.tolist() for key, value in hist["background"].items()},
            "signal": {key: value.tolist() for key, value in hist["signal"].items()},
        }
    return payload


def _freeze_histograms(histograms: dict[str, Any]) -> dict[str, Any]:
    frozen = {}
    for var, hist in histograms.items():
        frozen[var] = {
            "bins": hist["bins"],
            "data": hist["data"],
            "background": dict(hist["background"]),
            "signal": dict(hist["signal"]),
        }
    return frozen


def _merge_histograms(target: dict[str, Any], source: dict[str, Any]) -> None:
    for var, hist in source.items():
        target[var]["data"] += hist["data"]
        for group, counts in hist["background"].items():
            target[var]["background"][group] += counts
        for group, counts in hist["signal"].items():
            target[var]["signal"][group] += counts


def _process_sample_worker(args: tuple[dict[str, Any], list[RegionSpec], int | None]) -> tuple[dict[str, Any], dict[str, Any]]:
    sample, regions, max_events = args
    local_histograms = _initial_histograms()
    return _process_sample(sample, regions, local_histograms, max_events=max_events), _freeze_histograms(local_histograms)


def _plot_histograms(histograms: dict[str, Any], out_dir: Path) -> dict[str, list[str]]:
    ensure_dir(out_dir)
    manifest: dict[str, list[str]] = {}
    for var, hist in histograms.items():
        bins = hist["bins"]
        centers = 0.5 * (bins[:-1] + bins[1:])
        widths = np.diff(bins)
        fig, ax = plt.subplots(figsize=(8, 5))
        bottom = np.zeros_like(centers)
        for group, counts in sorted(hist["background"].items()):
            ax.bar(
                centers,
                counts,
                width=widths,
                bottom=bottom,
                align="center",
                color=PLOT_COLORS.get(group, "#8C8C8C"),
                alpha=0.75,
                label=group,
                linewidth=0,
            )
            bottom += counts
        for group, counts in sorted(hist["signal"].items()):
            ax.step(centers, counts, where="mid", linewidth=1.8, label=f"{group} signal proxy")
        data = hist["data"]
        ax.errorbar(centers, data, yerr=np.sqrt(np.maximum(data, 0.0)), fmt="o", color="black", label="data")
        ax.set_xlabel(HIST_SPECS[var]["xlabel"])
        ax.set_ylabel("events")
        ax.set_yscale("log" if max(np.max(bottom) if bottom.size else 0.0, np.max(data) if data.size else 0.0) > 20 else "linear")
        ax.legend(fontsize=8, ncol=2)
        ax.grid(True, axis="y", alpha=0.25)
        fig.tight_layout()
        path = out_dir / f"{var}.png"
        fig.savefig(path, dpi=160)
        plt.close(fig)
        manifest[var] = [str(path)]
    return manifest


def _plot_region_yields(aggregate: dict[str, Any], stats: dict[str, Any], out_dir: Path) -> dict[str, list[str]]:
    ensure_dir(out_dir)
    region_names = list(aggregate["regions"])
    x = np.arange(len(region_names))
    bkg = np.array([aggregate["regions"][name]["background_total"]["weighted"] for name in region_names])
    sig = np.array([aggregate["regions"][name]["signal_proxy_primary"]["weighted"] for name in region_names])
    data = np.array([aggregate["regions"][name]["data"]["unweighted"] for name in region_names])
    bkg_err = np.array([_background_uncertainty(aggregate["regions"][name]["background_total"]) for name in region_names])

    fig, ax = plt.subplots(figsize=(max(9, 0.7 * len(region_names)), 5))
    ax.bar(x - 0.2, bkg, width=0.38, color="#4C78A8", label="expected background")
    ax.errorbar(x - 0.2, bkg, yerr=bkg_err, fmt="none", ecolor="black", linewidth=1)
    ax.bar(x + 0.2, data, width=0.38, color="#F58518", label="observed data")
    ax.step(x, sig, where="mid", color="#54A24B", linewidth=2, label="signal proxy")
    ax.set_xticks(x)
    ax.set_xticklabels(region_names, rotation=45, ha="right")
    ax.set_ylabel("events")
    ax.set_title("Signal-region yields")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    yields_path = out_dir / "region_yields.png"
    fig.savefig(yields_path, dpi=170)
    plt.close(fig)

    exp_z = [stats["regions"][name]["expected_z_approx"] or 0.0 for name in region_names]
    obs_z = [stats["regions"][name]["observed_z_approx"] or 0.0 for name in region_names]
    fig, ax = plt.subplots(figsize=(max(9, 0.7 * len(region_names)), 5))
    ax.bar(x - 0.2, exp_z, width=0.38, color="#72B7B2", label="expected proxy Z")
    ax.bar(x + 0.2, obs_z, width=0.38, color="#E45756", label="observed excess Z")
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(region_names, rotation=45, ha="right")
    ax.set_ylabel("approximate Gaussian Z")
    ax.set_title("Approximate expected and observed sensitivity")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    stats_path = out_dir / "region_sensitivity.png"
    fig.savefig(stats_path, dpi=170)
    plt.close(fig)
    return {"region_yields": [str(yields_path)], "region_sensitivity": [str(stats_path)]}


def _region_table(aggregate: dict[str, Any], stats: dict[str, Any]) -> str:
    lines = [
        "| Region | Observed | Background used for stat | Signal used for stat | Exp. Z | Exp. mu95 | Obs. Z | Obs. mu95 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, payload in stats["regions"].items():
        raw_b = float(payload["expected_background"])
        stat_b = float(payload["expected_background_for_stat"])
        raw_s = float(payload["signal_proxy_yield_mu1"])
        stat_s = float(payload["signal_proxy_yield_for_stat"])
        b_text = f"{stat_b:.2f} +/- {payload['background_uncertainty']:.2f}"
        s_text = f"{stat_s:.3f}"
        if raw_b < 0.0:
            b_text += f" (raw signed {raw_b:.2f})"
        if raw_s < 0.0:
            s_text += f" (raw signed {raw_s:.3f})"
        lines.append(
            "| {name} | {obs:.0f} | {b} | {s} | {ze} | {mue} | {zo} | {muo} |".format(
                name=name,
                obs=payload["observed_count"],
                b=b_text,
                s=s_text,
                ze="-" if payload["expected_z_approx"] is None else f"{payload['expected_z_approx']:.2f}",
                mue="-" if payload["expected_mu95_approx"] is None else f"{payload['expected_mu95_approx']:.2f}",
                zo="-" if payload["observed_z_approx"] is None else f"{payload['observed_z_approx']:.2f}",
                muo="-" if payload["observed_mu95_approx"] is None else f"{payload['observed_mu95_approx']:.2f}",
            )
        )
    return "\n".join(lines)


def _cutflow_table(aggregate: dict[str, Any]) -> str:
    lines = [
        "| Step | Data | Background | Signal proxy |",
        "| --- | ---: | ---: | ---: |",
    ]
    for step, payload in aggregate["cutflow"].items():
        lines.append(
            f"| {step} | {payload['data']['unweighted']} | {payload['background']['weighted']:.2f} | {payload['signal_proxy_primary']['weighted']:.3f} |"
        )
    return "\n".join(lines)


def _implementation_differences(samples: list[dict[str, Any]], branch_summary: dict[str, Any]) -> list[dict[str, str]]:
    has_vlq = any("vlq" in sample.get("descriptor", "").lower() for sample in samples)
    return [
        {
            "reference_concept": "Dedicated vector-like quark signal hypotheses and mass/branching-ratio scans",
            "available_replacement": "No dedicated VLQ ntuple is present; the central proxy is the available SM four-top sample, with other top-rich BSM samples retained as alternatives.",
            "reasoning": "The open-data sample directory contains top-rich and BSM-like samples but no explicit VLQ production sample.",
            "expected_impact": "The output is a VLQ-style reinterpretation and not a VLQ mass exclusion.",
        },
        {
            "reference_concept": "Data-driven fake and nonprompt lepton matrix estimates",
            "available_replacement": "Prompt and nonprompt sources are grouped from available MC, with multijet/photon-associated samples retained in a separate background group.",
            "reasoning": "The ntuples do not provide the prompt/fake efficiency measurements or anti-identification control samples needed for the matrix method.",
            "expected_impact": "Background estimates have larger method uncertainty; a conservative 30 percent relative uncertainty is applied in the simplified statistical model.",
        },
        {
            "reference_concept": "Electron charge-misidentification estimate from dedicated control regions",
            "available_replacement": "No charge-misID transfer factor is built; same-sign selections use reconstructed lepton charge directly.",
            "reasoning": "The required charge-flip probability maps and dedicated sideband machinery are not available in the open-data files.",
            "expected_impact": "Same-sign dilepton backgrounds can be mismodeled, especially in electron-rich regions.",
        },
        {
            "reference_concept": "Reference trigger menu and lepton identification operating points",
            "available_replacement": "The 1lepMET30 open-data stream is used; trigger flags are applied when present, and available lepton tight-ID/isolation branches define selected leptons.",
            "reasoning": "The input dataset is already skimmed to a one-lepton plus missing-energy stream rather than the full reference trigger set.",
            "expected_impact": "Acceptance differs from the reference same-sign/trilepton analysis, particularly for low-MET or dilepton-trigger-only events.",
        },
        {
            "reference_concept": "Full profile-likelihood combination with correlated nuisance parameters",
            "available_replacement": "Per-region counting results with an approximate Gaussian expected/observed Z and signal-strength upper limit.",
            "reasoning": "PyROOT/RooFit is unavailable and the open-data inputs do not include the full systematic model or correlation scheme.",
            "expected_impact": "Statistical outputs are useful diagnostics, but they are not full CLs limits or official likelihood results.",
        },
        {
            "reference_concept": "Orthogonal combined signal regions",
            "available_replacement": "All reference-like regions are reported individually; the best expected region is identified without claiming a combined fit.",
            "reasoning": "The region definitions are threshold-based and may overlap, while the covariance model is unavailable.",
            "expected_impact": "Combined sensitivity is not quoted to avoid double counting.",
        },
    ] + (
        []
        if has_vlq
        else [
            {
                "reference_concept": "Explicit VLQ sample availability",
                "available_replacement": f"Branch inventory found common object branches {', '.join(branch_summary.get('common_required_branches', [])[:8])}.",
                "reasoning": "Actual available branches support object-level selection but not a dedicated generated VLQ truth label.",
                "expected_impact": "Signal interpretation is restricted to the named proxy model.",
            }
        ]
    )


def _write_report(
    *,
    out_dir: Path,
    summary: dict[str, Any],
    samples: list[dict[str, Any]],
    aggregate: dict[str, Any],
    stats: dict[str, Any],
    plot_manifest: dict[str, Any],
    branch_summary: dict[str, Any],
) -> Path:
    report_dir = ensure_dir(out_dir / "report")
    registry_counts = {
        "data": sum(1 for sample in samples if sample["kind"] == "data"),
        "background": sum(1 for sample in samples if sample["role"] == "background"),
        "signal_proxy": sum(1 for sample in samples if sample["role"].startswith("signal_proxy")),
    }
    best = stats.get("best_expected_region")
    best_text = "No region has nonzero proxy signal acceptance."
    if best:
        payload = stats["regions"][best]
        best_text = (
            f"The best expected region is `{best}` with approximate expected Z={payload['expected_z_approx']:.2f} "
            f"and expected signal-strength upper limit mu95={payload['expected_mu95_approx']:.2f}."
        )
    diff_lines = []
    for item in _implementation_differences(samples, branch_summary):
        diff_lines.append(
            f"- Reference concept: {item['reference_concept']}\n"
            f"  Available open-data replacement: {item['available_replacement']}\n"
            f"  Reasoning: {item['reasoning']}\n"
            f"  Expected impact: {item['expected_impact']}"
        )
    image_blocks = []
    for group, paths in plot_manifest.items():
        for path in paths:
            rel = os.path.relpath(path, report_dir)
            image_blocks.append(f"![{group}]({rel})\n\n*Caption:* {group.replace('_', ' ')} diagnostic for the VLQ-style search.")
    text = f"""# Same-Charge Leptons plus b-jets VLQ-Style Open-Data Analysis

## Summary

This run implements a same-sign dilepton and trilepton plus b-jets search using the available 13 TeV ATLAS open-data ntuples at {LUMI_FB:.1f} fb-1. The authoritative target is `analysis/leptons-bjet-vlq-search.json`; inherited diphoton configuration files are not used for the physics workflow.

{best_text}

The statistical outputs are simplified per-region counting approximations because the runtime has no ROOT/RooFit backend and the open-data samples do not contain the full reference likelihood ingredients.

## Dataset and Sample Grouping

Processed sample counts: {registry_counts['data']} data files, {registry_counts['background']} background MC files, and {registry_counts['signal_proxy']} signal-proxy or alternative signal MC files. MC samples use the ROOT metadata branches for cross section, filter efficiency, k-factor, and signed generator-weight sum when available.

The central signal proxy is the available SM four-top sample. Other top-rich BSM samples are processed and retained as alternatives, but they are not merged into the central background.

## Object and Event Selection

Leptons require pT above 28 GeV, |eta| below 2.5, nonzero charge, available tight-ID flags, and available isolation cone requirements. Jets require pT above 25 GeV, |eta| below 2.5, lepton overlap removal with DeltaR > 0.4 where possible, and b-tagging from the available MV2c10-like branch at the 70 percent working-point threshold.

Same-sign dilepton regions require exactly two selected leptons with equal charge sign. Same-sign top subregions additionally apply the available leading-pair flavour and positive-charge requirements from the target JSON. Trilepton regions require at least three selected leptons. H_T is computed from selected leptons and jets, and missing transverse momentum uses the available MET branch.

## Cut Flow

{_cutflow_table(aggregate)}

## Signal Regions and Statistical Results

Expected results are computed first from fixed MC background and the signal proxy. Observed data counts are then evaluated with the same fixed selections and statistical formulae. Raw signed MC yields are preserved in JSON; when a sparse signed-weight sum is negative, the simplified counting statistic uses a nonnegative clipped yield and records the raw signed value in the table.

{_region_table(aggregate, stats)}

## Plots

{chr(10).join(image_blocks)}

## Blinding and Unblinding Record

The implementation fixes object definitions, sample grouping, signal-region thresholds, background grouping, uncertainty policy, and statistical formulae before reading observed signal-region counts into the reported statistical table. Expected and observed results are stored separately in the machine-readable statistics artifact.

## Implementation Differences from Reference Analysis

{chr(10).join(diff_lines)}

## Reproducibility

The exact CLI command is saved in `outputs/vlq/repro/commands.sh`. Core machine-readable artifacts include the sample registry, branch summary, per-sample cut flows, region yields, histogram payloads, statistics JSON, plot manifest, and this report.
"""
    path = report_dir / "final_report.md"
    write_text(text, path)
    return path


def _branch_summary(sample_results: list[dict[str, Any]]) -> dict[str, Any]:
    maps = [result["diagnostics"].get("branch_map", {}) for result in sample_results if result["status"] == "processed"]
    required = ["lep_pt", "lep_eta", "lep_phi", "lep_charge", "jet_pt", "jet_eta", "jet_phi", "jet_btag", "met"]
    common_required = sorted({maps[0][key] for key in required if maps and maps[0].get(key)})
    trigger_available = any(result["diagnostics"].get("trigger_available") for result in sample_results)
    return {
        "status": "ok" if maps else "blocked",
        "processed_sample_count": len(maps),
        "common_required_branches": common_required,
        "example_branch_map": maps[0] if maps else {},
        "trigger_flags_available": trigger_available,
        "energy_unit_scales_seen": sorted(
            {
                float(scale)
                for result in sample_results
                for scale in result["diagnostics"].get("energy_unit_scales", [])
            }
        ),
    }


def run_vlq_pipeline(summary_path: Path, inputs: Path, outputs: Path, max_events: int | None = None, workers: int = 1) -> dict[str, Any]:
    out_dir = ensure_dir(outputs)
    ensure_dir(out_dir / "logs")
    started = utcnow_iso()
    summary = read_json(summary_path)
    regions = parse_regions(summary)
    samples, discovery_notes = discover_samples(inputs)
    histograms = _initial_histograms()
    sample_results: list[dict[str, Any]] = []
    workers = max(1, int(workers))
    if workers == 1:
        for index, sample in enumerate(samples, start=1):
            result = _process_sample(sample, regions, histograms, max_events=max_events)
            sample_results.append(result)
            with (out_dir / "logs" / "processing.log").open("a") as handle:
                handle.write(f"{utcnow_iso()} {index}/{len(samples)} {sample['sample_id']} {result['status']}\n")
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(_process_sample_worker, (sample, regions, max_events)): sample
                for sample in samples
            }
            for index, future in enumerate(as_completed(futures), start=1):
                sample = futures[future]
                result, sample_histograms = future.result()
                sample_results.append(result)
                _merge_histograms(histograms, sample_histograms)
                with (out_dir / "logs" / "processing.log").open("a") as handle:
                    handle.write(f"{utcnow_iso()} {index}/{len(samples)} {sample['sample_id']} {result['status']}\n")
    aggregate = _aggregate_results(sample_results, regions)
    stats = _stat_results(aggregate)
    branch_info = _branch_summary(sample_results)
    plot_manifest = {}
    plot_manifest.update(_plot_histograms(histograms, out_dir / "plots" / "distributions"))
    plot_manifest.update(_plot_region_yields(aggregate, stats, out_dir / "plots" / "regions"))
    plot_manifest_path = write_json({"status": "ok", "plots": plot_manifest}, out_dir / "plots" / "manifest.json")

    write_json(
        {
            "status": "ok",
            "summary_path": str(summary_path),
            "inputs": str(inputs),
            "outputs": str(outputs),
            "started_at_utc": started,
            "ended_at_utc": utcnow_iso(),
            "config_hash": stable_hash({"summary": summary, "regions": [region.__dict__ for region in regions]}),
            "max_events_per_sample": max_events,
            "workers": workers,
            "luminosity_fb": LUMI_FB,
            "blinding_sequence": [
                "object, sample, region, and statistic definitions fixed",
                "expected MC-only sensitivity computed",
                "observed counts read with fixed selections for final observed table",
            ],
        },
        out_dir / "run_manifest.json",
    )
    write_json([region.__dict__ for region in regions], out_dir / "regions.json")
    write_json(samples, out_dir / "samples" / "sample_registry.json")
    write_json(discovery_notes, out_dir / "samples" / "discovery_notes.json")
    write_json(branch_info, out_dir / "branches" / "branch_summary.json")
    write_json(aggregate, out_dir / "yields" / "aggregate_yields.json")
    write_json({"status": "ok", "samples": aggregate["samples"]}, out_dir / "yields" / "per_sample_cutflows.json")
    write_json(_jsonable_histograms(histograms), out_dir / "hists" / "histograms.json")
    write_json(
        {
            "status": "ok",
            "expected": {
                name: {
                    "expected_background": payload["expected_background"],
                    "background_uncertainty": payload["background_uncertainty"],
                    "signal_proxy_yield_mu1": payload["signal_proxy_yield_mu1"],
                    "expected_z_approx": payload["expected_z_approx"],
                    "expected_mu95_approx": payload["expected_mu95_approx"],
                }
                for name, payload in stats["regions"].items()
            },
            "observed": {
                name: {
                    "observed_count": payload["observed_count"],
                    "observed_z_approx": payload["observed_z_approx"],
                    "observed_mu95_approx": payload["observed_mu95_approx"],
                }
                for name, payload in stats["regions"].items()
            },
            "details": stats,
        },
        out_dir / "stats" / "expected_observed_statistics.json",
    )
    write_json(
        {
            "status": "ok",
            "backend": "simplified_binned_counting_likelihood",
            "limitations": [
                "No full CLs calculation",
                "No correlated nuisance parameter model",
                "No dedicated VLQ signal sample",
                "No data-driven fake or charge-misidentification estimate",
            ],
        },
        out_dir / "stats" / "statistical_model_limitations.json",
    )
    report_path = _write_report(
        out_dir=out_dir,
        summary=summary,
        samples=samples,
        aggregate=aggregate,
        stats=stats,
        plot_manifest=plot_manifest,
        branch_summary=branch_info,
    )
    write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "PYTHONPATH=. MPLCONFIGDIR=.cache/matplotlib XDG_CACHE_HOME=.cache \\",
                "  python3 -m analysis.vlq_pipeline \\",
                "  --summary analysis/leptons-bjet-vlq-search.json \\",
                "  --inputs input-data \\",
                "  --outputs outputs/vlq \\",
                "  --workers 8",
                "",
            ]
        ),
        out_dir / "repro" / "commands.sh",
    )
    return {
        "status": "ok",
        "outputs": str(out_dir),
        "report": str(report_path),
        "plot_manifest": str(plot_manifest_path),
        "processed_samples": len([item for item in sample_results if item["status"] == "processed"]),
        "skipped_samples": len([item for item in sample_results if item["status"] != "processed"]),
        "best_expected_region": stats.get("best_expected_region"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the VLQ-style same-charge lepton plus b-jets open-data analysis.")
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--inputs", required=True, type=Path)
    parser.add_argument("--outputs", required=True, type=Path)
    parser.add_argument("--max-events", type=int, default=None)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()
    result = run_vlq_pipeline(args.summary, args.inputs, args.outputs, max_events=args.max_events, workers=args.workers)
    print(f"status={result['status']} processed={result['processed_samples']} skipped={result['skipped_samples']} report={result['report']}")


if __name__ == "__main__":
    main()
