from pathlib import Path

from analysis.common import read_json
from analysis.vlq_pipeline import parse_regions


SUMMARY_PATH = Path("analysis/analysis.summary.json")


def test_summary_alias_points_to_vlq_target():
    assert SUMMARY_PATH.is_symlink()
    assert SUMMARY_PATH.resolve().name == "leptons-bjet-vlq-search.json"

    source = read_json(SUMMARY_PATH)

    assert source["analysis_metadata"]["analysis_short_name"] == "same_charge_leptons_bjets"


def test_vlq_regions_have_analysis_inventory():
    source = read_json(SUMMARY_PATH)
    regions = parse_regions(source)

    assert regions
    assert source.get("fit_setup")
    assert any(region.n_btags_min >= 1 for region in regions)
    assert any(region.search_family == "VLQ_4top" for region in regions)
