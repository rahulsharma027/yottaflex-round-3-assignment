import copy
import json
import sqlite3
import tempfile
from pathlib import Path
from django.test import SimpleTestCase
from integrity.dataset import generate, negative_fixtures, write_exports
from integrity.validation import evaluate, validate

class DatasetTests(SimpleTestCase):
    def test_full_counts_scenarios_and_baseline(self):
        data, truth = generate()
        self.assertEqual((len(data["submission"]), sum(r["flagged"] for r in data["similarityreport"]), len(data["case"])), (10000, 1000, 300))
        self.assertEqual(validate(data, "full"), [])
        self.assertEqual(len({t["scenario"] for t in truth}), 5)
        for rows in data.values():
            for row in rows:
                self.assertTrue({"scenario", "misconduct", "expected_final_outcome", "process_anomaly"}.isdisjoint(row))

    def test_four_isolated_anomalies_detected_before_truth_join(self):
        data, truth = generate()
        fixtures = negative_fixtures(data)
        expected = [{"fixture_id": f["fixture_id"], "expected_detection": f["fixture_id"]} for f in fixtures]
        report = evaluate(data, truth, fixtures, expected)
        self.assertTrue(report["passed"])
        self.assertEqual(report["detection_confusion"], {"true_positive": 4, "false_positive": 0, "false_negative": 0})
        self.assertEqual(validate(data, "full"), [])

    def test_corrupt_ids_joins_math_enums_and_state_are_detected(self):
        base, _ = generate("starter")
        mutations = [
            ("submission", "id", base["submission"][1]["id"], "duplicate_id"),
            ("submission", "learner_id", "MISSING", "foreign_key"),
            ("similarityreport", "raw_score", 101, "arithmetic"),
            ("case", "state", "convicted", "enum"),
            ("case", "state", "triage", "lifecycle"),
        ]
        for table, field, value, expected in mutations:
            data = copy.deepcopy(base)
            data[table][0][field] = value
            with self.subTest(field=field, expected=expected):
                self.assertIn(expected, {f["code"] for f in validate(data)})

    def test_reproducible_exports_and_sql_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            left, right = Path(tmp)/"a", Path(tmp)/"b"
            a, b = write_exports(left, "starter"), write_exports(right, "starter")
            self.assertEqual(a, b)
            self.assertEqual({p.name: p.read_bytes() for p in left.iterdir()}, {p.name: p.read_bytes() for p in right.iterdir()})
            conn = sqlite3.connect(":memory:")
            conn.executescript((left/"seed.sql").read_text(encoding="utf-8"))
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM submission").fetchone()[0], 100)
            self.assertEqual(conn.execute("PRAGMA foreign_key_check").fetchall(), [])
            conn.close()

    def test_seed_changes_variation_but_preserves_required_counts(self):
        first, _ = generate("starter", 1)
        second, _ = generate("starter", 2)
        self.assertNotEqual(first["similarityreport"], second["similarityreport"])
        self.assertEqual(validate(second, "starter"), [])

    def test_malformed_datetime_and_numeric_type_fail_clearly(self):
        data, _ = generate("starter")
        data["case"][0]["opened_at"] = "not-a-date"
        self.assertIn("date_format", {f["code"] for f in validate(data)})
        data, _ = generate("starter")
        data["similarityreport"][0]["raw_score"] = "56"
        self.assertIn("field_type", {f["code"] for f in validate(data)})
