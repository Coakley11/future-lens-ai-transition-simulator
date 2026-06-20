"""Disk + cloud persistence for Future Lens."""

from __future__ import annotations

import copy
from typing import Any

from suite_user_persistence import autosave_if_changed, finalize_suite_reset, sync_workspace_protocol

APP_ID = "future_lens"
_DISK_SHELL_KEY = "_future_lens_disk_shell_applied"
_WORKSPACE_PREPARED_KEY = "_future_lens_workspace_prepared"

_SESSION_KEYS = (
    "broad_domain",
    "area",
    "specific_skill",
    "sim_year",
    "timeline_year",
    "wizard_complete",
)

_PERSIST_EXTRA_KEYS = (
    "_suite_fl_view",
    "_suite_fl_sim",
    "future_project",
)

_DEFAULTS: tuple[tuple[str, Any], ...] = (
    ("broad_domain", None),
    ("area", None),
    ("specific_skill", None),
    ("sim_year", 2030),
    ("timeline_year", None),
    ("wizard_complete", False),
)


FL_ACTIVE_TAB_KEY = "_fl_active_tab_label"

FL_TAB_LABELS: tuple[str, ...] = (
    "📅 Evolution",
    "🔍 Drivers",
    "💡 Future Advice",
    "🚀 Simulation",
)

FL_VIEW_TO_TAB_LABEL: dict[str, str] = {
    "timeline": "📅 Evolution",
    "drivers": "🔍 Drivers",
    "advice": "💡 Future Advice",
    "simulation": "🚀 Simulation",
    "skills": "💡 Future Advice",
}

FL_TAB_LABEL_TO_VIEW: dict[str, str] = {
    "📅 Evolution": "timeline",
    "🔍 Drivers": "drivers",
    "💡 Future Advice": "advice",
    "🚀 Simulation": "simulation",
}


def apply_future_lens_view_from_restore(st: Any) -> None:
    """Seed active tab from persisted ``_suite_fl_view`` before widgets render."""
    ss = st.session_state
    current = ss.get(FL_ACTIVE_TAB_KEY)
    if current in FL_TAB_LABELS:
        view = FL_TAB_LABEL_TO_VIEW.get(str(current))
        if view:
            ss["_suite_fl_view"] = view
        return
    view = str(ss.get("_suite_fl_view") or "").strip()
    label = FL_VIEW_TO_TAB_LABEL.get(view, FL_TAB_LABELS[0])
    ss[FL_ACTIVE_TAB_KEY] = label
    ss["_suite_fl_view"] = FL_TAB_LABEL_TO_VIEW.get(label, "timeline")


def sync_future_lens_view_after_tab(st: Any, tab_label: str) -> None:
    """Keep ``_suite_fl_view`` aligned with the selected tab for autosave."""
    view = FL_TAB_LABEL_TO_VIEW.get(tab_label)
    if view:
        st.session_state["_suite_fl_view"] = view


def _apply_suite_fl_sim(st: Any) -> None:
    """Map resume/deep-link hints onto wizard fields when missing."""
    ss = st.session_state
    domain = str(ss.get("broad_domain") or ss.get("_suite_fl_domain") or "").strip()
    area = str(ss.get("area") or ss.get("_suite_fl_area") or "").strip()
    sim = str(ss.get("_suite_fl_sim") or ss.get("specific_skill") or "").strip()
    if domain and not ss.get("broad_domain"):
        ss["broad_domain"] = domain
    if area and not ss.get("area"):
        ss["area"] = area
    if sim and not ss.get("specific_skill"):
        ss["specific_skill"] = sim
    project = str(ss.get("future_project") or "").strip()
    if project and " / " in project and not ss.get("broad_domain"):
        domain_part, _, area_part = project.partition(" / ")
        if domain_part.strip():
            ss["broad_domain"] = domain_part.strip()
        if area_part.strip():
            ss["area"] = area_part.strip()
    if domain and area:
        ss.setdefault("future_project", f"{domain} / {area}")


