from pathlib import Path

from analysis.config.load_summary import normalize_summary
from analysis.common import read_json


def test_summary_normalization_has_inventory():
    summary_path = Path("analysis/analysis.summary.json")
    normalized, errors = normalize_summary(read_json(summary_path), summary_path)
    assert not errors
    assert normalized["inventory"]["n_signal_regions"] == 5
    assert normalized["inventory"]["n_control_regions"] == 1
    assert any(category["category_id"] == "two_jet_vbf_enriched" for category in normalized["categories"])
