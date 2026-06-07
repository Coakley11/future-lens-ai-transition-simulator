"""Import smoke tests — Future Lens startup must not crash on missing deps."""

from __future__ import annotations

import importlib
import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MODULES = (
    "activity_time",
    "future_lens_boot",
    "future_lens_persistent_state",
    "future_lens_sidebar",
    "suite_deploy_probe",
    "suite_storage_supabase",
    "suite_deep_links",
    "suite_resume_launch",
    "suite_cloud_state",
    "suite_user_persistence",
    "suite_activity_client",
)

COMPILE_TARGETS = (
    "streamlit_app.py",
    "future_lens_boot.py",
    "future_lens_persistent_state.py",
    "future_lens_sidebar.py",
    "suite_deploy_probe.py",
    "suite_storage_supabase.py",
    "suite_deep_links.py",
    "suite_resume_launch.py",
)


def test_import_smoke_modules():
    for name in MODULES:
        mod = importlib.import_module(name)
        assert mod is not None


def test_future_lens_boot_exports_tab_constants():
    import future_lens_boot as boot

    assert boot.FL_ACTIVE_TAB_KEY
    assert len(boot.FL_TAB_LABELS) == 4
    assert callable(boot.bootstrap_persistence)
    assert callable(boot.apply_future_lens_view_from_restore)


def test_py_compile_core_modules():
    for rel in COMPILE_TARGETS:
        path = ROOT / rel
        py_compile.compile(str(path), doraise=True)


def test_streamlit_app_imports_boot():
    import streamlit_app  # noqa: F401 — must not raise

    import future_lens_boot as boot

    assert boot.FL_TAB_LABELS
