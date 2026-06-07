"""Future Lens wizard domain selection."""

from __future__ import annotations

from future_lens_wizard import ensure_wizard_session_keys, select_domain


class _FakeSt:
    def __init__(self) -> None:
        self.session_state: dict = {}


def test_select_domain_sets_session_and_clears_children():
    st = _FakeSt()
    st.session_state["broad_domain"] = None
    st.session_state["area"] = "Old"
    select_domain(st, "Technology")
    assert st.session_state["broad_domain"] == "Technology"
    assert st.session_state["area"] is None
    assert st.session_state["specific_skill"] is None


def test_ensure_wizard_session_keys_defaults():
    st = _FakeSt()
    ensure_wizard_session_keys(st)
    assert "broad_domain" in st.session_state
    assert st.session_state["sim_year"] == 2030
