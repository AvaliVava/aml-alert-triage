"""Minimal, dependency-free foundation regression tests."""

import contextlib
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aml_triage.cli import main  # noqa: E402
from aml_triage.status import get_status  # noqa: E402


class FoundationTests(unittest.TestCase):
    def test_status_reports_no_classifier(self) -> None:
        status = get_status()
        self.assertEqual(status["phase"], "week-1-foundation")
        self.assertFalse(status["llm_classifier_implemented"])
        self.assertFalse(status["synthetic_generator_implemented"])

    def test_cli_returns_valid_json(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(["status"]), 0)
        payload = json.loads(out.getvalue())
        self.assertEqual(payload["project"], "aml-alert-triage")

    def test_project_context_files_exist(self) -> None:
        for filename in ["AGENTS.md", "PROJECT_STATUS.md", "DECISIONS.md", "WORKLOG.md"]:
            with self.subTest(filename=filename):
                self.assertTrue((ROOT / filename).is_file())


if __name__ == "__main__":
    unittest.main()
