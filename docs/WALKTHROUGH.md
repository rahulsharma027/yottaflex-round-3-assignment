# Reviewer walkthrough

Start `python run.py`, open its URL, and use its generated passwords. Sign out between roles; every account establishes an actual authorized server session.

On the login page, **Your first sign-in** recommends `academic-admin`. Use the username shortcut and copy the matching generated password from the terminal. The expandable password help identifies `.local/demo-accounts.json`, the `academic-admin` key and the non-destructive reprint command. Expand **Want to try a different role?** for role descriptions and other username shortcuts. After signing in, the administrator can open **Explore demo cases** for a guided tour.

1. As `academic-admin`, inspect queue counts, Needs review, search, sorting and pagination. Open a case; Back to case queue preserves context.
2. Select Explore demo cases: 000001 clears attributed quotation; 000002 explains shared templates; 000003 has two reviewers; 000004 retains an original finding and a successful independent appeal.
3. Open Data & validation: inspect baseline findings, separate deliberately invalid fixtures, actual execution timestamp and matching file checksums.

## A new case from start to appeal

1. As `learner`, create a submission with raw 75, quote 10 and template 5. Adjusted score is 60%. A flag appears; no automatic case or misconduct decision.
2. As `academic-admin`, find that submission in Flag triage. Inspect the report; open a formal case with a meaningful reason. Save the case ID.
3. Assign Dr. Mira Sen (`reviewer`). Record an in-app learner notice; this sends no email.
4. As `learner`, open your new case, respond and add an evidence title, excerpt and source identifier.
5. As `reviewer`, select evidence and record a reasoned decision. To explore an appeal, choose Misconduct substantiated for the fictional example.
6. As `learner`, submit an appeal and add new dated attribution evidence. Earlier records remain visible.
7. As `academic-admin`, assign Dr. Leena Rao (`appeal-reviewer`). Reusing Dr. Mira Sen must be rejected.
8. As `appeal-reviewer`, consider the evidence and record No misconduct found with a rationale. Case closes, appeal is overturned, and both findings remain.

## Blocked-action checks

- Dr. Evan Cole cannot review LRN-00001: recorded supervisor conflict.
- An unassigned administrator cannot author a decision, including through a forged request.
- Decisions need evidence, rationale, notice and response.
- Late evidence requires an open appeal; pending appeals cannot close administratively.
- All original reviewers, including reassigned ones, are excluded from appeal review.
- A second action from a stale tab is rejected without a partial event.
- Learners cannot access another learner's case or evaluation outputs.

Tests exercise these controls in an isolated database. Keep your walkthrough data by avoiding reset.
