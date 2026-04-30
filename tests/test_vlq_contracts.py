from pathlib import Path

from analysis.cli import bootstrap
from analysis.common import read_json
from analysis.vlq_pipeline import _classify_sample


SUMMARY_PATH = Path("analysis/analysis.summary.json")


def test_bootstrap_writes_vlq_normalized_summary(tmp_path: Path):
    bootstrap(SUMMARY_PATH, tmp_path)

    payload = read_json(tmp_path / "summary.normalized.json")

    assert payload["analysis_short_name"] == "same_charge_leptons_bjets"
    assert payload["source_summary"] == str(SUMMARY_PATH)
    assert payload["inventory"]["n_signal_regions"] > 0
    assert (tmp_path / "report" / "runtime_recovery.json").exists()


def test_sample_classifier_marks_signal_proxy_and_key_backgrounds():
    signal_role, signal_key, _ = _classify_sample("SM4topsNLO", "412043")
    _, ttw_key, _ = _classify_sample("Sherpa_221_NNPDF30NNLO_ttW", "410155")
    _, reducible_key, _ = _classify_sample("PowhegPythia8EvtGen_A14_ttbar_hdamp", "410470")

    assert signal_role == "signal_proxy_primary"
    assert signal_key == "four_top_signal_proxy"
    assert ttw_key == "rare_top"
    assert reducible_key == "ttbar"
