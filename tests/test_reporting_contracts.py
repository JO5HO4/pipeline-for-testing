from pathlib import Path

from analysis.common import write_json, write_text
from analysis.report.artifacts import (
    write_enforcement_policy_defaults,
    write_final_review,
    write_smoke_and_repro_artifacts,
    write_verification_status,
)


def test_enforcement_policy_defaults_use_canonical_keys(tmp_path: Path):
    summary = {
        "runtime_defaults": {
            "target_lumi_fb": 36.1,
            "central_mc_lumi_fb": 36.1,
            "fit_mass_range_gev": [105.0, 160.0],
            "signal_window_gev": [120.0, 130.0],
            "sidebands_gev": [[105.0, 120.0], [130.0, 160.0]],
            "blinding": {"observed_significance_allowed": False},
        }
    }

    payload = write_enforcement_policy_defaults(summary, tmp_path)

    assert payload["threshold_multiplier"] == 10.0
    assert payload["required_min_effective_lumi_fb"] == 361.0
    assert payload["override_used"] is False
    assert (tmp_path / "report" / "enforcement_policy_defaults.json").exists()


def test_smoke_artifacts_fail_closed_on_warning_fit(tmp_path: Path):
    smoke_outputs = tmp_path / "outputs_smoke_case"
    production_outputs = tmp_path / "outputs_full_case"

    for base in (smoke_outputs, production_outputs):
        write_json(
            {
                "status": "warning",
                "fit_status": 1,
                "cov_qual": 2,
                "backend": "pyroot_roofit",
            },
            base / "fit" / "FIT1" / "results.json",
        )
        write_json(
            {
                "status": "warning",
                "fit_status_free": 1,
                "fit_status_mu0": 1,
                "cov_qual_free": 2,
                "cov_qual_mu0": 2,
            },
            base / "fit" / "FIT1" / "significance_asimov.json",
        )

    result = write_smoke_and_repro_artifacts(
        {"source_summary": "analysis/analysis.summary.json", "config_hash": "abc123"},
        smoke_outputs,
        production_outputs,
    )

    assert result["smoke"]["status"] == "failed"
    assert any(check["status"] == "fail" for check in result["smoke"]["smoke_checks"])
    assert result["completion"]["status"] == "failed"
    assert result["skill_checkpoint"]["status"] == "failed"


def test_final_review_blocks_warning_fit_and_missing_inline_images(tmp_path: Path):
    outputs = tmp_path / "outputs_case"
    reports = tmp_path / "reports"

    write_text(
        "\n".join(
            [
                "# Report",
                "## Introduction",
                "## Dataset Description",
                "## Object Definitions And Event Selection",
                "## Signal, Control, And Blinding Regions",
                "## Distribution Plots",
                "## Statistical Interpretation",
                "## Summary",
            ]
        ),
        outputs / "report" / "report.md",
    )
    write_text("same", reports / "final_analysis_report.md")
    write_json({"plot_groups": {}}, outputs / "report" / "plots" / "manifest.json")
    write_json({"status": "ok"}, outputs / "report" / "artifact_link_inventory.json")
    write_json({"status": "ok", "failed_checks": []}, outputs / "report" / "enforcement_handoff_gate.json")
    write_json({"status": "none_found"}, outputs / "report" / "skill_extraction_summary.json")
    write_json({"status": "no_substantial_discrepancy"}, outputs / "report" / "data_mc_discrepancy_audit.json")
    write_json({"status": "pass"}, outputs / "report" / "skill_checkpoint_status.json")
    write_json({"status": "ok"}, outputs / "report" / "smoke_test_execution.json")
    write_json({"status": "ok"}, outputs / "report" / "verification_status.json")
    write_json({"status": "warning", "fit_status": 1, "cov_qual": 2}, outputs / "fit" / "FIT1" / "results.json")
    write_json(
        {"status": "ok", "fit_status_free": 0, "fit_status_mu0": 0, "cov_qual_free": 3, "cov_qual_mu0": 3},
        outputs / "fit" / "FIT1" / "significance_asimov.json",
    )
    write_json({"categories": {}}, outputs / "fit" / "FIT1" / "background_pdf_choice.json")

    review = write_final_review(outputs, reports)

    assert review["status"] == "blocked"
    assert "fit_stage_not_converged" in review["anomalies"]
    assert "report_markdown_has_no_inline_images" in review["consistency_issues"]
    assert review["handoff_ready"] is False


def test_verification_status_accepts_asimov_fit_plots(tmp_path: Path):
    plot_manifest = {
        "plot_groups": {
            "objects": {
                "photon_pt_leading": [],
                "photon_pt_subleading": [],
                "photon_eta_leading": [],
                "photon_eta_subleading": [],
            },
            "events": {
                "diphoton_mass_preselection": [],
                "diphoton_pt": [],
                "diphoton_deltaR": [],
                "photon_multiplicity": [],
                "cutflow_plot": [],
            },
            "control_regions_prefit": {"catA": []},
            "control_regions_postfit": {"catA": []},
            "fits": {"catA": [], "combined": []},
            "smoothing_sb_fit": {},
            "asimov_fits": {
                "free_fit": {"catA": [], "combined": []},
                "mu0_fit": {"catA": [], "combined": []},
            },
        }
    }
    fit_context = {
        "fit_summary": {"categories": ["catA"]},
        "smoothing_applied": False,
    }

    payload = write_verification_status(plot_manifest, fit_context, tmp_path)

    assert payload["status"] == "ok"
    assert payload["missing"] == []
