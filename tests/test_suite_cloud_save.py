"""Cloud save must use suite_storage_supabase when suite_storage is absent."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import suite_account
from suite_cloud_state import CloudSaveResult, clear_cloud_full_session, save_cloud_full_session


def test_resolve_storage_falls_back_to_supabase():
    with patch.dict("sys.modules", {"suite_storage": None}):
        storage = suite_account._resolve_storage()
        assert storage.__name__ == "suite_storage_supabase"


def test_save_cloud_full_session_writes_full_session_blob():
    mock_storage = MagicMock()
    mock_storage.normalize_app_key = lambda app: app
    state = {"broad_domain": "Technology", "area": "Software"}

    with patch("suite_cloud_state.cloud_storage_enabled", return_value=True, create=True):
        with patch("suite_storage_config.cloud_storage_enabled", return_value=True):
            with patch("suite_cloud_state._import_storage", return_value=(mock_storage, "suite_storage_supabase")):
                result = save_cloud_full_session("future_lens", state, page="simulation", summary="Tech")

    assert isinstance(result, CloudSaveResult)
    assert result.success is True
    assert result.storage_module == "suite_storage_supabase"
    mock_storage.save_current_state.assert_called_once()
    _args, kwargs = mock_storage.save_current_state.call_args
    assert _args[0] == "future_lens"
    assert kwargs["metrics"]["full_session"]["broad_domain"] == "Technology"


def test_clear_cloud_full_session():
    mock_storage = MagicMock()
    mock_storage.normalize_app_key = lambda app: app

    with patch("suite_storage_config.cloud_storage_enabled", return_value=True):
        with patch("suite_cloud_state._import_storage", return_value=(mock_storage, "suite_storage_supabase")):
            result = clear_cloud_full_session("future_lens")

    assert result.success is True
    mock_storage.save_current_state.assert_called_once()
