"""Developer diagnostics and sidebar layout tests."""

from __future__ import annotations


def test_dev_mode_from_query_param():
    class _QP:
        def get(self, key):
            return "1" if key == "dev" else None

    class _St:
        session_state = {}
        query_params = _QP()

    from suite_deploy_probe import developer_mode, init_developer_mode_from_query

    init_developer_mode_from_query(_St())
    assert developer_mode(_St()) is True


def test_saved_session_helper_sets_attempted_trace():
    class _St:
        session_state = {}

    from future_lens_sidebar import render_saved_session_controls

    try:
        render_saved_session_controls(_St(), on_reset=lambda _s: None)
    except AttributeError:
        pass
    trace = _St.session_state.get("_fl_reset_render_trace")
    assert trace.get("attempted") is True
