from pathlib import Path

from analysis.cli import bootstrap
from analysis.common import read_json
from analysis.vlq_pipeline import PRIMARY_SIGNAL_PROCESS, classify_process


SUMMARY_PATH = Path("analysis/analysis.summary.json")


def test_bootstrap_writes_vlq_normalized_summary(tmp_path: Path):
    bootstrap(SUMMARY_PATH, tmp_path)

    payload = read_json(tmp_path / "summary.normalized.json")

    assert payload["analysis_short_name"] == "same_charge_leptons_bjets"
    assert payload["source_summary"] == str(SUMMARY_PATH)
    assert (tmp_path / "report" / "runtime_recovery.json").exists()


def test_process_classifier_marks_signal_proxy_and_key_backgrounds():
    signal_kind, signal_key, _ = classify_process("MadGraphPythia8EvtGen_A14NNPDF23LO_DM_4topScalar")
    _, ttw_key, _ = classify_process("Sherpa_221_NNPDF30NNLO_ttW")
    _, reducible_key, _ = classify_process("PowhegPythia8EvtGen_A14_ttbar_hdamp")

    assert signal_kind == "signal_proxy"
    assert signal_key == PRIMARY_SIGNAL_PROCESS
    assert ttw_key == "ttW"
    assert reducible_key == "ttbar_reducible"
