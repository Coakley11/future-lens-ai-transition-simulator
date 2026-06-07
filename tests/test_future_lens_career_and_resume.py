"""Future Lens E1/E2 — career logging metrics and resume URL restore."""

from __future__ import annotations

from unittest.mock import patch

from future_lens_activity import log_career_analysis
from future_lens_persistent_state import _apply_suite_fl_sim
from suite_resume_launch import _apply_future_lens


class _FakeSt:
    def __init__(self, qp: dict | None = None) -> None:
        self.session_state: dict = {}
        self.query_params = qp or {}


def test_log_career_analysis_metrics_include_domain_area():
    captured: dict = {}

    def _fake_record(event, **kwargs):
        captured["event"] = event
        captured.update(kwargs)

    with patch("future_lens_activity._record", side_effect=_fake_record):
        log_career_analysis(
            scenario="Technology / Programming / Debugging",
            domain="Technology",
            area="Computer programming",
            skill="Debugging",
            sim_year=2040,
            timeline_year=2025,
        )

    assert captured["event"] == "career_analysis"
    metrics = captured["metrics"]
    assert metrics["broad_domain"] == "Technology"
    assert metrics["area"] == "Computer programming"
    assert metrics["specific_skill"] == "Debugging"
    assert metrics["sim_year"] == 2040
    assert metrics["timeline_year"] == 2025
    assert captured["resume_key"].startswith("career:")


def test_apply_future_lens_resume_query_params():
    st = _FakeSt(
        {
            "suite_sim": "Debugging",
            "suite_fl_domain": "Technology",
            "suite_fl_area": "Computer programming",
            "suite_fl_sim_year": "2040",
            "suite_fl_timeline_year": "2025",
            "suite_fl_view": "simulation",
            "suite_page": "simulation",
            "suite_resume": "career:Technology / Computer programming / Debugging",
        }
    )
    _apply_future_lens(st, st.query_params["suite_resume"], "simulation")
    assert st.session_state["broad_domain"] == "Technology"
    assert st.session_state["area"] == "Computer programming"
    assert st.session_state["specific_skill"] == "Debugging"
    assert st.session_state["sim_year"] == 2040
    assert st.session_state["timeline_year"] == 2025
    assert st.session_state["_suite_fl_view"] == "simulation"
    assert st.session_state["future_project"] == "Technology / Computer programming"


def test_apply_suite_fl_sim_from_resume_keys():
    st = _FakeSt()
    st.session_state["_suite_fl_sim"] = "Spreadsheet modeling"
    st.session_state["future_project"] = "Finance / Personal investing"
    _apply_suite_fl_sim(st)
    assert st.session_state["specific_skill"] == "Spreadsheet modeling"
    assert st.session_state["broad_domain"] == "Finance"
    assert st.session_state["area"] == "Personal investing"
