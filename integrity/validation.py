"""Structural and process detection consumes operational records only.

Truth is joined afterward, exclusively in evaluate(), to score the detector.
"""
from collections import Counter, defaultdict
from datetime import datetime
import re
from .dataset import REFERENCES, SCALES

def validate(data, mode=None):
    findings = []
    def error(code, record, detail):
        findings.append({"code": code, "record_id": record, "detail": detail})
    indices = {table: {r["id"]: r for r in rows} for table, rows in data.items()}
    # Fail clearly on malformed dates/types before any comparisons or joins.
    for table, rows in data.items():
        for row in rows:
            for field, value in row.items():
                if value is not None and (field.endswith("_at") or field in {"effective_from", "effective_to"}):
                    try:
                        parsed = datetime.fromisoformat(value)
                        if parsed.tzinfo is None:
                            raise ValueError("Timezone required")
                    except (ValueError, TypeError):
                        error("date_format", row["id"], f"{field} must be a timezone-aware ISO datetime.")
                if field in {"raw_score", "quoted_score", "template_score", "adjusted_score", "threshold_snapshot", "threshold", "case_threshold", "version"} and (type(value) is not int):
                    error("field_type", row["id"], f"{field} must be an integer.")
    if findings:
        return findings
    def dt(value):
        return datetime.fromisoformat(value) if value else None
    def rows_for(table, field):
        result = defaultdict(list)
        for row in data.get(table, []):
            result[row[field]].append(row)
        return result
    assignments = rows_for("assignment", "case_id")
    events = rows_for("caseevent", "case_id")
    decisions = rows_for("decision", "case_id")
    links = rows_for("decisionevidence", "decision_id")
    conflicts = {(r["reviewer_id"], r["learner_id"]) for r in data["reviewerconflict"]}
    appeals = {r["case_id"]: r for r in data["appeal"]}
    triage_records = {r["report_id"]: r for r in data["triagerecord"]}
    for table, rows in data.items():
        ids = [r["id"] for r in rows]
        if len(ids) != len(set(ids)):
            error("duplicate_id", table, "Primary IDs must be unique.")
        for row in rows:
            for field, parent in REFERENCES.get(table, {}).items():
                if row[field] is not None and row[field] not in indices[parent]:
                    error("foreign_key", row["id"], f"Missing {parent}: {row[field]}.")
    if any(f["code"] in {"foreign_key", "duplicate_id"} for f in findings):
        return findings  # Avoid misleading downstream join errors.
    if mode:
        submissions, flags, cases = SCALES[mode]
        if (len(data["submission"]), sum(r["flagged"] for r in data["similarityreport"]), len(data["case"])) != (submissions, flags, cases):
            error("volume", mode, "Requested submissions / flags / cases do not match.")
    patterns = {"submission": r"SUB-2026-\d{6}", "similarityreport": r"SIM-SUB-2026-\d{6}-01",
                "case": r"INT-2026-\d{6}", "evidenceitem": r"EVD-INT-2026-\d{6}-\d{3}",
                "appeal": r"APL-INT-2026-\d{6}-01"}
    for table, pattern in patterns.items():
        for row in data[table]:
            if not re.fullmatch(pattern, row["id"]):
                error("id_pattern", row["id"], "ID does not match the documented pattern.")
    enum_fields = {"case": {"state": {"triage", "review", "decided", "appeal", "closed"}},
                   "similarityreport": {"triage": {"pending", "dismissed", "case", "unflagged"}},
                   "assignment": {"phase": {"original", "appeal"}},
                   "decision": {"phase": {"original", "appeal"}, "outcome": {"cleared", "misconduct"}},
                   "appeal": {"resolution": {"", "upheld", "overturned"}}}
    for table, fields in enum_fields.items():
        for row in data[table]:
            for field, allowed in fields.items():
                if row[field] not in allowed:
                    error("enum", row["id"], f"Invalid {field}.")
    for table, fields in {"similarityreport": ["submission_id"], "case": ["report_id"], "appeal": ["case_id", "original_decision_id"],
                          "integrityrule": ["version"], "learner": ["email"]}.items():
        for field in fields:
            values = [r[field] for r in data[table]]
            if len(values) != len(set(values)):
                error("duplicate_relation", table, f"{field} must be unique.")
    for rule in data["integrityrule"]:
        if not 0 <= rule["threshold"] <= rule["case_threshold"] <= 100 or (rule["effective_to"] and dt(rule["effective_to"]) <= dt(rule["effective_from"])):
            error("rule", rule["id"], "Invalid rule thresholds or effective interval.")
    for report in data["similarityreport"]:
        scores = [report[k] for k in ["raw_score", "quoted_score", "template_score", "adjusted_score"]]
        if any(not 0 <= s <= 100 for s in scores) or scores[0] != sum(scores[1:]):
            error("arithmetic", report["id"], "Disjoint score components must reconcile in percentage points.")
        rule = indices["integrityrule"][report["rule_id"]]
        if report["threshold_snapshot"] != rule["threshold"] or report["flagged"] != (report["adjusted_score"] >= report["threshold_snapshot"]):
            error("threshold", report["id"], "Stored warning must match the effective threshold snapshot.")
        if dt(report["generated_at"]) < dt(indices["submission"][report["submission_id"]]["submitted_at"]) or dt(report["generated_at"]) < dt(rule["effective_from"]) or (rule["effective_to"] and dt(report["generated_at"]) >= dt(rule["effective_to"])):
            error("date_order", report["id"], "Report date violates submission or policy dates.")
        if report["flagged"] == (report["triage"] == "unflagged"):
            error("triage", report["id"], "Flag and triage status disagree.")
        if report["triage"] in {"case", "dismissed"} and len(report["triage_reason"].strip()) < 15:
            error("triage", report["id"], "Human triage requires rationale.")
        if report["triage"] in {"case", "dismissed"}:
            triage = triage_records.get(report["id"])
            if not triage or not triage["actor"] or triage["reason"] != report["triage_reason"] or triage["action"] != ("open" if report["triage"] == "case" else "dismiss") or dt(triage["occurred_at"]) < dt(report["generated_at"]):
                error("triage_audit", report["id"], "Triage requires a matching action, actor, reason and valid time.")
    for case in data["case"]:
        cid = case["id"]
        report = indices["similarityreport"][case["report_id"]]
        learner_id = indices["submission"][report["submission_id"]]["learner_id"]
        cevents = events[cid]
        event_ids = {(e["action"], e["related_id"]) for e in cevents}
        cdecisions = decisions[cid]
        if not report["flagged"] or report["triage"] != "case" or dt(case["opened_at"]) < dt(report["generated_at"]):
            error("case_origin", cid, "Case needs a triaged flag with valid dates.")
        if (case["state"] == "closed") != bool(case["closed_at"]):
            error("lifecycle", cid, "Closure timestamp and lifecycle disagree.")
        if case["closed_at"] and dt(case["closed_at"]) < dt(case["opened_at"]):
            error("date_order", cid, "Case closes before it opens.")
        if not any(e["action"] == "case_opened" for e in cevents):
            error("audit", cid, "Missing opening event.")
        if case["notification_at"] and not any(e["action"] == "learner_notified" for e in cevents):
            error("audit", cid, "Missing learner notice event.")
        if case["learner_response"] and not any(e["action"] in {"learner_response", "learner_response_recorded"} for e in cevents):
            error("audit", cid, "Missing learner response event.")
        original_reviewers = {a["reviewer_id"] for a in assignments[cid] if a["phase"] == "original"}
        for assignment in assignments[cid]:
            rid = assignment["reviewer_id"]
            if (rid, learner_id) in conflicts:
                error("conflicted_reviewer", assignment["id"], "Assigned reviewer has a recorded learner conflict.")
            if assignment["phase"] == "appeal" and rid in original_reviewers:
                error("nonindependent_appeal", assignment["id"], "Appeal reviewer participated in original review.")
            if not indices["reviewer"][rid]["active"] or not assignment["reason"].strip():
                error("assignment", assignment["id"], "Assignment needs an active reviewer and a reason.")
            if dt(assignment["assigned_at"]) < dt(case["opened_at"]) or (assignment["ended_at"] and dt(assignment["ended_at"]) < dt(assignment["assigned_at"])):
                error("date_order", assignment["id"], "Invalid assignment dates.")
            if ("reviewer_assigned", assignment["id"]) not in event_ids:
                error("audit", assignment["id"], "Missing assignment event.")
        phases = [d["phase"] for d in cdecisions]
        if len(phases) != len(set(phases)):
            error("duplicate_decision", cid, "Only one immutable decision is supported per phase.")
        for decision in cdecisions:
            did = decision["id"]
            selected = links[did]
            if len(decision["rationale"].strip()) < 15 or not selected:
                error("automatic_guilt", did, "A similarity warning was recorded as a finding without substantive rationale and evidence.")
            if not case["notification_at"] or not case["learner_response"] or (case["notification_at"] and dt(case["notification_at"]) > dt(decision["decided_at"])):
                error("due_process", did, "Decision lacks prior learner notice and response.")
            if not any(a["reviewer_id"] == decision["reviewer_id"] and a["phase"] == decision["phase"] and
                       dt(a["assigned_at"]) <= dt(decision["decided_at"]) and
                       (a["ended_at"] is None or dt(a["ended_at"]) > dt(decision["decided_at"])) for a in assignments[cid]):
                error("assignment", did, "Decision author was not assigned in this phase when the decision was made.")
            if decision["phase"] == "appeal" and decision["reviewer_id"] in original_reviewers:
                error("nonindependent_appeal", did, "Appeal decision author is not independent.")
            for link in selected:
                evidence = indices["evidenceitem"][link["evidence_id"]]
                if evidence["case_id"] != cid:
                    error("evidence_case", did, "Evidence belongs to another case.")
                if dt(evidence["added_at"]) > dt(decision["decided_at"]):
                    error("unlogged_late_evidence", evidence["id"], "Evidence was not available when this decision was made.")
            if ("decision_recorded", did) not in event_ids:
                error("audit", did, "Missing decision event.")
        if cid in appeals:
            appeal = appeals[cid]
            original = indices["decision"][appeal["original_decision_id"]]
            resolved = next((d for d in cdecisions if d["phase"] == "appeal"), None)
            if original["case_id"] != cid or original["phase"] != "original" or dt(appeal["submitted_at"]) < dt(original["decided_at"]):
                error("appeal_origin", appeal["id"], "Appeal must follow this case's original decision.")
            if appeal["resolved_at"]:
                if not resolved or dt(appeal["resolved_at"]) < dt(appeal["submitted_at"]):
                    error("nonindependent_appeal", appeal["id"], "Appeal resolved without an appeal decision or valid dates.")
                elif appeal["resolution"] != ("overturned" if original["outcome"] != resolved["outcome"] else "upheld"):
                    error("appeal_resolution", appeal["id"], "Appeal resolution disagrees with retained decisions.")
            elif case["state"] != "appeal":
                error("nonindependent_appeal", appeal["id"], "Pending appeal cannot be closed.")
        # Replay transitions from events, independent of stored final state.
        state = None
        for e in sorted(cevents, key=lambda e: (e["occurred_at"], e["id"])):
            action = e["action"]
            if dt(e["occurred_at"]) < dt(case["opened_at"]):
                error("date_order", e["id"], "Event precedes opening.")
            if action == "case_opened":
                state = "triage"
            elif action == "reviewer_assigned" and state == "triage":
                state = "review"
            elif action == "decision_recorded":
                d = indices["decision"].get(e["related_id"])
                if state not in {"review", "appeal"}:
                    error("lifecycle", e["id"], "Decision occurred outside an active review.")
                state = "closed" if d and d["phase"] == "appeal" else "decided"
            elif action == "appeal_submitted":
                if state not in {"decided", "closed"}:
                    error("lifecycle", e["id"], "Appeal occurred before a decision.")
                state = "appeal"
            elif action == "case_closed":
                if state not in {"decided", "closed"}:
                    error("lifecycle", e["id"], "Closure without a decision.")
                state = "closed"
        if state != case["state"]:
            error("lifecycle", cid, "Replayed event state does not match stored state.")
    for evidence in data["evidenceitem"]:
        logged = [e for e in events[evidence["case_id"]] if e["action"] == "evidence_added" and e["related_id"] == evidence["id"] and e["occurred_at"] == evidence["added_at"]]
        if not logged:
            error("unlogged_late_evidence", evidence["id"], "Evidence lacks a matching, timestamped provenance event.")
        if not evidence["excerpt"].strip() or not evidence["source_reference"].strip():
            error("evidence_provenance", evidence["id"], "Evidence needs source and excerpt.")
        if evidence["supersedes_id"]:
            previous = indices["evidenceitem"][evidence["supersedes_id"]]
            if previous["case_id"] != evidence["case_id"] or dt(previous["added_at"]) >= dt(evidence["added_at"]):
                error("evidence_version", evidence["id"], "Evidence versions must be same-case and strictly ordered.")
    return findings

