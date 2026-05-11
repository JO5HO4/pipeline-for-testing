from pathlib import Path

import numpy as np

from analysis.cli import bootstrap
from analysis.common import read_json
from analysis.vlq_pipeline import (
    PRIMARY_SIGNAL_PROCESS,
    _region_mask,
    analysis_spec_conformance_audit,
    classify_process,
    parse_regions,
    selection_config_from_summary,
)


SUMMARY_PATH = Path("analysis/analysis.summary.json")


def test_bootstrap_writes_vlq_normalized_summary(tmp_path: Path):
    bootstrap(SUMMARY_PATH, tmp_path)

    payload = read_json(tmp_path / "summary.normalized.json")
    audit = read_json(tmp_path / "report" / "analysis_spec_conformance_audit.json")

    assert payload["analysis_short_name"] == "same_charge_leptons_bjets"
    assert payload["source_summary"] == str(SUMMARY_PATH)
    assert audit["gate_outcome"] == "PASS"
    assert (tmp_path / "report" / "runtime_recovery.json").exists()


def test_process_classifier_marks_signal_proxy_and_key_backgrounds():
    signal_kind, signal_key, _ = classify_process("MadGraphPythia8EvtGen_A14NNPDF23LO_DM_4topScalar")
    _, ttw_key, _ = classify_process("Sherpa_221_NNPDF30NNLO_ttW")
    _, reducible_key, _ = classify_process("PowhegPythia8EvtGen_A14_ttbar_hdamp")

    assert signal_kind == "signal_proxy"
    assert signal_key == PRIMARY_SIGNAL_PROCESS
    assert ttw_key == "ttW"
    assert reducible_key == "ttbar_reducible"


def _base_features(size: int = 2) -> dict[str, np.ndarray]:
    return {
        "n_leptons": np.full(size, 2),
        "n_jets": np.full(size, 7),
        "n_btags": np.full(size, 3),
        "ht": np.full(size, 900.0),
        "met": np.full(size, 50.0),
        "delta_phi_ll": np.full(size, 3.0),
        "lead_lepton_type": np.full(size, 13),
        "sublead_lepton_type": np.full(size, 13),
        "lead_lepton_eta": np.zeros(size),
        "sublead_lepton_eta": np.zeros(size),
        "lead_lepton_charge": np.ones(size),
        "sublead_lepton_charge": np.ones(size),
        "dilepton_mass": np.full(size, 50.0),
        "is_ss2l": np.ones(size, dtype=bool),
        "is_3l": np.zeros(size, dtype=bool),
        "is_3l_exact": np.zeros(size, dtype=bool),
    }


def test_analysis_spec_conformance_gate_passes_for_canonical_summary():
    source = read_json(SUMMARY_PATH)
    regions = parse_regions(source)
    selection = selection_config_from_summary(source)

    audit = analysis_spec_conformance_audit(source, regions, selection)

    assert audit["gate_outcome"] == "PASS"
    assert not audit["failures"]
    assert selection.btag_working_point == "77"
    assert selection.btag_quantile_min == 3


def test_region_parser_preserves_ht_upper_bounds():
    source = read_json(SUMMARY_PATH)
    regions = {region.name: region for region in parse_regions(source)}

    assert regions["SR3b2l_L"].ht_max == 1200.0
    assert regions["SR3b3l_L"].ht_max == 1000.0


def test_region_mask_enforces_ht_upper_bound():
    source = read_json(SUMMARY_PATH)
    selection = selection_config_from_summary(source)
    regions = {region.name: region for region in parse_regions(source)}
    features = _base_features(size=2)
    features["ht"] = np.array([900.0, 1300.0])

    mask = _region_mask(regions["SR3b2l_L"], features, selection)

    assert mask.tolist() == [True, False]


def test_region_mask_requires_exact_trilepton_category():
    source = read_json(SUMMARY_PATH)
    selection = selection_config_from_summary(source)
    regions = {region.name: region for region in parse_regions(source)}
    features = _base_features(size=2)
    features.update(
        {
            "n_leptons": np.array([3, 4]),
            "n_jets": np.array([1, 1]),
            "n_btags": np.array([1, 1]),
            "ht": np.array([1200.0, 1200.0]),
            "met": np.array([150.0, 150.0]),
            "is_ss2l": np.array([False, False]),
            "is_3l": np.array([True, True]),
            "is_3l_exact": np.array([True, False]),
        }
    )

    mask = _region_mask(regions["SR1b3l"], features, selection)

    assert mask.tolist() == [True, False]


def test_trilepton_regions_do_not_apply_same_sign_ee_mass_veto():
    source = read_json(SUMMARY_PATH)
    selection = selection_config_from_summary(source)
    regions = {region.name: region for region in parse_regions(source)}
    features = _base_features(size=1)
    features.update(
        {
            "n_leptons": np.array([3]),
            "n_jets": np.array([1]),
            "n_btags": np.array([1]),
            "ht": np.array([1200.0]),
            "met": np.array([150.0]),
            "lead_lepton_type": np.array([11]),
            "sublead_lepton_type": np.array([11]),
            "dilepton_mass": np.array([91.1876]),
            "is_ss2l": np.array([False]),
            "is_3l": np.array([True]),
            "is_3l_exact": np.array([True]),
        }
    )

    mask = _region_mask(regions["SR1b3l"], features, selection)

    assert mask.tolist() == [True]


def test_region_mask_applies_same_sign_ee_mass_veto_and_central_eta_rule():
    source = read_json(SUMMARY_PATH)
    selection = selection_config_from_summary(source)
    regions = {region.name: region for region in parse_regions(source)}
    features = _base_features(size=3)
    features.update(
        {
            "n_jets": np.array([1, 1, 1]),
            "n_btags": np.array([1, 1, 1]),
            "lead_lepton_type": np.array([11, 11, 11]),
            "sublead_lepton_type": np.array([11, 11, 11]),
            "lead_lepton_eta": np.array([0.2, 0.2, 1.45]),
            "sublead_lepton_eta": np.array([0.2, 0.2, 0.2]),
            "dilepton_mass": np.array([91.1876, 50.0, 50.0]),
        }
    )

    mask = _region_mask(regions["SRttee"], features, selection)

    assert mask.tolist() == [False, True, False]
