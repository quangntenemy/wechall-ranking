from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("parse_module", ROOT / "scripts" / "parse.py")
PARSE_MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(PARSE_MODULE)


class ParseTests(unittest.TestCase):
    def test_parse_sample_html(self) -> None:
        html_path = ROOT / "data" / "history" / "2026-07-09.html"
        self.assertTrue(html_path.exists(), "sample HTML fixture should exist")

        data = PARSE_MODULE.parse_html_file(html_path, date_value="2026-07-09")

        self.assertEqual(data["date"], "2026-07-09")
        self.assertEqual(data["source"], "https://www.wechall.net/ranking")
        self.assertGreaterEqual(len(data["users"]), 1)
        first_user = data["users"][0]
        self.assertEqual(first_user["rank"], 1)
        self.assertEqual(first_user["username"], "rayaseiren")
        self.assertEqual(first_user["sites"], 43)
        self.assertEqual(first_user["totalscore"], 759439)
        self.assertEqual(first_user["English"], 574219)
        self.assertEqual(first_user["German"], 34682)


if __name__ == "__main__":
    unittest.main()
