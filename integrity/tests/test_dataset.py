import copy
import json
import sqlite3
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from django.test import SimpleTestCase
from integrity.dataset import generate, negative_fixtures, write_exports
from integrity.validation import evaluate, validate

class DatasetTests(SimpleTestCase):
    def test_original_submissions_do_not_disclose_process_events_or_findings(self):
        data, _ = generate("full")
        for submission in data["submission"]:
            text = submission["content"].lower()
            for term in ["appeal", "overturned", "misconduct", "cleared", "reviewer", "evidence bundle", "initial report", "source comparison"]:
                self.assertNotIn(term, text, submission["id"])
        assessment_titles = {a["id"]: a["title"] for a in data["assessment"]}
        for submission in data["submission"]:
            self.assertTrue(submission["title"].startswith(assessment_titles[submission["assessment_id"]]))

    def test_scenarios_are_mixed_across_assessments_learners_and_score_strata(self):
        for seed in [20261022, 1]:
            data, truth = generate("full", seed)
            labels = {row["submission_id"]: row for row in truth}
            for group in [data["submission"], data["submission"][:300], data["submission"][:1000], data["submission"][1000:]]:
                by_assessment = defaultdict(set)
                for submission in group:
                    by_assessment[submission["assessment_id"]].add(labels[submission["id"]]["scenario"])
                self.assertEqual(len(by_assessment), 5)
                self.assertTrue(all(len(scenarios) == 5 for scenarios in by_assessment.values()))
            by_learner = defaultdict(set)
            for submission in data["submission"]:
                by_learner[submission["learner_id"]].add(labels[submission["id"]]["misconduct"])
            self.assertGreater(sum(len(outcomes) == 2 for outcomes in by_learner.values()), len(by_learner) // 2)
            self.assertEqual(set(Counter(row["scenario"] for row in truth).values()), {2000})
            self.assertEqual(set(Counter(row["scenario"] for row in truth[:1000]).values()), {200})

    def test_walkthroughs_and_appeal_evidence_keep_their_historical_boundaries(self):
        data, truth = generate("full")
        self.assertEqual([row["scenario"] for row in truth[:4]],
            ["legitimate_quotation", "shared_template", "false_positive", "successful_appeal"])
        original = next(d for d in data["decision"] if d["case_id"] == "INT-2026-000004" and d["phase"] == "original")
        appeal = next(d for d in data["decision"] if d["case_id"] == "INT-2026-000004" and d["phase"] == "appeal")
        late = next(e for e in data["evidenceitem"] if e["case_id"] == "INT-2026-000004" and e["title"] == "Dated bibliography and draft")
        self.assertLess(original["decided_at"], late["added_at"])
        self.assertLess(late["added_at"], appeal["decided_at"])
        original_links = {r["evidence_id"] for r in data["decisionevidence"] if r["decision_id"] == original["id"]}
        self.assertNotIn(late["id"], original_links)
        for item in data["evidenceitem"]:
            if item["added_at"] < original["decided_at"]:
                self.assertNotIn("on appeal", item["excerpt"].lower())

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

    def test_external_response_event_is_recognized_without_changing_baseline_data(self):
        data, _ = generate("starter")
        response = next(e for e in data["caseevent"] if e["case_id"] == "INT-2026-000001" and e["action"] == "learner_response")
        response.update(action="learner_response_recorded", actor="support", related_id="LRN-00001",
            detail="Externally received response. Source reference: Signed statement REF-001. Learner response retained.")
        self.assertEqual(validate(data, "starter"), [])
