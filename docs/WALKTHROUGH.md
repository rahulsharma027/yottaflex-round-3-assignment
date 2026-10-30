# Reviewer walkthrough

Start `python run.py`, open its URL, and use its generated passwords. Sign out between roles; every account establishes an actual authorized server session.

On the login page, **Your first sign-in** recommends `academic-admin`. Use the username shortcut and copy the matching generated password from the terminal. The expandable password help identifies `.local/demo-accounts.json`, the `academic-admin` key and the non-destructive reprint command. Expand **Want to try a different role?** for role descriptions and other username shortcuts. After signing in, the administrator can open **Explore demo cases** for a guided tour.

1. As `academic-admin`, inspect queue counts, Needs review, search, sorting and pagination. Open a case; Back to case queue preserves context.
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

## Blocked-action checks

### Learners without a portal login

The ten demo accounts remain the primary role walkthrough. Other generated learners can respond through received correspondence without being given additional logins:

1. As administrator, open a case for that learner, assign an eligible reviewer and record notice.
2. As administrator or support, choose **Case actions → Record received learner response**. This action appears for a learner without a linked login after notice in an open review or appeal.
3. Enter the received learner response and an identifiable source reference, such as a signed-statement reference. Save it. The portal records the staff account as the recorder; it does not impersonate a learner or send/fetch email.
4. Inspect **Response** and **Timeline** for the recorder, timestamp, source and preserved text. An assigned reviewer can now consider the response and evidence when deciding.

Staff cannot use this route for learners who have linked portal accounts. Those learners submit through their own session. Responses must be supplied deliberately; the app never invents one to unblock a case.

### Authorization and lifecycle checks

- Dr. Evan Cole cannot review LRN-00001: recorded supervisor conflict.
- An unassigned administrator cannot author a decision, including through a forged request.
- Decisions need evidence, rationale, notice and response.
- Late evidence requires an open appeal; pending appeals cannot close administratively.
- All original reviewers, including reassigned ones, are excluded from appeal review.
- A second action from a stale tab is rejected without a partial event.
- Learners cannot access another learner's case or evaluation outputs.

Tests exercise these controls in an isolated database. Keep your walkthrough data by avoiding reset.
