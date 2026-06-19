"""Developer-only deploy / persistence diagnostics (``?dev=1``)."""

from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path
from typing import Any

SUITE_BUILD_MARKER = "2026-06-08-prod-persist-v4"


def developer_mode(st: Any) -> bool:
    try:
        from suite_workspace import can_show_developer_tools

        return can_show_developer_tools(st=st)
    except ImportError:
        return bool(st.session_state.get("developer_mode"))


def init_developer_mode_from_query(st: Any) -> None:
    """Enable developer diagnostics when URL contains ``?dev=1`` (Daniel workspace only)."""
    try:
        raw = st.query_params.get("dev")
        if isinstance(raw, list):
            raw = raw[0] if raw else ""
        if str(raw or "").strip().lower() in {"1", "true", "yes", "on"}:
            try:
                from suite_workspace import is_developer_workspace

                if is_developer_workspace(st=st):
                    st.session_state["developer_mode"] = True
            except ImportError:
                pass
    except Exception:
        pass


def _git_short() -> str:
    env = str(os.environ.get("SOURCE_VERSION") or os.environ.get("COMMIT_SHA") or "").strip()
    if env:
        return env[:12]
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            timeout=2,
            cwd=str(Path(__file__).resolve().parent),
        )
        return out.decode().strip()
    except Exception:
        return "unknown"


def _git_branch() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL,
            timeout=2,
            cwd=str(Path(__file__).resolve().parent),
        )
        return out.decode().strip()
    except Exception:
        return "unknown"


