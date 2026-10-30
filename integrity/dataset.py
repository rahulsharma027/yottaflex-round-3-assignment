"""Pure, deterministic synthetic generation. No network, clock or database reads."""
import copy
import csv
import hashlib
import io
import json
import random
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

SEED = 20261022
GENERATOR_VERSION = 2
SCALES = {"starter": (100, 10, 3), "full": (10000, 1000, 300)}
SCENARIOS = ("legitimate_quotation", "shared_template", "false_positive", "successful_appeal", "unattributed_copying")
BASE = datetime(2026, 9, 1, 8, tzinfo=timezone.utc)
TABLES = ["learner", "assessment", "integrityrule", "reviewer", "reviewerconflict", "submission",
          "similarityreport", "triagerecord", "case", "assignment", "evidenceitem", "decision", "decisionevidence", "appeal", "caseevent"]
REFERENCES = {
    "reviewerconflict": {"reviewer_id": "reviewer", "learner_id": "learner"},
    "submission": {"learner_id": "learner", "assessment_id": "assessment"},
    "similarityreport": {"submission_id": "submission", "rule_id": "integrityrule"},
    "case": {"report_id": "similarityreport"},
    "triagerecord": {"report_id": "similarityreport"},
    "assignment": {"case_id": "case", "reviewer_id": "reviewer"},
    "evidenceitem": {"case_id": "case", "supersedes_id": "evidenceitem"},
    "decision": {"case_id": "case", "reviewer_id": "reviewer"},
    "decisionevidence": {"decision_id": "decision", "evidence_id": "evidenceitem"},
    "appeal": {"case_id": "case", "original_decision_id": "decision"},
    "caseevent": {"case_id": "case"},
}

def at(hours):
    return (BASE + timedelta(hours=hours)).isoformat()

def scenario_order(count, flags, case_count, seed):
    """Balance each score stratum, shuffle scenarios, and reserve the walkthroughs."""
    rng = random.Random(f"{seed}:scenarios")
    result = []
    for start, stop in [(0, case_count), (case_count, flags), (flags, count)]:
        pool = [n % len(SCENARIOS) for n in range(start, stop)]
        prefix = list(range(min(4, case_count))) if start == 0 else []
        for kind in prefix:
            pool.remove(kind)
        rng.shuffle(pool)
        result.extend(prefix + pool)
    return result

def academic_text(assessment, kind, number):
    """Original academic work contains no review verdicts or future process facts."""
    passages = [
        "Attribution makes the origin of an argument visible and allows readers to inspect its supporting sources.",
        "Responsible data use requires a clear purpose, proportionate collection, and an explanation of who benefits.",
        "A dataset describes a selected population, so sampling choices affect the conclusions that can be drawn.",
        "An algorithm is a finite sequence of steps whose assumptions determine which inputs it can handle.",
        "An academic argument connects a specific claim to relevant observations and explains the limits of that connection.",
    ]
    passage = passages[assessment]
    introduction = f"Study note {number % 97 + 1}. This discussion considers how a claim can be supported and tested in a practical setting."
    if kind == 0:
        body = f'Research Note A states, "{passage}" I use this principle to compare the assumptions in two examples.\n\nBibliography: Synthetic Research Note A, section {assessment + 1}.'
    elif kind == 1:
        body = f"Research question: identify the main assumption.\nMethod: compare two examples and record the relevant observations.\nDiscussion: {passage}\nConclusion: explain the limits of the available information."
    elif kind == 2:
        body = "I compare the starting assumptions in two examples before drawing a conclusion. Common technical terms help describe the problem, but each observation needs an explanation of how it supports the claim. A result from one setting may not apply to a different population or input."
    elif kind == 3:
        body = f'"{passage}" (Note A). My accompanying source notes identify the background reading. I compare this principle with the observations in two examples and discuss the limits of each explanation.'
    else:
        body = f"{passage} This principle can be applied to compare the assumptions in two examples and describe the limits of the available information."
    return introduction + "\n\n" + body

