"""Regression: Future Lens developer diagnostics workspace gate."""

from __future__ import annotations

import unittest

from suite_workspace import can_show_developer_tools, set_active_workspace_id


class _FakeSt:
    def __init__(self, workspace: str, *, dev_query: bool = False) -> None:
        self.session_state: dict = {}
        self.query_params = {"dev": "1"} if dev_query else {}
        set_active_workspace_id(self, workspace)  # type: ignore[arg-type]


class TestDeveloperWorkspaceGating(unittest.TestCase):
    def test_suite_deploy_probe_ariel_blocked(self) -> None:
        from suite_deploy_probe import developer_mode, init_developer_mode_from_query

        st = _FakeSt("ariel", dev_query=True)
        init_developer_mode_from_query(st)  # type: ignore[arg-type]
        self.assertFalse(developer_mode(st))  # type: ignore[arg-type]

    def test_suite_deploy_probe_daniel_dev(self) -> None:
        from suite_deploy_probe import developer_mode, init_developer_mode_from_query

        st = _FakeSt("daniel", dev_query=True)
        init_developer_mode_from_query(st)  # type: ignore[arg-type]
        self.assertTrue(developer_mode(st))  # type: ignore[arg-type]
        self.assertTrue(can_show_developer_tools(st=st))  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
