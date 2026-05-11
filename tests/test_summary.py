from pathlib import Path

from analysis.common import read_json
from analysis.vlq_pipeline import is_vlq_summary, normalize_vlq_summary


SUMMARY_PATH = Path("analysis/analysis.summary.json")


def test_summary_alias_points_to_vlq_target():
    assert SUMMARY_PATH.is_symlink()
    assert SUMMARY_PATH.resolve().name == "leptons-bjet-vlq-search.json"

    source = read_json(SUMMARY_PATH)

    assert is_vlq_summary(source, SUMMARY_PATH)


def test_vlq_normalization_has_analysis_inventory():
    source = read_json(SUMMARY_PATH)
    normalized = normalize_vlq_summary(source, SUMMARY_PATH)

    assert normalized["analysis_short_name"] == "same_charge_leptons_bjets"
    assert normalized["inventory"]["n_signal_regions"] > 0
    assert normalized["inventory"]["fit_ids"]
    object_selection = normalized["runtime_defaults"]["object_selection"]
    assert object_selection["btag_working_point"] == "77% efficiency"
    assert object_selection["btag_quantile_min"] == 3
    assert object_selection["electron_crack_veto"] == [1.37, 1.52]
    assert object_selection["require_exact_trilepton"] is True
    assert normalized["runtime_defaults"]["statistics"]["method"].startswith("Gaussian")
    assert normalized["implementation_differences"]
