# Actual verification — 2026-10-30

Checks below were performed by the AI coding agent, not asserted as candidate personal review. All records used were synthetic. No production or portal action was taken.

## Automated and data checks

| Check | Observed result |
|---|---|
| Django `manage.py check` | No issues |
| `manage.py makemigrations --check --dry-run` | No model/migration drift |
| `manage.py test` on Python 3.15.1 / Windows | 26 tests passed, 1.239 seconds (test-body time) |
| Same tests on Python 3.14.10 / Windows | 26 tests passed, 1.352 seconds |
| Full generator volumes | 10,000 submissions, 1,000 flags, 300 cases |
| Full baseline validation | Zero unexpected findings |
| Isolated invalid fixtures | Four correct fixture/type detections, zero false positives/false negatives |
| Two independent full export runs | All counts and per-file SHA-256 match |
| Python 3.14 / 3.15 export comparison | All exported file hashes also match between these tested runtimes |
| SQL round-trip | Starter SQL imports into empty SQLite; counts correct, foreign_key_check empty |

The suite covers full review → original decision → independent successful appeal → closure; conflict/inactive-account rejection; original/ended-assignment appeal independence; missing evidence/rationale/notice/response; cross-case evidence; append-only versions; late evidence; unauthorized/stale/duplicate requests; submission receipts; learner ownership; CSRF; escaping; return URL validation; page rendering and form preservation. Dataset tests mutate IDs, foreign keys, arithmetic, enums, lifecycle and malformed dates/types.