def evaluate(data, truth, fixtures, negative_truth, mode="full"):
    baseline = validate(data, mode)
    # Detector never receives fixture_id, scenario or expected labels.
    detected = [{"fixture_id": fixture["fixture_id"], "findings": validate(fixture["records"])} for fixture in fixtures]
    expected = {(r["fixture_id"], r["expected_detection"]) for r in negative_truth}
    predicted = {(f["fixture_id"], finding["code"]) for f in detected for finding in f["findings"]}
    tp, fp, fn = len(expected & predicted), len(predicted - expected), len(expected - predicted)
    def ratio(numerator, denominator):
        return round(numerator / denominator, 6) if denominator else None
    labels = {r["submission_id"]: r for r in truth}
    known = [r for r in data["similarityreport"] if r["submission_id"] in labels]
    flagged = [r for r in known if r["flagged"]]
    legitimate = [r for r in known if not labels[r["submission_id"]]["misconduct"]]
    resolved = [a for a in data["appeal"] if a["resolved_at"]]
    durations = [(datetime.fromisoformat(c["closed_at"]) - datetime.fromisoformat(c["opened_at"])).total_seconds()/3600
                 for c in data["case"] if c["closed_at"]]
    record_cases = {row["id"]: row["case_id"] for table in ["evidenceitem", "assignment", "decision", "caseevent"] for row in data[table]}
    record_cases.update({c["id"]: c["id"] for c in data["case"]})
    incomplete_cases = {record_cases[f["record_id"]] for f in baseline if f["code"] in {"audit", "unlogged_late_evidence", "lifecycle"} and f["record_id"] in record_cases}
    return {"baseline_findings": baseline, "negative_results": detected,
        "counts": {table: len(rows) for table, rows in data.items()},
        "scenario_coverage": dict(sorted(Counter(t["scenario"] for t in truth).items())),
        "metrics": {"flag_rate": ratio(len(flagged), len(known)),
            "flag_to_case_rate": ratio(len(data["case"]), len(flagged)),
            "flag_precision": ratio(sum(labels[r["submission_id"]]["misconduct"] for r in flagged), len(flagged)),
            "false_positive_rate": ratio(sum(r["flagged"] for r in legitimate), len(legitimate)),
            "appeal_overturn_rate": ratio(sum(a["resolution"] == "overturned" for a in resolved), len(resolved)),
            "closed_case_mean_hours": ratio(sum(durations), len(durations)),
            "process_detection_precision": ratio(tp, tp+fp), "process_detection_recall": ratio(tp, tp+fn),
            "audit_complete_case_rate": ratio(len(data["case"]) - len(incomplete_cases), len(data["case"]))},
        "detection_confusion": {"true_positive": tp, "false_positive": fp, "false_negative": fn},
        "passed": not baseline and not fp and not fn}
