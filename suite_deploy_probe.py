"""Developer-only deploy / persistence probe (``?dev=1``)."""

from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path
from typing import Any

# Bump on every production persistence deploy so live marker is obvious.
SUITE_BUILD_MARKER = "2026-06-08-prod-persist-v2"


def developer_mode(st: Any) -> bool:
    return bool(st.session_state.get("developer_mode"))


def init_developer_mode_from_query(st: Any) -> None:
    try:
        raw = st.query_params.get("dev")
        if isinstance(raw, list):
            raw = raw[0] if raw else ""
        if str(raw or "").strip().lower() in {"1", "true", "yes", "on"}:
            st.session_state["developer_mode"] = True
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


def cloud_config_probe() -> dict[str, Any]:
    out: dict[str, Any] = {
        "cloud_enabled": False,
        "storage_module": "",
        "suite_user_id_set": False,
        "config_error": None,
    }
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


def render_future_lens_deploy_probe(st: Any) -> None:
    if not developer_mode(st):
        return
    info = deploy_info()
    cloud = cloud_config_probe()
    ss = st.session_state
    ops = _persist_ops(st, "future_lens")
    reset_trace = ss.get("_fl_reset_render_trace")
    if not isinstance(reset_trace, dict):
        reset_trace = {}

    with st.sidebar.expander("Future Lens deploy probe", expanded=True):
        st.markdown("**Live deploy**")
        st.text(f"commit: {info['commit']}")
        st.text(f"branch: {info['branch']}")
        st.text(f"build_marker: {info['build_marker']}")

        st.markdown("**Modules**")
        st.text(f"suite_user_persistence loaded: {_module_loaded('suite_user_persistence')}")
        st.text(f"render_reset_controls exists: {_callable_exists('suite_user_persistence', 'render_reset_controls')}")
        st.text(f"suite_storage_supabase loaded: {_module_loaded('suite_storage_supabase')}")
        st.text(f"suite_storage loaded: {_module_loaded('suite_storage')}")

        st.markdown("**Saved Session UI**")
        st.text(f"render attempted: {reset_trace.get('attempted')}")
        st.text(f"render completed: {reset_trace.get('completed')}")
        err = reset_trace.get("error")
        if err:
            st.text(f"reset render error: {err}")

        st.markdown("**Cloud config**")
        st.text(f"cloud enabled: {cloud.get('cloud_enabled')}")
        st.text(f"storage module: {cloud.get('storage_module')}")
        st.text(f"suite_user_id set: {cloud.get('suite_user_id_set')}")
        if cloud.get("config_error"):
            st.warning(f"Cloud config: {cloud['config_error']}")
        elif not cloud.get("cloud_enabled"):
            st.warning(
                "Supabase/cloud persistence is NOT configured. "
                "Disk-only saves will not survive Streamlit Cloud reboot."
            )

        st.markdown("**Last save / restore**")
        for label, key in (
            ("last save source", "last_save_source"),
            ("last save cloud ok", "last_cloud_save_ok"),
            ("last save cloud error", "last_cloud_save_error"),
            ("last restore source", "last_restore_source"),
            ("last restore domain", "last_restore_domain"),
            ("cloud save attempted", "last_cloud_save_attempted"),
        ):
            val = ops.get(key)
            if val is not None and val != "":
                st.text(f"{label}: {val}")

        st.text(f"session broad_domain: {ss.get('broad_domain')}")
        st.text(f"final broad_domain: {ss.get('broad_domain')}")


def render_music_deploy_probe(st: Any) -> None:
    """Not used in Future Lens repo; kept for parity when copied."""
    pass