def generate(mode="full", seed=SEED):
    count, flags, case_count = SCALES[mode]
    rng = random.Random(seed)
    data = {table: [] for table in TABLES}
    truth = []
    first_names = ["Aarav", "Maya", "Riya", "Kabir", "Isha", "Arjun", "Sara", "Dev", "Nina", "Omar"]
    last_names = ["Mehta", "Sen", "Rao", "Iyer", "Das", "Shah", "Nair", "Roy", "Kapoor", "Ali"]
    for n in range(1, max(100, count // 5) + 1):
        data["learner"].append({"id": f"LRN-{n:05}", "name": f"{first_names[(n-1)%10]} {last_names[((n-1)//10)%10]} {n:03}",
            "email": f"learner{n}@example.invalid", "programme": "BSc Computer Science" if n % 2 else "BA Social Sciences"})
    titles = ["Research methods & citation", "Ethics in digital systems", "Data and society", "Foundations of computing", "Academic writing"]
    for n, title in enumerate(titles, 1):
        data["assessment"].append({"id": f"ASM-{n:03}", "title": title, "course": f"RES-{200+n}", "due_at": at(100)})
    data["integrityrule"].append({"id": "RULE-001", "version": 1, "title": "Context-aware similarity review",
        "threshold": 20, "case_threshold": 35, "effective_from": at(-1000), "effective_to": None,
        "description": "Disjoint quoted and template overlap is removed from raw similarity. Adjusted ≥20 triggers human triage; ≥35 is the synthetic historical case-opening policy. No score establishes guilt."})
    for n, (name, department) in enumerate([
        ("Dr. Mira Sen", "Academic Integrity"), ("Prof. James Okafor", "Research Methods"),
        ("Dr. Leena Rao", "Independent Appeals"), ("Dr. Theo Martin", "Computing"),
        ("Prof. Anika Das", "Social Sciences"), ("Dr. Evan Cole", "Writing Centre"),
    ], 1):
        data["reviewer"].append({"id": f"REV-{n:03}", "name": name, "department": department, "active": True})
    data["reviewerconflict"].append({"id": "COI-001", "reviewer_id": "REV-006", "learner_id": "LRN-00001",
                                      "reason": "Current academic supervisor of the learner."})
    learners = len(data["learner"])
    kinds = scenario_order(count, flags, case_count, seed)
    assessment_order = [n % len(titles) for n in range(count)]
    random.Random(f"{seed}:assessments").shuffle(assessment_order)
    for n in range(1, count + 1):
        sid = f"SUB-2026-{n:06}"
        assessment = assessment_order[n - 1]
        aid = f"ASM-{assessment + 1:03}"
        adjusted = rng.randint(35, 65) if n <= case_count else rng.randint(20, 34) if n <= flags else rng.randint(0, 19)
        quoted, template = rng.randint(0, 15), rng.randint(0, 10)
        # Facts precede outcomes: independently authored, attributed quotations,
        # shared templates, initially missing attribution, or unattributed copying.
        kind = kinds[n - 1]
        is_violation = kind == 4
        facts = [
            "The overlap is a correctly attributed quotation; citation and bibliography match the source.",
            "The highlighted passage is an assignment template supplied to all learners.",
            "An independently written explanation shares common technical language with the source.",
            "The submitted body mentions Note A, but its full attribution notes are absent from the initial comparison packet.",
            "The passage copies a synthetic source without quotation marks, attribution or an independent draft.",
        ][kind]
        data["submission"].append({"id": sid, "learner_id": f"LRN-{(n-1)%learners+1:05}", "assessment_id": aid,
            "title": f"{titles[assessment]} — essay {n:05}", "content": academic_text(assessment, kind, n),
            "submitted_at": at(n / count * 48)})
        data["similarityreport"].append({"id": f"SIM-{sid}-01", "submission_id": sid, "rule_id": "RULE-001",
            "raw_score": adjusted + quoted + template, "quoted_score": quoted, "template_score": template,
            "adjusted_score": adjusted, "flagged": n <= flags, "threshold_snapshot": 20,
            "generated_at": at(49 + n / count), "source_reference": f"synthetic://source/{n:06}",
            "triage": "case" if n <= case_count else "pending" if n <= (flags+case_count)//2 else "dismissed" if n <= flags else "unflagged",
            "triage_reason": "Historical human triage: adjusted overlap warrants formal context review." if n <= case_count else
                             "Historical triage reviewed the attributed or common material; no formal case required." if (flags+case_count)//2 < n <= flags else ""})
        truth.append({"submission_id": sid, "case_id": f"INT-2026-{n:06}" if n <= case_count else "",
            "misconduct": is_violation, "scenario": SCENARIOS[kind],
            "expected_final_outcome": "misconduct" if is_violation else "cleared", "process_anomaly": ""})
        if n <= case_count or (flags+case_count)//2 < n <= flags:
            report = data["similarityreport"][-1]
            data["triagerecord"].append({"id": f"TRI-{report['id']}", "report_id": report["id"],
                "action": "open" if n <= case_count else "dismiss", "actor": "academic-admin",
                "reason": report["triage_reason"], "occurred_at": at(51)})
        if n > case_count:
            continue
        cid = f"INT-2026-{n:06}"
        events = []
        def evt(action, hours, detail, related_id="", actor="academic-admin"):
            events.append({"id": f"EVT-{cid}-{len(events)+1:03}", "case_id": cid, "action": action,
                "actor": actor, "occurred_at": at(hours), "detail": detail, "related_id": related_id})
        # First three are walkthroughs; fourth is a resolved successful appeal.
        state = "closed" if n in (1, 2, 4) else ["triage", "review", "decided", "appeal", "closed"][(n-1)//5 % 5]
        if n == 3:
            state = "review"
        # All successful-appeal scenarios are resolved historical appeals.
        if kind == 3:
            state = "closed"
        evt("case_opened", 51, "Formal review opened after human triage. Similarity alone is not a finding.", f"SIM-{sid}-01")
        notice = at(52) if state != "triage" else None
        response = "Please consider my source notes and the assignment context in the evidence file." if notice else ""
        data["case"].append({"id": cid, "report_id": f"SIM-{sid}-01", "state": state, "opened_at": at(51),
            "closed_at": at(100 if kind == 3 else 80) if state == "closed" else None,
            "version": 1, "notification_at": notice, "learner_response": response})
        if notice:
            evt("learner_notified", 52, "Local in-app notice recorded; learner invited to respond.")
            evt("learner_response", 54, response, actor="synthetic-learner")
        if state != "triage":
            for r in ([1, 2] if kind == 2 else [1]):
                assignment_id = f"ASG-{cid}-{r:03}"
                data["assignment"].append({"id": assignment_id, "case_id": cid, "reviewer_id": f"REV-{r:03}",
                    "phase": "original", "assigned_at": at(53), "ended_at": None, "reason": "Eligible reviewer assigned after conflict screening."})
                evt("reviewer_assigned", 53, "Original reviewer assigned after conflict screening.", assignment_id)
        eid = f"EVD-{cid}-001"
        data["evidenceitem"].append({"id": eid, "case_id": cid, "title": "Source comparison and attribution notes",
            "excerpt": facts,
            "source_reference": f"synthetic://source/{n:06}", "added_at": at(55), "added_by": "support", "supersedes_id": None})
        evt("evidence_added", 55, "Source comparison and attribution notes added with provenance.", eid, actor="support")
        if state in {"decided", "appeal", "closed"}:
            outcome = "misconduct" if is_violation or kind == 3 else "cleared"
            did = f"DEC-{cid}-01"
            rationale = "Reviewed source evidence and learner response. " + ("Unattributed copying is substantiated by the source comparison." if outcome == "misconduct" else "Attribution or common material explains the overlap; no misconduct established.")
            data["decision"].append({"id": did, "case_id": cid, "reviewer_id": "REV-001", "phase": "original",
                "outcome": outcome, "rationale": rationale, "decided_at": at(70)})
            data["decisionevidence"].append({"id": f"DE-{cid}-01", "decision_id": did, "evidence_id": eid})
            evt("decision_recorded", 70, rationale, did, "reviewer")
            if kind == 3 or state == "appeal":
                apid = f"APL-{cid}-01"
                resolved = kind == 3
                data["appeal"].append({"id": apid, "case_id": cid, "original_decision_id": did,
                    "reason": "Please review the dated bibliography and independent draft that were not in the first evidence bundle.",
                    "submitted_at": at(75), "resolved_at": at(95) if resolved else None, "resolution": "overturned" if resolved else ""})
                evt("appeal_submitted", 75, "Learner requested review of omitted attribution evidence.", apid, "synthetic-learner")
                asid = f"ASG-{cid}-APL"
                data["assignment"].append({"id": asid, "case_id": cid, "reviewer_id": "REV-003", "phase": "appeal",
                    "assigned_at": at(76), "ended_at": None, "reason": "Independent reviewer with no original involvement or recorded conflict."})
                evt("reviewer_assigned", 76, "Independent appeal reviewer appointed.", asid)
                if resolved:
                    late_id = f"EVD-{cid}-002"
                    data["evidenceitem"].append({"id": late_id, "case_id": cid, "title": "Dated bibliography and draft",
                        "excerpt": "The original dated bibliography attributes the matching passage. Draft provenance confirms legitimate quotation.",
                        "source_reference": f"synthetic://learner-draft/{n:06}", "added_at": at(78), "added_by": "synthetic-learner", "supersedes_id": None})
                    evt("evidence_added", 78, "New attribution evidence logged after original decision; available to the appeal only.", late_id, "synthetic-learner")
                    adid = f"DEC-{cid}-02"
                    rationale = "Independent review of the dated attribution page explains the overlap. Original misconduct finding overturned."
                    data["decision"].append({"id": adid, "case_id": cid, "reviewer_id": "REV-003", "phase": "appeal",
                        "outcome": "cleared", "rationale": rationale, "decided_at": at(95)})
                    for j, ev in enumerate([eid, late_id], 1):
                        data["decisionevidence"].append({"id": f"DE-{cid}-02-{j}", "decision_id": adid, "evidence_id": ev})
                    evt("decision_recorded", 95, rationale, adid, "appeal-reviewer")
                    evt("appeal_resolved", 95, "Original finding overturned by independent review.", apid, "appeal-reviewer")
            if state == "closed":
                evt("case_closed", 100 if kind == 3 else 80, "Closed after a reasoned human decision; original records retained.")
        data["caseevent"].extend(events)
    for rows in data.values():
        rows.sort(key=lambda row: row["id"])
    return data, truth

def negative_fixtures(data):
    """Standalone relational slices; preserve the deliberately bad records."""
    # Use suitable historical cases independent of operational labels.
    closed = next(c for c in data["case"] if c["state"] == "closed" and c["id"].endswith("000001"))
    appealed = next((c for c in data["case"] if any(a["case_id"] == c["id"] and a["resolved_at"] for a in data["appeal"])), None)
    if appealed is None:  # Starter mode has three cases; use full same-generator case slice for coverage.
        full, _ = generate("full")
        return negative_fixtures(full)
    fixtures = []
    for code, target in [("automatic_guilt", closed), ("conflicted_reviewer", closed),
                         ("unlogged_late_evidence", closed), ("nonindependent_appeal", appealed)]:
        cid = target["id"]
        sliced = {table: [] for table in TABLES}
        for table in ["case", "assignment", "evidenceitem", "decision", "appeal", "caseevent"]:
            sliced[table] = [copy.deepcopy(r) for r in data[table] if r.get("case_id", r["id"] if table == "case" else "") == cid]
        dids = {d["id"] for d in sliced["decision"]}
        sliced["decisionevidence"] = [copy.deepcopy(r) for r in data["decisionevidence"] if r["decision_id"] in dids]
        report = next(r for r in data["similarityreport"] if r["id"] == target["report_id"])
        sub = next(s for s in data["submission"] if s["id"] == report["submission_id"])
        for table, ids in [("similarityreport", {report["id"]}), ("submission", {sub["id"]}),
                           ("learner", {sub["learner_id"]}), ("assessment", {sub["assessment_id"]}),
                           ("integrityrule", {report["rule_id"]})]:
            sliced[table] = [copy.deepcopy(r) for r in data[table] if r["id"] in ids]
        sliced["reviewer"] = copy.deepcopy(data["reviewer"])
        sliced["triagerecord"] = [copy.deepcopy(r) for r in data["triagerecord"] if r["report_id"] == report["id"]]
        sliced["reviewerconflict"] = [copy.deepcopy(r) for r in data["reviewerconflict"] if r["learner_id"] == sub["learner_id"]]
        if code == "automatic_guilt":
            d = sliced["decision"][0]
            d["outcome"], d["rationale"] = "misconduct", ""
            sliced["decisionevidence"] = []
        elif code == "conflicted_reviewer":
            sliced["assignment"][0]["reviewer_id"] = "REV-006"
            sliced["decision"][0]["reviewer_id"] = "REV-006"
        elif code == "unlogged_late_evidence":
            # The referenced evidence is changed after the decision, silently.
            sliced["evidenceitem"][0]["added_at"] = at(110)
            sliced["caseevent"] = [e for e in sliced["caseevent"] if e["action"] != "evidence_added"]
        else:
            next(d for d in sliced["decision"] if d["phase"] == "appeal")["reviewer_id"] = "REV-001"
            next(a for a in sliced["assignment"] if a["phase"] == "appeal")["reviewer_id"] = "REV-001"
        fixtures.append({"fixture_id": code, "records": sliced})
    return fixtures

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"

def write_exports(directory, mode="full", seed=SEED):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    data, truth = generate(mode, seed)
    (directory / "data.json").write_text(canonical(data), encoding="utf-8", newline="\n")
    (directory / "ground_truth.json").write_text(canonical(truth), encoding="utf-8", newline="\n")
    fixtures = negative_fixtures(data)
    (directory / "negative_fixtures.json").write_text(canonical(fixtures), encoding="utf-8", newline="\n")
    (directory / "negative_ground_truth.json").write_text(canonical([
        {"fixture_id": f["fixture_id"], "expected_detection": f["fixture_id"]} for f in fixtures
    ]), encoding="utf-8", newline="\n")
    db = sqlite3.connect(":memory:")
    for table, rows in data.items():
        if not rows:
            continue
        columns = list(rows[0])
        definitions = []
        for col in columns:
            sample = next((r[col] for r in rows if r[col] is not None), None)
            kind = "INTEGER" if isinstance(sample, (int, bool)) else "TEXT"
            definitions.append(f'"{col}" {kind}' + (" PRIMARY KEY" if col == "id" else ""))
        for col, parent in REFERENCES.get(table, {}).items():
            definitions.append(f'FOREIGN KEY("{col}") REFERENCES "{parent}"("id")')
        db.execute(f'CREATE TABLE "{table}" ({", ".join(definitions)})')
        quoted = ", ".join(f'"{col}"' for col in columns)
        db.executemany(f'INSERT INTO "{table}" ({quoted}) VALUES ({", ".join("?" for _ in columns)})',
                       [[row[col] for col in columns] for row in rows])
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        (directory / f"{table}.csv").write_text(stream.getvalue(), encoding="utf-8", newline="\n")
    (directory / "seed.sql").write_text("\n".join(db.iterdump()) + "\n", encoding="utf-8", newline="\n")
    db.close()
    manifest = {"generator_version": GENERATOR_VERSION, "seed": seed, "mode": mode, "source": "Entirely synthetic; no external learner data.",
                "counts": {table: len(rows) for table, rows in data.items()},
                "flagged_reports": sum(r["flagged"] for r in data["similarityreport"]),
                "sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(directory.iterdir()) if p.is_file() and p.name != "manifest.json"}}
    (directory / "manifest.json").write_text(canonical(manifest), encoding="utf-8", newline="\n")
    return manifest