def build_future_lens_disk_state(st: Any) -> dict[str, Any]:
    ss = st.session_state
    state: dict[str, Any] = {}
    for key in _SESSION_KEYS:
        if key in ss:
            state[key] = copy.deepcopy(ss[key])
    for extra in _PERSIST_EXTRA_KEYS:
        if extra in ss and ss[extra]:
            state[extra] = copy.deepcopy(ss[extra])
    if ss.get("broad_domain") and ss.get("area"):
        state.setdefault(
            "future_project",
            f"{ss.get('broad_domain')} / {ss.get('area')}",
        )
    return state


def apply_future_lens_disk_state(st: Any, state: dict[str, Any]) -> None:
    for key, val in state.items():
        st.session_state[key] = copy.deepcopy(val)
    _apply_suite_fl_sim(st)
    apply_future_lens_view_from_restore(st)


def apply_future_lens_session_defaults(st: Any) -> None:
    ss = st.session_state
    for key in list(ss.keys()):
        if str(key).startswith("_suite_"):
            ss.pop(key, None)
    for key, default in _DEFAULTS:
        ss[key] = default
    ss.pop("future_project", None)
    ss.pop(FL_ACTIVE_TAB_KEY, None)


def apply_future_lens_session_defaults_if_missing(st: Any) -> None:
    """Seed wizard defaults only for keys not restored from disk/cloud."""
    ss = st.session_state
    for key, default in _DEFAULTS:
        if key not in ss:
            ss[key] = default


def clear_future_lens_startup_restore_flags(st: Any) -> None:
    """Reset shell restore flags when workspace profile changes."""
    for key in (
        _DISK_SHELL_KEY,
        "_future_lens_disk_shell_had_state",
        _WORKSPACE_PREPARED_KEY,
        FL_ACTIVE_TAB_KEY,
    ):
        st.session_state.pop(key, None)


def restore_future_lens_disk_shell(st: Any) -> bool:
    """Fast disk-only restore — once per session before widgets."""
    if st.session_state.get(_DISK_SHELL_KEY):
        return bool(st.session_state.get("_future_lens_disk_shell_had_state"))
    try:
        from suite_user_persistence import _load_raw

        disk_state, _, _ = _load_raw(APP_ID)
    except Exception:
        st.session_state[_DISK_SHELL_KEY] = True
        st.session_state["_future_lens_disk_shell_had_state"] = False
        return False
    if disk_state:
        apply_future_lens_disk_state(st, disk_state)
    st.session_state[_DISK_SHELL_KEY] = True
    st.session_state["_future_lens_disk_shell_had_state"] = bool(disk_state)
    return bool(disk_state)


def prepare_future_lens_workspace(st: Any, *, cloud_first: bool = True) -> bool:
    """Authoritative workspace-scoped disk + cloud sync before sidebar widgets."""
    return sync_workspace_protocol(
        st,
        APP_ID,
        apply_state=lambda st_obj, s: apply_future_lens_disk_state(st_obj, s),
        cloud_first=cloud_first,
    )


def restore_future_lens_state_once(st: Any) -> bool:
    """Backward-compatible alias — prefer ``prepare_future_lens_workspace()`` at startup."""
    return prepare_future_lens_workspace(st)


def autosave_future_lens_state(st: Any) -> dict[str, Any]:
    return autosave_if_changed(st, APP_ID, build_state=build_future_lens_disk_state)


def persist_future_lens_decade_change(
    st: Any,
    *,
    sim_year: int | None = None,
    timeline_year: int | None = None,
) -> bool:
    """Persist simulation/timeline decade immediately for the active workspace."""
    ss = st.session_state
    if sim_year is not None:
        ss["sim_year"] = sim_year
    if timeline_year is not None:
        ss["timeline_year"] = timeline_year
    from suite_user_persistence import _local_dirty_key, force_autosave

    ss[_local_dirty_key(APP_ID)] = True
    return force_autosave(
        st,
        APP_ID,
        build_state=build_future_lens_disk_state,
        reason="decade_change",
    )


def default_reset_future_lens_session(st: Any) -> None:
    """Full Future Lens reset: session, disk, and cloud ``full_session``."""
    apply_future_lens_session_defaults(st)
    fresh = build_future_lens_disk_state(st)
    finalize_suite_reset(st, APP_ID, fresh, summary="Reset to defaults")