def _module_loaded(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def _callable_exists(module_name: str, attr: str) -> bool:
    try:
        mod = __import__(module_name, fromlist=[attr])
        return callable(getattr(mod, attr, None))
    except Exception:
        return False


def _import_probe(name: str) -> tuple[bool, str | None]:
    try:
        __import__(name)
        return True, None
    except Exception as exc:
        return False, str(exc)


def cloud_config_probe() -> dict[str, Any]:
    out: dict[str, Any] = {
        "cloud_enabled": False,
        "storage_module": "",
        "suite_user_id_set": False,
        "config_error": None,
        "activity_time_ok": False,
        "activity_time_error": None,
    }
    ok, err = _import_probe("activity_time")
    out["activity_time_ok"] = ok
    out["activity_time_error"] = err

    try:
        from suite_storage_config import cloud_storage_enabled, get_cloud_config

        cfg = get_cloud_config()
        out["cloud_enabled"] = cloud_storage_enabled()
        out["suite_user_id_set"] = bool(str(cfg.get("suite_user_id") or "").strip())
    except Exception as exc:
        out["config_error"] = str(exc)
        return out
    try:
        from suite_cloud_state import _import_storage

        _, out["storage_module"] = _import_storage()
    except Exception as exc:
        out["config_error"] = out.get("config_error") or str(exc)
    return out


def deploy_info() -> dict[str, str]:
    return {
        "commit": _git_short(),
        "branch": _git_branch(),
        "build_marker": SUITE_BUILD_MARKER,
    }


def _persist_ops(st: Any, app_id: str) -> dict[str, Any]:
    raw = st.session_state.get("_suite_persist_ops")
    if not isinstance(raw, dict):
        return {}
    block = raw.get(app_id)
    return dict(block) if isinstance(block, dict) else {}


def _wizard_trace(st: Any) -> dict[str, Any]:
    raw = st.session_state.get("_fl_wizard_trace")
    return dict(raw) if isinstance(raw, dict) else {}


def _step2_lock_reason(st: Any) -> str:
    ss = st.session_state
    if not ss.get("broad_domain"):
        return "Step 2 locked: no domain selected (complete Step 1 first)."
    return ""


def render_future_lens_developer_diagnostics(st: Any) -> None:
    """Single sidebar expander for all ?dev=1 persistence / wizard diagnostics."""
    if not developer_mode(st):
        return

    info = deploy_info()
    cloud = cloud_config_probe()
    ss = st.session_state
    ops = _persist_ops(st, "future_lens")
    wiz = _wizard_trace(st)
    reset_trace = ss.get("_fl_reset_render_trace")
    if not isinstance(reset_trace, dict):
        reset_trace = {}

    restore_flag = bool(ss.get("_suite_disk_state_restored::future_lens"))
    restore_ok = bool(ops.get("last_restore_attempted")) and (
        ops.get("last_restore_source") not in (None, "", "none")
        or restore_flag
    )

    with st.expander("Developer diagnostics", expanded=True):
        st.markdown("**Live deploy**")
        st.text(f"commit: {info['commit']}")
        st.text(f"branch: {info['branch']}")
        st.text(f"build_marker: {info['build_marker']}")

        st.markdown("**Persistence modules**")
        sup_ok, sup_err = _import_probe("suite_user_persistence")
        st.text(f"suite_user_persistence loaded: {sup_ok}")
        if sup_err:
            st.text(f"  import error: {sup_err}")
        st.text(f"render_reset_controls exists: {_callable_exists('suite_user_persistence', 'render_reset_controls')}")
        st.text(f"activity_time loaded: {cloud.get('activity_time_ok')}")
        if cloud.get("activity_time_error"):
            st.error(f"activity_time import failed: {cloud['activity_time_error']}")

        st.markdown("**Saved Session UI**")
        st.text(f"render attempted: {reset_trace.get('attempted')}")
        st.text(f"render completed: {reset_trace.get('completed')}")
        if reset_trace.get("error"):
            st.text(f"Saved Session render error: {reset_trace['error']}")
        if reset_trace.get("messages_error"):
            st.text(f"persistence messages error: {reset_trace['messages_error']}")

        st.markdown("**Cloud**")
        st.text(f"cloud configured: {cloud.get('cloud_enabled')}")
        st.text(f"storage module: {cloud.get('storage_module')}")
        st.text(f"suite_user_id set: {cloud.get('suite_user_id_set')}")
        if cloud.get("config_error"):
            st.warning(f"Cloud config error: {cloud['config_error']}")
        elif not cloud.get("cloud_enabled"):
            st.warning("Cloud disabled — add [suite_activity] secrets or persistence will not survive reboot.")

        st.text(f"cloud save attempted: {ops.get('last_cloud_save_attempted')}")
        cloud_ok = ops.get("last_cloud_save_ok")
        st.text(f"cloud save success: {cloud_ok}")
        if ops.get("last_cloud_save_error"):
            st.error(f"cloud save error: {ops['last_cloud_save_error']}")
        elif cloud_ok is False and ops.get("last_cloud_save_attempted"):
            st.error("cloud save failed (see error above)")

        st.text(f"last save source: {ops.get('last_save_source', '—')}")

        st.markdown("**Restore**")
        st.text(f"restore attempted: {ops.get('last_restore_attempted', restore_flag)}")
        st.text(f"restore source: {ops.get('last_restore_source', 'none')}")
        st.text(f"restore success: {restore_ok}")
        if ops.get("last_restore_error"):
            st.text(f"restore error: {ops['last_restore_error']}")
        st.text(f"restored domain: {ops.get('last_restore_domain', '—')}")
        st.text(f"restored area: {ops.get('last_restore_area', '—')}")
        st.text(f"restored skill: {ops.get('last_restore_skill', '—')}")
        st.text(f"restored timeline_year: {ops.get('last_restore_timeline_year', '—')}")

        st.markdown("**Final session state**")
        st.text(f"domain: {ss.get('broad_domain')}")
        st.text(f"area: {ss.get('area')}")
        st.text(f"skill: {ss.get('specific_skill')}")
        st.text(f"timeline_year: {ss.get('timeline_year')}")

        st.markdown("**Wizard**")
        st.text(f"selected domain widget: {wiz.get('domain_widget_value', '—')}")
        st.text(f"session domain key: {ss.get('broad_domain')}")
        st.text(f"persisted domain key: {ops.get('last_saved_domain') or wiz.get('persisted_domain', '—')}")
        st.text(f"wizard_complete: {ss.get('wizard_complete')}")
        lock = _step2_lock_reason(st) or wiz.get("wizard_block_reason") or ""
        if lock:
            st.text(f"step 2 lock reason: {lock}")

        try:
            import future_lens_boot as boot

            st.text(f"persistence boot OK: {boot.PERSISTENCE_OK}")
            if boot.BOOT_ERROR:
                st.text(f"persistence boot error: {boot.BOOT_ERROR}")
        except Exception as exc:
            st.text(f"persistence boot import error: {exc}")


def render_future_lens_deploy_probe(st: Any) -> None:
    """Backward-compatible alias."""
    render_future_lens_developer_diagnostics(st)


def render_music_deploy_probe(st: Any) -> None:
    pass
