"""Safe one-shot import of Future Lens persistence + resume helpers."""

from __future__ import annotations

from typing import Any, Callable

FL_ACTIVE_TAB_KEY = "_fl_active_tab_label"
FL_TAB_LABELS: tuple[str, ...] = (
    "\U0001f4c5 Evolution",
    "\U0001f50d Drivers",
    "\U0001f4a1 Future Advice",
    "\U0001f680 Simulation",
)

PERSISTENCE_OK = False
BOOT_ERROR: str | None = None


def _noop(*_args: Any, **_kwargs: Any) -> None:
    return None


def _noop_restore(_st: Any) -> bool:
    return False


def _default_apply_view(st: Any) -> None:
    if FL_ACTIVE_TAB_KEY not in st.session_state:
        st.session_state[FL_ACTIVE_TAB_KEY] = FL_TAB_LABELS[0]


apply_future_lens_session_defaults_if_missing: Callable[[Any], None] = _noop
restore_future_lens_state_once: Callable[[Any], bool] = _noop_restore
prepare_future_lens_workspace: Callable[[Any], bool] = _noop_restore
apply_future_lens_view_from_restore: Callable[[Any], None] = _default_apply_view
sync_future_lens_view_after_tab: Callable[[Any, str], None] = _noop
autosave_future_lens_state: Callable[[Any], None] = _noop
default_reset_future_lens_session: Callable[[Any], None] = _noop
apply_suite_fl_sim: Callable[[Any], None] = _noop
apply_suite_resume_launch: Callable[..., bool] = lambda *_a, **_k: False
persist_future_lens_decade_change: Callable[..., bool] = lambda *_a, **_k: False
apply_future_lens_decade_selection: Callable[..., dict] = lambda *_a, **_k: {}


try:
    from future_lens_persistent_state import (
        FL_ACTIVE_TAB_KEY as _FL_KEY,
        FL_TAB_LABELS as _FL_LABELS,
        _apply_suite_fl_sim,
        apply_future_lens_session_defaults_if_missing as _apply_defaults_if_missing,
        apply_future_lens_view_from_restore as _apply_view,
        autosave_future_lens_state as _autosave,
        default_reset_future_lens_session as _default_reset,
        apply_future_lens_decade_selection as _apply_decade_selection,
        persist_future_lens_decade_change as _persist_decade_change,
        prepare_future_lens_workspace as _prepare_workspace,
        record_decade_render_snapshot as _record_decade_render_snapshot,
        restore_future_lens_disk_shell as _restore_disk_shell,
        restore_future_lens_state_once as _restore_once,
        sync_future_lens_view_after_tab as _sync_tab,
    )
    from suite_resume_launch import apply_suite_resume_launch as _apply_resume_launch

    FL_ACTIVE_TAB_KEY = _FL_KEY
    FL_TAB_LABELS = _FL_LABELS
    apply_future_lens_session_defaults_if_missing = _apply_defaults_if_missing
    restore_future_lens_state_once = _restore_once
    prepare_future_lens_workspace = _prepare_workspace
    apply_future_lens_view_from_restore = _apply_view
    sync_future_lens_view_after_tab = _sync_tab
    autosave_future_lens_state = _autosave
    default_reset_future_lens_session = _default_reset
    apply_suite_fl_sim = _apply_suite_fl_sim
    apply_suite_resume_launch = _apply_resume_launch
    persist_future_lens_decade_change = _persist_decade_change
    apply_future_lens_decade_selection = _apply_decade_selection
    record_decade_render_snapshot = _record_decade_render_snapshot
    PERSISTENCE_OK = True
except Exception as exc:
    BOOT_ERROR = f"{type(exc).__name__}: {exc}"


def bootstrap_persistence(st: Any) -> bool:
    """Initialize workspace profile, restore scoped state, then resume params."""
    restored = False
    if not PERSISTENCE_OK:
        return False
    try:
        from suite_workspace import bootstrap_suite_workspace

        bootstrap_suite_workspace(st)
    except Exception:
        pass
    try:
        from future_lens_persistent_state import _WORKSPACE_PREPARED_KEY

        _restore_disk_shell(st)
        if not st.session_state.get(_WORKSPACE_PREPARED_KEY):
            restored = bool(prepare_future_lens_workspace(st))
            st.session_state[_WORKSPACE_PREPARED_KEY] = True
        else:
            restored = bool(st.session_state.get("_future_lens_disk_shell_had_state"))
        apply_future_lens_session_defaults_if_missing(st)
        apply_future_lens_view_from_restore(st)
    except Exception:
        pass
    try:
        apply_suite_resume_launch(st, "future_lens")
        apply_suite_fl_sim(st)
    except Exception:
        pass
    return restored
