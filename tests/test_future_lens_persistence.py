"""Tests for Future Lens view/tab persistence."""

from __future__ import annotations

from future_lens_persistent_state import (
    FL_ACTIVE_TAB_KEY,
    FL_TAB_LABELS,
    apply_future_lens_disk_state,
    apply_future_lens_view_from_restore,
    sync_future_lens_view_after_tab,
)


class _FakeSt:
    def __init__(self) -> None:
        self.session_state = {}


def test_apply_view_from_restore_simulation_tab():
    st = _FakeSt()
    st.session_state["_suite_fl_view"] = "simulation"
    apply_future_lens_view_from_restore(st)
    assert st.session_state[FL_ACTIVE_TAB_KEY] == "🚀 Simulation"


def test_sync_view_after_tab_selection():
    st = _FakeSt()
    st.session_state[FL_ACTIVE_TAB_KEY] = FL_TAB_LABELS[1]
    sync_future_lens_view_after_tab(st, FL_TAB_LABELS[1])
    assert st.session_state["_suite_fl_view"] == "drivers"


def test_disk_state_restore_applies_view():
    st = _FakeSt()
    apply_future_lens_disk_state(
        st,
        {
            "broad_domain": "Technology",
            "area": "Software",
            "specific_skill": "Debugging",
            "_suite_fl_view": "simulation",
            "sim_year": 2050,
        },
    )
    assert st.session_state[FL_ACTIVE_TAB_KEY] == "🚀 Simulation"
    assert st.session_state["sim_year"] == 2050
