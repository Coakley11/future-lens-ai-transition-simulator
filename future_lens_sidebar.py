"""Future Lens sidebar: Saved Session + suite-standard layout."""

from __future__ import annotations

from typing import Any, Callable


def render_saved_session_controls(
    st: Any,
    *,
    on_reset: Callable[[Any], None],
) -> None:
    """
    Render Saved session / Reset directly under Command Center.

    Always visible for normal users; records render status for ?dev=1 diagnostics.
    """
    trace: dict[str, Any] = st.session_state.setdefault("_fl_reset_render_trace", {})
    trace["attempted"] = True

    try:
        from suite_user_persistence import render_reset_controls

        render_reset_controls(
            st,
            "future_lens",
            on_reset=on_reset,
            help_text="Clears wizard progress, local disk, and cloud session for Future Lens.",
            in_sidebar=True,
        )
        trace["completed"] = True
        trace.pop("error", None)
    except Exception as exc:
        trace["completed"] = False
        trace["error"] = str(exc)
        with st.expander("Saved session", expanded=False):
            st.caption("Saved session controls could not load.")
            if st.session_state.get("developer_mode"):
                st.code(str(exc))
