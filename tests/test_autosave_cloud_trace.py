"""Regression: autosave must report cloud failure, not pretend success."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from suite_cloud_state import CloudSaveResult
from suite_user_persistence import autosave_if_changed


class _FakeSt:
    def __init__(self) -> None:
        self.session_state: dict = {}


def test_autosave_records_cloud_failure():
    st = _FakeSt()

    def build(_st):
        return {"broad_domain": "Arts"}

    with patch("suite_user_persistence.save_user_state", return_value=True):
        with patch(
            "suite_cloud_state.save_cloud_full_session",
            return_value=CloudSaveResult(
                attempted=True,
                success=False,
                error="network",
                cloud_enabled=True,
            ),
        ):
            result = autosave_if_changed(st, "future_lens", build_state=build)

    assert result["cloud_ok"] is False
    assert result["cloud_error"] == "network"
    ops = st.session_state["_suite_persist_ops"]["future_lens"]
    assert ops["last_cloud_save_ok"] is False
    assert ops["last_cloud_save_error"] == "network"
