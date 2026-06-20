"""Future Lens workspace profile isolation — Daniel vs Ariel state separation."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from future_lens_persistent_state import (
    apply_future_lens_disk_state,
    build_future_lens_disk_state,
    prepare_future_lens_workspace,
)
from suite_user_persistence import save_user_state, state_file_path
from suite_workspace import scoped_cloud_app_id


class _FakeSessionState(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):
        self[name] = value


class _FakeSt:
    def __init__(self, state: _FakeSessionState) -> None:
        self.session_state = state


class TestFutureLensWorkspaceIsolation(unittest.TestCase):
    def test_scoped_cloud_app_id(self) -> None:
        self.assertEqual(scoped_cloud_app_id("future_lens", "daniel"), "future_lens")
        self.assertEqual(scoped_cloud_app_id("future_lens", "ariel"), "future_lens__ariel")

    def test_daniel_and_ariel_disk_paths_differ(self) -> None:
        daniel = state_file_path("future_lens", "daniel")
        ariel = state_file_path("future_lens", "ariel")
        self.assertNotEqual(daniel, ariel)
        self.assertIn("workspaces", str(daniel))
        self.assertIn("ariel", str(ariel))

    def test_separate_domain_area_persist_per_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            with patch("suite_workspace.DATA_DIR", data), patch("suite_user_persistence.DATA_DIR", data):
                save_user_state(
                    "future_lens",
                    {
                        "broad_domain": "Technology",
                        "area": "Computer programming",
                        "specific_skill": "Debugging",
                        "_suite_fl_view": "simulation",
                    },
                    workspace_id="daniel",
                )
                save_user_state(
                    "future_lens",
                    {
                        "broad_domain": "Finance",
                        "area": "Personal investing",
                        "specific_skill": "Spreadsheet modeling",
                        "_suite_fl_view": "timeline",
                    },
                    workspace_id="ariel",
                )
                daniel_blob = json.loads(state_file_path("future_lens", "daniel").read_text(encoding="utf-8"))
                ariel_blob = json.loads(state_file_path("future_lens", "ariel").read_text(encoding="utf-8"))
            self.assertEqual(daniel_blob["state"]["broad_domain"], "Technology")
            self.assertEqual(ariel_blob["state"]["broad_domain"], "Finance")
            self.assertEqual(daniel_blob["state"]["specific_skill"], "Debugging")
            self.assertEqual(ariel_blob["state"]["specific_skill"], "Spreadsheet modeling")

    def test_prepare_future_lens_workspace_applies_disk_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            with patch("suite_workspace.DATA_DIR", data), patch("suite_user_persistence.DATA_DIR", data):
                save_user_state(
                    "future_lens",
                    build_future_lens_disk_state(
                        _FakeSt(
                            _FakeSessionState(
                                {
                                    "broad_domain": "Technology",
                                    "area": "Computer programming",
                                    "specific_skill": "Debugging",
                                    "_suite_fl_view": "simulation",
                                }
                            )
                        ),
                    ),
                    workspace_id="daniel",
                )
                ss = _FakeSessionState({})
                st = _FakeSt(ss)
                with patch("suite_workspace.resolve_workspace_id", return_value="daniel"):
                    applied = prepare_future_lens_workspace(st)
                self.assertTrue(applied)
                self.assertEqual(ss.get("broad_domain"), "Technology")
                self.assertEqual(ss.get("specific_skill"), "Debugging")
                self.assertEqual(ss.get("_suite_fl_view"), "simulation")

    def test_activity_tags_workspace_id(self) -> None:
        with patch("suite_workspace.get_active_workspace_id", return_value="ariel"):
            with patch("suite_activity_client.record_activity") as mock_record:
                from future_lens_activity import log_career_analysis

                log_career_analysis(
                    scenario="Finance transition",
                    domain="Finance",
                    area="Personal investing",
                    skill="Spreadsheet modeling",
                )
        metrics = mock_record.call_args.kwargs.get("metrics") or mock_record.call_args[1].get("metrics")
        self.assertEqual(metrics.get("workspace_id"), "ariel")


if __name__ == "__main__":
    unittest.main()
