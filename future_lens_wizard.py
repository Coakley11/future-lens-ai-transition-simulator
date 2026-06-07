"""Future Lens wizard session keys + developer persistence trace."""

from __future__ import annotations

from typing import Any

FL_WIZARD_KEYS: tuple[tuple[str, Any], ...] = (
    ("broad_domain", None),
    ("area", None),
    ("specific_skill", None),
    ("sim_year", 2030),
    ("timeline_year", None),
    ("wizard_complete", False),
)

TRACE_KEY = "_fl_wizard_trace"
FL_PERSIST_DEPLOY_VERSION = "2026-06-08-fl-wizard-fix-v1"


def init_developer_mode_from_query(st: Any) -> None:
    try:
        raw = st.query_params.get("dev")
        if isinstance(raw, list):
            raw = raw[0] if raw else ""
        if str(raw or "").strip().lower() in {"1", "true", "yes", "on"}:
            st.session_state["developer_mode"] = True
    except Exception:
        pass


def developer_mode(st: Any) -> bool:
    return bool(st.session_state.get("developer_mode"))


def ensure_wizard_session_keys(st: Any) -> None:
    ss = st.session_state
    for key, default in FL_WIZARD_KEYS:
        ss.setdefault(key, default)


def select_domain(st: Any, domain: str) -> None:
    prev = st.session_state.get("broad_domain")
    st.session_state["broad_domain"] = domain
    if prev != domain:
        st.session_state["area"] = None
        st.session_state["specific_skill"] = None
        st.session_state["timeline_year"] = None
    update_trace(
        st,
        domain_widget_value=domain,
        session_broad_domain=domain,
        wizard_block_reason="",
    )


def update_trace(st: Any, **fields: Any) -> None:
    trace = st.session_state.get(TRACE_KEY)
    if not isinstance(trace, dict):
        trace = {}
    trace.update(fields)
    trace.setdefault("deploy_version", FL_PERSIST_DEPLOY_VERSION)
    st.session_state[TRACE_KEY] = trace


def render_wizard_trace(st: Any) -> None:
    if not developer_mode(st):
        return
    ss = st.session_state
    domain = ss.get("broad_domain")
    block = "Select a domain above to continue." if not domain else ""
    update_trace(
        st,
        session_broad_domain=domain,
        persisted_domain=domain,
        final_domain=domain,
        wizard_complete=ss.get("wizard_complete"),
        wizard_block_reason=block,
    )
    trace = ss.get(TRACE_KEY) or {}
    with st.sidebar.expander("Future Lens wizard trace", expanded=False):
        st.caption(f"Deploy: {trace.get('deploy_version', FL_PERSIST_DEPLOY_VERSION)}")
        st.caption(f"Persistence OK: {trace.get('persistence_ok')}")
        for label, key in (
            ("session domain", "session_broad_domain"),
            ("restore ran", "restore_ran"),
            ("default init ran", "default_init_ran"),
            ("persistence boot error", "boot_error"),
            ("wizard block reason", "wizard_block_reason"),
        ):
            val = trace.get(key)
            if val is not None and val != "":
                st.text(f"{label}: {val}")
