# Reviewer walkthrough

This guide covers the interface improvements and the three completed audit fixes. F4 (response chronology validation), F5 (accessibility gaps), and F6 (AI/candidate-review reconciliation) remain open.

| Fix | Result | Commit |
|---|---|---|
| F1 | Administrators/support can record sourced external responses for learners without logins, preserving the real staff recorder and response history | [ded02e6](https://github.com/rahulsharma027/yottaflex-round-3-assignment/commit/ded02e633a0ec4b74743b167e3e32187e9433f5f) |
| F2 | Learners can revise only their own current evidence and add separate rebuttals; staff evidence remains protected from learner replacement | [64356fb](https://github.com/rahulsharma027/yottaflex-round-3-assignment/commit/64356fb87031ce79274e6b112140ac17608e1f61) |
| F3 | Generator revision 2 removes future appeal information from original submissions and the fixed assessment/learner-to-label shortcuts; archive/proof regenerated | [2a1ff3e](https://github.com/rahulsharma027/yottaflex-round-3-assignment/commit/2a1ff3e7d461ac7de20e9bd335bd2d23877eb3f0) |

## Prepare a separate current dataset

Use the latest `main` and Python 3.12–3.14. First setup needs internet to install the pinned dependencies. From the repository directory, start a separate review workspace to preserve earlier edits and load generator revision 2. In PowerShell:

```powershell
$env:YOTTA_LOCAL_DIR = ".local/manual-review-v2"
python run.py
```

On macOS/Linux: `YOTTA_LOCAL_DIR=.local/manual-review-v2 python3 run.py`. Open the printed URL and use the generated passwords for this workspace. Credentials are also saved in `.local/manual-review-v2/demo-accounts.json`. Existing directories retain their data, so choose an unused workspace name for a fresh review. All examples below create or update fictional records in the selected workspace.

Sign out between roles. Each account establishes an actual authorized server session. Keep the submission/case IDs created during the checks, and reload the case after role changes. To return to the original default workspace later, stop the app and remove the environment override; in PowerShell use `Remove-Item Env:YOTTA_LOCAL_DIR`.

On the login page, **Your first sign-in** recommends `academic-admin`. Use the username shortcut and copy the matching generated password from the terminal. The expandable password help identifies the credentials file, the `academic-admin` key and the non-destructive reprint command. For the custom workspace above, use `.local/manual-review-v2/demo-accounts.json`. Expand **Want to try a different role?** for role descriptions and other username shortcuts. After signing in, the administrator can open **Explore demo cases** for a guided tour.

1. As `academic-admin`, inspect queue counts, Needs review, search, sorting and pagination. Click the four summary cards: each filters and smoothly moves to the queue. Open a case; Back to case queue preserves context. Login help, navy navigation and light content surfaces are shared across roles.
2. Select Explore demo cases: 000001 clears attributed quotation; 000002 explains shared templates; 000003 has two reviewers; 000004 retains an original finding and a successful independent appeal.
3. Open Data & validation: inspect baseline findings, separate deliberately invalid fixtures, actual execution timestamp and matching file checksums.

## A new case from start to appeal

Reviewer accounts initially show **Assigned to me**, newest opened cases first. Select **All cases** above the status tabs for the wider authorized workspace; select **Assigned to me** to return. These scope controls apply immediately. **All statuses** clears only the status filter. Click a summary card to filter and move smoothly down to the queue; tabs, search and pagination retain the selected assignment scope. Opening a case and using Back to case queue preserves those choices.

Only reviewers, including appeal reviewers, see the assignment switch. Administrators and support start with all authorized cases; learners have their own cases without assignment controls.

In the case file, read Student details → Submitted work → Evidence → Response → Decisions → Timeline. The section bar and Case actions link avoid scrolling through the entire file to find a specific part.

1. As `learner`, create a submission with raw 75, quote 10 and template 5. Adjusted score is 60%. A flag appears; no automatic case or misconduct decision.
2. As `academic-admin`, find that submission in Flag triage. Inspect the report; open a formal case with a meaningful reason. Save the case ID.
3. Assign Dr. Mira Sen (`reviewer`). Record an in-app learner notice; this sends no email.
4. As `learner`, open your new case, respond and add an evidence title, excerpt and source identifier.
5. As `reviewer`, select evidence and record a reasoned decision. To explore an appeal, choose Misconduct substantiated for the fictional example.
6. As `learner`, submit an appeal and add new dated attribution evidence. Earlier records remain visible.
7. As `academic-admin`, assign Dr. Leena Rao (`appeal-reviewer`). Reusing Dr. Mira Sen must be rejected.
8. As `appeal-reviewer`, consider the evidence and record No misconduct found with a rationale. Case closes, appeal is overturned, and both findings remain.

## Completed audit fixes: manual checks

### F1 — response from a learner without a login

The ten demo accounts remain the primary role walkthrough. Use a new case for **LRN-00002**, who has no portal login:

1. As `academic-admin`, choose **New submission**, select the learner whose ID is **LRN-00002**, select an assessment, and provide a title and fictional submission text. Use raw **75**, quoted **10**, template **5**; adjusted overlap should be **60%**.
2. On the report, choose **Open a formal case**, enter a meaningful reason, and press **Record triage**. Save the returned case ID.
3. In **Case actions**, assign Dr. Mira Sen (`reviewer`) and record learner notice. Add a staff evidence item with a title, excerpt and source reference so the reviewer has evidence to consider.
4. As `reviewer`, open that case and attempt **No misconduct found** with evidence selected and a rationale. **Expected:** the decision is rejected because a learner response is still required; no finding is saved.
5. As `support`, open the same case and choose **Case actions → Record received learner response**. Enter, for example, `My dated bibliography attributes the quoted passage. Please consider my original source notes.` Use source reference `Signed learner statement REF-002`. Press **Record learner response**.
6. Inspect **Response** and **Timeline**. **Expected:** the full response and source are visible, the recorder is `support`, and the recorded timestamp is present. The learner is identified by ID; staff capture is clearly labelled as external.
7. As `reviewer`, select the evidence and record a reasoned finding again. **Expected:** the decision now succeeds. As `academic-admin`, the decided case can be closed with a reason.

Boundary check: staff capture appears only after notice in an open case for an unlinked learner. For **LRN-00001**, the linked `learner` account submits its own response. The available learner account cannot access LRN-00002's case. These actions record local synthetic correspondence; the app does not send or fetch email.

### F2 — evidence ownership and retained revisions

Use a second new case for **LRN-00001**, which belongs to the `learner` login. Complete this check before recording its decision:

1. As `learner`, create a new fictional submission using the same scores as above. As `academic-admin`, open its case, assign Dr. Mira Sen, record notice, and add evidence titled **Staff source comparison**. Save the case ID.
2. As `learner`, open that case, submit a response, and expand **Add evidence or a new version**.
3. Inspect **Revise existing evidence**. **Expected:** it initially offers **Add as separate evidence**; the staff comparison is not offered as a replacement target.
4. Add **My dated draft** as separate evidence with a source reference. Reopen the form. **Expected:** your own current item is now available for revision, while the staff comparison remains protected.
5. Select your item, submit **My corrected draft** with revised text/reference, and inspect the case and timeline. **Expected:** the original and corrected drafts are retained with authorship; the selector offers the corrected version as the current item. The staff source still exists.
6. As `reviewer`, inspect the decision form. **Expected:** the staff source and latest learner draft are selectable; the superseded draft is excluded. After selecting current evidence and providing a rationale, a decision can succeed.

Staff correction choices include current staff and learner evidence under the documented staff permissions. Learner forged-replacement attempts, rollback and client-supplied authorship are additionally covered by the automated regression tests; normal UI inspection alone does not prove those server-side checks.

### F3 — temporal information and dataset distribution

1. As `academic-admin`, open **Explore demo cases → An independent appeal**, case **INT-2026-000004**. Read **Submitted work**. **Expected:** it contains academic text; the separate Decisions/Timeline sections retain the later original finding, attribution evidence and appeal resolution.
2. Confirm the dated bibliography evidence is later than the original decision and earlier than the appeal decision. The original finding references only evidence available at that time.
3. Open **Data & validation**. **Expected for the packaged baseline:** 10,000 submissions, 300 cases from 1,000 flags, zero baseline findings, four detected isolated exceptions, and matched repeatability checks. These packaged counts remain separate from cases created during this manual walkthrough.
4. In the repository, open `data/verification.json` and inspect `scenario_distribution.by_assessment`. **Expected:** each of the five assessments has positive counts for all five families. `learners_with_both_outcomes` is **1342** of **2000** for the default full seed.
5. Extract `data/full-dataset.zip`. **Expected:** `manifest.json` reports `generator_version: 2`; operational CSV/JSON/SQL, separate truth files and four negative fixtures are present. The default data has 2,000 examples of each scenario family. Assessment ID no longer uniquely determines misconduct truth.

Optional repeatability check from the repository directory, using Python 3.12–3.14:

```powershell
python scripts/verify_dataset.py --output artifacts/manual-review-proof
```

**Expected:** passed is true, baseline_errors is 0, true_positive is 4, false_positive/false_negative are 0, and checksums_match is true. This writes ignored proof output and preserves the packaged report and live database. The latest automated suite has **46 passing tests**; runtime/export checks were performed on Python 3.12 and 3.14. These synthetic checks do not establish real-world detection accuracy or resolve the open F4 chronology-validator gap.

### Authorization and lifecycle checks

- Dr. Evan Cole cannot review LRN-00001: recorded supervisor conflict.
- An unassigned administrator cannot author a decision, including through a forged request.
- Decisions need evidence, rationale, notice and response.
- Late evidence requires an open appeal; pending appeals cannot close administratively.
- All original reviewers, including reassigned ones, are excluded from appeal review.
- A second action from a stale tab is rejected without a partial event.
- Learners cannot access another learner's case or evaluation outputs.

Tests exercise these controls in an isolated database. Keep your walkthrough data by avoiding reset.