Recorded full proof is in [../data/verification.json](../data/verification.json); supported-runtime proof is [../data/python314-verification.json](../data/python314-verification.json). Runtime 3.14 was the official portable Windows distribution, extracted into ignored `.tools`, reusing the four pure-Python dependency pins. Its SHA-256 matched the [official release listing](https://www.python.org/downloads/release/python-31410/): `90905e64a840557d8c1bc4f5b74db3d7ee85e3ffb217611cac1c7813acea4159`. It did not replace system Python. Portable-runtime testing is distinct from testing a normal Python installation's venv/bootstrap route.

## Launcher and reviewer setup

Environment: Windows / PowerShell, host CPython 3.15.1, Django 5.2.18. Source snapshot from local commit `23065c6`, current README copied beside it; no inherited database/config/venv, and no parent-directory source imports. Archive extraction is a clean-source test, not a claim that unpushed code was cloned from GitHub.

| Check | Observed result |
|---|---|
| `python run.py --setup-only` in clean source snapshot | Exit 0; created environment/config/accounts, migrated and seeded full dataset; **19.92 s** |
| Second setup after adding a synthetic submission | Exit 0; **1.79 s**; 10,001 submissions, one seed marker, new record retained, passwords unchanged |
| `python run.py --port 8002` in that workspace | Printed local URL; login HTTP 200 with expected page |
| Occupied port 8001 | Clear error and suggested port 8002 before setup writes |
| `--reset-demo` without confirmation | Refused, explicit required confirmation flag |
| Explicit confirmed reset in disposable verification workspace | Exit 0; starter counts 100/10/3, previous synthetic edit removed, credentials rotated, signing secret retained |

Times include local process/setup overhead and **cached dependency downloads**. They do not predict a cold internet connection's setup time. Raw setup logs contain generated passwords and remain in ignored artifacts, not this public repository. Python 3.15 is experimental under the chosen Django pin; recommended reviewer versions remain 3.12–3.14.

Final packaging check: cloned the completed local repository at `9980067` using `git clone --no-hardlinks` into a new ignored verification directory. Its one-command setup (`run.py --setup-only`) passed in **19.83 s** on the same host, with all documentation/source present, ten generated accounts, all six active reviewers linked to accounts, exact full counts, and 650 audited triage actions. This was a real local Git clone; the public remote still has not received these commits. The agent-created working demo was refreshed to the same final schema/accounts after its initial database was backed up under ignored artifacts. Owned preview servers were stopped after verification.

Initial sandbox attempts could not use network/socket access and could not clean a Windows temporary test directory. Retried with approved permissions; the successful results above come from those completed runs. An initial browser attempt occurred before the server was ready; the working preview used port 8001. No failed attempt is counted as a successful check.

## Browser and interface verification

Actual in-app Chromium browser inspection:

- Signed in using the generated administrator account; inspected queue counts/statuses.
- Desktop workspace at 1440 × 1000; phone at 375 × 812; tablet case at 768 × 1024.
- Phone menu toggles with aria-expanded; queue becomes readable case cards. Wider tables retain their own scroll region. Browser viewport override was reset afterward.
- Inspected the successful-appeal case: original finding, late evidence and independent overturned decision all visible.
- Searched for case 000003; one result. Opened it and returned with query/sort retained; reset restored all cases.
- Submitted an already-assigned reviewer; server rejected it, preserved the reason/reviewer choice, focused the error, and added no partial domain change.
- Inspected real form labels, semantic controls, focus styles, text status labels, local assets and reduced-motion CSS. This is a bounded accessibility inspection, not a full WCAG certification or screen-reader audit.

Screenshots: [desktop workspace](screenshots/workspace-desktop.png), [phone queue](screenshots/workspace-phone.png), [phone case](screenshots/case-phone.png), [tablet case](screenshots/case-tablet.png), [preserved validation error](screenshots/assignment-validation.png).

Interface-polish review scope: Django templates/plain CSS, primary queue/case flow. Typography was enlarged after desktop inspection; mobile navigation and cards replaced the initial overly tall menu/table view. Structural borders and restrained surfaces are shared; icons use currentColor; no entrance animation or motion library is used; transitions name specific properties. Rejected extra animation and a second CSS framework because they add distraction/setup without improving these tasks. Unverified: complete hover/focus matrix for every secondary page and full assistive-technology testing; therefore no unrestricted accessibility/polish approval claim.

## Public repository and remaining checks

Unauthenticated read-only HTTPS request to the configured GitHub repository returned **200**, its expected repository title, and a **Public** label. This verifies existing public access without an authenticated GitHub session. The new implementation is committed locally; it has not been pushed or submitted through the portal in this task.

Still unverified: normal-install bootstrap on Python 3.12/3.13/3.14; macOS/Linux startup; literal network-disconnected workflow (assets/code have no external runtime dependencies, but no network adapter was disabled); dependency-install failure recovery by forced outage; missing-Python/version error simulation; sustained concurrent load; complete browser walkthrough using every role; candidate personal review; complete prompt export reconciliation; final comparison with absent source attachments; remote publication and portal submission.

## Branding follow-up

Renamed to **ACI (Academic Integrity) Portal By Yotta** at the user's request. `manage.py check` and the existing `test_all_pages_render_and_search_pagination_preserve_context` check passed on Python 3.14.10. Browser login/tab title and workspace branding were verified at desktop 1440×1000 and phone 375×812. Updated the desktop screenshot and added [phone branding](screenshots/branding-phone.png). Other original workflow screenshots retain their historical branding. No new schema or dataset changes were required.

## First-run sign-in guide follow-up

Django system check and all 20 existing workflow tests passed on Python 3.14.10 (0.619 s test-body time). An unauthenticated login response returned 200 with administrator/password/role guidance; comparing the HTML with generated local passwords found no exposed passwords. An authenticated test client visiting login received a 302 to the workspace. Login HTML no longer automatically focuses a field, keeping the guide visible first on phones.

Actual browser checks: administrator username shortcut followed by successful password sign-in; failed sign-in keeps the guide visible and focuses its error; role shortcuts update account guidance, focus the password field and clear a previous account’s password; password-file/reprint instructions and role descriptions expand; signed-in navigation to login returns to the workspace. Inspected desktop 1440×1000 and phone 375×812. Screenshots: [desktop sign-in guide](screenshots/login-guide-desktop.png), [phone sign-in guide](screenshots/login-guide-phone.png). No fresh dataset generation was needed for this interface/auth-form change.

## Reviewer queue and case-file follow-up

All 30 tests passed on Python 3.14.10 in 1.619 s test-body time. Four added checks cover reviewer defaults/newest dates, exclusion of ended/unassigned cases, explicit All cases with status/search/sort, actor access boundaries and escaped original submission/student details. Django system and migration-drift checks passed; JavaScript syntax passed node --check. Node is a development check, not a reviewer runtime requirement. A sandbox temporary-export restriction affected an initial suite attempt; the approved full rerun above passed.

Actual browser inspection used an existing local synthetic workspace without reseeding or changing cases. Original reviewer sign-in defaulted to Assigned to me / Newest first. All four summary cards updated the queue and live result announcement, kept the assignment scope, and visibly scrolled down; the selected card/tab changed. Back/Forward restored filters. Switching to All cases, case-ID search, Reset, page 2, and returning from a case retained the expected URL state/queue anchor. Case files exposed student facts, complete submitted text and chronological events; section links reached submission and timeline. No browser console errors were observed.

Inspected desktop 1440×1000, phone 375×812 and tablet 768×1024. Native smooth scroll was observed at normal speed; 10%-speed replay and actual OS reduced-motion preference switching were not performed. Reduced-motion behavior is explicit in JavaScript/CSS. Normal GET fallbacks are present; browser JavaScript was not disabled during this inspection.

Screenshots: reviewer-workspace-desktop.png, reviewer-queue-phone.png, case-file-structured-desktop.png, case-file-structured-phone.png, case-file-structured-tablet.png and case-submission-desktop.png under docs/screenshots. Counts in these screenshots reflect the live selected scope and may differ from the packaged baseline after reviewer changes. No dataset-generation/export artifacts changed.

The independent appeal reviewer was also checked in the browser: its own Assigned to me scope loaded, the zero Awaiting review count led to a recoverable empty queue, and Open appeals restored its assigned appeal list. All these interactions were read-only apart from normal sign-in/session updates.
