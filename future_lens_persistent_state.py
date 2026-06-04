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

_DEFAULTS: tuple[tuple[str, Any], ...] = (
    ("broad_domain", None),
    ("area", None),
    ("specific_skill", None),
    ("sim_year", 2030),
    ("timeline_year", None),
    ("wizard_complete", False),
)


def build_future_lens_disk_state(st: Any) -> dict[str, Any]:
    ss = st.session_state
    state: dict[str, Any] = {}
    for key in _SESSION_KEYS:
        if key in ss:
            state[key] = copy.deepcopy(ss[key])
    for extra in ("_suite_fl_view",):
        if extra in ss and ss[extra]:
            state[extra] = ss[extra]
    return state


def apply_future_lens_disk_state(st: Any, state: dict[str, Any]) -> None:
    for key, val in state.items():
        st.session_state[key] = copy.deepcopy(val)


def apply_future_lens_session_defaults(st: Any) -> None:
    ss = st.session_state
    for key in list(ss.keys()):
        if str(key).startswith("_suite_"):
            ss.pop(key, None)
    for key, default in _DEFAULTS:
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
