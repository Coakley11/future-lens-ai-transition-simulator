"""Disk + cloud persistence for Future Lens."""

from __future__ import annotations

import copy
from typing import Any

from suite_user_persistence import autosave_if_changed, finalize_suite_reset, restore_once

APP_ID = "future_lens"

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


def _apply_suite_fl_sim(st: Any) -> None:
    """Map resume/deep-link simulation hint onto wizard fields when missing."""
    sim = str(st.session_state.get("_suite_fl_sim") or "").strip()
    if not sim:
        return
    if not st.session_state.get("specific_skill"):
        st.session_state["specific_skill"] = sim
    project = str(st.session_state.get("future_project") or "").strip()
    if project and " / " in project and not st.session_state.get("broad_domain"):
        domain_part, _, area_part = project.partition(" / ")
        if domain_part.strip():
            st.session_state["broad_domain"] = domain_part.strip()
        if area_part.strip():
            st.session_state["area"] = area_part.strip()


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


def apply_future_lens_session_defaults(st: Any) -> None:
    ss = st.session_state
    for key in list(ss.keys()):
        if str(key).startswith("_suite_"):
            ss.pop(key, None)
    for key, default in _DEFAULTS:
        ss[key] = default
    ss.pop("future_project", None)


def apply_future_lens_session_defaults_if_missing(st: Any) -> None:
    """Seed wizard defaults only for keys not restored from disk/cloud."""
    ss = st.session_state
    for key, default in _DEFAULTS:
        if key not in ss:
            ss[key] = default


def restore_future_lens_state_once(st: Any) -> bool:
    return restore_once(
        st,
        APP_ID,
        apply_state=lambda st_obj, s: apply_future_lens_disk_state(st_obj, s),
    )


def autosave_future_lens_state(st: Any) -> None:
    autosave_if_changed(st, APP_ID, build_state=build_future_lens_disk_state)


def default_reset_future_lens_session(st: Any) -> None:
    """Full Future Lens reset: session, disk, and cloud ``full_session``."""
    apply_future_lens_session_defaults(st)
    fresh = build_future_lens_disk_state(st)
    finalize_suite_reset(st, APP_ID, fresh, summary="Reset to defaults")
